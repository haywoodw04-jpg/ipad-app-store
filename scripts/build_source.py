#!/usr/bin/env python3
"""Build SideStore / AltStore Source v2 JSON for haywoodw04-jpg/ipad-app-store.

Queries the latest published GitHub Releases of:
  - haywoodw04-jpg/lx-music-ipad
  - haywoodw04-jpg/legado-ipad

For each release asset (*.ipa), downloads the unsigned IPA into a temporary
directory, verifies binary integrity & SideStore safety invariants:
  - Exactly one Payload/*.app/Info.plist
  - 0 _CodeSignature entries
  - 0 embedded.mobileprovision files
  - 0 .appex app extensions (strictly 1 App ID per app)
  - UIDeviceFamily contains both 1 (iPhone) and 2 (iPad)
  - UIBackgroundModes contains "audio"
  - Exact byte size match and SHA-256 checksum computation/verification

Then emits a standards-compliant SideStore / AltStore Source v2 JSON file.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import plistlib
import re
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
import zipfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


HUB_REPOSITORY = "haywoodw04-jpg/ipad-app-store"
HUB_BRANCH = "main"


@dataclass(frozen=True)
class AppSpec:
    key: str
    repository: str
    display_name: str
    developer_name: str
    subtitle: str
    localized_description: str
    icon_filename: str
    tint_color: str
    category: str
    expected_bundle_id: str | None = None
    forbidden_privacy_keys: tuple[str, ...] = ()


APP_SPECS: tuple[AppSpec, ...] = (
    AppSpec(
        key="lx-music-ipad",
        repository="haywoodw04-jpg/lx-music-ipad",
        display_name="洛雪音乐",
        developer_name="haywoodw04-jpg",
        subtitle="开源聚合音乐播放器 · iPad 原生大屏适配版",
        localized_description=(
            "基于开源项目 lx-music-mobile (ios-adaptation) 深度适配 iPad 的纯净未签名版。"
            "支持原生 iPad 四方向全屏、分屏/侧拉/台前调度、横竖屏侧栏与双栏播放页、"
            "iPad 缩放优化、按需音频混音开关、FormSheet 音源导入及外接键盘快捷键（空格播停、Cmd+左右切歌）。"
            "本应用为纯净播放器空壳，不含任何内置音源、遥测或广告，自定义 JS 音源需自行导入。"
        ),
        icon_filename="lx-music-ipad.png",
        tint_color="#18A058",
        category="entertainment",
        expected_bundle_id="cn.toside.music.mobile",
        forbidden_privacy_keys=("NSLocationWhenInUseUsageDescription",),
    ),
    AppSpec(
        key="legado-ipad",
        repository="haywoodw04-jpg/legado-ipad",
        display_name="小浣熊阅读",
        developer_name="haywoodw04-jpg",
        subtitle="兼容 Legado 书源 · iPad 大屏双页与 WebDAV 加强版",
        localized_description=(
            "基于开源项目 Aminark/legado-ios 深度适配 iPad 的纯净未签名版。"
            "支持原生 iPad 侧边栏导航、EPUB 横屏双页并排阅读、正文最大列宽滑块（600–1000pt）、"
            "外接键盘方向键与空格翻页、兼容安卓 Legado 格式的 WebDAV 备份恢复（密码强制加密存储于 iOS Keychain），"
            "并默认开启严格 HTTPS 证书校验。本应用不提供或内置任何书源与书库，书源需自行导入。"
        ),
        icon_filename="legado-ipad.png",
        tint_color="#315C50",
        category="utilities",
        expected_bundle_id="com.epiboly.legado",
        forbidden_privacy_keys=(),
    ),
)


def resolve_github_token(explicit_token: str | None = None) -> str | None:
    if explicit_token:
        return explicit_token.strip()
    for env_key in ("GITHUB_TOKEN", "GH_TOKEN"):
        val = os.environ.get(env_key, "").strip()
        if val:
            return val
    try:
        out = subprocess.check_output(
            ["gh", "auth", "token"],
            stderr=subprocess.DEVNULL,
            text=True,
            timeout=5,
        ).strip()
        return out or None
    except Exception:
        return None


def http_get_json(url: str, token: str | None) -> Any:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "ipad-app-store-source-builder/1.0",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"GitHub API error {exc.code} for {url}: {body[:300]}") from exc


def download_file(url: str, dest: Path, token: str | None) -> None:
    headers = {"User-Agent": "ipad-app-store-source-builder/1.0"}
    if token and "api.github.com" in url:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=180) as resp, dest.open("wb") as fh:
        while True:
            chunk = resp.read(1024 * 256)
            if not chunk:
                break
            fh.write(chunk)


def compute_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        while True:
            chunk = fh.read(1024 * 256)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def inspect_unsigned_ipa(ipa_path: Path, spec: AppSpec) -> dict[str, Any]:
    with zipfile.ZipFile(ipa_path) as archive:
        names = archive.namelist()
        info_paths = [
            name for name in names if re.fullmatch(r"Payload/[^/]+\.app/Info\.plist", name)
        ]
        if len(info_paths) != 1:
            raise ValueError(
                f"{ipa_path.name}: expected exactly 1 Payload/*.app/Info.plist, found {info_paths}"
            )

        code_sigs = [n for n in names if "/_CodeSignature/" in n]
        provisions = [n for n in names if n.endswith("/embedded.mobileprovision")]
        appexs = [n for n in names if ".appex/" in n or n.endswith(".appex")]
        if code_sigs:
            raise ValueError(f"{ipa_path.name}: unexpected _CodeSignature found ({code_sigs[0]})")
        if provisions:
            raise ValueError(f"{ipa_path.name}: unexpected embedded.mobileprovision found")
        if appexs:
            raise ValueError(f"{ipa_path.name}: unexpected app extension (.appex) found ({appexs[0]})")

        info = plistlib.loads(archive.read(info_paths[0]))

    for key in ("CFBundleIdentifier", "CFBundleShortVersionString", "CFBundleVersion", "MinimumOSVersion"):
        val = info.get(key)
        if not isinstance(val, str) or not val or "$(" in val:
            raise ValueError(f"{ipa_path.name}: invalid or unresolved Info.plist key {key}={val!r}")

    if spec.expected_bundle_id and info["CFBundleIdentifier"] != spec.expected_bundle_id:
        raise ValueError(
            f"{ipa_path.name}: bundle id mismatch: expected {spec.expected_bundle_id}, "
            f"got {info['CFBundleIdentifier']}"
        )

    device_family = info.get("UIDeviceFamily", [])
    if not ({1, 2}.issubset(set(device_family))):
        raise ValueError(
            f"{ipa_path.name}: UIDeviceFamily must include both 1 and 2 for native iPad support, "
            f"got {device_family!r}"
        )

    bg_modes = info.get("UIBackgroundModes", [])
    if "audio" not in bg_modes:
        raise ValueError(f"{ipa_path.name}: UIBackgroundModes missing 'audio': {bg_modes!r}")

    for forbidden in spec.forbidden_privacy_keys:
        if forbidden in info:
            raise ValueError(f"{ipa_path.name}: forbidden Info.plist key still present: {forbidden}")

    privacy = {
        k: v
        for k, v in sorted(info.items())
        if isinstance(k, str)
        and k.startswith("NS")
        and "UsageDescription" in k
        and isinstance(v, str)
        and v.strip()
    }

    return {
        "bundleIdentifier": info["CFBundleIdentifier"],
        "displayName": info.get("CFBundleDisplayName") or info.get("CFBundleName") or spec.display_name,
        "version": info["CFBundleShortVersionString"],
        "buildVersion": info["CFBundleVersion"],
        "minOSVersion": info["MinimumOSVersion"],
        "deviceFamily": list(device_family),
        "requiresFullScreen": info.get("UIRequiresFullScreen", False),
        "privacy": privacy,
    }


def pick_ipa_asset(release: dict[str, Any]) -> dict[str, Any] | None:
    assets = [
        a
        for a in release.get("assets", [])
        if a.get("name", "").lower().endswith(".ipa") and a.get("state") == "uploaded"
    ]
    if not assets:
        return None
    unsigned = [a for a in assets if "unsigned" in a["name"].lower()]
    if len(unsigned) == 1:
        return unsigned[0]
    if len(assets) == 1:
        return assets[0]
    raise ValueError(
        f"Ambiguous .ipa assets in release {release.get('tag_name')}: {[a['name'] for a in assets]}"
    )


def validate_iso_date(date_str: str) -> str:
    parsed = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError(f"Release published_at must include timezone: {date_str!r}")
    return date_str


def build_app_entry(
    spec: AppSpec,
    token: str | None,
    hub_repo: str,
    hub_branch: str,
    max_versions: int,
    work_dir: Path,
    local_override: Path | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    raw_base = f"https://raw.githubusercontent.com/{hub_repo}/{hub_branch}"
    icon_url = f"{raw_base}/icons/{spec.icon_filename}"

    releases_url = f"https://api.github.com/repos/{spec.repository}/releases?per_page=15"
    releases = http_get_json(releases_url, token)
    if not isinstance(releases, list):
        raise RuntimeError(f"Unexpected releases payload for {spec.repository}")

    published = [
        r
        for r in releases
        if not r.get("draft") and not r.get("prerelease") and pick_ipa_asset(r) is not None
    ]
    if not published:
        raise RuntimeError(f"No published stable release with an uploaded .ipa found in {spec.repository}")

    versions: list[dict[str, Any]] = []
    latest_meta: dict[str, Any] | None = None
    latest_summary: dict[str, Any] | None = None

    for idx, release in enumerate(published[:max_versions]):
        asset = pick_ipa_asset(release)
        assert asset is not None
        tag_name = release["tag_name"]
        pub_date = validate_iso_date(release["published_at"])
        download_url = asset["browser_download_url"]
        expected_size = int(asset["size"])

        if idx == 0 and local_override is not None:
            ipa_file = local_override
        else:
            ipa_file = work_dir / f"{spec.key}-{tag_name}-{asset['name']}"
            download_file(download_url, ipa_file, token)

        actual_size = ipa_file.stat().st_size
        if actual_size != expected_size:
            raise ValueError(
                f"{spec.repository} {tag_name}: downloaded size {actual_size} != asset size {expected_size}"
            )

        sha256 = compute_sha256(ipa_file)
        gh_digest = asset.get("digest")
        if gh_digest and gh_digest != f"sha256:{sha256}":
            raise ValueError(
                f"{spec.repository} {tag_name}: SHA-256 mismatch: GitHub={gh_digest}, computed=sha256:{sha256}"
            )

        ipa_meta = inspect_unsigned_ipa(ipa_file, spec)
        description = (release.get("body") or release.get("name") or tag_name).strip()

        version_obj = {
            "version": ipa_meta["version"],
            "buildVersion": ipa_meta["buildVersion"],
            "date": pub_date,
            "localizedDescription": description,
            "downloadURL": download_url,
            "size": actual_size,
            "minOSVersion": ipa_meta["minOSVersion"],
            "sha256": sha256,
        }
        versions.append(version_obj)

        if idx == 0:
            latest_meta = ipa_meta
            latest_summary = {
                "key": spec.key,
                "name": spec.display_name,
                "repository": spec.repository,
                "tag": tag_name,
                "releaseURL": release["html_url"],
                "bundleIdentifier": ipa_meta["bundleIdentifier"],
                "version": ipa_meta["version"],
                "buildVersion": ipa_meta["buildVersion"],
                "minOSVersion": ipa_meta["minOSVersion"],
                "downloadURL": download_url,
                "assetName": asset["name"],
                "size": actual_size,
                "sha256": sha256,
                "publishedAt": pub_date,
                "privacy": ipa_meta["privacy"],
            }

    assert latest_meta is not None and latest_summary is not None
    latest_ver = versions[0]

    app_entry = {
        "name": spec.display_name,
        "bundleIdentifier": latest_meta["bundleIdentifier"],
        "developerName": spec.developer_name,
        "subtitle": spec.subtitle,
        "localizedDescription": spec.localized_description,
        "iconURL": icon_url,
        "tintColor": spec.tint_color,
        "category": spec.category,
        "versions": versions,
        # Top-level legacy AltStore / SideStore compatibility fields
        "version": latest_ver["version"],
        "versionDate": latest_ver["date"],
        "versionDescription": latest_ver["localizedDescription"],
        "downloadURL": latest_ver["downloadURL"],
        "size": latest_ver["size"],
        "appPermissions": {
            "entitlements": [],
            "privacy": latest_meta["privacy"],
        },
    }
    return app_entry, latest_summary


def build_source(
    token: str | None,
    hub_repo: str = HUB_REPOSITORY,
    hub_branch: str = HUB_BRANCH,
    max_versions: int = 5,
    local_overrides: dict[str, Path] | None = None,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    raw_base = f"https://raw.githubusercontent.com/{hub_repo}/{hub_branch}"
    overrides = local_overrides or {}

    apps: list[dict[str, Any]] = []
    summaries: list[dict[str, Any]] = []

    with tempfile.TemporaryDirectory(prefix="ipad-source-build-") as tmp:
        work_dir = Path(tmp)
        for spec in APP_SPECS:
            entry, summary = build_app_entry(
                spec=spec,
                token=token,
                hub_repo=hub_repo,
                hub_branch=hub_branch,
                max_versions=max_versions,
                work_dir=work_dir,
                local_override=overrides.get(spec.key),
            )
            apps.append(entry)
            summaries.append(summary)

    source_doc = {
        "name": "iPad 专属双应用源（洛雪 + 阅读）",
        "identifier": "com.haywoodw04.ipad-app-store",
        "subtitle": "洛雪音乐 & 小浣熊阅读 · iPad 深度适配纯净开源源",
        "description": (
            "专为 iPad 打造的纯净开源双应用 SideStore / AltStore 应用源，"
            "收录经源码安全审计、深度适配 iPad 大屏分屏与外接键盘、由 GitHub Actions 自动编译的未签名版本。"
            "每款应用仅占 1 个 App ID，合计 3/3 名额与 4/10 App ID，免 LiveContainer 原生满血运行；"
            "不含任何书源、音源或个人数据。"
        ),
        "sourceURL": f"{raw_base}/source.json",
        "website": f"https://github.com/{hub_repo}",
        "iconURL": f"{raw_base}/icons/hub-icon.png",
        "tintColor": "#2B6CB0",
        "apps": apps,
        "news": [],
    }
    return source_doc, summaries


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("source.json"),
        help="Path to write the generated SideStore / AltStore Source v2 JSON.",
    )
    parser.add_argument(
        "--summary-output",
        type=Path,
        default=None,
        help="Optional path to write machine-readable release summary JSON.",
    )
    parser.add_argument("--hub-repo", default=HUB_REPOSITORY)
    parser.add_argument("--hub-branch", default=HUB_BRANCH)
    parser.add_argument("--max-versions", type=int, default=5)
    parser.add_argument("--token", default=None, help="Optional GitHub token.")
    parser.add_argument(
        "--local-lx-ipa",
        type=Path,
        default=None,
        help="Optional local .ipa path to inspect instead of downloading latest lx-music-ipad asset.",
    )
    parser.add_argument(
        "--local-legado-ipa",
        type=Path,
        default=None,
        help="Optional local .ipa path to inspect instead of downloading latest legado-ipad asset.",
    )
    args = parser.parse_args()

    token = resolve_github_token(args.token)
    overrides: dict[str, Path] = {}
    if args.local_lx_ipa:
        overrides["lx-music-ipad"] = args.local_lx_ipa
    if args.local_legado_ipa:
        overrides["legado-ipad"] = args.local_legado_ipa

    source_doc, summaries = build_source(
        token=token,
        hub_repo=args.hub_repo,
        hub_branch=args.hub_branch,
        max_versions=args.max_versions,
        local_overrides=overrides,
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(source_doc, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    if args.summary_output:
        args.summary_output.parent.mkdir(parents=True, exist_ok=True)
        args.summary_output.write_text(
            json.dumps(summaries, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    print(f"Successfully generated {args.output}")
    for item in summaries:
        mb = item["size"] / (1024 * 1024)
        print(
            f"  - {item['name']} ({item['bundleIdentifier']}) "
            f"v{item['version']} (build {item['buildVersion']}) "
            f"[{mb:.2f} MiB, {item['size']} B] sha256={item['sha256']}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
