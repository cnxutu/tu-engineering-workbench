# 跨服务契约

## 已验证

- 网关向 IoT 平台转发设备上行消息，并接收下行指令。
- 下行总线主题格式：`iot:gw:down:${serverId}`；协议实例启动时订阅该格式主题。
- P4 DJI Codec Adapter 是 P3 网关的进程内编解码依赖；不是独立消息总线节点。
- P2 的 Data Rule 可将完整 `IotDeviceMessage` 交给 P1 默认 RocketMQ 消费入口 `iot_business_event:DEFAULT_FLOW`；普通 OSD、DRC OSD 和下行 identifier 的语义见 [DJI OSD/指令链路](../flows/dji-osd-command-flow.md)。

## 待验证

完整 Topic 列表、Data Rule 启用状态、消息 schema、幂等/重试、超时、鉴权和版本兼容策略均需结合运行配置确认。改动跨服务消息前应同时核查生产者、消费者、运行 Jar 与 Broker 配置。
