# P0 运行时约束

本文件是 P0 作为 Primary（主仓库）时 Codex 的最小运行时入口：先定义**工程范围、工程任务必读基准、任务阶段与条件读取、角色边界、指令优先级和事实可信度**，再将公共约束作用于本会话识别出的范围内仓库。Primary 只提供公共协作约束，不自动成为任务的代码阅读、核实或修改范围，也不以 P0 文档替代目标仓库的局部约束与代码。本文件不能覆盖 Codex 平台、系统或开发者施加的约束。`README.md`、`docs/` 与产品文档用于人工维护或在下列条件满足时按需读取，不是默认上下文。

## 1. 会话范围与路径地图

当 P0 被设置为 Primary 时，Codex 每次任务都应先读取本文件的公共约束，无需用户重复提及 `P0`。会话首次任务中，从用户的直接说明识别项目标记；仅当识别到标记时，读取 [`core/registry/repositories.yaml`](core/registry/repositories.yaml) 确认它是否已登记、对应工程及产品绑定。除 Primary 的默认加载外，已登记标记共同构成本次可操作范围，后续消息沿用该范围，直到用户明确变更。引用的示例、代码块、文档标题、路径或历史记录中的项目标记不自动扩大范围；语义不明确时先确认，不猜测扩大范围。

项目标记可出现在自然语言、列表、括号或可选的 Stage Shortcut 前后；`范围：` 只是可选前缀。短横线 `-` 或连接号 `–` 仅展开连续的已登记主序列（如 `P0–P7`）；带连字符的独立标记（如 `P0-1`、`P0-2`、`P3-1`、`P4-1`）不拆分，未登记标记也不能由范围语法推断。用户始终可以自然语言描述任务；Stage Shortcut 只是可选加速器，不是使用前提。

项目标记只用于 P0 的会话范围和跨仓库导航；目标仓库及其生成物必须使用实际工程名、服务名、模块名或领域术语，不得把项目标记写入源码、注释、日志、配置、数据库说明、测试、接口说明或新文档。项目标记作为优先级、阶段、变量或协议/型号值时可按原语义保留。

需打开、核实或修改已登记源码时，读取未提交的 `workspace.local.yaml` 获取本机绝对路径；其仅保存路径，仓库身份与产品绑定以 registry 为准，产品内责任以对应 repository manifest 和已验证产品知识为准。首次接入且该文件不存在时，可从 `workspace.example.yaml` 创建；缺少条目或路径不可访问时，报告缺口，不猜测替代位置。范围外项目仅可作为依赖背景，不读取、核实或修改其源码。

### Baseline Constraints and Context Routing

根 `AGENTS.md` 始终是 Workbench Runtime 入口：先识别用户任务的 scope、task semantics 与是否为 engineering task。工程任务按第 2 节加载 Baseline Engineering Constraints：[`core/rules/development.md`](core/rules/development.md) 与适用的 repository / directory local `AGENTS.md`；随后才按任务语义做 Context Routing。这里的先后是逻辑 Authority 层级，不要求所有任务机械读取全部文档；非工程知识查询不默认加载 `development.md`。

`DF-YYYYMMDD-NN` 是 Delivery 的 durable identity 与 Context Address，不是 Baseline Constraint。对“继续 / 查询 / 关闭 DF-xxxx”，在 Delivery routing 内先于 `work/active/` 按 DF ID 定位 Package；未找到时读取 `work/closed/` 的 Thin Context Index，并仅在该索引指向时访问 local/external cold archive。随后读取 `task.yaml`、`resume.md` 与当前 Phase Artifact，或 Closed Index 的 Product Truth links、repositories、capabilities、related deliveries 和 archive reference。

再按该入口记录的 `product`、capabilities 和 repositories 渐进读取最小相关 Product Truth、真实项目代码/契约与 Core 方法；只有任务确实需要时才加载 Plugin Skill。解释当前产品能力时从 `products/` 入口开始；解释工程方法时从 `core/` 开始；不要默认扫描整个 `products/`、`work/` 或 `plugins/`。完整模型见 [Living Engineering Model](docs/workbench-model.md)。

## 2. 工程任务必读基准

凡是阅读、评审、设计或修改源码、配置、脚本、测试的任务，必须先读取 [`core/rules/development.md`](core/rules/development.md)。它是所有服务通用的 Codex 开发基准，规定上下文装载、分析与确认、最小实现、调试、验证、交接和安全边界；随后按第 3 节读取目标仓库或目录的局部 `AGENTS.md`，以及任务命中的专项上下文。语言、框架、仓库和产品专属要求仍按条件读取，且仓库局部约束优先。

