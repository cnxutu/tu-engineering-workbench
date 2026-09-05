# Feature Delivery × Skill Integration Best Practices

`tu-deliver-feature` 负责 durable Feature lifecycle、Delivery ID、Phase/Gate、Artifact 和恢复路由。Provider 决定如何完成某一步；Task Package、批准 Contract 和证据决定 Delivery 当前含义。

本页回答 Feature Delivery 各阶段优先使用什么 Provider；具体一个 DEV / Bug 如何结合 Goal/Explore、Plan Mode、implement、TDD、review 与验证，统一参考 [Engineering Task Loop](../engineering-task-loop/README.md)。该 Loop 不改变本页的 Lifecycle Authority 边界。

本页不是 Skill Catalog，也不声明某个外部 Skill 在所有 Session 都已安装。仅在当前环境暴露且调用策略允许时使用下列 capability；否则借鉴其方法或继续使用 Phase Contract。

| Context | Preferred capability | Relationship to Feature Delivery |
| --- | --- | --- |
| 整个 Feature 生命周期 | `tu-deliver-feature` | 生命周期入口与状态 Authority。 |
| 原型/PRD → Backend Impact | `tu-analyzing-feature-impact` | Phase 1 OWN provider，产出 Impact Review。 |
| 外部 SDK、协议或技术资料核实 | `research`（可用时） | 补充证据，不替代 CAP/Impact Artifact。 |
| 领域概念、状态或实体关系复杂 | `domain-modeling`（可用时） | 帮助澄清 Phase 1/2，不接管 Contract。 |
| Repository seam、责任或改造入口 | `codebase-design`（可用时） | 提供代码事实与切分输入。 |
| Contract / Spec 收敛 | Adapt `to-spec` | 采用方法；批准的 Workbench Contract 仍是 Authority。 |
| Backlog / Vertical Slice | Adapt `to-tickets` | 采用 tracer bullet、vertical slice、blocker edge 方法。 |
| 已有 ready DEV Task 的实现 | explicit `implement`（适用且可用时） | 用户显式调用；不从总入口绕过调用策略。 |
| 行为驱动实现 | `tdd`（可用时） | 用于一个已授权 DEV Task。 |
| 实现后代码/Spec Review | `code-review`（可用时） | 审查实现，不重写 Lifecycle 状态。 |
| 可复现 Implementation Bug | `diagnosing-bugs`（可用时） | Phase 4 的执行 provider；总入口保留 Bug 分类。 |
| 普通临时 Session 交接 | `handoff`（可用时） | 临时 transfer；不替代 Delivery 包。 |
| Durable Feature Delivery Resume | `resume.md` | 持久 Resume Cache；配合 Task Package 恢复。 |

## When not to use Feature Delivery

- 已有堆栈、范围和复现路径的明确小 Bug：使用 `diagnosing-bugs` 或现有 Spring incident Skill。
- 单纯 Code Review：使用 `code-review`。
- 独立技术研究（SDK、Redis、协议）：使用 `research`。
- Scope、Contract、Verification 都完整的单个 DEV Task：直接使用适用的 `implement`。
- 领域建模或独立 Architecture Review：使用相应 capability、Playbook 或 Role。

`tu-deliver-feature` 是 durable feature lifecycle，不是每个工程问题的通用入口。

## Easy-to-confuse capabilities

产品原型到后端影响分析使用 `tu-analyzing-feature-impact`。若外部 `prototype` Skill 表示 throwaway implementation 或实验，应只用于快速验证想法，不能与既有产品原型分析混用。

`handoff` 是 ad-hoc Session transfer；`resume.md` 是 Feature Delivery 的持久 Resume Cache。Feature Delivery 中不得用 handoff 替代 `task.yaml`、阶段 Artifact 或 `resume.md`。

## Authority boundary

Provider 可以替换；Delivery ID、CAP、Gate、Artifact 和 Task State 不能随 provider 改变。Runtime Skill Contract 在 [Plugin Skill](../../../plugins/ai-guidance-workflows/skills/tu-deliver-feature/SKILL.md) 及其 references 中；本页只解释何时结合能力。
