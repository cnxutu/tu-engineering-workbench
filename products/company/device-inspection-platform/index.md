# 无人机巡检平台

这是面向多仓库协作的产品上下文入口。先读本页，再按任务加载文档；当前代码和仓库局部约束优先。

## 已验证范围

- 巡检业务平台包含业务、核心、IoT 与启动模块，并涉及 RocketMQ 上下游及媒体/视频能力（证据：`c-drone-inspection/README.md`）。
- 网关上报连接与协议事实（证据：`c-iot-server/docs/device_online_state_architecture_optimization.md`）。IoT Server 是否已在当前实现中集中作最终状态判定，仍待验证。
- 网关是协议与连接入口，负责协议转换、鉴权补齐及与 IoT 平台之间的转发（证据：`c-iot-gateway/README.md`）。
- DJI 适配器负责协议/SDK 映射，不承担业务编排（证据：`ad-iot-codec-adapter-dji/README.md`）。

## 按需加载

- 范围、术语与仓库定位：[上下文](context/system-overview.md)、[领域模型](context/domain-model.md)、[仓库地图](context/repository-map.md)。
- 服务边界与契约：[服务地图](architecture/service-map.md)、[数据所有权](architecture/data-ownership.md)、[跨服务契约](architecture/cross-service-contracts.md)。
- 设备、指令、DJI、巡检或媒体改动：读取对应 [流程目录](flows/)；机场/无人机 OSD、State 或 DRC 数据改动优先读 [DJI OSD 上行数据链路](flows/dji-osd-upstream-flow.md)，控制、任务或 DRC 指令改动优先读 [DJI 设备指令下行链路](flows/dji-osd-command-flow.md)。
- 具体仓库：按 [仓库导航](repositories/index.md) 选择清单；设备、指令等改动按 [流程导航](flows/index.md) 定位。示例仅作演示，见 [minimal-demo](examples/minimal-demo/README.md)。

部署节点、地址、端口、完整 Topic/接口清单均未在本知识包中确认，修改前须核实运行配置和代码。
