# Dafeiyu One-Click Installer (SnowLuma / NapCat Edition)

[简体中文](README.md) | English

A Windows one-click installer that puts a DeepSeek-powered QQ companion into your QQ account.

Based on [Jack-Cherish/DSQQ](https://github.com/Jack-Cherish/DSQQ), this is a modified edition that adds SnowLuma support and a redesigned installer interface.

> **Attribution:** 在 Jack-Cherish 的 DSQQ（https://github.com/Jack-Cherish/DSQQ）的基础上，我制作了一个改版，添加了 SnowLuma 功能。
>
> In English: this is a modified edition of Jack-Cherish's DSQQ, with SnowLuma support added.

## Download

Download `DaFeiYu-OneClick-v1.3.1-SnowLuma.exe` (about 174 MB) from the [latest release](../../releases/latest).

The executable is not stored in this Git repository because it is larger than GitHub's normal file limit. It is attached to the GitHub Release instead.

SHA-256:

```
7b1324288f2d7c3bbe78504ea66353ab043263405a0662795f64e84ab50d464c
```

## What is new in this edition

- Choose **NapCat** or **SnowLuma** for the QQ account connection.
- The installer, progress page, login page and status page all show the currently selected protocol endpoint.
- SnowLuma support: download verification, configuration generation, desktop QQ detection, account recognition, connection status and restart.
- Redesigned interface: a dark "deep-sea console" layout with a top step bar and a companion panel on the right.
- Logic improvements: no duplicate SnowLuma status scan; no repeated config writes during login polling; short cache for desktop QQ detection.
- SnowLuma source: v2.4.2, with official URL + mirrors and SHA-256 verification.

## Requirements

- Windows 10 / 11, 64-bit
- At least 10 GB free space on the installation drive
- Installation path with English letters, digits and symbols only (no Chinese characters or spaces)
- **For SnowLuma:** desktop QQ (official NT client) must be installed, and the small QQ account must be logged in inside desktop QQ

## Three connection modes

| | NapCat | SnowLuma | QQ Official Bot |
|---|---|---|---|
| Login | Scan a QR code with the small account | Log in the small account in desktop QQ | AppID + AppSecret from QQ Open Platform |
| Bundled QQ | Yes, an isolated QQ client | No, hooks the desktop QQ | No QQ client needed |
| Features | Full companion features | Depends on SnowLuma's current implementation | Basic chat |
| Risk | Third-party login may trigger risk control | Third-party login; may need a SnowLuma update after QQ upgrades | Official Tencent API |

If unsure, choose NapCat. Choose SnowLuma if desktop QQ is already running on the machine and you do not want another isolated QQ client.

## Install

1. Double-click the exe. If Windows SmartScreen appears, click "More info" → "Run anyway".
2. Choose the connection mode and installation path.
3. Fill in the DeepSeek API key and the owner QQ number (or AppID/AppSecret for the official bot).
4. Personalize the name, persona, voice and meme packs if you want.
5. Wait for the installer to finish.
6. Log in:
   - NapCat: scan the QR code with the small account.
   - SnowLuma: log in the small account in the desktop QQ window; the installer detects it automatically.
   - Official bot: send the binding command to the bot from your owner QQ.
7. Send "在吗" to the bot from your main QQ.

## SnowLuma notes

- SnowLuma does not bundle QQ. It hooks the desktop QQ client of the current Windows user.
- The small account must be logged in inside desktop QQ.
- If QQ auto-updates to a version SnowLuma does not support yet, wait for a new SnowLuma release or switch to NapCat.
- SnowLuma's license allows personal, non-commercial use only. This repository does not redistribute SnowLuma. The installer downloads it from the official release or a mirror, and verifies the SHA-256.
- If the download fails, place `SnowLuma-v2.4.2-win-x64.zip` in the installation directory (or its `downloads` folder) and click Retry.

## Source layout

```
app/                  installer and status UI
  snowluma.py         SnowLuma download, verification, config, QQ detection, status
  installer.py        resumable installation pipeline
  server.py           local HTTP API
  web/                frontend
build/                build script
vendor/               dafeiyu-config-pack (MIT)
tests/                unit tests
预览/                  UI screenshots
```

## Build and test

Windows, Python 3.12+, network access.

```
python -m unittest discover -s tests -t tests
node --test tests/test_web.cjs
python build/build.py --skip-download --no-prewarm
```

The default build pre-installs plugins and memes and produces a larger exe. `--no-prewarm` produces a smaller exe; plugins and memes are downloaded during installation.

## License and credits

This repository is a modified edition of [Jack-Cherish/DSQQ](https://github.com/Jack-Cherish/DSQQ). The original project did not declare an open-source license; the copyright of the original DSQQ code remains with Jack-Cherish. This repository is a credited, personal, non-commercial derivative and does not change the copyright of the original code.

The modifications and new files authored by maobuben (including the SnowLuma integration, redesigned installer UI, documentation and build changes) are released under the MIT License. See [LICENSE](LICENSE); the scope note for the original upstream code is in [LICENSE-SCOPE.md](LICENSE-SCOPE.md).

Third-party components keep their own licenses:

- AstrBot — AGPL-3.0
- NapCat — see the NapCat repository
- SnowLuma — personal non-commercial use only; not redistributed here
- dafeiyu-config-pack — MIT
- Python — PSF License

See [NOTICE.md](NOTICE.md) for details.

## Contributors

1. [deepseek-ai](https://github.com/deepseek-ai) — AI-assisted development, code organization and documentation.
2. [maobuben](https://github.com/maobuben) — modified edition author, publisher and maintainer.
3. [Jack-Cherish](https://github.com/Jack-Cherish) — original DSQQ author.

See [CONTRIBUTORS.md](CONTRIBUTORS.md).

## Repository

https://github.com/maobuben/DFYQQ
