#!/usr/bin/env python3
"""
Stage 1 - Normalize
Processes all source files for a given exam objective.
Runs three sequential jobs per file:
  Job A: Format conversion (PDF, SRT, HTML, DOCX -> plain text/markdown)
  Job B: Formatting noise removal (encoding fixes, deduplication, cleanup)
  Job C: Semantic noise removal (Haiku Batch API classifies SIGNAL vs NOISE)

Output: one *_clean.md file per source, written to 01_normalize/output/<objective_id>/

Usage:
  python3 stage1_run.py x200_103
"""

import sys
import os
import re
import json
import time
import subprocess
from datetime import date
import ftfy
import anthropic

# ── Config ────────────────────────────────────────────────────────────────────

SUPPORTED = {".pdf", ".md", ".txt", ".srt", ".html", ".docx"}

if len(sys.argv) < 2:
    print("Usage: python3 stage1_run.py <objective_id>")
    print("Example: python3 stage1_run.py x200_103")
    sys.exit(1)

objective_id = sys.argv[1].strip().rstrip("/")
# Accept full path — extract basename
if os.sep in objective_id or "/" in objective_id:
    objective_id = os.path.basename(objective_id)

INPUT_DIR  = "01_normalize/input/"  + objective_id
OUTPUT_DIR = "01_normalize/output/" + objective_id

if not os.path.isdir(INPUT_DIR):
    print("ERROR: Input directory not found: " + INPUT_DIR)
    print("Create it and drop source files in before running Stage 1.")
    sys.exit(1)

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── File discovery ────────────────────────────────────────────────────────────

input_files = sorted([
    os.path.join(INPUT_DIR, f)
    for f in os.listdir(INPUT_DIR)
    if os.path.splitext(f)[1].lower() in SUPPORTED
    and not f.startswith(".")
])

if not input_files:
    print("ERROR: No supported source files found in " + INPUT_DIR)
    print("Supported formats: " + ", ".join(sorted(SUPPORTED)))
    sys.exit(1)

print("Stage 1 - Normalize")
print("Objective:  " + objective_id)
print("Input:      " + INPUT_DIR + "/")
print("Output:     " + OUTPUT_DIR + "/")
print("Files:      " + str(len(input_files)))
print()
for f in input_files:
    size = os.path.getsize(f)
    print("  " + os.path.basename(f) + " (" + str(size) + " bytes)")
print()

# ── Job A — Format Conversion ─────────────────────────────────────────────────

