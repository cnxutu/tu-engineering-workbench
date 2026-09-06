# 编写指南

编写面向下一位工程师或 AI 的知识：让其知道该加载什么、什么可以信任，以及下一步去哪里核实。目标是导航与决策，不是替代代码阅读。

## 收录标准

只收录以下长期、跨任务复用的信息：

- 关键入口：从哪个仓库、模块、接口或配置开始。
- 关键链路：触发、跨服务跳点、数据/命令方向、关键契约和联调风险。
- 关键设计：服务边界、数据所有权、架构决策和不可违反的约束。

不要收录大段代码、完整接口或 Topic 清单、环境地址、敏感信息、一次性排查笔记，或未经证实的推断。细节以链接指向代码、契约、配置或 `work/` 中的交付归档；无法证实的内容标为 `pending_verification` 或 `unknown`。

## 固定结构

每篇文档只解决一个问题，优先使用以下最小章节并删除不适用项：

| 类型 | 推荐章节 |
| --- | --- |
| 产品/目录入口 | 范围；何时读取；按任务导航；证据状态 |
| 链路 | 触发与边界；关键跳点；契约/时序约束；联调必验项；证据 |
| 设计或 ADR | 决策/边界；责任或所有权；影响与约束；待验证项；证据 |
| 仓库入口地图 | 任务语义；首选代码入口；阅读顺序；待核实项 |
| 产品 Capability | 当前行为；架构/流程；数据与契约；约束/取舍；实现入口；相关 Capability；证据 |

使用短段落、表格和链接表达稳定结论；同一事实只保留一个权威页面，其他页面链接到它。Capability 页面说明“现在是什么”，不叙述“先考虑 A、再改 B”的 Delivery 历史；必要时仅链接相关 Closed Index。链路只列关键跳点，不复制每个方法调用；入口地图只列首选起点，不替代完整源码索引。

## 公共规则维护

维护 `core/rules/` 下的公共规则时，默认使用简洁中文：一条只表达一个可执行要求，条件、动作和例外明确。路径、命令、代码标识符、配置键和技术名称保持原始拼写，不为统一语言而翻译。

只保留可长期复用且可验证的规则；示例、解释和项目事实放到按需读取的文档。清晰度优先于英文、中文或形式化措辞本身。

## 产品文档

每个产品从 `index.md` 开始。入口应说明范围、何时读取、证据状态，并链接最小必要的领域、架构、流程、仓库和决策文档。Core 保持通用，只提供方法和契约，不承载产品事实；产品事实应放在产品树中，并用 repository manifest 维护仓库在该产品中的责任。项目标记、仓库身份和产品绑定只在 `core/registry/repositories.yaml` 维护。

`products/` 回答“产品现在是什么”。当前行为、架构、flow、contract、ownership、constraint、implementation entry 和已确认 ADR 属于 Current Product Truth。`context/domain/`、vendor / SDK 摘要、技术背景与候选设计属于 Supporting Context：它们可保留在产品树，不自动拥有 Current Product Truth Authority，不替代代码、Contract 或验证证据，并只在任务需要时加载；重要结论须标明 evidence / verification state。

现有按版本存放的 PRD、原型和旧需求是 Transition / Existing Historical Material。它们不移动、不删除，但必须明确 Current Requirement 与 Historical Reference 的区别。Current Requirement 由 approved Product Spec/PRD、Product Decision、Contract 或 acceptance criteria 确认；Implementation Reality 由代码、测试、配置和运行证据确认。两者不一致时记录 Requirement / Implementation Gap，不让代码反向否定已批准需求；未来不得让所有递增版本 PRD 自动持续拥有 Current Truth Authority，实际迁移待 tu-vault archive 模型建立后再进行。

采用渐进式读取：以链接代替重复细节，每篇文档只聚焦一个主题。必要时标注负责人或来源。通常优先级是：仓库局部说明与代码，其次产品知识，最后 Core。

## 事实与引用

每条重要产品结论都要说明证据与可信度。优先引用稳定的源码、测试、契约或批准设计记录。目标架构必须明确标为目标，不能证明当前代码行为；不确定时直接使用 `pending_verification` 或 `unknown`，不要猜测。

完成引入跨服务事实的工作前，评估服务地图、所有权、契约、拓扑或流程是否需要修订。有证据时更新适用文档，并在任务元数据中记录结果。

## 记录

`Core` 下的 [契约](../../core/contracts/) 是文档契约，不是可执行校验器。任务记录应保持简洁：活跃 Delivery 位于 `work/active/`；用户授权 Closing 后，完整过程 Archive 至配置的 `tu-vault` 并验证，再在 `work/closed/` 留下薄索引、retire active Package。`work/<domain>/<product>/tasks/archive/` 是 legacy / local cold history。持久架构选择使用 ADR；加入证据前先脱敏。单个 Task Loop Verify 只回填父 Artifact；只有 Delivery Closing 时的 Integrate 才提炼已验证且仍有效的结论为产品当前事实，不直接把排查过程写入 `products/`。

仓库配置见 [接入指南](../guides/integration-guide.md)，AI 读取、Skill 与 Template 使用见 [工程师使用与维护指南](../guides/usage-guide.md)。
