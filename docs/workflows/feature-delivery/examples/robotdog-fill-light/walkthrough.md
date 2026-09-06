# 模拟案例：机器狗补光控制四阶段操作剧本

> **仅用于体验 V1 工作方式。** 本案例的接口、字段、权限和验证结果均为演示值，不代表当前产品或代码的真实契约。

假设需求是“驾驶舱增加前灯、后灯、自动补光控制，并在操作后回显最新状态”。新功能只需从 Delivery 入口开始，并附上自然语言需求或原型：

```text
$ai-guidance-workflows:tu-deliver-feature
原型：<原型 URL、截图或 PDF>
目标：梳理机器狗补光控制的前后端与上下游影响，先不要写代码。
```

Skill 创建一个 canonical Delivery ID，例如 `DF-20260903-99`，并建立当前阶段所需的 Task Package。可读目录 slug 不是身份，也不替代 Delivery ID。

本示例包保留以下演练产物：

- [任务状态与导航](task.yaml)
- [影响范围评审](01-impact-review.md)
- [接口契约](02-api-contract.md)
- [OpenAPI 草案](02-openapi.yaml)
- [执行任务清单](03-execution-backlog.md)
- [联调与提测记录](04-integration-log.md)
- [恢复缓存](resume.md)

## 继续、查询与 Bug

后续会话仍用同一个 Delivery ID：

```text
继续 DF-20260903-99
DF-20260903-99 当前进展
DF-20260903-99 设备状态偶尔不刷新
```

Skill 先读取 `task.yaml`、`resume.md` 和当前阶段的权威 Artifact。Bug 属于已归档 Delivery 时，先重开整个包，再将 `BUG-xx`、分类、证据和回归结果回填到相应 Artifact；不新建丢失上下文的 Delivery。

## 对具体 DEV 或 Bug 使用 Engineering Task Loop

对一个明确的 DEV/BUG 修改，在已知仓库范围后使用 Engineering Task Loop。例如：

```text
P1
E
DF-20260903-99 DEV-01：核对补光控制接口的现有入口、权限和状态回读链路。
```

阶段可用 `E / P / X / V` 或完整英文，大小写不敏感；Repository Scope 位于阶段前。`E` 用于取证，`P` 用于收敛候选计划。Plan Mode 帮助形成计划，但只有用户确认的 Plan 才是本轮 Execution Boundary。

确认计划后，优先使用 Codex 原生 **Execute Plan / Implement**。只有原生 UI 不可用或计划发生变化时才显式使用 `X`；完成后用 `V` 执行约定验证。实施结果、证据和剩余风险回填 `03-execution-backlog.md`，Bug/联调结论回填 `04-integration-log.md`，暂停或阶段变化时刷新 `resume.md`。

## 结束时保留什么

`task.yaml` 只保存生命周期状态、Gate 和 Artifact 导航；批准的 Contract、阶段 Artifact 与可复现验证证据才是 Delivery Authority。单个 DEV / BUG 的 Verify 只回填父 Artifact，不关闭整个 Delivery。整个 Delivery 在 G4 / acceptance 或明确 Closing condition 后，才可完成、阻塞或被替代地关闭：先将仍有效的已验证事实 Integrate 至 Product Truth，再创建 Closed Index；完整包在外部 archive 未配置时保留为 local cold history，并补齐最终状态和 `archived_at`。Archive 表示 lifecycle closed，不表示一定成功。

本案例是静态演练，不证明真实设备、接口或环境已经验证。
