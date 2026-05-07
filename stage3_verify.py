#!/usr/bin/env python3
"""
Stage 3 - Verification
Dynamically discovers all tutorial_NN and howto_NN files.
Pure stdlib — no external dependencies.

Usage: python3 stage3_verify.py 03_diataxis/output/x200_101
"""

import sys
import os
import re

if len(sys.argv) < 2:
    print("Usage: python3 stage3_verify.py 03_diataxis/output/x200_101")
    sys.exit(1)

PREFIX       = sys.argv[1]
OUTPUT_DIR   = os.path.dirname(PREFIX)
OBJECTIVE_ID = os.path.basename(PREFIX)

print(f"Stage 3 - Verification")
print(f"Prefix: {PREFIX}")
print()

EXPLANATION_PATH = f"{PREFIX}_explanation.md"
REFERENCE_PATH   = f"{PREFIX}_reference.md"

tutorial_paths = sorted([
    os.path.join(OUTPUT_DIR, f)
    for f in os.listdir(OUTPUT_DIR)
    if f.startswith(f"{OBJECTIVE_ID}_tutorial_") and f.endswith(".md")
])

howto_paths = sorted([
    os.path.join(OUTPUT_DIR, f)
    for f in os.listdir(OUTPUT_DIR)
    if f.startswith(f"{OBJECTIVE_ID}_howto_") and f.endswith(".md")
])

print(f"  Found: 1 explanation, {len(tutorial_paths)} tutorial(s), {len(howto_paths)} how-to(s), 1 reference")

missing = []
if not os.path.exists(EXPLANATION_PATH):
    missing.append(EXPLANATION_PATH)
if not os.path.exists(REFERENCE_PATH):
    missing.append(REFERENCE_PATH)
if not tutorial_paths:
    missing.append(f"{PREFIX}_tutorial_01.md (no tutorials found)")
if not howto_paths:
    missing.append(f"{PREFIX}_howto_01.md (no how-tos found)")

if missing:
    for m in missing:
        print(f"  ERROR: Missing: {m}")
    print()
    print("VERIFICATION FAILED — required documents not present")
    sys.exit(1)

def load(path):
    with open(path, encoding="utf-8") as f:
        return f.read()

explanation = load(EXPLANATION_PATH)
reference   = load(REFERENCE_PATH)
tutorials   = [(p, load(p)) for p in tutorial_paths]
howtos      = [(p, load(p)) for p in howto_paths]

passes   = []
failures = []

# ── EXPLANATION ───────────────────────────────────────────────────────────────

exp = explanation

if re.search(r'^type:\s*explanation', exp, re.MULTILINE):
    passes.append("explanation: type field correct")
else:
    failures.append("FAIL explanation: wrong or missing type field")

if len(exp) >= 3000:
    passes.append(f"explanation: substantial ({len(exp):,} chars)")
else:
    failures.append(f"FAIL explanation: too short ({len(exp):,} chars) — expected ≥3000")

markers = ["## Background", "## How", "## Why", "## Design",
           "## Trade-off", "## Misconception", "## Relationship", "## Key Concept"]
found = [m for m in markers if m in exp]
if len(found) >= 2:
    passes.append(f"explanation: {len(found)} conceptual sections ({', '.join(found)})")
else:
    failures.append(f"FAIL explanation: only {len(found)} conceptual sections — need ≥2")

step_contam = re.findall(
    r'(?m)^#{1,3} Step \d|^\d+\. (?:Run|Type|Execute|Enter|Open|Press|Click)', exp)
if not step_contam:
    passes.append("explanation: no step-by-step contamination")
else:
    failures.append(f"FAIL explanation: instruction contamination: {step_contam[:3]}")

if "<!-- Source:" not in exp:
    passes.append("explanation: no source comments leaked")
else:
    failures.append("FAIL explanation: <!-- Source: --> comments present — strip before publishing")

if any(s in exp for s in ["## Further Reading", "## See Also", "## Related"]):
    passes.append("explanation: cross-reference section present")
