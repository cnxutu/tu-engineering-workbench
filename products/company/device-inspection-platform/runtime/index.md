# Runtime Context

## 范围

本页是无人机巡检平台 Runtime 任务的按需入口。逻辑环境由
[`core/registry/environments.yaml`](../../../../core/registry/environments.yaml) 定义；本机 SSH
别名由忽略的 `runtime.local.yaml` 绑定；完整的主机、容器、挂载、端口和日志路径只可保存到忽略的
`.runtime.local/<environment>/`。三者不替代现有仓库注册表、产品架构页或源码配置。

当前已登记的 `company-dev` 是逻辑开发环境，SSH 访问是用户提供的前提；其实际运行模型、物理主机和
部署单元尚未由本轮可复现的运行时勘察确认。

## 何时读取

当任务涉及开发/测试环境、服务器、Docker、容器、运行日志、服务异常、Nacos 或 trace 时，先读取本页，
再依次读取环境注册表、存在时的本机绑定和对应环境的本地 snapshot。普通源码任务不读取这些运行时文件。
运行时错误先根据下表定位仓库，再读取该仓库的局部 `AGENTS.md` 与相关代码、配置和契约。

## 源码已验证的逻辑服务

| Repository | Logical service | Runtime role | Deployment evidence |
| --- | --- | --- | --- |
| `c-drone-inspection` | `b-inspection-platform` | 巡检业务、设备消息消费与控制 | pending runtime reconnaissance |
| `c-iot-server` | `c-iot` | IoT 消息、物模型、Data Rule 与下行服务 | pending runtime reconnaissance |
| `c-iot-gateway` | `c-iot-gateway` | 协议接入、连接和设备消息上下行转发 | pending runtime reconnaissance |
| `c-wvp` | `c-video-center` | 视频控制面、媒体节点与播放/录像生命周期 | pending runtime reconnaissance |
| `ad-iot-codec-adapter-dji` | in-process adapter | 由 `c-iot-gateway` 装载的 DJI 编解码与映射 | 不是独立部署单元 |
| `ad-iot-codec-adapter-robotDog-zhiyuan` | unknown | 协议适配器角色已登记；运行装载方式待核实 | pending runtime reconnaissance |
| `c-gateway`、`c-system`、`c-tag` | unknown | 已登记的产品仓库 | pending runtime reconnaissance |

上述 logical service 名称来自各仓库的应用配置；它们不证明任一服务已部署到 `company-dev`。

## 逻辑依赖与观察入口

| Component | Source-confirmed relationship | Runtime status |
| --- | --- | --- |
| Nacos | `b-inspection-platform`、`c-iot`、`c-iot-gateway` 与 `c-video-center` 配置其服务/配置接入 | deployed status unknown |
| Redis | 产品业务与 IoT 运行态、视频控制面分别使用 Redis；数据所有权以现有架构页为准 | deployed status unknown |
| RocketMQ | 设备事件、业务投递与视频事件的消息边界 | deployed status unknown |
| MQTT / EMQX | `c-iot-gateway` 的设备协议接入；具体 broker 与运行实例待核实 | deployed status unknown |
| MySQL、TDengine | 服务配置与已维护架构资料表明的持久化边界 | deployed status unknown |
| ZLMediaKit | `c-wvp` 管理媒体节点；ZLMediaKit 承担媒体数据面 | deployed status unknown |

抽象服务关系与排查边界见既有的
[P1-P4、P3-1 技术栈与系统架构](../architecture/p1-p4-technology-and-system-architecture.md)。该页是
逻辑架构，不是 `company-dev` 的部署快照。

## 本地 Runtime Snapshot 规范

在完成只读勘察后，在 `.runtime.local/company-dev/` 创建 `runtime-snapshot.md` 与
`deployment-map.yaml`。它们必须保持忽略，且不得记录 secret。可记录真实主机、Docker、容器、镜像、
绑定端口、挂载、网络、日志路径和证据时间；commit 前只能把已验证、稳定且非敏感的抽象结论提炼回本产品
知识。

## 新环境接入

新增测试或其他逻辑环境时：

1. 在环境注册表新增 logical environment，不以服务器编号作为标识。
2. 在 `~/.ssh/config` 新增该环境的 SSH alias，并由现有 company-scoped public key 获得服务器账号授权。
3. 在 `runtime.local.yaml` 仅将 logical environment 绑定至 SSH alias。
4. 先执行只读 Runtime Reconnaissance，生成本地 snapshot，并由人工审核映射、遗留服务与中间件用途。
5. 仅同步已验证、稳定、非敏感的结论到本产品知识。

公钥注释或别名变更前应先检查既有 SSH 配置的引用；不应为了命名而重建密钥或破坏现有连接。

## 待人工核实

- `company-dev` 对应的物理主机、运行时模型和已运行服务。
- logical service 到容器/JAR/Compose stack 的映射，以及历史遗留或弃用单元。
- 各中间件的实际部署位置、用途和依赖方向。
- Docker stdout 与文件日志的实际可用性、真实日志路径和轮转结果。
- `traceId` 在 RPC、异步、RocketMQ、MQTT 与 WebSocket 边界的传播语义。
