#!/usr/bin/env python3
"""
Stage 2 - Objective Map
Classifies all paragraphs from Stage 1 output against a selected exam objective.
Uses Haiku 4.5 Batch API — one request per paragraph, no pre-filtering.

Output: one *_mapped-passages.md file written to 02_map/output/<objective_id>/

Usage:
  python3 stage2_run.py _config/exam-objectives/x200_103.md
"""

import sys
import os
import re
import json
import time
from datetime import date
import anthropic

# ── Config ────────────────────────────────────────────────────────────────────

if len(sys.argv) < 2:
    print("Usage: python3 stage2_run.py _config/exam-objectives/x200_103.md")
    sys.exit(1)

OBJECTIVE_FILE = sys.argv[1]

if not os.path.exists(OBJECTIVE_FILE):
    print("ERROR: Objective file not found: " + OBJECTIVE_FILE)
    sys.exit(1)

objective_id = os.path.splitext(os.path.basename(OBJECTIVE_FILE))[0]
CLEAN_DIR    = "01_normalize/output/" + objective_id
OUTPUT_DIR   = "02_map/output/"       + objective_id

if not os.path.isdir(CLEAN_DIR):
    print("ERROR: Stage 1 output directory not found: " + CLEAN_DIR)
    print("Run Stage 1 first: python3 stage1_run.py " + objective_id)
    sys.exit(1)

os.makedirs(OUTPUT_DIR, exist_ok=True)
output_path = OUTPUT_DIR + "/" + objective_id + "_mapped-passages.md"

print("Stage 2 - Objective Map")
print("Objective:  " + OBJECTIVE_FILE)
print("Source dir: " + CLEAN_DIR)
print("Output:     " + output_path)
print()

# ── Load objective ────────────────────────────────────────────────────────────

with open(OBJECTIVE_FILE, encoding="utf-8") as f:
    objective_content = f.read()

objective_title = objective_content.splitlines()[0].strip().lstrip("# ")
print("Objective: " + objective_title)

# ── Load all paragraphs from Stage 1 output ───────────────────────────────────

print("\nLoading paragraphs from " + CLEAN_DIR + "...")

clean_files = sorted([
    f for f in os.listdir(CLEAN_DIR)
    if f.endswith("_clean.md")
])

if not clean_files:
    print("ERROR: No *_clean.md files found in " + CLEAN_DIR)
    print("Run Stage 1 first: python3 stage1_run.py " + objective_id)
    sys.exit(1)

all_paragraphs = []  # list of (source_file, paragraph_text)

for filename in clean_files:
    filepath = os.path.join(CLEAN_DIR, filename)
    with open(filepath, encoding="utf-8") as f:
        content = f.read()
    paras = [
        p.strip() for p in content.split("\n\n")
        if p.strip() and not p.startswith("<!--")
    ]
    for p in paras:
        all_paragraphs.append((filepath, p))

print("  Files loaded: " + str(len(clean_files)))
print("  Total paragraphs: " + str(len(all_paragraphs)))

est_input_tokens = len(all_paragraphs) * 250
est_cost         = (est_input_tokens / 1_000_000) * 0.50
print("  Estimated cost: ~$" + str(round(est_cost, 3)) + " (Haiku Batch pricing)")
print()

# ── Haiku 4.5 Batch classification ───────────────────────────────────────────

print("Classifying paragraphs via Haiku 4.5 Batch API...")

SYSTEM_PROMPT = (
    "You are a relevance classifier for RHCSA Linux certification study material.\n\n"
    "You will receive a paragraph from a study source. Determine whether it is "
    "relevant to the following RHCSA exam objective:\n\n"
    "OBJECTIVE:\n" + objective_content[:2000] + "\n\n"
    "---\n\n"
    "RELEVANT: The paragraph directly addresses this objective, covers a required "
    "prerequisite concept, explains a command or procedure this objective tests, "
    "or describes a failure mode when executing this objective.\n\n"
    "IRRELEVANT: The paragraph is about a completely different topic, covers a "
    "different exam objective, or is general content with no specific connection "
    "to this objective.\n\n"
    "When uncertain: classify as RELEVANT.\n\n"
    "Respond with ONLY valid JSON on a single line, no markdown fences:\n"
    '{"r": 1} for RELEVANT or {"r": 0} for IRRELEVANT'
)

client   = anthropic.Anthropic()
requests = []

