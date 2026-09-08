# Playbook：Engineering Task Loop

## 用途

用于一个具体的 DEV、Bug、Refactor 或技术改造任务：先核实现状、验证关键可行性并收敛推荐方向，再确认实际修改边界，在授权范围内实施，并以可复现证据验证结果。它是通用工程方法，不是 Codex Skill、状态机或长期交付记录。

## 核心循环

Stage Shortcut 位于消息的任务头部区域，可在可选 Repository Scope 之后、主要自然语言任务正文之前，以独立 token / 独立标签出现；支持大小写不敏感的 `E` / `Explore`、`P` / `Plan`、`X` / `Execute`、`V` / `Verify`。`P1`、`P2`、`P3-1` 等仍是项目标记，正文中的普通单字母不触发 Stage。

1. **Explore / E — Prove the solution is viable**：先核实现状、Goal、事实/假设/未知、change / integration seam 与可复用实现；再以证据验证方案成立所依赖的关键可行性和约束（现有扩展点、架构/Contract 兼容性、外部能力、性能或前置条件）；最后收敛推荐方案、影响范围、Non-scope、风险/约束、Verification Strategy 与未决前置条件，必要时给出替代方案及取舍。Explore 的产物是附 Evidence / Reasoning 的 **Viable Solution**：足以证明推荐方向可行并进入 Plan，但不要求边界、异常、兼容和实施细节已经完整，也不展开为逐步实施计划；关键未知项仍阻塞 Plan 时，继续验证而非结束 Explore。默认不修改任何 tracked file；可读取、搜索调用链、运行现有测试和非持久诊断/验证。用户可只放宽明确允许的范围。
2. **Plan / P — Make the solution complete and executable**：Codex Plan Mode 基于 Explore 的 Viable Solution 继续 Refine、Bound、Close the Loop 和 Prepare Execution，补齐与正确实施相关的边界与约束、失败/边缘路径、Change Map、依赖与兼容性、执行顺序和可执行 Verification Plan。Plan 不重新无依据选择技术方向，也不一开始就机械拆 todo；简单任务可保持为 change、impact、execution、verification 的短计划，复杂度或风险需要时才展开 Contract、data、failure mode、migration、rollout 等细节。产物是可安全进入 Execute 的 **Executable Plan**；Plan 本身不实施或充当业务 Contract Authority。若产品提供原生 Plan 执行 Action，优先使用。属于 Feature Delivery 时，持久边界和结果必须回填对应 Workbench Artifact。
3. **Execute / X — Change only inside the approved boundary**：原生 Action 不可用、Plan 后重新收敛或恢复明确边界时，`X` 确认并执行当前唯一、明确、无未决且未失效的最新 Plan。否则回到 Plan；只实施已确认范围内的改动，发现边界假设不成立或范围必须扩大时停止。
4. **Verify / V — Prove the result with evidence**：先定义 Verification Target，再选择与目标、风险和当前环境相称的 Verification Depth，收集实际 Evidence 并给出不超过证据范围的 Verdict。产物是 **Verification Evidence + Verdict**。V 可独立审核现有代码；完整 E2E 不可用时，仍应尝试能证明目标行为的 service/component smoke。默认只验证，不扩大实现 Scope 或自动修复。

## E → P 交界

Explore 回答真实问题、当前状态、可行性、主要约束、推荐方向和主要 change seam，退出时应有足够证据说明该方向可行。Plan 接受这个 Viable Solution，继续回答它是否已经完整到可以安全执行。正确关系是 **E = viable but not necessarily complete；P = complete enough to execute**。

Plan 只补齐与当前任务相关的内容：

