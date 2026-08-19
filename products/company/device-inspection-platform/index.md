# 无人机巡检平台

> **当前维护边界：设备数据上行与设备指令下行。** 本产品知识包暂不维护设备在线状态、巡检任务、媒体的详细领域资料、部署拓扑、完整领域模型或全量协议资料；架构总览只标注这些能力的服务边界，具体事实必须以目标仓库代码、契约和运行配置核实。

## 当前已登记服务

无人机巡检平台的已登记服务职责如下。其中设备消息与指令主链路仅覆盖 P1–P4；P5 是系统统一网关，P6/P7 是平台公共服务，尚未在本知识包中登记为该主链路的跳点。

| 服务 | 当前链路中的职责 |
| --- | --- |
| P1 `c-drone-inspection` | 设备业务的上行消费与控制、任务、DRC 指令发起。 |
| P2 `c-iot-server` | IoT 消息处理、Data Rule 投递与下行服务调用。 |
| P3 `c-iot-gateway` | 协议接入、设备连接与上/下行转发。 |
| P4 `ad-iot-codec-adapter-dji` | P3 进程内 DJI 编解码与协议映射，不承担业务编排。 |
| P5 `c-gateway` | 巡检系统统一网关；具体路由、鉴权和下游服务契约待核实。 |
| P6 `c-system` | RBAC、基础用户信息与系统管理能力。 |
| P7 `c-tag` | 树模型、标签资源关联与标签维度的数据权限能力；不拥有接入业务系统的资源本体。 |

当前核心证据覆盖设备消息上行和设备指令下行两条链路；架构页另外标注流媒体边界。当前代码、契约、配置和测试仍优先于本页。

## 按任务读取

- OSD、State 或 DRC 数据从设备进入平台：读 [DJI OSD 上行数据链路](flows/dji-osd-upstream-flow.md)。
- 控制、任务或 DRC 指令从平台下发设备：读 [DJI 设备指令下行链路](flows/dji-osd-command-flow.md)。
- 需要一个已核对的远程调试下行与进度回显样例：读 [DJI 机场强制关舱盖：端到端案例](flows/dji-cover-force-close-case.md)。
- P1 的业务命令路由、上行消费或 Handler：读 [P1 关键入口地图](repositories/c-drone-inspection/key-entry-points.md)。
- P2 设备主数据变更、P1 `manage_device` 投影、空间展示隔离或日终修复：读 [P2 设备主数据到 P1 投影同步](flows/device-master-projection-sync.md)。
- P1 的 OSD/DRC 快照、拓扑、运行任务或 DRC 会话：读 [P1 缓存设计](repositories/c-drone-inspection/cache-design.md)。
- P1 监控中心顶部统计刷新 WebSocket、状态触发与 CAMERA 覆盖：读 [顶部统计刷新 WebSocket 链路](repositories/c-drone-inspection/monitor-business-overview-websocket.md)。
- P1 监控中心左上角基础统计刷新 WebSocket、标注/围栏/设备关联触发：读 [左上角基础统计刷新 WebSocket 链路](repositories/c-drone-inspection/monitor-overview-websocket.md)。
- P1 设备任务状态展示、任务快照解析与 WebSocket 实时推送闭环：读 [设备任务状态展示与 WebSocket 推送闭环](repositories/c-drone-inspection/device-task-status-display-and-websocket.md)。
- P1 监控中心核心设备列表、局部 WebSocket 字段合并与全局刷新：读 [监控中心设备核心列表与刷新模型](repositories/c-drone-inspection/monitor-device-v2-list-refresh-model.md)。
- P2 的上行消息订阅、Data Rule、RocketMQ 投递或消息未进入 P1：读 [P2 消息桥接与 Data Rule](repositories/c-iot-server/message-bridge-and-data-rule.md)。
- P2 的设备查询、物模型服务、TSL、下行路由或同步调用：读 [P2 设备、物模型与 TSL 边界](repositories/c-iot-server/device-thing-model-tsl.md)。
- P3 的协议实例、多协议接入、`protocolCodecId` 或 P4 集成：读 [P3 协议实例与 Codec 选择](repositories/c-iot-gateway/protocol-instance-and-codec-selection.md)。
- P3 的上行转发、下行订阅、连接、编码或回复模式：读 [P3 网关上/下行桥接](repositories/c-iot-gateway/gateway-upstream-downstream-bridge.md)。
- P4 的 DJI Topic、字段、identifier、命令或回复映射：读 [P4 DJI 协议映射](repositories/ad-iot-codec-adapter-dji/dji-adapter-mapping.md)。
- P5 的统一入口、路由或鉴权问题：从 `c-gateway` 仓库的 `README.md` 和局部 `AGENTS.md` 开始核实。
- P6 的用户、部门、岗位、角色、权限或系统管理能力：从 `c-system` 仓库的 `README.md` 和局部 `AGENTS.md` 开始核实。
- P7 的标签树、资源关联或标签维度数据权限能力：从 `c-tag` 仓库的 `README.md` 和局部 `AGENTS.md` 开始核实。
- 评审 P1 项目集/项目、角色池、空间池与 P7 项目树边界：读 [项目集与项目管理设计（P1 + P7）](decisions/project-set-project-management.md)。
- 维护按版本归档的产品 PRD：从 [产品 PRD 目录](prd/index.md) 开始，当前版本读 [v2.1.0 项目管理 PRD](prd/v2.1.0/project-management.md)。
- DJI 无人机行业术语、HMS、OSD、DRC 与姿态角语义：读 [DJI 无人机领域知识](context/domain/index.md)。
- P1-P4 技术栈、中间件、职责边界、消息/指令/视频流媒体架构与问题定位范围：读 [P1-P4 技术栈与系统架构](architecture/p1-p4-technology-and-system-architecture.md)。

未命中这两类场景时，不因项目名称自动加载整个产品目录；先从受影响仓库的局部 `AGENTS.md`、代码、契约和测试核实。新增长期可复用的产品事实时，遵循 `docs/authoring-guide.md` 与 `docs/governance.md`。
