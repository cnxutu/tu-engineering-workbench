# 多厂商设备接入边界

> **证据等级：P3 当前代码核对已确认（2026-08-31）。** 本页定义新设备厂商或型号接入时的资料归档与平台边界；它不代表任何非 DJI 厂商已经接入，也不预先指定适配器仓库、通信协议、物模型或部署方式。

## 何时读取

- 询价、评估或接入新的无人机、机器狗或其他巡检设备厂商/型号。
- 判断厂商资料应归档到哪里，以及设备连接应走原始报文还是厂商 SDK。
- 新增设备能力、状态、故障、控制权、命令或媒体数据，需要划定 P1/P2/P3 与厂商适配器的责任。

## 知识归档边界

| 层级 | 保存内容 | 不保存 |
| --- | --- | --- |
| 厂商入口 | 官方资料入口、交付/授权渠道、版本追溯和跨型号约束。 | 某型号的字段、频率、平台 TSL 或接入方案。 |
| 型号页面 | 已核对的 SDK/协议能力、状态与安全语义、型号特有待确认项。 | 其他型号的事实，或未批准的平台通用决策。 |
| 平台接入页面 | P3 扩展边界、P2/P1 契约、通信选型、联调和回滚要求。 | 厂商完整 SDK/API 手册。 |

新厂商在 `context/domain/<vendor>/index.md` 建立厂商入口；有可复用型号事实时再建立型号页面。当前 [智元酷拓（Agibot）厂商资料入口](agibot/index.md) 与 [D1 Max 型号页面](zhiyuan-d1-max-sdk.md) 是该结构的首个实例。既有 DJI 文档暂按主题维护，迁移只在有明确维护需求时进行。

## 当前平台的接入分流

| 厂商能力与连接归属 | P3 当前可复用边界 | 仍须在具体接入中确认 |
| --- | --- | --- |
| 设备向 P3 协议入口收发原始报文 | `ProtocolCodecAdapter`；P3 由协议实例的 `protocolCodecId` 选择 Codec。 | 适配器实现与装载位置、协议实例、认证/连接方式、上下行映射。 |
| 厂商 SDK 在适配器内部自管连接与收发 | `CustomProtocolAdapter`；P3 注册标准上行回调并调用下行方法。 | Java 调用 SDK 的受支持方式，或独立原生 Bridge 的本地/网络契约。 |
| 独立 C++/原生 Bridge | 仍需 P3 内的薄 Java Adapter/Ingress 把事件转为 `UpstreamDecodedData`、将下行委托给 Bridge。 | HTTP/JSON、gRPC、MQTT 或其他 transport，认证、重连、反压、幂等与部署拓扑。 |

P4 `ad-iot-codec-adapter-dji` 是当前 DJI Codec 模块的事实，不是新厂商必须复用或必须新建的模块。新厂商的适配器归属、打包和发布方式须在已确认的实现任务中决定。

## 每个新型号的最小核对项

1. 固定厂商、型号、固件、SDK/协议版本和一手资料来源；不得用会变动的分支或宣传资料替代交付版本。
2. 区分设备身份、SDK/网络连接、平台 ONLINE/OFFLINE、状态、故障、控制权、命令受理和动作完成语义。
3. 选择接入分流后，定义设备身份映射、上/下行标准消息、TSL identifier、事件幂等、错误/超时和安全控制权契约。
4. 分别联调连接/重连、状态、故障、命令受理、动作完成、人工接管或急停，以及高频传感器/媒体的数据面。
5. 准备 TSL、P1 Handler/Data Rule、P3 协议实例或 Adapter 与厂商组件的联合回滚；不让未知 identifier 被业务侧确认消费。

落实这些核对项及后续开发、联调、发布时，使用[设备接入核心上下行对接任务清单](device-integration-task-checklist.md)记录责任、产物和验收证据。

## 当前代码证据

- [P3 协议实例与 Codec 选择](../../repositories/c-iot-gateway/protocol-instance-and-codec-selection.md)：`ProtocolCodecAdapter` 的唯一注册与实例选择。
- [P3 网关上/下行桥接](../../repositories/c-iot-gateway/gateway-upstream-downstream-bridge.md)：标准上/下行桥接与回复模式。
- [原生 SDK Bridge 的通信选型](grpc-edge-bridge-selection.md)：独立 Bridge 的 HTTP/JSON、gRPC 与 MQTT 候选取舍。
