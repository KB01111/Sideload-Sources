# Kevin's Legit GitHub Sideload — Sidestore/AltStore Source

A curated **AltStore / SideStore** source of iOS apps whose `.ipa` is published directly on **GitHub Releases**.

- **Core 11**: 100% open-source, OSI-licensed (Delta/Provenance/UTM/PPSSPP/etc.)
- **New 13 (Aug 2026)**: newer / SwiftUI + tweaked / **AppDB** value picks — every `.ipa` is the project's official GitHub Release artifact (no repacked piracy).

> Every `downloadURL` points straight to the upstream GitHub Release asset (all 24 verified `HEAD 200` on 2026-08-08).

## Quick add — LIVE on GitHub Pages

**Source URL (paste in SideStore/AltStore):**
```
https://kb01111.github.io/Sideload-Sources/source.json
```
One-tap install links: [Add to SideStore](sidestore://source?url=https://kb01111.github.io/Sideload-Sources/source.json) · [Add to AltStore](altstore://source?url=https://kb01111.github.io/Sideload-Sources/source.json)

Landing page: https://kb01111.github.io/Sideload-Sources/ · Repo: https://github.com/KB01111/Sideload-Sources

1. On iPhone open **SideStore** (or **AltStore**) → **Settings → Sources → Add Source** → paste the URL above (or tap the one-tap link on your phone).
2. Browse the **Apps/Browse** tab — all 24 apps appear for one-tap install/refresh.

> Tip: SideStore/AltStore caches the source. After you push an update to `source.json`, users pull-to-refresh the Sources screen to fetch it.

## What's included (24 apps — 16 + 8 new including AppDB)

| App | Bundle ID | Version | What it is | License |
|---|---|---|---|---|
| **Delta** | `com.rileytestut.Delta` | 1.6 (2024-07-11) | Retro emulator (NES/SNES/N64/GB/GBA/DS) | AGPL-3.0 |
| **Provenance** | `org.provenance-emu.provenance` | 3.3.0 (2026-03-14) | Multi-system frontend (Atari/Nintendo/Sega/Sony/…) | GPL-2.0-ish |
| **UTM** | `com.utmapp.UTM` | 4.7.5 (2026-01-03) | QEMU VMs for iOS (needs JIT) | Apache-2.0 |
| **UTM SE** | `com.utmapp.UTM-SE` | 4.7.5 | UTM Slow Edition — no JIT needed | Apache-2.0 |
| **PPSSPP** | `org.ppsspp.ppsspp-free` | 1.20.4 (2026-05-16) | PSP emulator | GPL-2.0 |
| **iTorrent** | `com.xitrix.iTorrent2` | 2.2.0 (2026-07-19) | Native torrent client | MIT |
| **Feather** | `thewonderofyou.Feather` | 2.9.0 (2026-07-05) | On-device IPA signer/installer | GPL-3.0 |
| **LiveContainer** | `com.kdt.livecontainer` | 3.8.0 (2026-07-17) | Run IPAs without installing | AGPL-3.0 |
| **SideStore** | `com.SideStore.SideStore` | 0.6.3 (2026-05-05) | AltStore fork — no AltServer | AGPL-3.0 |
| **iSH** | `app.ish.iSH` | 494 (2023-05-20) | Alpine Linux shell via x86 emulation | BSD |
| **StikDebug** | `com.stik.stikdebug` | 3.1.9 (2026-08-01) | On-device JIT/debugger for iOS 17.4+ | AGPL-3.0 |
| **Spotube** ✨ | `oss.krtirtho.spotube` | 5.1.2 (2026-06-05) | Spotify frontend — no premium needed (Flutter/SwiftUI) | GPL-ish |
| **BHTwitter** ✨ tweaked | `com.atebits.Tweetie2` | 4.4 (2025-05-13) | Twitter/X tweaked — ad block, downloads, premium | Theos tweak |
| **PojavLauncher** ✨ | `net.kdt.pojavlauncher` | 2.2 (2023-05-06) | Minecraft Java Edition on iOS | GPL-3.0 |
| **LBox** ✨ SwiftUI | `Lolendor.LBox` | 1.2 (2025-12-08) | SwiftUI LiveContainer companion — browse/install IPAs | MIT |
| **Apollo (Patched)** ✨ tweaked | `com.christianselig.Apollo` | 1.15.11-0.1.0 (2026-02-18) | Reddit Apollo revived — BYO API key | GPL-3.0 |
| **AppDB** ✨ | `it.ned.appdb-ios` | 1.1.6 (2023-08-24) | Full client for appdb.to — sideload DB | MIT |
| **Cowabunga** | `com.leemin.Cowabunga` | 10.3.2 (2023-05-29) | MacDirtyCow toolbox (iOS 14-16.1.2) | GPL-3.0 |
| **Misaka** | `com.straighttamago.misaka` | 8.2.4 (2024-01-20) | KFD & MDC customisation (iOS/tvOS) | MIT |
| **Yattee** | `stream.yattee.app` | 1.5.1 (2024-01-28) | Privacy YouTube player (iOS/tvOS) | AGPL-3.0 |
| **Paperback** ✨ | `com.paperback.ios` | 0.8.11-r2 (2025-05-20) | Manga reader — extensions & tracking | — |
| **DebToIPA** | `net.sourceloc.DebToIPA` | 1.1.1 (2022-10-18) | Convert .deb → .ipa on-device (SwiftUI) | GPL-3.0 |
| **ModMyIPA** | `com.powen.ModMyIPA` | 1.0.2 (2022-10-26) | Duplicate any IPA (multi-install) | — |
| **Azula** | `com.paisseon.Azula` | 1.0.1 (2023-03-16) | Inject dylibs into IPAs on-device | AGPL-3.0 |

✨ = Aug 2026 value picks. All 24 sizes/URLs HEAD-checked.

## Inclusion criteria

Core 11: **all** of (1) public GitHub (2) OSI license (3) tagged Release with `.ipa` (4) not piracy.

New 5 expand toward **value/feature**: SwiftUI-native apps (LBox, Spotube) and reputable **tweaked/patcher** IPAs where the patcher is open-source and the sideloaded IPA is the project's official Release artifact (BHTwitter-sideloaded.ipa, ApolloPatcher 1.15.11). YouTube/Spotify++ style IPAs that publish no Release `.ipa` remain excluded.

**Excluded on purpose (no GH Release .ipa):** RetroArch, Flycast (APK/appx only), ScummVM, a-shell, uYouPlus/uYouEnhanced/YTLitePlus (no IPA artifact — need local build), EeveeSpotify (DMCA 451), TrollStore (deb/tar only).

## Updating the source

```powershell
# check latest releases
gh api repos/RileyTestut/Delta/releases/latest --jq "{tag:.tag_name,date:.published_at,assets:[.assets[].name]}"
gh api repos/utmapp/UTM/releases/latest --jq "{tag:.tag_name,assets:[.assets[].name]}"
# bump version/size/downloadURL in source.json, validate:
Get-Content source.json -Raw | ConvertFrom-Json | ForEach-Object { "apps=$($_.apps.Count) OK" }
# HEAD-check every URL:
Get-Content source.json -Raw | ConvertFrom-Json | ForEach-Object { $_.apps | ForEach-Object { Invoke-WebRequest $_.downloadURL -Method Head -UseBasicParsing | Select-Object StatusCode,Headers } }
```

## File layout

```
Sideload-Sources/                ← https://github.com/KB01111/Sideload-Sources
  source.json   ← https://kb01111.github.io/Sideload-Sources/source.json (add THIS url)
  index.html    ← https://kb01111.github.io/Sideload-Sources/ (tap-to-add landing page)
  README.md     ← this file
```

## Credits & provenance

Bundle IDs were verified from `Info.plist` / `project.pbxproj` / `*.xcconfig` on each repo's default branch. Icons point to each org's GitHub avatar (replace with hosted icons if you prefer). Upstream wikis: Provenance https://wiki.provenance-emu.com · UTM https://docs.getutm.app
