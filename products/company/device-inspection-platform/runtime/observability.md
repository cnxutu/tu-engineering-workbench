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

`c-iot-gateway` 的 HTTP filter 接收 request-id header，或在缺失时创建 MDC `traceId`，并把它返回到
response header。其 MQTT、TCP 与 Custom 上行处理器也在处理边界创建并清理 MDC `traceId`。这证明 P3
进程内的上行处理日志可关联；它不证明消息转发后的跨进程传播。

`c-iot-server` 的 `DeviceMessageLogStore` 会在消息日志未携带 traceId 时读取当前 MDC 值；两个视频
RocketMQ consumer 会确保其消费处理存在 traceId。当前证据不足以确认设备消息在 gateway、IoT、RocketMQ
和业务服务之间保留同一值。`c-drone-inspection` 与 `c-iot-server` 的 Logback pattern 会输出 MDC 值，但本
轮未找到足以证明其全部 ingress、异步执行器或 RPC 传播语义的代码证据。

## Runtime Reconnaissance 检查点

1. 对每个已运行 logical service 保存 stdout 与文件日志是否可用，而不复制业务 payload 或 credential。
2. 以一次可识别的请求或设备事件验证网关入口、IoT 消费与业务消费的 trace/request/message 标识；无安全
   测试事件时只记录为 not verifiable。
3. 核实异步 executor、RocketMQ consumer、MQTT handler 和 WebSocket 消息是否保留或重建 trace context。
4. 记录 warning/error 的首选入口、文件轮转和时间范围，真实路径仅进入本地 snapshot。

## 证据

- `c-iot-gateway`: `TraceIdWebFilter`、`IotMqttUpstreamHandler` 与 `logback-spring.xml`。
- `c-iot-server`: `DeviceMessageLogStore`、视频 RocketMQ consumer 与 `logback-spring.xml`。
- `c-drone-inspection`: `logback-spring.xml`。
- `c-wvp`: `logback-spring.xml`。
