# 全局 `AGENTS.md` 指南

本页说明个人级 Codex 指令应放在哪里、应写什么，以及如何与仓库规则配合。它面向工程师维护，不是 Codex 的默认任务上下文；P0 的运行时规则仍以 [`../AGENTS.md`](../AGENTS.md) 为准。

## 范围与边界

全局 `AGENTS.md` 是开发者在所有仓库中的长期默认约定。它适合约束沟通方式、证据标准和低风险的协作习惯；不适合承载任何项目事实、技术栈、服务边界、构建命令或发布流程。

将团队或代码库规则放入仓库根目录或更接近目标目录的 `AGENTS.md`。可重复且有明确输入、输出、步骤或参考资料的流程应改用 Skill；需要从外部系统读取数据或执行操作时使用 MCP。入口选择见 [Codex 可配置入口地图](codex-customization-map.md)。

## 加载与优先关系

Codex 在用户目录先读取 `AGENTS.override.md`；该文件不存在时读取 `AGENTS.md`。之后从仓库根目录逐层读取到当前工作目录，越靠近当前目录的项目指令越晚合并，因此对同一事项具有更强的局部约束力。平台、系统、开发者指令和用户本次明确要求仍高于这些持久文件。

在 Windows 默认配置目录中：

| 用途 | 路径 | 适用场景 |
| --- | --- | --- |
| 长期个人默认 | `%USERPROFILE%\.codex\AGENTS.md` | 每个仓库都希望遵循的协作习惯。 |
| 临时全局覆盖 | `%USERPROFILE%\.codex\AGENTS.override.md` | 短期试验或临时调整；完成后删除或移回基础文件。 |
| 项目规则 | `<repository>\AGENTS.md` | 团队约定、代码入口、命令、验证和架构边界。 |
| 目录规则 | `<repository>\<subdir>\AGENTS.md` | 仅对特定模块生效的专属约束。 |

空文件会被忽略。若全局和项目规则很多，应保持每份精简；`config.toml` 的 `project_doc_max_bytes` 控制构建指令链时读取的最大总字节数，默认值以当前 Codex 文档为准。编辑后请新开 task（或重新运行 CLI），不要假定正在进行的 task 会重新加载指令。

## 推荐的全局内容

以下模板从 P0 [`core/rules/development.md`](../core/rules/development.md) 提取了可跨项目复用的部分，特别用于避免把用户给出的排查方向当成结论。复制时只保留确实希望在每个项目生效的条目。

```md
# Global Coding Guidance

These are personal defaults for all repositories. Follow higher-priority
platform, system, developer, user, and repository-local instructions.

## Evidence before conclusion

- Treat user-provided symptoms, suspected causes, suggested directions,
  historical notes, and examples as leads to investigate—not proof.
- Establish current facts from the smallest relevant set of source code,
  configuration, contracts, tests, logs, reproducible commands, or tool output.
- Clearly distinguish verified facts, inference, and unverified assumptions.
- If evidence contradicts the user's hypothesis, explain the contradiction
  respectfully and continue from the evidence. Do not steer the investigation
  to fit the hypothesis.
- If key evidence is unavailable and different interpretations would materially
  change the result, state the uncertainty and ask one focused question or
  propose the next smallest verification step.

## Investigation and diagnosis

- For a bug, failure, regression, or unexpected behavior: reproduce or inspect
  observable evidence first, then trace the smallest relevant call path before
  proposing a fix.
- Do not use speculative patches, weakened assertions, skipped tests, swallowed
  exceptions, or unexplained fallback behavior to hide a symptom.
- When reproduction is impossible, report the symptom, evidence collected,
  evidence gap, and a concrete next diagnostic step. Do not claim a root cause
  without support.

## Scope and verification

- Prefer the smallest change that satisfies the confirmed requirement; preserve
  existing user changes and avoid unrelated refactors.
- Before changing a public API, message contract, data semantics, permissions,
  security behavior, production configuration, or external state, explain the
  impact and obtain the necessary confirmation.
- Run verification proportional to risk when available. Never claim that a
  test, build, behavior, or root cause is confirmed without direct evidence.
- If verification cannot run, state why, what remains unverified, and the
  residual risk.
- Never expose, copy, log, or commit secrets, credentials, personal data, or
  production payloads.

## Communication

- Be concise and direct. State assumptions explicitly.
- Ask one focused clarification only when it materially affects correctness,
  safety, or scope; otherwise make a low-risk, clearly stated assumption.
```

不要把下面内容放入全局文件：

- P0–P4 的路径、产品知识、服务拓扑或本机环境信息；它们会在无关仓库中造成错误上下文。
- Java、Maven、Node 等特定项目命令；应由仓库规则或 CI 约束。
- 详细的事故处置、代码评审或发布步骤；应写成按需触发的 Skill。
- “永远同意”“不要提问”“一定修复”等绝对指令；它们会绕过风险判断并削弱证据要求。

## 验证与维护

1. 编辑 `%USERPROFILE%\.codex\AGENTS.md`，保存后新开一个 task。
2. 在一个普通仓库中要求 Codex 概述当前适用指令，确认全局和仓库规则都已加载。
3. 若某条规则在多个仓库持续造成误导，删除或缩窄它；若只在某个仓库出现重复问题，迁移到该仓库的局部 `AGENTS.md`。
4. 把可由工具稳定检查的要求转为 CI、linter、Hook 或 `.rules`，不要只依赖自然语言指令。

## 证据状态

本文的配置位置与指令发现规则依据 2026-08-03 获取的 Codex 官方手册；具体键名和表面能力可能随客户端版本演进。更新时优先核对 [Custom instructions with AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md.md) 与 [Configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference)。