纯知识维护、纯文案或不涉及工程实现的问答不默认读取该规则；它们仍须遵循第 1 节的范围规则与第 4 节的指令、事实和安全边界。

### 快速判定

| 任务情形 | 在本入口基础上的最小读取 |
| --- | --- |
| 纯问答、纯文案或纯知识维护 | 第 1、4 节及已适用的局部 `AGENTS.md`；不默认读取 `development.md`。 |
| 单项目工程任务 | `core/rules/development.md`、目标局部 `AGENTS.md`、相关代码/契约/测试。 |
| 涉及服务关系、公开契约或多个项目 | 单项目工程任务的读取项，再按第 3.2 节读取最小必要的产品资料与受影响仓库事实。 |
| 维护 P0 运行时规则、Core、脚本或校验 | `development.md`、受影响文件和第 3.2 节对应的维护资料；不加载无关产品知识。 |

## 3. 任务阶段与条件上下文

### 3.1 Engineering Task Loop Stage Shortcuts

自然语言是默认入口。Stage Shortcut 应位于消息的任务头部区域，可出现在可选 Repository Scope 之后、主要自然语言任务正文之前，并作为独立 token / 独立标签出现：`Explore` / `E`、`Plan` / `P`、`Execute` / `X`、`Verify` / `V`；长写、短写和大小写均等价，也可带 `:`。这是人机快捷约定，不是严格 Parser 或新 DSL；正文中的普通字母不触发识别。独立 `P` 是 Plan，`P1`、`P2`、`P3-1` 等始终是项目标记。未使用 Shortcut 时，仍根据用户的自然语言任务语义选择适用的 Role、Playbook 和 Skill。

默认协作输入是 Human 提供 Goal 与已知 Evidence，并仅在确定时提供 Confirmed Boundary；Agent 通过 Context Routing 推导调查 Scope，Human 无须预先定位 Repository、服务、类、数据或日志路径。Human 的 Hypothesis 只是调查线索而非事实；Agent 应直接复用已知 Evidence，并在不确定性已足够降低时收敛，不因自主路由而扩展为全量探索。

- **Explore / E — Prove the solution is viable**：默认不修改任何 tracked file（生产代码、测试、配置、文档或脚本），不提交、不推送、不发布，也不执行外部业务副作用；可读取代码、配置、契约和必要产品知识，搜索调用链，并运行只读命令、现有测试、诊断命令或不会产生持久修改的验证。先核实现状、Goal、事实/假设/未知和 change / integration seam；再以证据验证方案成立所依赖的关键可行性与约束（如现有扩展点、架构/契约兼容性、外部能力、性能或前置条件）；最后收敛出足以进入 Plan 的推荐方案、影响范围、Non-scope、风险/约束、Verification Strategy 与未决前置条件，必要时说明替代方案及取舍。产物是附 Evidence / Reasoning 的 Viable Solution：可行但不要求边界和实施细节已经完整，也不展开成逐步实施计划；关键未知项仍会阻塞 Plan 时，继续验证而非完成 Explore。完成后停在方案评审，不开始实施。
- **Plan / P — Make the solution complete and executable**：Codex Plan Mode（当前产品表面提供时）基于 Explore 的 Viable Solution 补齐与正确实施相关的 Scope / Non-scope、边界与约束、失败/边缘路径、Change Map、依赖与兼容性、执行顺序、Verification Plan 和 Stop Conditions，形成可安全进入 Execute 的 Executable Plan；简单任务保持短小，复杂度或风险需要时才展开。Plan 不重新无依据选择技术方向，也不机械先列 todo；若新事实使可行性不再确定，携带证据回到 Explore。默认不实施、不自动扩大 Scope、新增 Repository、修改公开 Contract、引入 DB Schema，或调整权限/数据隔离模型；若产品 UI 提供执行该计划的原生 Action，优先使用它，不另要求输入 `X`。
- **Execute / X — Change inside the approved boundary**：在没有原生 Plan 执行 Action，或 Plan 后继续讨论并重新收敛、或恢复已有明确边界时使用。若当前 Thread 有唯一、明确、无未决关键决定、未被新证据推翻的最新 Plan，`Execute` / `X` 即表示用户确认该 Plan 并授权本轮实施；若存在互斥方案、关键未决项、新证据或实质 Scope 冲突，先回到 Plan。只在已确认 Scope 和 Files / Components 内实施，遵守 Stop Conditions，不顺手优化或重新发散设计，并完成适当 Verification。若没有可识别 Plan，只有 Level 1 的明确小改可按用户当前说明直接实施；非平凡任务先说明缺少执行边界。`Execute` 授权本轮代码修改，但不自动授权 commit、push、release、deploy、生产写入、外部系统变更、付费或破坏性操作。
- **Verify / V — Prove the result with evidence**：先明确本轮 Verification Target，再按目标、风险、环境、可访问依赖和用户要求选择 Static Review、Automated Verification、Targeted / Scoped Smoke 或 Integration / Runtime / E2E；这些 Depth 不是强制逐级执行。Verification Boundary 默认沿证明 Target 所必需的调用链传播，跨越 Service / Module / Repository 本身不是停止条件；但用户显式 Verification Scope / Non-scope 和当前 Repository Scope 是硬边界，不自动扩大读取范围或获得写权限。V 可在没有当前 Execute 时独立审核现有代码；完整 E2E 不可用时，仍应优先尝试能证明目标行为的最小 service/component smoke。逐项报告 passed、failed、not executed 或 not verifiable、Evidence 与 Verdict，且结论不得超过证据覆盖范围。失败时先报告证据，默认回到 Explore；若只是 Plan 边界缺失可建议回到 Plan。除非用户明确要求继续修复，Verify 本身不授权新的生产代码修改。

