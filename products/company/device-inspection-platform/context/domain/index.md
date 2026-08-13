# DJI 无人机领域知识

## 范围

本目录维护 DJI 无人机巡检场景中可跨任务复用的行业术语、协议语义和判定基础。它不替代 P1-P4 的代码、消息契约或运行配置，也不记录未经核实的项目行为。

## 何时读取

- 需要理解 HMS、OSD、DRC 或 DJI 设备消息语义时。
- 需要区分行业/协议原始字段与平台展示、业务判定字段时。
- 需要设计或排查角度、姿态、位置等遥测处理时。

## 主题导航

- [HMS](hms.md)：健康管理、告警和故障语义的术语边界。
- [OSD](osd.md)：设备遥测、姿态角和普通/DRC OSD 的语义边界。
- [DJI Dock 3 OSD 属性](dji-dock3-osd.md)：当前对接机场型号的官方 MQTT 属性参考。
- [DJI Matrice 4TD OSD 属性](dji-m4td-osd.md)：当前对接无人机型号的官方 MQTT 属性参考。
- [DRC](drc.md)：远程控制链路与高频遥测的术语边界。
- OSD 角度判定：当前项目阈值和异常规则尚未形成可复用、可追溯的批准结论；新增规则前应在 `decisions/` 建立 ADR，并引用代码、协议文档或测试证据。

## 证据状态

本目录的行业定义需要以 DJI 官方协议/SDK 文档或经确认的设备样本为证据。当前平台链路的已验证事实见 [DJI OSD 上行数据链路](../../flows/dji-osd-upstream-flow.md) 和 [DJI 协议映射](../../repositories/ad-iot-codec-adapter-dji/dji-adapter-mapping.md)。未有直接证据的内容标记为 `pending_verification`。
