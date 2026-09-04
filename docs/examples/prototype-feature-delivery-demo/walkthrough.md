# 模拟案例：机器狗补光控制四阶段操作剧本

> **仅用于体验 Skill 工作方式。** 本案例模拟“驾驶舱新增机器狗前灯、后灯、自动补光控制与状态回显”。接口、字段、权限和验收结果均为演示值，不代表当前产品或代码的真实契约。

## 0. 你最初只需要提供什么

假设产品刚发布两张原型图：

- 驾驶舱右侧增加前灯、后灯、自动补光三个开关。
- 操作后页面应展示最新开关状态；设备被其他控制源占用时不可操作。

你在新会话中可以这样调用：

```text
$ai-guidance-workflows:tu-scaffolding-spring-feature-from-prototype
impact
范围：P0 + P1
原型：<原型 URL、截图或 PDF>
目标：梳理机器狗驾驶舱补光控制的前后端和上下游影响，先不要写代码
```

AI 创建本任务包并完成 Step 1。你不需要预先填写接口、模块、任务拆分或验收模板。

本示例任务包包含：

- [任务状态与导航](task.yaml)
- [Step 1：影响范围评审](01-impact-review.md)
- [Step 2：接口契约](02-api-contract.md)
- [Step 2：OpenAPI 草案](02-openapi.yaml)
- [Step 3：执行任务清单](03-execution-backlog.md)
- [Step 4：联调与提测记录](04-integration-log.md)

## 1. Step 1 如何发生

### AI 做什么

AI 阅读原型、目标仓库约束、现有 Controller/DTO、状态快照、WebSocket、IoT 下行入口和测试，生成 `01-impact-review.md`。

本例不会因为页面上有三个开关就直接设计三个接口。AI 先得到以下影响判断：

- 状态查询：现有机器狗完整快照已包含三个补光字段，判为 `reuse`。
- 实时刷新：现有状态快照 WebSocket 可承载状态变化，判为 `reuse`。
- 补光控制：需要面向机器狗的低频控制入口，判为 `new`。
- 控制占用：需要复用状态中的控制源并确认拦截规则，判为 `change`。
- P2/适配器：必须确认下行 service、command、参数和设备回读，判为 `upstream_dependency`。

AI 同时列出需要你带出去确认的 `Q-01`～`Q-05`，不会替产品或上游拍板。

### 你做什么

你拿 `01-impact-review.md` 与前端、产品和上游评审，只需要带回“最终结论 + 必要证据摘要”。例如：

```text
Q-01：三个灯允许分别控制，自动补光开启时仍允许手动覆盖。
Q-02：HTTP 200 只表示平台受理；页面等待状态快照回显，不显示“设备执行成功”。
Q-03：前端首屏和 WS 重连后都重新请求状态快照。
Q-04：外部控制源占用时返回业务错误，不允许下发。
Q-05：上游确认复用 inspection_device_control，命令值为模拟值 SET_FILL_LIGHT。
```

然后调用：

```text
$ai-guidance-workflows:tu-scaffolding-spring-feature-from-prototype
contract
任务：robot-dog-fill-light-demo
确认结果：见上面的 Q-01～Q-05；请更新任务包并形成接口契约，不修改业务代码
```

AI 校验这些答案是否足以关闭 `G1_scope_confirmed`。缺失某一项时，只阻塞依赖它的契约，不会要求你重新描述整个需求。

## 2. Step 2 如何发生

### AI 做什么

AI 生成 `02-api-contract.md` 和可选的 `02-openapi.yaml`。本例最终形成：

- 不新增补光状态查询接口，复用完整快照 REST。
- 不新增补光 WebSocket，复用完整快照推送。
- 新增一个补光控制命令接口，而不是三个按钮三个接口。
- HTTP 响应表示 `ACCEPTED`，设备最终状态以 REST/WS 回读为准。
- 明确控制源占用、设备不存在、参数非法等错误语义。

前端可以用 Markdown 评审完整交互和实时语义，也可以把 OpenAPI 草案导入 Apifox 查看 REST 模型。

### 你做什么

你将契约交给前端和相关后端确认。若路径或字段调整，只需给出差异：

```text
接口评审结论：
1. path 改为 /drone/robot-dog/{deviceId}/fill-light/action（单数）。
2. requestId 由前端生成并必传。
3. 接受 ACCEPTED 语义和快照回读方式。
4. 其余字段通过。
```

继续调用：

```text
$ai-guidance-workflows:tu-scaffolding-spring-feature-from-prototype
contract
任务：robot-dog-fill-light-demo
按本轮接口评审结论修订并检查 G2；仍然不写业务代码
```

当 `G2_contract_confirmed=verified` 后，如果你确实想先让 IDEA/Apifox 从 Java 代码识别接口，可以另行授权：

```text
$ai-guidance-workflows:tu-scaffolding-spring-feature-from-prototype
controller-contract
任务：robot-dog-fill-light-demo
范围：P1
按已确认契约生成 Controller/DTO 契约骨架；先核实仓库是否有不会暴露伪成功接口的既有模式
```

若仓库没有安全的契约骨架模式，Skill 应拒绝凭空增加平行抽象，保留 OpenAPI 为本阶段产物，并建议把 Controller/DTO 创建放进第一个 `DEV` 任务。

## 3. Step 3 如何发生

### AI 做什么

你要求生成任务清单：

```text
$ai-guidance-workflows:tu-scaffolding-spring-feature-from-prototype
plan
任务：robot-dog-fill-light-demo
根据已确认的影响范围和接口契约，生成可逐项执行的任务清单
```

