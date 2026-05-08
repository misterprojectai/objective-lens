#!/usr/bin/env python3
"""
Stage 4 - Verification
Checks all Stage 4 GitBook output documents for structural correctness,
platform separation, rendering safety, and SUMMARY.md integrity.

Checks per file:
  - File exists
  - GitBook frontmatter present and valid (---, description, icon fields)
  - No Diataxis frontmatter fields leaked (type:, exam_objective:, status:, version:)
  - No YAML code fences wrapping frontmatter
  - No iximiuz MDC syntax (platform separation)
  - All liquid blocks properly closed (stepper, step, hint, tabs, tab,
    columns, column, code, content-ref, details)
  - Substantial content (type-specific minimums)
  - Type-specific structure: stepper in tutorials/how-tos, absent in explanation/reference
  - Tables present in reference

Global checks:
  - Tutorial count >= 3
  - How-to count >= 3
  - SUMMARY.md exists, contains objective section, links all output files, no duplicates
  - .gitbook.yaml exists and references SUMMARY.md

Pure stdlib — no external dependencies.

Usage: python3 stage4_verify.py 04_publish/output/x200_101
"""

import sys
import os
import re

if len(sys.argv) < 2:
    print("Usage: python3 stage4_verify.py 04_publish/output/x200_101")
    sys.exit(1)

OUTPUT_DIR   = sys.argv[1].rstrip("/")
SUMMARY_FILE = "04_publish/output/SUMMARY.md"
objective_id = os.path.basename(OUTPUT_DIR)

passes   = []
failures = []

def ok(msg):
    passes.append(msg)

def fail(msg):
    failures.append(msg)

def normalise_path(path):
    return path.replace(os.sep, "/")

# ── Discover files ────────────────────────────────────────────────────────────

expected_static = ["explanation.md", "reference.md"]
all_files      = sorted(os.listdir(OUTPUT_DIR)) if os.path.isdir(OUTPUT_DIR) else []
tutorial_files = sorted([f for f in all_files if re.match(r'tutorial_\d+\.md', f)])
howto_files    = sorted([f for f in all_files if re.match(r'howto_\d+\.md', f)])
all_expected   = expected_static + tutorial_files + howto_files

print("Stage 4 - Verification")
print("Output dir:  " + OUTPUT_DIR)
print("Objective:   " + objective_id)
print("Expected:    " + str(len(all_expected)) + " files")
print("  explanation + reference + " + str(len(tutorial_files)) + " tutorial(s) + " + str(len(howto_files)) + " how-to(s)")
print()

# ── Per-file checker ──────────────────────────────────────────────────────────

