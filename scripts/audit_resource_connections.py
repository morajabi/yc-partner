#!/usr/bin/env python3
"""Audit how processed resources are connected to indexes and guides."""

from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT_DIR / "skills" / "yc-partner"
RESOURCE_DIR = SKILL_DIR / "resources"
ROUTING_DIRS = [
    SKILL_DIR / "indexes",
    SKILL_DIR / "guides",
    SKILL_DIR / "references",
]
ROUTING_FILES = [
    SKILL_DIR / "SKILL.md",
    ROOT_DIR / "AGENTS.md",
    ROOT_DIR / "README.md",
]

BULK_FOLDERS = {
    "rfs",
    "examples/getintoyc",
    "dalton-michael",
    "yc-company-directory",
}


def read_routing_text() -> str:
    parts: list[str] = []
    for folder in ROUTING_DIRS:
        parts.extend(path.read_text(encoding="utf-8", errors="ignore") for path in folder.glob("*.md"))
    for path in ROUTING_FILES:
        if path.exists():
            parts.append(path.read_text(encoding="utf-8", errors="ignore"))
    return "\n".join(parts)


def resource_files() -> list[Path]:
    return sorted(path for path in RESOURCE_DIR.rglob("*.md") if path.name != "README.md")


def is_bulk_folder(relative: Path) -> bool:
    relative_text = relative.as_posix()
    return any(relative_text == folder or relative_text.startswith(f"{folder}/") for folder in BULK_FOLDERS)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--show-bulk",
        action="store_true",
        help="Include resources in folders that are normally routed at folder level.",
    )
    args = parser.parse_args()

    routing_text = read_routing_text()
    missing: list[Path] = []
    counts_by_folder: dict[str, list[Path]] = defaultdict(list)

    for path in resource_files():
        relative = path.relative_to(RESOURCE_DIR)
        resource_ref = f"../resources/{relative.as_posix()}"
        skill_ref = str(path.relative_to(SKILL_DIR))
        if resource_ref in routing_text or skill_ref in routing_text:
            continue
        if is_bulk_folder(relative) and not args.show_bulk:
            continue
        missing.append(relative)
        folder = relative.parts[0] if relative.parts else "."
        counts_by_folder[folder].append(relative)

    print(f"Resources: {len(resource_files())}")
    print(f"Unreferenced direct resources: {len(missing)}")
    if not args.show_bulk:
        print("Bulk-routed folders hidden: " + ", ".join(sorted(BULK_FOLDERS)))

    for folder, paths in sorted(counts_by_folder.items()):
        print(f"\n## {folder} ({len(paths)})")
        for path in paths:
            print(path.as_posix())

    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
