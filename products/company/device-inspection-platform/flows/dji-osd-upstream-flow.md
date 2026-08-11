# DJI OSD 上行数据链路

> **证据等级：代码核对已确认（原始链路：2026-07-24；`businessStatus` 再包装：2026-08-11）**。本文只描述 DJI 机场或无人机到 P1 的 OSD、State 与 DRC OSD 上行；控制、任务与 DRC 指令下行见 [DJI 设备指令下行链路](dji-osd-command-flow.md)。Topic 配置、Data Rule、运行 Jar 版本、Broker ACL 与线上行为仍须按文末清单验证。

## 运行时边界

`ad-iot-codec-adapter-dji`（P4）不是独立部署或消息总线的一跳。P3 以 Maven 依赖、SPI/Bean 方式加载 P4 进行 Topic 路由与解码，再由 P3 将规范化消息发送给 P2；P2 的 Data Rule 可投递给 P1。

## 关键契约

| 契约 | 已确认含义 |
| --- | --- |
| 上行来源 | DJI 机场或无人机向 `thing/product/{sn}/osd`、`state` 或 `drc/up` 发布消息。 |
| 普通 OSD identifier | `inspection_device_status_report`，用于机场、无人机 OSD 与 State。 |
| DRC OSD identifier | `inspection_drc_osd_report`，用于含位置的高频 DRC OSD。 |
| P1 业务 Topic | P1 默认消费 `iot_business_event` / `DEFAULT_FLOW`；P2 是否实际投递取决于 Data Rule。 |
| 身份路由 | P4 将机场 SN 映射自身设备名，将无人机 SN 映射父机场设备名；P1 再以 `parentDeviceSn` 与 `deviceSn` 恢复子机业务实体。 |

## OSD 上行

1. DJI 机场或无人机发布 OSD、State 或 DRC 上行消息。
2. P3 的 EMQX 上行协议进入 `MessageProcessingEngine`；P4 的 `DjiCodecAdapter` 依次完成 Topic 预判、身份路由与解码。
3. P4 将 DJI `data` 规范化为 `identifier` 与同名 payload：普通 OSD/State 为 `inspection_device_status_report`，DRC 高频 OSD 为 `inspection_drc_osd_report`。
4. P3 补齐设备、租户、网关等上下文，发送至 P2 对应网关的上行 Topic。
5. P2 平台消息处理与 Data Rule 是并行消费者；不得假设属性落库先于 Data Rule 投递。
6. 匹配的 P2 Data Rule 将完整 `IotDeviceMessage` 投递给 P1 的 `iot_business_event:DEFAULT_FLOW`。
7. P1 以 `params.identifier` 和同名动态字段解析并路由：普通 OSD 由 `DeviceStatusPropertyHandler`，DRC OSD 由 `DrcOsdPropertyHandler`。

普通 OSD 与 DRC OSD 的 Redis/前端推送语义不同：前者驱动机场或子机状态、任务与业务联动；后者承载低延迟位置、姿态与视锥。不得将两者当成可相互覆盖的同一缓存。

## P1 OSD 再包装：`businessStatus`

`businessStatus` 不是 DJI Topic 或 P4 编解码字段，而是 P1 在普通 `DEVICE_TELEMETRY` 处理完成后，对 WebSocket OSD 消息 `data`（`InspectionTelemetryDTO`）增加的展示控制字段。它不改变 P2 Data Rule、P3 上行消息或 P4 的 `identifier`/payload 契约。

| 消息 | 计算时机 | `data.businessStatus` | 依据 |
| --- | --- | --- | --- |
| `dock_osd` | 机场普通 OSD 处理时 | 机场状态枚举名称 | 当前分包优先、写入前 `osd:{dockSn}` 120 秒快照补齐缺失的异常字段 |
| `device_osd` | 无人机普通 OSD 处理时 | 无人机状态枚举名称 | 当前普通无人机 OSD 快照 |
| `device_osd`（DRC 高频 OSD） | DRC OSD 处理时 | `null` | DRC DTO 缺少完整业务状态判定所需字段，本链路不伪造该状态 |

当前 P1 映射规则由 `MonitorBusinessStatusMapper` 统一复用：

- 机场：离线为 `OFFLINE`；`modeCode` 优先取当前分包、缺失时取 120 秒缓存。1/2/3/5 为 `DEBUG_UPGRADE`；4/0 时若 `coverState=3`、`emergencyStopState=true`、`alarmState=true`、`flighttaskStepCode=255/256`、`positionState.isFixed=3` 或 `networkState.quality=0` 任一命中，则为 `ABNORMAL`；未命中时分别为 `WORKING`/`IDLE`，其他或缺失为 `UNCLASSIFIED`。
- 无人机：离线为 `OFFLINE`；`modeCode` 11/12/14 为 `ABNORMAL`，13/19 为 `DEBUG_UPGRADE`，0 为 `IDLE`，1–10、15–18、20/21 为 `WORKING`，其他或缺失为 `UNCLASSIFIED`。
- `businessStatus` 传输为枚举名称字符串（如 `WORKING`），common DTO 不依赖 core 枚举；顶部业务统计与 OSD 展示复用同一映射器。

机场异常判定不新增缓存或改变现有缓存写入：当前分包显式携带 `false`、`0` 或其他非异常值时优先覆盖旧异常；字段未携带时才回退缓存。该字段只控制 P1 OSD 展示及相关统计，不代表设备协议原始状态，也不由设备离线事件额外触发 OSD 推送。离线后的状态展示仍需结合 `online:{deviceSn}`、OSD TTL 和相应缓存读取边界判断。

## 代码阅读入口

| 项目 | 首选入口 |
| --- | --- |
| P1 | `InspectionIotUpstreamConsumer`、`InspectionDeviceStatusBusinessServiceImpl`、`DeviceStatusPropertyHandler`、`DrcOsdPropertyHandler` |
| P2 | `IotDeviceMessageServiceImpl`、Data Rule 与 RocketMQ action |
| P3 | `IotEmqxUpstreamProtocol`、`MessageProcessingEngine` 与上行 handler |
| P4 | `DjiCodecAdapter`、`DjiOsdTopicHandler`、`DjiDrcTopicHandler` |

P1 再包装与状态判定的代码入口：`InspectionDeviceStatusBusinessServiceImpl#handleHostTelemetry`、`#handleSubDeviceTelemetry`、`#handleDrcOsd`，`MonitorBusinessStatusMapper`，以及 common 模块的 `InspectionTelemetryDTO`。

## 联调前必验项

- P3 配置的 codecId 与 P4 `DjiConstants.DJI_CODEC_ID` 必须一致；运行 Jar 版本需与当前源码核对。
- P2 的 Data Rule 必须分别覆盖普通 OSD 与 DRC OSD，并投递到 P1 实际消费的 Topic/Tag。
- P4 的机场—无人机身份注册依赖 `update_topo`；重启后先验证其重新建立。
- 平台状态处理和 Data Rule 消费并行；P1 不得依赖“P2 已先落库”的时序。
- 新增或调整 `businessStatus` 时，必须分别验证普通机场 OSD、普通无人机 OSD 与 DRC 高频 OSD；不得把 DRC 的空值误当成普通 OSD 的状态缺失，也不得把 P1 展示字段回写为 P4 原始协议字段。
- EMQX 入口的认证、ACL、订阅 Topic 与 QoS 属运行配置事实，必须单独核实。

相关资料：原始核对文档《机场OSD与设备指令上下行链路梳理》（用户提供，2026-07-24）。
