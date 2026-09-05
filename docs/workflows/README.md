# Workflow Best Practices

本目录保存已形成稳定使用方式的 Workbench 工程工作流最佳实践，供工程师按需阅读；它不替代 Runtime Skill Contract。

当前工作流：

- [Feature Delivery](feature-delivery/README.md)：从需求/原型到长期联调、Bug 与归档的完整交付生命周期。

后续成熟工作流使用 `workflows/<workflow-name>/`，按以下边界维护：

- Current Best Practice：`<workflow>/README.md`
- Skill integration / provider experience：`<workflow>/skill-integration.md`
- Teaching / dry-run examples：`<workflow>/examples/`
- Superseded proposals / historical design：`<workflow>/history/`

只在工作流已经稳定且确有内容时创建目录；不要将 `*-workflow.md`、`*-v2.md` 或 `*-plan.md` 继续平铺在 `docs/` 根目录。
