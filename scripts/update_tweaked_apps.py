#!/usr/bin/env python3
"""Refresh tracked tweaked-app catalog entries from official GitHub IPA releases.

The updater only tracks projects declared in .github/tweaked-apps.json. It checks
GitHub release metadata every run and downloads an IPA only when its release or
asset fingerprint changes (or when the catalog entry is missing). The IPA's
Info.plist is authoritative for bundle ID, CFBundleShortVersionString, and
MinimumOSVersion; tweak/release tags are never substituted for app versions.
"""
from __future__ import annotations

import fnmatch
import io
import json
import os
import re
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
import zipfile
import plistlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / ".github" / "tweaked-apps.json"
STATE_PATH = ROOT / ".github" / "tweaked-apps-state.json"
SOURCE_PATH = ROOT / "source.json"
USER_AGENT = "Sideload-Sources-upstream-refresh/1.0"
API_ROOT = "https://api.github.com/repos/"
MAX_IPA_BYTES = 600 * 1024 * 1024
HISTORY_PER_REPO = 10
MAX_NEWS_ITEMS = 30


def json_read(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def api_headers() -> dict[str, str]:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": USER_AGENT,
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def get_json(url: str) -> Any:
    request = urllib.request.Request(url, headers=api_headers())
    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read(1000).decode("utf-8", "replace")
        raise RuntimeError(f"GitHub API {exc.code} for {url}: {body}") from exc


def latest_release_and_asset(project: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    url = API_ROOT + urllib.parse.quote(project["repo"], safe="/") + "/releases?per_page=100"
    releases = get_json(url)
    pattern = project["assetGlob"]
    for release in releases:
        if release.get("draft") or release.get("prerelease"):
            continue
        matching = [
            asset for asset in release.get("assets", [])
            if fnmatch.fnmatchcase(asset.get("name", ""), pattern)
            and asset.get("state") == "uploaded"
        ]
        if matching:
            matching.sort(key=lambda asset: asset.get("name", ""))
            # Twitch publishes a no-plugins and plugins IPA; the configured
            # pattern selects the no-plugins asset. Other patterns are exact.
            return release, matching[0]
    raise RuntimeError(f"No stable release IPA matching {pattern!r} found for {project['repo']}")


def ipa_info(download_url: str, expected_size: int, expected_bundle: str) -> tuple[dict[str, Any], int]:
    request = urllib.request.Request(download_url, headers={"User-Agent": USER_AGENT})
    total = 0
    with tempfile.SpooledTemporaryFile(max_size=16 * 1024 * 1024, mode="w+b") as package:
        try:
            with urllib.request.urlopen(request, timeout=180) as response:
                while True:
                    chunk = response.read(1024 * 1024)
                    if not chunk:
                        break
                    total += len(chunk)
                    if total > MAX_IPA_BYTES:
                        raise RuntimeError(f"IPA exceeds safety limit of {MAX_IPA_BYTES} bytes")
                    package.write(chunk)
        except urllib.error.HTTPError as exc:
            raise RuntimeError(f"IPA download returned HTTP {exc.code}: {download_url}") from exc
        if expected_size and total != expected_size:
            raise RuntimeError(f"IPA size mismatch for {download_url}: expected {expected_size}, downloaded {total}")
        package.seek(0)
        try:
            with zipfile.ZipFile(package) as archive:
                plist_paths = [
                    name for name in archive.namelist()
                    if name.startswith("Payload/") and name.count("/") == 2
                    and name.endswith(".app/Info.plist")
                ]
                matches = []
                for plist_path in plist_paths:
                    info = plistlib.loads(archive.read(plist_path))
                    if info.get("CFBundleIdentifier") == expected_bundle:
                        matches.append(info)
        except (zipfile.BadZipFile, plistlib.InvalidFileException) as exc:
            raise RuntimeError(f"Could not read IPA Info.plist for {download_url}: {exc}") from exc
    if len(matches) != 1:
        found = [item.get("CFBundleIdentifier") for item in matches]
        raise RuntimeError(
            f"Expected exactly one app with bundle ID {expected_bundle!r} in {download_url}; "
            f"found {len(matches)} matches {found} among {len(plist_paths)} root apps"
        )
    info = matches[0]
    version = str(info.get("CFBundleShortVersionString", "")).strip()
    min_os = str(info.get("MinimumOSVersion", "")).strip()
    if not version or not min_os:
        raise RuntimeError(f"IPA is missing CFBundleShortVersionString or MinimumOSVersion: {download_url}")
    return info, total


def release_url(repo: str, tag: str) -> str:
    return "https://github.com/" + repo + "/releases/tag/" + urllib.parse.quote(tag, safe="")


def release_date(release: dict[str, Any], asset: dict[str, Any]) -> str:
    published = release.get("published_at") or release.get("created_at") or ""
    asset_updated = asset.get("updated_at") or ""
    return max(published, asset_updated) if asset_updated else published


def version_record(project: dict[str, Any], release: dict[str, Any], asset: dict[str, Any], info: dict[str, Any]) -> dict[str, Any]:
    version = str(info["CFBundleShortVersionString"])
    min_os = str(info["MinimumOSVersion"])
    note = project["description"].format(tag=release.get("tag_name", ""), version=version)
    return {
        "version": version,
        "date": release_date(release, asset),
        "size": int(asset["size"]),
        "downloadURL": asset["browser_download_url"],
        "localizedDescription": note + f" Requires iOS {min_os} or later.",
        "minOSVersion": min_os,
    }


def date_key(version: dict[str, Any]) -> str:
    return str(version.get("date", ""))


def repo_download_prefix(repo: str) -> str:
    return f"https://github.com/{repo}/releases/download/"


def project_version_present(app: dict[str, Any] | None, project: dict[str, Any]) -> bool:
    if not app:
        return False
    prefix = repo_download_prefix(project["repo"])
    return any(v.get("downloadURL", "").startswith(prefix) for v in app.get("versions", []))


def make_news(project: dict[str, Any], group: dict[str, Any], release: dict[str, Any], asset: dict[str, Any], record: dict[str, Any], old_version: str | None) -> dict[str, Any]:
    new_version = record["version"]
    same_version_note = " The IPA's embedded app version is unchanged, so SideStore may not display its normal Update button even though the upstream package changed; refresh the source and reinstall manually if you need this tweak-only rebuild." if old_version == new_version else " SideStore can offer the newer version after the source refresh; you still need to tap its Update button in SideStore."
    identifier = "auto-" + re.sub(r"[^A-Za-z0-9._-]+", "-", project["repo"] + "-" + str(asset["id"]))
    return {
        "title": f"Upstream update: {project['displayName']} {new_version}",
        "identifier": identifier,
        "caption": (
            f"Detected official release {release.get('tag_name', '')} from {project['repo']}. "
            f"The IPA reports app version {new_version} and requires iOS {record['minOSVersion']}. "
            "Catalog metadata was refreshed by the scheduled GitHub Action." + same_version_note
        ),
        "date": release_date(release, asset),
        "tintColor": group["tintColor"],
        "imageURL": group["iconURL"],
        "notify": True,
        "url": release_url(project["repo"], release.get("tag_name", "")),
    }


def source_app(source: dict[str, Any], group: dict[str, Any]) -> dict[str, Any] | None:
    matches = [a for a in source.get("apps", []) if a.get("bundleIdentifier") == group["bundleIdentifier"]]
    if len(matches) > 1:
        raise RuntimeError(f"Duplicate bundleIdentifier in source: {group['bundleIdentifier']}")
    if matches and matches[0].get("name") != group["name"]:
        raise RuntimeError(
            f"Bundle ID {group['bundleIdentifier']} already belongs to {matches[0].get('name')!r}, "
            f"not configured listing {group['name']!r}; refusing to overwrite it"
        )
    return matches[0] if matches else None


def refresh_group(source: dict[str, Any], group: dict[str, Any], project_records: list[tuple[dict[str, Any], dict[str, Any]]]) -> None:
    app = source_app(source, group)
    current_versions = list(app.get("versions", [])) if app else []
    for project, new_record in project_records:
        prefix = repo_download_prefix(project["repo"])
        # Replace the same repo/version record (for example an updated asset
        # under a stable loader-latest tag), otherwise preserve its history.
        current_versions = [
            old for old in current_versions
            if not (old.get("downloadURL", "").startswith(prefix) and old.get("version") == new_record["version"])
        ]
        current_versions.append(new_record)
    # AltStore/SideStore require unique app version strings. If two projects
    # publish identical CFBundleShortVersionString values under this shared
    # bundle ID, retain the more recent package instead of an invalid duplicate.
    current_versions.sort(key=date_key, reverse=True)
    unique: dict[str, dict[str, Any]] = {}
    for version in current_versions:
        unique.setdefault(str(version["version"]), version)
    current_versions = list(unique.values())
    # Bound the catalog history to recent releases; retain at least one per tracked project.
    newest_by_repo: dict[str, dict[str, Any]] = {}
    for project, _ in project_records:
        prefix = repo_download_prefix(project["repo"])
        entries = [v for v in current_versions if v.get("downloadURL", "").startswith(prefix)]
        if entries:
            newest_by_repo[project["repo"]] = max(entries, key=date_key)
    allowed = {id(v) for v in newest_by_repo.values()}
    for version in current_versions:
        if len([v for v in current_versions if id(v) in allowed]) >= HISTORY_PER_REPO * max(1, len(project_records)):
            break
        allowed.add(id(version))
    current_versions = [v for v in current_versions if id(v) in allowed]
    current_versions.sort(key=date_key, reverse=True)
    if not current_versions:
        return
    latest = current_versions[0]
    if app is None:
        app = {
            "name": group["name"],
            "bundleIdentifier": group["bundleIdentifier"],
            "developerName": group["developerName"],
            "subtitle": group["subtitle"],
            "localizedDescription": group["localizedDescription"],
            "iconURL": group["iconURL"],
            "tintColor": group["tintColor"],
            "category": group["category"],
            "appPermissions": {"entitlements": [], "privacy": []},
            "screenshots": [],
        }
        source.setdefault("apps", []).append(app)
    app.update({
        "name": group["name"],
        "bundleIdentifier": group["bundleIdentifier"],
        "developerName": group["developerName"],
        "subtitle": group["subtitle"],
        "localizedDescription": group["localizedDescription"],
        "iconURL": group["iconURL"],
        "tintColor": group["tintColor"],
        "category": group["category"],
        "version": latest["version"],
        "versionDate": latest["date"],
        "versionDescription": latest["localizedDescription"],
        "downloadURL": latest["downloadURL"],
        "size": latest["size"],
        "minOSVersion": latest["minOSVersion"],
        "versions": current_versions,
    })
    app.setdefault("appPermissions", {"entitlements": [], "privacy": []})
    app.setdefault("screenshots", [])


def main() -> int:
    config = json_read(CONFIG_PATH, {})
    source = json_read(SOURCE_PATH, {})
    state = json_read(STATE_PATH, {"projects": {}})
    state.setdefault("projects", {})
    groups = config.get("groups", {})
    projects = config.get("projects", [])
    if not projects or not groups:
        raise RuntimeError("Tracker configuration is missing groups or projects")
    initial_groups = {
        key for key, group in groups.items() if source_app(source, group) is not None
    }
    records_by_group: dict[str, list[tuple[dict[str, Any], dict[str, Any]]]] = {}
    news_items: list[dict[str, Any]] = []
    changed_repos: list[str] = []

    for project in projects:
        release, asset = latest_release_and_asset(project)
        repo = project["repo"]
        old_state = state["projects"].get(repo, {})
        identity = {
            "releaseId": release["id"],
            "tag": release["tag_name"],
            "assetId": asset["id"],
            "assetUpdatedAt": asset.get("updated_at", ""),
        }
        old_identity = {key: old_state.get(key) for key in identity}
        existing_app = source_app(source, groups[project["group"]])
        need_inspection = identity != old_identity or not project_version_present(existing_app, project)

        if need_inspection:
            info, downloaded_size = ipa_info(
                asset["browser_download_url"], int(asset["size"]), project["expectedBundleIdentifier"]
            )
            record = version_record(project, release, asset, info)
            record["size"] = downloaded_size
            prior_version = old_state.get("version")
            if repo in state["projects"] and project["group"] in initial_groups:
                news_items.append(make_news(project, groups[project["group"]], release, asset, record, prior_version))
            state["projects"][repo] = {
                **identity,
                "version": record["version"],
                "minOSVersion": record["minOSVersion"],
                "size": record["size"],
                "downloadURL": record["downloadURL"],
            }
            records_by_group.setdefault(project["group"], []).append((project, record))
            changed_repos.append(repo)
            print(f"Refreshed {repo}: {release['tag_name']} -> IPA {record['version']} (iOS {record['minOSVersion']})")
        else:
            print(f"No change for {repo}: {identity['tag']} asset {identity['assetId']}")

    for group_key, group in groups.items():
        group_projects = [p for p in projects if p["group"] == group_key]
        refresh_group(source, group, records_by_group.get(group_key, []))
        if group_key not in initial_groups and source_app(source, group) is not None:
            # Initial source entries are announced once; later runs do not
            # republish this notice because the group now exists.
            records = records_by_group.get(group_key, [])
            if records:
                newest_project = max(records, key=lambda row: date_key(row[1]))[0]
                latest_record = max((row[1] for row in records), key=date_key)
                latest_release, latest_asset = latest_release_and_asset(newest_project)
                # The initial catalog commit adds a human-readable entry notice
                # separately; no automatic announcement is needed during bootstrap.
                _ = latest_record, latest_release, latest_asset

    if news_items:
        existing_ids = {item.get("identifier") for item in source.get("news", [])}
        source["news"] = [item for item in news_items if item["identifier"] not in existing_ids] + source.get("news", [])
        source["news"] = source["news"][:MAX_NEWS_ITEMS]

    count = len(source.get("apps", []))
    description = source.get("description", "")
    description = re.sub(r"\b\d+ direct upstream GitHub Release IPAs\b", f"{count} direct upstream GitHub Release IPAs", description)
    source["description"] = description

    SOURCE_PATH.write_text(json.dumps(source, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    bundle_ids = [app.get("bundleIdentifier") for app in source.get("apps", [])]
    if len(bundle_ids) != len(set(bundle_ids)):
        raise RuntimeError("Refusing to publish source with duplicate bundleIdentifier values")
    for app in source.get("apps", []):
        versions = [str(item.get("version")) for item in app.get("versions", [])]
        if len(versions) != len(set(versions)):
            raise RuntimeError(f"Duplicate version strings for {app.get('name')}: {versions}")
        if app.get("versions") and app.get("version") != app["versions"][0]["version"]:
            raise RuntimeError(f"Root version must match first version for {app.get('name')}")
    print(f"Catalog apps: {count}; refreshed projects: {len(changed_repos)}")
    if changed_repos:
        print("Changed upstreams: " + ", ".join(changed_repos))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as error:
        print(f"ERROR: {error}", file=sys.stderr)
        sys.exit(1)
