# AI 工程上下文平台

`ai-guidance` 是 P0 中面向 P1–P4 的统一系统知识库与 AI 工作方法库，不是单纯的 Prompt 集合或业务代码副本。

它只维护高价值、可长期复用的上下文：关键入口、跨服务链路、服务/数据边界与重要设计决策。实现细节、全量配置和临时排查过程应留在代码、契约、配置或任务记录中。

## 从这里开始

- [使用指南](docs/usage-guide.md)：AI 读取链路、P0–P4 全量/局部工作区、Skill/Template 使用和变量替换规则。
- [Core 入口](core/index.md)：角色、规则、Skill 与 Template。
- [无人机巡检产品入口](products/company/device-inspection-platform/index.md)：P1–P4 的业务、架构和链路上下文。
- [接入指南](docs/integration-guide.md)：如何让一个代码仓库绑定产品上下文。

## 目录职责

- `core/`：跨产品复用的角色、规则、工作流和模板。
- `products/`：产品、仓库、架构、流程、缓存与历史任务知识。
- `bootstrap/`：`AGENTS.md` 和仓库清单模板。
- `docs/`：使用、接入、编写和治理说明。

产品事实应有代码、接口或运行证据；未知内容必须标记为待验证。语义优先级始终是：仓库局部约束与代码 > 产品上下文 > Core 通用规则。

产品入口、链路、设计和仓库入口地图的固定写法见 [编写指南](docs/authoring-guide.md)。
