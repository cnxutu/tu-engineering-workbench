# Runtime Context 使用与维护指南

本页面向使用或维护 Workbench Runtime Context 的工程师，是 Human Usage Guide，不是 Codex Runtime Contract、
Product Truth、Runtime Snapshot、Secret Store 或 MCP 文档。Codex 的实际行为始终以根
[`AGENTS.md`](../../AGENTS.md) 为准。

## Authority 与存储边界

| 位置 | Authority / 用途 |
| --- | --- |
| `AGENTS.md` | Codex Runtime behavior authority |
| `core/registry/environments.yaml` | Logical Environment Registry |
| `runtime.local.yaml` | Local Runtime Binding |
| `products/<product>/runtime/` | Durable Runtime Knowledge |
| `.runtime.local/` | Local Runtime Snapshot |
| 本页 | Human Usage Guide |

## Runtime 四层模型

```text
Runtime Shortcut
        ↓
Logical Environment
        ↓
SSH Alias
        ↓
Physical Runtime
```

当前本机可按以下方式理解：

```text
150
↓
company-dev
↓
<local SSH alias>
↓
physical development server
```

`150` 只是用户本机习惯使用的 Runtime Shortcut；它不是 IP authority、Environment ID、Repository Scope 或
Product ID。`company-dev` 才是 Workbench 中的 Logical Environment；SSH alias 只属于本机 connection
configuration。

## 日常使用

Runtime Target Hint 是可选加速器，不是严格 DSL。Workbench 保持 **Natural Language First**：可以只说“去开发
环境看看服务状态”，也可以在任务头部写 `ssh <shortcut>` 精确指定目标运行时。

### 只指定环境

```text
ssh 150
看看当前服务状态
```

### Repository + Runtime

```text
P3 ssh 150 E
排查设备离线
```

### Trace 排障

```text
ssh 150 E
traceId xxx 帮我定位异常
```

### Runtime Diagnosis

Runtime-aware incidents use the existing Spring incident diagnostic Skill's evidence procedure. A request such as
`P3 ssh 150 E` followed by “排查设备离线” is routed through Runtime Context, targeted runtime evidence, and then the
responsible repository code. The result separates Facts, Evidence, Hypothesis, Unknown, Next Evidence, and Diagnosis;
runtime access remains read-only unless a later request explicitly authorizes a mutation.

### Runtime + Verification

```text
P2 ssh 150 V
验证这个接口当前在开发环境的实际行为
```

在这些示例中，`P3` / `P2` 是 Repository Scope，`ssh 150` 是 Runtime Target Hint，`E` / `V` 是 Engineering
Stage，余下自然语言定义任务本身。Hint 会按 `Environment Registry → local binding → product Runtime Context`
路由；普通源码任务不会因此读取 Runtime Context。

## 权限边界

`ssh 150` 只选择目标 Runtime，不自动授权 restart、stop、start、deploy、Docker Compose mutation、DB write、
Redis write、Nacos write、file modification 或 cleanup。实际权限仍由 `E`、`P`、`X`、`V` 以及用户本轮明确授权
共同决定；例如 `P3 ssh 150 E` 默认仍是 read-only。

## 新电脑首次配置

### 1. 准备本机 SSH alias

先确认 `~/.ssh/config` 中已有可工作的 SSH alias；真实公司 Host/IP 不进入 Workbench Git。占位示例：

```text
Host <company-dev-alias>
    HostName <host>
    User <user>
    IdentityFile <key>
```

真实 SSH 配置只保存在本机。

### 2. 创建 Local Runtime Binding

以仓库根的 [`runtime.example.yaml`](../../runtime.example.yaml) 为参考创建 `runtime.local.yaml`：

```yaml
version: v1

environments:
  company-dev:
    targets:
      - shortcut: "150"
        ssh_alias: "<company-dev-alias>"
```

`runtime.local.yaml` 已被 Git Ignore；它将 Runtime Shortcut 绑定到 Logical Environment 与本机 SSH alias。

### 3. 测试解析与连接

提交 Runtime 任务时使用：

```text
ssh 150
```

它应唯一解析为：

```text
150
→ company-dev
→ configured SSH alias
```

连接确认应只执行最小 read-only connectivity check；不要把它当作对服务器修改的授权。

## 新增服务器或目标

未来新增 `112` 等服务器时，不要先假设 `112 = company-test`。Physical Server 与 Logical Environment 是两层概念，
应依次处理：

1. 判断它属于已有 Logical Environment，还是需要新增一个环境。
2. 若是新环境，更新 `core/registry/environments.yaml`。
3. 在 `~/.ssh/config` 增加本机 SSH alias。
4. 按公司权限策略，将个人持有的 company-scoped public key 授权给目标服务器账号。
5. 在 `runtime.local.yaml` 增加 `112 → logical environment → SSH alias` 的 local binding。
6. 执行 Read-only Runtime Reconnaissance。
7. 将当前 snapshot 保存在 `.runtime.local/`。
8. 仅把 Verified、Durable、Non-sensitive 的结论同步到 `products/**/runtime/`。

不要因为新增服务器自动生成新 key。推荐使用一把个人持有、公司工程范围使用的 dedicated SSH key；公司安全策略允许时，
多个 Dev/Test Server 可以授权同一个 public key。Private Key 永远只保存在本机，Public Key comment 仅用于识别归属，
不参与认证语义；若公司策略要求 environment/server-scoped key，则以公司策略为准。

## Committed、Local-only 与禁止保存

| 分类 | 位置 | 保存内容 |
| --- | --- | --- |
| Committed | `core/registry/environments.yaml` | Logical Environment、Product binding、runtime model |
| Committed | `products/**/runtime/` | Repository ↔ Runtime、Deployment Architecture、Middleware Role、Observability、Durable Runtime Knowledge |
| Local-only | `runtime.local.yaml` | Shortcut、SSH alias |
| Local-only | `.runtime.local/` | Physical Runtime Snapshot、Container、Image、Port、Mount、Log Path、当前 Runtime State |
| Local-only | `~/.ssh/config` | Host、User、IdentityFile |
| Never Store | Workbench / committed docs | private key content、password、token、Cookie、DB password、Secret |

## Code ↔ Runtime Navigation

```text
Code → Runtime

P3
→ c-iot-gateway
→ company-dev
→ Runtime Unit
→ Logs / Trace
```

```text
Runtime → Code

Runtime Error
→ Logical Service
→ Repository
→ Scope
→ Source Code
```

这是 Phase 1 Runtime Context 的核心价值：让工程师和 Codex 能在代码责任与运行现象之间双向导航。

## Durable Knowledge 与 Snapshot

下列 Durable Truth 可以写入 committed Product Runtime Knowledge：

```text
c-iot → service container
company-dev → Docker runtime model
```

下列信息只属于 `.runtime.local/` 的 snapshot：

```text
某容器此刻 exited
某端口当前映射
某 image tag
某日志文件当前大小
```

不要把 Runtime Snapshot 当作 Product Truth。Runtime 任务先从产品的
[`runtime/index.md`](../../products/company/device-inspection-platform/runtime/index.md) 进入，再按问题读取最小的
Deployment、Observability 或 Framework Capability 页面。
