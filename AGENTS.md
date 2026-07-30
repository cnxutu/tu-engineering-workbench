# ai-guidance 运行时约束

本文件是 P0 作为 Primary（主仓库）时 Codex 的最小运行时入口：先定义**工程范围、任务简写、条件读取、角色边界、指令优先级和事实可信度**，再将公共约束作用于本会话识别出的范围内仓库。Primary 只提供公共协作约束，不自动成为任务的代码阅读、核实或修改范围，也不以 P0 文档替代目标仓库的局部约束与代码。本文件不能覆盖 Codex 平台、系统或开发者施加的约束。`README.md`、`docs/` 与产品文档用于人工维护或在下列条件满足时按需读取，不是默认上下文。

## 1. 会话范围与路径地图

当 P0 被设置为 Primary 时，Codex 每次任务都应先读取本文件的公共约束，无需用户重复提及 `P0`。会话首次任务中，Codex 再从用户的直接任务说明中识别独立项目标记 `P0`–`P4`、`K1`、`K2`；无需固定的范围声明格式。除 Primary 的默认加载外，识别出的标记共同构成本次可操作工程范围，后续消息沿用该范围，直到用户明确变更。引用的示例、代码块、文档标题、路径或历史记录中的项目标记不自动扩大范围；语义不明确时先确认，不猜测扩大可操作范围。

| 标记 | 工程 | 本机路径 |
| --- | --- | --- |
| `P0` | `tu-devkit`：AI 上下文与开发工具 | 本机工作区映射 |
| `P1` | `c-drone-inspection`：巡检业务 | 本机工作区映射 |
| `P2` | `c-iot-server`：IoT 服务 | 本机工作区映射 |
| `P3` | `c-iot-gateway`：协议与连接入口 | 本机工作区映射 |
| `P4` | `ad-iot-codec-adapter-dji`：DJI 编解码适配 | 本机工作区映射 |
| `K1` | `knowledge-hub`：Knowledge Hub 后端 | 待登记 |
| `K2` | `knowledge-web`：Knowledge Hub 前端 | 待登记 |

项目标记可出现在自然语言、列表、括号或字段中；`P1 + P2`、`P1,P2`、`P1，P2`、`P1、P2`、`P1 P2` 等均识别为 P1 与 P2。短横线 `-` 或连接号 `–` 表示连续范围：`P0–P4` 表示 P0、P1、P2、P3、P4；它可与其他标记混用，例如 `P0、P2-P4`。`范围：` 只是提高可读性的可选前缀，不是必需格式。

例如，用户要求调整 `P1` 的功能时，应先应用 P0 的公共约束，再将 P1 作为可操作范围，读取 P1 的局部 `AGENTS.md`（如有）、相关代码与按需上下文；此时 P0 不在可修改范围。仅当会话首次任务明确提及 `P0` 时，P0 才进入可操作范围，并在后续消息中默认沿用。

需打开、核实或修改已登记源码时，优先读取未提交的 `workspace.local.yaml` 获取本机绝对路径；首次接入时从已提交的 `workspace.example.yaml` 复制创建该文件。缺少本机映射时报告阻塞并请求路径，不猜测源码位置。范围外项目仅可作为依赖背景，不读取、核实或修改其源码。K1/K2 在路径登记前不得假定其源码可访问。

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

若已安装团队插件 `ai-guidance-workflows`，按以下条件优先使用其原生 Codex Skill；未安装时继续遵循本文件引用的 Core 工作流：

- `B` 涉及未知根因的 Spring Boot 异常、消息处理失败、数据不一致、性能退化或线上事故时，使用 `tu-diagnosing-spring-backend-incidents`。
- `X`，或任务明确涉及 P1–P4 间的 API、消息、数据归属、协议、上/下行链路、MQTT、OSD、DJI 或跨服务发布依赖时，使用 `tu-loading-device-inspection-cross-service-context`。
- 仅出现多个项目标记但未说明服务交互时，不因该标记自动加载 P1–P4 的全局上下文；先确认关联边界或分别按单项目任务处理。

## 3. 条件读取与公共开发约束

### 3.1 公共开发约束

凡是阅读、评审、设计或修改源码、配置、脚本、测试的任务，先读取 `core/rules/development.md`。它是所有服务通用的 Codex 开发基准，规定上下文装载、分析与确认、最小实现、调试、验证、交接和安全边界；语言、框架、仓库和产品专属要求仍按下表条件读取，且仓库局部约束优先。

纯知识维护、纯文案或不涉及工程实现的问答不默认读取该规则。

### 3.2 按任务读取的上下文

| 条件 | 必须读取 | 不默认读取 |
| --- | --- | --- |
| 修改 P0 中 `ai-guidance` 的产品知识、架构、流程、清单或任务记录 | `docs/authoring-guide.md`、`docs/governance.md`，以及受影响文档 | 其他产品知识与所有使用教程 |
| 修改 P0 的工具/脚本 | `core/rules/development.md`、目标目录局部约束、README 和代码 | 产品知识、知识编写规范 |
| 修改 P1/P2/P3/P4/K1/K2 的单项目代码 | `core/rules/development.md`、范围内仓库的局部约束、相关代码与本任务所需专项 Core | `README.md`、`docs/usage-guide.md`、P0 知识收录规范、无关产品材料 |
| `X`、`i` 涉及多个项目，或任务明确涉及服务关系/OSD/指令/协议/缓存链路 | `products/company/device-inspection-platform/index.md`，再按链接读取最小必要的架构、Flow、入口或缓存资料 | 整个产品目录 |
| K1/K2 的 Knowledge Hub 产品架构或跨端任务 | `products/personal/knowledge-hub/index.md`，再按链接读取所需资料 | 无关公司产品材料 |

任务涉及多个仓库、公开 API、消息契约或数据所有权时，必须先确认产品知识和目标代码；不能以 P0 文档替代代码核实。

## 4. 指令、事实与安全边界

### 4.1 指令优先级

指令冲突时，按以下顺序处理：**Codex 平台、系统和开发者约束 > 用户最新明确要求 > 目标仓库或目录的局部 `AGENTS.md` > 本文件与 Core 公共规则 > 产品文档、模板和示例**。同一层级的补充约束应一并遵循；只有同一事项互相矛盾时才采用较高优先级来源。

`core/skills/` 是本仓库定义的工作流参考，不等同于 Codex 平台的 `SKILL.md`。适用的 Codex Skill 必须先读取并遵循；本仓库工作流只能补充其执行方式，不能覆盖平台、系统或开发者约束。

### 4.2 事实可信度

当前代码、契约、配置、测试和可复现命令结果用于证明**当前事实**；带证据的产品知识用于提供已确认上下文；Core 规则、模板和示例只提供通用方法，不能证明现状。当前代码不能否定用户已授权的目标变更，只能说明变更前状态和兼容性影响。未知项标为待核实。

不得记录或输出密钥、Token、凭据、客户数据或其他敏感运行信息。
