#!/usr/bin/env python3
"""Build the 1.3.0-2 repack with the requested display name and 58px icon."""
from __future__ import annotations

import argparse
import plistlib
import subprocess
import tempfile
from pathlib import Path

from PIL import Image

PACKAGE_ID = "local.preference-label-keeper"
SOURCE_VERSION = "1.3.0-1"
TARGET_VERSION = "1.3.0-2"
DISPLAY_NAME = "名称保护（Roothide）"
ICON_URL = "https://shgnix.github.io/repo/icons/pref-label-keeper.png"
BUNDLE = Path("Library/PreferenceLoader/Preferences/PreferenceLabelKeeper.bundle")


def control_fields(path: Path) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if line and not line[0].isspace() and ":" in line:
            key, value = line.split(":", 1)
            fields[key] = value.strip()
    return fields


def update_control(path: Path) -> None:
    lines = path.read_text(encoding="utf-8").splitlines()
    updates = {
        "Version": TARGET_VERSION,
        "Name": DISPLAY_NAME,
        "Icon": ICON_URL,
    }
    output: list[str] = []
    skip_continuations = False
    found: set[str] = set()

    for line in lines:
        if line.startswith((" ", "\t")):
            if not skip_continuations:
                output.append(line)
            continue

        key = line.split(":", 1)[0] if ":" in line else ""
        if key in updates:
            output.append(f"{key}: {updates[key]}")
            found.add(key)
            skip_continuations = True
        else:
            output.append(line)
            skip_continuations = False

    for key, value in updates.items():
        if key not in found:
            output.append(f"{key}: {value}")

    path.write_text("\n".join(output) + "\n", encoding="utf-8")


def update_labels(value):
    if isinstance(value, dict):
        for key, item in list(value.items()):
            if key in {"label", "title"} and item == "名称保护":
                value[key] = DISPLAY_NAME
            else:
                update_labels(item)
    elif isinstance(value, list):
        for item in value:
            update_labels(item)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("target", type=Path)
    args = parser.parse_args()

    if not args.source.is_file():
        raise SystemExit(f"Source package not found: {args.source}")

    source_fields = control_fields_from_deb(args.source)
    if source_fields.get("Package") != PACKAGE_ID:
        raise SystemExit("Unexpected source package identifier")
    if source_fields.get("Version") != SOURCE_VERSION:
        raise SystemExit(f"Expected source version {SOURCE_VERSION}, got {source_fields.get('Version')}")
    if source_fields.get("Architecture") != "iphoneos-arm64e":
        raise SystemExit("Unexpected source package architecture")

    with tempfile.TemporaryDirectory(prefix="shgnix-package-") as temp:
        root = Path(temp) / "root"
        subprocess.run(["dpkg-deb", "-R", str(args.source), str(root)], check=True)

        update_control(root / "DEBIAN/control")

        info_path = root / BUNDLE / "Info.plist"
        info = plistlib.loads(info_path.read_bytes())
        info["CFBundleName"] = DISPLAY_NAME
        info["CFBundleShortVersionString"] = "1.3.0"
        info["CFBundleVersion"] = "1.3.0"
        info_path.write_bytes(plistlib.dumps(info, fmt=plistlib.FMT_XML, sort_keys=False))

        root_path = root / BUNDLE / "Root.plist"
        settings = plistlib.loads(root_path.read_bytes())
        update_labels(settings)
        root_path.write_bytes(plistlib.dumps(settings, fmt=plistlib.FMT_XML, sort_keys=False))

        icon_path = root / BUNDLE / "icon.png"
        with Image.open(icon_path) as icon:
            icon = icon.convert("RGBA").resize((58, 58), Image.Resampling.LANCZOS)
            icon.save(icon_path, format="PNG", optimize=True)

        args.target.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            ["dpkg-deb", "--build", "--root-owner-group", str(root), str(args.target)],
            check=True,
        )

    target_fields = control_fields_from_deb(args.target)
    if target_fields.get("Package") != PACKAGE_ID or target_fields.get("Version") != TARGET_VERSION:
        raise SystemExit("Built package metadata did not pass verification")
    if target_fields.get("Name") != DISPLAY_NAME:
        raise SystemExit("Built package display name did not pass verification")

    with tempfile.TemporaryDirectory(prefix="shgnix-verify-") as temp:
        root = Path(temp) / "root"
        subprocess.run(["dpkg-deb", "-R", str(args.target), str(root)], check=True)
        info = plistlib.loads((root / BUNDLE / "Info.plist").read_bytes())
        if info.get("CFBundleShortVersionString") != "1.3.0" or info.get("CFBundleVersion") != "1.3.0":
            raise SystemExit("Plugin version fields are not 1.3.0")
        with Image.open(root / BUNDLE / "icon.png") as icon:
            if icon.size != (58, 58):
                raise SystemExit(f"Embedded icon must be 58x58, got {icon.size}")

    print(f"Built and verified {args.target}: {DISPLAY_NAME} {TARGET_VERSION}")
    return 0


def control_fields_from_deb(path: Path) -> dict[str, str]:
    result = subprocess.run(
        ["dpkg-deb", "-f", str(path)],
        check=True,
        capture_output=True,
        text=True,
    )
    fields: dict[str, str] = {}
    for line in result.stdout.splitlines():
        if line and not line[0].isspace() and ":" in line:
            key, value = line.split(":", 1)
            fields[key] = value.strip()
    return fields


if __name__ == "__main__":
    raise SystemExit(main())
