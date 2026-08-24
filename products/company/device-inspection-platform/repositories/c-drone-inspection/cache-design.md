# P1：关键缓存设计与读取边界

> **证据等级：代码核对已确认。** 本页记录 P1 Redis 中对跨服务设计、实时展示和任务编排重要的缓存；它们是共享运行时快照，不替代数据库、P2 设备主数据或设备协议的最终事实。

## 设计总则

P1 的缓存不是单纯的性能优化，而是“异步设备消息 → 可直接消费的系统状态”的收口层。读取前先判断问题属于哪种状态：

- **实时设备快照、在线态、DRC 会话、运行任务：** 优先读取缓存。
- **历史记录、审计、持久化任务状态、设备档案：** 以数据库或 P2/P1 服务查询为准。
- **缓存缺失：** 不能默认设备离线或任务结束；应按场景回退到业务查询、等待上报或明确返回“状态未知”。

## 1. OSD：按设备 SN 的全局实时快照

| 项目 | 设计 |
| --- | --- |
| Key | `osd:{deviceSn}` |
| 值 | 机场 `InspectionHostTelemetryDTO` 或子机 `InspectionSubDeviceTelemetryDTO` |
| 写入 | `InspectionDeviceStatusBusinessServiceImpl#setOsd` |
| 过期 | `DEVICE_ALIVE_SECOND = 120` 秒；每次有效遥测刷新 |
| 主要读取者 | 监控状态 Resolver、航线计划/任务服务、设备控制与前端统计 |

### 为什么应优先读 OSD 缓存

机场 OSD 存在分包上报：同一设备的模式码、DRC 状态等字段可能不在同一帧。`fillHostTelemetry` 会读取旧 `osd:{dockSn}`，合并未出现但仍有效的字段后再写回，避免前端或状态计算在单帧中读到“字段闪空”。

因此，需要“当前完整度较高的设备遥测”时，应读取 `osd:{deviceSn}`，不要只使用本次 MQTT/RocketMQ 消息的 payload。典型场景包括：机场顶部状态、当前模式、子机相机/变焦参数、任务收尾判断和设备控制的运行前判断。

### 边界

- 普通 OSD 与 DRC OSD **不可混读或互相覆盖**。
- TTL 到期只代表 P1 未在窗口内收到有效遥测，不等价于设备物理故障。
- 主数据坐标仅在缺失时可被有效机场 OSD 一次性回填；OSD 不是设备档案的长期存储。

### 代码入口与 Redis 排查

普通 OSD 从 `inspection_device_status_report` 进入 `InspectionIotUpstreamConsumer`，经
`DeviceStatusPropertyHandler` 转交 `InspectionDeviceStatusBusinessServiceImpl#handle`；该服务按
机场/子机遥测分流至 `handleHostTelemetry` 或 `handleSubDeviceTelemetry`，最终由 `setOsd` 写入
`osd:{deviceSn}`。机场分包遥测会先读取旧快照后合并并回写；子机遥测直接刷新其自身快照。

在 Redis 工具或 `redis-cli` 中，可先用 `SCAN 0 MATCH osd:* COUNT 100` 查找候选 key，再对目标设备使用
`GET osd:{deviceSn}` 与 `TTL osd:{deviceSn}` 查看快照和剩余有效期。实际序列化展示格式取决于运行时 Redis
客户端配置；不要用 `KEYS osd:*` 在生产实例全量扫描。

代码证据：`b-inspection-platform-iot/.../InspectionIotUpstreamConsumer.java`、
`b-inspection-platform-iot/.../DeviceStatusPropertyHandler.java`、
`b-inspection-platform-core/.../InspectionDeviceStatusBusinessServiceImpl.java`（`setOsd`、
`handleHostTelemetry`、`handleSubDeviceTelemetry`）、
`b-inspection-platform-common/.../RedisConst.java`（`OSD_PREFIX`、`DEVICE_ALIVE_SECOND`）。

## 2. DRC OSD：独立的高频快照

| 项目 | 设计 |
| --- | --- |
| Key | `drc_osd:{droneSn}` |
| 值 | `InspectionDrcOsdTelemetryDTO` |
| 写入 | `InspectionDeviceStatusBusinessServiceImpl#setDrcOsd` |
| 过期 | 120 秒，与设备存活窗口一致 |
| 用途 | 高频位置、姿态、视锥与 DRC 前端推送 |

普通 OSD 驱动任务、业务状态和常规展示；DRC OSD 服务低延迟操控视图。涉及视锥、摇杆或 DRC 页面时优先读 `drc_osd:{droneSn}`；涉及任务状态或普通设备状态时优先读 `osd:{deviceSn}`。

