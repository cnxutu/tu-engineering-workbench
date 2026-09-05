# Workflow Best Practices

本目录保存已形成稳定使用方式的 Workbench 工程工作流最佳实践，供工程师按需阅读；它不替代 Runtime Skill Contract。

当前工作流：

- [Feature Delivery](feature-delivery/README.md)：从需求/原型到长期联调、Bug 与归档的完整交付生命周期。
- [Engineering Task Loop](engineering-task-loop/README.md)：对一个具体 DEV / Bug / Refactor / 技术任务进行 Explore → Plan → Execute → Verify 的细粒度执行最佳实践。

两者并列：Feature Delivery 是 durable delivery lifecycle；Engineering Task Loop 是 one engineering task execution loop，不替代 Delivery 的 ID、CAP、Gate 或 Artifact。

后续成熟工作流使用 `workflows/<workflow-name>/`，按以下边界维护：

- Current Best Practice：`<workflow>/README.md`
- Skill integration / provider experience：`<workflow>/skill-integration.md`
- Teaching / dry-run examples：`<workflow>/examples/`
- 已被替代的设计默认由 Git history 保存；仅在仍具教学或治理价值时保留独立历史文档。

只在工作流已经稳定且确有内容时创建目录；不要将 `*-workflow.md`、`*-v2.md` 或 `*-plan.md` 继续平铺在 `docs/` 根目录。
