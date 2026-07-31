# P4：DJI 协议映射

> **证据等级：代码核对已确认（2026-07-31）。** P4 是 P3 进程内的 DJI 编解码 Adapter，负责 Topic、DJI payload 与统一物模型 identifier/参数之间的映射；不承载巡检任务、控制权、重试或会话编排。

## 何时读取

- 新增或修复 DJI Topic、上行字段、统一 identifier、下行命令或回复映射。
- 排查 P3 已选择 DJI Codec 但解码/编码失败、identifier 未注册或命令回复无法关联。

## 已确认的映射边界

| 方向 | P4 当前职责 |
| --- | --- |
| 上行 | `DjiCodecAdapter` 先按 DJI Topic 分类，再以唯一的 Topic Handler 解码为平台标准消息。OSD 与 DRC OSD 分别转换为统一属性上报；服务回复转换为同步回复与业务事件所需结构。 |
| 统一语义 | 上行消息以 `params.identifier` 声明物模型标识。属性可展开为 identifier 与业务字段同级的参数；事件保留 identifier 与同名 payload。 |
| 下行 | 仅接受 `thing.service.invoke`；外层 `identifier` 选择编码器，内层 `params` 为命令参数。注册表拒绝重复 identifier，未知 identifier 明确失败。 |
| DJI 报文 | 具体编码器将 identifier/command 映射为 DJI 原子 method、Topic 与 JSON。P4 不自动插入开机、控制权、重试或心跳等业务步骤。 |

## 维护约束

- 新 Topic 必须有唯一 `DjiTopicHandler`；新下行 identifier 必须有唯一 `DjiDownstreamEncoder`，并与 P2 物模型服务及 P1 调用方核对。
- 回复映射依赖固定的 DJI method → identifier/command 表。相同 DJI method 无法天然表达多个业务语义时，不应靠 payload 猜测。
- P4 当前未发现生产 TSL 文件；其测试契约只验证映射结果，不能取代 P2 的 TSL 管理。

## 代码证据

以下路径相对 P4 仓库根目录：

- `ad-iot-codec-adapter-inspection-dji/.../DjiCodecAutoConfiguration.java`：P3 classpath 自动配置与 Adapter Bean 注册。
- `ad-iot-codec-adapter-inspection-dji/.../DjiCodecAdapter.java`：Topic 解码与 `thing.service.invoke` 编码入口。
- `ad-iot-codec-adapter-inspection-dji/.../router/DjiTopicRouterFactory.java`：Topic Handler 唯一注册。
- `ad-iot-codec-adapter-inspection-dji/.../handler/DjiOsdTopicHandler.java`、`DjiDrcTopicHandler.java`、`DjiServicesReplyTopicHandler.java`：代表性上行映射。
- `ad-iot-codec-adapter-inspection-dji/.../encoder/DjiDownstreamEncoderRegistry.java`：下行 identifier 路由。
- `ad-iot-codec-adapter-inspection-dji/.../mapping/DjiMethodMappings.java`：DJI method 与统一 identifier/command 固定映射。
- `ad-iot-codec-adapter-inspection-dji/src/test/resources/*-contract.json`：测试契约，不是生产 TSL。
