# 来源、署名和第三方组件

## 改版说明

在 Jack-Cherish 的 DSQQ（https://github.com/Jack-Cherish/DSQQ）的基础上，我制作了一个改版，添加了 SnowLuma 功能。

- 上游项目：DSQQ
- 上游作者：Jack-Cherish
- 上游地址：https://github.com/Jack-Cherish/DSQQ
- 本改版发布者：maobuben（https://github.com/maobuben）

本仓库保留上游的目录结构、安装流程和配置包，主要新增/修改：

- SnowLuma 协议端支持（下载、校验、配置、启动、登录检测、状态判断）。
- 安装器界面整体重做（深海控制台风格）。
- 协议端选择、进度页、登录页、状态页的区分和文案。
- 相关 README、测试和构建说明。

## 贡献者

- [deepseek-ai](https://github.com/deepseek-ai)：AI 辅助开发、代码整理与文档协作。
- [maobuben](https://github.com/maobuben)：改版作者、发布者与维护者。
- [Jack-Cherish](https://github.com/Jack-Cherish)：上游 DSQQ 作者。

## 第三方组件

本仓库的源码不包含 AstrBot、NapCat、SnowLuma 的二进制发行包；一键包会在安装时下载或调用它们。各组件版权和许可证归各自作者所有：

| 组件 | 用途 | 许可证/说明 |
|---|---|---|
| [AstrBot](https://github.com/AstrBotDevs/AstrBot) | QQ 机器人框架 | AGPL-3.0 |
| [NapCat](https://github.com/NapNeko/NapCatQQ) | QQ OneBot 协议端（可选项） | 以 NapCat 上游仓库声明为准 |
| [SnowLuma](https://github.com/SnowLuma/SnowLuma) | QQ OneBot 协议端（可选项） | 作者许可：仅限个人非商业使用；不随本仓库分发 |
| [dafeiyu-config-pack](https://github.com/zexuanw958-svg/dafeiyu-config-pack) | 大肥鱼人格、插件和表情包配置包 | MIT（许可证见 `vendor/dafeiyu-config-pack/LICENSE`） |
| Python | 运行时 | PSF License |

SnowLuma 的用户协议和隐私政策由 SnowLuma 作者提供。安装器只会在用户勾选同意后传递“已同意”状态；本仓库不重新分发 SnowLuma 的发行包。

## 关于 exe

`DaFeiYu-OneClick-v1.3.1-SnowLuma.exe` 约 174 MB，超过 GitHub 普通 Git 仓库的单文件建议大小，因此**不放进 Git 仓库**，请作为 GitHub Release 附件上传。源码、README、LICENSE、测试和预览图在仓库中。

## 素材

人设文字、立绘和表情包素材仅供个人学习与自用。请勿把本仓库或其中素材用于商业用途、二次售卖或再分发。素材权利人如希望移除，请提 Issue 联系。
