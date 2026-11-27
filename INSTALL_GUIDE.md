# iPad 洛雪音乐 + 小浣熊阅读｜零基础保姆级安装与使用手册

> **适用人群**：只有 **Windows 电脑 + iPad**（没有 Mac），希望**完全免费、极简开箱、不折腾、不泄露隐私**地在 iPad 上同时畅听「洛雪音乐」和畅读「小浣熊阅读（Legado 兼容）」。  
> **隐私与安全承诺**：两款 App 均由开源代码经独立源码安全审计后，通过 GitHub Actions 公开透明自动编译；**0 遥测、0 广告、0 内置书源/音源**；你的书源、阅读记录、歌单和自定义音源 **100% 只保存在你自己的 iPad 本地**。

---

## 零、核心交付链接与校验区（开箱速取）

### 1. SideStore 二合一专属应用源链接（主力推荐，复制这一条即可）

```text
https://raw.githubusercontent.com/haywoodw04-jpg/ipad-app-store/main/source.json
```

> 在 iPad 的 **SideStore → Sources** 粘贴上面这一条地址，就能像 App Store 一样同时安装和一键更新两款 App！

### 2. 未签名 `.ipa` 官方直链与 SHA-256 校验（用于 Sideloadly 兜底或手动核验）

| 应用名称 | Bundle ID | 版本号 | 文件大小 | 下载直链（GitHub Releases） | SHA-256 校验值 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **洛雪音乐 iPad 版** | `cn.toside.music.mobile` | `v1.9.2` (build `79`, tag `v1.9.2-ipad.1`) | `12.51 MiB` (`13,113,426` 字节) | [lx-music-ipad-v1.9.2-ipad.1-unsigned.ipa](https://github.com/haywoodw04-jpg/lx-music-ipad/releases/download/v1.9.2-ipad.1/lx-music-ipad-v1.9.2-ipad.1-unsigned.ipa) | `bc985c95fb700694abfe82229e5f34699ec502f1ce9034f506c397c93bdc2bbb` |
| **小浣熊阅读 iPad 版** | `com.epiboly.legado` | `v0.1.16` (build `31`, tag `v0.1.16-ipad.1`) | `15.90 MiB` (`16,676,844` 字节) | [legado-ipad-v0.1.16-ipad.1-unsigned.ipa](https://github.com/haywoodw04-jpg/legado-ipad/releases/download/v0.1.16-ipad.1/legado-ipad-v0.1.16-ipad.1-unsigned.ipa) | `9e3a7f4a904f31f900f30d8cb9807249501ba418984e69edfd61341403fd49a6` |

### 3. 为什么这套方案稳？（免费 Apple ID 额度账本）

Apple 免费个人账号允许同设备同时激活 **3 个侧载 App**、每 7 天最多注册 **10 个 App ID**：
- **SideStore 本体**：占 `1` 个 App 名额 / `2` 个 App ID
- **洛雪音乐 iPad 版**：占 `1` 个 App 名额 / `1` 个 App ID（实测 **0 扩展**）
- **小浣熊阅读 iPad 版**：占 `1` 个 App 名额 / `1` 个 App ID（实测 **0 扩展**）
- **总计**：正好 **`3 / 3` 个名额、`4 / 10` 个 App ID**！**无需折腾 LiveContainer**，后台听歌、锁屏切歌、AirPlay、后台听书与本地文件导入全部 **100% 原生满血**。

> 💡 **安装前 10 秒彩蛋检查**：打开 iPad「设置 → 通用 → 关于本机」看一眼 **iPadOS 版本**。如果你的老 iPad 恰好停留在 **iPadOS 17.0 或更低**（不含 16.7.x 正式版），可直接去搜索用 Windows 跑 **TrollRestore 安装 TrollStore（巨魔商店）**，装完上面两个 `.ipa` 即可**永久免续签**！绝大多数 iPadOS 17.0.1 / 18 / 26 用户请直接看下面「主力方案」。

---

## 一、主力安装路径：SideStore（首次连 Windows 10 分钟，以后彻底脱离电脑）

这套方案由 **Windows `iloader`（只插线用 1 次）+ iPad `LocalDevVPN`（免费回环工具）+ `SideStore` + iPadOS 快捷指令自动续签** 组成，全面支持 **iPadOS 15 / 16 / 17 / 18 / 26**。

### 账号准备说明（先看清 3 个账号互不干扰）
1. **你的主力 iCloud 账号**：负责照片、备忘录、同步，**全程绝对不要退出**！
2. **美区（或任意非国区）Apple ID**：仅在蓝色 **App Store** 里临时登录 1 分钟，用来免费下载 `LocalDevVPN`，下完马上切回国区。
3. **自签专用免费小号 Apple ID（强烈推荐）**：单独注册一个普通免费 Apple ID（国区/美区均可），专门填给 `iloader` 和 `SideStore` 做 7 天自签，和主力号完全隔离更安心。

---

### 第 1 步（iPad）：下载免费 `LocalDevVPN`

> 🚨 **【红字高危警告 · 千万别点错！】**  
> **绝对不要在 iPad「设置」最顶部退出你的 iCloud 账号！** 那样会导致照片、备忘录、云盘同步混乱。  
> 下方操作**只在桌面上蓝色的「App Store」图标里**切换账号！

1. 打开 iPad 桌面上的蓝色 **App Store** App。
2. 点击右上角你的**圆形头像** → 滑到页面最底部 → 点击 **「退出登录」**。
3. 在同一页面登录你的**美区 / 外区 Apple ID**。
4. 在 App Store 搜索并免费下载 **`LocalDevVPN`**（开发者：`Coxson Engineering LLC`，免费开源本地回环工具，不上传任何网络流量、几乎零耗电）。
5. 打开 `LocalDevVPN` → 点击 **Connect（连接）** → 弹出“允许添加 VPN 配置”时点 **「允许」** 并输入 iPad 锁屏密码。
6. 下载并授权完成后，回到 **App Store** 右上角头像处退出外区号，**重新登录回你的国区 Apple ID** 即可。

---

### 第 2 步（Windows + 数据线）：用 `iloader` 一次性安装 SideStore

1. **在 Windows 电脑安装 Apple 官网桌面版 iTunes（关键！）**：
   - 前往 Apple 官网下载 **Windows 64 位独立安装包版 iTunes（`.exe`）** 并安装完成（安装完重启一次电脑最稳）。
   - ⚠️ **千万不要使用微软商店（Microsoft Store）里的 iTunes 或“Apple 设备”应用**！商店版缺少底层通信驱动，会导致识别不到 iPad（若电脑里已装微软商店版，建议先卸载）。
2. **下载 Windows 版 `iloader`**：
   - 从 SideStore 官方主页（`https://sidestore.io`）或官方 GitHub 下载最新的 Windows 版 **`iloader`**。
3. **USB 连接并安装 SideStore**：
   - 用支持数据传输的 USB 线把 iPad 接到 Windows 电脑，解锁 iPad，弹窗点 **「信任此电脑」** 并输入锁屏密码。
   - 运行 Windows 上的 `iloader`，登录你的**签名专用免费小号 Apple ID**（注意邮箱大小写敏感）。
   - 在设备列表选中你的 iPad → 点击 **Install SideStore (Stable)**。
   - 等待进度条走完：`iloader` 会自动把 SideStore 装到你的 iPad 桌面，并自动生成注入配对文件（`pairing-file.plist`）。
4. **在 iPad 开启「开发者模式」并信任证书**：
   - 打开 iPad **设置 → 隐私与安全性** → 滑到最底部 → 开启 **「开发者模式」** → 按提示重启 iPad，重启完成后弹窗再次点「开启」并输入密码。
   - 打开 iPad **设置 → 通用 → VPN 与设备管理** → 在「开发者 App」下方点开你的签名 Apple ID → 点击 **「信任」** 并确认。
5. **完成首次本机激活**：
   - 确保 iPad 连着 Wi-Fi，打开 **`LocalDevVPN`** 确认处于 **Connected（已连接）** 状态（右上角出现 `VPN` 图标）。
   - 打开桌面上的 **SideStore** → 用**同一个签名小号 Apple ID** 登录。
   - 切到底部 **My Apps** 标签页 → 点一下 SideStore 右侧的 **`7 DAYS`** 绿色按钮完成首次本机续签（若提示创建/撤销开发证书，点确认即可）。
   - 🎉 **恭喜！现在可以拔掉数据线了，以后再也不需要插电脑！**

---

### 第 3 步（iPad）：粘贴 1 条源链接，一键安装「洛雪音乐」和「小浣熊阅读」

1. 确认 iPad 已连接 Wi-Fi 且 **`LocalDevVPN` 处于开启状态**。
2. 打开 **SideStore** → 点击底部 **Sources（源）** → 点击右上角 **`+`** 号。
3. 粘贴我们的二合一源地址并确认添加：
   ```text
   https://raw.githubusercontent.com/haywoodw04-jpg/ipad-app-store/main/source.json
   ```
4. 点击刚添加好的 **「iPad 专属双应用源（洛雪 + 阅读）」**，你会看到两款专属 App：
   - 点 **「洛雪音乐」** 右侧的 **GET / 安装**；
   - 点 **「小浣熊阅读」** 右侧的 **GET / 安装**。
5. 稍等半分钟，两款 App 就会直接出现在 iPad 桌面！
   - 以后我们发布了新版本优化，你只需打开 `LocalDevVPN` → 打开 `SideStore` → 点一下 **Update（更新）** 就能原地无损升级，**书架、书源、进度和歌单全部保留**！

---

### 第 4 步（iPad · 3 步搞定）：配置「快捷指令」每日自动续签（彻底免管）

免费个人证书每 7 天需要续签一次。用 iPad 自带的「快捷指令」做好自动化后，**每天插电充电时 iPad 自己偷偷续签**，你再也不用记着 7 天倒计时：

1. **创建自动化触发器**：
   - 打开 iPad 自带 **「快捷指令（Shortcuts）」** → 底部切到 **「自动化」** → 点右上角 **`+`**。
   - 选 **「充电器」** → 勾选 **「已连接」**（或者选 **「特定时间」** 如每天凌晨 `03:00`）。
   - ⚠️ **关键一步**：下方必须选中 **「立即运行（Run Immediately）」**，并关闭「运行时通知」→ 点「下一步」→ 点 **「新建空白自动化」**。
2. **按顺序添加 5 个动作**：
   - 点「添加操作」，依次搜索并加入：
     1. **连接 `LocalDevVPN`**（搜索 `LocalDevVPN` 或系统动作 `设定 VPN` → 选 `LocalDevVPN` → 连接）
     2. **等待** → 改成 **`5` 秒**
     3. **Refresh All Apps**（搜索 `SideStore` → 选 `Refresh All Apps`）
     4. **等待** → 改成 **`30` 秒**
     5. **断开 `LocalDevVPN`**（同第 1 步，改为断开连接）
3. **保存并试跑**：
   - 点右上角 **「完成」**。你可以先点一下自动化里的播放按钮手动试跑一次，看到 SideStore 进度正常刷新且 VPN 自动断开即大功告成！

---

## 二、兜底安装路径：Windows `Sideloadly`（没有外区 Apple ID 时）

如果你实在不想注册/切换外区 Apple ID 下载 `LocalDevVPN`，且 iPad 主要在家里使用、Windows 电脑每周至少开几次机，可以直接用 **Sideloadly**：
- ✅ 无需外区 Apple ID、无需 VPN
- ✅ 不占 iPad 商店名额（3 个免费名额全留给业务 App，装完这两款还多 1 个空位）
- ⚠️ 缺点：必须靠家中开机的 Windows 电脑同 Wi-Fi 续签（出门超 7 天会临时过期）

### 傻瓜 4 步操作
1. **安装官网版 iTunes 并开启 Wi-Fi 同步**：
   - Windows 安装 **Apple 官网桌面版 iTunes**（不要微软商店版），USB 连接 iPad 并在 iPad 点「信任」。
   - 打开 iTunes → 点左上角小 iPad 图标 → 左侧选 **摘要** → 下方勾选 **「通过 Wi-Fi 与此 iPad 同步」** → 点击 **应用**。
2. **下载 Sideloadly 与两款 `.ipa`**：
   - 前往 `https://sideloadly.io` 下载并安装 Windows 版 **Sideloadly**。
   - 点击本手册最上方表格中的直链，把「洛雪音乐」和「小浣熊阅读」两个 `.ipa` 下载到电脑。
3. **拖入安装并勾选自动续签**：
   - 打开 Sideloadly → 左侧拖入第 1 个 `.ipa` → 填入你的免费小号 Apple ID → **勾选「Automatic Refresh（自动续签）」** → 点击 **Start** 等待完成。
   - 重复拖入第 2 个 `.ipa` 点击 **Start**。
   - 在 iPad 打开 `设置 → 隐私与安全性 → 开发者模式`（重启生效），再到 `设置 → 通用 → VPN 与设备管理` 点击「信任」你的 Apple ID。
4. **保持托盘守护进程开机自启**：
   - 确认 Windows 任务栏右下角托盘里的 **Sideloadly Daemon** 正在运行（默认会随开机启动）。以后只要 iPad 和 Windows 电脑连着同一个 Wi-Fi，到期前会自动无线续签！

---

## 三、开箱导入与 iPad 专属功能使用指引

### 📖 1. 小浣熊阅读（Legado iPad 加强版）

#### ① 安全导入书源与本地电子书
- **在线书源**：进入 **「我的 → 书源管理」**，支持 JSON 文件、剪贴板、URL 链接、二维码或直接点击 `legado://` 链接导入你信赖的开源 Legado 书源（支持批量搜索、自动换源、替换净化规则与 RSS 订阅）。
- **本地 TXT / EPUB**：点击书架右上角菜单或 **「我的 → 文件管理」**，从 iPad 自带「文件」App 直接导入 TXT / EPUB（集成 Readium 3.8 引擎，完美保留 EPUB 2/3 原书插图、表格与目录）。
- **HTTPS 证书安全加固**：我们已默认关闭“忽略证书错误”（`ignoreCertificateErrors = false`），防中间人劫持。只有当你明确信任某个证书过期的旧书源站点时，再去设置页临时开启即可。

#### ② 必配：坚果云免费 WebDAV 云备份（密码 Keychain 加密）
强烈建议花 2 分钟配好免费 WebDAV，换设备或误删 App 时 1 秒找回全部书架、书源和阅读进度：
1. 浏览器登录 **坚果云（Jianguoyun）** 网页版 → 右上角账号 → **账户信息 → 安全选项 → 第三方应用管理** → 点击「添加应用」（名字填 `Legado`）→ 复制生成的**专属应用密码**（⚠️ 不要填坚果云登录密码！）。
2. 打开小浣熊阅读 → **「我的 / 设置 → WebDAV 备份与恢复」**：
   - 服务器地址：选择预设 **坚果云**（`https://dav.jianguoyun.com/dav/`），也支持 InfiniCLOUD（`https://teracloud.jp/dav/`）或自建 WebDAV。
   - 账号：填你的坚果云登录邮箱；密码：粘贴刚才生成的**应用密码**。
3. 点击 **「测试连接」** 提示成功后，点 **「立即备份」** 即可上传标准 `backupYYYY-MM-DD.zip`（与安卓版 Legado 互通！）。
4. 🔐 **隐私保障**：你的 WebDAV 密码已通过 iOS 原生 **Keychain（系统钥匙串）** 加密存储，绝不会以明文保存在配置或数据库里。

#### ③ iPad 专属大屏效率用法
- **原生侧边栏导航**：在 iPadOS 16+ 宽屏/横屏下自动展开原生侧边栏（书架 / 发现 / 统计 / 我的），书架网格自适应大屏，支持分屏一边看书一边记笔记。
- **EPUB 横屏双页并排**：打开 EPUB 电子书 → 点屏幕中央呼出菜单 → **阅读设置** → 找到「分栏排版」设置（支持 **自动 / 单页 / 双页**，默认「自动」横屏即双页并排、竖屏单页）。
- **正文列宽自由调节**：阅读设置中新增 **「iPad 最大列宽」滑块（`600pt – 1000pt`，默认 `760pt`）**，按个人眼距调出最舒服的版心宽度。
- **外接键盘翻页快捷键**：连接妙控键盘或蓝牙键盘后，在网文/TXT 与 EPUB 阅读页均支持 **`←` / `→` / `↑` / `↓` / `Space（空格）`** 丝滑翻页（在搜索框、编辑书源、设置中输入文字时会自动放行，绝不抢占输入）。

---

### 🎵 2. 洛雪音乐（LX Music iPad 加强版）

#### ① 通过 iPad「文件」App 安全导入自定义 JS 音源
1. 将你自备的洛雪 `.js` 自定义音源文件保存到 iPad 的 **「文件」App**（比如“我的 iPad”或 iCloud 云盘任意文件夹；也可以通过微信/QQ/隔空投送选「存储到“文件”」）。
2. 打开洛雪音乐 → 进入 **「设置 → 自定义源管理」** → 点击 **「导入」**。
3. 在适配好的 iPad 弹出卡片窗口（FormSheet）中选中你的 `.js` 文件，导入后**勾选启用**该音源即可搜歌与播放！

#### ② 歌单导入与电脑多端同步
- **导入导出歌单**：在设置 → 备份与恢复中，可直接导入/导出洛雪标准的 **`.lxmc` 歌单文件** 或完整 **`.bin` 备份文件**，也可在 iPad「文件」App 的“我的 iPad → LX Music”文件夹里直接拷贝管理。
- **与 Windows 电脑实时同步**：若你在 Windows 电脑上也在用洛雪桌面版，可在局域网或自建服务器开启官方 `lx-music-sync-server`，在 iPad 洛雪设置 → 数据同步里填入地址和连接码即可双向同步全部收藏歌单。

#### ③ iPad 专属大屏、混音与快捷键用法
- **原生 iPad 全屏与分屏**：已解锁原生 iPad 设备支持与四方向旋转，支持 **分屏（Split View）、侧拉（Slide Over）、台前调度（Stage Manager）**。宽度 ≥700pt（包括 iPad 竖屏和宽分屏）均自动切换为**左侧导航栏 + 双栏播放视图**，整体字体和按钮缩放已针对大屏限幅优化，视觉精致不臃肿。
- **后台播放与混音开关**：
  - **默认模式（音频焦点开启）**：锁屏大封面、控制中心切歌、蓝牙耳机/AirPods 线控、AirPlay 投送 **100% 稳定满血**。
  - **边看视频/边玩游戏边听歌（混音模式）**：如果你希望刷小红书/打游戏时不打断洛雪背景音乐，进入洛雪 **设置 → 播放设置**，关闭 **「音频焦点管理（处理音频焦点）」** 开关即可启用 iOS 混音模式（⚠️ 开启混音时按 iOS 系统机制锁屏播控会交还给前台媒体，想恢复锁屏切歌再把开关打开即可）。
- **外接键盘快捷键**：
  - `Space（空格键）`：播放 / 暂停
  - `⌘ (Command) + →`：下一首
  - `⌘ (Command) + ←`：上一首
  - *(在搜索框等任意输入框打字时自动禁用快捷键，绝不干扰输入)*

---

## 四、常见报错速查排雷表

| 遇到的现象 / 报错 | 原因 | 一键解决办法 |
| :--- | :--- | :--- |
| **SideStore 刷新提示 `Failed to Refresh` / `Minimuxer` 错误** | `LocalDevVPN` 未连上，或与其他常驻 VPN / 广告拦截 DNS 冲突 | 1. 确认已连 Wi-Fi；<br>2. 打开 `LocalDevVPN` 断开重连一次，确保状态栏出现 `VPN`；<br>3. 临时关闭其他代理/去广告 VPN，彻底杀掉 SideStore 后台重开再刷新。 |
| **SideStore 登录或刷新报错 `-80045` / `503` / Anisette 超时** | 默认公共 Anisette 签名服务器拥堵或国内直连超时 | 进入 SideStore **Settings → Anisette Server** 切换其他内置公共节点（如 `jkcoxson`、`Macley` 等），或在顺畅网络环境下重试。 |
| **国内打开源链接或下载 `.ipa` 特别慢 / 超时** | 国内直连 `github.com` / `raw.githubusercontent.com` 偶尔波动 | 切换顺畅网络重试；或先用电脑/浏览器下载好 `.ipa` 发到 iPad「文件」App，打开 SideStore 点左上角 `+` 直接本地安装 `.ipa`。 |
| **提示 `Error 1009`（10 个 App ID 超限）** | 你在同一个 Apple ID 下额外装了带很多小组件/扩展的其他第三方 IPA | 我们这两款包均严格 **0 扩展（总计仅占 4/10）**。安装其他第三方 IPA 时记得在弹窗选 **Remove App Extensions**；已有 App ID 满 7 天后会自动释放。 |
| **Windows `iloader` 或 `Sideloadly` 识别不到 iPad** | 装了微软商店版 iTunes/Apple 设备，或数据线仅支持充电 | 卸载微软商店版 Apple 软件 → 改装 **Apple 官网独立安装包版 iTunes** → 重启电脑 → 换原装/数据线并重新在 iPad 点「信任」。 |
| **忘记续签超过 7 天，App 点不开闪退了，数据会丢吗？** | 免费描述文件 7 天到期失效（**数据完好无损！**） | ⚠️ **千万不要卸载 App！** 直接连 Wi-Fi 开 `LocalDevVPN` 进 SideStore 点刷新即可恢复；若连 SideStore 本身也过期打不开，插一次 Windows 用 `iloader` 原地重装一次 SideStore，原有书架和歌单全部都在！ |
| **iPad 跨大版本系统升级（如 iPadOS 18 → 26）后 SideStore 无法刷新** | 大版本升级重置了设备 lockdown 配对状态 | 插一次 Windows 电脑，打开 `iloader` 重新推送一次 pairing file（耗时 1 分钟，无需删任何 App）。 |
