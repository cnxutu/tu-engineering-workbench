# Engineering Kernel

Core 是 Engineering Operating Model：只描述通用工程方法、生命周期与 Context Routing，不存放任何产品或仓库事实。使用时按任务选择最小必要集合；整体区域边界见 [Living Engineering Model](../docs/workbench-model.md)。

## 概念边界

- **Rule**：必须遵守的稳定工程约束。
- **Playbook**：仓库内可复用的工程方法；说明如何分析和交付，但不是平台能力单元。
- **Skill**：Codex 平台可发现、可触发的能力单元，放在 `plugins/*/skills/`。
- **Workflow**：针对一次真实交付，将 Rule、Playbook、Skill 和产品上下文组合起来的过程；不为它另建通用框架。

## 角色

- [Java Engineer](agents/java-engineer.md)：Java / Spring Boot 实现。
- [Backend Architect](agents/backend-architect.md)：后端边界与演进设计。
- [System Designer](agents/system-designer.md)：跨服务系统设计与链路梳理。
- [Database Expert](agents/database-expert.md)：数据模型与迁移。
- [Code Reviewer](agents/reviewer.md)：变更质量评审。

角色选择：服务内部的后端职责、模块边界和实现演进使用 `Backend Architect`；涉及多个仓库、服务拓扑、消息协议或端到端链路时使用 `System Designer`。

角色只提供任务视角，不按 Redis、MQTT、Spring 等技术标签无限扩张 Persona；技术约束应来自当前代码、规则和产品上下文。

## 规则

- [公共 Codex 开发基准](rules/development.md)：所有服务中代码、配置、脚本与测试任务的默认基准，涵盖上下文装载、分析与确认、最小实现、调试、验证、交接与安全。
- [架构](rules/architecture.md)、[Java](rules/java.md)、[Spring Cloud](rules/spring-cloud.md)、[数据库](rules/database.md)、[Git](rules/git.md)：按技术和任务条件加载。

## Playbook

- [Delivery Closing](playbooks/delivery-closing.md)：用户显式授权后执行 Integrate、Vault Archive、Closed Index 与 Active Package retirement 的有序收尾事务。
- [Engineering Task Loop](playbooks/engineering-task-loop.md)：通用的 Explore → Plan → Execute → Verify 细粒度任务执行循环。
- [功能开发](playbooks/feature-development.md)、[问题排查](playbooks/bug-analysis.md)、[架构评审](playbooks/architecture-review.md)、[重构分析](playbooks/refactor-analysis.md)。

Playbook 是仓库级的通用工程方法，不等同于 Codex 平台安装且可触发的 `SKILL.md`。平台 Skill 的适用与优先级以 [P0 运行时约束](../AGENTS.md) 为准；Playbook 仅在不冲突时补充其执行细节。

## 日常任务

用户默认使用自然语言描述任务。对非平凡工程任务，可选用 [Engineering Task Loop](playbooks/engineering-task-loop.md) 的 Stage Shortcuts：Explore → Plan → Execute → Verify。它们表达本轮阶段意图，不取代用户确认、局部 `AGENTS.md`、Contract 或证据。

任务涉及多个仓库、公开契约或消息协议时，应先加载最小必要的产品架构与链路资料，使用 `System Designer` 进行设计或评审；Explore 以证据形成 Viable Solution，Plan 再补齐边界、影响、失败路径、执行和验证闭环，形成 Executable Plan。完整定义以 [Engineering Task Loop](playbooks/engineering-task-loop.md) 为准；面向人的日常示例见 [Engineering Task Loop Best Practice](../docs/workflows/engineering-task-loop/README.md)，但 Runtime 不强制加载该页面。
