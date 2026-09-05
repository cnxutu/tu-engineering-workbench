# Documentation

此目录是面向工程师的按需资料入口，不属于 Codex 默认运行时上下文。

| 目标 | 阅读入口 |
| --- | --- |
| 第一次使用 Workbench | [使用指南](guides/usage-guide.md) |
| 接入新的 Repository | [接入指南](guides/integration-guide.md) |
| 理解项目结构与维护路径 | [项目导航](guides/project-guide.md) |
| 维护知识与文档 | [治理与编写规范](governance/governance.md) |
| 理解 Codex、AGENTS 与 Skill 环境 | [Codex 文档](codex/) |
| 使用成熟的软件交付工作流 | [Workflow Best Practices](workflows/) |

Authority 边界：`docs/` 是人类最佳实践；`plugins/**/SKILL.md` 与 references 是 Runtime Skill Contract；`work/` 是当前 Delivery State；`products/` 是已验证 Product Knowledge；`core/` 是稳定规则与契约。发生冲突时遵循现有 instruction hierarchy。
