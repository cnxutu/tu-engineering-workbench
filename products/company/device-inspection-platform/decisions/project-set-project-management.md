# 项目集与项目管理设计（P1 + P7）

## 决策与边界

P7 仅保存项目树；P1 是人员池、空间池、项目成员和项目空间绑定的唯一业务真相。项目树只能通过 P1 项目门面维护，前端不直调 P7 通用标签接口。

```mermaid
flowchart LR
  P1[P1 项目管理门面] -->|创建 / 编辑 / 删除项目节点| P7[P7 c_tag 项目树]
  P1 --> DB[(P1 项目关系表)]
  P7 --> PS[0003 项目根 → 项目集 → 项目]
```

| 范围 | 归属 | 约束 |
| --- | --- | --- |
| 项目树节点 | P7 `c_tag` | `0003` 项目根 → 直属项目集 → 直属项目；根节点只初始化，不允许业务编辑或删除，节点类型不写入 `config`。 |
| 项目集人员池与角色 | P1 `project_set_user_role` | 仅允许 `INS_PM_ADMIN`、`INS_PM_STAFF`；同一用户可拥有两个角色。 |
| 项目集空间池 | P1 `project_set_space_pool` | 活动记录的 `space_code` 全局唯一，空间仅能进入一个项目集池。 |
| 项目成员 | P1 `project_member` | 只保存项目和用户；角色继承所属项目集，不重复保存角色。 |
| 项目空间 | P1 `project_space_binding` | 活动记录的 `space_code` 全局唯一，一个项目可选多个池内空间。 |

`c_tag_relation` 不承载项目空间池、项目空间、项目成员或项目角色，避免通用标签关系与项目业务关系形成双重真相。

项目节点只按结构识别：`parent_code = 0003` 是项目集；其直属子节点是项目。`config` 仅存储 JSON 扩展字段：项目集当前维护 `description`，项目还维护 `longitude`、`latitude`；更新时保留未知扩展字段。P7 不再使用 `config.type` 初始化项目根或识别项目节点。

## 面向前端的门面契约

项目管理页面只调用 P1 `ProjectManagementController` 的统一保存与详情接口；不公开成员、项目集角色、项目集空间或项目空间的原子页面操作。项目集和项目的创建、编辑各通过一次请求提交基本信息及关系编码集合。

| 页面能力 | P1 输出边界 | 前端组合责任 |
| --- | --- | --- |
| 项目集列表/详情 | 项目集卡片、基本信息、`members(userId, roleCode, projectCodes)` 与空间编码 | 按 `userId` 调用 P6 补齐姓名、账号和部门。 |
| 项目列表 | 项目卡片及中心点 `longitude`、`latitude` | 使用坐标渲染项目地图标记。 |
| 项目编辑详情 | 所属项目集编码和名称、成员选择状态、可用/已选/禁用空间编码 | 复用 P1 空间树接口，按 `availableSpaceCodes` 过滤并用 `spaceCodes`、`disabledSpaceCodes` 标记选择和禁用状态。 |

`disabledSpaceCodes` 仅包含同项目集其他项目已绑定的空间；当前项目已选空间不会被标记为禁用，以便页面取消选择。列表和详情响应不得透传 P7 `TagDTO` 或 P1 持久化实体。

## 表设计与关键关系

```mermaid
erDiagram
  PROJECT_SET_USER_ROLE {
    bigint id PK
    varchar project_set_code
    bigint user_id
    varchar role_code
  }
  PROJECT_SET_SPACE_POOL {
    bigint id PK
    varchar project_set_code
    varchar space_code UK
  }
  PROJECT_MEMBER {
    bigint id PK
    varchar project_code
    bigint user_id
  }
  PROJECT_SPACE_BINDING {
    bigint id PK
    varchar project_code
    varchar space_code UK
  }
  PROJECT_SET_USER_ROLE ||--o{ PROJECT_MEMBER : "项目从人员池选择"
  PROJECT_SET_SPACE_POOL ||--o| PROJECT_SPACE_BINDING : "项目从空间池选择"
```

项目授权由 `project_member`、项目集有效角色和角色可执行权限共同决定；项目成员表不保存 `role_code`。

四张关系表均继承 P1 `BaseEntity`，必须完整包含 `create_user`、`create_time`、`update_user`、`update_time` 和 `is_deleted`。前两个用户审计字段保存系统操作人名称；项目集角色池和项目成员另使用 `user_id` 保存项目业务用户 ID。所有唯一键将 `is_deleted` 纳入约束，逻辑删除后允许按业务规则重新建立同一关系。

## 保存与删除约束

统一保存将请求中的成员、项目授权和空间编码作为目标集合同步到 P1 关系表；项目创建和更新还同步项目中心点配置。创建项目以请求中的 `projectSetCode` 确定所属项目集；更新项目时以路径中的既有项目确定所属项目集，请求中的 `projectSetCode` 不参与变更。

前端仅可删除空项目或空项目集：项目存在成员或空间绑定时不可删除；项目集存在直属项目、角色或空间池关系时不可删除。不提供项目集/项目的级联删除、关闭/重新开启或关系级联解除接口。

P1 不再把空间关系投影到 P7，故不需要 outbox。项目树的创建、编辑、删除是同步 P7 标签操作；删除仅适用于 P1 关系已清空的节点，不构成跨服务双写。

## 当前实现与待验证

**已实现（本地代码变更，尚未发布）**：P1 四张业务关系表、项目管理门面及页面 Req/Resp；项目集和项目统一保存，项目列表包含中心点，项目详情包含项目集名称及空间选择状态。P7 保留项目根迁移与 `PROJECT_ROOT_CODE`。

**待发布 / 待确认**：

- P1 已发布依赖尚未包含 P7 的 `TagCodes.PROJECT_ROOT_CODE`，当前使用兼容性常量 `"0003"`；发布 P7 API 并升级 P1 依赖后移除该硬编码。
- 平台级接口访问权限编码尚未确认；项目域角色继承不替代系统级接口访问控制。
- 在集成环境验证 P7 项目根迁移、项目树接口权限和 P1 空间池行锁并发行为。

## 证据

- P1：`b-inspection-platform-core/.../service/project/impl/ProjectManagementServiceImpl.java`、`controller/admin/project/ProjectManagementController.java`。
- P1：`b-inspection-platform-common/.../project/`（实体、页面 Req/Resp）与 `docs/sql/v2.1.0_add_project_management.sql`。
- P7：`c-tag-api/.../constants/TagCodes.java`、`c-tag-bootstrap/.../V1.2.0__project_root.sql` 与 `V1.2.1__clear_project_type_config.sql`。
