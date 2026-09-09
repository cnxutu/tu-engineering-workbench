# Runtime Context

## 范围

本页是无人机巡检平台 Runtime 任务的按需入口。逻辑环境由
[`core/registry/environments.yaml`](../../../../core/registry/environments.yaml) 定义；本机 SSH
别名由忽略的 `runtime.local.yaml` 绑定；完整的主机、容器、挂载、端口和日志路径只可保存到忽略的
`.runtime.local/<environment>/`。三者不替代现有仓库注册表、产品架构页或源码配置。

当前已登记的 `company-dev` 是逻辑开发环境。一次授权的只读 Docker inventory 已验证它采用容器化 Docker
运行模型，并观察到多个业务服务与中间件部署单元；物理主机、连接参数、容器状态及其时间点属于本地 snapshot，
不写入 committed Product Truth。

## 何时读取

当任务涉及开发/测试环境、服务器、Docker、容器、运行日志、服务异常、Nacos 或 trace 时，先读取本页，
再依次读取环境注册表、存在时的本机绑定和对应环境的本地 snapshot。普通源码任务不读取这些运行时文件。
运行时错误先根据下表定位仓库，再读取该仓库的局部 `AGENTS.md` 与相关代码、配置和契约。

## 源码已验证的逻辑服务

| Repository | Logical service | Runtime role | `company-dev` evidence |
| --- | --- | --- | --- |
| `c-drone-inspection` | `b-inspection-platform` | 巡检业务、设备消息消费与控制 | container observed |
| `c-iot-server` | `c-iot` | IoT 消息、物模型、Data Rule 与下行服务 | container observed |
| `c-iot-gateway` | `c-iot-gateway` | 协议接入、连接和设备消息上下行转发 | container observed; active state is snapshot-only |
| `c-wvp` | `c-video-center` | 视频控制面、媒体节点与播放/录像生命周期 | container observed |
| `ad-iot-codec-adapter-dji` | in-process adapter | 由 `c-iot-gateway` 装载的 DJI 编解码与映射 | source-confirmed embedded component; runtime loading not observed |
| `ad-iot-codec-adapter-robotDog-zhiyuan` | in-process adapter | 协议适配器角色已登记 | runtime loading unknown |
| `c-gateway` | `c-gateway` | 统一入口、路由与鉴权 | container observed |
| `c-system` | `c-system` | RBAC、基础用户信息与系统管理 | container observed |
| `c-tag` | `c-tag` | 标签资源与数据权限 | container observed |

上述 logical service 名称来自各仓库的应用配置；它们不证明任一服务已部署到 `company-dev`。

## Shared Framework Dependency

`star-framework` 是 Maven 多模块共享框架，而非本产品的 Runtime Service 或部署节点。它通过
`fw-*` artifact 提供 Web、RPC、MQ、Security、Redis、异步任务等横切能力；某个仓库声明或传递引入这些
artifact，只能证明其构建期消费关系，不能证明目标环境已经部署了 `star-framework`，也不能替代该服务当前 JAR 的版本核验。

涉及 trace、日志、Feign、MQ 或异步排障时，先读
[共享框架能力溯源](framework-capability-provenance.md)，再按其中的版本和入口回到 `star-framework` 与业务仓库源码。
`star-framework` 不得画入 Deployment Architecture；它只应作为 Runtime Capability Provenance 图中的 provider。

## 逻辑依赖与观察入口

| Component | Source-confirmed relationship | `company-dev` evidence |
| --- | --- | --- |
| Nacos | `b-inspection-platform`、`c-iot`、`c-iot-gateway` 与 `c-video-center` 配置其服务/配置接入 | container observed |
| Redis | 产品业务与 IoT 运行态、视频控制面分别使用 Redis；数据所有权以现有架构页为准 | container observed |
| RocketMQ | 设备事件、业务投递与视频事件的消息边界 | nameserver and broker containers observed |
| MQTT / EMQX | `c-iot-gateway` 的设备协议接入；具体 broker 与运行实例待核实 | MQTT-named container observed, role/health unknown |
| MySQL、TDengine | 服务配置与已维护架构资料表明的持久化边界 | containers observed |
| ZLMediaKit | `c-wvp` 管理媒体节点；ZLMediaKit 承担媒体数据面 | container observed |

抽象服务关系与排查边界见既有的
[P1-P4、P3-1 技术栈与系统架构](../architecture/p1-p4-technology-and-system-architecture.md)。该页是
逻辑架构，不是 `company-dev` 的部署快照。

## 本地 Runtime Snapshot 规范

本机 binding 的结构及 `company-dev` 的非敏感拓扑见 [Deployment Architecture V1](deployment-architecture.md)。
在完成只读勘察后，在 `.runtime.local/company-dev/` 创建 `runtime-snapshot.md` 与 `deployment-map.yaml`。
它们必须保持忽略，且不得记录 secret。可记录真实主机、Docker、容器、镜像、绑定端口、挂载、网络、日志路径和
证据时间；commit 前只能把已验证、稳定且非敏感的抽象结论提炼回本产品知识。

## 新环境接入

新增测试或其他逻辑环境时：

1. 在环境注册表新增 logical environment，不以服务器编号作为标识。
2. 在 `~/.ssh/config` 新增该环境的 SSH alias，并由现有 company-scoped public key 获得服务器账号授权。
3. 在 `runtime.local.yaml` 以 `targets[]` 将 Runtime Shortcut 绑定到 logical environment 与 SSH alias。
4. 先执行只读 Runtime Reconnaissance，生成本地 snapshot，并由人工审核映射、遗留服务与中间件用途。
5. 仅同步已验证、稳定、非敏感的结论到本产品知识。

公钥注释或别名变更前应先检查既有 SSH 配置的引用；不应为了命名而重建密钥或破坏现有连接。

## 待人工核实

- logical service 到 Compose stack/JAR 的精确映射，以及历史遗留或弃用单元。
- 各中间件的实际用途和依赖方向。
- Docker stdout 与文件日志的实际可用性、真实日志路径和轮转结果。
- `traceId` 在 RPC、异步、RocketMQ、MQTT 与 WebSocket 边界的传播语义。
