# 大肥鱼一键包（SnowLuma / NapCat 可选版）

[简体中文](README.md) | [English](README.en.md)

把 DeepSeek 养进 QQ，双击一个 exe 就能装好。

装完后，她就是住在你 QQ 里的「大肥鱼」：有自己的性格，会发表情包、发语音、唱歌，记得你说过的话，隔一阵会主动找你，心情变了还会自己改 QQ 签名。

整个过程你只需要：**双击、选协议端、填 key、扫码或登录、等它装完**。不用装 Python，不用敲命令，也不用翻墙。

> ⚠️ **用小号模式时请用 QQ 小号**。第三方客户端登录有被风控、封号的风险，别拿自己的大号去登。

## 来源和改版说明

在 Jack-Cherish 的 DSQQ（https://github.com/Jack-Cherish/DSQQ）的基础上，我制作了一个改版，添加了 SnowLuma 功能。

- 上游项目：[Jack-Cherish/DSQQ](https://github.com/Jack-Cherish/DSQQ)
- 改版发布者：[maobuben](https://github.com/maobuben)
- 本仓库：[maobuben/DFYQQ](https://github.com/maobuben/DFYQQ)

原项目未声明开源许可证；原 DSQQ 代码的版权归 Jack-Cherish 所有。本仓库是带署名的个人非商业改版，不改变原代码的版权归属。第三方组件的许可证见 [NOTICE.md](NOTICE.md)。

## 这一版改了什么

这一版基于 [Jack-Cherish/DSQQ](https://github.com/Jack-Cherish/DSQQ) v1.2.0 修改，主要改动：

- **QQ 小号模式不再只能选 NapCat**：第一页可以在 **NapCat** 和 **SnowLuma** 之间选，两个协议端都支持全自动安装。
- 安装页、进度页、登录页、状态页都会写明当前用的是哪一个协议端，不会再出现「到底装的是 NapCat 还是 SnowLuma」的混淆。
- 进度列表里，原来固定写死的「启动 NapCat（登 QQ 用）」会按选择显示成「启动 NapCat（登 QQ 用）」或「下载并启动 SnowLuma（登 QQ 用）」。
- 登录页也分成两种：NapCat 是手机 QQ 扫码；SnowLuma 是在桌面 QQ 窗口里登录小号，页面会自动认出小号并接上 AstrBot。
- 新增 SnowLuma 的下载校验、配置生成、桌面 QQ 检测、连接状态判断和「打开桌面 QQ」按钮。
- 状态页会显示 SnowLuma 是否在运行、小号有没有被认出来、有没有连上 AstrBot，并能一键重启 SnowLuma。
- **界面整体重做**：从原来的「左侧蓝色大侧栏 + 白底表单」改成深海控制台风格——顶部横向步骤、右侧角色伴侣栏、深色玻璃卡片；在 1000×740 的小窗口里也能完整操作。
- 逻辑上顺手优化：SnowLuma 状态不再重复扫描、登录轮询不再每 2 秒重写配置、桌面 QQ 检测加了短缓存。
- README 同步更新。

## 下载

到 [Releases](../../releases/latest) 下载 `DaFeiYu-OneClick-v1.3.1-SnowLuma.exe`（约 174 MB）。GitHub 不支持中文文件名，所以用了英文名，下载后改不改名都能用。

> 这个 exe 没有把插件和表情包预装进去。第一次安装走到「装上人设、插件、表情包、语音、记忆」那一步时会联网下载（插件和两套表情包，几百 MB）；网络不好会停在那一步，点「重试」会接着下。只想先把聊天跑通的，也可以先跳过表情包，装好后再补。

如果这个 exe 是别人直接发给你的文件夹，文件夹里同时还会有源码、`README.md` 和 `SHA256.txt`。

下载后可以核对 sha256，确认文件完整、没被改过：

```
7b1324288f2d7c3bbe78504ea66353ab043263405a0662795f64e84ab50d464c
```

在 PowerShell 里运行 `Get-FileHash .\DaFeiYu-OneClick-v1.3.1-SnowLuma.exe` 就能看到。

## 系统要求

- Windows 10 / 11，64 位
- 安装盘剩余空间 10 GB 以上
- 安装路径只能有英文、数字和符号，不能有中文和空格（默认是 `D:\DaFeiYu`，没有 D 盘就用 `C:\DaFeiYu`）
- **选 SnowLuma 时**：电脑上要先装好**桌面版 QQ**（官方 NT 版，[im.qq.com](https://im.qq.com/)），并且小号要登在这个桌面 QQ 里

## 三种接入方式

安装第一页先选她怎么上 QQ：

| | QQ 小号 · NapCat | QQ 小号 · SnowLuma | QQ 官方机器人 |
|---|---|---|---|
| 怎么登录 | 手机 QQ 扫小号的码 | 在**桌面 QQ 窗口**里登录小号 | 用 QQ 开放平台的机器人 AppID 和 AppSecret |
| 自带的 QQ | 自带一份独立的 QQ，跟你平时用的 QQ 互不影响 | 不带 QQ，挂在你电脑正常打开的桌面 QQ 上 | 不需要 QQ 客户端 |
| 功能 | 完整：聊天、表情包、语音、主动找你、改签名、发空间 | 同样支持这些；具体以 SnowLuma 当前版本实现为准 | 基础聊天，QQ 空间这类小号功能用不了 |
| 风险 | 第三方登录，可能被风控或限制功能 | 第三方登录，可能被风控；QQ 自动升级后可能要等 SnowLuma 跟上 | 走腾讯官方接口，不用登录小号 |
| 认主人 | 安装时填你的大号 QQ | 安装时填你的大号 QQ | 装完后用你的 QQ 私聊机器人完成绑定 |

**怎么选：**

- **拿不准就选 NapCat**：它自带独立 QQ，不碰你平时用的 QQ，装法最成熟。
- 这台电脑平时就开着桌面 QQ、或者你不想再装一份独立 QQ，可以选 **SnowLuma**。它挂在桌面 QQ 上；QQ 支持多账号的话，小号和大号可以同时登着（具体以你的 QQ 版本为准）。
- 官方机器人适合不想登录小号、能接受基础功能的人。

### SnowLuma 需要你知道的几件事

SnowLuma 是 NapCat 那拨人做的新协议端。它和 NapCat 最大的不同是：**它自己不带 QQ，而是挂到这台电脑的桌面 QQ 上**，所以：

- 必须先装桌面版 QQ，小号要登在桌面 QQ 里。
- 你平时用桌面 QQ 登大号也没关系，可以再添加一个小号（QQ 支持多账号同时登录；具体以你的 QQ 版本为准）。
- QQ 自动升级到 SnowLuma 还不支持的新版本时，可能挂不上；要等 SnowLuma 出新版，或者换回 NapCat。
- SnowLuma 还在早期版本，更新很勤；好不好用、稳不稳是它作者维护的，本包只负责把它装好、接上 AstrBot。
- SnowLuma 的用户协议只允许**个人非商业使用**，不许修改它的程序，也不许把它单独转发、打包给别人。所以本一键包**不内置 SnowLuma**：安装时从官方发布地址下载，或者用你自己下载的官方 zip。安装第一页会让你先勾选同意它的用户协议和隐私政策。

## 开始之前要准备的

| 要准备什么 | 用来干什么 | 必须吗 |
|---|---|---|
| DeepSeek API key | 她用来想事情、说话 | 必须 |
| 你自己的 QQ 大号 | 她只认这个号是主人 | 必须（官方机器人模式装完再绑定） |
| 一个 QQ 小号，登在手机上 | NapCat 模式安装时用手机 QQ 扫码 | NapCat 模式需要 |
| 一个 QQ 小号，登在桌面 QQ 上 | SnowLuma 模式安装时在 QQ 窗口里登录 | SnowLuma 模式需要 |
| 桌面版 QQ（官方 NT 版） | SnowLuma 要挂在这个 QQ 上 | SnowLuma 模式需要 |
| QQ 机器人的 AppID 和 AppSecret（[QQ 开放平台](https://q.qq.com/)） | 机器人登录 | 官方机器人模式需要 |
| 豆包语音的 APP ID 和 Access Token（火山引擎） | 发语音、唱歌 | 可选，打开「语音与唱歌」才需要 |
| 硅基流动 API key | 长期记忆 | 可选，打开「长期记忆」才需要 |

每一项在安装界面里都有「去哪申请」，点开有一步步的说明。

## 安装步骤

1. **双击下载的 exe**。弹出「Windows 已保护你的电脑」时，点「更多信息」→「仍要运行」。exe 没有数字签名，所以会有这个提示。
2. **选接入方式和安装位置**：
   - 选 **小号 · NapCat**、**小号 · SnowLuma** 或 **QQ 官方机器人**。
   - 选 SnowLuma 时，页面会显示有没有检测到桌面 QQ；还要勾选同意它的用户协议和隐私政策，按钮才能点。
   - 点「开始安装」。从这一步起后台就开始装了，你填后面几页的时候它一直在跑。
3. **填信息**：DeepSeek key，再加上大号 QQ（小号模式）或机器人的 AppID 和 AppSecret（官方机器人模式）。语音和长期记忆按需要打开，再填对应的 key。每填一项就马上检查，打勾才算对。
4. **个性化**（可以跳过）：改名字、改性格、写一句话描述她的声音并试听、选表情包，也可以加你自己的图。
5. **等安装完成**。进度页会写明当前协议端：
   - NapCat：「启动 NapCat（登 QQ 用）」；
   - SnowLuma：「下载并启动 SnowLuma（登 QQ 用）」，第一次会下载约 41 MB，并自动打开桌面 QQ。
6. **登录**：
   - **NapCat**：用登着**小号**的手机 QQ 扫窗口里的二维码。
   - **SnowLuma**：在自动打开的**桌面 QQ** 窗口里登录小号（扫码或点「登录」都行）。页面会自动认出小号、把它接到 AstrBot，不用再点别的。如果页面一直没反应，点「重新检测 / 重启 SnowLuma」。
   - **官方机器人**：点「复制指令」，用你的 QQ 私聊机器人把这行指令发过去，再回窗口点「我已发送，检查结果」。指令 10 分钟内有效。
7. **完成**。用大号私聊她说一句「在吗」，她会回你。

桌面上会多一个「启动大肥鱼」。以后电脑重启了，双击它就能让她重新上线。

装到一半关了窗口、断电或者出错，再双击 exe 就会从断点接着装，填过的东西不用重填。

### SnowLuma 下载不动怎么办

一键包会依次尝试官方地址和几个 GitHub 加速地址。都不行时，进度页会停下并提示你：

1. 用浏览器打开 [SnowLuma Releases](https://github.com/SnowLuma/SnowLuma/releases)，下载 `SnowLuma-v2.4.2-win-x64.zip`；官方仓库偶尔打不开时，可以用同一个 release 的镜像 [TomyJan/SnowLuma](https://github.com/TomyJan/SnowLuma/releases)；
2. 把 zip 放到安装目录（比如 `D:\DaFeiYu\`）或安装目录的 `downloads\` 里；
3. 回到一键包点「重试」。

一键包会校验官方公布的 SHA-256，不会运行下坏的文件。

### 官方机器人模式要先做的设置

在 [QQ 开放平台](https://q.qq.com/) 创建机器人后：

1. 在开发设置里复制 AppID 和 AppSecret。
2. 「开发基础设置」→「事件订阅与回调地址」选 **WebSocket**，不能选 Webhook。
3. 「开发基础设置」→「内部体验号码」里加上你自己的 QQ 号。

详细说明见 [AstrBot 接入指南](https://docs.astrbot.app/platform/qqofficial/websockets.html)。

## 装好以后

双击「启动大肥鱼」会打开状态页，可以在里面：

- 看她现在的状态：在线、正在启动、需要扫码 / 需要在桌面 QQ 登录、或者出错了（会写原因）
- 让她上线、暂停聊天，或者全部停止并退出
- 选 SnowLuma 的，状态页有「打开桌面 QQ」「重新检测 / 重启 SnowLuma」
- 改名字、性格、声音、表情包，改各种 key，改完自动生效
- 退出小号或换一个号
- 打开 AstrBot 后台
- 遇到问题时点「检测与修复」

后台的地址、账号、密码在安装目录的 `我的信息.txt` 里。选 SnowLuma 的，这个文件里还会写 SnowLuma 后台的地址和密码。

改了性格之后，在 QQ 上给她发 `/reset`，她就会用新的人格重新开始聊。

### 用 SnowLuma 时平时要注意

- 桌面 QQ 要一直开着，小号也要一直登着；把 QQ 退掉，她就下线了。
- 电脑重启后，先让桌面 QQ 自动登录小号（QQ 设置里可以开开机自启和自动登录），再双击「启动大肥鱼」。
- QQ 自动升级后如果 SnowLuma 挂不上，先等 SnowLuma 出新版；等不及就在新目录装一套 NapCat 版，两套不要同时用小号。

## 常见问题

**被杀毒软件拦了**
把安装目录加进杀毒软件的信任列表，然后再双击 exe 接着装。SnowLuma 要往 QQ 里挂东西，最容易被杀毒软件盯上；文件被拿走了就重跑一键包，它会重新解压。

**SnowLuma 一直说「没找到桌面 QQ」**
先确认装的是**桌面版 QQ**（不是手机 QQ、不是 NapCat 自带的那份）。装好后重新打开一键包，或在状态页点「重新检测 / 重启 SnowLuma」。

**SnowLuma 说「桌面 QQ 里登着不止一个号」**
它分不清哪个是小号。请在桌面 QQ 里退出其他号，只留小号；或者退出所有号，只登小号，再点「重新检测」。

**SnowLuma 认出了小号，但一直连不上 AstrBot**
先点「重新检测 / 重启 SnowLuma」。还不行就点「检测与修复」，看 SnowLuma 日志（`logs\snowluma.log`）；确认小号没有在别的地方同时登录。

**SnowLuma 下载失败 / 校验不对**
按上面「SnowLuma 下载不动怎么办」手动放官方 zip。校验不对的包会被删掉，重新下即可。

**她不回话了 / 掉线了**
NapCat：新注册的小号容易被风控踢下线，重新扫一次码就好。
SnowLuma：先在桌面 QQ 里确认小号还在线；不在就重新登录，再点状态页的「重新检测 / 重启 SnowLuma」。

**装不上、起不来，不知道哪里出了问题**
点「检测与修复」。它会在本机检查安装文件和最近一次的启动错误，能修的直接给你修复按钮。看不懂结果的话，可以点「补充解释（DeepSeek）」让 DeepSeek 帮你分析。只会发送固定的诊断码，不会发原始日志、聊天记录、路径和配置，发之前也会先问你。

**端口被占用**
不用管。安装器会自己换一个没人用的端口。

**会不会动我电脑上原来的 QQ、AstrBot、NapCat？**
- NapCat 模式：不会。一键包只用它自己目录里的那一套。
- SnowLuma 模式：SnowLuma 会挂到**这个 Windows 用户打开的桌面 QQ** 上，这是它的工作方式；它只让小号那份配置连机器人。你原来的 QQ 登录记录、聊天数据不会被删。装之前请确认你接受这一点。

**想从 NapCat 换成 SnowLuma（或反过来）**
已经装好的目录不能直接切协议端（两套的登录方式不一样）。请用一键包选一个新的安装目录重装；旧目录先「全部停止并退出」，不要两套同时用小号。

**想卸载**
双击「启动大肥鱼」，在状态页里点「彻底卸载」，会删掉全部文件（包括下载的 SnowLuma 和它的配置）。桌面 QQ 本身不会被卸载。

## 安全

- AstrBot 后台、NapCat 后台、SnowLuma 后台、OneBot 连接都只在本机（`127.0.0.1`）开放，局域网里的其他设备连不上。OneBot 连接带随机 Token。
- 你填的 key 用 Windows DPAPI 加密保存，日志里会把 key、Token、密码过滤掉。
- 她只认你那个号是主人。发空间、改签名这类操作只听主人的。
- AstrBot 的「使用电脑能力」是关着的。
- 诊断不读聊天记录，也不会执行模型给出的命令。
- SnowLuma 的用户协议和隐私政策由它自己的作者提供；一键包只在用户勾选同意后才替用户传「已同意」，不会替用户做别的决定。

## 贡献者

1. [deepseek-ai](https://github.com/deepseek-ai) — AI 辅助开发、代码整理与文档协作。
2. [maobuben](https://github.com/maobuben) — 改版作者、发布者与维护者。

上游：[Jack-Cherish](https://github.com/Jack-Cherish) — DSQQ 原作者。完整名单见 [CONTRIBUTORS.md](CONTRIBUTORS.md)。

## 许可证和素材

本仓库是在 [Jack-Cherish/DSQQ](https://github.com/Jack-Cherish/DSQQ) 基础上制作的改版。原项目未声明开源许可证，原 DSQQ 代码的版权归 Jack-Cherish 所有；本仓库是带署名的个人非商业改版，不改变原代码的版权归属。

由 maobuben 新编写或修改的部分（SnowLuma 集成、安装器界面、文档和构建脚本改动）采用 MIT 许可证，详见 [LICENSE](LICENSE)。第三方组件（AstrBot AGPL-3.0、NapCat、SnowLuma、大肥鱼配置包 MIT、Python PSF）的版权与许可证归各自作者所有，详见 [NOTICE.md](NOTICE.md)。SnowLuma 不随本仓库分发，安装时从官方地址或镜像下载。

人设文字、立绘和表情包素材只供个人学习和自用。**请勿把本包或其中素材用于商业用途、二次售卖或再分发。** 素材的权利人如果希望移除，请提 Issue 联系。

---

## 开发者说明

下面是给维护者看的。普通用户直接下载 exe 就行。

### 它是怎么做的

- **外壳**：7-Zip 自解压（SFX）。双击后先解出一个很小的引导部分（便携 Python + 向导程序），等用户选好安装位置，再把真正的大包解到那里。
- **向导**：用 Python 标准库写的本地 HTTP 服务，只绑 `127.0.0.1`、随机端口，URL 里带一次性 token。页面是纯 HTML/CSS/JS，用 Edge 的 `--app` 模式打开，所以没有地址栏，看着像个独立窗口。
- **机器人**：[AstrBot](https://github.com/AstrBotDevs/AstrBot) 4.29.3 跑在便携 Python 3.12.10 上。
- **QQ 协议端（二选一）**：
  - **NapCat**：`NapCat.Shell.Windows.Node` v4.18.42 的自包含 Node 版，自带一份独立的 QQ。
  - **SnowLuma**：v2.4.2 的官方完整包，不带 QQ，挂在本机桌面 QQ 上，对 AstrBot 提供同样的 OneBot v11 反连。因为 SnowLuma 的许可不允许二次打包转发，一键包**不在 exe 里内置它**，而是在安装时下载，或使用用户自己放在安装目录里的官方 zip。
- **官方机器人模式**：直接用 AstrBot 自带的 QQ 官方 WebSocket 适配器。
- **大肥鱼的配置**：直接调用 [dafeiyu-config-pack](https://github.com/zexuanw958-svg/dafeiyu-config-pack) 自带的导入工具，没有另外重写。

### 目录结构

```
app/                  向导和状态页程序
  main.py             入口：判断这次该开安装向导还是状态页，然后打开窗口
  server.py           本地 HTTP 服务和接口
  installer.py        后台安装流程，支持断点续装；protocol 步按平台分发
  checks.py           检查安装路径，以及 DeepSeek、豆包、硅基流动的 key
  configs.py          生成 AstrBot / NapCat / SnowLuma 配置，挑空闲端口
  snowluma.py         SnowLuma 下载、校验、解压、配置、桌面 QQ 检测、状态判断
  services.py         启动、停止 AstrBot、NapCat、SnowLuma
  personalize.py      把名字、性格、声音、表情包写进配置包
  store.py            state.json 读写，key 用 DPAPI 加密
  shortcut.py         创建桌面快捷方式
  official_binding.py QQ 官方机器人模式：私聊绑定主人时的本机确认
  diagnostics.py      本机诊断和受限修复
  safe_logging.py     排障日志：先脱敏再限量写入
  log_capture.py      独立的日志读取进程，向导退出后继续收集服务输出
  fileio.py           先完整写临时文件再替换，避免配置写坏
  uninstall.py        卸载（实际删除由 uninstall.ps1 完成）
  web/                前端页面和图片
build/
  build.py            打包脚本，产出 dist/大肥鱼一键包.exe
  sfx_config.txt      自解压模块的配置
vendor/dafeiyu-config-pack/   大肥鱼配置包（上游提交 8c01b03）
dev/fake_wizard.py    本地调界面用的假后端，不装任何东西
tests/                单元测试
```

`state.json` 里的 `platform` 取值：

- `napcat`：QQ 小号 + NapCat
- `snowluma`：QQ 小号 + SnowLuma
- `official`：QQ 官方机器人

安装步骤的 key 固定为 `extract / ports / configs / astrbot / protocol / import / shortcut / login`；旧版的 `napcat` 会在打开时自动迁移成 `protocol`。

### 本地调界面

```
python dev/fake_wizard.py            # 走一遍安装向导
python dev/fake_wizard.py --status   # 看状态页
```

然后打开它打印出来的地址。假后端不会装任何东西：key 里带 `bad` 就算填错，进入扫码页 8 秒后自动登录成功。

### 跑测试

测试要在 **Windows** 上跑，有些用例依赖 `msvcrt` 和 PowerShell。

```
python -m unittest discover -s tests -t tests
node --test tests/test_web.cjs
```

### 打包

要在 **Windows** 上跑，要联网，要 Python 3.12+。

1. 先把下面三个文件放进 `downloads/`：
   - `astrbot-src.zip`：AstrBot 4.29.3 源码（GitHub tag v4.29.3 的 zip）
   - `astrbot.zip`：AstrBot 后台页面（`AstrBot-v4.29.3-dashboard.zip`）
   - `napcat-node.zip`：`NapCat.Shell.Windows.Node` v4.18.42（NapCat 原仓库发布已删除，可用归档镜像 [XingYunStar/NapCatQQ](https://github.com/XingYunStar/NapCatQQ) 的 v4.18.42）
2. 运行：

   ```
   python build/build.py
   ```

   便携 Python、get-pip、7-Zip 这些脚本会自己下载，已经下载过的话可以加 `--skip-download`。依赖走阿里云 PyPI 镜像。输出目录默认是 `dist/`，可以用 `--out` 改。中间文件都在 `.tmp/build/`。

   默认流程：组装目录 → 装依赖 → 起一个临时的 AstrBot，把插件和表情包提前下好 → 清掉构建过程中留下的密码、数据库、日志，然后扫一遍确认没有残留 → 压成 SFX。最后会输出 exe 的大小和 sha256。

   插件市场或 GitHub 连不上时，预装会失败。这时用：

   ```
   python build/build.py --skip-download --no-prewarm
   ```

   跳过预装，exe 会小很多（本次交付的就是这种，约 174 MB），插件和表情包改到安装时下载。两种模式装完都能用，区别只是第一次安装要不要等下载。

3. SnowLuma 不进构建产物。想改默认下载版本或地址，改 `app/snowluma.py` 顶部的 `VERSION`、`SHA256`、`URLS`。

### 发布

把 `dist/大肥鱼一键包.exe` 改名为 `DaFeiYu-OneClick-v1.3.1-SnowLuma.exe`，传到 GitHub Release，再把本文「下载」一节的文件名和 sha256 更新一下。exe 不进 git 仓库。





