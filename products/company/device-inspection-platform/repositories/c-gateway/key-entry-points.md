# P5：统一网关关键入口地图

> **证据等级：代码与本地配置核对已确认（2026-08-26）。** 本页只覆盖 `c-gateway` 的服务内入口。网关是否已为某个巡检服务配置生产路由、目标实例状态及 Nacos 运行配置，均须按目标环境核实。

## 范围

`c-gateway` 是 HTTP 入口层：它负责路径匹配与转发、跨域、登录用户上下文传递、灰度负载均衡、访问日志、License 过滤和网关异常响应。它不拥有下游巡检、IoT、系统或标签业务语义；请求到达网关后业务异常应继续定位目标服务。

## 按问题类型读取

| 问题 | 首选入口 | 阅读顺序 |
| --- | --- | --- |
| 请求未进入或转发到错误服务 | `src/main/resources/application.yaml`、`route/GatewayDiscoveryLocatorConfig.java` | 路径 predicate → `grayLb://` 目标服务名 → Nacos 实例与运行配置。 |
| Token、用户/租户上下文或伪造 Header | `filter/security/TokenAuthenticationFilter.java`、`util/SecurityFrameworkUtils.java` | Token 提取 → 远程校验/本地缓存 → `login-user` Header 注入 → 下游安全校验。 |
| 灰度实例选择错误 | `filter/grey/GrayReactiveLoadBalancerClientFilter.java`、`GrayLoadBalancer.java`、`util/EnvUtils.java` | 请求 `version`/`tag` → 实例 metadata 筛选 → Nacos 权重选择。 |
| 浏览器跨域或预检失败 | `filter/cors/CorsFilter.java`、`CorsResponseHeaderFilter.java` | 请求 Origin/预检 → 网关响应头 → 下游响应头叠加。 |
| 请求耗时、5xx 或统一错误格式 | `filter/logging/AccessLogFilter.java`、`handler/GlobalExceptionHandler.java`、`skywalking/` | 网关访问日志/trace → 已匹配路由 → 下游服务日志与响应。 |
| 许可证校验或被踢下线 | `filter/license/LicenseFilter.java`、`LicenseManager.java`、`mq/UserKickoutListener.java` | 网关本地过滤/消息处理 → 再核实 P6 的授权或用户事件来源。 |

## 已确认的约束

- `TokenAuthenticationFilter` 会先移除客户端伪造的 `login-user` Header；有有效 Token 时将用户、用户类型、租户和 scope 写入下游请求上下文/Header。
- Token 缺失或校验失败时，该网关过滤器仍会继续转发；接口是否必须登录由下游服务决定。因此“网关放行”不能证明下游接口应匿名可用。
- 端口、路由、服务发现和配置中心均存在运行环境差异；本地 `application.yaml` 是首选代码入口，不将其中的环境参数复制到知识页。

## 代码证据

- 启动入口：`GatewayServerApplication.java`。
- 路由与服务发现：`src/main/resources/application.yaml`、`route/GatewayDiscoveryLocatorConfig.java`。
- 过滤器与异常处理：`filter/`、`handler/GlobalExceptionHandler.java`。

## 待核实项

- 巡检业务服务的实际路径是否由静态路由、服务发现自动路由或外部网关配置暴露。
- 生产环境的 Nacos metadata、灰度标签、下游实例健康状态与访问日志留存策略。
