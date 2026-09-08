# Workbench 治理规范

P0 `tu-engineering-workbench` 是 Living Engineering Model：`core/` 提供工程运行模型，`products/` 保存 Current Product Truth，`work/` 保存 Delivery Change State，`plugins/` 提供可替换执行能力。治理要求读者能区分已验证事实与假设，并追溯事实证据。

产品 Current Truth 维护关键入口、链路和设计边界；评审新增内容时，同时检查它是否可长期复用、是否足够精炼、是否已有权威页面。不能满足任一项的细节应放入代码、契约、配置或 `work/` 交付记录，而非新增产品文档。仓库身份与产品绑定由 registry 维护；仓库责任与已验证产品知识由产品 repository manifest 维护。

## 证据与过期性

产品事实必须具备可复现来源：代码位置、API 或消息契约、已提交文档、测试或已批准的运行记录。标注来源，并说明它证明的是当前行为、目标设计还是未决假设；没有证据的内容使用 `pending_verification` 或 `unknown` 标记。

当任务改变服务边界、共享数据所有权、公开契约、部署拓扑或端到端流程时，必须复核产品知识。若任务改变了这些事实，更新对应产品文档并写入证据；若无需更新，在任务元数据中记录 `not-needed`。发布或基础设施发生重大变化后，应复核易变事实；过期证据要淘汰或标注，不能默认为当前事实。

## 敏感信息

禁止在 Workbench 中保存凭据、Token、私钥、客户标识、生产 payload、内部主机信息或未脱敏日志。应引用受控来源或使用脱敏示例；证据引用必须在不复制敏感内容的前提下仍有意义。

## ADR、Product Knowledge 与 Delivery State

针对持久且重要的架构选择，在产品 `decisions/` 下创建 ADR，例如服务边界、数据所有权、契约、持久化策略或重大技术方向。ADR 应说明决策、背景、候选方案、结果和证据。

`products/` 是 Current Verified Product Truth：稳定、经验证且长期可复用的当前行为、架构、flow、contract、ownership、constraint、implementation entry 和 ADR 通常属于这里。`context/domain/`、vendor / SDK 摘要、技术背景与候选设计可作为 Supporting Context 留在产品树，但不自动成为 Current Product Truth，不替代代码、Contract 或验证证据，只按任务需要读取并标明 evidence / verification state。

`work/` 是 Delivery Change State。新 Delivery 在 `work/active/<domain>/<product>/` 保存完整 Package；用户授权 Closing、Vault Archive 验证通过后，才在 `work/closed/<domain>/<product>/` 保留 Thin Context Index 并 retire active Package。`work/**/tasks/archive/` 是 legacy / local cold history；pre-V1 archive 保持原样，不能与 `active/`、`closed/` 并列为当前正式结构。任务记录不是产品 Current Truth 默认入口，也不是保存密钥或临时草稿的地方。

普通 Delivery 的候选事实仍记录在 `work/`；但显式 Product Truth Sync 可在无 DF 的独立任务，或 Delivery 中的独立 DEV / BUG 后，基于可靠工程证据将同时满足 Verified、Current、Durable 与 Independently Valid 的精炼结论写入 `products/` 的唯一权威页面或 ADR。Sync 不修改 Delivery metadata、状态或 Archive；没有满足 Gate 的结论则不写入。Delivery Closing 在用户显式授权后对整个 Delivery 做最终 reconciliation：复核此前同步的结论是否仍正确，不重复同一结论，修正被后续工作改变的结论，并补充最终尚未同步的 Delta。`completed` 通常须满足 G4 / acceptance；`blocked` 与 `superseded` 也可关闭，但只 Integrate 仍有效的事实，且不能把被替代设计写成 Current Product Truth。Archive 表示 lifecycle closed / cold context，不等于成功。Sensitive Data Review 通过后，完整 Package 才 copy 至配置 `tu-vault` 的 deterministic Unit 并 finalise archived snapshot；验证后才创建 Closed Index。Closed Index 是当前 Closed Context Authority，Vault manifest 与 archived task metadata 是 Final Historical Snapshot Authority；它们只保留结果、Product Truth links、关键决定与同一逻辑 archive reference，不复制过程正文。

参见 [编写指南](authoring-guide.md)、[接入指南](../guides/integration-guide.md) 和 [任务元数据契约](../../core/contracts/task-metadata.schema.yaml)。
