#!/usr/bin/env python3
"""
Stage 3 - Verification
Validates all Stage 3 Diataxis output documents before passing to Stage 4.
Dynamically discovers all tutorial_NN and howto_NN files.

Checks per document type:
  Explanation: type field, substance, conceptual sections, no contamination,
               no source comments, cross-reference section
  Tutorial:    type field, substance, numbered steps, 'You should see:',
               prerequisites, closing summary, no source comments
  How-to:      type field, substance, procedural steps, verification,
               troubleshooting, no source comments, no tutorial framing,
               difficulty field
  Reference:   type field, substance, table density, syntax section,
               examples section, no source comments, no instructional language

Cross-document: consistent exam_objective, draft status, difficulty progression,
                adequate explanation word count

Pure stdlib — no external dependencies.

Usage:
  python3 stage3_verify.py 03_diataxis/output/x200_103/x200_103
"""

import sys
import os
import re

if len(sys.argv) < 2:
    print("Usage: python3 stage3_verify.py 03_diataxis/output/x200_103/x200_103")
    sys.exit(1)

PREFIX       = sys.argv[1]
OUTPUT_DIR   = os.path.dirname(PREFIX)
OBJECTIVE_ID = os.path.basename(PREFIX)

print("Stage 3 - Verification")
print("Prefix: " + PREFIX)
print()

EXPLANATION_PATH = PREFIX + "_explanation.md"
REFERENCE_PATH   = PREFIX + "_reference.md"

tutorial_paths = sorted([
    os.path.join(OUTPUT_DIR, f)
    for f in os.listdir(OUTPUT_DIR)
    if f.startswith(OBJECTIVE_ID + "_tutorial_") and f.endswith(".md")
])

howto_paths = sorted([
    os.path.join(OUTPUT_DIR, f)
    for f in os.listdir(OUTPUT_DIR)
    if f.startswith(OBJECTIVE_ID + "_howto_") and f.endswith(".md")
])

print("  Found: 1 explanation, " + str(len(tutorial_paths)) + " tutorial(s), "
      + str(len(howto_paths)) + " how-to(s), 1 reference")

missing = []
if not os.path.exists(EXPLANATION_PATH):
    missing.append(EXPLANATION_PATH)
if not os.path.exists(REFERENCE_PATH):
    missing.append(REFERENCE_PATH)
if not tutorial_paths:
    missing.append(PREFIX + "_tutorial_01.md (no tutorials found)")
if not howto_paths:
    missing.append(PREFIX + "_howto_01.md (no how-tos found)")

if missing:
    for m in missing:
        print("  ERROR: Missing: " + m)
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
    failures.append("explanation: wrong or missing type field")

if len(exp) >= 3000:
    passes.append("explanation: substantial (" + str(len(exp)) + " chars)")
else:
    failures.append("explanation: too short (" + str(len(exp)) + " chars) — expected >= 3000")

markers = ["## Background", "## How", "## Why", "## Design",
           "## Trade-off", "## Misconception", "## Relationship", "## Key Concept"]
found = [m for m in markers if m in exp]
if len(found) >= 2:
    passes.append("explanation: " + str(len(found)) + " conceptual sections ("
                  + ", ".join(found) + ")")
else:
    failures.append("explanation: only " + str(len(found))
                    + " conceptual sections — need >= 2")

step_contam = re.findall(
    r'(?m)^#{1,3} Step \d|^\d+\. (?:Run|Type|Execute|Enter|Open|Press|Click)', exp)
if not step_contam:
    passes.append("explanation: no step-by-step contamination")
else:
    failures.append("explanation: instruction contamination: " + str(step_contam[:3]))

if "<!-- Source:" not in exp:
    passes.append("explanation: no source comments leaked")
else:
    failures.append("explanation: <!-- Source: --> comments present — strip before publishing")

if any(s in exp for s in ["## Further Reading", "## See Also", "## Related"]):
    passes.append("explanation: cross-reference section present")
else:
    failures.append("explanation: no Further Reading / See Also section")

