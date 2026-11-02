# Kevin's GitHub Sideload Source

A SideStore/AltStore catalog of iOS apps whose install packages are published as first-party GitHub Release assets. It now contains **31 entries**. Every package link goes directly to its upstream release asset; there are no repacked IPAs.

The latest relevant upstream IPA is listed. Alpha, beta, nightly and automated daily builds are marked **PRE-RELEASE**. Where upstream changes a bundle ID, the preview is listed separately rather than presented as an update to the stable app. Read each app description and minimum iOS version before installing.

## Add the source

Use this URL in SideStore or AltStore:

```text
https://kb01111.github.io/Sideload-Sources/source.json
```

In SideStore, open **Settings → Sources → Add Source** and paste the URL. After source changes are published, refresh the Sources screen.

## Catalog

| App | Bundle ID | Version | Description |
|---|---|---|---|
| Delta | `com.rileytestut.Delta` | [1.6](https://github.com/RileyTestut/Delta/releases/tag/v1.6) | Retro emulator for NES, SNES, N64, Game Boy, GBA and DS. |
| Provenance | `org.provenance-emu.provenance` | [3.3.0](https://github.com/Provenance-Emu/Provenance/releases/tag/3.3.0) | Multi-system emulator frontend; stable build. |
| Provenance Alpha | `com.provenance-emu.provenance.alpha` | [alpha, b6069a2](https://github.com/Provenance-Emu/Provenance/releases/tag/alpha) | Preview build from develop; separate bundle ID, NoExtensions IPA. |
| UTM | `com.utmapp.UTM` | [5.0.8](https://github.com/utmapp/UTM/releases/tag/v5.0.8) | QEMU virtual machines; HV build requires JIT; iOS 15+. |
| UTM SE | `com.utmapp.UTM-SE` | [5.0.8](https://github.com/utmapp/UTM/releases/tag/v5.0.8) | Slow Edition VM app; no JIT required; iOS 15+. |
| PPSSPP | `org.ppsspp.ppsspp-free` | [1.20.4](https://github.com/hrydgard/ppsspp/releases/tag/v1.20.4) | PSP emulator. |
| Pocket8 | `com.jevon.pocket8` | [1.6.2](https://github.com/jevonlipsey/pico-ios/releases/tag/v1.6.2) | PICO-8 cartridge player; provide your own cartridges. |
| iTorrent | `com.xitrix.iTorrent2` | [2.2.0](https://github.com/XITRIX/iTorrent/releases/tag/v2.2.0-1) | Native torrent client. |
| Feather | `thewonderofyou.Feather` | [2.9.0](https://github.com/claration/Feather/releases/tag/v2.9.0) | On-device IPA signer and installer. |
| LiveContainer | `com.kdt.livecontainer` | [3.8.11 nightly](https://github.com/LiveContainer/LiveContainer/releases/tag/nightly) | PRE-RELEASE; run apps in a container; SideStore/AltStore companion required. |
| SideStore | `com.SideStore.SideStore` | [0.7.0-alpha](https://github.com/SideStore/SideStore/releases/tag/0.7.0-alpha) | PRE-RELEASE; upstream says this fixes the 503 sign-in issue in 0.6.4 and earlier. |
| iSH | `app.ish.iSH` | [1.3.3, build 813](https://github.com/ish-app/ish/releases/tag/builds/813) | PRE-RELEASE automated daily build; Alpine Linux shell. |
| StikDebug | `com.stik.stikdebug` | [3.2.0](https://github.com/StiKDebug/StikDebug/releases/tag/3.2.0) | On-device pairing, debugger and JIT utility; iOS 17.4+. |
| Roam Control | `com.roamcontrol` | [0.9.9, build 105](https://github.com/seanhowarthdev/Roam-Control/releases/tag/v0.9.9) | Location-testing utility; iOS 27+, Developer Mode and LocalDevVPN required. |
| Spotube | `oss.krtirtho.spotube` | [5.1.2](https://github.com/team-spotube/spotube/releases/tag/v5.1.2) | Stable open-source music client. |
| Spotube 6 Beta | `org.spotube.spotube.Spotube` | [6.0.0-beta.0](https://github.com/team-spotube/spotube/releases/tag/v6.0.0-beta.0) | PRE-RELEASE Compose rewrite; new bundle ID; iOS 18.2+. |
| BHTwitter | `com.atebits.Tweetie2` | [4.4](https://github.com/BandarHL/BHTwitter/releases/tag/4.4) | Tweaked X/Twitter client. |
| PojavLauncher | `net.kdt.pojavlauncher` | [2.2](https://github.com/PojavLauncherTeam/PojavLauncher_iOS/releases/tag/v2.2) | Minecraft Java launcher for iOS. |
| LBox | `Lolendor.LBox` | [1.2](https://github.com/Lolendor/LBox/releases/tag/v1.2) | LiveContainer source browser and companion. |
| Apollo Patched | `com.christianselig.Apollo` | [1.15.11-0.1.0](https://github.com/ichitaso/ApolloPatcher/releases/tag/v0.1.0) | Apollo with configurable Reddit API credentials. |
| Cowabunga | `com.leemin.Cowabunga` | [10.3.2](https://github.com/leminlimez/Cowabunga/releases/tag/v10.3.2) | MacDirtyCow customization tool for supported iOS versions. |
| Misaka | `com.straighttamago.misaka` | [8.2.4](https://github.com/straight-tamago/misaka/releases/tag/8.2.4) | KFD/MDC customization tool. |
| Yattee | `stream.yattee.app` | [2.0.0-beta.278](https://github.com/yattee/yattee/releases/tag/2.0.0-beta.278) | PRE-RELEASE privacy-focused YouTube player; iOS 18+. |
| YouProEXTRA / YTKACE | `com.google.ios.youtube` | [YouProEXTRA 6.0-b2](https://github.com/mrdrvt99/YouProEXTRA/releases/tag/ytl-ipa6), YouTube 21.43.5 | The latest entry is an unofficial build that the uploader labels cracked; iOS 17+. YTKACE 1.1.4 iOS 17+ and iOS 16 builds remain available in the version list. |
| Paperback | `com.paperback.ios` | [0.8.11-r2](https://github.com/Paperback-iOS/app/releases/tag/v0.8.11-r2) | Manga and comic reader. |
| DebToIPA | `net.sourceloc.DebToIPA` | [1.1.1](https://github.com/sourcelocation/DebToIPA/releases/tag/1.1.1) | Convert `.deb` packages to IPA on-device. |
| ModMyIPA | `com.powen.ModMyIPA` | [1.0.2](https://github.com/powenn/ModMyIPA/releases/tag/1.0.2) | Change an IPA's bundle identifier to install a separate copy. |
| Azula | `com.paisseon.Azula` | [1.0.1](https://github.com/Paisseon/Azula/releases/tag/v1.0.1) | Inject dynamic libraries into IPAs on-device. |
| AppDB | `it.ned.appdb-ios` | [1.1.6](https://github.com/n3d1117/appdb/releases/tag/v1.1.6) | Client for the appdb.to catalog. Review the content and source you choose. |
| AerioTV | `app.molinete.aerio` | [1.8.44](https://github.com/jonzey231/AerioTV/releases/tag/v1.8.44) | IPTV player for user-configured playlists and servers; iOS 18+. |
| Mirarr | `com.example.Mirarr` | [3.3.3](https://github.com/mirarr-app/mirarr/releases/tag/3.3.3) | Cross-platform movie and TV app; use authorized sources only. |

## Modified apps and compatibility notes

The YouTube listing uses one bundle ID and offers multiple build variants through the version selector: the latest YouProEXTRA / YouTubePlus 6.0-b2 build (YouTube 21.43.5, iOS 17+), plus YTKACE 1.1.4 builds for iOS 17+ and iOS 16. The YouProEXTRA release page labels its build cracked and says no subscription is required; this is an unofficial community build. All variants use YouTube’s bundle ID and cannot coexist under separate listings or with another copy carrying that ID. BHTwitter and Apollo Patched are also modified clients already listed above.


SideStore 0.7.0-alpha is listed because the upstream release page says 0.6.4 and earlier have a sign-in failure, while this alpha addresses the 503 issue. iSH build 813, LiveContainer nightly 3.8.11, Spotube 6 beta, Yattee 2.0 beta, and Provenance Alpha are explicitly labelled previews. Provenance Alpha has a separate bundle ID and can coexist with stable Provenance. It uses the NoExtensions IPA to reduce the number of app identifiers registered during free signing.

Pocket8 needs cartridges supplied by the user. AerioTV needs a user-configured server or playlist; the catalog does not include media. Roam Control is a developer/testing tool and requires iOS 27 or later, Developer Mode and LocalDevVPN. These requirements are shown in the source app descriptions as well.

## Maintenance

App versions, sizes, bundle IDs and minimum iOS requirements are taken from the upstream release metadata and, where practical, the IPA's `Info.plist`. Each `downloadURL` should point to the project's own GitHub Release asset. Before publishing a catalog refresh, validate the JSON and send a `HEAD` request to every package URL.

## TrollStore-only apps

TrollRecorder is not included because its `.tipa` package requires TrollStore and cannot be installed through SideStore/AltStore. TrollStore-specific packages are kept out of this SideStore source.
