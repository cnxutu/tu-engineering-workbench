# 项目导航与维护地图

本页面向 `tu-devkit` 与 `ai-guidance` 的维护者，用于理解项目骨架、两条协作链路和扩展入口。它不是 Codex 的默认上下文；AI 的运行时入口始终是 [`../AGENTS.md`](../AGENTS.md)。

## 两条链路

### 1. AI 运行时加载链路

```mermaid
flowchart TD
    U[用户任务] --> R[仓库根目录 AGENTS.md]
    R --> P0[ai-guidance/AGENTS.md\n公共入口]
    P0 --> S[识别项目范围与任务类型]
    S --> L[目标仓库/目录的局部 AGENTS.md]
    L --> C{按任务条件加载}
    C --> CR[Core 规则、角色或工作流]
    C --> PK[最小必要的产品知识]
    C --> SK[适用的 Codex Skill]
    CR --> E[核实代码、契约、配置与测试]
    PK --> E
    SK --> E
    E --> I[最小实现与风险相称验证]
    H[README.md 与 docs/] -. 仅供维护者按需查阅 .-> U
```

核心原则：`AGENTS.md` 决定 AI **何时读取什么**；产品文档用于导航，当前代码、契约、配置和测试才用于核实现状。P0 提供公共约束，不会因被设为 Primary 而自动成为目标代码的阅读或修改范围。

### 2. 人类使用与维护链路

```mermaid
flowchart TD
    M[维护者的需求] --> T{要做什么？}
    T -->|日常使用 Codex| U[usage-guide.md\n范围、Compact Syntax、Plugin 调用]
    T -->|接入新仓库| I[integration-guide.md\nbootstrap/、仓库清单与本机路径]
    T -->|维护产品事实| A[authoring-guide.md + governance.md\n证据、目录结构与归档]
    T -->|维护公共规则| R[authoring-guide.md\n公共规则维护] --> C[core/rules/]
    T -->|维护角色/工作流| C
    T -->|维护原生 Skill/Plugin| P[ai-guidance/plugins/ai-guidance-workflows/\nSkill、manifest 与测试]
    U --> V[validate_guidance.py]
    I --> V
    A --> V
    R --> V
    P --> PT[test-plugin.sh\n更新 cachebuster、重装 Plugin]
```

核心原则：面向人的说明和维护规范放在 `README.md`、`docs/`；面向 AI 的最小运行时约束放在 `AGENTS.md` 与按需加载的 Core、产品知识、原生 Skill 中。不要把人类教程反向塞进 AI 默认上下文。

## 项目骨架与职责

| 位置 | 职责 | 何时进入或修改 |
| --- | --- | --- |
| 根目录 `AGENTS.md` | 将 Codex 引导到 `ai-guidance/AGENTS.md` | 调整 P0 的唯一 AI 协作入口时。 |
| `ai-guidance/AGENTS.md` | 公共运行时入口：范围、任务简写、条件读取、优先级与事实边界 | 调整跨仓库且长期稳定的 AI 加载或协作规则时。 |
| `ai-guidance/core/` | 跨产品复用的角色、规则、工作流、契约和模板 | 需要通用方法而非产品事实时；遵循渐进式加载。 |
| `ai-guidance/products/` | 已有证据支撑的产品、服务边界、链路、决策和任务历史 | 改变长期入口、服务/数据边界、公开契约或端到端流程时。 |
| `ai-guidance/docs/` | 仅供维护者查阅的使用、接入、编写、治理和项目导航 | 调整人类使用方式、维护入口或知识治理规则时。 |
| `ai-guidance/bootstrap/` | 目标仓库接入 P0 的 `AGENTS.md` 与清单模板 | 接入新仓库或修订接入模板时。 |
| `ai-guidance/scripts/`、`tests/` | 文档结构、链接、路径和契约的校验实现 | 调整校验能力或修复校验问题时。 |
| `workspace.example.yaml` / `workspace.local.yaml` | 可提交的路径模板 / 不提交的本机绝对路径映射 | 接入或移动本机工作区时；不得把本机路径写入可提交模板。 |
| `ai-guidance/.agents/plugins/marketplace.json` | 团队 Plugin 市场清单；`ai-guidance/` 是市场根目录 | 新增 Plugin、调整市场元数据或重新配置本地市场时。 |
| `ai-guidance/plugins/ai-guidance-workflows/` | 团队原生 Codex Skill 与 Plugin 测试 | 新增、修改或重命名团队 Skill 时。 |

## 常见维护入口

| 目标 | 首先阅读 | 主要修改位置 | 必做核对 |
| --- | --- | --- | --- |
| 使用 Compact Syntax 或团队 Skill | [使用指南](usage-guide.md) | 通常无需修改 | 安装 Plugin 后新建 Codex 任务以重新发现 Skill。 |
| 接入新服务仓库 | [接入指南](integration-guide.md) | `bootstrap/`、仓库清单、目标仓库局部 `AGENTS.md`、本机映射 | 不猜测路径或产品绑定；运行 guidance 校验。 |
| 补充产品链路、边界或决策 | [编写指南](authoring-guide.md)、[治理规范](governance.md) | `products/` 中最小必要的权威页面 | 记录证据和可信度；不以文档替代代码核实。 |
| 修改跨仓库公共规则 | [编写指南](authoring-guide.md) 的“公共规则维护” | `AGENTS.md` 或 `core/` | 保持条件、动作、例外清晰；避免加入产品事实。 |
| 新增或更新团队 Skill | [使用指南](usage-guide.md) 的 Plugin 章节 | `ai-guidance/plugins/ai-guidance-workflows/skills/` | 更新引用和测试；更新 cachebuster、重装 Plugin，并在新任务验证发现结果。 |
| 修改校验脚本或结构规则 | 受影响脚本与测试 | `scripts/`、`tests/` 或 Plugin 测试 | 运行对应校验；不把校验器当作产品事实来源。 |

## 扩展原则

1. 先判断新增内容属于运行时约束、通用方法、产品事实、维护者说明、接入模板还是原生 Skill；只放入一个权威位置，其他位置用链接导航。
2. 新增运行时读取规则时，明确触发条件、最小读取集和不默认读取的内容，避免扩大每个任务的上下文。
3. 新增产品事实时，先取得代码、契约、测试或批准记录等可复现证据；不确定内容标为 `pending_verification` 或 `unknown`。
4. 新增原生 Skill 时，保持触发描述具体、正文精炼，并同步 Plugin 测试、使用说明和更新安装后的发现流程。
5. 每次维护后，运行与改动相称的校验；文档结构变更至少执行：

   ```powershell
   python ai-guidance/scripts/validate_guidance.py --repo-root .
   git diff --check
   ```

## 维护边界速查

- AI 默认阅读：根目录 `AGENTS.md`、`ai-guidance/AGENTS.md`、当前任务触发的局部约束和最小必要上下文。
- 人类按需阅读：`README.md`、`docs/`、接入与治理说明、项目导航页。
- 当前事实：代码、契约、配置、测试和可复现命令结果。
- 长期知识：经证据支撑的产品入口、链路、边界和设计决策。
- 不应进入知识库：密钥、敏感运行数据、全量环境配置、未经核实猜测和一次性排查细节。
