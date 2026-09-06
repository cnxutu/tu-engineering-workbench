# Living Engineering Model

`tu-engineering-workbench` 描述工程如何进行、产品当前是什么样、正在发生哪些变化，以及可调用哪些工程能力。它不是业务代码集合、历史资料的永久仓库或每次任务必须全量加载的上下文。

## 四个核心区域

| 区域 | 长期语义 | 回答的问题 |
| --- | --- | --- |
| `core/` | Engineering Operating Model | 应如何做工程？ |
| `products/` | Current Verified Product Truth | 产品当前是什么？ |
| `work/` | Delivery Change State | 系统正在发生什么变化？ |
| `plugins/` | Replaceable execution providers | Agent 可调用什么能力？ |

`products/` 记录当前已验证的能力、边界、链路、契约、约束、取舍和实现入口；它不保存某次 Delivery 的探索过程。真实项目仓库仍是可执行实现、完整源码和运行配置的 Authority。`plugins/` 不承载产品事实或 Delivery State。

## Delivery 生命周期与位置

Feature Delivery 的四个工程阶段保持为 Impact → Contract → Execution → Integration & Stabilization；具体 DEV、BUG 或 INT 修改使用 Engineering Task Loop 的 Explore → Plan → Execute → Verify。Verify 仅为当前工程任务返回证据，并回填父 Delivery Artifact。G4 / acceptance 或明确 Closing condition 只代表 Ready to Close；只有用户显式授权 `tu-close-delivery DF-...`，才进入 **Delivery Closing → Integrate → Archive → Closed Index → Retire Active**。Integrate 和 Archive 不是新的 E/P/X/V Stage Shortcut，也不属于第五个工程 Phase。

```text
work/active/<domain>/<product>/DF-YYYYMMDD-NN-<slug>/
    complete Task Package while the Delivery can continue

work/closed/<domain>/<product>/DF-YYYYMMDD-NN.md
    thin closed index after Delivery Closing, Vault Archive verification, and Active Package retirement

work/<domain>/<product>/tasks/archive/
    retained local cold history and pre-V1 evidence during the transition
```

目录在首次有对应 Package 或 Closed Index 时创建，不为形式预建空目录。`active/` 是完整上下文；`closed/` 是可发现的薄索引；`work/**/tasks/archive/` 是 local legacy compatibility cold context。正式 Archive 只在用户授权 Closing 后写入配置的 `tu-vault`，不是默认读取范围。现有 pre-V1 archive 不迁移、不伪造 DF ID。

## DF as Context Address

`DF-YYYYMMDD-NN` 既是 durable Delivery identity，也是 Context Address。Active Package 的 `task.yaml` 使用现有 metadata 模型记录 Product、repositories、capabilities 和 related deliveries；它们让 Agent 从 DF 定位到最小相关上下文，而不是扫描整个 Workbench。

当用户说“继续 DF-xxxx”时：

1. 在 `work/active/` 按 DF ID 定位 Task Package；若未找到，再读 `work/closed/` 中的薄索引。
2. 读取 `task.yaml`、`resume.md` 和当前阶段 Artifact，或 Closed Index 的 Product Truth、archive reference 与相关 Delivery。
3. 只读取所指向 Product 的入口、Capability/Flow、repositories 和真实项目代码/契约。
4. 仅在任务需要时加载 Core 方法与 Plugin Skill。

解释产品能力时从 `products/` 开始；解释工程方法时从 `core/` 开始；只有继续、查询或关闭某个 Delivery 时才从 `work/` 开始。

## Closing semantics

Delivery Closing 的 readiness 由整个 Delivery 的关闭条件决定，而不是任一 DEV、BUG 或 INT 的 Verify；执行权则来自用户的显式 Closing Authorization。`tu-deliver-feature` 只能报告 ready 并建议 `tu-close-delivery`。`completed` 需要 acceptance satisfied，通常也满足 G4；`blocked` 和 `superseded` 也可关闭，但 Archive 不表示成功。blocked 只 Integrate 已验证且仍有效的事实，没有则记录 `knowledge_update_assessment: not-needed`；superseded 仅 Integrate 仍有效的事实，不把被替代的旧设计写成 Current Product Truth，并以 related delivery / superseded-by reference 说明去向。

**Integrate**：将本次已验证且未来可复用的事实更新到对应 `products/` 权威页或 ADR；未形成此类事实时在 Delivery 中明确 `not-needed`。Requirement Authority（approved Product Spec/PRD、decision、Contract 或 acceptance criteria）与 Implementation Reality（code、test、configuration、runtime evidence）分别维护，差异记为 Requirement / Implementation Gap。产品当前状态不应依赖阅读多个旧 Delivery 才能拼出。

**Archive**：按 [Delivery Closing Playbook](../core/playbooks/delivery-closing.md) 将完整 Package 写入 `workspace.local.yaml` 的可选 `external_contexts.tu_vault` target，验证后以 `tu-vault:<relative-path>` 创建 Closed Index，最后 retire active Package。配置缺失或 Archive Verification 失败时保留 active Package。普通 Workbench 运行不依赖 `tu-vault`；只有 Closing 需要已配置 target。

## External boundary and navigation

`tu-vault` 是未来可选的个人/历史记忆，Workbench 是 Engineering Model，项目仓库是 Executable Reality。Obsidian 可改善人类导航，但标准 Markdown 链接、明确目录和 metadata 才是确定性的 Agent 路由；不依赖 WikiLink、Graph View 或 `.obsidian` 配置。
