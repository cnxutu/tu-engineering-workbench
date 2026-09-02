# P4-1：智元机器狗协议映射

> **证据等级：适配器源码与测试已核对（2026-09-02）。** 该仓库是 P3 `CustomProtocolAdapter` 的智元机器狗适配器：管理 WebSocket 会话，将智元 APDU 映射为统一物模型上行消息，并将两个统一异步 service 编码为下行 APDU。P4-1 仅为 P0 导航编号，不是仓库内的服务名或运行配置值。

## 何时读取

- 新增或排查智元机器狗的 WebSocket 握手、心跳、重连、APDU 解析、上行字段或下行 service 映射。
- 联调 P3 Custom 协议制品装载、`zhiyuan-robot-dog` codec ID、`robot-dog` 产品与设备 SN 绑定。

## 已确认的映射边界

| 方向 | 适配器当前职责 |
| --- | --- |
| 会话 | 以 WebSocket 客户端连接设备；仅在握手 SN 命中 Gateway 同步的候选设备后绑定会话，并在本适配器内维护握手、心跳与重连。 |
| 上行 | 将 `1004`、`1100`–`1104` 等状态帧映射为 `thing.property.post`；将 `1005`、`1016`、`1017` 映射为统一事件。上行身份使用 `productKey=robot-dog` 与握手 SN。 |
| 下行 | 仅接受 `thing.service.invoke`，将 `inspection_device_control` 与 `inspection_config_command` 转码后写入已绑定 WebSocket；返回 `NONE`，不等待设备动作完成。 |
| 非职责 | 不定义或发布 TSL/Data Rule，不编排控制权、急停、遥控频率或业务重试，也不替代 P3 的运行时配置和制品装载。 |

## 联调约束与待核实项

- P3 必须实际引入适配器制品并启用匹配的 Custom 协议配置；仅存在 YAML 或仅存在 Jar 都不足以建立会话。
- P2 的产品、TSL、Data Rule 与 P1 的消费/控制语义属于跨服务契约，当前仓库源码不能证明其联调状态。
- 本地自动化测试覆盖协议映射和模拟 WebSocket；真实设备兼容性、P3 运行配置与生产部署状态仍为 `pending_verification`。

## 代码证据

以下路径相对适配器仓库根目录：

- `src/main/java/com/xmkj/codec/adapter/robotdog/zhiyuan/ZhiyuanRobotDogCustomProtocolAdapter.java`：Custom 协议生命周期、候选 SN 绑定、上/下行入口。
- `src/main/java/com/xmkj/codec/adapter/robotdog/zhiyuan/autoconfigure/ZhiyuanRobotDogAutoConfiguration.java`：自动配置与固定 Bean 注册。
- `src/main/java/com/xmkj/codec/adapter/robotdog/zhiyuan/protocol/ZhiyuanUpstreamMapper.java`：APDU 上行物模型映射。
- `src/main/java/com/xmkj/codec/adapter/robotdog/zhiyuan/protocol/ZhiyuanDownstreamEncoder.java`：统一异步 service 的下行编码。
- `src/test/java/com/xmkj/codec/adapter/robotdog/zhiyuan/`：协议、映射、生命周期与自动配置测试。
