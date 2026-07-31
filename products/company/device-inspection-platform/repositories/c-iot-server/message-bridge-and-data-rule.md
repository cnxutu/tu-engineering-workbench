# P2：消息桥接与 Data Rule

> **证据等级：代码核对已确认（2026-07-31）。** 用于排查设备上行消息从 P3 进入平台、被处理或投递 P1 的路径；不定义具体设备的 Data Rule 配置、Broker 部署或线上投递结果。

## 何时读取

- P1 未收到设备上行、消息未落设备属性或 Data Rule 未触发。
- 新增或调整上行 `method`、`identifier`、Data Sink 或 P1 消费链路。

## 已确认的桥接边界

1. P3 将已规范化的 `IotDeviceMessage` 发送至 IoT 消息总线，并补齐设备、租户、`serverId`、`iotGatewayId` 与标签上下文。
2. P2 注册网关时，会为同一上行 Topic 建立独立消费者：设备消息处理、Data Rule 和场景规则。三者的处理顺序不可假定。
3. 设备消息消费者仅处理上行：按消息类型更新在线活动，并处理状态、属性与 OTA 进度；未知设备不会继续进入该处理分支。
4. Data Rule 按设备、`method` 与可选 `identifier` 匹配；命中后按 Data Sink 类型调用动作。RocketMQ 动作将完整 `IotDeviceMessage` 投递至规则配置的 Topic/Tag，P1 的业务消费只是其中一种目标。

## 排查顺序

1. 在 P3 确认消息是否已被编解码并携带正确设备身份与 `iotGatewayId`。
2. 在 P2 确认对应网关已注册上行 Topic，且动态消息订阅者与 Data Rule 订阅者均已建立。
3. 检查 P2 是否能从缓存找到设备，以及 `method`、`identifier` 是否符合 Data Rule 的匹配条件。
4. 检查命中的 Sink 状态和 RocketMQ 的 Topic/Tag；再转入 P1 `InspectionIotUpstreamConsumer`、Converter 与 Router。

不要以“P2 已完成属性落库”作为 P1 收到消息的前置条件：两条消费者链路独立。

## 待核实项

- 某一设备、产品或租户实际启用的 Data Rule 与 Sink 配置。
- Broker ACL、重试、死信和线上投递状态。

## 代码证据

以下路径相对 P2 仓库根目录：

- `c-iot-core/.../service/gateway/IotGatewayService.java`：动态订阅者注册。
- `c-iot-core/.../mq/consumer/device/IotDeviceMessageProcesser.java`：设备上行消费与基础处理。
- `c-iot-core/.../service/device/message/IotDeviceMessageServiceImpl.java`：状态、属性与 OTA 分支。
- `c-iot-core/.../service/rule/data/IotDataRuleServiceImpl.java`：规则匹配与 Sink 调用。
- `c-iot-core/.../service/rule/data/action/IotRocketMQDataRuleAction.java`：RocketMQ 投递。
