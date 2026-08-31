# P1：关键缓存设计与读取边界

> **证据等级：代码核对已确认（更新至 2026-08-31）。** 本页记录 P1 Redis 中对跨服务设计、实时展示和任务编排重要的缓存；它们是共享运行时快照，不替代数据库、P2 设备主数据或设备协议的最终事实。

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

## 4. 任务缓存：DRONE/DOCK 与 CAMERA 分域维护

`wayline_task` 是两类任务共同的持久化事实表，但运行态缓存按设备类型分域：机场/无人机飞行任务使用按机场组织的单任务快照；CAMERA 固定点位巡检使用按项目和相机设备组织的任务集合。两者不能仅因 `EnumTaskType` 同属任务表而互相替代。

### 4.1 DRONE/DOCK：运行中的航线或手动飞行任务

| 项目 | 设计 |
| --- | --- |
| Key | `wayline_task_running:{dockId}` |
| 值 | `WaylineTaskDTO` |
| 写入 | 普通航线任务开始、暂停、恢复；一键起飞创建的手动飞行任务；DRC 控制、任务进度与部分 IoT 命令路径 |
| 读取 | 任务指令、OSD 落库关联、任务状态与监控逻辑 |
| 清理 | 显式删除；任务终态可标记 `ending` 后短暂保留再过期 |

该缓存按**机场设备 ID**而非飞机 SN 组织。同一机场 key 同时承载不同任务类型的运行态，必须以 DTO 的 `taskType` 区分，不能仅凭 key 名或 `actionType` 判断任务类别。`WaylineRedisServiceImpl#setRunningTask` 只用新 DTO 中的非空字段覆盖旧值，避免进度、航程、动作类型等分批事件相互覆盖。

#### ID 语义排查提示：`dockId` 不是可靠的数据语义

`WaylineTaskEntity.dockId` 是 Java 历史属性名，物理列实际为 `wayline_task.device_id`；**不得仅因属性名为 `dockId`，就推断该列或所有调用方保存的是机场 ID**。应以每条写入链路和 Redis Key 构造点为准：

| 场景 | 任务表 `device_id` | 运行缓存 Key / DTO `dockId` | 结论 |
| --- | --- | --- | --- |
| 普通航线 | 当前任务执行机场维度 | 机场设备 ID | 表字段和缓存通常同维度。 |
| 手动一键起飞 | 创建时从机场子设备中解析 UAV，写入 UAV 设备 ID | 同一创建方法以传入机场 ID 写 `wayline_task_running:{dockId}`，DTO 也写机场 ID | 表字段与运行缓存**刻意不是同一 ID**。 |

因此，排查“空间设备是否命中手动任务”时，必须先回答“当前校验读的是任务表还是运行缓存”。项目移除校验读缓存时，空间资源集合必须包含机场 ID；如果空间仅关联 UAV，即使 `wayline_task.device_id` 能命中 UAV，也不会命中机场维度缓存。本页不把该数据关联缺口自动修正为父子设备转换；需通过 P7 空间资源关联数据做集成验证。

### `taskType`：运行任务类别

| `taskType` | `EnumTaskType` | 枚举名称 | 当前写入/使用边界 |
| --- | --- | --- | --- |
| `1` | `NORMAL` | 飞行巡检 | 普通航线任务。`TaskCommandExecStart` 将任务表中的类型写入运行缓存；设备列表的运行任务快照只展示该类型。 |
| `2` | `MANUAL` | 手动飞行任务 | 一键起飞 `POST /drone/control/actions/takeoffToPoint` 成功下发后，`InspectionIotCommandGatewayImpl#createManualFlightTask` 创建 `wayline_task` 并写入该类型的运行缓存。它不是普通航线任务；暂停时的可恢复语义也由该类型单独处理。 |
| `3` | `FIXED_POINT_INSPECTION` | 固定点位巡检 | CAMERA 固定点位巡检任务。它**不写入**本节的 `wayline_task_running:{dockId}`；运行态见下一节的 CAMERA 专属缓存。 |

`WaylineTaskDTO.taskType` 是该缓存值的一部分，而不是 Redis key 的分片维度：一个机场在同一时刻只应有一个当前飞行运行态。读取方如果需要回源 `wayline_task`，必须同时校验 `taskId + projectId`，再按 `taskType` 选择业务处理；缺少 `taskType` 时不得擅自按普通任务解释。

适合用于“当前正在执行哪个任务、当前进度/航程/暂停状态是什么”的实时判断；不适合作为任务历史或最终业务状态唯一来源。任务终态、重试和恢复操作仍须结合任务表及业务状态核实。

### 4.2 CAMERA：固定点位巡检的设备任务集合与展示快照

固定点位巡检（`taskType=3`）可同时关联多个 CAMERA 通道，不能用“每个机场一个 DTO”的 `wayline_task_running:{dockId}` 表达。当前实现使用以下 Redis 状态：

