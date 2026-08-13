# DJI Dock 3 OSD 属性

## 适用范围

本页只维护当前项目对接的 DJI Dock 3 机场 OSD 属性参考，不扩展到其他机场型号。

## 官方参考

- [DJI Dock 3 MQTT Properties（官方文档）](https://developer.dji.com/doc/cloud-api-tutorial/cn/api-reference/dock-to-cloud/mqtt/dock/dock3/properties.html)

官方页面是字段名称、数据类型、枚举和版本语义的权威来源。当前网页抓取不可用时，不从记忆或样例 payload 推导未列出的字段含义。

## 当前代码接入事实

- P4 以 DJI OSD Topic 解码机场属性；P1 接收规范化后的机场遥测并发送 `dock_osd`。
- P1 当前监控列表局部刷新重点字段为 `businessStatus`、`modeCode`、`droneInDock`、`flighttaskStepCode`。
- `wireless_link` 的 `link_workmode`、`sdr_quality`、`4g_quality` 还会驱动 P1 的 `wireless_link` 展示事件；具体平台语义见 [DJI OSD 上行数据链路](../../flows/dji-osd-upstream-flow.md)。

## 证据状态

型号范围和平台入口为代码核对已确认；官方字段逐项映射待按官方页面补录（`pending_verification`）。