# ── TUTORIALS ─────────────────────────────────────────────────────────────────

for path, tut in tutorials:
    label = os.path.basename(path).replace(".md", "")

    if re.search(r'^type:\s*tutorial', tut, re.MULTILINE):
        passes.append(label + ": type field correct")
    else:
        failures.append(label + ": wrong or missing type field")

    if len(tut) >= 2000:
        passes.append(label + ": substantial (" + str(len(tut)) + " chars)")
    else:
        failures.append(label + ": too short (" + str(len(tut)) + " chars) — expected >= 2000")

    steps   = re.findall(r'(?m)^#{1,3} Step \d+', tut)
    min_yss = max(1, len(steps) // 2)
    if len(steps) >= 3:
        passes.append(label + ": " + str(len(steps)) + " numbered steps")
    else:
        failures.append(label + ": only " + str(len(steps)) + " steps — need >= 3")

    yss = len(re.findall(r'You should see', tut, re.IGNORECASE))
    if yss >= min_yss:
        passes.append(label + ": 'You should see:' " + str(yss) + "x")
    else:
        failures.append(label + ": 'You should see:' only " + str(yss)
                        + "x for " + str(len(steps)) + " steps")

    if any(s in tut for s in ["## Prerequisites", "## Before"]):
        passes.append(label + ": Prerequisites present")
    else:
        failures.append(label + ": no Prerequisites section")

    if any(s in tut for s in ["## What We", "## Summary", "## Next Steps"]):
        passes.append(label + ": closing summary present")
    else:
        failures.append(label + ": no closing summary")

    if "<!-- Source:" not in tut:
        passes.append(label + ": no source comments leaked")
    else:
        failures.append(label + ": <!-- Source: --> comments present")

# ── HOW-TOS ───────────────────────────────────────────────────────────────────

for path, howto in howtos:
    label = os.path.basename(path).replace(".md", "")

    if re.search(r'^type:\s*how-to', howto, re.MULTILINE):
        passes.append(label + ": type field correct")
    else:
        failures.append(label + ": wrong or missing type field")

    if len(howto) >= 1000:
        passes.append(label + ": content present (" + str(len(howto)) + " chars)")
    else:
        failures.append(label + ": too short (" + str(len(howto))
                        + " chars) — expected >= 1000")

    steps = re.findall(r'(?m)^#{2,3} (?:Step )?\d+', howto)
    if len(steps) >= 2:
        passes.append(label + ": " + str(len(steps)) + " procedural steps")
    else:
        failures.append(label + ": only " + str(len(steps)) + " steps — need >= 2")

    if any(s in howto for s in ["## Verification", "## Verify"]):
        passes.append(label + ": Verification section present")
    else:
        failures.append(label + ": no Verification section")

    if any(s in howto for s in ["## Troubleshooting", "## Trouble"]):
        passes.append(label + ": Troubleshooting section present")
    else:
        failures.append(label + ": no Troubleshooting section")

    if "<!-- Source:" not in howto:
        passes.append(label + ": no source comments leaked")
    else:
        failures.append(label + ": <!-- Source: --> comments present")

    teaching = re.findall(
        r"In this tutorial|we will learn|you will learn|Let's learn|Now we'll",
        howto, re.IGNORECASE)
    if not teaching:
        passes.append(label + ": no tutorial-style framing")
    else:
        failures.append(label + ": tutorial framing found: " + str(teaching[:2]))

    if re.search(r'^difficulty:', howto, re.MULTILINE):
        passes.append(label + ": difficulty field present")
    else:
        failures.append(label + ": no difficulty field in frontmatter")

# ── REFERENCE ────────────────────────────────────────────────────────────────

ref = reference

if re.search(r'^type:\s*reference', ref, re.MULTILINE):
    passes.append("reference: type field correct")
else:
    failures.append("reference: wrong or missing type field")

if len(ref) >= 2000:
    passes.append("reference: substantial (" + str(len(ref)) + " chars)")
else:
    failures.append("reference: too short (" + str(len(ref)) + " chars) — expected >= 2000")

table_rows = len(re.findall(r'(?m)^\|', ref))
if table_rows >= 10:
    passes.append("reference: table-heavy (" + str(table_rows) + " rows)")
else:
    failures.append("reference: too few table rows (" + str(table_rows) + ") — expected >= 10")

if any(s in ref for s in ["## Syntax", "## Command Syntax", "## Usage"]):
    passes.append("reference: Syntax section present")
else:
    failures.append("reference: no Syntax section")

if any(s in ref for s in ["## Examples", "## Example"]):
    passes.append("reference: Examples section present")
else:
    failures.append("reference: no Examples section")

if "<!-- Source:" not in ref:
    passes.append("reference: no source comments leaked")
else:
    failures.append("reference: <!-- Source: --> comments present")

instr = re.findall(
    r'(?m)^To (?:use|run|execute|configure|set up)|^First,|^Next,|^Then,|^Finally,', ref)
if not instr:
    passes.append("reference: no instructional contamination")
else:
    failures.append("reference: instructional language: " + str(instr[:3]))

# ── CROSS-DOCUMENT ────────────────────────────────────────────────────────────

all_docs = {"explanation": explanation, "reference": reference}
for p, c in tutorials:
    all_docs[os.path.basename(p)] = c
for p, c in howtos:
    all_docs[os.path.basename(p)] = c

# Consistent exam_objective across all documents
obj_ids = {}
for lbl, content in all_docs.items():
    m = re.search(r'exam_objective:\s*["\']?(\S+?)["\']?\s*$', content, re.MULTILINE)
    if m:
        obj_ids[lbl] = m.group(1).strip("\"'")

if len(set(obj_ids.values())) == 1:
    passes.append("cross-doc: consistent exam_objective ("
                  + list(obj_ids.values())[0] + ")")
elif obj_ids:
    failures.append("cross-doc: inconsistent exam_objective: " + str(obj_ids))
else:
    failures.append("cross-doc: exam_objective missing from all files")

# Draft status on all documents
for lbl, content in all_docs.items():
    if re.search(r'^status:\s*draft', content, re.MULTILINE):
        passes.append("cross-doc: " + lbl + " status is draft")
    else:
        m2     = re.search(r'^status:\s*(\S+)', content, re.MULTILINE)
        status = m2.group(1) if m2 else "missing"
        failures.append("cross-doc: " + lbl + " status is '"
                        + status + "' — should be draft")

# How-to difficulty progression
difficulties = []
for p, howto in howtos:
    m = re.search(r'^difficulty:\s*(\S+)', howto, re.MULTILINE)
    if m:
        difficulties.append(m.group(1))
if difficulties:
    passes.append("cross-doc: how-to difficulty progression: " + str(difficulties))

# Explanation word count
exp_words = len(explanation.split())
if exp_words >= 800:
    passes.append("cross-doc: explanation word count adequate (" + str(exp_words) + " words)")
else:
    failures.append("cross-doc: explanation too short (" + str(exp_words)
                    + " words) — expected >= 800")

# ── REPORT ────────────────────────────────────────────────────────────────────

total = len(passes) + len(failures)
print()
print("Results: " + str(len(passes)) + "/" + str(total)
      + " passed, " + str(len(failures)) + " failed")
print()

for p in passes:
    print("  \u2713 " + p)

if failures:
    print()
    for f in failures:
        print("  \u2717 " + f)
    print()
    print("VERIFICATION FAILED — fix issues before Stage 4")
    sys.exit(1)
else:
    total_docs = 2 + len(tutorials) + len(howtos)
    print()
    print("VERIFICATION PASSED — " + str(total_docs) + " documents ready for Stage 4")
    print("  1 explanation  |  " + str(len(tutorials)) + " tutorial(s)  |  "
          + str(len(howtos)) + " how-to(s)  |  1 reference")
    print("Next: python3 stage4_run.py " + OBJECTIVE_ID)