- **Boundary Completion**：Scope / Non-scope，以及输入输出、模块、数据、生命周期、权限、外部系统和旧数据/旧行为兼容边界；
- **Constraint Completion**：性能、并发、一致性、数据量、SDK/API、数据库、服务间 Contract、发布、安全、兼容和可观测性等已识别且影响实现的约束；
- **Failure / Edge Cases**：正常流程之外，与任务相关的空值、重复/幂等、超时、重试、部分失败、中断、外部依赖失败、数据不一致、并发冲突、历史数据、升级和回滚；
- **Change Map**：需修改、仅受影响和明确不改的模块，以及 API、DB、MQ/event、config、调用方、测试、迁移和部署影响；
- **Execution Design**：Files / Components、步骤与依赖、可独立验证点、必须原子完成的步骤、分阶段实施、migration、feature flag 和 rollout 顺序；
- **Verification Closure**：将 Explore 的 Verification Strategy 转成可执行计划，明确 unit/integration/API/performance/compatibility/failure-path 验证及 Verify 阶段需收集的 Evidence。

若 Plan 发现新事实使推荐方案的可行性、成本或风险重新变得不确定，应携带新证据回到 Explore，而不是在 Plan 中静默重选技术方向。**Plan refines a viable solution; if viability becomes uncertain, return to Explore.**

## Plan 退出条件

Plan 仅在以下适用条件均满足后完成并进入 Execute；按任务复杂度表达，不要求固定大文档或机械枚举无关项：

1. Explore 的推荐方向仍成立，不存在需要重新验证的关键可行性问题；
2. Goal、Scope 和 Non-scope 已经足够明确；
3. 影响实现正确性的关键边界和约束已经覆盖；
4. 主要异常和失败路径已经处理或形成显式 Stop Condition；
5. 依赖关系和整体影响范围已经明确；
6. 数据、API、Contract、MQ/event、config、迁移和部署变化已经明确；
7. 现有调用方、旧数据和旧行为的兼容性已处理或明确为需确认的影响；
8. Files / Components 和 Change Map 已经明确；
9. 执行顺序、任务拆分及必要的 rollout / rollback 边界已经明确；
10. Verification Strategy 已转成可执行 Verification Plan，能证明正常路径、关键失败路径和兼容性闭环；
11. 不存在阻塞 Execute 的关键 Unknown，且当前 Plan 唯一、明确、可排序、可验证并有 Stop Conditions。

## Verify：对目标取得证据并限定结论

Verify 回答 **What can we prove about this target with the available evidence?**，而不是机械确认是否运行了全部测试。它可以验证刚完成的 Execute，也可以在没有当前 Execute 时独立审核现有代码。开始时先识别本轮真正需要证明的 **Verification Target**，例如一个 Service 的状态处理、一次变更对离线判定的影响，或 MQTT message → Service → Redis → WS 中限定在单服务内的链路。用户可明确收窄到代码审核、Service 内部行为或其他局部对象；V 不默认把 Target 扩大为整个 Feature 或完整 E2E。

### Verification Modes / Depth

按 Verification Target、风险、当前环境、可访问依赖和用户明确要求，选择一个或多个适用 Depth：

| Mode | 可证明的内容 | 常用手段 |
| --- | --- | --- |
| **Static Review** | 代码逻辑、调用链、数据流、状态流转、边界判断、异常处理、资源释放、并发风险、Contract 使用，以及与 Requirement / Plan 的一致性 | code/diff review、call-chain、data-flow、contract inspection |
| **Automated Verification** | 可由现有或新增授权范围内自动化检查直接覆盖的行为和结构 | unit/integration test、build、lint、typecheck、existing test |
| **Targeted / Scoped Smoke Verification** | 不依赖完整真实系统的最小可执行 service/component 链路，例如输入 → 业务决策 → 状态流转 → repository/publisher call | existing test harness、mock、stub、fake dependency、fixture、local API、protocol simulation、existing dev environment、non-production diagnostic execution |
| **Integration / Runtime / E2E Verification** | 跨组件、外部依赖或真实运行链路 | API、SQL、MQ/MQTT、WS、Redis、DB、external service、device、runtime observation、full-chain smoke |

