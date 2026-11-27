# iPad 专属双应用源（洛雪音乐 + 小浣熊阅读）

专为 **Windows + iPad** 用户打造的纯净、开源、零隐私外泄 **SideStore / AltStore 二合一应用源**与自动构建交付中心。

- **SideStore / AltStore 一键订阅源地址**：
  ```text
  https://raw.githubusercontent.com/haywoodw04-jpg/ipad-app-store/main/source.json
  ```
- **零基础小白保姆级图文安装与使用手册**：👉 [**点此阅读 `INSTALL_GUIDE.md`**](./INSTALL_GUIDE.md)

---

## 收录应用与校验信息

| 应用 | 上游源码仓 | 版本 | 大小 | 未签名 `.ipa` 直链 | SHA-256 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **洛雪音乐 iPad 版** | [`haywoodw04-jpg/lx-music-ipad`](https://github.com/haywoodw04-jpg/lx-music-ipad) | `1.9.2` (build `79`) | `12.51 MiB` (`13,113,426` B) | [下载 IPA](https://github.com/haywoodw04-jpg/lx-music-ipad/releases/download/v1.9.2-ipad.1/lx-music-ipad-v1.9.2-ipad.1-unsigned.ipa) | `bc985c95fb700694abfe82229e5f34699ec502f1ce9034f506c397c93bdc2bbb` |
| **小浣熊阅读 iPad 版** | [`haywoodw04-jpg/legado-ipad`](https://github.com/haywoodw04-jpg/legado-ipad) | `0.1.16` (build `31`) | `15.90 MiB` (`16,676,844` B) | [下载 IPA](https://github.com/haywoodw04-jpg/legado-ipad/releases/download/v0.1.16-ipad.1/legado-ipad-v0.1.16-ipad.1-unsigned.ipa) | `9e3a7f4a904f31f900f30d8cb9807249501ba418984e69edfd61341403fd49a6` |

## 核心特性

1. **刚好满编免费 Apple ID 额度**：SideStore（1 名额 / 2 App ID）+ 洛雪音乐（1 名额 / 1 App ID）+ 小浣熊阅读（1 名额 / 1 App ID）= **`3/3` 名额、`4/10` App ID**，无需 LiveContainer，后台音频/锁屏播控/TTS/本地文件导入 100% 原生满血。
2. **iPad 深度原生优化**：
   - **洛雪音乐**：解锁原生 iPad 四方向全屏、分屏/台前调度、宽屏侧栏与双栏播放页、平板缩放限幅、按需混音开关、FormSheet 音源导入、外接键盘播控快捷键，清理残留定位权限。
   - **小浣熊阅读**：iPadOS 16+ 原生侧边栏导航、EPUB 横屏双页并排阅读、正文最大列宽滑块（600–1000pt）、外接键盘翻页、安卓兼容 WebDAV 备份恢复（密码强制存入 iOS Keychain）、默认开启严格 HTTPS 证书校验。
3. **透明可审计、零数据外泄**：两款应用均由 GitHub Actions 公开自动编译，严禁内置任何书源、音源或个人凭据；本仓 [`scripts/build_source.py`](./scripts/build_source.py) 自动解包校验每个 `.ipa` 的 `Info.plist`、0 签名、0 扩展、文件大小与 SHA-256。

## 仓库结构

```text
.
├── source.json                         # SideStore / AltStore Source v2 统一应用源
├── INSTALL_GUIDE.md                    # 中文小白保姆级安装与使用手册
├── README.md                           # 仓库总览与快捷入口
├── icons/                              # 应用图标（1024x1024 PNG）与源图标
│   ├── hub-icon.png
│   ├── lx-music-ipad.png
│   └── legado-ipad.png
├── scripts/
│   └── build_source.py                 # 自动拉取最新 Release、校验 .ipa 并生成 source.json
└── .github/workflows/
    └── update-source.yml               # GitHub Actions 定时/手动刷新 source.json
```

## 致谢与免责声明

- 洛雪音乐 iPad 版基于 [`lyswhut/lx-music-mobile`](https://github.com/lyswhut/lx-music-mobile) 与 [`fansa92/lx-music-mobile`](https://github.com/fansa92/lx-music-mobile)（Apache-2.0）。
- 小浣熊阅读 iPad 版基于 [`Aminark/legado-ios`](https://github.com/Aminark/legado-ios)（GPL-3.0）。
- 本仓库仅提供开源空壳应用的自动化打包与 SideStore 应用源索引，**不提供、不内置、不分发任何书源、音源或版权内容**；请遵守相关法律法规并支持正版。
