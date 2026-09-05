# Delivery State

`work/` 保存正在推进或已归档的真实交付状态：范围、证据、接口审查、执行清单、联调记录和短小的会话恢复缓存。Feature Delivery V1 的生命周期、任务包和归档规则见 [Feature Delivery Workflow](../docs/workflows/feature-delivery/README.md)。

它不是产品知识的默认读取入口。任务过程先保留在这里；只有经代码、契约、测试或批准记录验证且可长期复用的结论，才提炼到 `products/` 的唯一权威页或 ADR。每个产品在 `work/<domain>/<product>/tasks/{active,archive}/` 管理自己的任务包，并遵循 [`task-metadata` 契约](../core/contracts/task-metadata.schema.yaml)。