`Static → Automated → Scoped Smoke → Integration → E2E` 不是强制 pipeline。只需证明 Service-level behavior 时，可以完成 Static Review 与 Service Smoke，同时将 Integration 标为 `not executed`、真实设备 E2E 标为 `not verifiable`。缺少完整链路不等于无法验证；应先寻找已有测试、fixture、mock、stub 或 Service 调用入口，尝试完成 Target 所需的最小可执行验证。不得为了追求更深层级而越过用户明确 Non-scope、访问生产环境或制造外部业务副作用。

### Verification Boundary Propagation

**Verification Boundary follows the Verification Target, unless the user explicitly narrows the scope.** 开始取证前，从 Target 推导其成立所必需的行为路径；只要某个 downstream service、external API、Feign/RPC、MQ/MQTT、adapter、callback、asynchronous consumer、Redis、DB、external SDK 或 event handler 是证明 Target 的必要环节，Verification Boundary 就应沿调用链传播。跨越 Service、Module 或 Repository 本身不是停止条件。在设备状态更新依赖 `Service A → Feign Contract → Service B → Repository → DB` 时，只证明 Service A 发起 Feign 调用不足以判定整条 Target 通过。

若必要依赖可实际运行，优先执行相称的 integration/runtime verification 或 scoped/full-chain smoke 并取得真实 Evidence。无法完整运行时，继续建立静态 Evidence Chain，例如从 caller code、Contract / DTO 到 downstream Controller / Consumer、Service、Repository / SQL、config、existing tests 及可用 logs/runtime evidence，尽可能核对链路两端行为与 Contract 语义。当前条件无法继续取证时，将相应环节标为 `not executed` 或 `not verifiable`，说明缺少的 Evidence；不得因链路跨服务而默认其通过。

用户显式 Verification Scope / Non-scope 优先于默认传播：只要求验证当前 Service 内部行为时，在该边界停止；外部环节标为 `not executed` 并注明 `out of scope`，或在缺少必要证据时标为 `not verifiable`。Repository Scope 同样不会因 Target 跨仓而自动扩大：当前 Scope 允许读取的 Repository 可继续取证；未在 Scope 内的 Repository 不读取，并以 `not verifiable` / `insufficient scope` 说明证据缺口。Boundary Propagation 只授权既有范围内的 read / inspect / verify，不授予任何生产代码写权限。

Target 决定应追到哪里，用户显式 Scope / Non-scope 与 Repository Scope 决定最多允许追到哪里，实际 Evidence 决定最终能证明到哪里。Verdict 只能覆盖三者交集。

### Evidence、状态与 Verdict

对每个适用验证项明确报告 `passed`、`failed`、`not executed` 或 `not verifiable`，并附实际 Evidence；Evidence 可以是代码位置与调用链、diff finding、测试或构建输出、请求与响应、状态变化、依赖调用记录或运行观测。`not executed` 表示本轮没有运行；`not verifiable` 表示在当前证据和可用环境下无法证明，二者都不得写成通过。

**Verification verdict must not exceed evidence scope.** Static Review `passed` 只证明已检查的静态逻辑没有发现阻断问题，不代表 Runtime 或 E2E 已验证；Service Smoke `passed` 只证明已执行的单服务/组件行为，不代表跨服务、前端或真实设备链路通过。最终 Verdict 必须同时说明已证明的范围与仍未验证的范围，不能只给一个脱离 Target 和 Evidence 的 `PASS`。

### 独立 Code Review

V 可以在没有当前 Execute 时审核现有代码。此时读取 Verification Target 所需的代码、调用方与 Contract，对照可用的 Requirement / Plan，检查正常路径和关键异常/边缘路径，列出 finding、Evidence 与 Verdict。Static Review 是有效的验证模式，但只能提供静态证据；发现问题时报告 `failed` 或明确的 review finding，默认不修改生产代码。

### Targeted / Scoped Smoke

