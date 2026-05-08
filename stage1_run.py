#!/usr/bin/env python3
"""
Stage 1 - Normalize
Processes all files in 01_normalize/input/ or a single specified file.
Usage:
  python3 stage1_run.py                          # process all files in input/
  python3 stage1_run.py 01_normalize/input/file  # process single file
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

# Objective ID passed as first argument (e.g. x200_102)
# Usage: python3 stage1_run.py x200_102
if len(sys.argv) > 1 and not sys.argv[1].startswith("01_normalize"):
    _OBJ = sys.argv[1]
else:
    _OBJ = "x200_101"  # default for backward compatibility

INPUT_DIR  = f"01_normalize/input/{_OBJ}"
OUTPUT_DIR = f"01_normalize/output/{_OBJ}"
os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

SUPPORTED = {".pdf", ".md", ".txt", ".srt", ".html", ".docx"}

# ── File discovery ────────────────────────────────────────────────────────────

input_files = sorted([
    os.path.join(INPUT_DIR, f)
    for f in os.listdir(INPUT_DIR)
    if os.path.splitext(f)[1].lower() in SUPPORTED
    and not f.startswith(".")
])

print(f"Stage 1 - Normalize")
print(f"Files to process: {len(input_files)}")
for f in input_files:
    size = os.path.getsize(f)
    print(f"  {os.path.basename(f)} ({size:,} bytes)")
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
        # Strip sequence numbers and timing lines
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
        raise RuntimeError(f"pandoc failed: {result.stderr}")

    elif ext == ".docx":
        result = subprocess.run(
            ["pandoc", filepath, "-t", "markdown"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            return result.stdout
        raise RuntimeError(f"pandoc failed: {result.stderr}")

    else:
        raise ValueError(f"Unsupported format: {ext}")

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
    seen = set()
    deduped = []
    for p in text.split('\n\n'):
        key = p.strip()
        if key not in seen:
            seen.add(key)
            deduped.append(p)
    return '\n\n'.join(deduped)

# ── Job C — Semantic Noise Removal ────────────────────────────────────────────

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
    requests = []
    for start in range(0, len(paragraphs), CHUNK_SIZE):
        chunk = paragraphs[start:start + CHUNK_SIZE]
        numbered = "\n\n---\n\n".join(
            f"[{start + j}] {p}" for j, p in enumerate(chunk)
        )
        requests.append({
            "custom_id": f"{file_label}-chunk-{start}",
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

# Process all files through Jobs A and B first
processed = []
skipped = []

for filepath in input_files:
    basename = os.path.basename(filepath)
    source_slug = re.sub(r'[^\w\-]', '_', os.path.splitext(basename)[0])
    output_path = f"{OUTPUT_DIR}/{source_slug}_clean.md"

    # Skip if already processed
    if os.path.exists(output_path):
        print(f"[SKIP] {basename} — output already exists: {output_path}")
        skipped.append(filepath)
        continue

    print(f"[A+B] {basename}")
    try:
        raw = convert_to_text(filepath)
        cleaned = clean_text(raw)
        paragraphs = [p.strip() for p in cleaned.split('\n\n') if p.strip()]
        reduction = 100 * (1 - len(cleaned) / max(len(raw), 1))
        print(f"  Extracted: {len(raw):,} chars → {len(cleaned):,} chars ({reduction:.1f}% reduction)")
        print(f"  Paragraphs: {len(paragraphs)}")
        processed.append((filepath, source_slug, output_path, raw, paragraphs))
    except Exception as e:
        print(f"  ERROR: {e} — skipping")
        skipped.append(filepath)

if not processed:
    print("\nNothing to process.")
    sys.exit(0)

# Build and submit single batch for all files
print(f"\n[C] Building batch for {len(processed)} files...")
all_requests = []
file_meta = {}

batch_offset = 0
for filepath, source_slug, output_path, raw, paragraphs in processed:
    label = source_slug[:20]
    requests = classify_paragraphs(client, paragraphs, label)
    # Track offset mapping: custom_id -> (output_path, raw, paragraphs)
    file_meta[label] = {
        "output_path": output_path,
        "raw": raw,
        "paragraphs": paragraphs,
        "filepath": filepath
    }
    all_requests.extend(requests)

print(f"  Total batch requests: {len(all_requests)}")
batch = client.messages.batches.create(requests=all_requests)
print(f"  Batch ID: {batch.id}")

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
parse_errors = 0

for result in client.messages.batches.results(batch.id):
    if result.result.type == "succeeded":
        # custom_id format: "{label}-chunk-{start}"
        parts = result.custom_id.rsplit("-chunk-", 1)
        if len(parts) != 2:
            continue
        label, start_str = parts
        start = int(start_str)

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
            print(f"  Warning: parse error on {result.custom_id} — keeping chunk")
    else:
        print(f"  Warning: {result.custom_id} failed — {result.result.type}")

if parse_errors:
    print(f"  Total parse errors: {parse_errors}/{len(all_requests)} chunks")

# Write output files
print()
summary = []
for filepath, source_slug, output_path, raw, paragraphs in processed:
    label = source_slug[:20]
    noise_indices = noise_by_file.get(label, set())
    signal_paragraphs = [p for i, p in enumerate(paragraphs) if i not in noise_indices]

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"<!-- Source: {filepath} | Cleaned: {date.today()} -->\n\n")
        f.write("\n\n".join(signal_paragraphs))

    final_size = os.path.getsize(output_path)
    noise_pct = 100 * len(noise_indices) / max(len(paragraphs), 1)
    print(f"  Written: {output_path}")
    print(f"    {len(signal_paragraphs)}/{len(paragraphs)} paragraphs kept ({noise_pct:.1f}% noise removed)")
    print(f"    {final_size:,} bytes")
    summary.append((os.path.basename(output_path), len(signal_paragraphs), len(paragraphs), noise_pct))

print(f"\nStage 1 complete — {len(processed)} files processed, {len(skipped)} skipped")
print()
print("Run verification:")
for _, source_slug, output_path, _, _ in processed:
    print(f"  python3 stage1_verify.py {output_path}")
