# Step 2：机器狗补光控制接口契约（模拟）

> 本契约仅演示 Step 2 的产物形态。路径、枚举、错误码和服务标识不是已批准的真实接口。

## 决策

| ID | 决策 | 来源 |
| --- | --- | --- |
| D-01 | 补光状态复用机器狗完整状态快照 REST/WS。 | CAP-01、CAP-02、模拟评审 |
| D-02 | 三种灯统一使用一个动作接口，通过 `light` 区分。 | CAP-03、Q-01 |
| D-03 | HTTP 成功只表示 `ACCEPTED`；最终状态从快照回读。 | CAP-05、Q-02、Q-05 |
| D-04 | 外部控制源占用时，后端必须拒绝命令。 | CAP-04、Q-04 |

## REST 清单

| 能力 | Method / Path | 结论 | 用途 |
| --- | --- | --- | --- |
| CAP-01 | `GET /drone/robot-dog/{deviceId}/snapshot` | 复用 | 首屏和重连读取完整状态；三个灯位于 `properties`。 |
| CAP-03 | `POST /drone/robot-dog/{deviceId}/fill-light/action` | 新增 | 提交一次前灯、后灯或自动补光开关动作。 |

## 补光动作请求

```json
{
  "requestId": "01JDEMO123456",
  "light": "FRONT",
  "enabled": true
}
```

| 字段 | 类型 | 必填 | 语义与校验 |
| --- | --- | --- | --- |
| `deviceId` | path integer(int64) | 是 | P1 设备 ID；必须属于当前项目且为机器狗。 |
| `requestId` | string | 是 | 前端生成的请求标识；用于关联日志与重复提交，长度 1～64。 |
| `light` | string enum | 是 | `FRONT`、`REAR`、`AUTO`；仅为模拟 wire value。 |
| `enabled` | boolean | 是 | `true` 开启，`false` 关闭。 |

## 响应

```json
{
  "code": 0,
  "data": {
    "requestId": "01JDEMO123456",
    "acceptance": "ACCEPTED",
    "acceptedAt": "2026-09-03T10:15:30+08:00"
  },
  "msg": "success"
}
```

`ACCEPTED` 只表示 P1/P2 接受本次调用，不表示设备已经切换灯光。前端保持操作中状态，直到：

1. 收到完整状态快照，目标字段变为期望值；或
2. 到达前端等待窗口，提示“状态暂未确认”，允许重新拉取；不得显示“设备执行成功”。

## 错误语义

| 场景 | 模拟业务错误 | 前端行为 |
| --- | --- | --- |
| 设备不存在、不是机器狗或不属于当前项目 | `DEVICE_NOT_FOUND` | 关闭操作并刷新设备上下文。 |
| 当前用户无控制权限 | `FORBIDDEN` | 禁用入口并提示无权限。 |
| 外部控制源占用 | `ROBOT_DOG_CONTROL_OCCUPIED` | 保持当前状态，显示占用提示。 |
| `light` 非法或字段缺失 | `BAD_REQUEST` | 表单/请求校验，不重试。 |
| 上游未受理或设备无会话 | `ROBOT_DOG_COMMAND_REJECTED` | 结束操作中状态，允许用户重试。 |

## 状态与 WebSocket

状态 REST 和 WS 使用同一完整快照模型：

```json
{
  "deviceId": 10001,
  "deviceSn": "DEMO-ROBOT-001",
  "projectId": "demo-project",
  "properties": {
    "frontFillLight": true,
    "backFillLight": false,
    "autoFillLight": false,
    "controlSource": 2,
    "reportTime": 1788401730000
  }
}
```

- 首屏：调用快照 REST。
- 实时：消费完整快照 WS；不把单帧缺失字段当作 `false`。
- 重连：重新调用快照 REST，随后继续消费 WS。
- 项目过滤与设备匹配按既有完整快照契约执行。
- 本功能不新增独立补光查询、补光 WS 或命令结果 WS。

## 上游契约（模拟）

| 项目 | 值 | 成功证据 |
| --- | --- | --- |
| P2 service | `inspection_device_control` | P2 接受并路由请求 |
| command | `SET_FILL_LIGHT` | 仅为示例值 |
| 参数 | `light`, `enabled`, `requestId` | 脱敏下行样本 |
| 设备完成 | 后续状态上报对应字段变化 | 状态快照 REST/WS 回读 |

## 兼容与非目标

- 新增接口，不改变现有快照结构和其他机器狗控制接口。
- 不新增数据库表；请求追踪复用现有日志/调用链约定，真实实现前需从仓库核实。
- 不自动重试可能改变设备状态的控制命令。
- 不在本契约中定义亮度、定时、批量、控制权获取/释放或设备执行超时状态机。

## G2 结果

模拟接口评审已确认上述契约，`G2_contract_confirmed=verified`。真实任务需要前端、后端和相关上游对公开字段与成功语义确认后才能关闭。
