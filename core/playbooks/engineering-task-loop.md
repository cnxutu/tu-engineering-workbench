# Playbook：Engineering Task Loop

## 用途

用于一个具体的 DEV、Bug、Refactor 或技术改造任务：先理解事实，再确认实际修改边界，在授权范围内实施，并以可复现证据验证结果。它是通用工程方法，不是 Codex Skill、状态机或长期交付记录。

## 核心循环

Stage Shortcut 位于消息的任务头部区域，可在可选 Repository Scope 之后、主要自然语言任务正文之前，以独立 token / 独立标签出现；支持大小写不敏感的 `E` / `Explore`、`P` / `Plan`、`X` / `Execute`、`V` / `Verify`。`P1`、`P2`、`P3-1` 等仍是项目标记，正文中的普通单字母不触发 Stage。

1. **Explore / E — Understand before changing**：核实发生了什么、原因、真实 change seam、可复用实现、受影响仓库/模块、替代方案、最小可行改动、风险与验证方式。默认不修改任何 tracked file；可读取、搜索调用链、运行现有测试和非持久诊断/验证。用户可只放宽明确允许的范围。
2. **Plan / P — Lock the execution boundary**：Codex Plan Mode 用于形成和收敛候选计划，确认 Goal、Scope、Files / Components、Steps、Verification 与 Stop Conditions；它本身不实施，也不是业务 Contract Authority。若产品提供原生 Plan 执行 Action，优先使用。属于 Feature Delivery 时，持久边界和结果必须回填对应 Workbench Artifact。
3. **Execute / X — Change only inside the approved boundary**：原生 Action 不可用、Plan 后重新收敛或恢复明确边界时，`X` 确认并执行当前唯一、明确、无未决且未失效的最新 Plan。否则回到 Plan；只实施已确认范围内的改动，发现边界假设不成立或范围必须扩大时停止。
4. **Verify / V — Prove the result with evidence**：默认只验证，不扩大实现 Scope 或自动修复；按任务选择测试、构建、lint、typecheck、契约/API、协议模拟、运行观测或 review。验证失败时先以新证据重新 Explore，不做无限猜测式 patch。

## 分档

| Level | 适用情形 | 路径 |
| --- | --- | --- |
| 1 — Fast Path | 修复位置与风险都明确的小改动 | Execute → Verify |
| 2 — Standard Path | 一般 Service、缓存、SQL、WS、权限条件、小重构或 Bug | Explore → Plan → Execute → Verify |
| 3 — Controlled Path | 跨服务、公开 Contract、DB Schema/迁移、并发、认证授权、设备控制、多仓库或陌生遗留代码 | Deep Explore → Plan Review → Execute → Code Review → Verify |

## Stop Conditions

停止执行并重新汇报证据、回到 Explore / Plan，若发现需要：

- 修改 DB Schema、公开 API Contract、权限或数据隔离模型；
- 修改第二个未授权 Repository；
- 推翻当前 Explore 假设或原计划无法满足成功标准；
- 明显扩大已确认 Scope。

## 与 Feature Delivery 的边界

Engineering Task Loop 管一次具体工程修改。Feature Delivery 管跨天或跨周的 Delivery ID、CAP、Phase/Gate、Task Package 与 Artifact Authority。属于 Delivery 的非平凡 DEV 任务，将重要 Plan 和实际结果回填 `03-execution-backlog.md`；Bug/Integration 的根因、修复和回归回填 `04-integration-log.md`；暂停或 Phase 变化刷新 `resume.md`。
