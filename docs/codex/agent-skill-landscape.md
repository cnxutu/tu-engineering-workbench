# Agent Skill Landscape

本页只维护长期有效的 Skill 边界与使用基线；当前客户端、缓存路径、安装数量和逐日快照不属于仓库事实。

## 边界

- Workbench Workflow 定义交付语义、持久状态与 Authority；Skill 是可替换的能力提供者。
- `tu-deliver-feature` 是 Feature Delivery 的生命周期入口与编排器；Task Package、批准的 Contract、阶段 Artifact 和可复现证据才是持久 Delivery Authority。
- 当前正式 Plugin Skill 为 `tu-deliver-feature`、`tu-analyzing-feature-impact`、`tu-diagnosing-spring-backend-incidents` 与 `tu-loading-device-inspection-cross-service-context`。
- 是否可调用某个外部 Skill 由当前 Codex Session 决定；不能因为文档列出方法就假定它已安装或可隐式调用。

## 借鉴外部方法

外部 Skill、公开仓库和内部经验可以提供研究、契约收敛、任务拆分、诊断、TDD 或评审方法。借鉴时保留原项目边界、用户授权和本仓库 Authority 模型；不把外部 Skill、聊天记录或 Tracker 升格为 Delivery Authority。

## Workbench 维护基线

- Runtime 说明、Plugin metadata 与 Skill 验证脚本必须保持同一组正式 Skill。
- 只在真实的产品语义或运行入口变化时更新 Workflow/Skill 文档；被替代设计默认交由 Git history 保存。
- Product Knowledge 记录已验证、可复用事实；`work/` 记录特定交付的过程证据与结果。
