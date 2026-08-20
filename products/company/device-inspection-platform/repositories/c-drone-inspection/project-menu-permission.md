# P1 项目菜单权限（P1 + P6）

> 证据等级：P1 当前本地实现、P6 `PermissionApi` 当前源码和 P1 单元测试已核对（2026-08-20）。本文记录项目上下文菜单权限链路；菜单角色配置与 P6 的用户角色归属仍须以运行环境数据核实。

## 范围与边界

P1 向前端提供当前登录用户在指定项目下的菜单权限，响应复用 P6 `UserPermissionRespDTO`，不新增项目专用响应模型。P1 拥有用户—项目—项目角色关系；P6 拥有角色—菜单、按钮权限关联。

该接口只提供前端菜单与权限标识，不替代业务接口的服务端鉴权。超级管理员和全局自定义角色由前端既有全局路由逻辑处理，不应调用此项目角色接口。

## 前端契约与调用链

```text
GET /drone/projects/{projectCode}/permission-info
  → P1 从登录态取得 userId，校验项目有效及访问权
  → P1 解析项目角色
  → P6 PermissionApi#getUserPermissionInfo(userId, roleCode, false)
  → P1 将项目角色编码追加至 UserPermissionRespDTO.roles
```

前端按既有 `roles`、`permissions`、`menus` 通用字段消费。切换项目时必须替换项目层菜单状态，不能把不同项目的菜单或项目角色编码累加。

## 项目角色解析

| 优先级 | P1 关系条件 | 传给 P6 的 `roleCode` |
| --- | --- | --- |
| 1 | 用户在项目所属项目集的 `project_set_user_role` 中为管理员 | `INS_PM_ADMIN` |
| 2 | 用户存在该项目的 `project_member` 关系 | `INS_PM_STAFF` |
| 3 | 均不满足 | P1 返回 `PROJECT_ACCESS_DENIED`，不调用 P6 |

管理员优先于成员关系。同一用户可以在不同项目中解析出不同项目角色；项目角色不是 P6 全局角色的替代品。

## P6 契约与发布约束

P1 使用 P6 已有三参数接口，不改变 P6 行为。当前 P6 实现会先验证该用户是否拥有传入的全局 `roleCode`；未拥有时返回空菜单、空权限和空角色。故运行环境必须同时满足：

1. P6 已存在 `INS_PM_ADMIN`、`INS_PM_STAFF` 两个角色及其菜单、按钮关联；
2. 调用用户在 P6 `system_user_role` 中拥有被 P1 解析出的对应角色；
3. P1 使用包含 `UserPermissionRespDTO` 与 `getUserPermissionInfo` 的 `c-system-api:2.3.0` 制品，且 P6 服务端部署相同契约。

P1 不为该 RPC 增加降级：P6 调用失败沿既有异常链路返回，避免以空菜单掩盖跨服务故障。

## 代码与验证证据

P1 入口位于：

- `b-inspection-platform-core/.../controller/admin/project/ProjectPermissionController.java`
- `b-inspection-platform-core/.../service/project/impl/ProjectPermissionServiceImpl.java`
- `b-inspection-platform-core/.../config/SystemPermissionRpcConfiguration.java`
- `b-inspection-platform-core/.../test/.../ProjectPermissionServiceImplTest.java`

P6 契约位于 `c-system-api/.../permission/PermissionApi.java`，实现位于 `c-system-core/.../service/permission/PermissionServiceImpl.java`。

已运行：

```text
mvn -pl b-inspection-platform-core -am "-Dtest=ProjectPermissionServiceImplTest" "-Dsurefire.failIfNoSpecifiedTests=false" test
```

结果：5 tests，0 failures，0 errors；覆盖管理员优先、普通成员、无项目角色拒绝、跨项目角色差异和 P6 异常不降级。
