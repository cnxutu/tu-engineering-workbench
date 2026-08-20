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
| 项目集人员池与角色 | P1 `project_set_user_role` | 仅允许 `INS_PM_ADMIN`、`INS_PM_STAFF`；同一用户在同一项目集中只能有一个角色。 |
| 项目集空间池 | P1 `project_set_space_pool` | 活动记录的 `space_code` 全局唯一，空间仅能进入一个项目集池。 |
| 项目成员 | P1 `project_member` | 只保存项目和用户；角色继承所属项目集，不重复保存角色。 |
| 项目空间 | P1 `project_space_binding` | 活动记录的 `space_code` 全局唯一，一个项目可选多个池内空间。 |
| 项目（集）活动名称 | P1 `project_node_identity` | 以节点类型隔离的有效名称唯一登记；P7 的 `tag_name` 不作为名称唯一性的最终裁决。 |

`c_tag_relation` 不承载项目空间池、项目空间、项目成员或项目角色，避免通用标签关系与项目业务关系形成双重真相。

项目节点只按结构识别：`parent_code = 0003` 是项目集；其直属子节点是项目。`config` 仅存储 JSON 扩展字段：项目集当前维护 `description`，项目还维护 `longitude`、`latitude`；更新时保留未知扩展字段。P7 不再使用 `config.type` 初始化项目根或识别项目节点。

P1 用 `project_node_identity` 维护项目节点的活动名称。`node_type` 为 `PROJECT_SET` 或 `PROJECT`，活动记录固定 `is_deleted = 0`，唯一键为 `(node_type, normalized_name, is_deleted)`：项目集之间、项目之间分别不能重名；项目和项目集可以同名；节点标记 `REMOVED` 后释放其名称，后续可复用。数据库唯一键是并发场景的最终裁决，服务端的活动记录查询只用于提前给出业务校验结果。`project_set_identity` 仅保存 `project_set_code` 与创建者 ID；历史项目集没有该记录时不施加创建者锁定，也不再永久占用名称。

## 面向前端的门面契约

项目管理页面只调用 P1 `ProjectManagementController` 的统一保存与详情接口；不公开成员、项目集角色、项目集空间或项目空间的原子页面操作。项目集和项目的创建、编辑各通过一次请求提交基本信息及关系编码集合。

| 页面能力 | P1 输出边界 | 前端组合责任 |
| --- | --- | --- |
| 项目集列表/详情 | 项目集卡片、基本信息、`members(userId, roleCode, projectCodes, isCreator)` 与空间编码 | P1 批量调用 P6 补齐姓名、账号和部门；前端不再自行组合人员基础资料。 |
| 项目列表 | 项目卡片及中心点 `longitude`、`latitude` | 使用坐标渲染项目地图标记。 |
| 项目编辑详情 | 所属项目集编码和名称、成员选择状态、可用/已选/禁用空间编码 | 复用 P1 空间树接口，按 `availableSpaceCodes` 过滤并用 `spaceCodes`、`disabledSpaceCodes` 标记选择和禁用状态。 |

`disabledSpaceCodes` 仅包含同项目集其他项目已绑定的空间；当前项目已选空间不会被标记为禁用，以便页面取消选择。列表和详情响应不得透传 P7 `TagDTO` 或 P1 持久化实体。

### 成员详情、创建人和保存语义

项目集详情的成员列表以 `project_set_user_role` 为主数据；`project_member` 仅用于计算普通成员的项目授权集合。项目详情同样以项目集角色池返回可选成员，`project_member` 仅用于标记该成员是否已选中当前项目。两类详情均通过 `project_set_identity.creator_user_id` 标记项目集创建人并将其置顶；身份记录存在但角色关系缺失时，详情按项目管理员补出创建人记录，避免页面缺失创建人。

`project_set_identity` 只在创建项目集时写入，编辑不改变创建人。项目集保存将 `members` 作为完整目标集合：创建人必须以项目管理员身份保留，不能被移除或降级；当前实现会拒绝未回传创建人或将其降级的请求。项目管理员有效授权为全部直属项目，因此项目集保存重建关系时会为管理员写入全部直属项目的 `project_member` 关系；项目详情的单独保存只根据 `memberUserIds` 写入当前项目成员，不会因身份表自动新增创建人关系。

