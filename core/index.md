# Core 公共能力

Core 只描述通用工程方法，不存放任何产品或仓库事实。使用时按任务选择最小必要集合。

## 角色

- [Java Engineer](agents/java-engineer.md)：Java / Spring Boot 实现。
- [Backend Architect](agents/backend-architect.md)：后端边界与演进设计。
- [System Designer](agents/system-designer.md)：跨服务系统设计与链路梳理。
- [Database Expert](agents/database-expert.md)：数据模型与迁移。
- [Code Reviewer](agents/reviewer.md)：变更质量评审。

角色选择：服务内部的后端职责、模块边界和实现演进使用 `Backend Architect`；涉及多个仓库、服务拓扑、消息协议或端到端链路时使用 `System Designer`。

## 规则

- [架构](rules/architecture.md)、[Java](rules/java.md)、[Spring Cloud](rules/spring-cloud.md)、[数据库](rules/database.md)、[Git](rules/git.md)。

## 工作流

- [功能开发](skills/feature-development.md)、[问题排查](skills/bug-analysis.md)、[架构评审](skills/architecture-review.md)、[重构分析](skills/refactor-analysis.md)。

## 日常任务入口

- [Prompt Compact Syntax](prompt-compact-syntax.md)：用户与 Codex 的默认简写协议。日常任务优先使用它，不要求填写长 Markdown 模板。

任务涉及多个仓库、公开契约或消息协议时，应先加载产品架构与链路文档，使用 `System Designer` 进行设计或评审；任务类型使用 `X`，并在 `i` 中列出受影响的仓库。

## 历史模板

`templates/` 保留为历史参考或需要长篇任务文档时的输出框架：功能、缺陷修复、重构、架构设计、代码评审与跨服务变更。除非用户明确指定，Codex 不主动要求或加载它们。
