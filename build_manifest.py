#!/usr/bin/env python3
"""
Build iximiuz manifest for an objective from already-deployed content.
Queries labctl for all deployed tutorials and challenges matching the
objective slug, then writes a manifest JSON file for stage4b_run.py.

Usage:
  python3 build_manifest.py x200_101            # standard
  python3 build_manifest.py x200_101 --verbose  # print full manifest JSON

Output: 05_iximiuz/output/x200_101-manifest.json

Run this AFTER stage5_run.py and stage5b_run.py have deployed all content.
Run stage4b_run.py AFTER this to inject links into GitBook.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

STAGE5_DIR = "05_iximiuz/output"


def list_content(kind):
    """Query labctl for all deployed content of a given kind.
    Returns list of name strings, or exits with error if labctl fails."""
    result = subprocess.run(
        ['labctl', 'content', 'list', '--kind', kind],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"ERROR: labctl content list --kind {kind} failed:")
        print(f"  {result.stderr.strip()}")
        print("Ensure labctl is authenticated: labctl auth whoami")
        sys.exit(1)

    names = []
    for line in result.stdout.splitlines():
        line = line.strip()
        if line.startswith('name:'):
            names.append(line.split(':', 1)[1].strip())
    return names


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 build_manifest.py <obj_id> [--verbose]")
        print("       python3 build_manifest.py x200_101")
        print("       python3 build_manifest.py x200_101 --verbose")
        sys.exit(1)

    obj_id  = sys.argv[1].strip()
    verbose = '--verbose' in sys.argv

    if '_' not in obj_id and len(obj_id) == 7:
        obj_id = obj_id[:4] + '_' + obj_id[4:]

    slug = obj_id.replace('_', '')

    print(f"\n{'='*60}")
    print(f"Build Manifest: {obj_id}")
    print(f"{'='*60}\n")

    print(f"Querying labctl...")
    tutorials  = list_content('tutorial')
    challenges = list_content('challenge')

    print(f"  Found {len(tutorials)} tutorials on server")
    print(f"  Found {len(challenges)} challenges on server")

    # Patterns match:
    #   exact base name (no hex suffix — rare but possible)
    #   base name + 8-char hex suffix (standard iximiuz behavior)
    tut_pat = re.compile(rf'^rhcsa-{slug}-tutorial-(\d+)(?:-[0-9a-f]{{8}})?$')
    how_pat = re.compile(rf'^rhcsa-{slug}-howto-(\d+)(?:-[0-9a-f]{{8}})?$')
    ch_pat  = re.compile(rf'^rhcsa-{slug}-challenge-(\d+)(?:-[0-9a-f]{{8}})?$')
    br_pat  = re.compile(rf'^rhcsa-{slug}-challenge-broken-(\d+)(?:-[0-9a-f]{{8}})?$')

    manifest = {
        'obj_id':            obj_id,
        'tutorials':         {},
        'howtos':            {},
        'challenges':        {},
        'challenges_broken': {},
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

    # Validate completeness
    n_tut = len(manifest['tutorials'])
    n_how = len(manifest['howtos'])
    n_ch  = len(manifest['challenges'])
    n_br  = len(manifest['challenges_broken'])

    print(f"\nMatched for {obj_id}:")
    print(f"  tutorials:          {n_tut}")
    print(f"  howtos:             {n_how}")
    print(f"  challenges:         {n_ch}")
    print(f"  challenges_broken:  {n_br}")

    # Warn on asymmetry
    if n_tut != n_how:
        print(f"  WARNING: tutorial count ({n_tut}) != howto count ({n_how})")
    if n_ch != n_br:
        print(f"  WARNING: clean challenge count ({n_ch}) != broken count ({n_br})")
    if n_tut == 0 and n_how == 0:
        print(f"  ERROR: No tutorials or howtos found for {obj_id}")
        print(f"  Run stage5_run.py {obj_id} first")
        sys.exit(1)

    # Write manifest
    out_path = Path(STAGE5_DIR) / f"{obj_id}-manifest.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(manifest, indent=2, sort_keys=False))

    print(f"\nManifest written: {out_path}")

    if verbose:
        print(json.dumps(manifest, indent=2))
    else:
        print("(use --verbose to print full manifest JSON)")

    print(f"\nNext: python3 stage4b_run.py {obj_id}")


if __name__ == '__main__':
    main()
