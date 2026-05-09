#!/usr/bin/env python3
"""
Stage 5 Verifier — iximiuz Labs
Checks local output integrity and confirms deployment on iximiuz server.

Usage: python3 stage5_verify.py x200_101
"""

import re
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. Run: pip install pyyaml --break-system-packages")
    sys.exit(1)

STAGE5_DIR = "05_iximiuz/output"

CATEGORY_NAMES = {
    "linux", "networking", "containers", "kubernetes",
    "programming", "observability", "security", "ci-cd"
}

REQUIRED_FRONTMATTER = ['kind', 'title', 'description', 'categories', 'tagz', 'createdAt', 'cover']


def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def extract_frontmatter(content):
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return {}
    try:
        return yaml.safe_load(match.group(1)) or {}
    except Exception:
        return {}


def get_expected_names(obj_id):
    """Derive expected tutorial names from Stage 3 output."""
    from pathlib import Path as P
    stage3_dir = P(f"03_diataxis/output/{obj_id}")
    names = []
    slug = obj_id.replace('_', '')

    for path in sorted(stage3_dir.glob(f"{obj_id}_tutorial_*.md")):
        content = read_file(str(path))
        fm = extract_frontmatter(content)
        idx = fm.get('tutorial_index', 1)
        names.append(f"rhcsa-{slug}-tutorial-{idx}")

    for path in sorted(stage3_dir.glob(f"{obj_id}_howto_*.md")):
        content = read_file(str(path))
        fm = extract_frontmatter(content)
        idx = fm.get('howto_index', 1)
        names.append(f"rhcsa-{slug}-howto-{idx}")

    return names


