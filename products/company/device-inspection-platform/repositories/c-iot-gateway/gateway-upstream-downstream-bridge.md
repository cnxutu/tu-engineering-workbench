# P3：网关上/下行桥接

> **证据等级：代码核对已确认（2026-07-31）。** 本页描述 P3 在 P2 与设备协议 Adapter 之间的运行时桥接；P3 不持久化设备业务数据，设备查询通过 P2 RPC 完成。

## 何时读取

- 上行已到网关但 P2/P1 未收到，或下行已由 P2 发出却未到设备。
- 排查设备离线、连接不存在、编码失败、Topic 构建失败或同步回复未完成。

## 已确认链路

### 上行

`MessageProcessingEngine` 固定驱动预检查、预代理、完整解码、登录/Token 检查、回复、异步转发与在线处理等步骤。异步转发阶段将 P4 或其他 Adapter 的标准化结果封装成 `IotDeviceMessage`，通过 P2 RPC 查询设备，再补齐设备、租户、网关和标签上下文后投递 IoT 消息总线。

### 下行

P2 按设备关联的网关投递下行消息；P3 的协议订阅者消费所属网关的消息，再按该协议实例选择 Codec。以 EMQX 为例，P3 先调用 Adapter 编码；若 Adapter 未提供 Topic 才按消息 method 与设备身份构建 Topic，最终由 P3 发布 MQTT。编码、设备离线、连接缺失、Topic 构建和发布失败都会返回明确失败结果。

同步调用的完成语义由 Adapter 给出的 `WAIT_REPLY`、`NONE` 或 `UNSUPPORTED` 决定；P3 只保存等待设备回复所需的临时关联，不替代 P2 的调用超时语义。

## 排查顺序

1. 核对 P2 的目标 `iotGatewayId` 与 P3 实际订阅者是否一致。
2. 核对 P3 协议实例的 codec ID、P4 Adapter Bean 与输入 `method`/`identifier`。
3. 下行再查设备连接和最终 Topic；上行再查 P3 是否成功通过 P2 RPC 解析设备。
4. 涉及同步命令时，检查 requestId 与回复模式，随后回到 P2 的结果等待逻辑。

## 代码证据

以下路径相对 P3 仓库根目录：

- `c-iot-gateway-core/.../core/handler/MessageProcessingEngine.java`：上行处理管道。
- `c-iot-gateway-core/.../core/handler/upstream/AsyncForwardHandler.java`：上行消息封装、设备查询与发送。
- `c-iot-gateway-core/.../adapter/outbound/device/IotDeviceMessageForwardAdapter.java`：P2 设备查询与消息总线投递。
- `c-iot-gateway-core/.../protocol/emqx/IotEmqxDownstreamSubscriber.java`：所属网关的下行订阅。
- `c-iot-gateway-core/.../protocol/emqx/router/IotEmqxDownstreamHandler.java`：编码、Topic 与 MQTT 发布。
- `c-iot-gateway-core/.../core/handler/downstream/GatewayDownstreamSubscriber.java`：下行结果与回复模式处理。