def check_file(fname):
    path  = os.path.join(OUTPUT_DIR, fname)
    label = fname.replace(".md", "")

    # 1. Exists
    if not os.path.exists(path):
        fail(label + ": file missing — " + path)
        return
    ok(label + ": file exists")

    content = open(path, encoding="utf-8").read()

    # 2. Frontmatter starts with ---
    if content.startswith("---"):
        ok(label + ": frontmatter delimiter present")
    else:
        fail(label + ": no frontmatter (must start with ---)")

    # 3. description field present
    if re.search(r'^description:', content[:500], re.MULTILINE):
        # Also check it is not a placeholder
        m = re.search(r'^description:\s*(.+)', content[:500], re.MULTILINE)
        if m:
            val = m.group(1).strip()
            if val.startswith("[") or val == "":
                fail(label + ": description is a placeholder or empty: " + repr(val))
            else:
                ok(label + ": description field present and populated")
        else:
            ok(label + ": description field present")
    else:
        fail(label + ": missing description field in frontmatter")

    # 4. icon field present
    if re.search(r'^icon:', content[:500], re.MULTILINE):
        ok(label + ": icon field present")
    else:
        fail(label + ": missing icon field in frontmatter")

    # 5. No Diataxis frontmatter fields leaked
    diataxis_fields = ["type:", "exam_objective:", "status:", "version:"]
    leaked = [f for f in diataxis_fields if re.search(r'^' + re.escape(f), content[:500], re.MULTILINE)]
    if leaked:
        fail(label + ": Diataxis frontmatter fields leaked: " + str(leaked))
    else:
        ok(label + ": no Diataxis frontmatter fields leaked")

    # 6. No YAML code fences in frontmatter region
    if "```yaml" in content[:400]:
        fail(label + ": YAML code fence found in frontmatter region")
    else:
        ok(label + ": no YAML code fences in frontmatter")

    # 7. No iximiuz MDC syntax (platform separation)
    mdc_patterns = [r'::simple-task', r'::remark-box', r'::hint-box',
                    r'::details-box', r'\bexaminerd\b', r'::\w+-\w+']
    mdc_found = [p for p in mdc_patterns if re.search(p, content)]
    if mdc_found:
        fail(label + ": iximiuz MDC syntax found (platform separation violation): " + str(mdc_found))
    else:
        ok(label + ": no iximiuz MDC syntax (platform separation clean)")

    # 8. All liquid blocks properly closed
    # Each tuple: (opener_pattern, closer_string, description)
    # opener_pattern uses str.count for exact matching where possible
    block_pairs = [
        ("{% stepper %}",     "{% endstepper %}",     "stepper"),
        ("{% step %}",        "{% endstep %}",         "step"),
        ("{% hint",           "{% endhint %}",         "hint"),
        ("{% tabs %}",        "{% endtabs %}",         "tabs"),
        ("{% tab ",           "{% endtab %}",          "tab"),
        ("{% columns %}",     "{% endcolumns %}",      "columns"),
        ("{% column %}",      "{% endcolumn %}",       "column"),
        ("{% code ",          "{% endcode %}",         "code"),
        ("{% content-ref ",   "{% endcontent-ref %}", "content-ref"),
    ]
    unclosed = []
    for opener, closer, name in block_pairs:
        open_count  = content.count(opener)
        close_count = content.count(closer)
        if open_count != close_count:
            unclosed.append(name + "(" + str(open_count) + " open vs " + str(close_count) + " close)")

    # details: count <details and </details> separately
    details_open  = len(re.findall(r'<details', content))
    details_close = content.count("</details>")
    if details_open != details_close:
        unclosed.append("details(" + str(details_open) + " open vs " + str(details_close) + " close)")

    if unclosed:
        fail(label + ": unclosed blocks: " + "; ".join(unclosed))
    else:
        ok(label + ": all blocks properly closed")

    # 9. Substantial content
    min_chars = {
        "explanation": 4000,
        "reference":   4000,
        "tutorial":    2000,
        "howto":       1500,
    }
    if "tutorial" in label:
        doc_type = "tutorial"
    elif "howto" in label:
        doc_type = "howto"
    elif "explanation" in label:
        doc_type = "explanation"
    elif "reference" in label:
        doc_type = "reference"
    else:
        doc_type = "unknown"

    threshold = min_chars.get(doc_type, 1000)
    if len(content) >= threshold:
        ok(label + ": substantial content (" + str(len(content)) + " chars)")
    else:
        fail(label + ": content too short (" + str(len(content)) + " chars, min " + str(threshold) + ")")

    # 10. Type-specific structure checks
    if doc_type in ("tutorial", "howto"):
        if "{% stepper %}" in content:
            ok(label + ": stepper block present")
        else:
            fail(label + ": no stepper block (required for " + doc_type + ")")

        if "{% hint" in content:
            ok(label + ": hint blocks present")
        else:
            fail(label + ": no hint blocks (expected for " + doc_type + ")")

    if doc_type == "explanation":
        if "{% stepper %}" not in content:
            ok(label + ": no stepper (correct — explanation is conceptual)")
        else:
            fail(label + ": stepper found in explanation (Diataxis contamination)")

        if "{% hint" in content:
            ok(label + ": hint blocks present")
        else:
            fail(label + ": no hint blocks (explanation should have at least an opening info hint)")

    if doc_type == "reference":
        if "{% stepper %}" not in content:
            ok(label + ": no stepper (correct — reference is not procedural)")
        else:
            fail(label + ": stepper found in reference (Diataxis contamination)")

        table_rows = len(re.findall(r'^\|.+\|', content, re.MULTILINE))
        if table_rows >= 10:
            ok(label + ": tables present (" + str(table_rows) + " rows)")
        else:
            fail(label + ": insufficient tables (" + str(table_rows) + " rows, min 10)")

