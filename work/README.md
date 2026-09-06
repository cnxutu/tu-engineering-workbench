# Delivery Change State

`work/` 回答“系统正在发生什么变化”。它保存 Delivery 的需求/上下文、探索、决策、计划、契约、执行、验证、问题、开放项与结果；它不是临时目录，也不是 Product Truth 的默认入口。

新 Delivery 使用 `work/active/<domain>/<product>/DF-YYYYMMDD-NN-<slug>/` 保存完整 Task Package。达到 Closing readiness 后仍保持 active；只有用户显式授权、完整 Package 已 Archive 至配置的 `tu-vault` 并验证后，才在 `work/closed/<domain>/<product>/DF-YYYYMMDD-NN.md` 留下 Thin Context Index，指向已更新的 Product Truth、关键决定、相关 Delivery 与逻辑 archive reference，并 retire active Package。目录只在首次有实际内容时创建。

`work/<domain>/<product>/tasks/archive/` 仅作为 local legacy cold compatibility；其中 pre-V1 平铺记录继续有效，不迁移或伪造 DF ID。新 Closing 不因 external archive 未配置而降级为本地归档。正常 Session 优先读 active Package 与相关 `products/`，仅在回溯原因时读 closed index 或 archive。

Feature Delivery V1 的生命周期与收尾语义见 [Feature Delivery Workflow](../docs/workflows/feature-delivery/README.md)，整体模型见 [Living Engineering Model](../docs/workbench-model.md)，metadata 继续遵循 [`task-metadata` 契约](../core/contracts/task-metadata.schema.yaml)。
