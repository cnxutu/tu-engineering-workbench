# P1 监控设备地理位置

> **证据等级：代码核对已确认（2026-09-07）。** 本页记录 P1 `c-drone-inspection` 当前的监控设备位置契约、来源优先级和缓存边界；运行时数据、接口契约和代码以 P1 当前版本为准。

## 范围与入口

监控设备位置有两个 HTTP 查询入口和一个 WebSocket 派生字段；三者服务于不同的展示场景。

| 入口 | 返回模型 | 设备范围 | 位置口径 |
| --- | --- | --- | --- |
| `POST /drone/monitor/v2/list` | `List<MonitorDeviceV2ListDTO>` | DOCK、DRONE、CAMERA、ROBOT_DOG 卡片 | `location` 使用统一位置解析器：实时 OSD → 最后有效 OSD（仅无人机）→ 空间登记位置。 |
| `GET /drone/monitor/v2/location/list` | `List<MonitorDeviceLocationDTO>` | 全部机场、其子无人机、摄像头 | 与 V2 卡片相同的统一位置解析器，适合前端轮询；每条记录以 `actualLocation` 返回。 |
| `/ws/drone` 的 `dock_osd`、`device_osd` | `InspectionTelemetryDTO.location` | 普通机场与普通无人机 OSD 推送 | 仅从本次 OSD 派生的有效实时坐标；不读取缓存、空间节点或最后位置，不做地址解析。DRC `device_osd` 当前不填此字段。 |

V2 列表请求在 Controller 注入当前 `projectId`；V2 位置轮询入口不在 Controller 层注入该值。HTTP 位置解析读取设备投影、空间节点和 Redis 快照，不以任务状态决定位置。

## HTTP V2 统一位置模型

`/v2/list` 与 `/v2/location/list` 均使用下列位置语义。

| 字段 | 含义 |
| --- | --- |
| `longitude` / `latitude` | 有效 WGS84 经纬度，使用 `BigDecimal`。 |
| `altitude` | OSD 高度或空间节点配置的海拔；数据源未提供时为空。 |
| `address` | 按最终坐标做天地图逆地理解析得到的展示地址；解析失败不阻断接口，字段为空。 |
| `source` | `REALTIME_OSD_LOCATION`、`LAST_REPORTED_OSD_LOCATION` 或 `REGISTERED_LOCATION`。 |
| `reportedAt` | OSD 来源的毫秒时间戳；空间登记位置为空。 |

每次请求内按“经度_纬度”去重逆地理解析；天地图工具还使用 `administrative_district:*` Redis 哈希缓存地址结果。

## WebSocket 的实时位置派生字段

`InspectionDeviceStatusBusinessServiceImpl` 在普通机场或无人机 OSD 推送前，为 `InspectionTelemetryDTO.location` 单独组装实时位置。该字段不等同于 `host` 内的原始遥测字段，也不复用 HTTP V2 的降级结果。

| 字段 | 生成条件与语义 |
| --- | --- |
| `longitude` / `latitude` | 本次 OSD 的有效 WGS84 经纬度。 |
| `altitude` | 无人机取 `elevation`，机场取 `height`；单位为米。 |
| `reportedAt` | 本次 OSD 的毫秒时间戳；缺失时整个 `location` 为 `null`。 |
| `source` | 固定为 `REALTIME_OSD_LOCATION`。 |

机场还要求 `homePositionIsValid = 1` 才派生位置。经纬度无效或上报时间缺失时，字段为 `null`。DRC 高频 OSD 虽同样发送 `device_osd`，但当前调用的推送路径未传入 `location`；前端不得把缺失字段解释为 HTTP V2 的空间或最后位置回退。

### 无人机优先级

1. 读取普通 OSD `osd:{droneSn}` 与 DRC OSD `drc_osd:{droneSn}`；坐标合法、上报时间在最近 120 秒窗口内时视为实时位置。两个实时快照同时有效时选择上报时间更新的一条。
2. 无实时位置时，读取长期保存的 `drone:last_location:{droneSn}`。该缓存只写入坐标合法的普通 OSD，保留最后一次有效坐标、海拔和 `reportedAt`，无 TTL。
3. 仍无有效位置时，按无人机 `parent_id` 找到机场设备投影，读取该机场绑定的空间节点坐标。
4. 三类来源均不可用时，V2 位置对象为 `null`。