# Run per-file checks
for fname in all_expected:
    check_file(fname)

# ── Global document count checks ─────────────────────────────────────────────

if len(tutorial_files) >= 3:
    ok("document counts: " + str(len(tutorial_files)) + " tutorial(s) >= min 3")
else:
    fail("document counts: " + str(len(tutorial_files)) + " tutorial(s) — min 3 required")

if len(howto_files) >= 3:
    ok("document counts: " + str(len(howto_files)) + " how-to(s) >= min 3")
else:
    fail("document counts: " + str(len(howto_files)) + " how-to(s) — min 3 required")

# ── SUMMARY.md checks ─────────────────────────────────────────────────────────

if os.path.exists(SUMMARY_FILE):
    ok("SUMMARY.md: file exists")
    summary = open(SUMMARY_FILE, encoding="utf-8").read()

    if "RHCSA — " + objective_id in summary:
        ok("SUMMARY.md: section for " + objective_id + " present")
    else:
        fail("SUMMARY.md: section for " + objective_id + " missing")

    # Paths in SUMMARY.md are relative to .gitbook.yaml root (04_publish/output/)
    # so they appear as x200_101/fname.md, not 04_publish/output/x200_101/fname.md
    missing_links = []
    for fname in all_expected:
        gitbook_path = objective_id + "/" + fname
        if gitbook_path not in summary:
            missing_links.append(fname)
    if missing_links:
        fail("SUMMARY.md: links missing for: " + str(missing_links))
    else:
        ok("SUMMARY.md: all " + str(len(all_expected)) + " output files linked")

    # Duplicate link check — match GitBook-relative paths
    link_pattern = re.findall(
        r'\(' + re.escape(objective_id) + r'/[^\)]+\)',
        summary
    )
    seen  = set()
    dupes = []
    for lnk in link_pattern:
        if lnk in seen:
            dupes.append(lnk)
        seen.add(lnk)
    if dupes:
        fail("SUMMARY.md: duplicate links: " + str(dupes))
    else:
        ok("SUMMARY.md: no duplicate links")

else:
    fail("SUMMARY.md: file missing")

# ── .gitbook.yaml check ───────────────────────────────────────────────────────

if os.path.exists(".gitbook.yaml"):
    ok(".gitbook.yaml: file exists")
    gb = open(".gitbook.yaml", encoding="utf-8").read()
    if "SUMMARY.md" in gb:
        ok(".gitbook.yaml: SUMMARY.md referenced")
    else:
        fail(".gitbook.yaml: SUMMARY.md not referenced")
else:
    fail(".gitbook.yaml: file missing (required for GitBook Git Sync)")

# ── Print results ─────────────────────────────────────────────────────────────

total = len(passes) + len(failures)
print("Results: " + str(len(passes)) + "/" + str(total) + " passed, " + str(len(failures)) + " failed")
print()
for p in passes:
    print("  \u2713 " + p)

if failures:
    print()
    for f in failures:
        print("  \u2717 " + f)
    print()
    print("VERIFICATION FAILED — fix issues before Stage 5")
    sys.exit(1)
else:
    print()
    print("VERIFICATION PASSED — Stage 4 output ready for Stage 5")
    print("Next: verify GitBook rendered correctly, then build stage5_run.py")
