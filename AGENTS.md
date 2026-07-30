# ai-guidance 运行时约束

本文件是 Codex 在 P0 中的最小运行时入口：只定义**工程范围、任务简写、条件读取、角色边界和事实优先级**。`README.md`、`docs/` 与产品文档用于人工维护或在下列条件满足时按需读取，不是默认上下文。

## 1. 会话范围与路径地图

会话首次任务中，Codex 应从用户文本直接识别项目标记 `P0`–`P4`、`K1`、`K2`；无需固定的范围声明格式。识别出的标记共同构成本次范围，后续消息沿用该范围，直到用户明确变更。

| 标记 | 工程 | 本机路径 |
| --- | --- | --- |
| `P0` | `tu-devkit`：AI 上下文与开发工具 | `workspace.yaml` |
| `P1` | `c-drone-inspection`：巡检业务 | `workspace.yaml` |
| `P2` | `c-iot-server`：IoT 服务 | `workspace.yaml` |
| `P3` | `c-iot-gateway`：协议与连接入口 | `workspace.yaml` |
| `P4` | `ad-iot-codec-adapter-dji`：DJI 编解码适配 | `workspace.yaml` |
| `K1` | `knowledge-hub`：Knowledge Hub 后端 | 待登记 |
| `K2` | `knowledge-web`：Knowledge Hub 前端 | 待登记 |

项目标记可出现在自然语言、列表、括号或字段中；`P1 + P2`、`P1,P2`、`P1，P2`、`P1、P2`、`P1 P2` 等均识别为 P1 与 P2。短横线 `-` 或连接号 `–` 表示连续范围：`P0–P4` 表示 P0、P1、P2、P3、P4；它可与其他标记混用，例如 `P0、P2-P4`。`范围：` 只是提高可读性的可选前缀，不是必需格式。

需打开、核实或修改已登记源码时，读取 `workspace.yaml` 获取绝对路径。范围外项目仅可作为依赖背景，不读取、核实或修改其源码。K1/K2 在路径登记前不得假定其源码可访问。

## 2. Prompt Compact Syntax

用户可用一个大写任务类型与小写上下文字段描述任务。大小写有语义：`B` 是 Bugfix，`b` 是 Background。

| 大写类型 | 含义 | 默认 Core 角色/工作流 |
| --- | --- | --- |
| `F` | Feature Development，开发 | 后端任务：`Java Engineer` + `feature-development` |
| `B` | Bugfix，缺陷修复 | 后端任务：`Java Engineer` + `bug-analysis` |
| `R` | Refactor，重构 | `Backend Architect` + `refactor-analysis` |
| `A` | Architecture，架构设计/评审 | `System Designer` 或 `Backend Architect` + `architecture-review` |
| `X` | Cross-service Change，跨服务变更 | `System Designer` + `architecture-review` |
| `C` | Code Review，代码评审 | `Code Reviewer` |
| `D` | Discovery / Feasibility，可行性探索 | 按范围选择 `System Designer` 或 `Backend Architect`；只调查、核实和比较，不修改代码 |
| `P` | Planning / Change Plan，变更计划 | 按范围选择 `System Designer` 或 `Backend Architect`；锁定边界与计划，不直接实施 |

| 小写字段 | 含义 |
| --- | --- |
| `g` | Goal，目标 |
| `b` | Background，背景 |
| `s` | State，当前状态 |
| `c` | Constraints，约束 |
| `r` | Result，期望结果 |
| `i` | Impact，影响范围 |
| `p` | Plan，实施要求/执行步骤 |
| `v` | Verification，验证方式 |
| `q` | Questions，需要探索或回答的问题（`D`） |
| `d` | Decision，已确认方案或决策（`P`） |

收到此格式时，按类型加载表中最小必要的 `core/agents/`、`core/skills/` 与规则；K2 或其他非后端任务没有适用角色时，不强行套用 Java 角色。完整示例和解析细节见 `core/prompt-compact-syntax.md`，仅在需要查阅时读取。

`D` 和 `P` 的默认边界是**不修改代码**：`D` 的产物是带证据的可行性结论与推荐下一步；`P` 的产物是已确认方案对应的修改边界、代码入口、步骤、风险与验证计划。实施须由后续 `F/B/R/X` 任务明确授权。

## 3. 条件读取

| 条件 | 必须读取 | 不默认读取 |
| --- | --- | --- |
| 修改 P0 中 `ai-guidance` 的产品知识、架构、流程、清单或任务记录 | `docs/authoring-guide.md`、`docs/governance.md`，以及受影响文档 | 其他产品知识与所有使用教程 |
| 修改 P0 的工具/脚本 | 目标目录局部约束、README 和代码 | 产品知识、知识编写规范 |
| 修改 P1/P2/P3/P4/K1/K2 的单项目代码 | 范围内仓库的局部约束、相关代码与本任务所需 Core | `README.md`、`docs/usage-guide.md`、P0 知识收录规范、无关产品材料 |
| `X`、`i` 涉及多个项目，或任务明确涉及服务关系/OSD/指令/协议/缓存链路 | `products/company/device-inspection-platform/index.md`，再按链接读取最小必要的架构、Flow、入口或缓存资料 | 整个产品目录 |
| K1/K2 的 Knowledge Hub 产品架构或跨端任务 | `products/personal/knowledge-hub/index.md`，再按链接读取所需资料 | 无关公司产品材料 |

任务涉及多个仓库、公开 API、消息契约或数据所有权时，必须先确认产品知识和目标代码；不能以 P0 文档替代代码核实。

## 4. 事实与安全边界

冲突优先级：**用户最新明确要求与当前代码/仓库局部约束 > 产品知识 > Core 通用规则**。

只能将已读取代码、契约、配置或带证据的产品知识作为事实；未知项标为待核实。不得记录或输出密钥、Token、凭据、客户数据或其他敏感运行信息。
