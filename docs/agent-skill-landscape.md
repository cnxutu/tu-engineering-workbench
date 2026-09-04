# Agent Skill 项目与安装清单

> 快照日期：2026-09-03。Skill、Plugin 与本地缓存会随客户端更新；本页记录核实口径和当日状态，不代替运行时实际暴露的 Skill 列表。

## S1 开源参考模块

| 项目 | 标识 | 定位 | 本机路径 | GitHub |
| --- | --- | --- | --- | --- |
| `skills` | `S1` | 外部开源 Agent Skill 项目参考模块 | 由 `workspace.local.yaml` 解析 | [mattpocock/skills](https://github.com/mattpocock/skills) |

本地 `origin` 已核实指向 `git@github.com:mattpocock/skills.git`，与表中的 HTTPS 查询地址为同一仓库。S1 用于研究开源 Skill 的组织、触发边界、渐进式披露、安装和版本管理；它不是 P0 团队 Skill 的事实来源，也不表示其中 Skill 已安装或已在当前任务启用。修改 S1 前仍须读取其仓库级 `AGENTS.md` 并尊重上游许可证与本地未提交改动。

截至快照日期，本地 S1 的 `skills/` 下有 37 个 `SKILL.md`：`engineering` 18 个、`productivity` 7 个、`misc` 4 个、`in-progress` 8 个。`skills-lock.json` 登记 9 个 Skill：`code-review`、`diagnosing-bugs`、`domain-modeling`、`grill-with-docs`、`handoff`、`implement`、`setup-matt-pocock-skills`、`to-spec`、`to-tickets`。这是 S1 仓库状态，不等同于 P0 当前任务的可用清单。

## GitHub 模板与借鉴结论

| 来源 | 适合借鉴 | 使用边界 |
| --- | --- | --- |
| [Agent Skills 开放规范](https://github.com/agentskills/agentskills) | 以目录为分发单元，`SKILL.md` 为入口，名称和描述承担发现职责。 | 作为跨运行时的最低兼容基线。 |
| [Anthropic Skills](https://github.com/anthropics/skills) 与其 [template](https://github.com/anthropics/skills/tree/main/template) | 自包含 Skill、按需加入 `scripts/`、`references/`、`assets/`，复杂文档能力可拆分资源。 | 仓库同时包含开源和 source-available 内容，复用前逐项核对许可证。 |
| [OpenAI Plugins](https://github.com/openai/plugins) | Codex 当前 Plugin 结构：`.codex-plugin/plugin.json` 加可选 `skills/`、MCP、App、Hook、Agent 与资源。 | [旧 OpenAI Skills Catalog](https://github.com/openai/skills) 已标记 deprecated，不作为新项目模板。 |
| [mattpocock/skills](https://github.com/mattpocock/skills) | 小而可组合的 Skill、用户调用与模型调用分层、分类目录、`skills-lock.json` 与多运行时分发。 | S1 是外部上游克隆；借鉴模式，不直接把全部 Skill 复制进 P0。 |
| [obra/superpowers](https://github.com/obra/superpowers) | 阶段化工程流程、验证门禁、Skill 间显式依赖。 | 其强制流程需要按 P0 指令优先级和任务风险裁剪，不能整体覆盖 P0 规则。 |
| [github/awesome-copilot](https://github.com/github/awesome-copilot) | 社区案例发现、跨工具兼容写法与目录样例。 | 作为候选索引；采用前回到具体来源核实维护状态和许可证。 |

P0 新建或改造 Skill 时采用以下最小基线：

1. 每个 Skill 使用独立目录和必需的 `SKILL.md`；`name` 使用小写字母、数字和短横线，`description` 同时说明能力与触发场景。
2. 入口只保留会改变执行决策的公共约束；大段模式说明放 `references/`，重复且确定的机械操作放 `scripts/`，交付素材放 `assets/`。
3. 仅在需要 Codex UI 元数据时加入 `agents/openai.yaml`；需要团队安装、MCP、Hook 或其他能力组合时再升级为 Plugin。
4. 安装第三方 Skill 前核对来源、许可证、脚本和外部访问权限；不要把“仓库里存在”“缓存到本机”和“当前任务已暴露”视为同一状态。
5. 新增或大改后运行结构校验，并用真实请求验证触发是否准确、引用是否可达、授权边界是否保留。

## 当前环境可用 Skill 快照

本节的“可用”指本任务启动时 Codex 明确暴露、可按触发规则加载的 42 个 Skill；这是回答“现在装了哪些”的首选口径。

| 来源 | 数量 | Skill |
| --- | ---: | --- |
| Codex 系统 | 5 | `imagegen`、`openai-docs`、`plugin-creator`、`skill-creator`、`skill-installer` |
| 个人目录 | 1 | `find-skills` |
| `ai-guidance-workflows` | 3 | `tu-diagnosing-spring-backend-incidents`、`tu-loading-device-inspection-cross-service-context`、`tu-scaffolding-spring-feature-from-prototype` |
| Adobe | 6 | `adobe-batch-edit-photos`、`adobe-create-mockups`、`adobe-create-social-variations`、`adobe-design-from-template`、`adobe-edit-quick-cut`、`adobe-retouch-portraits` |
| Data Analytics | 14 | `analyze-data-quality`、`build-dashboard`、`build-report`、`design-kpis`、`gather-business-context`、`index`、`jupyter-notebooks`、`kpi-reporting`、`market-sizing`、`metric-diagnostics`、`product-business-analysis`、`publish-artifact-to-sites`、`validate-data`、`visualize-data` |
| Google Drive | 5 | `google-drive`、`google-docs`、`google-drive-comments`、`google-sheets`、`google-slides` |
| Artifact Runtime | 7 | `documents`、`pdf`、`presentations`、`spreadsheets`、`excel-live-control`、`template-creator`、`deep-research` |
| Plugin 管理 | 1 | `plugin-management` |

### 不应计入“当前可用”的本机内容

- Codex 系统目录还存在 `review-agent`，但本任务启动清单未暴露它，因此只记为“磁盘存在、当前不可确认可用”。
- Plugin 缓存中存在浏览器控制、Superpowers、Artifact Template 以及 Data Analytics 内部子 Skill 等 `SKILL.md`；缓存存在不能证明当前任务允许直接调用。
- S1 的 37 个源码 Skill 和 `.agents/skills/` 内容属于参考仓库/项目级文件；除非运行时在 S1 范围内重新发现并暴露，否则不计入 P0 当前可用清单。

## 维护口径

更新本页时依次核对：当前任务暴露的 Skill 列表、Codex 系统与个人 Skill 目录、已启用 Plugin 的版本化缓存、S1 的 `git remote -v`、`skills-lock.json` 和 `skills/**/SKILL.md`。数量或版本变化时更新快照日期；不能从可复现证据确认的状态标为 `pending_verification`，不要根据目录名推断已启用。
