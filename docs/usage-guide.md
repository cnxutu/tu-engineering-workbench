# 使用指南（维护者）

本页面向维护者，帮助理解 P0 的目录、会话范围和知识维护方式；Codex 执行任务时不默认读取本页。运行时规则以 [`../AGENTS.md`](../AGENTS.md) 为准。

## 1. 会话首次声明范围

会话首次任务中出现 `P0`–`P4`、`K1`、`K2` 等项目标记时，Codex 应直接识别本次范围；以下 `范围：` 只是便于人阅读的写法：

```text
范围：P0 + P1
F
g: 增加巡检任务的状态查询能力
i: P1
p: 先核实现有缓存与接口，再提出最小实现方案并完成代码和测试
v: 单元测试与接口回归
```

`P0–P4` 是当前无人机巡检系统的全量范围；`K1` 和 `K2` 分别预留给 Knowledge Hub 后端与前端。本机绝对路径维护在未提交的 `workspace.local.yaml`；首次接入时从 [`../workspace.example.yaml`](../workspace.example.yaml) 复制创建。缺少映射时不得猜测源码位置。

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

日常 Prompt 使用 [Compact Syntax](../core/prompt-compact-syntax.md)。`core/templates/` 是防遗漏的完整参考表单，不是自动渲染器，也不是默认输入。

## 4. 接入新仓库

接入或迁移仓库时阅读 [接入指南](integration-guide.md)，并同步更新 `workspace.example.yaml`、本机的 `workspace.local.yaml`、产品清单与目标仓库的局部 `AGENTS.md`。
