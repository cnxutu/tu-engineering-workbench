# Playbook：Delivery Closing

## 用途与 Ownership

本 Playbook 定义一个已激活 Feature Delivery 的收尾事务。`tu-deliver-feature` 可以评估 **Ready to Close**，但只有用户显式提供 DF ID 并明确要求关闭、收尾或归档时，`tu-close-delivery` 才可执行写操作。Readiness 不等于 Closing Authorization；单个 DEV / BUG / INT 的 Verify 或 G4 通过均不自动关闭 Delivery。

Delivery Closing 不属于 Feature Delivery 的四个工程 Phase，也不是 Engineering Task Loop 的 E/P/X/V Stage。它保持以下顺序：

```text
Inspect → Closing Assessment → Final Product Truth Reconciliation → Sensitive Data Review
→ Resolve deterministic Archive Unit → Archive Full History to tu-vault
→ Finalize Archived Snapshot Metadata → Verify Archive → Create Closed Index
→ Retire Active Package → Verify Closing State
```

## Inspect 与 Assessment

从 `work/active/<domain>/<product>/DF-YYYYMMDD-NN-<slug>/` 读取 `task.yaml`、`resume.md` 和当前 Phase Artifact，核对 ID、title、status、phase、gates、product、capabilities、repositories、related deliveries、acceptance evidence、open items、knowledge update 与 artifacts。若仅在 `work/closed/` 找到该 ID，报告 Already Closed；若用户要恢复，使用既有 reopen 机制，不再次 archive。两处都找不到时停止，不猜测。

在任何 mutation 前形成 Closing Assessment：推荐 status、acceptance/Gate 证据、open items、整个 Delivery 的最终 Product Truth Delta（含此前 Sync 的结论及其后续变化）、archive target 与 `ready` / `not-ready` / `blocked` / `superseded` 建议。`completed` 要有 acceptance evidence，通常也满足 G4；`blocked` 可阶段性关闭；`superseded` 必须有 related Delivery 或等价 replacement reference。

## Mutation Order

1. **Final Product Truth Reconciliation**：审查整个 Delivery 的最终 Delta，并复核期间已由合法 Product Truth Sync 写入的结论是否仍正确；不重复写入相同结论，修正后续工作已改变的结论，并补充最终尚未同步的事实。只将已验证、仍有效且可复用的当前 capability、behavior、flow、architecture、contract、constraint、tradeoff、implementation entry 或 ADR 写入最小相关 `products/` 页面。不得复制探索历史、失败尝试、临时 workaround 或排查日志。Requirement Authority（approved product/spec/decision/contract/acceptance criteria）与 Implementation Reality（code/test/runtime evidence）分别标明；两者不一致时记录 Requirement / Implementation Gap。该 Closing assessment 仍按 Delivery metadata contract 设置 `knowledge_update_assessment`；Sync 从不预先设置它。
2. **Sensitive Data Review**：在任何 Archive copy 前检查 token、credential、API key、private key、customer identifier、internal host、private network information、production payload、未脱敏日志及其他明确敏感数据。发现时停止 Closing Transaction，输出 `Sensitive Data Review Failed`、文件、finding type 与阻塞原因；不得静默删改历史、Archive、创建 Closed Index 或 retire active。用户完成脱敏后可重新执行 Closing。
3. **Resolve deterministic Archive Unit**：仅在 `workspace.local.yaml` 的 `external_contexts.tu_vault.path` 已配置且可访问，并且 tracked `core/registry/external-contexts.yaml` 定义有效 `delivery_archive_root` 时使用 `<delivery_archive_root>/<DF-ID>/`。例如 shared root 为 `04_Work/deliveries` 时，唯一 Unit 为 `04_Work/deliveries/DF-20260906-01/`，唯一 logical reference 为 `tu-vault:04_Work/deliveries/DF-20260906-01`。不得写入 Workbench、嵌套目录树、未配置位置、Vault 的其他 taxonomy 或额外年/月/domain/product/slug 层级；不得把本机绝对路径写入记录。
4. **Archive Full History and finalize snapshot**：先复制完整 active Package 到 Unit 的 `delivery/`，不改动 Workbench Active Source。仅在 archived copy 中将 `delivery/task.yaml` finalise 为最终 `status`（`completed`、`blocked` 或 `superseded`）并写入 `archived_at`、`archive_reference` 与 `closed_index`；随后生成 `summary.md` 和 `manifest.yaml`。Re-run 时先 inspect existing manifest、archived task metadata、delivery ID、status、archive reference、closed time 和 artifacts；已经完整一致时不覆盖，从未完成的后续步骤继续。
5. **Verify Archive**：核对 Unit、summary、manifest、`delivery/task.yaml` 与所有 `task.yaml.artifacts` 文件。`manifest.yaml` 与 archived `delivery/task.yaml` 必须对 `delivery_id`、final `status`、`closed_at` / `archived_at` 与 `archive_reference` 一致；不一致则失败，不得继续 Closed Index 或 retire active。
6. **Create Closed Index**：仅在 Archive Verification 通过后创建 `work/closed/<domain>/<product>/DF-YYYYMMDD-NN.md`。它是 Thin Context Index，不复制 Delivery 历史，至少包含 `Status`、`Result`、`Product`、`Capabilities`、`Repositories`、`Product Truth`、`Knowledge Update`、`Key Decisions`、`Related Deliveries`、`Archive` 与 `Closed At`。Status 只可为 `completed`、`blocked` 或 `superseded`；`superseded` 的 replacement 以 `Related Deliveries` 或 `Superseded By` 指向。Archive 使用上述唯一 logical reference。
7. **Retire Active Package**：仅在最终 Product Truth reconciliation、Sensitive Data Review、Archive、Archive Verification 与 Closed Index 全部成功后，才移除对应 active Package。任何中间失败都保留 active Package。
8. **Verify Closing State and Report**：确认 Closed Index、manifest 与 archived task metadata 的 DF identity、final status、logical archive reference 和 closed time 一致，且 active/closed 不再冲突；报告 status、Product Truth Delta、archive reference、retired package 与任何残余风险。

