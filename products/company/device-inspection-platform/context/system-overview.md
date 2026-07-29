# 系统概览

## 已验证

平台由巡检业务平台、IoT Server、IoT 网关与 DJI 协议适配器协作组成。业务平台拥有业务/核心/IoT/启动模块，并处理媒体与视频；网关承担设备侧连接和协议入口；DJI 适配器仅做映射。

## 待验证

IoT Server 是否已集中作最终状态判定，以及服务运行边界、部署单元、数据库划分、API 网关与完整消息拓扑，均尚待确认。参见 [部署拓扑](../architecture/deployment-topology.md) 与 [集成地图](../architecture/integration-map.md)。
