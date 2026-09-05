# Engineering Workbench

`tu-engineering-workbench` 是面向 AI Coding / Agent Engineering 的工程上下文、工作流编排与工程知识中枢。它帮助 AI 在正确的工程上下文中，以正确的方法持续推进真实软件交付。

它不是 Prompt 集合、Skill 大全、项目 Wiki、业务代码副本、任务管理系统，也不承担开发环境、CLI、VPS 或工程工具职责；这些属于 `tu-devkit`。

## 目录模型

- `core/`：Engineering Kernel——规则、契约、仓库注册表、Playbook 与最小运行时路由。
- `products/`：What we know——经证据验证、可长期复用的产品架构、边界、链路、领域语义与 ADR。
- `work/`：What we are doing——真实需求的 Delivery State；过程证据、执行清单与联调记录。
- `plugins/`：How AI works——可触发的 Codex Skill 及其组合能力。
- `docs/`：How humans use and maintain the Workbench。
- `bootstrap/`：仓库如何接入 Workbench。

产品知识不是工作过程的副本：任务先留在 `work/`，只有经代码、契约、测试或批准记录验证且值得复用的结论，才进入 `products/` 的唯一权威页。

## 从这里开始

- [运行时约束](AGENTS.md)：供 Codex 按范围、简写协议和条件读取执行任务的最小入口。
- [文档导航](docs/README.md)：按使用、治理、Codex 与工作流目标查找资料。
- [工程师使用与维护指南](docs/guides/usage-guide.md)：供工程师理解范围声明、目录与日常使用方式。
- [Feature Delivery Workflow V1](docs/workflows/feature-delivery/README.md)：一个 Delivery ID 串起影响分析、契约、实施、联调与 Bug 回归的正式说明。
- [Agent Skill 项目与安装清单](docs/codex/agent-skill-landscape.md)：S1 开源参考模块、GitHub 模板来源与当前环境 Skill 快照。
- [项目导航与维护地图](docs/guides/project-guide.md)：供工程师理解 AI 运行时加载链路、工程师使用与维护路径、项目骨架与扩展入口。
- [Core 入口](core/index.md)：角色、规则、Playbook、契约与参考模板。
- [仓库注册表](core/registry/repositories.yaml)：项目标记、工程身份与产品绑定的唯一来源；仓库在产品中的职责由 `products/**/repositories/*.yaml` 维护。
- [交付状态](work/README.md)：任务过程和归档的边界。
- [无人机巡检产品入口](products/company/device-inspection-platform/index.md)：P1–P4、P3-1 的业务、架构和链路上下文。
- [接入指南](docs/guides/integration-guide.md)：如何让一个代码仓库绑定产品上下文。

## 目录职责

- `core/`：跨产品复用的 Kernel、角色、规则、Playbook、契约与模板。
- `products/`：稳定的产品、仓库、架构、流程、领域与决策知识。
- `work/`：当前与归档的交付状态，不作为产品知识默认入口。
- `plugins/`：少量、边界清晰、可触发的 Codex Skill。
- `bootstrap/`：目标仓库的 `AGENTS.md` 和仓库清单模板。
- `docs/`：使用、接入、编写和治理说明。

产品事实应有代码、接口或运行证据；未知内容必须标记为待验证。语义优先级始终是：仓库局部约束与代码 > 产品上下文 > Core 通用规则。

产品入口、链路、设计和仓库入口地图的固定写法见 [编写指南](docs/governance/authoring-guide.md)。

`README.md` 与 `docs/` 面向维护者，不是 Codex 的默认读取范围；实际运行时加载规则以 [AGENTS.md](AGENTS.md) 为准。
