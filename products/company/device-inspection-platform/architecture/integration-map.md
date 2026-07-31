# 集成地图

已验证的逻辑链路：设备/第三方协议 → IoT 网关 → IoT 平台；IoT 平台的下行指令经网关送往设备。DJI 适配器作为网关进程内依赖参与编解码，不是独立部署的一跳。

按网关隔离的上、下行 MessageBus、P2 Data Rule 到 P1 `iot_business_event:DEFAULT_FLOW` 的投递、OSD identifier 与同步下行回执语义均已有代码核对证据；完整 Topic 命名、运行配置、Data Rule 启用状态和线上时序仍待验证。

参见 [跨服务契约](cross-service-contracts.md)、[DJI OSD 上行数据链路](../flows/dji-osd-upstream-flow.md) 与 [DJI 设备指令下行链路](../flows/dji-osd-command-flow.md)。
