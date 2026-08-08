# Kevin's Legit GitHub Sideload — Sidestore/AltStore Source

A curated **AltStore / SideStore** source that only lists **100% open-source iOS apps** whose `.ipa` is published directly on **GitHub Releases**. No piracy, no repacks, no sideloaded tweaks.

> Every `downloadURL` in `source.json` points straight to the upstream repo's release asset (verified 2026-08-08 with `HEAD 200`).

## Quick add

1. Host `source.json` on any HTTPS URL (GitHub Pages, Gist, Cloudflare R2, etc.).
   - Example GitHub Pages URL: `https://kevin.github.io/Sideload-Sources/source.json`
   - Raw gist URL also works as long as it serves `application/json` over HTTPS.
2. On iPhone open **SideStore** (or **AltStore**) → **Settings → Sources → Add Source** → paste the URL.
3. Browse the **Apps/Browse** tab — all 11 apps will appear for one-tap install/refresh.

> Tip: SideStore/AltStore caches the source. After you push an update to `source.json`, users pull-to-refresh the Sources screen to fetch it.

## What's included (11 apps)

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

All sizes/URLs were HEAD-checked; `Content-Length` matches the `size` field in `source.json`.

## Inclusion criteria

An app is added only if it meets **all** of:
1. Public GitHub repo
2. OSI-approved license (`LICENSE` file)
3. Tagged **GitHub Release** with an `.ipa` asset (not just source)
4. Not a piracy/tweaked client (no YouTube/Spotify++ etc.)

**Excluded on purpose:** RetroArch (no iOS `.ipa` on Releases), Flycast (Android/AppImage only), ScummVM (no iOS IPA artifact), a-shell (no IPA), dolphin-emu (no iOS IPA on latest).

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
Sideload-Sources/
  source.json   ← add this URL to SideStore/AltStore
  README.md     ← this file
```

## Credits & provenance

Bundle IDs were verified from `Info.plist` / `project.pbxproj` / `*.xcconfig` on each repo's default branch. Icons point to each org's GitHub avatar (replace with hosted icons if you prefer). Upstream wikis: Provenance https://wiki.provenance-emu.com · UTM https://docs.getutm.app