### 机场、摄像头与其他设备

机场和摄像头先读取 `osd:{deviceSn}`；只有 `homePositionIsValid = 1`、经纬度有效且上报时间在最近 120 秒内，才作为实时位置。否则读取自身 `spaceCode` 对应空间节点配置中的经纬度和可选海拔；两类来源都不可用时，V2 位置对象为 `null`。

当前 V2 的 ROBOT_DOG 不读取 OSD，直接使用自身空间节点登记位置。新增设备类别时，应显式选择实时快照、最后位置缓存或空间登记的来源链，不要隐式套用无人机规则。

## 数据所有权与约束

| 数据 | 所有者 / 写入方 | 读取方 | 约束 |
| --- | --- | --- | --- |
| `osd:{deviceSn}` | `InspectionDeviceStatusBusinessServiceImpl` 写入普通 OSD | V2 列表、V2 位置轮询 | TTL 120 秒；只代表近期实时快照。WebSocket `location` 不读取此缓存，而是从本次普通 OSD 派生。 |
| `drc_osd:{droneSn}` | 同服务写入 DRC OSD | 无人机 V2 位置解析 | TTL 120 秒；仅无人机参与实时位置竞争。 |
| `drone:last_location:{droneSn}` | 同服务在有效普通无人机 OSD 到达时写入 | 无人机位置解析、旧列表 | 长期保留；不是设备档案，也不能被当作实时位置。 |
| `manage_device.space_code` 与父子关系 | 设备投影 | 两个 V2 HTTP 入口 | 无人机回退必须使用父机场的空间，不使用无人机自身空间。 |
| 空间节点坐标 / 海拔 | 空间标签配置，经 `TagApi#getTagByCodes` 读取 | 两个 V2 HTTP 入口 | 是登记位置；坐标缺失或越界不能伪造位置。 |

## 维护与排障边界

- V2 HTTP 的 `location`/`actualLocation` 与 WebSocket `location` 不能混为同一口径：前者可回退到最后位置或空间登记，后者仅表达本次普通 OSD 的实时位置。
- 修改无人机普通 OSD、DRC OSD 或缓存 TTL 时，必须同时验证 V2 列表、`/v2/location/list` 的实时选择及降级顺序，以及 `dock_osd`/`device_osd` 的 `location` 派生条件。
- 修改 `parent_id`、机场空间绑定或空间节点坐标时，需验证无人机的最终回退位置；无父机场或无有效空间坐标应返回空位置。
- 地址解析为展示增强：天地图或 Redis 故障只能使 `address` 为空，不能使设备列表或位置轮询失败。

## 实现入口与证据

- Controller：`b-inspection-platform-core/src/main/java/com/xmkj/business/core/controller/admin/monitor/controller/FlightMonitorController.java`
- 解析与组装：`b-inspection-platform-core/src/main/java/com/xmkj/business/core/service/monitor/impl/MonitorDeviceServiceImpl.java`
- WebSocket 位置派生：`b-inspection-platform-core/src/main/java/com/xmkj/business/core/service/iot/impl/InspectionDeviceStatusBusinessServiceImpl.java`、`b-inspection-platform-common/src/main/java/com/xmkj/business/common/iot/model/InspectionTelemetryDTO.java`
- 来源枚举与缓存常量：`b-inspection-platform-common/src/main/java/com/xmkj/business/common/enums/MonitorDeviceLocationSourceEnum.java`、`b-inspection-platform-common/src/main/java/com/xmkj/business/common/redis/RedisConst.java`
- 回归测试：`b-inspection-platform-core/src/test/java/com/xmkj/business/core/service/monitor/impl/MonitorDeviceServiceImplTest.java`、`b-inspection-platform-core/src/test/java/com/xmkj/business/core/service/monitor/impl/MonitorDeviceV2ServiceImplTest.java`
