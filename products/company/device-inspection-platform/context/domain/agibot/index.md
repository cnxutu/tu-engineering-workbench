# 智元酷拓（Agibot）厂商资料入口

> **证据等级：厂商公开 SDK 仓库核对（阅读日期 2026-08-31）。** 本目录维护智元酷拓设备接入可复用的厂商资料入口、版本追溯与使用边界；不定义任何型号的产品契约、平台物模型或接入架构。当前已登记的公开资料仅覆盖 D1 Max；其他型号须在获得一手资料后另建型号页面或补充本页。

## 何时读取

- 新增或评估智元酷拓设备接入，需要定位 SDK、官方示例、版本兼容或原始协议资料。
- 核对 SDK 与设备固件的匹配关系，或准备 SDK 升级、回滚与厂商技术支持材料。
- 需要确认厂商资料的适用型号，避免将 D1 Max 的接口、频率或状态语义套用到其他型号。

## 资料导航

| 用途 | 一手资料 | 使用约束 |
| --- | --- | --- |
| D1 Max SDK 下载、示例、头文件与预编译库 | [AgibotTech/Agibot_D1_Max](https://github.com/AgibotTech/Agibot_D1_Max) | 实施前记录实际使用的 commit/tag、SDK 包版本与设备固件版本。 |
| D1 Max 版本兼容、环境与 C++ Demo | [D1 Max 中文 README](https://github.com/AgibotTech/Agibot_D1_Max/blob/main/README_zh.md) | README 的兼容表只作入口；最终以厂商为目标设备交付的配套 SDK 包为准。 |
| D1 Max SDK 版本演进 | [D1 Max CHANGELOG](https://github.com/AgibotTech/Agibot_D1_Max/blob/main/CHANGELOG.md) | 升级前核对破坏性变更、固件兼容性与回滚包。 |
| D1 Max 数据、故障、控制权与命令 ACK 回调 | [D1 Max SDK 回调接口](https://github.com/AgibotTech/Agibot_D1_Max/blob/main/docs/zh/sdk_callback_zh.md) | 回调仅做复制或入队；不得在回调线程执行网络阻塞或业务处理。 |
| D1 Max API、数据结构、状态流转与原始协议 | [D1 Max SDK 文档目录](https://github.com/AgibotTech/Agibot_D1_Max/tree/main/docs) | 原始协议仅在不使用 SDK 且获得厂商授权/说明时评估；不得据此假定可由 Java 重实现。 |

## 版本与资料治理

- 公开仓库的 `main` 分支不是可复现的实施版本。每次接入、升级或问题排查都应记录固定 commit/tag、SDK 包版本和目标设备固件版本。
- 厂商交付的私有 SDK 压缩包、PDF 或许可证如与公开仓库不一致，以与目标设备固件配套的交付包为准；任务记录仅保存脱敏后的版本号、获取渠道和固定 commit/tag。
- 不将厂商包内凭据、设备网络信息、许可证全文或未脱敏运行样本写入本知识库。

## 型号入口

- [D1 Max SDK 能力与接入约束](../zhiyuan-d1-max-sdk.md)：D1 Max 的已核对能力、状态/安全语义、与平台边界及待确认契约。