Stage Shortcut 给出默认行为；用户本轮最新明确补充提供问题、范围和额外约束，可收窄或覆盖默认行为，但仍受指令优先级约束。例如 `E` 后明确允许新增临时测试，只放宽该测试级修改，不授权其他 tracked file 修改。K2 或其他非后端任务没有适用角色时，不强行套用 Java 角色。

### 3.1.1 Runtime Target Hint

自然语言仍是 Runtime 任务的默认入口；`ssh <shortcut>` 是可选的 **Runtime Target Hint**，不是新的 DSL。例如 `P3 ssh 150 E 排查设备离线` 中，项目标记用于 Repository Scope，`ssh 150` 只指定目标运行时，`E` 仍定义只读 Explore 边界。普通源码任务不因存在此约定而加载 Runtime Context。

出现该 Hint 时，先读取 [`core/registry/environments.yaml`](core/registry/environments.yaml)，再仅在存在时读取忽略的仓库根 `runtime.local.yaml`。该 local overlay 的 `environments.<logical-environment>.targets[]` 将用户 shortcut 绑定到本机 SSH alias：唯一命中时以该 alias 作为实际 SSH target；未命中时报告 `Runtime shortcut not configured`；重复命中时停止并请求用户确认。不得猜测 IP、SSH alias 或未配置 mapping；服务器编号不是 logical environment identity，也不得写入环境注册表。Runtime binding 只负责路由；依赖凭据必须从 `.runtime.local/<environment>/access.local.yaml` 单独读取。

Runtime Target Hint 只选择 Runtime Context，绝不授予 restart、stop、start、deploy、Docker Compose、数据库/中间件写入、文件修改或 cleanup 权限，也不改变 `E / P / X / V` 的权限模型。`runtime.local.yaml` 只保存 Shortcut → Logical Environment → SSH Alias 绑定；`.runtime.local/<environment>/access.local.yaml` 可在公司策略允许时保存 Dev/Test Runtime Diagnostic 所需的本地访问信息，必须保持忽略。模板见 [`runtime.example.yaml`](runtime.example.yaml) 与 [`runtime-access.example.yaml`](runtime-access.example.yaml)。

### 3.1.2 Product Truth Sync Shortcut

`Sync` / `S` 是独立的 Product Truth Sync Action，不是 Engineering Task Loop 的第五个 Stage，也不改变 `E / P / X / V`。它可位于任务头部、可选 Repository Scope 之后，以独立 token / 标签出现；`S1` 始终是 Repository Scope，不会被识别为 `S`。`P0 S` 的含义是允许在 `tu-engineering-workbench` 执行该 Action：基于当前 Thread 已有的实现、契约和 Verification Evidence，判断是否应最小更新 `products/` 中现有的 canonical Current Product Truth 页面。

Sync 不要求 DF、Active Delivery 或 `work/`；也不关闭 Delivery、Archive、修改 `task.yaml` 或 `knowledge_update_assessment`。只有事实同时为 **Verified、Current、Durable、Independently Valid** 时才可同步；否则分别报告 `not-needed`、`not-ready` 或 `insufficient-evidence`，且不写 `products/`。优先使用当前 Thread 已有证据；重新读取业务仓库需要已在 Scope 内，不能因 Sync 自动扩大范围。Sync 仅可最小修改 P0 `products/` 及必要的 canonical navigation links，不写 `work/`、源代码仓库、Archive，也不 commit、push、release 或 deploy。属于 Delivery 的事实可在其间独立 Sync；Delivery Closing 仍负责整个 Delivery 的最终 Product Truth reconciliation。