| Key | 类型/范围 | 值与用途 | 写入与清理 |
| --- | --- | --- | --- |
| `fixed_point_device_running_tasks:{projectId}:{deviceId}` | Set；单个 CAMERA 的作业中任务集合 | 成员为 `taskId:projectId`；用于判定 CAMERA 是否作业中、计算运行任务数。允许同一 CAMERA 存在多个作业中任务。 | 固定点位任务至少一个关联通道启动成功后写入；任务完成、终止或启动失败时移除成员，集合为空后删除 key。读写受设备维度锁 `fixed_point_device_running_lock:{projectId}:{deviceId}` 串行保护。 |
| `monitor:device_task_status:{projectId}:{deviceSn}` | 带 3 天 TTL 的监控展示快照 | `CameraTaskStatusPushDTO`；供 `/drone/monitor/v2/list` 的 CAMERA 卡片 `taskInfo` 首次加载，以及 `device_task_status` WebSocket 推送复用。 | `CameraTaskStatusNotifier` 在固定点位任务创建、启动、结束、终止时回源任务表计算并回写；缓存缺失或项目不匹配时，`/v2/list` 批量回源后重建。 |
| `fixed_point_task_timed_finish` | Sorted Set；固定点位任务自动结束队列 | 成员为 `taskId + projectId`，score 为计划结束时间。 | 创建后事务提交写入；完成、终止或启动失败时移除；停止会话失败时按 5 秒延后重入队列。它是调度状态，不是 CAMERA 卡片任务详情来源。 |

`POST /drone/monitor/v2/list` 的 CAMERA 分支先查询 `manage_device` 投影，再按项目和 CAMERA `deviceSn` 读取 `monitor:device_task_status:{projectId}:{deviceSn}`。命中有效 `CameraTaskStatusPushDTO` 直接填充 `taskInfo`；未命中时由 `CameraTaskStatusNotifier#resolveAndCacheBatch` 批量查询固定点位任务表及关联通道后回填。运行中判断还会读取 `fixed_point_device_running_tasks:{projectId}:{deviceId}`，因此 CAMERA 的任务状态不能从机场任务缓存或无人机 OSD 推断。

**两类设备任务缓存的选择：**

| 设备/任务场景 | 首选运行态 | 展示快照 | 不应使用 |
| --- | --- | --- | --- |
| DOCK/DRONE 的普通航线任务或一键起飞手动飞行 | `wayline_task_running:{dockId}` | `monitor:device_task_status:{projectId}:{droneSn}` | CAMERA 固定点位设备集合 |
| CAMERA 的固定点位巡检 | `fixed_point_device_running_tasks:{projectId}:{deviceId}` | `monitor:device_task_status:{projectId}:{cameraSn}` | `wayline_task_running:{dockId}`、无人机 OSD |

两类展示快照共用 `monitor:device_task_status:{projectId}:{deviceSn}` 前缀，但值类型不同：DRONE 为 `DeviceTaskStatusPushDTO`，CAMERA 为 `CameraTaskStatusPushDTO`。读取方必须按设备类别和实际 DTO 类型校验，不能把同名 key 视为可互换的载荷。

### 4.3 项目/项目集移除：运行任务的专用缓存口径

项目、项目集整体移除，以及项目或项目集编辑时移除空间，均先由 P7 空间资源关联按 `CASCADE` 解析设备 ID，再由 P1 读取本节两类运行态缓存。该场景的 `blockedTaskCount` / `runningTaskCount` 表示**运行中任务数（按运行缓存统计）**，不是“命中设备数”，也不回查 `wayline_task` 的 `IN_PROGRESS` / `SUSPEND` 状态。

| 来源 | 计数规则 | 去重边界 |
| --- | --- | --- |
| 普通/手动飞行 | 每个非空 `wayline_task_running:{dockId}` 缓存计一个任务；缓存内 `projectId` 优先确定归属，缺失时才按该设备所属项目空间归属。 | 一台设备同一时刻只维护一个当前飞行缓存，因此按设备命中数等价于按任务数。 |
| CAMERA 固定点位 | 读取本次涉及全部 `fixed_point_device_running_tasks:{projectId}:{deviceId}` Set 的成员，按 `taskId:projectId` 做并集后计数。 | 同一个固定点位任务跨多个 CAMERA 或多个通道出现时仅计一次；不同任务成员分别计数。 |

空间预检以“该空间解析出的设备集合”为边界独立计算；同一任务关联多个待移除空间时，每个空间都可被判定为阻断，但单个空间内部仍按上述规则去重。项目/项目集整体移除则按项目汇总其全部绑定空间设备后计算。

**失败与缺失语义：** Redis 读取异常必须向上抛出，提交前复核不得更新 P7 节点或删除 P1 关系；运行缓存缺失不回查任务表，按本校验口径视为未命中。这个“只信运行缓存”的规则仅适用于项目移除阻断，不覆盖监控设备卡片等允许回源任务表的展示场景。

### 4.4 与数据库的一致性边界

> **证据等级：代码核对已确认。** 下述内容描述当前实现，不是跨存储强一致设计。

