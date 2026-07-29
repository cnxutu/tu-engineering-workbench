# Skill：重构分析

## 用途

用于在不改变已确认外部行为的前提下，识别结构性技术债并制定可验证的渐进式重构方案。

## 依赖

- Agent：[`Java Engineer`](../agents/java-engineer.md)；涉及边界调整时使用 [`Backend Architect`](../agents/backend-architect.md)
- Rules：[`Java`](../rules/java.md)、[`架构`](../rules/architecture.md)、[`数据库`](../rules/database.md)（涉及持久化时）
- Template：[`重构任务`](../templates/refactor.md)
- Context：目标仓库的调用链、测试基线、公开契约和性能指标

## 流程

1. 用代码、缺陷、测试或度量证实重构动机，明确必须保持的行为。
2. 划定影响模块、接口、数据和发布边界，识别不可安全拆分的耦合点。
3. 给出小步方案、每步验证与可回滚边界；不把顺手优化混入目标。
4. 实施后执行行为回归与必要的性能、兼容性验证。

## 输出格式

按“动机与证据、目标与非目标、影响范围、分步方案、验证、风险与回滚”输出。
