# P6：系统管理服务关键入口地图

> **证据等级：代码与公开 API 契约核对已确认（2026-08-26）。** 本页只说明 `c-system` 的服务内职责与入口。某一巡检功能实际使用哪些 P6 API、权限模型和租户语义，须由调用方契约及运行配置进一步确认。

## 范围

`c-system` 提供用户、组织、角色、菜单、权限、OAuth2、字典、配置、文件及审计等通用系统能力。它的 `c-system-api` 模块是其他服务的 Feign/RPC 契约入口，`c-system-core` 实现管理端接口和业务服务，`c-system-bootstrap` 提供应用装配与迁移资源。

## 按问题类型读取

| 问题 | 首选入口 | 阅读顺序 |
| --- | --- | --- |
| 登录、Token、OAuth2 授权或踢下线 | `core/controller/admin/auth/`、`core/controller/admin/oauth2/`、`core/service/auth/`、`core/service/oauth2/` | HTTP/RPC 入口 → 授权服务 → Token/客户端数据 → 调用方或网关。 |
| 用户、部门、岗位信息不正确 | `api/user/AdminUserApi.java`、`api/dept/DeptApi.java`、`api/dept/PostApi.java`；对应 `core/api/` 与 `core/service/` | API 契约 → API 实现 → 服务/持久化。 |
| 菜单、角色、数据权限或用户权限不正确 | `api/permission/PermissionApi.java`、`RoleApi.java`；`core/controller/admin/permission/`、`core/service/permission/` | 请求入口 → 角色/菜单分配 → 权限计算 → 调用方权限使用点。 |
| 字典或参数配置未同步 | `api/dict/DictDataApi.java`、`api/config/ConfigApi.java`；对应 `core/api/` 与 `infra/core/` | RPC 契约 → 实现 → 缓存/配置与调用方刷新。 |
| 文件、日志或系统基础设施问题 | `api/file/`、`api/logger/`、`infra/core/` | API 契约 → Infra Controller/Service → 存储或审计实现。 |

## 已确认的边界

- `AdminUserApi` 提供用户查询、部门/岗位维度查询与有效性校验；`PermissionApi` 提供角色关联用户和用户菜单/角色/权限标识查询。
- P6 是用户、权限及其主数据的所有者；业务服务应通过 API/RPC 使用这些能力，不能以本地复制的用户或角色数据替代权限判断。
- 管理端 REST 与 RPC/Feign 契约应分别从 `c-system-core` Controller 和 `c-system-api` 接口开始，不以 README 中的接口清单替代当前注解契约。

## 代码证据

- 模块边界：`c-system-api`、`c-system-core`、`c-system-bootstrap`。
- 用户/权限 API：`c-system-api/.../api/user/AdminUserApi.java`、`.../api/permission/PermissionApi.java`、`RoleApi.java`。
- 实现入口：`c-system-core/.../api/user/AdminUserApiImpl.java`、`.../api/permission/PermissionApiImpl.java`、`core/service/user/`、`core/service/permission/`。

## 待核实项

- P1 的项目角色、菜单与数据权限请求在 P6 的具体 API 调用、缓存失效与错误码处理。
- OAuth2 Token 的生产签发/校验拓扑，以及 P5 到 P6 的实际调用路径。
