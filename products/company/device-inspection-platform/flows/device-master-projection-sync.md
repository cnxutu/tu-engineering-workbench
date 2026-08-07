# P2 设备主数据到 P1 投影同步

> **证据等级：代码核对已确认（2026-08-07）。** 本页描述 P2 IoT 设备主数据到 P1 `manage_device` 的实时投影与日终修复；不覆盖设备在线状态、Data Rule 上行或空间绑定的具体业务操作。

## 何时读取

- 调整 P2 设备创建、更新、删除后的外部同步，或排查 P1 投影缺失、残留、分类迁出。
- 调整 P1 `manage_device` 的当前设备列表、拓扑、监控统计或空间绑定边界。
- 评估 MQ 丢失、重试、乱序与日终对账的恢复能力。

## 决策与数据边界

P2 是 IoT 设备主数据的所有者；P1 的 `manage_device` 是可供巡检业务绑定和展示的投影。`space_code` 是 P1 当前空间绑定事实，不是 P2 主数据过滤条件：

1. 实时消费和日终对账覆盖所有可投影的 `AGC` 设备，即使尚未绑定空间。
2. 当前设备查询、拓扑和监控补全只读取 `is_deleted = 0 AND space_code IS NOT NULL` 的投影；未绑定设备不进入当前展示或统计。
3. 空间绑定流程保留全量活动投影可见性，使已同步但未绑定的设备仍可被选择。历史任务、轨迹、媒体查询和任务状态写入不使用 `space_code` 过滤，以保留已发生业务事实。

## 同步链路

```text
P2 设备 create/update/delete
  -> IoTDeviceRpcApi#sendDeviceChangeEvent
  -> iot_business_event : DEVICE_CREATE | DEVICE_UPDATE | DEVICE_DELETE
  -> P1 DeviceProjection*Consumer
  -> create/update 时 IoTDeviceApi#get 回查 P2 快照
  -> DeviceProjectionRealtimeSyncService
  -> manage_device 投影

每日 02:00
  -> P1 DeviceProjectionSyncTask 完整分页读取 P2
  -> 缓存 P2 快照并记录字段差异
  -> 仅完整扫描成功时清理 P2 缺失的本地投影
```

### 实时处理语义

- 创建和更新只携带 `deviceId`、`productCode`、`platformProductCode`；P1 以 `deviceId` 回查 P2，使用 P2 快照幂等 upsert。
- 只有根分类为 `AGC` 且 P2 分类可映射到 P1 设备分类时才建立或更新投影。更新只覆盖 P2 主数据字段，保留已有 `space_code` 和 P1 扩展字段。
- 删除不依赖删除后的回查。P1 会校验消息中可选的 `platformProductCode` 与本地投影身份一致，再清空 `space_code` 并逻辑删除。
- 若实时回查为不存在，或已投影设备迁出 `AGC` / 分类不可映射，P1 记录 `P2_MISSING` 或 `UNPROJECTABLE_CATEGORY` 对账日志，并解除空间、逻辑删除。身份不匹配的删除消息只记录 `DELETE_IDENTITY_MISMATCH`，不删除本地记录。
- 消息格式错误或缺少 `deviceId` 确认消费；P2 回查或 P1 数据库处理失败抛出异常，交由 MQ 框架重试。

### 日终修复语义

`DeviceProjectionSyncTask` 每日 02:00 取得分布式锁后分页枚举 P2。扫描过程记录 P1 缺失和字段差异；对于 P2 中已不属于投影范围的已有投影，记录 `UNPROJECTABLE_CATEGORY` 并停用。

只有分页调用均成功、每页声明总数存在且已枚举完整总数时，任务才读取活动的 P2 投影（`platform_product_code IS NOT NULL`）并清理本次 P2 集合中不存在的记录，记录 `P2_MISSING`。任一页失败、缺少 `total`、提前空页或枚举数不足时，跳过遗留清理，避免把 P2 暂时不可见的数据误删。

## 可靠性与非目标

- P2 当前以同步 RocketMQ 发送主数据事件，但发送异常只记录日志并返回，且没有 outbox。因此实时链路是低延迟同步，不是零丢失或严格顺序保证；完整日终扫描提供最终修复。
- P2 事件没有版本或单设备递增序列。P1 的 create/update 回查当前快照可降低重复消息影响，但不能保证跨事件乱序时的瞬时顺序；后续需要严格顺序或更短修复窗口时，应在 P2 评估 outbox、版本号和可靠发布方案。
- 日终任务不替代人工处理 `manage_device_projection_reconcile_log` 中的身份不匹配或字段差异；它只负责投影范围内的自动失效清理。

## 联调与回归必验

1. 未绑定空间的合格 AGC 设备被投影，但不出现在当前设备列表、拓扑与监控统计；绑定后可立即展示。
2. 创建/更新保留 P1 的 `space_code` 与扩展字段；删除、P2 缺失、分类迁出均解除空间并逻辑删除。
3. 丢失删除事件后，完整日终扫描清理 P1 遗留投影；P2 分页失败或不完整时不得删除本地投影。
4. P2 回查失败触发消费重试；无效消息不造成永久阻塞；删除身份不匹配不误删。

## 代码证据

以下路径相对对应仓库根目录：

- P2 `c-iot-core/.../api/device/IoTDeviceRpcApi.java`：创建、更新、删除后的事件发起与消息身份组装。
- P2 `c-iot-core/.../mq/producer/IotBusinessEventProducer.java`：`iot_business_event` 发送及发送失败处理。
- P1 `b-inspection-platform-core/.../mq/DeviceProjection*Consumer.java`：三个 Tag 的消费入口与重试边界。
- P1 `b-inspection-platform-core/.../service/device/DeviceProjectionRealtimeSyncService.java`：实时回查、幂等投影、身份校验与失效。
- P1 `b-inspection-platform-core/.../service/device/DeviceProjectionSyncTask.java`：分页完整性判定、差异记录和遗留清理。
- P1 `b-inspection-platform-core/.../dao/device/IDeviceMapper.java`、`ManagedDeviceQueryService.java`、`MonitorDeviceServiceImpl.java`：已绑定空间的展示与统计查询边界。
