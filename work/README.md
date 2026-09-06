# Delivery Change State

`work/` 回答“系统正在发生什么变化”。它保存 Delivery 的需求/上下文、探索、决策、计划、契约、执行、验证、问题、开放项与结果；它不是临时目录，也不是 Product Truth 的默认入口。

新 Delivery 使用 `work/active/<domain>/<product>/DF-YYYYMMDD-NN-<slug>/` 保存完整 Task Package。结束后在 `work/closed/<domain>/<product>/DF-YYYYMMDD-NN.md` 留下 Thin Context Index，指向已更新的 Product Truth、关键决定、相关 Delivery 与可选 archive reference。目录只在首次有实际内容时创建。

完整历史在外部 archive 尚未配置时保留在现有 `work/<domain>/<product>/tasks/archive/` 作为 local cold context；其中 pre-V1 平铺记录继续有效，不迁移或伪造 DF ID。正常 Session 优先读 active Package 与相关 `products/`，仅在回溯原因时读 closed index 或 archive。

Feature Delivery V1 的生命周期与收尾语义见 [Feature Delivery Workflow](../docs/workflows/feature-delivery/README.md)，整体模型见 [Living Engineering Model](../docs/workbench-model.md)，metadata 继续遵循 [`task-metadata` 契约](../core/contracts/task-metadata.schema.yaml)。
