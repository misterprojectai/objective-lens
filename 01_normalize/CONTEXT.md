# Stage 1 — Normalize
**ICM Layer: L2 (Stage Contract)**

Transform raw source files of any format into clean, signal-only `.md` files. Remove all noise. Preserve all signal. Nothing is interpreted or transformed — only cleaned.

---

## Inputs

- `01_normalize/input/` — SOURCE (L4): raw files in any format — PDF, .txt, .md, .docx, blog post exports, video transcripts (.srt converted to .txt), podcast transcripts, lesson notes.

**Accepted input formats:** `.pdf`, `.txt`, `.md`, `.docx`, `.srt`, `.html`

**Do not process:** Binary files, images, spreadsheets, audio, video. Log and skip.

---

## Noise Definition

Two categories. Both must be removed.

**Formatting noise** — structural artifacts with no content value:
- Page headers and footers (page numbers, document titles repeated on every page)
- Timestamps and chapter markers from video transcripts (`[00:14:32]`, `Chapter 2:`)
- SRT sequence numbers and timing lines (`1`, `00:00:01,000 --> 00:00:04,000`)
- Repeated boilerplate (copyright notices, "visit our website at...", course platform UI text)
- Encoding artifacts (garbled characters from PDF extraction: `ï¬`, `â€"`, `\x84`)
- Excessive blank lines (more than two consecutive → reduce to one)
- Markdown formatting artifacts from PDF conversion (random `#` headers, `***` dividers with no content)

**Semantic noise** — off-topic content with no RHCSA/Linux signal:
- Instructor personal anecdotes unrelated to technical content
- Course platform navigation instructions ("click next to continue", "pause and try this")
- Advertisements and promotional content
- General computing history with no relevance to exam objectives
- Content from a completely different domain

**Signal** — everything that is NOT noise. When in doubt, keep it. Stage 2 filters by relevance — Stage 1 only cleans.

---

## Tool Stack

### Job A — Format Conversion

| Input format | Tool | Command |
|---|---|---|
| PDF (all types) | `pymupdf4llm` | `python3 -c "import pymupdf4llm; print(pymupdf4llm.to_markdown('file.pdf'))"` |
| .docx | `pandoc` | `pandoc file.docx -t markdown -o file.md` |
| .srt | `sed` | See regex patterns below |
| .html | `pandoc` | `pandoc file.html -t plain -o file.txt` |
| .md / .txt | pass-through | No conversion needed — proceed to Job B |

**Why pymupdf4llm over pdftotext:** pymupdf4llm preserves heading structure, detects tables, and produces clean markdown — designed specifically for LLM pipeline ingestion. For RHCSA study material (Red Hat official guides, structured PDFs) this matters. pdftotext strips all structure.

**Scanned PDF fallback:** If pymupdf4llm output is unreadable (garbled, no text extracted), the PDF is likely scanned. Note it as `<!-- Source: [file] | Status: OCR required, skipped -->` and do not process.

### Job B — Formatting Noise Removal

Run these passes in order after conversion:

```bash
# Full Job B pipeline — runs as a single chain, no intermediate files left behind
# Replace INPUT and OUTPUT with actual file paths

INPUT="input.md"
OUTPUT="output_clean.md"

# 1. Repair encoding artifacts
python3 -c "import ftfy, sys; print(ftfy.fix_text(open(sys.argv[1]).read()))" "$INPUT" |

# 2+3. Strip SRT sequence numbers and timing lines (safe to run on all formats — no-op if not SRT)
sed '/^[0-9]*$/d' |
sed '/^[0-9].*-->/d' |

# 4. Strip inline timestamps [00:00:00] and (00:00:00) formats
sed 's/\[[0-9:]*\]//g; s/([0-9][0-9]:[0-9][0-9]:[0-9][0-9])//g' |

# 5. Collapse 3+ consecutive blank lines to one
sed '/^$/N;/^\n$/d' |

# 6. Remove exact duplicate lines (catches repeated headers/footers)
awk '!seen[$0]++' |

# 7. Normalize whitespace — remove null bytes and control characters while PRESERVING Unicode
# Note: Use python ftfy (step 1) for encoding repair. This step only removes genuine control chars.
# Do NOT use tr -cd '\40-\176' — it strips all Unicode above ASCII 126 including legitimate content.
LC_ALL=C sed 's/\x00//g' > "$OUTPUT"
```

