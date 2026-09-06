# Playbook：Delivery Closing

## 用途与 Ownership

本 Playbook 定义一个已激活 Feature Delivery 的收尾事务。`tu-deliver-feature` 可以评估 **Ready to Close**，但只有用户显式提供 DF ID 并明确要求关闭、收尾或归档时，`tu-close-delivery` 才可执行写操作。Readiness 不等于 Closing Authorization；单个 DEV / BUG / INT 的 Verify 或 G4 通过均不自动关闭 Delivery。

Delivery Closing 不属于 Feature Delivery 的四个工程 Phase，也不是 Engineering Task Loop 的 E/P/X/V Stage。它保持以下顺序：

```text
Inspect → Closing Assessment → Integrate Product Truth → Archive Full History to tu-vault
→ Verify Archive → Create Closed Index → Retire Active Package → Verify Closing State
```

## Inspect 与 Assessment

从 `work/active/<domain>/<product>/DF-YYYYMMDD-NN-<slug>/` 读取 `task.yaml`、`resume.md` 和当前 Phase Artifact，核对 ID、title、status、phase、gates、product、capabilities、repositories、related deliveries、acceptance evidence、open items、knowledge update 与 artifacts。若仅在 `work/closed/` 找到该 ID，报告 Already Closed；若用户要恢复，使用既有 reopen 机制，不再次 archive。两处都找不到时停止，不猜测。

在任何 mutation 前形成 Closing Assessment：推荐 status、acceptance/Gate 证据、open items、Product Truth Delta、archive target 与 `ready` / `not-ready` / `blocked` / `superseded` 建议。`completed` 要有 acceptance evidence，通常也满足 G4；`blocked` 可阶段性关闭；`superseded` 必须有 related Delivery 或等价 replacement reference。

## Mutation Order

1. **Integrate Product Truth**：先审查 Delta，只将已验证、仍有效且可复用的当前 capability、behavior、flow、architecture、contract、constraint、tradeoff、implementation entry 或 ADR 写入最小相关 `products/` 页面。不得复制探索历史、失败尝试、临时 workaround 或排查日志。Requirement Authority（approved product/spec/decision/contract/acceptance criteria）与 Implementation Reality（code/test/runtime evidence）分别标明；两者不一致时记录 Requirement / Implementation Gap。没有可提升事实时设 `knowledge_update_assessment: not-needed`。
2. **Archive Full History**：仅在 `workspace.local.yaml` 的可选 `external_contexts.tu_vault` 配置完整且可访问时，在其 `delivery_archive_root` 下创建一个 DF Archive Unit。不得写入未配置位置、Workbench 自身、Vault 的其他 taxonomy 或其他 Archive Unit；不得把本机绝对路径写入记录。Archive Unit 至少包含 `summary.md`、`manifest.yaml` 与 `delivery/` 下保持相对结构的完整 Active Package。
3. **Verify Archive**：核对 Unit、summary、manifest、`delivery/task.yaml`、所有 `task.yaml.artifacts` 文件、DF identity 与逻辑 archive reference。存在明显敏感数据（token、credential、private key、customer identifier、internal host、production payload 或未脱敏日志）时停止并要求先脱敏；不静默删改历史。
4. **Create Closed Index**：仅在 Archive Verification 通过后创建 `work/closed/<domain>/<product>/DF-YYYYMMDD-NN.md`。它是 Thin Context Index，不复制 Delivery 历史，至少包含 `Status`、`Result`、`Product`、`Capabilities`、`Repositories`、`Product Truth`、`Knowledge Update`、`Key Decisions`、`Related Deliveries`、`Archive` 与 `Closed At`。Archive 使用逻辑引用 `tu-vault:<relative-path>`。
5. **Retire Active Package**：仅在 Integrate、Archive、Archive Verification 与 Closed Index 全部成功后，才移除对应 active Package。任何中间失败都保留 active Package。
6. **Verify Closing State and Report**：确认 Closed Index、logical archive reference 与 final status 一致，且 active/closed 不再冲突；报告 status、Product Truth Delta、archive reference、retired package 与任何残余风险。

## Archive Unit

`delivery_archive_root` 的上层 taxonomy 由 Vault 自己决定；本 Playbook 只要求一个 DF 一个独立 Unit。`manifest.yaml` 只保存 archive navigation metadata：`delivery_id`、`title`、`status`、`product`、`capabilities`、`repositories`、`related_deliveries`、`closed_at`、`workbench_product_truth`、`source_workbench` 与 `archive_format_version`；superseded 另记录 replacement reference。`summary.md` 提供 Summary、Period、Closing Status、Result、Key Decisions、Product Changes、Known Remaining Issues、Related Deliveries、Current Product Truth logical paths 与 Historical Package `delivery/`，但不替代原始 Artifact Authority。

## Recovery 与 Authorization Boundary

事务可重跑并以当前文件系统、metadata 与 Archive Unit 恢复：已 Integrate 但未 Archive 时继续 Archive；已验证 Archive 但缺 Closed Index 时只创建 Index；Index 存在但 active 仍在时先校验一致性再 retire；active 不在而 Index 已在时报告 Already Closed。Active Package 在全过程中保持 `status: active`，直到最终 Closing 完成；不新增 `closing` status。

用户的显式 Closing Authorization 只授权该 DF 的最小 Product Truth 更新、配置的 Vault Archive Unit、Closed Index 与 Active Package retirement；不授权 commit、push、release、deploy、生产操作、无关 Delivery 或 Vault taxonomy 变更。外部 archive 不可访问时可读取 legacy `work/**/tasks/archive/` 作为 cold compatibility evidence；若外部与 legacy 都不可访问，报告 evidence gap，不伪造恢复。
