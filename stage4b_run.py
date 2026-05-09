#!/usr/bin/env python3
"""
Stage 4b — GitBook iximiuz Link Injection
Reads iximiuz manifest and updates GitBook pages with embed links.

Reads:   05_iximiuz/output/<obj_id>-manifest.json
Updates: 04_publish/output/<obj_id>/explanation.md  (full hub — all 3 sections)
         04_publish/output/<obj_id>/tutorial_NN.md   (single tutorial embed)
         04_publish/output/<obj_id>/howto_NN.md      (clean + broken challenge links)
Creates: 04_publish/output/<obj_id>/practice-labs.md (dedicated hub page)
Updates: 04_publish/output/SUMMARY.md

Commits and pushes on completion.

Usage: python3 stage4b_run.py x200_101

Run build_manifest.py first if manifest does not exist.
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path

STAGE5_DIR   = "05_iximiuz/output"
PUBLISH_DIR  = "04_publish/output"
IXIMIUZ_BASE = "https://labs.iximiuz.com"

# Section markers — used to detect and replace existing sections
MARKER_HUB      = "## Practice on a Live System"
MARKER_TUTORIAL = "## Practice This Lab"
MARKER_HOWTO    = "## Test Yourself"

# ── FILE I/O ──────────────────────────────────────────────────────────────────

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

# ── MANIFEST ──────────────────────────────────────────────────────────────────

def load_manifest(obj_id):
    path = Path(STAGE5_DIR) / f"{obj_id}-manifest.json"
    if not path.exists():
        print(f"ERROR: Manifest not found: {path}")
        print(f"Run first: python3 build_manifest.py {obj_id}")
        sys.exit(1)
    return json.loads(path.read_text())

# ── URL BUILDERS ──────────────────────────────────────────────────────────────

def tut_url(name):
    return f"{IXIMIUZ_BASE}/tutorials/{name}"

def ch_url(name):
    return f"{IXIMIUZ_BASE}/challenges/{name}"

def embed(url):
    return f'{{% embed url="{url}" %}}\n'

# ── SECTION BUILDERS ──────────────────────────────────────────────────────────

def build_explanation_hub(manifest):
    """Full three-section hub for the explanation page."""
    lines = [f"\n{MARKER_HUB}\n\n"]
    lines.append(
        "The following interactive labs run on a live Rocky Linux 9 playground. "
        "Start with tutorials, move to challenges when ready, then attempt the "
        "broken environment challenges for exam-level difficulty.\n\n"
    )

    tutorials = manifest.get('tutorials', {})
    challenges = manifest.get('challenges', {})
    broken = manifest.get('challenges_broken', {})

    if tutorials:
        lines.append("### Guided Tutorials\n\n")
        lines.append(
            "Learn the concepts with guided, step-by-step labs. "
            "Every command you run is verified in real time.\n\n"
        )
        for idx in sorted(tutorials.keys(), key=int):
            lines.append(embed(tut_url(tutorials[idx])))
            lines.append("\n")

    if challenges:
        lines.append("### Practice Challenges\n\n")
        lines.append(
            "Apply what you learned without guidance. "
            "Complete the task — the system verifies the outcome.\n\n"
        )
        for idx in sorted(challenges.keys(), key=int):
            lines.append(embed(ch_url(challenges[idx])))
            lines.append("\n")

    if broken:
        lines.append("### Advanced — Broken Environment\n\n")
        lines.append(
            "Diagnose and fix a misconfigured system. "
            "No steps, no hints unless you ask. This is exam conditions.\n\n"
        )
        for idx in sorted(broken.keys(), key=int):
            lines.append(embed(ch_url(broken[idx])))
            lines.append("\n")

    return ''.join(lines)


def build_tutorial_section(actual_name):
    """Single tutorial embed appended to a tutorial page."""
    return (
        f"\n{MARKER_TUTORIAL}\n\n"
        f"{embed(tut_url(actual_name))}\n"
    )


def build_howto_section(ch_name, br_name):
    """Clean challenge embed + broken environment link for a how-to page."""
    br_link = f"[Broken Environment Challenge →]({ch_url(br_name)})"
    return (
        f"\n{MARKER_HOWTO}\n\n"
        f"{embed(ch_url(ch_name))}\n"
        f"**Advanced — Broken Environment:** {br_link}\n"
    )


def build_practice_labs_page(obj_id, manifest):
    """Dedicated practice hub page listing all labs."""
    tutorials  = manifest.get('tutorials', {})
    challenges = manifest.get('challenges', {})
    broken     = manifest.get('challenges_broken', {})

    lines = [
        f"# Practice Labs — {obj_id.replace('_', ' ').upper()}\n\n",
        "All interactive labs for this objective on a live Rocky Linux 9 playground.\n\n",
        "Work through them in order: tutorials first to learn the skill, "
        "challenges to prove it, broken environment challenges for exam difficulty.\n\n",
    ]

    if tutorials:
        lines.append("## Guided Tutorials\n\n")
        for idx in sorted(tutorials.keys(), key=int):
            lines.append(embed(tut_url(tutorials[idx])))
            lines.append("\n")

    if challenges:
        lines.append("## Practice Challenges\n\n")
        for idx in sorted(challenges.keys(), key=int):
            lines.append(embed(ch_url(challenges[idx])))
            lines.append("\n")

    if broken:
        lines.append("## Advanced — Broken Environment\n\n")
        for idx in sorted(broken.keys(), key=int):
            lines.append(embed(ch_url(broken[idx])))
            lines.append("\n")

    return ''.join(lines)

# ── PAGE UPDATERS ─────────────────────────────────────────────────────────────

def update_explanation(obj_id, manifest):
    path = str(Path(PUBLISH_DIR) / obj_id / "explanation.md")
    if not Path(path).exists():
        print(f"  SKIP: explanation.md not found")
        return False

    content = read_file(path)
    hub = build_explanation_hub(manifest)

    if MARKER_HUB in content:
        idx = content.index(MARKER_HUB)
        content = content[:idx].rstrip() + "\n" + hub
    else:
        content = content.rstrip() + "\n" + hub

    write_file(path, content)
    print(f"  ✓ explanation.md — full hub ({len(manifest.get('tutorials',{}))} tutorials, "
          f"{len(manifest.get('challenges',{}))} challenges, "
          f"{len(manifest.get('challenges_broken',{}))} broken)")
    return True


def update_tutorial_page(obj_id, index, actual_name):
    fname = f"tutorial_{index:02d}.md"
    path  = str(Path(PUBLISH_DIR) / obj_id / fname)
    if not Path(path).exists():
        print(f"  SKIP: {fname} not found")
        return False

    content = read_file(path)
    section = build_tutorial_section(actual_name)

    if MARKER_TUTORIAL in content:
        idx = content.index(MARKER_TUTORIAL)
        content = content[:idx].rstrip() + "\n" + section
    else:
        content = content.rstrip() + "\n" + section

    write_file(path, content)
    print(f"  ✓ {fname}")
    return True


def update_howto_page(obj_id, index, ch_name, br_name):
    fname = f"howto_{index:02d}.md"
    path  = str(Path(PUBLISH_DIR) / obj_id / fname)
    if not Path(path).exists():
        print(f"  SKIP: {fname} not found")
        return False

    content = read_file(path)
    section = build_howto_section(ch_name, br_name)

    if MARKER_HOWTO in content:
        idx = content.index(MARKER_HOWTO)
        content = content[:idx].rstrip() + "\n" + section
    else:
        content = content.rstrip() + "\n" + section

    write_file(path, content)
    print(f"  ✓ {fname}")
    return True


def create_practice_labs_page(obj_id, manifest):
    path = str(Path(PUBLISH_DIR) / obj_id / "practice-labs.md")
    content = build_practice_labs_page(obj_id, manifest)
    write_file(path, content)
    print(f"  ✓ practice-labs.md (created)")
    return True


def update_summary(obj_id):
    summary_path = str(Path(PUBLISH_DIR) / "SUMMARY.md")
    if not Path(summary_path).exists():
        print(f"  SKIP: SUMMARY.md not found")
        return False

    content = read_file(summary_path)
    entry = f"  * [Practice Labs]({obj_id}/practice-labs.md)\n"

    if f"{obj_id}/practice-labs.md" in content:
        print(f"  SKIP: practice-labs.md already in SUMMARY.md")
        return True

    # Insert after last howto entry for this objective
    pattern = rf'(\* \[.*?\]\({re.escape(obj_id)}/howto_\d+\.md\)\n)'
    matches = list(re.finditer(pattern, content))
    if matches:
        pos = matches[-1].end()
        content = content[:pos] + entry + content[pos:]
        write_file(summary_path, content)
        print(f"  ✓ SUMMARY.md — added practice-labs.md")
        return True

    print(f"  WARNING: could not locate howto entries for {obj_id} in SUMMARY.md")
    return False

# ── GIT ───────────────────────────────────────────────────────────────────────

def git_commit_push(obj_id):
    subprocess.run(
        ['git', 'add',
         f'{PUBLISH_DIR}/{obj_id}/',
         f'{PUBLISH_DIR}/SUMMARY.md'],
        check=True
    )
    subprocess.run(
        ['git', 'commit', '-m',
         f'feat: link iximiuz labs to GitBook {obj_id} (Stage 4b)'],
        check=True
    )
    result = subprocess.run(
        ['git', 'push', 'origin', 'main'],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print("  Push rejected — rebasing...")
        subprocess.run(['git', 'pull', '--rebase', 'origin', 'main'], check=True)
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)
    print(f"  ✓ Committed and pushed")

# ── MAIN ──────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 stage4b_run.py <obj_id>")
        print("       python3 stage4b_run.py x200_101")
        sys.exit(1)

    obj_id = sys.argv[1].strip()
    if '_' not in obj_id and len(obj_id) == 7:
        obj_id = obj_id[:4] + '_' + obj_id[4:]

    print(f"\n{'='*60}")
    print(f"Stage 4b — GitBook iximiuz Links: {obj_id}")
    print(f"{'='*60}\n")

    manifest = load_manifest(obj_id)

    print(f"Manifest:")
    print(f"  tutorials:          {len(manifest.get('tutorials', {}))}")
    print(f"  howtos:             {len(manifest.get('howtos', {}))}")
    print(f"  challenges:         {len(manifest.get('challenges', {}))}")
    print(f"  challenges_broken:  {len(manifest.get('challenges_broken', {}))}")

    print(f"\nUpdating GitBook pages...")

    # 1. Explanation page — full hub
    update_explanation(obj_id, manifest)

    # 2. Tutorial pages — single embed each
    for idx_str, actual_name in sorted(
            manifest.get('tutorials', {}).items(), key=lambda x: int(x[0])):
        update_tutorial_page(obj_id, int(idx_str), actual_name)

    # 3. How-to pages — clean challenge + broken link
    challenges = manifest.get('challenges', {})
    broken     = manifest.get('challenges_broken', {})
    all_idxs   = sorted(
        set(list(challenges.keys()) + list(broken.keys())), key=int
    )
    for idx_str in all_idxs:
        ch_name = challenges.get(idx_str)
        br_name = broken.get(idx_str, ch_name)
        if ch_name:
            update_howto_page(obj_id, int(idx_str), ch_name, br_name)

    # 4. Practice labs hub page
    create_practice_labs_page(obj_id, manifest)

    # 5. SUMMARY.md
    update_summary(obj_id)

    # 6. Commit and push
    print(f"\nCommitting and pushing...")
    git_commit_push(obj_id)

    print(f"\n{'='*60}")
    print(f"Stage 4b Complete — {obj_id}")
    print(f"{'='*60}")
    print(f"GitBook syncing automatically.")
    print(f"Verify: stage4b_verify.py {obj_id}")


if __name__ == '__main__':
    main()
