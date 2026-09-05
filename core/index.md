# Engineering Kernel

Core 只描述通用工程方法，不存放任何产品或仓库事实。使用时按任务选择最小必要集合。

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

- [Engineering Task Loop](playbooks/engineering-task-loop.md)：通用的 Explore → Plan → Execute → Verify 细粒度任务执行循环。
- [功能开发](playbooks/feature-development.md)、[问题排查](playbooks/bug-analysis.md)、[架构评审](playbooks/architecture-review.md)、[重构分析](playbooks/refactor-analysis.md)。

Playbook 是仓库级的通用工程方法，不等同于 Codex 平台安装且可触发的 `SKILL.md`。平台 Skill 的适用与优先级以 [P0 运行时约束](../AGENTS.md) 为准；Playbook 仅在不冲突时补充其执行细节。

## 日常任务入口

- [Prompt Compact Syntax](prompt-compact-syntax.md)：熟练用户的快捷协议；自然语言任务同样有效，不要求填写长 Markdown 模板。

任务涉及多个仓库、公开契约或消息协议时，应先加载产品架构与链路文档，使用 `System Designer` 进行设计或评审；任务类型使用 `X`，并在 `i` 中列出受影响的仓库。只需先判断可行性时使用 `D`；已确认方向、只需锁定改动边界与步骤时使用 `P`。

## 历史模板

[`templates/README.md`](templates/README.md) 说明每类模板的最小必填、建议项、可选项与使用示例。`templates/` 提供功能、缺陷修复、重构、架构设计、代码评审、跨服务变更、可行性探索与变更计划的参考框架。除非用户明确指定，Codex 不主动要求或加载它们。