项目详情 `members` 增加 `isCreator` 字段；未登记身份记录的历史项目集不虚构创建人标识，成员按角色关系记录的主键升序返回。

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
  PROJECT_NODE_IDENTITY {
    bigint id PK
    varchar node_code
    varchar node_type
    varchar normalized_name
    bigint is_deleted
  }
  PROJECT_SET_USER_ROLE ||--o{ PROJECT_MEMBER : "项目从人员池选择"
  PROJECT_SET_SPACE_POOL ||--o| PROJECT_SPACE_BINDING : "项目从空间池选择"
```

项目授权由 `project_member`、项目集有效角色和角色可执行权限共同决定；项目成员表不保存 `role_code`。

四张关系表均继承 P1 `BaseEntity`，必须完整包含 `create_user`、`create_time`、`update_user`、`update_time` 和 `is_deleted`。前两个用户审计字段保存系统操作人名称；项目集角色池和项目成员另使用 `user_id` 保存项目业务用户 ID。所有唯一键将 `is_deleted` 纳入约束，逻辑删除后允许按业务规则重新建立同一关系。

`project_node_identity` 和关系表一样继承 `BaseEntity` 的审计与逻辑删除约定。节点名称登记的删除值沿用秒级 `UNIX_TIMESTAMP(now())`；因此极端自动化场景在同一秒内对同名节点反复“创建—移除”可能与既有已删除记录冲突，此风险与仓库现有逻辑删除唯一键约定一致。

## 保存与删除约束

统一保存将请求中的成员、项目授权和空间编码作为目标集合同步到 P1 关系表；项目创建和更新还同步项目中心点配置。创建项目以请求中的 `projectSetCode` 确定所属项目集；更新项目时以路径中的既有项目确定所属项目集，请求中的 `projectSetCode` 不参与变更。项目集创建者自动成为项目管理员，管理员的授权项目始终为该项目集全部直属项目；创建者不得被移除或降级，当前登录用户若为项目管理员也不得在本次保存中移除自身。

项目集与项目创建均按“先在 P7 创建节点，再登记 P1 活动名称”执行。名称登记触发唯一键冲突时，P1 补偿删除刚创建的空 P7 节点。改名在 P1 本地事务中释放旧活动登记并写入新登记，只有成功后才更新 P7 名称；失败时事务回滚，旧名称及 P7 名称保持不变。

项目删除采用“移除”语义，不物理删除 P7 项目节点及历史任务数据。删除入口执行前必须通过项目任务状态校验；存在 `task_biz_status in (2, 6)`（执行中或暂停）任务时拒绝移除。校验通过后，P1 逻辑删除项目成员、项目空间绑定及该项目的活动名称登记，P7 节点保留原名称、坐标、描述及未知扩展字段，并在 `config.status` 写入 `REMOVED`。

项目集移除先收集直属有效项目并完成全量任务状态校验，任何子项目存在执行中或暂停任务时整体失败，不产生部分移除。校验通过后，逐项释放项目成员、项目空间绑定、项目集角色池、空间池关系，以及项目集和全部直属项目的活动名称登记，并将所有子项目及项目集节点标记为 `REMOVED`。不提供恢复或重新开启接口。

P1 本地关系删除与 P7 生命周期更新不具备分布式事务。实施顺序为：完成全部本地校验 → 更新 P7 `config.status` → 删除 P1 关系；若后续本地操作失败，使用保存的原始 `config` 回写 P7 作为补偿，并记录失败上下文。P7 `deleteTag` 不用于项目移除。

P1 不再把空间关系投影到 P7，故不需要 outbox。项目树的创建、编辑和移除是同步 P7 标签操作；移除不构成跨服务双写事务。

项目权限失效通知复用 P1 现有 `/ws/drone` 全局通道和 `sendBatchByDeviceType`，业务码为 `project_permission_changed`。通知只在项目关系变更造成 `beforeAccess - afterAccess` 非空时发送，数据数组由 `userId` 与失效项目编码增量组成；事务提交后由 `@TransactionalEventListener(AFTER_COMMIT)` 广播，发送失败不回滚已提交关系。具体快照判定、触发入口和代码证据见 [P1 项目权限失效 WebSocket 广播](../repositories/c-drone-inspection/project-permission-websocket.md)。

前端需要按项目加载菜单时，P1 使用项目关系解析 `INS_PM_ADMIN` 或 `INS_PM_STAFF`，再调用 P6 获取角色菜单；接口响应复用 P6 通用权限结构。项目角色判定、P6 角色归属前提与发布约束见 [P1 项目菜单权限（P1 + P6）](../repositories/c-drone-inspection/project-menu-permission.md)。

## 删除前置校验接口

删除页面在调用移除接口前，可通过 P1 项目管理门面查询阻断原因。两个接口均为只读操作，不修改项目、关系、任务或 Redis 缓存；项目不存在、已移除或当前用户无项目访问权限时沿用项目管理域错误语义。

### 空间任务校验

```text
POST /drone/projects/{projectCode}/delete-check/spaces
Body: { "spaceCodes": ["SPACE-001", "SPACE-002"] }
Response: { "blockedSpaceNames": ["园区 A", "园区 B"] }
```

P1 先确认空间编码属于该项目的 `project_space_binding`，再通过 P7 资源关联查询按 `CASCADE` 获取空间及子空间下的设备 ID。以 `project_id = projectCode`、`dock_id in (deviceIds)`、`task_biz_status in (2, 6)` 查询 `wayline_task`，将命中设备反向映射到输入空间并批量读取空间名称，按输入顺序去重返回。父空间下子空间设备的任务必须计入父空间阻断结果。

### 人员驾驶舱控制校验

```text
POST /drone/projects/{projectCode}/delete-check/users
Body: { "userIds": [10001, 10002] }
Response: { "blockedUserNames": ["张三", "李四"] }
```

P1 先收集项目全部有效空间绑定，再解析其下设备 ID。对每个设备读取现有 `RedisService#getAuthorityUser(deviceId)` 对应的 `flight_authority:{deviceId}` 缓存；按缓存 `LoginUser.id` 与请求 `userIds` 过滤，从 `LoginUser.info.nickname` 返回去重后的人员名称。同一人员控制多个项目设备时只返回一次，不扫描 Redis 未知 Key。

接口响应建议同时保留 `spaceCode`/`userId` 与名称，名称集合用于原型提示，编码和 ID 用于前端精确定位；若当前前端只消费名称，可暂时只暴露名称字段。

## 删除校验的责任边界与风险

- `project_id` 与项目管理 `project_code` 是同一业务标识，P1 不做转换映射。
- 任务阻断状态以 P1 `EnumTaskBizStatus.IN_PROGRESS(2)` 和 `SUSPEND(6)` 为准。
- 项目空间设备归属通过 P7 空间资源关联解析；P1 不复制设备与空间的第二份关系真相。
- `RedisService#setAuthority` 当前使用无 TTL 的键值写入，异常断连可能留下陈旧控制权。前置接口的准确语义是“缓存仍显示该人员占有驾驶舱控制权”，不等价于实时在线证明。若后续需要严格在线判定，应独立增加显式删除、TTL 或心跳续约设计。
- 空间或 Redis 查询异常不得降级为空结果，否则可能误放行项目移除；应沿既有异常链路失败并保留可排查上下文。

## 当前实现与待验证

**已实现（本地代码变更，尚未发布）**：P1 四张业务关系表、项目管理门面及页面 Req/Resp；项目集和项目统一保存，项目列表包含中心点，项目详情包含项目集名称及空间选择状态；项目和项目集移除、`REMOVED` 读取隔离、任务状态拦截及失败补偿已在 P1 本地实现。P1 另已实现 `project_node_identity` 活动名称登记、`project_set_identity` 创建者识别，以及创建、改名、移除时的名称登记与 P7 补偿。P7 保留项目根迁移与 `PROJECT_ROOT_CODE`。

**已实现（本地代码变更，尚未发布）**：删除前置空间任务校验和人员驾驶舱控制权校验接口已写入 P1，并复用空间子树设备解析、运行任务查询及驾驶舱控制权查询逻辑；项目集保存仍在服务端再次执行相同阻断校验，前端预检不能绕过提交校验。服务单元测试已覆盖前置校验结果、名称并发裁决相关补偿、名称释放和移除阻断。

**2026-08-20 已提交的 P1 项目管理补充**：项目集详情补齐人员昵称、账号和部门，项目新增/编辑新增可选空间状态接口，项目集移除新增任务阻断前置检查；项目菜单权限接口与权限失效 WebSocket 的具体契约分别见 [P1 项目菜单权限](../repositories/c-drone-inspection/project-menu-permission.md) 和 [P1 项目权限失效 WebSocket 广播](../repositories/c-drone-inspection/project-permission-websocket.md)。当天提交范围和可复现 Git 证据见 [项目管理实现归档（2026-08-20）](../tasks/archive/p1-20260820-project-management-implementation.yaml)。

**待发布 / 待确认**：

- P1 已发布依赖尚未包含 P7 的 `TagCodes.PROJECT_ROOT_CODE`，当前使用兼容性常量 `"0003"`；发布 P7 API 并升级 P1 依赖后移除该硬编码。
- 平台级接口访问权限编码尚未确认；项目域角色继承不替代系统级接口访问控制。
- 在集成环境验证 P7 项目根迁移、项目树接口权限和 P1 空间池行锁并发行为。
- 发布名称登记前，须从 P7 `0003` 树导出全部未标记 `REMOVED` 的项目集及直属项目，按节点类型扫描重名；确认无冲突后回填 `project_node_identity`，再部署 P1。迁移脚本见 P1 `docs/sql/v2.1.0_add_project_node_identity.sql`，回填步骤见 `docs/sql/v2.1.0_project_node_identity_backfill.md`。

## 证据

- P1：`b-inspection-platform-core/.../service/project/impl/ProjectManagementServiceImpl.java`、`controller/admin/project/ProjectManagementController.java`。
- P1：`b-inspection-platform-common/.../project/`（实体、页面 Req/Resp）与 `docs/sql/v2.1.0_add_project_management.sql`、`v2.1.0_add_project_node_identity.sql`。
- P7：`c-tag-api/.../constants/TagCodes.java`、`c-tag-bootstrap/.../V1.2.0__project_root.sql` 与 `V1.2.1__clear_project_type_config.sql`。