- 对 4.1 的机场运行任务缓存，`WaylineRedisServiceImpl#setRunningTask` 只在 Redis 中读取、按非空字段合并并写回 `WaylineTaskDTO`，不会自动更新 `wayline_task` 表。
- 普通任务开始、暂停、恢复等控制入口，通常先更新任务实体的业务状态，再写入机场运行任务缓存；任务进度上报会更新任务表状态/结束时间，并分别回写 Redis 的进度字段和数据库百分比。两者不是一个跨 Redis/数据库的原子事务。
- OSD 计算得到的 `distanceToGo`、`timeToGo` 等实时字段只写入机场运行任务缓存；DRC/点飞等控制场景也可能只写入缓存，因为它们不一定对应持久化的 `wayline_task`。
- 普通飞行任务进入终态后不会立即删除机场缓存：`markRunningTaskEnding` 将 `ending=true` 并设置 10 秒 TTL，供稍晚到达的设备状态完成收尾；读取侧会过滤 `ending`，并用 `taskId + projectId` 回查任务表校验任务身份和数据库状态。之后由显式删除或 TTL 清理。
- 对 4.2 的 CAMERA 固定点位缓存，运行集合和监控快照同样不是持久任务事实：`CameraTaskStatusNotifier` 在展示快照缺失时会从固定点位任务/通道表重新计算，运行集合则在任务生命周期的启动、完成和终止操作中显式维护。
- `DroneTaskStatusReconciliationTask` 仅针对 DRONE 任务快照，每 5 分钟读取 Redis 并补发设备任务状态通知，用于补偿事件丢失、服务重启或缓存残留；它不是 Redis 与数据库的全量修复机制，也不替代 CAMERA 固定点位任务的回源计算。

因此，当前一致性模型是：**数据库保存任务的持久事实，Redis 保存按机场或 CAMERA 设备维度组织的实时投影；允许短暂不一致，通过数据库回源、终态延迟清理和低频对账降低影响**。缓存缺失不能直接解释为任务结束；监控展示等场景需要回查任务表或返回状态未知。项目移除阻断是已确认的例外：它只按 4.3 的运行缓存口径判断，不做数据库兜底。若需要严格一致，仍需另行设计事务消息、可靠事件/重建机制或统一状态写入边界。

代码入口：

- [`WaylineRedisServiceImpl`](../../../../../../../../xm-new/c-drone-inspection/b-inspection-platform-core/src/main/java/com/xmkj/business/core/service/wayline/impl/WaylineRedisServiceImpl.java)
- `b-inspection-platform-common/.../EnumTaskType.java`
- [`TaskCommandExecStart`](../../../../../../../../xm-new/c-drone-inspection/b-inspection-platform-core/src/main/java/com/xmkj/business/core/controller/admin/waylineTask/taskHandler/command/TaskCommandExecStart.java)
- [`InspectionIotCommandGatewayImpl`](../../../../../../../../xm-new/c-drone-inspection/b-inspection-platform-core/src/main/java/com/xmkj/business/core/service/iot/impl/InspectionIotCommandGatewayImpl.java)（一键起飞创建手动飞行任务）
- [`ProjectManagementServiceImpl`](../../../../../../../../xm-new/c-drone-inspection/b-inspection-platform-core/src/main/java/com/xmkj/business/core/service/project/impl/ProjectManagementServiceImpl.java)（项目移除缓存统计与空间移除复核）
- `b-inspection-platform-core/.../waylineTask/impl/FixedPointInspectionServiceImpl.java`（CAMERA 固定点位任务集合、自动结束队列）
- `b-inspection-platform-core/.../monitor/CameraTaskStatusNotifier.java`、`.../monitor/impl/MonitorDeviceServiceImpl.java`（CAMERA `/drone/monitor/v2/list` 任务快照）
- [`InspectionTaskProgressBusinessServiceImpl`](../../../../../../../../xm-new/c-drone-inspection/b-inspection-platform-core/src/main/java/com/xmkj/business/core/service/iot/impl/InspectionTaskProgressBusinessServiceImpl.java)
- [`DroneTaskStatusReconciliationTask`](../../../../../../../../xm-new/c-drone-inspection/b-inspection-platform-core/src/main/java/com/xmkj/business/core/service/monitor/DroneTaskStatusReconciliationTask.java)

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
3. 新增任务控制：写入或清理 `wayline_task_running:{dockId}` 的时机必须与任务状态机一致；同时核对任务表 `device_id`、DTO 字段和 Redis Key 的实际 ID 来源，禁止根据 `dockId` 名称推断。
4. 修改项目移除阻断：普通/手动按机场运行缓存计数；固定点位必须读取 Set 成员并按 `taskId:projectId` 去重，不能累加各 CAMERA Set 的 `SCARD`。
5. 新增 DRC 能力：同时评估心跳、持久会话、序列号、参数请求和 stop 清理。
6. 子机相关异常：依次核对 `iot_topology_child_parent`、`iot_topology_children`、在线 key、普通/DRC OSD 快照。

相关上下文：[P1 关键入口地图](key-entry-points.md)、[DJI OSD 上行数据链路](../../flows/dji-osd-upstream-flow.md)、[DJI 设备指令下行链路](../../flows/dji-osd-command-flow.md)。
