# DJI 设备指令下行链路

> **证据等级：代码核对已确认（2026-07-24）**。本文只描述 P1 到 DJI 设备的指令下行；OSD、State 与 DRC OSD 上行见 [DJI OSD 上行数据链路](dji-osd-upstream-flow.md)。Topic 配置、运行 Jar 版本、Broker ACL 与线上行为仍须按文末清单验证。

## 运行时边界

`ad-iot-codec-adapter-dji`（P4）不是独立部署或消息总线的一跳。它由 `c-iot-gateway`（P3）以 Maven 依赖、SPI/Bean 方式加载：P3 的下行处理器调用 P4 编码，再由 P3 通过 MQTT Broker 将指令发送至 DJI 机场或无人机。完整服务关系见[集成地图](../architecture/integration-map.md)。

## 关键契约

| 契约 | 已确认含义 |
| --- | --- |
| 网关下行 Topic | P2 按 `iotGatewayId` 创建下行 Topic；P3 消费所属网关的下行消息。 |
| 下行 identifier | `inspection_device_control`、`inspection_task_command`、`inspection_drc_command` 等驱动 P4 的命令族编码。 |
| 同步完成语义 | `WAIT_REPLY`、`NONE` 与 `UNSUPPORTED` 决定 P2 对同步 RPC 的完成语义。 |
| 指令目标路由 | 机场与无人机的目标 SN、通道及 `iotGatewayId` 必须由当前设备与配置核实，不能从 OSD 身份路由推断。 |

## 指令下行

1. P1 的控制、任务或 DRC API 统一收敛至 `InspectionIotCommandGateway`，再通过 `IoTDeviceApi.invokeDeviceService` 调用 P2。
2. P2 校验设备和物模型服务，构造 `thing.service.invoke`；按设备和通道解析 `iotGatewayId`，投递到对应 P3 下行 Topic。
3. P3 消费下行消息，按 codecId 调用 P4 的 `DjiCodecAdapter#encode`。
4. P4 由 `params.identifier` 选择 Device、Task、Payload、DRC 等命令族编码器，生成 `/services` 或 `/drc/down` Topic 与 DJI JSON。
5. P3 通过 EMQX 发布给 DJI 机场或无人机；按完成语义向 P2 返回处理结果。

DRC 先建立飞行控制权与 DRC 模式会话，`drc_mode_enter` 走 `/services`；摇杆、心跳、急停等高频命令走 `/drc/down`。会话心跳、Redis 会话键及停止逻辑应作为同一变更范围评估。

## 代码阅读入口

| 项目 | 首选入口 |
| --- | --- |
| P1 | `InspectionIotCommandGatewayImpl` 及控制、任务、DRC 路由层 |
| P2 | `IoTDeviceRpcApi#invokeDeviceService` 与下行消息投递 |
| P3 | 下行 handler、`ProtocolCodecAdapterManager` 与 MQTT 发布 |
| P4 | `DjiCodecAdapter`、`DjiDownstreamEncoderRegistry` 及命令族编码器 |

## 联调前必验项

- P3 配置的 codecId 与 P4 `DjiConstants.DJI_CODEC_ID` 必须一致；运行 Jar 版本需与当前源码核对。
- 核对 `targetDeviceSn` 是机场还是机体，以及最终 `/services`、`/drc/down` Topic。
- 验证 P2 的下行路由、P3 订阅与 P4 编码器是否支持目标 `identifier`。
- 验证 `WAIT_REPLY`、`NONE`、`UNSUPPORTED` 的超时、错误与调用方处理语义。
- DRC 改动额外核对控制权、模式会话、心跳、Redis 会话键和停止清理。
- EMQX 入口的认证、ACL、订阅 Topic 与 QoS 属运行配置事实，必须单独核实。

相关资料：原始核对文档《机场OSD与设备指令上下行链路梳理》（用户提供，2026-07-24）。
