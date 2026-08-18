# 工程师使用与维护指南

本页面面向使用或维护本仓库的工程师，帮助理解 P0 的目录、会话范围和知识维护方式；Codex 执行任务时不默认读取本页。运行时规则以 [`../AGENTS.md`](../AGENTS.md) 为准。

需要理解 AI 运行时加载、工程师使用与维护路径、项目骨架与扩展入口时，阅读[项目导航与维护地图](project-guide.md)。

## 1. 会话首次声明范围

会话首次任务中出现 `P0`–`P4`、`K1`、`K2`、`K5`、`L1`、`A1` 等项目标记时，Codex 应直接识别本次范围；以下 `范围：` 只是便于工程师阅读的写法：

```text
范围：P0 + P1
F
g: 增加巡检任务的状态查询能力
i: P1
p: 先核实现有缓存与接口，再提出最小实现方案并完成代码和测试
v: 单元测试与接口回归
```

`P0–P4` 是当前无人机巡检系统的全量范围；`K1` 和 `K2` 分别预留给 Knowledge Hub 后端与前端；`K5` 是语言学习与快速 Demo 运行项目 `tu-language-lab`；`L1` 是个人软考高级系统架构师学习沉淀汇总项目 `tu-arch-learning`；`A1` 是个人 AI 功能集合工程 `tu-ai-lab`。本机绝对路径维护在未提交的 `workspace.local.yaml`；首次接入时从 [`../workspace.example.yaml`](../workspace.example.yaml) 复制创建。缺少映射时不得猜测源码位置。

项目标记不依赖固定分隔符，因此 `P1 + P2`、`P1,P2`、`P1，P2`、`P1、P2`、`P1 P2`，或正文中分别出现 P1、P2，均表示本次涉及两者；`-` 或 `–` 表示连续范围，例如 `P0–P4`。`范围：` 是可选前缀。

## 2. 何时维护 P0 知识

仅当任务改变了长期可复用的关键入口、跨服务链路、服务/数据边界、公开契约或持久架构决策时，才更新 `products/`。修改时阅读：

- [编写指南](authoring-guide.md)：收录标准和文档结构。
- [治理规范](governance.md)：证据、过期性、敏感信息、ADR 与任务归档。

单个业务代码改动、临时排查过程、完整配置清单和未经证实的运行猜测不应进入产品知识。

## 3. 目录导航

- `core/`：通用角色、规则、工作流和参考模板。
- `products/`：产品架构、流程、仓库入口、缓存与任务历史。
- `workspace.example.yaml`：可提交的本机路径地图模板；实际路径写入被忽略的 `workspace.local.yaml`。
- `bootstrap/`：其他仓库接入时复制的模板。
- `docs/`：面向维护者的使用、接入、编写与治理资料。

个人级 Codex 指令、团队级工程规则与其他配置入口的边界，分别见 [全局 `AGENTS.md` 指南](global-agents-guidance.md) 和 [Codex 可配置入口地图](codex-customization-map.md)。这两页用于工程师理解和维护，不应复制进 P0 运行时 `AGENTS.md`。

日常 Prompt 使用 [Compact Syntax](../core/prompt-compact-syntax.md)。`core/templates/` 是防遗漏的完整参考表单，不是自动渲染器，也不是默认输入。

## 4. 接入新仓库

接入或迁移仓库时阅读 [接入指南](integration-guide.md)，并同步更新 `workspace.example.yaml`、本机的 `workspace.local.yaml`、产品清单与目标仓库的局部 `AGENTS.md`。

## 5. 使用团队 Workflow Plugin

`ai-guidance-workflows` 是可选的团队 Codex Plugin，为高价值且重复的场景提供原生 Skill；它补充 `AGENTS.md` 和 Core 规则，不替代任务类型、局部约束或代码核实。

团队自定义 Skill 统一以 `tu-` 开头，便于在列表中筛选和在任务中显式调用；该前缀不属于 Compact Syntax，因此不改变 `B`、`X` 等任务类型的含义。

首次使用时，在 P0 仓库根目录执行：

```powershell
codex plugin marketplace add .\ai-guidance
codex plugin add ai-guidance-workflows@tu-devkit
```

安装或更新 Plugin 后开启一个新任务，使 Codex 重新发现 Skill。Plugin 当前提供：

| Skill | 适用场景 |
| --- | --- |
| `tu-diagnosing-spring-backend-incidents` | Spring Boot 异常、消息处理失败、数据不一致、性能退化或未知根因的线上事故。 |
| `tu-loading-device-inspection-cross-service-context` | P1–P4 的 API、消息、数据归属、协议、MQTT、OSD、DJI 或上/下行链路变更前的全局理解。 |
| `tu-scaffolding-spring-feature-from-prototype` | 从产品原型图提取接口与数据需求，先确认契约，再按目标仓库约定生成 Spring Boot 分层代码、迁移 SQL 和 Swagger/OpenAPI 文档。 |

### 与 Compact Syntax 的关系

`F/B/R/A/X/C/D/P` 仍是任务类型；Skill 是可选的专用工作流，不新增 `S-B` 之类的任务类型，也不改变 `B` 的缺陷修复语义。最可靠的显式调用方式是在任务首行写 Skill 名称，下一行仍写原任务类型：

```text
$ai-guidance-workflows:tu-diagnosing-spring-backend-incidents
B
g: P2 的设备状态消息偶发丢失
i: P2
v: 输出证据链、根因或下一步取证计划
```

```text
$ai-guidance-workflows:tu-loading-device-inspection-cross-service-context
X
g: 支持新设备的状态上报和控制指令
i: P1、P2、P3、P4
p: 先核实上下行链路、契约与发布依赖，再给出方案
```

```text
$ai-guidance-workflows:tu-scaffolding-spring-feature-from-prototype
原型：https://prototype.example/device-group
目标：实现设备分组管理后端
```

也可以只调用 Skill 并附上原型图。目标项目、分层与数据约定、设计预览、确认门禁、实现范围和验证方式由 Skill 从当前工程上下文与代码中核实；只有无法可靠推断且会改变接口或数据语义的事项才需要补充确认。

安装后，Codex 也可根据任务描述和运行时约束自动选择 Skill；显式写 `$插件名:Skill名` 更确定。仅出现多个项目标记但未说明服务交互时，不自动加载 P1–P4 的全局上下文。
