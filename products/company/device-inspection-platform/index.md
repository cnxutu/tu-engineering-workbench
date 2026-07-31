# 无人机巡检平台

> **当前维护边界：设备数据上行与设备指令下行。** 本产品知识包暂不维护设备在线状态、巡检任务、媒体、部署拓扑、完整领域模型或全量协议资料；这些场景必须以目标仓库代码、契约和运行配置核实，后续取得可复现证据后再按需补充。

## 当前已验证范围

设备消息与指令跨 P1–P4 的最小职责边界如下：

| 服务 | 当前链路中的职责 |
| --- | --- |
| P1 `c-drone-inspection` | 设备业务的上行消费与控制、任务、DRC 指令发起。 |
| P2 `c-iot-server` | IoT 消息处理、Data Rule 投递与下行服务调用。 |
| P3 `c-iot-gateway` | 协议接入、设备连接与上/下行转发。 |
| P4 `ad-iot-codec-adapter-dji` | P3 进程内 DJI 编解码与协议映射，不承担业务编排。 |

当前证据只覆盖下列两条链路；当前代码、契约、配置和测试仍优先于本页。

## 按任务读取

- OSD、State 或 DRC 数据从设备进入平台：读 [DJI OSD 上行数据链路](flows/dji-osd-upstream-flow.md)。
- 控制、任务或 DRC 指令从平台下发设备：读 [DJI 设备指令下行链路](flows/dji-osd-command-flow.md)。
- P1 的业务命令路由、上行消费或 Handler：读 [P1 关键入口地图](repositories/c-drone-inspection/key-entry-points.md)。
- P1 的 OSD/DRC 快照、拓扑、运行任务或 DRC 会话：读 [P1 缓存设计](repositories/c-drone-inspection/cache-design.md)。
- P2 的上行消息订阅、Data Rule、RocketMQ 投递或消息未进入 P1：读 [P2 消息桥接与 Data Rule](repositories/c-iot-server/message-bridge-and-data-rule.md)。
- P2 的设备查询、物模型服务、TSL、下行路由或同步调用：读 [P2 设备、物模型与 TSL 边界](repositories/c-iot-server/device-thing-model-tsl.md)。
- P3 的协议实例、多协议接入、`protocolCodecId` 或 P4 集成：读 [P3 协议实例与 Codec 选择](repositories/c-iot-gateway/protocol-instance-and-codec-selection.md)。
- P3 的上行转发、下行订阅、连接、编码或回复模式：读 [P3 网关上/下行桥接](repositories/c-iot-gateway/gateway-upstream-downstream-bridge.md)。
- P4 的 DJI Topic、字段、identifier、命令或回复映射：读 [P4 DJI 协议映射](repositories/ad-iot-codec-adapter-dji/dji-adapter-mapping.md)。

未命中这两类场景时，不因项目名称自动加载整个产品目录；先从受影响仓库的局部 `AGENTS.md`、代码、契约和测试核实。新增长期可复用的产品事实时，遵循 `docs/authoring-guide.md` 与 `docs/governance.md`。