## 3. 在线状态：短 TTL 存活信号

| 项目 | 设计 |
| --- | --- |
| Key | `online:{deviceSn}` |
| 值 | `online` |
| 写入/刷新 | OSD 遥测、拓扑子设备上报、P2 的在线业务事件 |
| 删除 | P2 离线事件或拓扑子设备离线处理 |
| 过期 | 120 秒 |

这是“近期存在有效活动”的快速判断，用于监控和 OSD 状态 Resolver。它必须与 OSD 快照结合：在线 key 存在但 OSD 缓存缺失时，不能伪造遥测；OSD 存在但在线 key 已失效时，应按在线策略而不是只展示旧 OSD 判断设备可控性。

## 4. 运行中的航线任务：按机场维度的工作态

| 项目 | 设计 |
| --- | --- |
| Key | `wayline_task_running:{dockId}` |
| 值 | `WaylineTaskDTO` |
| 写入 | 任务开始/暂停/恢复、DRC 手动飞行、任务进度与部分 IoT 命令路径 |
| 读取 | 任务指令、OSD 落库关联、任务状态与监控逻辑 |
| 清理 | 显式删除；任务终态可标记 `ending` 后短暂保留再过期 |

该缓存按**机场设备 ID**而非飞机 SN 组织。`WaylineRedisServiceImpl#setRunningTask` 只用新 DTO 中的非空字段覆盖旧值，避免进度、航程、动作类型等分批事件相互覆盖。

适合用于“当前正在执行哪个任务、当前进度/航程/暂停状态是什么”的实时判断；不适合作为任务历史或最终业务状态唯一来源。任务终态、重试和恢复操作仍须结合任务表及业务状态核实。

## 5. DRC 会话与命令序列：控制面临时状态

| Key | 用途 | 生命周期 |
| --- | --- | --- |
| `drc_beat:{deviceId}` | DRC 活跃/自动会话保活标识 | 50 秒 TTL，心跳刷新 |
| `drc_osd_session:{deviceId}` | 显式开启的高频 OSD 持久会话 | 显式 stop 时删除 |
| `drc_seq:{deviceId}` | DRC 下行序列号 | 会话初始化为 0，停止时清理 |
| `drc_req:{deviceId}` | DRC 参数/请求关联状态 | 停止或重置时清理 |

DRC 控制设计必须把这些 key 视为一个会话整体：自动会话依赖短 TTL；显式 OSD 会话可持续维护；`stopDrcSession` 负责统一清理。不要只删除心跳 key 而保留序列、请求或持久会话标记。

## 6. 拓扑、负载与链路辅助缓存

| Key | 用途 | 设计提示 |
| --- | --- | --- |
| `iot_topology_children:{dockSn}` | 机场 → 子设备列表 | `update_topo` 建立；子机定位、离线处理和设备上下文依赖它 |
| `iot_topology_child_parent:{droneSn}` | 子机 → 父机场反向索引 | OSD 未带完整父设备信息时用于快速归属 |
| `device_psdk_index:{dockId}` | 机场挂载的喊话器、探照灯等索引 | 命令 Gateway 优先读取，缺失时才回退设备配置 |
| `payload_property:{dockSn}` | 相机/负载变焦等实时属性 | OSD 更新后供控制接口和前端读取 |
| `wireless_link:{deviceSn}` | 图传链路质量与模式 | 60 秒 TTL；写入时用短锁和旧值比较抑制重复 WebSocket 推送 |

拓扑缓存不是一次性初始化数据：P4/P3 的 `update_topo` 是其重建来源。涉及子机 OSD、指令目标 SN 或设备下线问题时，应先检查拓扑缓存是否已刷新。

## 接入与排障清单

1. 新增 OSD 字段：确认它是否分包；若会分包，应明确合并策略并更新完整快照，而非只消费单帧。
2. 新增实时页面/接口：选择正确快照（普通 OSD 或 DRC OSD），并处理缓存缺失、TTL 过期和字段未上报。
3. 新增任务控制：写入或清理 `wayline_task_running:{dockId}` 的时机必须与任务状态机一致。
4. 新增 DRC 能力：同时评估心跳、持久会话、序列号、参数请求和 stop 清理。
5. 子机相关异常：依次核对 `iot_topology_child_parent`、`iot_topology_children`、在线 key、普通/DRC OSD 快照。

相关上下文：[P1 关键入口地图](key-entry-points.md)、[DJI OSD 上行数据链路](../../flows/dji-osd-upstream-flow.md)、[DJI 设备指令下行链路](../../flows/dji-osd-command-flow.md)。