若已安装团队插件 `ai-guidance-workflows`：用户显式调用可用的 `tu-` Skill 时，使用该 Skill 并遵循其 `SKILL.md`；未显式调用时，按已安装 Skill 自身的触发描述和任务语义判断是否适用。未安装 Plugin 或没有适用原生 Skill 时，继续遵循本文件引用的 Core 工作流。仅出现多个项目标记但未说明服务交互时，不自动加载 P1–P4、P3-1 的全局上下文；先确认关联边界或分别按单项目任务处理。

### 3.2 按任务叠加读取的上下文

本节只列出**第 2 节工程基准和已适用局部 `AGENTS.md` 之外**的额外读取项；每行都是独立条件，命中多行时叠加读取，未命中时不为“可能有用”而加载。普通单项目工程任务按第 2 节读取目标局部约束、相关代码、调用方、契约与测试即可，不默认读取产品目录、使用教程或知识治理文档。

| 条件 | 额外必读项 | 不默认读取 |
| --- | --- | --- |
| 维护 P0 的运行时入口、`core/` 公共规则、角色、工作流或契约 | `docs/governance/authoring-guide.md` 的“公共规则维护”，以及受影响文件 | 产品知识、治理规范、使用教程 |
| 维护 P0 的产品知识、架构、流程、服务边界、清单或交付记录 | `docs/governance/authoring-guide.md`、`docs/governance/governance.md`，以及受影响的权威页面 | 其他产品目录与所有使用教程 |
| 修改 P0 的工具、脚本、校验或团队 Plugin | 目标目录的 README、实现与测试；Plugin 还读取 manifest、相关 `SKILL.md` 与 `tests/test-plugin.sh` | 产品知识、知识编写规范、无关 Plugin |
| 用户明确指定 P0-2 并明确提出 VPS 部署、升级、调整、网络排查、性能或稳定性问题 | 通过 `workspace.local.yaml` 定位 P0-2，再读取 P0-2 的 `docs/vps/AGENTS.md` 和当前链路所需资料；涉及实现时仍读取本仓 `development.md` 与 P0-2 的 `vps-init/README.md` | 仅因 P0 是 Primary、偶然提到 VPS、一般网络问答或无真实 VPS/网络目标的仓库开发，不触发该专项入口 |
| 任务明确含 `ssh <shortcut>`，或涉及开发/测试 Runtime、Docker/container、日志、trace/`traceId`、Nacos、Runtime Service 或服务运行异常 | 先读取 `core/registry/environments.yaml`，再在存在时读取忽略的 `runtime.local.yaml`；由唯一 resolved logical environment 的 `product` 读取 `products/<product>/runtime/index.md`，随后只按任务读取 `deployment-architecture.md`、`observability.md` 或 `framework-capability-provenance.md` | 普通源码任务、未命中的 Runtime 专题页、所有本地 snapshot 和未解析的 Runtime Target |
| 任务涉及多个已登记项目，或明确涉及服务关系、OSD、指令、协议、缓存链路、公开 Contract、数据所有权或跨服务发布依赖 | `products/company/device-inspection-platform/index.md`，再沿链接读取当前已维护的最小 Flow 或 P1 入口/缓存资料；未覆盖场景以目标代码、契约和配置核实 | 整个产品目录、无关服务源码 |
| K1/K2 的 Knowledge Hub 产品架构或跨端任务 | `products/personal/knowledge-hub/index.md`，再沿链接读取所需资料 | 无关公司产品材料 |
| L1 的软考高级系统架构师学习沉淀任务 | `products/personal/architecture-learning/index.md`，再沿链接读取所需资料 | 无关产品材料 |

涉及多个仓库、公开 API、消息契约或数据所有权时，必须先以目标代码和契约核实当前事实；产品知识只用于导航与已确认上下文，不能替代代码核实。

## 4. 指令、事实与安全边界

### 4.1 指令优先级

指令冲突时，按以下顺序处理：**Codex 平台、系统和开发者约束 > 用户最新明确要求 > 目标仓库或目录的局部 `AGENTS.md` > 本文件与 Core 公共规则 > 产品文档和示例**。同一层级的补充约束应一并遵循；只有同一事项互相矛盾时才采用较高优先级来源。用户授权可满足平台要求用户审批或确认的前提；但不能覆盖平台、系统或开发者的禁止性约束及实际权限限制。

`core/playbooks/` 是仓库级方法参考，不等同于 Codex 平台可触发的 `SKILL.md`。适用的 Codex Skill 必须先读取并遵循；Playbook 只在不冲突时补充执行方法，不能覆盖平台、系统或开发者约束。