def convert_to_text(filepath):
    ext = os.path.splitext(filepath)[1].lower()

    if ext == ".pdf":
        import pymupdf4llm
        return pymupdf4llm.to_markdown(filepath)

    elif ext in (".md", ".txt"):
        with open(filepath, encoding="utf-8", errors="replace") as f:
            return f.read()

    elif ext == ".srt":
        with open(filepath, encoding="utf-8", errors="replace") as f:
            raw = f.read()
        raw = re.sub(r'(?m)^\d+$', '', raw)
        raw = re.sub(r'(?m)^\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}$', '', raw)
        return raw

    elif ext == ".html":
        result = subprocess.run(
            ["pandoc", filepath, "-t", "plain"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            return result.stdout
        raise RuntimeError("pandoc failed: " + result.stderr)

    elif ext == ".docx":
        result = subprocess.run(
            ["pandoc", filepath, "-t", "markdown"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            return result.stdout
        raise RuntimeError("pandoc failed: " + result.stderr)

    else:
        raise ValueError("Unsupported format: " + ext)

# ── Job B — Formatting Noise Removal ─────────────────────────────────────────

def clean_text(raw_text):
    text = ftfy.fix_text(raw_text)
    text = re.sub(r'(?m)^\d+$', '', text)
    text = re.sub(r'(?m)^\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}$', '', text)
    text = re.sub(r'\[\d{1,2}:\d{2}:\d{2}\]', '', text)
    text = re.sub(r'\(\d{2}:\d{2}:\d{2}\)', '', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = text.replace('\x00', '')
    # Deduplicate paragraphs
    seen    = set()
    deduped = []
    for p in text.split('\n\n'):
        key = p.strip()
        if key not in seen:
            seen.add(key)
            deduped.append(p)
    return '\n\n'.join(deduped)

# ── Job C — Semantic Noise Removal (Haiku Batch) ──────────────────────────────

SYSTEM_PROMPT = (
    "You are a semantic noise filter for RHCSA Linux certification study material.\n\n"
    "For each numbered paragraph, classify it as SIGNAL or NOISE.\n\n"
    "SIGNAL: Linux concepts, commands, procedures, definitions, bash syntax, shell operations, "
    "configuration examples, or any exam-relevant technical content.\n\n"
    "NOISE: Instructor anecdotes, platform navigation instructions (click next, pause the video), "
    "advertisements, motivation with no technical content, TOC entries, copyright notices, "
    "index listings, bibliography entries.\n\n"
    "When uncertain: classify as SIGNAL.\n\n"
    "Respond with ONLY a valid JSON array, no markdown fences, no extra text:\n"
    '[{"index": 0, "classification": "SIGNAL"}, {"index": 1, "classification": "NOISE"}, ...]'
)

def strip_fences(raw):
    lines = raw.strip().splitlines()
    if lines and lines[0].startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].strip() == "```":
        lines = lines[:-1]
    return "\n".join(lines).strip()

def classify_paragraphs(client, paragraphs, file_label):
    CHUNK_SIZE = 20
    requests   = []
    for start in range(0, len(paragraphs), CHUNK_SIZE):
        chunk    = paragraphs[start:start + CHUNK_SIZE]
        numbered = "\n\n---\n\n".join(
            "[" + str(start + j) + "] " + p
            for j, p in enumerate(chunk)
        )
        requests.append({
            "custom_id": file_label + "-chunk-" + str(start),
            "params": {
                "model": "claude-haiku-4-5-20251001",
                "max_tokens": 4096,
                "system": SYSTEM_PROMPT,
                "messages": [{"role": "user", "content": numbered}]
            }
        })
    return requests

# ── Main pipeline ─────────────────────────────────────────────────────────────

client = anthropic.Anthropic()

processed = []
skipped   = []

for filepath in input_files:
    basename    = os.path.basename(filepath)
    source_slug = re.sub(r'[^\w\-]', '_', os.path.splitext(basename)[0])
    output_path = OUTPUT_DIR + "/" + source_slug + "_clean.md"

    if os.path.exists(output_path):
        print("[SKIP] " + basename + " — output already exists: " + output_path)
        skipped.append(filepath)
        continue

    print("[A+B] " + basename)
    try:
        raw      = convert_to_text(filepath)
        cleaned  = clean_text(raw)
        paras    = [p.strip() for p in cleaned.split('\n\n') if p.strip()]
        reduction = 100 * (1 - len(cleaned) / max(len(raw), 1))
        print("  Extracted: " + str(len(raw)) + " chars → " + str(len(cleaned))
              + " chars (" + str(round(reduction, 1)) + "% reduction)")
        print("  Paragraphs: " + str(len(paras)))
        processed.append((filepath, source_slug, output_path, raw, paras))
    except Exception as e:
        print("  ERROR: " + str(e) + " — skipping")
        skipped.append(filepath)

if not processed:
    print("\nNothing to process.")
    sys.exit(0)

# Build and submit single batch for all files
print("\n[C] Building batch for " + str(len(processed)) + " files...")
all_requests = []
file_meta    = {}

for filepath, source_slug, output_path, raw, paras in processed:
    label    = source_slug[:20]
    requests = classify_paragraphs(client, paras, label)
    file_meta[label] = {
        "output_path": output_path,
        "raw":         raw,
        "paragraphs":  paras,
        "filepath":    filepath,
    }
    all_requests.extend(requests)

print("  Total batch requests: " + str(len(all_requests)))
batch = client.messages.batches.create(requests=all_requests)
print("  Batch ID: " + batch.id)

print("  Polling...", end="", flush=True)
while True:
    status = client.messages.batches.retrieve(batch.id)
    if status.processing_status == "ended":
        break
    print(".", end="", flush=True)
    time.sleep(15)
print(" done")

# Collect results per file
noise_by_file = {}
parse_errors  = 0

for result in client.messages.batches.results(batch.id):
    if result.result.type == "succeeded":
        parts = result.custom_id.rsplit("-chunk-", 1)
        if len(parts) != 2:
            continue
        label, start_str = parts
        raw_response = strip_fences(result.result.message.content[0].text)
        try:
            classifications = json.loads(raw_response)
            if label not in noise_by_file:
                noise_by_file[label] = set()
            for item in classifications:
                if item.get("classification") == "NOISE":
                    noise_by_file[label].add(item["index"])
        except (json.JSONDecodeError, KeyError):
            parse_errors += 1
            print("  Warning: parse error on " + result.custom_id + " — keeping chunk")
    else:
        print("  Warning: " + result.custom_id + " failed — " + result.result.type)

if parse_errors:
    print("  Parse errors: " + str(parse_errors) + "/" + str(len(all_requests))
          + " — affected paragraphs kept")

# Write output files
print()
for filepath, source_slug, output_path, raw, paras in processed:
    label            = source_slug[:20]
    noise_indices    = noise_by_file.get(label, set())
    signal_paras     = [p for i, p in enumerate(paras) if i not in noise_indices]
    noise_pct        = 100 * len(noise_indices) / max(len(paras), 1)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("<!-- Source: " + filepath + " | Cleaned: "
                + str(date.today()) + " -->\n\n")
        f.write("\n\n".join(signal_paras))

    final_size = os.path.getsize(output_path)
    print("  Written: " + output_path)
    print("    " + str(len(signal_paras)) + "/" + str(len(paras))
          + " paragraphs kept (" + str(round(noise_pct, 1)) + "% noise removed)")
    print("    " + str(final_size) + " bytes")

print("\nStage 1 complete — " + str(len(processed)) + " files processed, "
      + str(len(skipped)) + " skipped")
print()
print("Run verification:")
print("  python3 stage1_verify.py " + OUTPUT_DIR)
