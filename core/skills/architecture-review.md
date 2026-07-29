# Skill：架构评审

## 用途

用于评估架构设计、跨模块改动或重要技术决策是否满足业务目标与工程约束。

## 依赖

- Agent：服务内部设计使用 [`Backend Architect`](../agents/backend-architect.md)；跨服务、协议或拓扑设计使用 [`System Designer`](../agents/system-designer.md)
- Rules：[`架构`](../rules/architecture.md)、[`数据库`](../rules/database.md)（涉及持久化时）
- Prompt：默认使用 [`Prompt Compact Syntax`](../prompt-compact-syntax.md) 的 `A`；跨服务改动使用 `X`。仅在用户明确要求长篇任务文档时，服务内部设计参考 [`架构设计任务`](../templates/architecture-design.md)，跨服务变更参考 [`跨服务变更任务`](../templates/cross-service-change.md)
- Context：目标项目的业务概览、当前架构、接口与数据模型事实

## 流程

1. 确认评审目标、范围、非目标、成功标准和不可变约束。
2. 提取现状：模块边界、调用链、数据所有权、外部依赖和已知问题。
3. 识别风险：复杂度、耦合、性能、可靠性、安全、兼容性、迁移与运维风险。
4. 给出最多三个可行方案，说明取舍并推荐一个方案。
5. 输出落地步骤、风险缓解措施、验证指标和待确认事项。

## 输出格式

按“背景与范围、现状、问题与风险、方案对比、推荐方案、实施与验证、待确认项”输出。证据不足时明确标注假设，不将假设当作事实。
