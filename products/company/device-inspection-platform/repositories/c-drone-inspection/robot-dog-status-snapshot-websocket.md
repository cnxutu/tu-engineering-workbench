# P1：机器狗完整状态快照 WebSocket 契约

> **证据等级：P1 当前代码与自动化测试已核对（2026-09-03）。** 本页是 `robot_dog_status_snapshot` 的通道、消息信封与载荷结构唯一说明；真实 P2/MQ/实机报文联调仍为 `pending_verification`。

## 范围与边界

该消息用于机器狗详情和驾驶舱状态部分的实时刷新。它发送的是合并后的**完整状态快照**，不是本次设备上报的增量字段，也不复用 DJI `device_osd`。

- 客户端连接：`/ws/dock`。
- 业务码：`robot_dog_status_snapshot`。
- 触发：机器狗有效状态帧合并后，快照内容或归约后的 `businessStatus` 发生变化。
- 不触发：旧 `properties.reportTime` 帧、内容不变的同时间重复帧，以及身份/项目校验失败的帧。
- 不提供机器狗专用离线 WS：120 秒有效窗口到期后的离线状态在 REST 查询时归约；页面重连或首次进入仍须调用 `GET /drone/robot-dog/{deviceId}/snapshot` 回拉。

`/ws/dock` 按路径中的 `dock` 聚合全部连接并广播，当前没有服务端项目会话筛选。`projectId` 是前端过滤标识，不是服务端项目隔离或授权边界。

## 外层消息信封

```json
{
  "biz_code": "robot_dog_status_snapshot",
  "deviceSn": "dock",
  "projectId": "project-a",
  "version": "1.0",
  "timestamp": 1788316800200,
  "data": {
    "deviceId": 10001,
    "deviceSn": "ROBOT-DOG-001",
    "projectId": "project-a",
    "businessStatus": "IDLE",
    "properties": {
      "reportType": "DEVICE_TELEMETRY",
      "deviceId": 10001,
      "deviceSn": "ROBOT-DOG-001",
      "productKey": "robot-dog",
      "reportTime": 1788316800123,
      "robotMode": "general",
      "motionStatus": "stand_up",
      "batteryPower1": 95.0,
      "batteryPower2": 75.0,
      "frontFillLight": false
    }
  }
}
```

示例只展示部分 `properties` 字段；实际 `data.properties` 是当前合并后的完整强类型快照。它可能含有设备尚未上报的 `null` 字段，具体 `null` 是否序列化取决于运行时 ObjectMapper 配置，前端不得把字段缺失解释为设备已清空该状态。

| 字段 | 当前实际值/类型 | 前端处理 |
| --- | --- | --- |
| `biz_code` | 固定字符串 `robot_dog_status_snapshot` | 先按此业务码分发。 |
| `deviceSn` | 固定字符串 `dock`，即 WS 通道标识 | **不能**用于匹配机器狗。 |
| `projectId` | 机器狗唯一项目空间绑定解析出的项目编码 | 仅接收与当前项目相等的消息。 |
| `userId` | 本消息发送时为 `null`，因统一信封的非空序列化规则不出现 | 不依赖该字段。 |
| `version` | 当前固定为 `1.0` | 仅作协议版本标识。 |
| `timestamp` | P1 发送时的服务器毫秒时间戳 | 不是设备上报时间；设备时序使用 `data.properties.reportTime`。 |
| `data` | 单个 `RobotDogStatusSnapshotDTO` 对象，非数组 | 在项目过滤后以其 `deviceId` 或 `deviceSn` 定位页面设备。 |

## `data` 与 `properties` 字段结构

