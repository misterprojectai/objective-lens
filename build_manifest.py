#!/usr/bin/env python3
"""
Build iximiuz manifest for an objective from already-deployed content.
Queries labctl for all deployed tutorials and challenges matching the
objective slug, then writes a manifest JSON file.

Usage: python3 build_manifest.py x200_101

Output: 05_iximiuz/output/x200_101-manifest.json
"""

import json
import re
import subprocess
import sys
from pathlib import Path

STAGE5_DIR = "05_iximiuz/output"


def list_content(kind):
    result = subprocess.run(
        ['labctl', 'content', 'list', '--kind', kind],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        return []
    names = []
    for line in result.stdout.splitlines():
        line = line.strip()
        if line.startswith('name:'):
            names.append(line.split(':', 1)[1].strip())
    return names


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 build_manifest.py <obj_id>")
        print("       python3 build_manifest.py x200_101")
        sys.exit(1)

    obj_id = sys.argv[1].strip()
    if '_' not in obj_id and len(obj_id) == 7:
        obj_id = obj_id[:4] + '_' + obj_id[4:]

    slug = obj_id.replace('_', '')

    print(f"Building manifest for {obj_id} (slug: {slug})...")

    tutorials  = list_content('tutorial')
    challenges = list_content('challenge')

    print(f"  Found {len(tutorials)} tutorials on server")
    print(f"  Found {len(challenges)} challenges on server")

    # Patterns — match base name with 8-char hex suffix
    tut_pat  = re.compile(rf'^rhcsa-{slug}-tutorial-(\d+)-[0-9a-f]{{8}}$')
    how_pat  = re.compile(rf'^rhcsa-{slug}-howto-(\d+)-[0-9a-f]{{8}}$')
    ch_pat   = re.compile(rf'^rhcsa-{slug}-challenge-(\d+)-[0-9a-f]{{8}}$')
    br_pat   = re.compile(rf'^rhcsa-{slug}-challenge-broken-(\d+)-[0-9a-f]{{8}}$')

    manifest = {
        'obj_id':             obj_id,
        'tutorials':          {},
        'howtos':             {},
        'challenges':         {},
        'challenges_broken':  {},
    }

    for name in tutorials:
        m = tut_pat.match(name)
        if m:
            manifest['tutorials'][m.group(1)] = name
        m = how_pat.match(name)
        if m:
            manifest['howtos'][m.group(1)] = name

    for name in challenges:
        m = ch_pat.match(name)
        if m:
            manifest['challenges'][m.group(1)] = name
        m = br_pat.match(name)
        if m:
            manifest['challenges_broken'][m.group(1)] = name

    # Report
    print(f"\nMatched:")
    print(f"  tutorials:          {len(manifest['tutorials'])}")
    print(f"  howtos:             {len(manifest['howtos'])}")
    print(f"  challenges:         {len(manifest['challenges'])}")
    print(f"  challenges_broken:  {len(manifest['challenges_broken'])}")

    # Write
    out_path = Path(STAGE5_DIR) / f"{obj_id}-manifest.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(manifest, indent=2))
    print(f"\nManifest written: {out_path}")
    print(json.dumps(manifest, indent=2))


if __name__ == '__main__':
    main()