**Note:** The pipeline uses Unix pipes — no intermediate temp files are written to disk. `$INPUT` is read once, `$OUTPUT` is the only file written. Clean working directory maintained throughout.

**ftfy installation:** `pip install ftfy --break-system-packages`

### Job C — Semantic Noise Removal

**Tool:** Haiku 4.5 via Anthropic Batch API

**Why Haiku 4.5, not Sonnet 4.6:** Binary classification ("is this paragraph technical Linux content or not?") is well within Haiku's capability. At $1/$5 per million input/output tokens vs Sonnet's $3/$15, the 3× cost difference is not justified for this task.

**Why Batch API:** Stage 1 is asynchronous — files are processed offline, not in real time. The Batch API gives a 50% discount on all tokens. Haiku 4.5 with Batch = $0.50/$2.50 per million tokens. Per 50-file objective run: approximately $0.30 total for semantic noise removal.

**Prompt caching:** The system prompt (noise definition rules) is identical for every file in a run. Cache it. After the first call, the cached portion costs 10% of standard input rate — effectively free for subsequent files.

**Batch API call pattern:**
```python
import anthropic

client = anthropic.Anthropic()

NOISE_SYSTEM_PROMPT = """You are a semantic noise filter for RHCSA Linux certification study material.

For each paragraph provided, classify it as SIGNAL or NOISE.

SIGNAL: Any paragraph containing Linux concepts, commands, procedures, definitions,
configuration examples, or exam-relevant technical content.

NOISE: Any paragraph that is purely:
- Personal instructor anecdote with no technical content
- Course platform navigation instruction ("click next", "pause the video")
- Advertisement or promotional content
- General motivation or encouragement with no technical content

When uncertain: classify as SIGNAL. Downstream filtering handles relevance.

Respond with ONLY a JSON array. One object per paragraph:
[{"index": 0, "classification": "SIGNAL"}, {"index": 1, "classification": "NOISE"}, ...]"""

# Build batch requests — one per file
requests = []
for i, (filename, paragraphs) in enumerate(files_to_process):
    requests.append({
        "custom_id": f"file-{i}",
        "params": {
            "model": "claude-haiku-4-5-20251001",
            "max_tokens": 4096,  # Must scale with paragraph count — 100 paragraphs ≈ 2000 tokens
            "system": NOISE_SYSTEM_PROMPT,
            "messages": [{"role": "user", "content": "\n\n---\n\n".join(paragraphs)}]
        }
    })

# Submit single batch — all files in this run, not file-by-file
batch = client.messages.batches.create(requests=requests)
print(f"Batch submitted: {batch.id} | Files: {len(requests)}")

# Poll until complete
import time
while True:
    status = client.messages.batches.retrieve(batch.id)
    if status.processing_status == "ended":
        break
    print(f"Status: {status.processing_status} — waiting...")
    time.sleep(15)

# Retrieve results and rebuild filtered files
results_map = {}
for result in client.messages.batches.results(batch.id):
    if result.result.type == "succeeded":
        response_text = result.result.message.content[0].text
        try:
            classifications = json.loads(response_text)
            # Map: {file_index: {paragraph_index: "SIGNAL"|"NOISE"}}
            file_idx = int(result.custom_id.split("-")[1])
            results_map[file_idx] = {
                item["index"]: item["classification"]
                for item in classifications
            }
        except (json.JSONDecodeError, KeyError):
            # If response malformed, keep all paragraphs (fail safe toward signal)
            print(f"Warning: malformed response for {result.custom_id} — keeping all paragraphs")

# Write filtered output files
import os
from datetime import date

os.makedirs("01_normalize/output", exist_ok=True)

for i, (filename, paragraphs) in enumerate(files_to_process):
    classifications = results_map.get(i, {})
    signal_paragraphs = [
        p for j, p in enumerate(paragraphs)
        if classifications.get(j, "SIGNAL") == "SIGNAL"  # default SIGNAL if missing
    ]
    source_slug = os.path.splitext(os.path.basename(filename))[0]
    output_path = f"01_normalize/output/{source_slug}_clean.md"
    with open(output_path, "w") as f:
        f.write(f"<!-- Source: {filename} | Cleaned: {date.today()} -->\n\n")
        f.write("\n\n".join(signal_paragraphs))
    print(f"Written: {output_path} ({len(signal_paragraphs)}/{len(paragraphs)} paragraphs kept)")
```

