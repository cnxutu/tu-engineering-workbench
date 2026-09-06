# 产品 PRD

## 范围

本目录保留无人机巡检平台按产品版本归档的需求文档。它们属于 Transition / Existing Historical Material，用于追溯背景，不自动拥有 Current Product Truth Authority；Current Requirement 必须由明确标注的 Current Product Spec/PRD、批准 Product Decision、批准 Contract 或明确 acceptance criteria 确认。Implementation Reality 由代码、测试、运行配置与可复现运行证据确认；两者不一致时记录 Requirement / Implementation Gap，而不以代码反向否定需求。服务实现、数据表和跨服务边界以对应的设计决策与代码证据为准。

## 版本导航

- [v2.1.0](v2.1.0/index.md)：历史版本参考——项目管理模块，包含项目集和项目的创建、编辑、列表、详情及关系选择。

## 维护约定

- 不将未来每个版本 PRD 自动视为 Current Truth；需要在 `products/` 保留当前有效需求时，明确其 Current Authority 与历史参考的边界。实际历史迁移留待 tu-vault archive 模型建立后处理。
- 原型、评审结论和实现状态必须区分标注；无法读取的原型区域标为 `pending_verification`。
- 已确认的长期架构边界链接到 `decisions/`，不在 PRD 中复制为第二份权威事实。