for i, (source_file, para_text) in enumerate(all_paragraphs):
    truncated = para_text[:1500] if len(para_text) > 1500 else para_text
    requests.append({
        "custom_id": "p-" + str(i),
        "params": {
            "model":      "claude-haiku-4-5-20251001",
            "max_tokens": 16,
            "system":     SYSTEM_PROMPT,
            "messages":   [{"role": "user", "content": truncated}]
        }
    })

print("  Submitting " + str(len(requests)) + " batch requests...")
batch = client.messages.batches.create(requests=requests)
print("  Batch ID: " + batch.id)

print("  Polling...", end="", flush=True)
while True:
    status = client.messages.batches.retrieve(batch.id)
    if status.processing_status == "ended":
        break
    print(".", end="", flush=True)
    time.sleep(15)
print(" done")

# ── Collect results ───────────────────────────────────────────────────────────

relevant_indices = set()
parse_errors     = 0

for result in client.messages.batches.results(batch.id):
    idx = int(result.custom_id.split("-")[1])

    if result.result.type != "succeeded":
        relevant_indices.add(idx)  # keep on failure
        continue

    raw   = result.result.message.content[0].text.strip()
    lines = raw.splitlines()
    if lines and lines[0].startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].strip() == "```":
        lines = lines[:-1]

    json_line = next((l for l in lines if l.strip().startswith("{")), None)
    if not json_line:
        parse_errors += 1
        relevant_indices.add(idx)
        continue

    try:
        data = json.loads(json_line.strip())
        if data.get("r", 1) == 1:
            relevant_indices.add(idx)
    except (json.JSONDecodeError, KeyError, ValueError):
        parse_errors += 1
        relevant_indices.add(idx)

if parse_errors:
    print("  Parse errors: " + str(parse_errors) + " — affected paragraphs kept")

relevant_passages = [
    (i, all_paragraphs[i][0], all_paragraphs[i][1])
    for i in sorted(relevant_indices)
]

total    = len(all_paragraphs)
kept     = len(relevant_passages)
filtered = total - kept
print("  Relevant: " + str(kept) + "/" + str(total)
      + " paragraphs (" + str(round(100 * kept / total, 1)) + "%)")
print("  Filtered: " + str(filtered)
      + " paragraphs (" + str(round(100 * filtered / total, 1)) + "%)")

# ── Write output ──────────────────────────────────────────────────────────────

print("\nWriting output to " + output_path + "...")

with open(output_path, "w", encoding="utf-8") as f:
    f.write("# Mapped Passages: " + objective_id + "\n\n")
    f.write("**Objective:** " + objective_title + "\n\n")
    f.write("**Run date:** " + str(date.today()) + "\n\n")
    f.write("---\n\n")

    for idx, source_file, para_text in relevant_passages:
        f.write("<!-- Source: " + source_file + " -->\n\n")
        f.write(para_text.strip())
        f.write("\n\n---\n\n")

    # Extraction summary — field names match stage2_verify.py exactly
    f.write("## Extraction Summary\n\n")
    f.write("- Objective: "                           + objective_id           + "\n")
    f.write("- Source files scanned: "                + str(len(clean_files))  + "\n")
    f.write("- Total paragraphs classified: "         + str(total)             + "\n")
    f.write("- Paragraphs classified RELEVANT: "      + str(kept)              + "\n")
    f.write("- Paragraphs filtered out: "             + str(filtered)          + "\n")
    f.write("- Parse errors (kept): "                 + str(parse_errors)      + "\n")
    f.write("- Batch ID: "                            + batch.id               + "\n")
    f.write("- Run date: "                            + str(date.today())      + "\n")

final_size = os.path.getsize(output_path)
print("  Output size: " + str(final_size) + " bytes")
print("\nStage 2 complete: " + output_path)
print()

# ── Self-check preview ────────────────────────────────────────────────────────

print("--- Self-check: first 5 passages ---")
shown = 0
with open(output_path) as f:
    raw_out = f.read()

for block in raw_out.split("\n\n---\n\n"):
    block = block.strip()
    if not block or block.startswith("#") or block.startswith("**") \
            or block.startswith("## Extraction"):
        continue
    lines       = block.splitlines()
    source_line = next((l for l in lines if l.startswith("<!-- Source:")), "")
    content_lines = [l for l in lines if not l.startswith("<!--")]
    preview     = " ".join(content_lines)
    print("\n[" + str(shown + 1) + "] " + source_line)
    print("     " + preview[:200] + ("..." if len(preview) > 200 else ""))
    shown += 1
    if shown >= 5:
        break

if shown == 0:
    print("  WARNING: No passages in output — check objective file and source material")

print("\nNext: python3 stage2_verify.py " + output_path)
