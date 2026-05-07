#!/usr/bin/env python3
"""
Stage 2 - Verification
Validates Stage 2 output before passing to Stage 3.
Usage: python3 stage2_verify.py 02_map/output/x200_101_mapped-passages.md
"""

import sys
import os
import re

OUTPUT_FILE = sys.argv[1] if len(sys.argv) > 1 else None

if not OUTPUT_FILE:
    print("Usage: python3 stage2_verify.py <output_file>")
    sys.exit(1)

if not os.path.exists(OUTPUT_FILE):
    print(f"ERROR: File not found: {OUTPUT_FILE}")
    sys.exit(1)

print(f"Stage 2 - Verification")
print(f"File: {OUTPUT_FILE}")
print()

with open(OUTPUT_FILE, encoding="utf-8") as f:
    content = f.read()

passes = []
failures = []

# ── Check 1: Objective header present ────────────────────────────────────────
if content.startswith("# Mapped Passages:"):
    passes.append("Objective header present")
else:
    failures.append("FAIL: Missing '# Mapped Passages:' header — wrong file or corrupt output")

# ── Check 2: File is non-empty ────────────────────────────────────────────────
if len(content) > 1000:
    passes.append(f"File non-empty ({len(content):,} chars)")
else:
    failures.append(f"FAIL: File too small ({len(content)} chars) — possible empty extraction")

# ── Check 3: Passage count sufficient ────────────────────────────────────────
source_comments = re.findall(r'<!-- Source:', content)
passage_count = len(source_comments)
if passage_count >= 10:
    passes.append(f"Passage count sufficient ({passage_count} passages)")
elif passage_count >= 1:
    failures.append(f"FAIL: Too few passages ({passage_count}) — possible over-filtering or wrong objective")
else:
    failures.append("FAIL: Zero passages — extraction completely failed")

# ── Check 4: Source attribution present ──────────────────────────────────────
if passage_count > 0:
    passes.append("Source attribution comments present")
else:
    failures.append("FAIL: No source attribution comments found")

# ── Check 5: Multiple source files represented ───────────────────────────────
sources = re.findall(r'<!-- Source: ([^>]+) -->', content)
unique_sources = set(os.path.basename(s.strip()) for s in sources)
if len(unique_sources) >= 3:
    passes.append(f"Multiple source files represented ({len(unique_sources)} files)")
elif len(unique_sources) >= 1:
    passes.append(f"Source files represented ({len(unique_sources)} file(s)) — consider adding more sources")
else:
    failures.append("FAIL: No source files identifiable")

# ── Check 6: Extraction summary present ──────────────────────────────────────
if "## Extraction Summary" in content:
    passes.append("Extraction summary present")
else:
    failures.append("FAIL: Missing extraction summary — script may have crashed before completion")

# ── Check 7: Batch ID recorded ───────────────────────────────────────────────
if "Batch ID:" in content and "msgbatch_" in content:
    batch_id = re.search(r'msgbatch_\w+', content)
    passes.append(f"Batch ID recorded ({batch_id.group() if batch_id else 'found'})")
else:
    failures.append("FAIL: No batch ID in extraction summary — traceability broken")

# ── Check 8: No template placeholders leaked in ───────────────────────────────
placeholders = re.findall(r'\[placeholder\]|\[fill this in\]|\[TOPIC\]|\[OBJECTIVE\]', content, re.I)
if not placeholders:
    passes.append("No template placeholders in output")
else:
    failures.append(f"FAIL: Template placeholders found: {placeholders[:3]} — template content leaked into output")

# ── Check 9: Content word density ────────────────────────────────────────────
# Strip headers and source comments, check remaining content
body = re.sub(r'#.*\n', '', content)
body = re.sub(r'<!--.*?-->', '', body)
body = re.sub(r'\*\*.*?\*\*', '', body)
word_count = len(body.split())
if word_count >= 500:
    passes.append(f"Content word count sufficient ({word_count:,} words)")
else:
    failures.append(f"FAIL: Too few words ({word_count}) — insufficient content for Stage 3 Diataxis transformation")

# ── Check 10: No Diataxis content leaked in ───────────────────────────────────
diataxis_markers = ["## Background", "## How ", "## Why This", "## Trade-offs",
                    "## Step 1", "## Prerequisites", "You should see:"]
leaked = [m for m in diataxis_markers if m in content]
if not leaked:
    passes.append("No Stage 3 Diataxis content in Stage 2 output")
else:
    failures.append(f"FAIL: Diataxis content found: {leaked} — Stage 3 template content leaked into Stage 2 output")

# ── Report ────────────────────────────────────────────────────────────────────
print(f"Results: {len(passes)} passed, {len(failures)} failed")
print()

for p in passes:
    print(f"  ✓ {p}")

if failures:
    print()
    for f in failures:
        print(f"  ✗ {f}")
    print()
    print("VERIFICATION FAILED — fix issues before running Stage 3")
    sys.exit(1)
else:
    print()
    # Show summary stats from extraction summary
    total_match = re.search(r'Total paragraphs classified: (\d+)', content)
    relevant_match = re.search(r'Passages classified RELEVANT: (\d+)', content)
    if total_match and relevant_match:
        total = int(total_match.group(1))
        relevant = int(relevant_match.group(1))
        print(f"  Stats: {relevant}/{total} paragraphs ({100*relevant/total:.1f}%) mapped to objective")
    print()
    print(f"VERIFICATION PASSED — ready for Stage 3")
    print(f"Next: python3 stage3_run.py {OUTPUT_FILE}")