else:
    failures.append("FAIL explanation: no Further Reading / See Also section")

# ── TUTORIALS (per file) ──────────────────────────────────────────────────────

for path, tut in tutorials:
    label = os.path.basename(path).replace(".md", "")

    if re.search(r'^type:\s*tutorial', tut, re.MULTILINE):
        passes.append(f"{label}: type field correct")
    else:
        failures.append(f"FAIL {label}: wrong or missing type field")

    if len(tut) >= 2000:
        passes.append(f"{label}: substantial ({len(tut):,} chars)")
    else:
        failures.append(f"FAIL {label}: too short ({len(tut):,} chars) — expected ≥2000")

    steps = re.findall(r'(?m)^#{1,3} Step \d+', tut)
    if len(steps) >= 3:
        passes.append(f"{label}: {len(steps)} numbered steps")
    else:
        failures.append(f"FAIL {label}: only {len(steps)} steps — need ≥3")

    yss = len(re.findall(r'You should see', tut, re.IGNORECASE))
    min_yss = max(1, len(steps) // 2)
    if yss >= min_yss:
        passes.append(f"{label}: 'You should see:' {yss}x")
    else:
        failures.append(f"FAIL {label}: 'You should see:' only {yss}x for {len(steps)} steps")

    if any(s in tut for s in ["## Prerequisites", "## Before"]):
        passes.append(f"{label}: Prerequisites present")
    else:
        failures.append(f"FAIL {label}: no Prerequisites section")

    if any(s in tut for s in ["## What We", "## Summary", "## Next Steps"]):
        passes.append(f"{label}: closing summary present")
    else:
        failures.append(f"FAIL {label}: no closing summary")

    if "<!-- Source:" not in tut:
        passes.append(f"{label}: no source comments leaked")
    else:
        failures.append(f"FAIL {label}: <!-- Source: --> comments present")

# ── HOW-TOS (per file) ────────────────────────────────────────────────────────

for path, howto in howtos:
    label = os.path.basename(path).replace(".md", "")

    if re.search(r'^type:\s*how-to', howto, re.MULTILINE):
        passes.append(f"{label}: type field correct")
    else:
        failures.append(f"FAIL {label}: wrong or missing type field")

    if len(howto) >= 1000:
        passes.append(f"{label}: content present ({len(howto):,} chars)")
    else:
        failures.append(f"FAIL {label}: too short ({len(howto):,} chars) — expected ≥1000")

    steps = re.findall(r'(?m)^#{2,3} (?:Step )?\d+', howto)
    if len(steps) >= 2:
        passes.append(f"{label}: {len(steps)} procedural steps")
    else:
        failures.append(f"FAIL {label}: only {len(steps)} steps — need ≥2")

    if any(s in howto for s in ["## Verification", "## Verify"]):
        passes.append(f"{label}: Verification section present")
    else:
        failures.append(f"FAIL {label}: no Verification section")

    if any(s in howto for s in ["## Troubleshooting", "## Trouble"]):
        passes.append(f"{label}: Troubleshooting section present")
    else:
        failures.append(f"FAIL {label}: no Troubleshooting section")

    if "<!-- Source:" not in howto:
        passes.append(f"{label}: no source comments leaked")
    else:
        failures.append(f"FAIL {label}: <!-- Source: --> comments present")

    teaching = re.findall(
        r"In this tutorial|we will learn|you will learn|Let's learn|Now we'll",
        howto, re.IGNORECASE)
    if not teaching:
        passes.append(f"{label}: no tutorial-style framing")
    else:
        failures.append(f"FAIL {label}: tutorial framing found: {teaching[:2]}")

    if re.search(r'^difficulty:', howto, re.MULTILINE):
        passes.append(f"{label}: difficulty field present")
    else:
        failures.append(f"FAIL {label}: no difficulty field in frontmatter")

# ── REFERENCE ────────────────────────────────────────────────────────────────

ref = reference

if re.search(r'^type:\s*reference', ref, re.MULTILINE):
    passes.append("reference: type field correct")
else:
    failures.append("FAIL reference: wrong or missing type field")

if len(ref) >= 2000:
    passes.append(f"reference: substantial ({len(ref):,} chars)")
else:
    failures.append(f"FAIL reference: too short ({len(ref):,} chars) — expected ≥2000")

table_rows = len(re.findall(r'(?m)^\|', ref))
if table_rows >= 10:
    passes.append(f"reference: table-heavy ({table_rows} rows)")
else:
    failures.append(f"FAIL reference: too few table rows ({table_rows}) — expected ≥10")

if any(s in ref for s in ["## Syntax", "## Command Syntax", "## Usage"]):
    passes.append("reference: Syntax section present")
else:
    failures.append("FAIL reference: no Syntax section")

if any(s in ref for s in ["## Examples", "## Example"]):
    passes.append("reference: Examples section present")
else:
    failures.append("FAIL reference: no Examples section")

if "<!-- Source:" not in ref:
    passes.append("reference: no source comments leaked")
else:
    failures.append("FAIL reference: <!-- Source: --> comments present")

instr = re.findall(
    r'(?m)^To (?:use|run|execute|configure|set up)|^First,|^Next,|^Then,|^Finally,', ref)
if not instr:
    passes.append("reference: no instructional contamination")
else:
    failures.append(f"FAIL reference: instructional language: {instr[:3]}")

# ── CROSS-DOCUMENT ────────────────────────────────────────────────────────────

all_docs = {"explanation": explanation, "reference": reference}
for p, c in tutorials:
    all_docs[os.path.basename(p)] = c
for p, c in howtos:
    all_docs[os.path.basename(p)] = c

obj_ids = {}
for lbl, content in all_docs.items():
    m = re.search(r'exam_objective:\s*["\']?(\S+?)["\']?\s*$', content, re.MULTILINE)
    if m:
        obj_ids[lbl] = m.group(1).strip('"\'')

if len(set(obj_ids.values())) == 1:
    passes.append(f"cross-doc: consistent exam_objective ({list(obj_ids.values())[0]})")
elif obj_ids:
    failures.append(f"FAIL cross-doc: inconsistent exam_objective: {obj_ids}")
else:
    failures.append("FAIL cross-doc: exam_objective missing from all files")

for lbl, content in all_docs.items():
    if re.search(r'^status:\s*draft', content, re.MULTILINE):
        passes.append(f"cross-doc: {lbl} status is draft")
    else:
        m2 = re.search(r'^status:\s*(\S+)', content, re.MULTILINE)
        status = m2.group(1) if m2 else "missing"
        failures.append(f"FAIL cross-doc: {lbl} status is '{status}' — should be draft")

difficulties = []
for p, howto in howtos:
    m = re.search(r'^difficulty:\s*(\S+)', howto, re.MULTILINE)
    if m:
        difficulties.append(m.group(1))
if difficulties:
    passes.append(f"cross-doc: how-to difficulty progression: {difficulties}")

exp_words = len(explanation.split())
if exp_words >= 800:
    passes.append(f"cross-doc: explanation word count adequate ({exp_words} words)")
else:
    failures.append(f"FAIL cross-doc: explanation too short ({exp_words} words) — expected ≥800")

# ── REPORT ────────────────────────────────────────────────────────────────────

total = len(passes) + len(failures)
print()
print(f"Results: {len(passes)}/{total} passed, {len(failures)} failed")
print()

for p in passes:
    print(f"  ✓ {p}")

if failures:
    print()
    for f_msg in failures:
        print(f"  ✗ {f_msg}")
    print()
    print("VERIFICATION FAILED — fix issues before Stage 4")
    sys.exit(1)
else:
    print()
    total_docs = 2 + len(tutorials) + len(howtos)
    print(f"VERIFICATION PASSED — {total_docs} documents ready for Stage 4")
    print(f"  1 explanation  |  {len(tutorials)} tutorial(s)  |  {len(howtos)} how-to(s)  |  1 reference")
    print(f"Next: commit and push, then build stage4_run.py")
