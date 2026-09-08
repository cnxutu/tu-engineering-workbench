# Playbook：Engineering Task Loop

## 用途

用于一个具体的 DEV、Bug、Refactor 或技术改造任务：先核实现状、验证关键可行性并收敛推荐方向，再确认实际修改边界，在授权范围内实施，并以可复现证据验证结果。它是通用工程方法，不是 Codex Skill、状态机或长期交付记录。

## 核心循环

Stage Shortcut 位于消息的任务头部区域，可在可选 Repository Scope 之后、主要自然语言任务正文之前，以独立 token / 独立标签出现；支持大小写不敏感的 `E` / `Explore`、`P` / `Plan`、`X` / `Execute`、`V` / `Verify`。`P1`、`P2`、`P3-1` 等仍是项目标记，正文中的普通单字母不触发 Stage。

1. **Explore / E — Prove the solution is viable**：先核实现状、Goal、事实/假设/未知、change / integration seam 与可复用实现；再以证据验证方案成立所依赖的关键可行性和约束（现有扩展点、架构/Contract 兼容性、外部能力、性能或前置条件）；最后收敛推荐方案、影响范围、Non-scope、风险/约束、Verification Strategy 与未决前置条件，必要时给出替代方案及取舍。Explore 的产物是附 Evidence / Reasoning 的 **Viable Solution**：足以证明推荐方向可行并进入 Plan，但不要求边界、异常、兼容和实施细节已经完整，也不展开为逐步实施计划；关键未知项仍阻塞 Plan 时，继续验证而非结束 Explore。默认不修改任何 tracked file；可读取、搜索调用链、运行现有测试和非持久诊断/验证。用户可只放宽明确允许的范围。
2. **Plan / P — Make the solution complete and executable**：Codex Plan Mode 基于 Explore 的 Viable Solution 继续 Refine、Bound、Close the Loop 和 Prepare Execution，补齐与正确实施相关的边界与约束、失败/边缘路径、Change Map、依赖与兼容性、执行顺序和可执行 Verification Plan。Plan 不重新无依据选择技术方向，也不一开始就机械拆 todo；简单任务可保持为 change、impact、execution、verification 的短计划，复杂度或风险需要时才展开 Contract、data、failure mode、migration、rollout 等细节。产物是可安全进入 Execute 的 **Executable Plan**；Plan 本身不实施或充当业务 Contract Authority。若产品提供原生 Plan 执行 Action，优先使用。属于 Feature Delivery 时，持久边界和结果必须回填对应 Workbench Artifact。
3. **Execute / X — Change only inside the approved boundary**：原生 Action 不可用、Plan 后重新收敛或恢复明确边界时，`X` 确认并执行当前唯一、明确、无未决且未失效的最新 Plan。否则回到 Plan；只实施已确认范围内的改动，发现边界假设不成立或范围必须扩大时停止。
4. **Verify / V — Prove the result with evidence**：默认只验证，不扩大实现 Scope 或自动修复；按任务选择测试、构建、lint、typecheck、契约/API、协议模拟、运行观测或 review。验证失败时先以新证据重新 Explore，不做无限猜测式 patch。

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