当完整设备或跨服务链路复杂、不可访问或明确不在本轮范围时，以最小必要输入和环境执行 service/component smoke。例如直接调用 Service method，以 mock、stub 或 fake dependency 观察状态转换、持久化决策及 publisher 调用；也可以使用已有 test harness、local API、协议模拟或非生产开发环境。结果应分别说明内部行为是否通过，以及 MQTT、真实设备、前端或其他外部链路为何 `not executed` 或 `not verifiable`。局部通过不得升级为完整 Feature 或 E2E 通过。

### 失败与 Plan 边界

Verify 执行 Plan 预先设计的 Verification Plan，并依据当前证据作出判断；Plan 回答“完成后准备如何证明”，V 回答“现在实际能证明什么”。V 不重新设计整个实现方案。若验证失败，先报告失败位置、Evidence、影响与未覆盖范围，默认携带新证据回到 Explore；若失败只是因为 Verification Plan 或执行边界缺失，可以建议回到 Plan。Verify 本身不授权生产代码修复；只有用户明确要求修复后，才按适用的 E / P / X 继续，不做无限猜测式 patch。

## Product Truth Sync

`Sync` / `S` 是 Verify 后可选的独立 Action，不是本循环的第五个 Stage。它不要求 DF 或 Active Delivery：以当前 Thread 已有的实现、契约和 Verification Evidence 判断是否存在同时 **Verified、Current、Durable、Independently Valid** 的 Product Truth Delta。`P0 S` 仅授权最小更新 P0 `products/` 的现有 canonical 页面及必要导航链接；它不读取未在 Scope 内的业务仓库，不写 `work/`、`task.yaml` 或 `knowledge_update_assessment`，也不 Closing、Archive、commit、push、release 或 deploy。没有合格 Delta 时分别报告 `not-needed`、`not-ready` 或 `insufficient-evidence`，不写文档；合格时报告 `synced` 及最小 Delta、页面和证据。`S1` 是 Repository Scope，不是 Sync。

## 分档

| Level | 适用情形 | 路径 |
| --- | --- | --- |
| 1 — Fast Path | 修复位置与风险都明确的小改动 | Execute → Verify |
| 2 — Standard Path | 一般 Service、缓存、SQL、WS、权限条件、小重构或 Bug | Explore → Plan → Execute → Verify |
| 3 — Controlled Path | 跨服务、公开 Contract、DB Schema/迁移、并发、认证授权、设备控制、多仓库或陌生遗留代码 | Deep Explore → Plan Review → Execute → Code Review → Verify |

## Stop Conditions

停止执行并重新汇报证据、回到 Explore / Plan，若发现需要：

- 修改 DB Schema、公开 API Contract、权限或数据隔离模型；
- 修改第二个未授权 Repository；
- 推翻当前 Explore 假设或原计划无法满足成功标准；
- 明显扩大已确认 Scope。

## 与 Feature Delivery 的边界

Engineering Task Loop 管一次具体工程修改。Feature Delivery 管跨天或跨周的 Delivery ID、CAP、Phase/Gate、Task Package 与 Artifact Authority。属于 Delivery 的非平凡 DEV 任务，将重要 Plan、实施结果与 Verify 证据回填 `03-execution-backlog.md`；Bug/Integration 的根因、修复、回归与 Verify 证据回填 `04-integration-log.md`；暂停或 Phase 变化刷新 `resume.md`。属于 Delivery 的独立事实仍可通过 `S` 同步，但不改变任何 Delivery 状态或 metadata。单个 Task Loop 的 Verify 不触发 Delivery Closing；G4 / acceptance 只允许 Agent 建议 Ready to Close。用户显式授权 `tu-close-delivery` 后，才按 [Delivery Closing](delivery-closing.md) 顺序进行最终 Product Truth reconciliation、Sensitive Data Review、Archive/verify finalized snapshot、创建 Closed Index 并 retire active Package；这不增加或替代 E/P/X/V。