---

## Process

1. **Convert to plain text** using Job A tools per format. Verify output is readable before proceeding. If conversion fails, log and skip.

2. **Remove formatting noise** using Job B pipeline. Run the single chained pipe command — it applies all seven transformations in sequence. One command, one execution.

3. **Remove semantic noise** using Job C Batch API call. Submit all files from a single run as one batch — do not submit file by file. Wait for batch completion, then filter out NOISE-classified paragraphs.

4. **Self-check** before writing output:
   - Is every remaining paragraph technical content? Spot-check five random paragraphs.
   - Is the file at least 20% smaller than the original by character count? If not, spot-check for missed noise patterns.
   - Is the file still readable as coherent technical prose? If garbled, conversion failed — retry.

5. **Write output** to `01_normalize/output/` using naming convention.

---

## Output

- **Format:** `.md` — plain text only
- **Write to:** `01_normalize/output/[source-slug]_clean.md`
- **Must include:**
  - All technical content from the source: concepts, commands, procedures, definitions, examples
  - Source attribution comment at top: `<!-- Source: [original filename] | Cleaned: [date] -->`
  - Consistent paragraph breaks between distinct topics
- **Must NOT include:**
  - Timestamps, sequence numbers, chapter markers
  - Page headers, footers, or repeated boilerplate
  - Encoding artifacts or garbled characters
  - Platform UI instructions ("click next", "pause the video")
  - Advertisements or promotional content
  - Multiple files merged into one — one source produces one clean output

---

## Done Looks Like

Every file in `01_normalize/input/` has a corresponding `_clean.md` in `01_normalize/output/` — readable plain text, technical content only, source attribution comment at top, no formatting artifacts.

---

## Common Failure Modes

**Failure 1 — pymupdf4llm produces empty or garbled output.**
What goes wrong: Scanned PDF — no embedded text layer.
How to detect: Output file is empty or contains only garbled characters.
How to fix: Log as OCR required, skip. Do not attempt to force through pipeline.

**Failure 2 — Batch API classification over-aggressive (too much SIGNAL stripped).**
What goes wrong: Haiku classifies borderline technical content as NOISE.
How to detect: Output file missing commands or concepts known to be in the source.
How to fix: Re-run semantic pass with stricter SIGNAL bias — add "If any Linux command, path, or technical term is present, classify as SIGNAL regardless of surrounding context" to the system prompt.

**Failure 3 — Multiple source files merged into one output.**
What goes wrong: Operator concatenates all sources for convenience.
How to detect: Output directory has fewer files than input directory.
How to fix: One source → one clean output. Merging happens at Stage 2, not here.

**Failure 4 — Batch API call submitted file-by-file instead of as one batch.**
What goes wrong: Higher cost, slower processing, loses the 50% batch discount.
How to detect: Multiple separate batch IDs instead of one per run.
How to fix: Collect all files for the run, submit as a single batch request.