| 层级 | 字段 | 当前语义 |
| --- | --- | --- |
| `data` | `deviceId`、`deviceSn`、`projectId` | P1 已校验的机器狗身份与项目归属。 |
| `data` | `businessStatus` | `OFFLINE`、`ABNORMAL`、`WORKING`、`IDLE`、`UNCLASSIFIED`；由在线键、软/硬急停和 `motionStatus` 动态归约。 |
| `data.properties` | `reportType`、`deviceId`、`deviceSn`、`parentDeviceId`、`parentDeviceSn`、`productKey`、`modelCode`、`firmwareVersion`、`reportTime` | 统一上行身份与元数据。`reportTime` 当前为 P1 `Long` 型设备上报毫秒时间戳。 |
| `data.properties` | `identifier`、`ssid`、`deviceType`、`chargingPileFirmwareVersion`、`robotStatusReportTime` | 设备与状态帧基础信息。 |
| `data.properties` | `robotTemperature`、`headAngle`、`headDirection`、`kneeMode`、`robotMode`、`motionStatus`、`obstacleAvoidance`、`controlSource`、`mileage` | 本体状态与模式原始上报值；除已归约的 `businessStatus` 外，不在前端写死未确认枚举。 |
| `data.properties` | `frontFillLight`、`backFillLight`、`autoFillLight`、`fillLightDisplayStatus`、`softwareEmergencyStop`、`hardwareEmergencyStop`、`speedLevel`、`bodySpeedX`、`bodySpeedY`、`bodyYawSpeed` | 灯光、安全与速度状态；不额外派生 `effectiveEmergencyStop`。 |
| `data.properties` | `batteryPower1/2`、`batteryPresent1/2`、`batteryCurrent1/2`、`batteryVoltage1/2`、`batteryTemperature1/2`、`batteryPowerSupplyStatus1/2` | 双电池状态。 |
| `data.properties` | `motorTemperatureFl1..4`、`motorTemperatureFr1..4`、`motorTemperatureBl1..4`、`motorTemperatureBr1..4`、`chargingPileConnected`、`uwbConnected`、`silenceEnabled` | 电机与连接状态。 |
| `data.properties` | `imuReportTime`、`imuAccelerationX/Y/Z`、`imuGyroscopeX/Y/Z`、`imuQuaternionW/X/Y/Z`、`lightSensorReportTime`、`ambientLightLux` | IMU 与光照传感器原始状态。 |
| `data.properties` | `motionControlReportTime`、`motionAccelerationX/Y/Z`、`motionGyroscopeX/Y/Z`、`bodyAngularVelocityX/Y/Z`、`worldAngularVelocityX/Y/Z`、`motionPositionX/Y/Z`、`motionQuaternionW/X/Y/Z`、`motionRpyRoll/Pitch/Yaw` | 运动控制状态。`motionPositionX/Y/Z` 是本地运动坐标，不是经纬度；`worldAngularVelocity*` 是世界坐标系角速度，不是地理坐标。 |
| `data.properties` | `bodyVelocityX/Y/Z`、`worldVelocityX/Y/Z`、`motionControlTimestamp`、`bodyVelocitySensorReportTime`、`bodyVelocitySensorX/Y/Yaw`、`jointStateReportTime`、`jointState` | 速度、时间戳和关节状态原始上报值。 |

所有 `properties` 字段的 Java 类型、Swagger `@Schema`、示例及当前可确认的枚举说明以 P1 的 `RobotDogStatusProperty` 和 `BaseDeviceStatusProperty` 为准；该页不另造字段或替代物模型定义。

## 前端接入顺序

1. 进入详情页或 WS 重连后，按当前项目请求 `GET /drone/robot-dog/{deviceId}/snapshot`；`data=null` 表示当前无可用快照。
2. 建立 `/ws/dock` 连接，收到消息先校验 `biz_code` 与外层 `projectId`。
3. 使用 `data.deviceId` 或 `data.deviceSn` 精确匹配当前页面设备；匹配后以**整个** `data` 替换本地快照，而不是把消息当增量 patch。
4. 以 `data.properties.reportTime` 判断设备数据的新旧；`timestamp` 仅表示 P1 的发送时间。

## 代码证据与验证边界

- WS 路径与会话分组：`b-inspection-platform-common/.../websocket/config/DeviceWebSocketConfigurer.java`、`DeviceWebSocketInterceptor.java`、`DeviceWebSocketHandler.java`。
- 统一消息信封及 JSON 字段名：`b-inspection-platform-common/.../websocket/resp/WebSocketMessageResponse.java`。
- 广播实现：`b-inspection-platform-common/.../websocket/service/impl/WebSocketMessageServiceImpl.java#sendBatchByDeviceType`。
- 触发、通道、业务码和完整快照：`b-inspection-platform-core/.../iot/impl/InspectionRobotDogStatusBusinessServiceImpl.java#updateSnapshot`，以及 `BizCodeEnum.ROBOT_DOG_STATUS_SNAPSHOT`。
- 载荷模型：`b-inspection-platform-common/.../iot/model/robotdog/RobotDogStatusSnapshotDTO.java`、`.../upstream/RobotDogStatusProperty.java`、`BaseDeviceStatusProperty.java`。

已有 P1 自动化覆盖状态合并、内容不变不重复推送和 WS 调用参数；真实浏览器连接、P2/MQ 和实机报文的端到端交付仍待 B4 与前端联调验证。