def get_deployed_names():
    """Query iximiuz server for deployed tutorial names."""
    result = subprocess.run(
        ['labctl', 'content', 'list', '--kind', 'tutorial'],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        return None, result.stderr.strip()

    names = []
    for line in result.stdout.splitlines():
        line = line.strip()
        if line.startswith('name:'):
            names.append(line.split(':', 1)[1].strip())
    return names, None


def check_index(index_path, name):
    """Run all checks on a single index.md. Returns list of (check, pass, detail)."""
    checks = []

    def add(label, passed, detail=""):
        checks.append((label, passed, detail))

    content = read_file(str(index_path))
    fm      = extract_frontmatter(content)

    # 1. Frontmatter parseable
    add("Frontmatter parseable", bool(fm))

    # 2. kind: tutorial
    add("kind: tutorial", fm.get('kind') == 'tutorial', fm.get('kind', 'MISSING'))

    # 3. Required fields present
    missing = [f for f in REQUIRED_FRONTMATTER if not fm.get(f)]
    add("Required fields present", not missing, ', '.join(missing) if missing else "")

    # 4. cover uses __static__/ prefix
    cover = str(fm.get('cover', ''))
    add("cover uses __static__/ prefix", cover.startswith('__static__/'), cover or 'MISSING')

    # 5. tagz clean (no category names)
    tagz    = [str(t) for t in (fm.get('tagz') or [])]
    bad     = [t for t in tagz if t in CATEGORY_NAMES]
    add("tagz contains no category names", not bad, ', '.join(bad) if bad else "")

    # 6. No GitBook liquid syntax
    has_liquid = '{%' in content or '%}' in content
    add("No GitBook liquid syntax", not has_liquid)

    # 7. Tasks have matching components
    tasks      = fm.get('tasks') or {}
    unmatched  = []
    for t in tasks:
        if t.startswith(('verify_', 'input_')):
            if f':name: {t}' not in content:
                unmatched.append(t)
    add("All verify/input tasks have body components", not unmatched,
        ', '.join(unmatched) if unmatched else "")

    # 8. init_history_flush present (RHCSA requirement)
    add("init_history_flush task present", 'init_history_flush' in tasks)

    # 9. playground defined
    add("playground defined", bool(fm.get('playground')))

    # 10. MDC blocks balanced (even :: count)
    double_colons = content.count('::')
    add("MDC blocks balanced (even :: count)", double_colons % 2 == 0,
        f"{double_colons} occurrences")

    # 11. No raw frontmatter fields in body (common generation artifact)
    body = content.split('---', 2)[-1] if content.count('---') >= 2 else content
    has_raw_fm = bool(re.search(r'^(kind|title|description|categories|tagz):', body, re.MULTILINE))
    add("No raw frontmatter leaked into body", not has_raw_fm)

    return checks


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 stage5_verify.py <objective_id>")
        print("       python3 stage5_verify.py x200_101")
        sys.exit(1)

    obj_id = sys.argv[1].strip()
    if '_' not in obj_id and len(obj_id) == 7:
        obj_id = obj_id[:4] + '_' + obj_id[4:]

    print(f"\n{'='*60}")
    print(f"Stage 5 Verify — {obj_id}")
    print(f"{'='*60}\n")

    expected_names = get_expected_names(obj_id)
    if not expected_names:
        print(f"ERROR: No Stage 3 output found for {obj_id}")
        sys.exit(1)

    print(f"Expected: {len(expected_names)} tutorials")
    for n in expected_names:
        print(f"  {n}")

    # Query server
    print(f"\nQuerying iximiuz server...")
    deployed_names, err = get_deployed_names()
    if err:
        print(f"  WARNING: Could not query server — {err}")
        deployed_names = []
    else:
        print(f"  {len(deployed_names)} tutorials found on server")

    # Run checks
    total_checks = 0
    total_passed = 0
    file_results = []

    for name in expected_names:
        output_dir = Path(STAGE5_DIR) / name
        index_path = output_dir / "index.md"
        cover_path = output_dir / "__static__" / "cover.png"

        file_checks = []

        # Existence checks
        index_exists = index_path.exists()
        cover_exists = cover_path.exists()
        on_server    = name in (deployed_names or [])

        file_checks.append(("index.md exists",         index_exists, ""))
        file_checks.append(("__static__/cover.png exists", cover_exists, ""))
        file_checks.append(("Deployed on iximiuz server", on_server, ""))

        # Content checks (only if index exists)
        if index_exists:
            content_checks = check_index(index_path, name)
            file_checks.extend(content_checks)

        n_pass = sum(1 for _, p, _ in file_checks if p)
        total_checks += len(file_checks)
        total_passed += n_pass
        file_results.append((name, file_checks, n_pass))

    # Print results
    all_pass = True
    for name, checks, n_pass in file_results:
        n_total = len(checks)
        status  = "✅" if n_pass == n_total else "⚠️ "
        print(f"\n{status} {name}  [{n_pass}/{n_total}]")
        for label, passed, detail in checks:
            icon = "  ✓" if passed else "  ✗"
            suffix = f" — {detail}" if detail and not passed else ""
            print(f"{icon} {label}{suffix}")
            if not passed:
                all_pass = False

    # Summary
    print(f"\n{'='*60}")
    print(f"{'PASS' if all_pass else 'FAIL'}  {total_passed}/{total_checks} checks passed")
    print(f"{'='*60}")

    if all_pass:
        print(f"\nAll {len(expected_names)} iximiuz tutorials verified.")
        print(f"View at: https://labs.iximiuz.com/tutorials")
    else:
        failed = [(n, [c for c in ch if not c[1]]) for n, ch, _ in file_results if any(not c[1] for c in ch)]
        print(f"\nFailed tutorials:")
        for name, fails in failed:
            print(f"\n  {name}:")
            for label, _, detail in fails:
                suffix = f" ({detail})" if detail else ""
                print(f"    ✗ {label}{suffix}")
        print(f"\nTo re-run generation:")
        print(f"  python3 stage5_run.py {obj_id}")
        sys.exit(1)


if __name__ == "__main__":
    main()
