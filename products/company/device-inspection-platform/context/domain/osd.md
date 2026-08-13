# OSD

## 范围

OSD（On-Screen Display）在本产品中指设备遥测状态数据。行业/协议字段语义与平台展示字段必须分开记录；普通 OSD、State 和 DRC 高频 OSD 也不能默认视为同一种缓存或业务事件。

## 当前平台边界

当前已核实的 DJI 上行入口、identifier、机场/无人机身份路由和普通/DRC OSD 分流，见 [DJI OSD 上行数据链路](../../flows/dji-osd-upstream-flow.md)。P1 的 `businessStatus` 是展示层再包装字段，不是 DJI 原始协议字段。

当前型号范围仅包括：[DJI Dock 3 OSD 属性](dji-dock3-osd.md) 与 [DJI Matrice 4TD OSD 属性](dji-m4td-osd.md)。其他机场和无人机型号不作为当前产品知识的默认上下文。

## 角度与姿态

姿态角的轴定义、正负方向、单位、范围、坐标系和缺失值处理必须先以具体 DJI 协议/SDK 版本核实，再讨论项目阈值。当前尚无经批准的通用“角度异常”规则，不能仅凭字段名推导业务结论。

## 证据状态

平台链路部分为代码核对已确认；具体字段定义和版本差异为 `pending_verification`，应在补充时附协议文档、P4 解码入口和测试证据。
