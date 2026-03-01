#!/usr/bin/env python3
"""Generate catalog.json from individual template files in templates/.

Each template file must be a valid Templatr JSON template with at a minimum
the fields: name, content.

The script reads meta-information from an optional sidecar `.meta.json` file
alongside the template, or from a top-level `_catalog_meta` key inside the
template JSON itself.  If neither is found the script emits a warning and
skips the file.

Expected meta fields (all required for catalog inclusion):
  - author      : str
  - tags        : list[str]
  - version     : str  (semver)
  - description : str  (falls back to template description field if present)

Usage:
    python scripts/generate_catalog.py [--output catalog.json]
"""

import argparse
import json
import os
import sys
from pathlib import Path

REQUIRED_FIELDS = {"name", "description", "author", "tags", "version", "download_url"}

REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = REPO_ROOT / "templates"
DEFAULT_OUTPUT = REPO_ROOT / "catalog.json"

RAW_BASE_URL = (
    "https://raw.githubusercontent.com/josiahH-cf/templatr-catalog/main/templates/"
)


def load_template(path: Path) -> dict | None:
    """Load and return a template JSON file, or None on error."""
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as exc:
        print(f"  WARNING: could not read {path.name}: {exc}", file=sys.stderr)
        return None


def build_entry(path: Path) -> dict | None:
    """Build a catalog entry dict from a template file.

    Looks for meta information in:
    1. A sidecar <stem>.meta.json file next to the template.
    2. A top-level `_catalog_meta` key inside the template JSON.

    Returns None and prints a warning if required fields are missing.
    """
    data = load_template(path)
    if data is None:
        return None

    # Gather meta from sidecar or inline key
    meta: dict = {}
    sidecar = path.with_suffix("").with_suffix(".meta.json")
    if sidecar.exists():
        try:
            with open(sidecar, encoding="utf-8") as f:
                meta = json.load(f)
        except (json.JSONDecodeError, OSError) as exc:
            print(f"  WARNING: could not read sidecar {sidecar.name}: {exc}", file=sys.stderr)
    elif "_catalog_meta" in data:
        meta = data["_catalog_meta"]

    if not meta:
        print(
            f"  WARNING: {path.name} has no catalog meta — skipping "
            "(add a .meta.json sidecar or a _catalog_meta key)",
            file=sys.stderr,
        )
        return None

    entry = {
        "name": data.get("name", ""),
        "description": meta.get("description") or data.get("description", ""),
        "author": meta.get("author", ""),
        "tags": meta.get("tags", []),
        "version": meta.get("version", "1.0.0"),
        "download_url": RAW_BASE_URL + path.name,
    }

    missing = [f for f in REQUIRED_FIELDS if not entry.get(f)]
    if missing:
        print(
            f"  WARNING: {path.name} missing required catalog fields: {missing} — skipping",
            file=sys.stderr,
        )
        return None

    return entry


def generate(output_path: Path) -> int:
    """Generate catalog.json; returns exit code (0 = success, 1 = errors)."""
    if not TEMPLATES_DIR.exists():
        print(f"ERROR: templates/ directory not found at {TEMPLATES_DIR}", file=sys.stderr)
        return 1

    entries = []
    errors = 0

    for path in sorted(TEMPLATES_DIR.glob("*.json")):
        # Skip sidecar meta files
        if path.stem.endswith(".meta"):
            continue
        print(f"Processing {path.name}...")
        entry = build_entry(path)
        if entry is None:
            errors += 1
        else:
            entries.append(entry)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2)
        f.write("\n")

    print(f"\nWrote {len(entries)} entries to {output_path}")
    if errors:
        print(f"{errors} file(s) skipped due to errors or missing meta.", file=sys.stderr)

    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate catalog.json")
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Output path for catalog.json",
    )
    args = parser.parse_args()
    sys.exit(generate(args.output))
