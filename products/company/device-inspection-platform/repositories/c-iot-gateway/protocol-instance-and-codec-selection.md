# P3：协议实例与 Codec 选择

> **证据等级：代码核对已确认（2026-07-31）。** 用于理解多设备/多协议的当前接入机制与 P4 集成方式；不将其延伸为未证实的“按产品自动选协议”策略。

## 何时读取

- 新增协议实例、切换 `protocolCodecId`、接入新的适配器或排查“找不到编解码器”。
- 判断 P3 应解决还是 P4 应解决某个协议差异。

## 已确认的选择机制

1. 每个 P3 协议实例配置 `protocolCodecId`。P3 在启动时收集 Spring 容器内全部 `ProtocolCodecAdapter`，以 `ProtocolCodecMeta.id` 建立唯一映射；空 ID 或重复 ID 使启动失败。
2. 上行处理开始时，P3 以当前协议实例的 codec ID 选定 Adapter；下行也以同一实例选择 Adapter 编码。
3. P4 DJI 模块由 P3 Bootstrap 的 Maven 依赖引入，其自动配置注册 `DjiCodecAdapter` Bean。DJI 协议实例将 `protocolCodecId` 配置为 P4 的 codec 元数据 ID。
4. 因此当前的多协议扩展点是“协议实例 + 唯一 Codec Bean”。新协议应新增或引入独立 Adapter 并配置独立 ID，而不是在业务服务中判断协议类型。

## 边界判断

- 通用的协议实例、连接和编解码器选择问题：优先从 P3 排查。
- DJI Topic、字段、identifier 或命令报文映射问题：转入 P4 的 [DJI 协议映射](../ad-iot-codec-adapter-dji/dji-adapter-mapping.md)。
- 智元机器狗的 WebSocket 会话、APDU 或统一物模型映射问题：转入 P4-1 的 [智元机器狗协议映射](../ad-iot-codec-adapter-robotDog-zhiyuan/zhiyuan-robot-dog-adapter-mapping.md)。该 Adapter 使用 P3 的 `CustomProtocolAdapter` 边界；P3 运行配置和制品装载仍须在联调环境另行核实。
- 设备、产品或物模型服务定义问题：转入 P2 的 [设备、物模型与 TSL 边界](../c-iot-server/device-thing-model-tsl.md)。

## 待核实项

- 是否存在按产品、租户或设备型号自动选择协议实例的额外运行规则。
- 实际部署配置、启用实例与运行 Jar 中的 Adapter 版本。

## 代码证据

以下路径相对 P3 仓库根目录：

- `c-iot-gateway-core/.../core/manager/ProtocolCodecAdapterManager.java`：Adapter 唯一注册与上下行选择。
- `c-iot-gateway-core/.../core/handler/MessageProcessingEngine.java`：上行实例绑定 Adapter。
- `c-iot-gateway-core/.../autoconfigure/IotGatewayProperties.java`：协议实例的 `protocolCodecId` 配置模型。
- `c-iot-gateway-bootstrap/pom.xml`：P4 DJI Adapter 依赖。
- `c-iot-gateway-bootstrap/src/main/resources/application.yaml`：DJI 协议实例配置示例，仅可作为本地配置证据。
