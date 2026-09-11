# P1 巡检业务平台导航

## 范围

本目录维护 P1 的已验证业务入口与专题知识。跨服务消息、协议和运行时事实应沿链接回到相应流程、仓库或 Runtime Context 核实。

## 当前文档

- [关键入口地图](key-entry-points.md)：业务命令路由、上行消费与 Handler。
- [关键缓存设计与读取边界](cache-design.md)：OSD、DRC、在线状态、任务与拓扑缓存。
- [WebSocket 推送维护入口](websocket-index.md)：推送专题和共用契约导航。
- [设备任务状态展示与 WebSocket 推送闭环](device-task-status-display-and-websocket.md)。
- [机器狗完整状态快照 WebSocket 契约](robot-dog-status-snapshot-websocket.md)。
- [监控中心顶部统计刷新 WebSocket 链路](monitor-business-overview-websocket.md)。
- [监控设备地理位置](monitor-device-geolocation.md)。
- [监控中心设备核心列表与刷新模型](monitor-device-v2-list-refresh-model.md)。
- [监控中心左上角基础统计刷新 WebSocket 链路](monitor-overview-websocket.md)。
- [项目菜单权限（P1 + P6）](project-menu-permission.md)。
- [项目权限失效 WebSocket 广播](project-permission-websocket.md)。

仓库角色、证据和待核实项见 [manifest](../c-drone-inspection.yaml)。
