# Runtime Context 使用与维护指南

本页面向使用或维护 Workbench Runtime Context 的工程师，是 Human Usage Guide，不是 Codex Runtime Contract、
Product Truth、Runtime Snapshot、Secret Store 或 MCP 文档。Codex 的实际行为始终以根
[`AGENTS.md`](../../AGENTS.md) 为准。

## Authority 与存储边界

| 位置 | Authority / 用途 |
| --- | --- |
| `AGENTS.md` | Codex Runtime behavior authority |
| `core/registry/environments.yaml` | Logical Environment Registry |
| `runtime.local.yaml` | Local Runtime Binding (Shortcut → Environment → SSH alias) |
| `products/<product>/runtime/` | Durable Runtime Knowledge |
| `.runtime.local/<environment>/runtime-snapshot.md` | Local Runtime Snapshot |
| `.runtime.local/<environment>/deployment-map.yaml` | Local Physical Deployment Mapping |
| `.runtime.local/<environment>/access.local.yaml` | Local Runtime Access (Dev/Test diagnostic credentials) |
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

已知的 Runtime Evidence（例如环境、服务、时间窗、`traceId`、已收到的事件、状态快照或脱敏异常摘要）应直接提供并复用，但不能直接当作 Root Cause。范围未知时，Agent 从这些事实推导最小 Runtime / Code Scope；已确认的服务或日志 Path 可以收窄调查。紧急 Incident 以恢复速度优先，可直接给出已知环境、服务、部署和代码 Path，但仍须保留 evidence-based diagnosis。

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

`runtime.local.yaml` 已被 Git Ignore；它只将 Runtime Shortcut 绑定到 Logical Environment 与本机 SSH alias，不保存凭据。

### Local Runtime Access

Runtime Context = AI 知道系统是什么；Runtime Binding = AI 知道去哪；Runtime Access = AI 有能力读取 Runtime
Dependency；Diagnostic Skill = AI 知道怎么查。四者共同形成：

```text
Context + Binding + Access + Diagnostic Procedure
```

在公司策略允许且仅面向 Dev/Test 时，将本地访问信息写入
`.runtime.local/<environment>/access.local.yaml`。以提交的
[`runtime-access.example.yaml`](../../runtime-access.example.yaml) 为模板；不要创建真实值的 committed 文件。
Local Runtime Access V1 不支持 Production credential；任何生产诊断都必须另行 Explore 公司策略、审计、审批、隔离和操作留痕。
该文件可以包含 MySQL、Redis、Nacos 以及按需的 RocketMQ 连接信息和轻量 `privilege`（`readonly` 或
`elevated`）。`privilege` 描述凭据潜在能力，不是给 AI 的授权：诊断无论哪种值都只执行 read-only 操作。

推荐使用最小权限账号：MySQL diagnostic readonly user（SELECT/schema metadata）、Redis read-oriented ACL、
Nacos read-only configuration/service query、RocketMQ query/inspect。此轮不创建或修改这些账号。

进入依赖证据阶段时，诊断流程先检查该文件对应 provider 的 entry；缺失时报告
`Runtime access not configured for <dependency>`，并停在 `Next Evidence`，不猜测凭据。回复、日志和快照只可记录
`MySQL access: configured` 这类状态，不输出值或包含凭据的完整连接字符串。

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
7. 将当前 snapshot 保存在 `.runtime.local/`；如配置了依赖访问，则将其单独保存在 `.runtime.local/<environment>/access.local.yaml`。
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
| Local-only | `.runtime.local/<environment>/` | Physical Runtime Snapshot、Deployment Mapping、Container、Image、Port、Mount、Log Path、当前 Runtime State |
| Local-only | `.runtime.local/<environment>/access.local.yaml` | 公司策略允许的 Dev/Test Runtime Diagnostic access；不得进入输出、日志或 Product Truth |
| Local-only | `~/.ssh/config` | Host、User、IdentityFile |
| Never Store | Workbench / committed docs / `.runtime.local/` | SSH private key content、个人密码、生产凭据、无关 API Secret、客户 Secret |

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

不要把 Runtime Snapshot 当作 Product Truth，也不要把 access.local.yaml 的值复制进 snapshot。Runtime 任务先从产品的
[`runtime/index.md`](../../products/company/device-inspection-platform/runtime/index.md) 进入，再按问题读取最小的
Deployment、Observability 或 Framework Capability 页面。

## Runtime Cognition v1

Runtime Cognition v1 复用既有目录与 Authority，不建立新的 Runtime 数据库、顶层目录或历史快照体系。

