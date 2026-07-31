# P2：设备、物模型与 TSL 边界

> **证据等级：代码核对已确认（2026-07-31）。** 本页说明 P2 对设备与统一物模型服务语义的责任；不记录某产品的完整 TSL 内容或具体设备配置。

## 何时读取

- 新增/修改 P1 发起的设备服务调用、`identifier` 或命令参数。
- 排查“设备不存在”“物模型服务不存在”、下行网关路由或同步调用超时。
- 导入、校验或调整产品 TSL。

## 已确认的责任

| 边界 | P2 当前行为 |
| --- | --- |
| 设备查询 | 网关通过 P2 的 `IotDeviceCommonApi` / `IotGatewayCommonApi` 查询和认证设备；设备返回包含产品的 codec 信息。 |
| 服务调用 | `IoTDeviceRpcApi#invokeDeviceService` 先校验设备与产品下的服务物模型，再构造 `thing.service.invoke`，其参数为 `identifier` 与业务 `params`。 |
| 下行路由 | 下行消息依据设备属性或缓存中关联的 `iotGatewayId` 投递给 P3；可按 identifier 解析通道标签。 |
| 同步回执 | 同步服务调用写入请求/结果关联信息，并等待 P3/P4 回传的结果；超时属于调用语义的一部分。 |
| TSL | P2 校验 properties、services、events 的 identifier 和数据类型；导入仅允许未发布产品，并替换该产品已有物模型记录后清理缓存。 |

## 维护约束

- 新增 P4 下行编码器前，先确认 P2 产品中有同名的**服务**物模型；P4 不替代 P2 的服务定义。
- 新增 P4 上行 identifier 前，确认 P2 Data Rule 的匹配语义和 P1 是否存在业务消费者。
- 修改 TSL 的 identifier、调用类型或参数结构时，连同 P1 调用方、P3/P4 编解码与兼容/回滚影响一起评估。

## 待核实项

- 实际 TSL 文件或生成源、导入发布流程及其负责人。
- 各产品的 identifier 与 P4 映射是否已全量一致。

P4 当前仅发现测试契约 JSON，未发现生产 TSL 文件；不得将 P4 写成 TSL 的存储或发布方。

## 代码证据

以下路径相对 P2 仓库根目录：

- `c-iot-core/.../api/device/IoTDeviceApiImpl.java`：设备查询、认证、网关注册 RPC。
- `c-iot-core/.../api/device/IoTDeviceRpcApi.java`：物模型服务校验、`thing.service.invoke` 与同步调用。
- `c-iot-core/.../service/device/message/IotDeviceMessageServiceImpl.java`：按设备网关归属的下行投递。
- `c-iot-core/.../service/thingmodel/IotThingModelServiceImpl.java`：TSL 校验与导入。
- `c-iot-core/.../util/IotTslDataTypeConverter.java`：TSL 属性、服务、事件和数据类型转换。