## Archive Unit

`core/registry/external-contexts.yaml` 定义共享的 `delivery_archive_root`；`workspace.local.yaml` 只解析本机 Vault 物理路径。本 Playbook 只负责 deterministic `<delivery_archive_root>/<DF-ID>/`：

```text
<delivery_archive_root>/<DF-ID>/
├── summary.md
├── manifest.yaml
└── delivery/
```

Unit 中的 `summary.md` 是给人和 Obsidian 导航的历史摘要，不替代 Artifact Authority；`manifest.yaml` 是 machine-readable navigation metadata，至少包含 `delivery_id`、`title`、`status`、`product`、`capabilities`、`repositories`、`related_deliveries`、`closed_at`、`archive_reference`、`workbench_product_truth`、`source_workbench` 与 `archive_format_version`，superseded 另记录 replacement reference；`delivery/` 保持完整 Historical Artifact Package 的相对结构。`delivery/task.yaml` 是 finalized historical metadata snapshot，不得保留 `status: active`。

## Recovery 与 Authorization Boundary

事务可重跑并以当前文件系统、metadata 与 Archive Unit 恢复：已 Integrate 但未 Archive 时继续 Sensitive Review 和 Archive；已验证 Archive 但缺 Closed Index 时只创建 Index；Index 存在但 active 仍在时先校验一致性再 retire；active 不在而 Index 已在时报告 Already Closed。Workbench active `task.yaml` 是 Closing Transaction Recovery Source，整个过程中保持 `status: active` 且不写 `archived_at`、`archive_reference` 或 `closed_index`；Vault `delivery/task.yaml` 是 Final Historical Snapshot。Reopen 只能将 immutable `<Archive Unit>/delivery/` restore/copy 为 `work/active/<domain>/<product>/<DF-ID>-<slug>/` 的 Active Package；不得把 Unit 的 `summary.md` 或 `manifest.yaml` 复制进 active，不得 move、delete 或 modify Vault Unit。优先从 archived metadata 恢复 slug；没有可靠 slug 时从 archived title 生成符合现有规则的 readable slug。active copy 重置为 `status: active` 并移除上述 archive fields，在 `04-integration-log.md` 记录 Reopened At、Reason、Previous Closing Status、Previous Closed At、Archive Reference、related BUG/CAP 和 Current Classification。legacy `work/**/tasks/archive/` 仍只作 compatibility fallback。

用户的显式 Closing Authorization 只授权该 DF 的最小 Product Truth 更新、配置的 Vault Archive Unit、Closed Index 与 Active Package retirement；不授权 commit、push、release、deploy、生产操作、无关 Delivery 或 Vault taxonomy 变更。外部 archive 不可访问时可读取 legacy `work/**/tasks/archive/` 作为 cold compatibility evidence；若外部与 legacy 都不可访问，报告 evidence gap，不伪造恢复。