AI 输出 `03-execution-backlog.md`。本例拆成：

- `EXT-01`：取得上游脱敏下行和状态回读样本。
- `DEV-01`：实现 Controller、DTO、权限和参数校验。
- `DEV-02`：实现机器狗补光命令业务服务及 IoT 调用。
- `DEV-03`：补齐状态回读与接口契约验证。
- `INT-01`：前端 REST/WS 联调。
- `INT-02`：P1→P2→适配器→设备闭环联调。

每项都带上下文入口、前置、非目标、执行步骤、预期、验收和证据要求。`EXT-01` 未完成时，`DEV-01` 可以 ready，但依赖真实上游参数的 `DEV-02` 保持 blocked。

### 你做什么

你可以逐项执行：

```text
$ai-guidance-workflows:tu-scaffolding-spring-feature-from-prototype
execute DEV-01
任务：robot-dog-fill-light-demo
范围：P1
```

也可以按功能块执行：

```text
$ai-guidance-workflows:tu-scaffolding-spring-feature-from-prototype
execute block=backend-control
任务：robot-dog-fill-light-demo
范围：P1
只执行状态为 ready 的任务；blocked 项不要猜测实现
```

AI 每完成一项就回填同一个 backlog，包括实际文件、测试命令、测试结果、剩余风险和下一项。你无需另建“今日计划”复制旧内容。

当外部样本拿到后，你这样解锁任务：

```text
$ai-guidance-workflows:tu-scaffolding-spring-feature-from-prototype
plan
任务：robot-dog-fill-light-demo
EXT-01 已完成，脱敏样本位置：<受控文件或评审记录>
请核验样本并更新受影响任务的 ready/blocked 状态
```

## 4. Step 4 如何发生

### AI 做什么

开始联调时调用：

```text
$ai-guidance-workflows:tu-scaffolding-spring-feature-from-prototype
integrate
任务：robot-dog-fill-light-demo
本轮场景：前端首屏、前灯开启、外部占用、WS 断线重连
证据：<脱敏日志、请求响应、截图或测试环境说明>
```

AI 按 `04-integration-log.md` 记录期望和实际，并把问题回流到正确阶段。例如：

- HTTP 返回 `ACCEPTED`，随后 WS 显示前灯打开：闭环通过。
- HTTP 成功但设备状态未变化：不能判前端通过，也不能把同步返回改写成“执行成功”；建立 `INT` 排查项。
- 前端认为 `requestId` 可选、后端认为必填：这是契约漂移，回到 Step 2。
- 原型新增“全部关闭”按钮：这是范围变化，回到 Step 1。
- 服务抛出空指针：这是实现缺陷，重开或新增 `DEV` 任务；若属于复杂 Spring 事故，可转诊断 Skill。

### 你做什么

你负责提供可访问的联调环境、协作方时间和脱敏证据，确认延期或非目标项，最后要求生成提测摘要：

```text
$ai-guidance-workflows:tu-scaffolding-spring-feature-from-prototype
status
任务：robot-dog-fill-light-demo
请判断是否达到 G4，并输出提测范围、已验证场景、未完成项、风险、发布顺序和回滚边界
```

AI 只能根据已有证据关闭 `G4_test_ready`。缺少实机回读时，可以声明“代码与模拟链路通过”，不能声称设备闭环已完成。

## 5. 四阶段中你和 AI 的职责

| 阶段 | AI 负责 | 你负责 | 你推动下一阶段的最小输入 |
| --- | --- | --- | --- |
| Step 1 影响范围 | 读原型、代码和契约；分类复用/改造/新增；列问题和责任边界。 | 组织产品、前端、上下游确认关键问题。 | 对问题逐项给最终结论、负责人或明确延期。 |
| Step 2 接口契约 | 形成 REST/WS/消息契约、示例、错误和成功语义；记录差异。 | 组织接口评审并确认公开契约。 | 给出通过项和变更项；授权时才生成代码骨架。 |
| Step 3 任务实施 | 生成 EXT/DEV/INT 清单；只执行 ready 项；完成代码验证和结果回填。 | 提供外部输入，选择单任务或功能块，处理代码评审决策。 | 指定任务 ID/功能块和允许修改范围。 |
| Step 4 联调提测 | 执行场景矩阵、定位问题归属、回流前置阶段、汇总提测证据。 | 协调环境与人员，提供脱敏运行证据，决定延期/上线。 | 指定联调场景、环境和证据位置。 |

## 6. 换会话后如何继续

任务状态写在 `task.yaml`，所以不需要复制历史对话：

```text
$ai-guidance-workflows:tu-scaffolding-spring-feature-from-prototype
status
任务包：<P0 中的任务包路径>
告诉我当前阶段、阻塞、下一项，以及我需要对外确认什么
```

AI 应先读 `task.yaml` 指向的权威产物，再只读取当前任务需要的代码和证据。它不应重新从原型开始生成另一套编号或接口文档。

## 7. 最终留下什么

功能结束时，任务包本身就是完整交付记录：

- `01-impact-review.md`：为什么要改、影响什么、哪些不做。
- `02-api-contract.md` / `02-openapi.yaml`：前后端最终按什么契约工作。
- `03-execution-backlog.md`：谁做了什么、代码和自动验证结果是什么。
- `04-integration-log.md`：哪些真实场景已通过、哪些延期、是否达到提测门禁。
- `task.yaml`：当前状态、门禁、证据和归档导航。

这组产物既能让 AI 断点续跑，也能让你在评审、联调和提测时直接拿同一份事实沟通。
