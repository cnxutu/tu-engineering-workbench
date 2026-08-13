# DRC

## 范围

DRC（Device Remote Control）描述 DJI 设备的远程控制会话、控制指令和相关低延迟遥测。DRC 的控制面与普通 OSD 的遥测面有关联，但不能共用未经核实的状态、缓存或时序假设。

## 当前平台边界

当前已核实的 DRC 高频 OSD 使用独立的 `inspection_drc_osd_report` identifier，并由 P1 独立处理；下行控制链路见 [DJI 设备指令下行链路](../../flows/dji-osd-command-flow.md)。DRC OSD 缺少完整业务状态判定所需字段时，平台 `businessStatus` 保持 `null`。

## 待补充内容

DRC 会话建立、心跳、控制权、频率限制、超时和失败恢复等协议细节，需要按具体 DJI 版本和当前代码分别核实；未核实内容标记为 `pending_verification`。
