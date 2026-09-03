# P1 WebSocket 推送维护入口

> **证据等级：代码与现有专题文档核对已确认。** 本页是 P1 WebSocket 相关知识的统一导航入口；具体字段、触发条件和代码证据以各专题文档及当前仓库代码为准。

## 统一边界

P1 WebSocket 主要面向前端实时刷新和局部状态更新。消息通常通过 `IWebSocketMessageService` 发送到 `/ws/drone` 或按设备类型/设备 SN 路由；全局刷新消息一般只携带“发生变化”的信号，前端收到后重新请求 REST 接口，不能把 WebSocket 当作完整数据快照或可靠消息队列。机器狗 `robot_dog_status_snapshot` 是已确认例外：它通过 `/ws/dock` 广播完整快照，具体契约见对应专题。

任务、OSD、HMS 等设备级消息与监控统计、权限失效等业务级消息共用前端通道，但 `biz_code`、触发源、载荷和前端处理方式不同。新增或修改推送时，必须同时核对通道、业务码、设备/项目路由、事务提交时机、去重策略及前端合并规则。

## 当前专题索引

| 场景 | 业务码/接口 | 维护文档 | 主要代码入口 |
| --- | --- | --- | --- |
| 设备 OSD、HMS、任务状态局部更新 | `device_osd`、`dock_osd`、`device_hms`、`device_task_status` | [设备任务状态展示与 WebSocket 推送闭环](device-task-status-display-and-websocket.md)、[监控中心设备核心列表与刷新模型](monitor-device-v2-list-refresh-model.md) | `InspectionDeviceStatusBusinessServiceImpl`、`InspectionAlarmBusinessServiceImpl`、`DeviceTaskStatusNotifier` |
| 机器狗完整状态快照 | `/ws/dock`；`robot_dog_status_snapshot` | [机器狗完整状态快照 WebSocket 契约](robot-dog-status-snapshot-websocket.md) | `InspectionRobotDogStatusBusinessServiceImpl`、`WebSocketMessageServiceImpl` |
| 顶部业务统计刷新 | `monitor_business_overview_changed`；`GET /drone/monitor/business-overview` | [顶部统计刷新 WebSocket 链路](monitor-business-overview-websocket.md) | `MonitorBusinessOverviewChangedNotifier`、`MonitorBusinessStatusNotifier` |
| 左上角基础统计刷新 | `monitor_overview_changed`；`GET /drone/monitor/overview` | [左上角基础统计刷新 WebSocket 链路](monitor-overview-websocket.md) | `MonitorOverviewChangedNotifier` |
| 项目/项目集权限失效广播 | `project_permission_changed` | [P1 项目权限失效 WebSocket 广播](project-permission-websocket.md) | `ProjectPermissionChangedNotifier` |

## 维护顺序

1. 先确认消息属于设备级局部更新、监控统计刷新还是权限/业务通知，并选择对应专题文档。
2. 再从 P1 代码核对触发入口、事务边界和 `IWebSocketMessageService` 的路由方式；专题文档只作导航，不能替代代码核实。
3. 修改公开 `biz_code`、载荷字段、通道或前端合并规则时，同步更新对应专题文档、产品入口和回归测试说明。
4. 涉及数据库事务提交后的广播，确认发送失败是否允许影响已提交业务；涉及实时状态，确认是否有缓存回源、去重或定时对账。

## 共用契约与排障入口

- P1 统一发送能力：`IWebSocketMessageService`、`WebSocketMessageServiceImpl`、`WebSocketMessageResponse`、`DeviceWebSocketConfigurer`。
- 监控设备列表的初始 HTTP 数据与局部消息合并规则见 [监控中心设备核心列表与刷新模型](monitor-device-v2-list-refresh-model.md)。
- 设备上行导致的 OSD/图传链路问题见 [DJI OSD 上行数据链路](../../flows/dji-osd-upstream-flow.md)。
