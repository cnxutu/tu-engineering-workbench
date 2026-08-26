# P7：标签资源管理关键入口地图

> **证据等级：代码与 API 契约核对已确认（2026-08-26）。** 本页只覆盖 `c-tag` 的标签树、资源弱关联和标签权限能力。它不拥有巡检设备、项目或空间资源本体；实际资源合法性和生命周期仍由接入业务服务核实。

## 范围

`c-tag` 维护标签树、外部资源与标签之间的弱关联、标签维度的数据权限，并在关联关系真实变化后发送消息。接入服务使用 `resourceType + resourceCode` 关联自己的资源；资源名称等展示字段只是关系快照，资源详情和在线状态必须回源到资源所有者。

## 按问题类型读取

| 问题 | 首选入口 | 阅读顺序 |
| --- | --- | --- |
| 标签节点、父子结构、树加载或搜索 | `c-tag-api/.../TagApi.java`、`TagTreeApi.java`；`c-tag-core/.../TagServiceImpl.java`、`TagTreeServiceImpl.java` | RPC/HTTP 契约 → 服务实现 → 标签编码/树查询。 |
| 资源绑定、解绑、多标签交集或标签下资源列表 | `TagResourceApi.java`、`TagResourceApiImpl.java`、`TagResourceServiceImpl.java` | 请求中的 `resourceType + resourceCode` → 关联关系写入/查询 → 调用方回源资源详情。 |
| 标签权限或列表过滤 | `TagPermissionApi.java`、`TagPermissionApiImpl.java`、`TagPermissionServiceImpl.java` | 授权主体与标签树边界 → 权限上下文 → 单点/列表查询语义。 |
| 关联变更事件未生效 | `mq/TagRelationChangePublisher.java`、`TagRelationChangeMessage.java` | 真实关联变化 → 事务后发布 → RocketMQ 发送结果 → 消费方投影/缓存。 |
| 空间域接入或巡检项目树边界 | `c-space` 模块及调用方的 Tag API 使用点 | 先确认标签树/资源关联，再回源 P1/P7 资源主数据边界。 |

## 已确认的边界与约束

- `TagResourceApi` 支持单个/批量绑定、解绑、按标签查询、按多标签 AND 查询以及轻量的资源编码—标签编码映射查询。
- 关联关系变更按 `resourceType:resourceCode` 构造顺序键，发布 BOUND、UNBOUND 或 UPDATED 事件；发送失败记录错误但不会回滚已提交的关系变更。
- 标签节点、关联关系和权限配置必须通过 API/RPC 维护；直接写库会绕过编码预占、事件或权限一致性机制。

## 代码证据

- API 契约：`c-tag-api/.../api/TagApi.java`、`TagTreeApi.java`、`TagResourceApi.java`、`TagPermissionApi.java`。
- 核心实现：`c-tag-core/.../api/*ApiImpl.java`、`service/impl/TagServiceImpl.java`、`TagTreeServiceImpl.java`、`TagResourceServiceImpl.java`、`TagPermissionServiceImpl.java`。
- 事件发布：`c-tag-core/.../mq/TagRelationChangePublisher.java`。

## 待核实项

- 巡检项目、空间和设备分别使用的 `resourceType`、标签树根及调用来源。
- P1 对关联变更事件的消费组、投影/缓存更新及异常重试策略。