### 4.2 事实可信度

当前代码、契约、配置、测试和可复现命令结果用于证明**当前事实**；带证据的产品知识用于提供已确认上下文；Core 规则和示例只提供通用方法，不能证明现状。当前代码不能否定用户已授权的目标变更，只能说明变更前状态和兼容性影响。未知项标为待核实。

Committed Workbench（包括 `core/`、`products/`、`docs/`、`plugins/`、`runtime.example.yaml` 和 `workspace.example.yaml`）永远不得保存 password、token、private key、credential value、Cookie 或其他 Secret。`.runtime.local/` 是仅限本机的 Dev/Test overlay，可按公司策略保存诊断所需访问信息，但不得进入 Git、Product Truth、诊断输出或日志；生产凭据、个人密码、SSH private key 内容和无关 Secret 永不保存。凭据存在不等于获得写权限，Runtime Diagnostic 与 `E / P / V / X` 默认仍为只读。

### 4.3 风险操作与平台审核

风险判断以受影响的公开契约、数据语义、权限、安全、生产或外部状态及操作可逆性为准；文件数量、改动行数或一次工具调用涉及多个路径本身不构成高风险。

识别出高风险操作时，先向用户说明具体风险原因、影响范围、推荐方案和备选方案，再请求用户决策。除非平台或系统层明确禁止，不得因风险较高而直接终止且不询问。

工具调用若被平台自动审核拒绝，应明确说明这是平台限制，不将其表述为用户拒绝或任务已完成。先判断能否在不改变用户目标的前提下缩小为可安全执行的步骤；不能时，必须向用户发起明确授权申请，而不是因一次拒绝结束、归档或交接任务。授权申请须列明被拒绝的操作与精确对象、审核给出的原因或权限缺口、推荐的继续方案和可选的缩小范围；等待回复期间，任务保持未完成状态。用户授权可满足该操作的用户审批前提；在平台允许执行时，仅重试已获授权的最小操作，并继续原任务。AGENTS 约束不得覆盖平台、系统或开发者的禁止性约束及实际权限结果。

遇到权限不足、沙箱限制、平台拦截，或授权请求未成功发出/未获得结果时，不得自行终止任务、将任务表述为已交接，或仅让用户手动执行命令。必须在本次响应中向用户发起明确的授权或决策请求，说明：受阻操作与精确对象、受阻原因和影响范围、推荐的授权/继续方案，以及可选的缩小范围、替代实施或暂缓方案；该响应只能作为等待用户决定的暂停点，不能宣称任务完成。在用户作出选择前，继续完成不依赖该权限的核实工作；用户授权后继续原任务，不要求用户重新描述目标。仅在平台或系统明确禁止再次请求授权时，才说明限制并交接可执行选项。

### 4.4 计划执行与完成声明

当 Codex 在本次**实施任务**中对用户列出计划、待办或执行步骤后，该计划即构成完成承诺：必须逐项执行并核验，不能只完成其中一部分就宣称任务、计划或实施已完成。仅产出方案且未获实施授权的任务不适用本节的执行要求；其计划须明确标注为待后续实施的建议。

如任一已列步骤无法完成，Codex 必须在交接中逐项列出未完成内容、无法完成的具体原因、已尝试或已核实的证据、受影响范围，以及可行的下一步；在剩余步骤依赖该阻塞时，必须明确说明计划未完成。不得将未执行、被拒绝、缺少权限、缺少依赖、验证失败或等待用户决策的步骤表述为已完成。

### 4.5 现有风格与持久化约定复用

修改代码前，Codex 必须先核实目标模块中同类实现、局部规则和框架约定，并以其作为命名、分层、异常处理、测试和依赖使用的首选风格；已有可复用的基类、公共组件、Mapper/Repository 模式或业务抽象时，必须直接复用，不得无依据另建平行实现。

新增或修改数据库表、实体、ORM 映射、迁移脚本或查询前，必须先检查目标仓库已有的实体基类、审计字段、创建/更新人和时间填充机制、逻辑删除策略、主键与命名规则、默认值、索引和同类表。应复用已验证的字段与框架机制，并同步处理查询过滤、唯一约束和迁移兼容性；不得凭空新建字段、重复审计列、绕过逻辑删除，或因未检查既有约定而引入不一致的表结构。

若目标仓库不存在可复用约定，或现有约定彼此冲突、无法从代码/配置/迁移中确认，必须明确证据缺口和拟采用方案；涉及公开数据语义或迁移风险时，先取得必要确认后再落库。
