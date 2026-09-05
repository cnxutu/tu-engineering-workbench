# 工程师使用与维护指南

本页面面向使用或维护本仓库的工程师，帮助理解 P0 的目录、会话范围和知识维护方式；Codex 执行任务时不默认读取本页。运行时规则以 [`../../AGENTS.md`](../../AGENTS.md) 为准。

需要理解 AI 运行时加载、工程师使用与维护路径、项目骨架与扩展入口时，阅读[项目导航与维护地图](project-guide.md)。

## 1. 会话首次声明范围

会话首次任务中出现 `P0`、`P0-1`、`P1`–`P7`、`P3-1`、`P4-1`、`P10`、`K1`、`K2`、`K5`、`L1`、`A1`、`S1` 等项目标记时，Codex 应直接识别本次范围；以下 `范围：` 只是便于工程师阅读的写法：

```text
范围：P0 + P1
Explore

增加巡检任务的状态查询能力。
先核实现有缓存与接口；本轮不修改代码。
```

项目标记、实际仓库名与产品绑定以 [仓库注册表](../../core/registry/repositories.yaml) 为准；仓库在产品中的职责由产品 repository manifest 维护。`P0–P7` 只展开连续主序列；P0-1、P3-1、P4-1 是独立标记。`workspace.local.yaml` 只维护本机绝对路径；首次接入时从 [`../../workspace.example.yaml`](../../workspace.example.yaml) 复制创建。缺少映射时不得猜测源码位置。除 P0 文档外，项目文件不得把这些标记当作项目或服务名称，应改用实际工程名；优先级、阶段、变量名和协议/型号值等非项目语义不受此限制。

项目标记不依赖固定分隔符，因此 `P1 + P2`、`P1,P2`、`P1，P2`、`P1、P2`、`P1 P2`，或正文中分别出现 P1、P2，均表示本次涉及两者；`-` 或 `–` 表示连续范围，例如 `P0–P7`，但不拆分 P0-1、P3-1、P4-1。`范围：` 是可选前缀。

## 2. 何时维护 P0 知识

仅当任务改变了长期可复用的关键入口、跨服务链路、服务/数据边界、公开契约或持久架构决策时，才更新 `products/`。修改时阅读：

- [编写指南](../governance/authoring-guide.md)：收录标准和文档结构。
- [治理规范](../governance/governance.md)：证据、过期性、敏感信息、ADR 与 Delivery State 归档。

单个业务代码改动、临时排查过程、完整配置清单和未经证实的运行猜测不应进入产品知识。

## 3. 目录导航

- `core/`：通用角色、规则、Playbook、契约和注册表。
- `products/`：已验证的产品架构、流程、仓库入口与长期决策。
- `work/`：当前与归档的 Delivery State；不作为产品知识默认入口。
- `workspace.example.yaml`：可提交的本机路径映射模板；实际路径写入被忽略的 `workspace.local.yaml`。
- `bootstrap/`：其他仓库接入时复制的模板。
- `docs/`：面向维护者的使用、接入、编写与治理资料。

个人级 Codex 指令、团队级工程规则与其他配置入口的边界，分别见 [全局 `AGENTS.md` 指南](../codex/global-agents-guidance.md) 和 [Codex 可配置入口地图](../codex/codex-customization-map.md)。这两页用于工程师理解和维护，不应复制进 P0 根 `AGENTS.md`。

日常任务默认使用自然语言；对非平凡工程任务，可选用 `Explore`、`Plan`、`Execute`、`Verify` 表达本轮阶段意图。最短用法、默认边界和受控模板见 [Engineering Task Loop](../workflows/engineering-task-loop/README.md)。

## 4. 接入新仓库

接入或迁移仓库时阅读 [接入指南](integration-guide.md)，并同步更新 `workspace.example.yaml`、本机的 `workspace.local.yaml`、产品清单与目标仓库的局部 `AGENTS.md`。

## 5. 使用团队 Skill Plugin

`ai-guidance-workflows` 是可选的团队 Codex Plugin，为高价值且重复的场景提供原生 Skill；它补充 `AGENTS.md` 和 Core 规则，不替代自然语言任务语义、用户边界、局部约束或代码核实。

团队自定义 Skill 统一以 `tu-` 开头，便于在列表中筛选和在任务中显式调用；Skill 是专用能力，不替代自然语言任务语义或可选 Stage Shortcut。

Skill 采用少量优先的策略：成熟通用能力优先 **Adopt**；需要叠加本仓工程语义时 **Adapt**；只有 Workbench 独有、且已被真实交付反复验证的模式才 **Own**。不要把每个技术主题或一次性流程变成新 Skill。

首次使用时，在 P0 仓库根目录执行：

```powershell
codex plugin marketplace add .
codex plugin add ai-guidance-workflows@tu-engineering-workbench
```

安装或更新 Plugin 后开启一个新任务，使 Codex 重新发现 Skill。Plugin 当前提供：

| Skill | 适用场景 |
| --- | --- |
| `tu-diagnosing-spring-backend-incidents` | Spring Boot 异常、消息处理失败、数据不一致、性能退化或未知根因的线上事故。 |
| `tu-deliver-feature` | 显式创建、恢复、查询或稳定一个 Delivery ID；从原型、契约、DEV 任务或 Bug 统一路由四阶段交付。 |
| `tu-analyzing-feature-impact` | 在 API 设计或实现前，将原型、PRD、截图或 PDF 归纳为有代码/契约证据的 Impact Review。 |
| `tu-loading-device-inspection-cross-service-context` | P1–P4、P3-1 的 API、消息、数据归属、协议、MQTT、OSD、DJI 或视频流媒体链路变更前的全局理解。 |
| `tu-scaffolding-spring-feature-from-prototype` | 兼容旧的显式原型调用；它路由到 `tu-deliver-feature` 与 Phase 1 Impact，不再维护独立生命周期。 |

### 与 Stage Shortcuts 的关系

Skill 是可选的专用工作流。最可靠的显式调用方式是在任务首行写 Skill 名称，随后用自然语言说明任务；需要强调本轮阶段时，再写可选 Stage Shortcut：

```text
$ai-guidance-workflows:tu-diagnosing-spring-backend-incidents
Explore

P2 的设备状态消息偶发丢失。
输出证据链、根因或下一步取证计划；不要修改代码。
```

```text
$ai-guidance-workflows:tu-loading-device-inspection-cross-service-context
Explore

P1、P2、P3、P4 需要支持新设备的状态上报和控制指令。
先核实上下行链路、契约与发布依赖，再给出方案。
```

```text
$ai-guidance-workflows:tu-deliver-feature
原型：https://prototype.example/device-group
目标：开始设备分组管理 Delivery
```

继续、查询和 Bug 都只需要 canonical Delivery ID：`继续 DF-20260904-01`、`DF-20260904-01 当前进展` 或 `DF-20260904-01 设备状态偶尔不刷新`。若匹配的 Delivery 已归档且反馈属于它，Skill 将整包重新打开到 `active/` 后再分类处理。Skill 先读取 `task.yaml`、`resume.md` 和当前阶段权威产物，再加载最小必要代码上下文。也可以只调用 Impact Skill 并附上原型图；目标项目、分层与数据约定、确认门禁、实现范围和验证方式仍须从当前工程上下文与代码核实。

安装后，Codex 也可根据任务描述和运行时约束自动选择 Skill；显式写 `$插件名:Skill名` 更确定。仅出现多个项目标记但未说明服务交互时，不自动加载 P1–P4、P3-1 的全局上下文。
