#!/usr/bin/env python3
"""
Stage 2 - Verification
Validates Stage 2 output before passing to Stage 3.

Checks:
  1.  Objective header present
  2.  File non-empty
  3.  Passage count sufficient (>= 10)
  4.  Source attribution comments present
  5.  Multiple source files represented
  6.  Extraction summary present
  7.  Batch ID recorded
  8.  No template placeholders leaked
  9.  Content word count sufficient
  10. No Stage 3 Diataxis content leaked in

Pure stdlib — no external dependencies.

Usage:
  python3 stage2_verify.py 02_map/output/x200_103/x200_103_mapped-passages.md
"""

import sys
import os
import re

if len(sys.argv) < 2:
    print("Usage: python3 stage2_verify.py 02_map/output/x200_103/x200_103_mapped-passages.md")
    sys.exit(1)

OUTPUT_FILE = sys.argv[1]

if not os.path.exists(OUTPUT_FILE):
    print("ERROR: File not found: " + OUTPUT_FILE)
    sys.exit(1)

print("Stage 2 - Verification")
print("File: " + OUTPUT_FILE)
print()

with open(OUTPUT_FILE, encoding="utf-8") as f:
    content = f.read()

passes   = []
failures = []

# ── Check 1: Objective header ─────────────────────────────────────────────────
if content.startswith("# Mapped Passages:"):
    passes.append("objective header present")
else:
    failures.append("missing '# Mapped Passages:' header — wrong file or corrupt output")

# ── Check 2: File non-empty ───────────────────────────────────────────────────
if len(content) > 1000:
    passes.append("file non-empty (" + str(len(content)) + " chars)")
else:
    failures.append("file too small (" + str(len(content))
                    + " chars) — possible empty extraction")

# ── Check 3: Passage count ────────────────────────────────────────────────────
source_comments = re.findall(r'<!-- Source:', content)
passage_count   = len(source_comments)
if passage_count >= 10:
    passes.append("passage count sufficient (" + str(passage_count) + " passages)")
elif passage_count >= 1:
    failures.append("too few passages (" + str(passage_count)
                    + ") — possible over-filtering or wrong objective")
else:
    failures.append("zero passages — extraction completely failed")

# ── Check 4: Source attribution ───────────────────────────────────────────────
if passage_count > 0:
    passes.append("source attribution comments present")
else:
    failures.append("no source attribution comments found")

# ── Check 5: Multiple source files ───────────────────────────────────────────
sources        = re.findall(r'<!-- Source: ([^>]+) -->', content)
unique_sources = set(os.path.basename(s.strip()) for s in sources)
if len(unique_sources) >= 3:
    passes.append("multiple source files represented ("
                  + str(len(unique_sources)) + " files)")
elif len(unique_sources) >= 1:
    passes.append("source files represented (" + str(len(unique_sources))
                  + " file(s)) — consider adding more sources")
else:
    failures.append("no source files identifiable")

# ── Check 6: Extraction summary ───────────────────────────────────────────────
if "## Extraction Summary" in content:
    passes.append("extraction summary present")
else:
    failures.append("missing extraction summary — script may have crashed before completion")

# ── Check 7: Batch ID ─────────────────────────────────────────────────────────
if "Batch ID:" in content and "msgbatch_" in content:
    batch_id = re.search(r'msgbatch_\w+', content)
    passes.append("batch ID recorded ("
                  + (batch_id.group() if batch_id else "found") + ")")
else:
    failures.append("no batch ID in extraction summary — traceability broken")

# ── Check 8: No template placeholders ────────────────────────────────────────
placeholders = re.findall(
    r'\[placeholder\]|\[fill this in\]|\[TOPIC\]|\[OBJECTIVE\]',
    content, re.I
)
if not placeholders:
    passes.append("no template placeholders in output")
else:
    failures.append("template placeholders found: "
                    + str(placeholders[:3]) + " — template content leaked into output")

# ── Check 9: Content word count ───────────────────────────────────────────────
body       = re.sub(r'#.*\n', '', content)
body       = re.sub(r'<!--.*?-->', '', body)
body       = re.sub(r'\*\*.*?\*\*', '', body)
word_count = len(body.split())
if word_count >= 500:
    passes.append("content word count sufficient (" + str(word_count) + " words)")
else:
    failures.append("too few words (" + str(word_count)
                    + ") — insufficient content for Stage 3 transformation")

# ── Check 10: No Diataxis content leaked in ───────────────────────────────────
diataxis_markers = [
    "## Background", "## How ", "## Why This", "## Trade-offs",
    "## Step 1", "## Prerequisites", "You should see:",
]
leaked = [m for m in diataxis_markers if m in content]
if not leaked:
    passes.append("no Stage 3 Diataxis content in Stage 2 output")
else:
    failures.append("Diataxis content found: " + str(leaked)
                    + " — Stage 3 template content leaked into Stage 2 output")

# ── Report ────────────────────────────────────────────────────────────────────

total = len(passes) + len(failures)
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
    print("VERIFICATION FAILED — fix issues before running Stage 3")
    sys.exit(1)
else:
    print()
    # Display stats from extraction summary
    total_match    = re.search(r'Total paragraphs classified: (\d+)', content)
    relevant_match = re.search(r'Paragraphs classified RELEVANT: (\d+)', content)
    if total_match and relevant_match:
        t = int(total_match.group(1))
        r = int(relevant_match.group(1))
        print("  Stats: " + str(r) + "/" + str(t)
              + " paragraphs (" + str(round(100 * r / t, 1)) + "%) mapped to objective")
    print()
    print("VERIFICATION PASSED — ready for Stage 3")
    print("Next: python3 stage3_run.py "
          + os.path.dirname(OUTPUT_FILE).replace("02_map/output/", "02_map/output/")
          + "/" + os.path.basename(OUTPUT_FILE))
