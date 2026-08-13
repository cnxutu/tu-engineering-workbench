# DJI Matrice 4TD OSD 属性

## 适用范围

本页只维护当前项目对接的 DJI Matrice 4TD（M4TD）无人机 OSD 属性参考，不扩展到 M4D 或其他无人机型号。

## 官方参考

- [DJI Matrice 4TD MQTT Properties（官方文档）](https://developer.dji.com/doc/cloud-api-tutorial/cn/api-reference/dock-to-cloud/mqtt/aircraft/m4d-properties.html)

该官方页面是 M4TD/M4D 页面入口；项目当前使用 M4TD，具体型号边界以本地设备模型和 P4 `DeviceEnum.M4TD` 核对。字段名称、数据类型、枚举和版本语义以官方文档为准。

## 当前代码接入事实

- P4 已注册 `DeviceEnum.M4TD`，设备模型编码为 `0-100-1`；负载 `99-0-0` 对应 M4TD Camera。
- P1 普通无人机 OSD 发送 `device_osd`，监控列表局部刷新重点字段为 `businessStatus`、`modeCode`、`battery`、`latitude`、`longitude`。
- DRC 高频 OSD 也使用 `device_osd`，但载荷字段较精简，当前不具备完整 `businessStatus` 判定数据。

## 证据状态

型号编码、P4 注册和 P1 处理入口为代码核对已确认；官方字段逐项映射待按官方页面补录（`pending_verification`）。