| Layer | Location | Purpose | Authority boundary |
| --- | --- | --- | --- |
| Product Runtime Cognition | `products/<product>/runtime/` | 服务职责、稳定依赖、代码入口、日志与关联方式 | Durable Product Truth；不保存环境瞬时状态。 |
| Local Runtime Routing Index | `.runtime.local/<environment>/deployment-map.yaml` | Agent Runtime Routing Index：将逻辑服务连接到 repository/module、Spring service、container、Nacos service、日志入口、依赖与 Trace capability | Local environment binding；引用 Product Truth 与代码，不成为第二个产品知识权威。 |
| Runtime Snapshot | `.runtime.local/<environment>/runtime-snapshot.md` | Last Known Runtime State：当前容器、资源、Nacos 查询结果、异常摘要与证据缺口 | Point-in-time local evidence；不是诊断结论或历史记录。 |
| P8 Framework Capability Evidence | 产品 Runtime 的 framework provenance 页面与 `star-framework` 源码 | MDC、Feign、MQ、异步等 build-time capability 的来源与边界 | Source evidence；不等于容器已经加载或验证该能力。 |

`deployment-map.yaml` 只保存稳定的 routing join：逻辑服务到代码、服务名、容器名、Nacos 名称、日志选择器、主要依赖、Trace capability 和 `source_refs`。它不得保存 health、restart count、CPU/Memory、image history、故障、凭据或全量接口、Topic、表清单。

`runtime-snapshot.md` 只维护一个当前快照，最少包含 `captured_at`、`environment`、`freshness`、host baseline、container summary、Nacos evidence、current observations、evidence gaps/unknowns 和 safety note。快照不保存 raw logs、password、token、secret、完整业务 payload 或完整连接串。

### Explore modes

**Targeted Runtime Explore（默认）** 从用户现象和已知 Evidence 出发：读取 Routing Index，加载最小 Code Evidence，取得最小 Runtime Evidence，在每个边界比较输入、接受/处理结果和可观测输出，定位 first mismatch boundary；只有证据要求时才扩大仓库、容器或中间件范围。自主路由用于降低不确定性，定位边界后不为完整性扫描无关 Runtime。

**Baseline Runtime Explore（显式）** 仅在用户明确要求“环境巡检”“刷新 baseline”或等价目标时，才采集 Docker inventory、网络、主机资源和全体容器基线。默认 Explore 只报告本轮证据；用户明确要求刷新/记录时才更新忽略的 local snapshot，仍不得修改目标 Runtime。

### Runtime Explore safety

Explore 默认只读。允许使用 `docker ps`、安全字段的 `docker inspect`、`docker logs`、`docker stats --no-stream`、Docker network read、`uptime`/`free`/`df`、authorized readonly Nacos query，以及源码和非敏感配置结构读取。

Explore 默认禁止 `restart`/`start`/`stop`/`rm`、`compose up/down`、`chmod`/`chown`、MySQL/Redis/MQ/Nacos 写操作、deploy/pull 和任何产生业务副作用的 `docker exec`。V1 不将 `docker exec` 纳入默认 allowlist；需要变更时必须离开 Explore，并获得相应的 Plan / Execute 授权。

### Runtime state suitability and mutation gate

Preflight 不只是检查节点是否 `running`；它应先判断当前状态是否适合**该环境与本轮验证场景**：

```text
Observed Runtime State
        ↓
Deployment Intent
        ↓
Environment Role
        ↓
Current Operational Intent
        ↓
Expected State
        ↓
Normal / Fault / Not Applicable / Unknown
```

- **Deployment Intent** 是 Compose、Helm、deployment config、restart policy 或 service mapping 所说明的静态部署能力或通常形态；它不能单独证明某服务此刻必须运行。
- **Environment Role** 回答该 Logical Environment 是否承载当前问题或验证场景。
- **Current Operational Intent** 是当前时间点允许运行、暂时停用、切换或迁移的动态事实，须由可用运行记录或 Human Context 确认。
- 只有当前状态违反已建立的 Expected State 时，才是 Runtime Fault；若环境不承载该场景，Verification 应标为 `Not Applicable`；角色或意图未知时标为 `Unknown`，并输出 `Need Human Context`。

在提出或执行 `start`、`restart`、`stop`、`deploy`、`redeploy`、`scale`、`clear`、`delete`、`migrate` 或运行配置修改前，依次确认 Environment Role、Current Operational Intent、Expected State 和实际违例，再取得针对该动作的 Human Approval。不得只凭 Deployment Intent 推荐恢复或重启。

### Human Evidence Bridge

Executor 因权限、SSH、网络、Runtime policy 或副作用审批不能继续时，不把约束解释为诊断结论，也不绕开安全边界。应停止推断，输出最小 `Need Evidence`，由 Human 提供脱敏证据或明确的操作意图后，继续既有 Evidence Chain。Human-assisted Execute 是受控证据桥接，不是 Runtime Diagnostic 的失败模式。

## Runtime phase status

```text
Runtime Phase 1 — Runtime Context / Routing: FROZEN
Runtime Phase 2 — Runtime Diagnostic: FROZEN
Next: Phase 3 — Integration Verification
```

冻结表示当前能力已达到日常使用标准：后续只接受“真实问题 → 已验证 Gap → 最小增量修复”的 usage-driven evolution，不主动扩展 Runtime framework、目录、DSL 或自动化平台。
