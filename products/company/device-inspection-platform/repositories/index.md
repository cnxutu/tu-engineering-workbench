# 仓库知识导航

## 范围

本目录按仓库保存已验证的产品责任、首选代码入口和专题知识。仓库角色以对应 manifest 为导航依据；当前代码、契约、配置和测试优先于本目录。

## 服务与适配器

| 仓库 | 目录入口 | Manifest |
| --- | --- | --- |
| `c-drone-inspection` | [P1 巡检业务平台](c-drone-inspection/index.md) | [manifest](c-drone-inspection.yaml) |
| `c-iot-server` | [P2 IoT 服务](c-iot-server/index.md) | [manifest](c-iot-server.yaml) |
| `c-iot-gateway` | [P3 IoT 网关](c-iot-gateway/index.md) | [manifest](c-iot-gateway.yaml) |
| `c-wvp` | [P3-1 视频流管理平台网关](c-wvp/index.md) | [manifest](c-wvp.yaml) |
| `ad-iot-codec-adapter-dji` | [P4 DJI 协议适配器](ad-iot-codec-adapter-dji/index.md) | [manifest](ad-iot-codec-adapter-dji.yaml) |
| `ad-iot-codec-adapter-robotDog-zhiyuan` | [P4-1 智元机器狗协议适配器](ad-iot-codec-adapter-robotDog-zhiyuan/index.md) | [manifest](ad-iot-codec-adapter-robotDog-zhiyuan.yaml) |
| `c-gateway` | [P5 统一网关](c-gateway/index.md) | [manifest](c-gateway.yaml) |
| `c-system` | [P6 系统管理服务](c-system/index.md) | [manifest](c-system.yaml) |
| `c-tag` | [P7 标签资源管理服务](c-tag/index.md) | [manifest](c-tag.yaml) |

## 共享依赖

- `star-framework` 是共享 Maven/Spring 基础框架，不是 Runtime Service；其已登记职责与待核实项见 [manifest](star-framework.yaml)，Runtime 能力溯源见 [共享框架能力溯源](../runtime/framework-capability-provenance.md)。
