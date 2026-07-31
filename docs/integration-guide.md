# 接入指南

本指南描述仓库接入模型；它不实现解析器、知识图谱、MCP Server 或 `ai-guidance init` 命令。运行时读取规则见 [`../AGENTS.md`](../AGENTS.md)，工程师使用方式见 [工程师使用与维护指南](usage-guide.md)。

## 绑定一个仓库

1. 将 [AGENTS.md.template](../bootstrap/AGENTS.md.template) 复制到目标仓库为 `AGENTS.md`，再补充本仓库局部说明路径。
2. 复制 [repository-manifest.template.yaml](../bootstrap/repository-manifest.template.yaml)，绑定一个产品，并保证其中产品清单与入口路径一致。
3. 通过 `AI_GUIDANCE_HOME` 或显式仓库配置（例如 `.ai-guidance.yaml`）配置 P0 的知识根目录；显式配置可以选择非默认清单路径。
4. 目标仓库的 `AGENTS.md` 应先定位 P0，再读取当前仓库和目标目录的局部约束；随后按 P0 `AGENTS.md` 的会话范围、任务类型与影响范围条件读取产品知识和 Core，最后核实代码。不要默认加载所有产品文档或维护者指南。

指令优先级独立于读取顺序：平台、系统和开发者约束 > 用户最新明确要求 > 仓库局部说明 > Core 公共规则 > 产品上下文。代码、契约、配置和测试用于核实当前事实，不取代用户已授权的目标变更。

未来的 `ai-guidance init` 可以自动复制模板和检查配置，但它必须生成同样明确的绑定，不能臆造产品事实。

## 解析器约定

未来解析器应按“显式配置 → `AI_GUIDANCE_HOME` → 安装默认位置”的顺序定位知识库。它应返回绑定的仓库清单、产品清单和产品入口；遇到缺失或歧义绑定时必须报错，不能猜测。预期字段见 [仓库清单契约](../core/contracts/repository-manifest.schema.yaml)。

## 知识图谱与 MCP Context Server

未来工具可将文档、仓库、服务、契约、证据、ADR 与任务作为带类型关系的节点暴露。未来 MCP Context Server 可基于该图谱回答定向上下文问题、返回证据与过期状态，并建议下一份按需读取的文档。

当前模板和文档**没有实现**上述能力；仓库清单仍是可移植的事实来源。

## 接入验证

发布接入前运行 `python ai-guidance/scripts/validate_guidance.py --repo-root <仓库根目录>`，检查路径、Markdown 链接、产品绑定、本机映射模板和疑似敏感配置值。跨服务变更还应记录产品知识更新评估。
