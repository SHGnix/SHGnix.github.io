#!/usr/bin/env python3
"""Add repository presentation fields to Packages and validate its entries."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REQUIRED_FIELDS = ("Package", "Version", "Architecture", "Filename", "Size", "MD5sum", "SHA256")


def parse_fields(stanza: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in stanza.splitlines():
        if line and not line[0].isspace() and ":" in line:
            key, value = line.split(":", 1)
            fields[key] = value.strip()
    return fields


def set_fields(stanza: str, extra: dict[str, str]) -> str:
    # Remove an existing field and its continuation lines before appending one canonical value.
    output: list[str] = []
    skip_continuations = False
    for line in stanza.splitlines():
        if line.startswith((" ", "\t")):
            if not skip_continuations:
                output.append(line)
            continue
        key = line.split(":", 1)[0] if ":" in line else ""
        skip_continuations = key in extra
        if not skip_continuations:
            output.append(line)
    output.extend(f"{key}: {value}" for key, value in extra.items())
    return "\n".join(output)


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: enrich-packages.py PACKAGES_FILE METADATA_JSON", file=sys.stderr)
        return 2

    packages_path = Path(sys.argv[1])
    metadata_path = Path(sys.argv[2])
    raw = packages_path.read_text(encoding="utf-8")
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))

    stanzas = [part.strip("\n") for part in re.split(r"\n\s*\n", raw.strip()) if part.strip()]
    seen: set[tuple[str, str, str]] = set()
    found: set[str] = set()
    enriched: list[str] = []

    for stanza in stanzas:
        fields = parse_fields(stanza)
        missing = [key for key in REQUIRED_FIELDS if not fields.get(key)]
        if missing:
            raise SystemExit(f"Invalid Packages stanza; missing {', '.join(missing)}: {fields.get('Package', '<unknown>')}")

        identity = (fields["Package"], fields["Version"], fields["Architecture"])
        if identity in seen:
            raise SystemExit("Duplicate package/version/architecture entry: " + " / ".join(identity))
        seen.add(identity)

        package_id = fields["Package"]
        if package_id in metadata:
            stanza = set_fields(stanza, metadata[package_id])
            found.add(package_id)

        enriched.append(stanza)

    missing_packages = sorted(set(metadata) - found)
    if missing_packages:
        raise SystemExit("Configured packages missing from Packages index: " + ", ".join(missing_packages))

    packages_path.write_text("\n\n".join(enriched) + "\n", encoding="utf-8")
    print(f"Validated and enriched {len(enriched)} package stanza(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
