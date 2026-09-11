# 流程导航

## 范围

本目录维护已核实、可跨任务复用的端到端流程。具体实现、完整消息契约和运行时状态仍以目标仓库代码、契约、配置和验证证据为准。

## 当前流程

- 机场/无人机 OSD、State 或 DRC 数据上行：[DJI OSD 上行数据](dji-osd-upstream-flow.md)。
- 机场/无人机控制、任务或 DRC 指令下行：[DJI 设备指令下行](dji-osd-command-flow.md)。
- 强制关舱盖的下行与进度回显参考案例：[DJI 机场强制关舱盖：端到端案例](dji-cover-force-close-case.md)。
- 从产品需求、TSL、设备上报到 P1 业务投影：[设备状态与物模型端到端链路](device-state-thing-model-end-to-end.md)。
- 设备离线、P2 运行态与 P1 监控排查闭环：[设备离线状态链路与排查 SOP](device-offline-status-flow.md)。
- P2 主数据变更到 P1 `manage_device` 投影：[P2 设备主数据到 P1 投影同步](device-master-projection-sync.md)。
- 智元机器狗从协议映射到驾驶舱状态回读与控制下行：[智元机器狗上下行集成闭环](zhiyuan-robot-dog-end-to-end-integration.md)。

设备在线状态以外的通用 MQTT、完整媒体数据面、完整巡检任务或未列出的协议场景尚无独立 Flow；直接以目标仓库代码、契约和运行配置核实，取得稳定证据后再按需补充。
