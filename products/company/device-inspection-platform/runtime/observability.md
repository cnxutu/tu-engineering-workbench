# Runtime Observability

## 范围

本页描述可由当前源码确认的日志与 `traceId` 设计，供 Runtime Reconnaissance 后与本地 snapshot
交叉验证。它不证明 Docker 日志、文件路径或任何环境中服务实际运行。

## 日志入口

| Logical service | Source-confirmed log sources | Trace format | Runtime verification needed |
| --- | --- | --- | --- |
| `b-inspection-platform` | console、滚动文件、独立 IoT upstream 文件 | console 和文件 pattern 包含 MDC `traceId` | stdout/file source、路径与 rotation |
| `c-iot` | console、滚动系统/错误文件 | console 和文件 pattern 包含 MDC `traceId` | stdout/file source、路径与 rotation |
| `c-iot-gateway` | console、主日志、core/codec/message-bus 分流文件 | console 和文件 pattern 包含 MDC `traceId` | stdout/file source、路径与 rotation |
| `c-video-center` | console、滚动应用文件、SIP 文件 | 当前 logback pattern 未显示 MDC `traceId` | 是否有其他 tracing integration |

在运行时，应先以容器 stdout（若存在）和对应服务的高优先级错误日志交叉确认，再以时间窗口、设备/业务
身份和消息标识建立跨服务证据链。不要把单个服务中的 `traceId` 当作端到端主键，除非传递机制已被实际代码和
运行日志共同证明。

## `traceId` 源码证据

`c-iot-gateway` 的 HTTP `TraceIdWebFilter` 是业务仓库实现：它接收 `X-Request-Id`，或使用 `star-framework`
`MdcTracerUtils` 生成带 `igw/web` 语义的值，并返回 response header。其 MQTT、TCP 与 Custom 上行处理器
也由 P3 自己在处理边界调用同一 `star-framework` 工具创建、写入和清理 MDC。因此 P3 是这些非 HTTP 入口的
trace owner，`star-framework` 是所复用的 MDC/key/ID 工具 provider；该分层不证明消息转发后的跨进程传播。

`c-iot-server` 的 `DeviceMessageLogStore` 会在消息日志没有 traceId 时读取当前 MDC 值。两个视频
RocketMQ consumer 调用 `MdcTracerUtils.getTraceId()`，这只能保证消费线程中存在一个 traceId；MDC 为空时
该工具会新建 ID，而不是从消息恢复。`star-framework` 的 `MqTraceUtils`/`StarMQProducer` 确实提供了
`X-Request-Id` message header 的附加与恢复能力，且 P2 `IotBusinessEventProducer` 使用 `StarMQProducer`；
但 P2 的其它直接 `RocketMQTemplate` 调用和上述视频 consumer 不构成同一条端到端保证。

`c-drone-inspection`、`c-iot-server`、`c-iot-gateway`、`c-gateway` 与 `c-system` 各自维护 Logback
pattern；它们都输出 MDC `traceId`，但 `star-framework` 没有为业务服务自动装载统一 Logback 配置。相同格式是当前各
仓库配置事实，不是已证明的 starter 行为。完整的 provider、consumer、版本和可依赖约束见
[共享框架能力溯源](framework-capability-provenance.md)。

## Runtime Reconnaissance 检查点

1. 对每个已运行 logical service 保存 stdout 与文件日志是否可用，而不复制业务 payload 或 credential。
2. 以一次可识别的请求或设备事件验证网关入口、IoT 消费与业务消费的 trace/request/message 标识；无安全
   测试事件时只记录为 not verifiable。
3. 核实异步 executor、RocketMQ consumer、MQTT handler 和 WebSocket 消息是否保留或重建 trace context。
4. 记录 warning/error 的首选入口、文件轮转和时间范围，真实路径仅进入本地 snapshot。

## Stable problem-to-evidence routing

下表是稳定的导航规则，不替代当前环境的 deployment-map、runtime-snapshot 或实际日志。Runtime Explore 默认先读取
最小 route 与代码入口，在边界出现证据缺口时才扩大范围。

| User symptom | Code Evidence first | Runtime Evidence next | Correlation boundary |
| --- | --- | --- | --- |
| 接口异常 | `c-gateway` 路由/过滤器，再到下游 Controller | API gateway 与目标服务的状态、时间窗日志 | `X-Request-Id` / `traceId`；实际路由须由环境配置确认。 |
| 设备离线 | `c-iot-gateway` 上行桥接，再到 `c-iot` 设备状态处理 | P3、P2 容器状态与日志；已确认后才查 MQTT broker | device identity、gateway identity、message/request identifier；MQTT binding 不可猜测。 |
| traceId | 发起服务的 ingress、Feign/MQ capability | 同一时间窗的相关容器 stdout/文件日志 | `traceId` 是候选关联键；跨 Feign、MQ、协议边界须由代码与运行证据共同确认。 |
| MQTT topic | P3 协议 bridge 与 P4 codec mapping | P3 日志与已确认的 broker 日志 | Topic、device identity、request/message identifier；不把 MQTT 容器名当作绑定证据。 |
| 视频黑屏或录像异常 | `c-wvp` 资源/播放/录像入口 | `c-video-center`、ZLMediaKit 与媒体网络证据 | video resource、stream、media server 与 RocketMQ message identifier。 |
| 服务启动失败 | 对应 bootstrap、Nacos 配置导入与启动 lifecycle | 容器 state、health、最近启动日志、authorized readonly Nacos query | service name、container lifecycle 与配置版本；容器 running 不等于已注册。 |

在每条路由中，Observation 不等于 Diagnosis，Source Evidence 不等于 Runtime Verification。未知的 broker、实例注册、
有效配置或跨进程 trace 传播必须明确保留为 `unknown`，不得用命名或容器存在补齐。

## 证据

- `c-iot-gateway`: `TraceIdWebFilter`、`IotMqttUpstreamHandler` 与 `logback-spring.xml`。
- `c-iot-server`: `DeviceMessageLogStore`、视频 RocketMQ consumer 与 `logback-spring.xml`。
- `c-drone-inspection`: `logback-spring.xml`。
- `c-wvp`: `logback-spring.xml`。
- `star-framework`: `MdcConstants`、`MdcTracerUtils`、`RequestIdTraceFilter`、
  `RequestIdFeignInterceptor` 与 `MqTraceUtils`。
