# Stage 2 — Objective Map
**ICM Layer: L2 (Stage Contract)**

Filter clean source files against a selected RHCSA exam objective. Extract every passage that directly addresses that objective. Produce a single collated file of raw, relevant signal — ready for Diataxis transformation in Stage 3.

---

## Inputs

- `01_normalize/output/[source-slug]_clean.md` — SOURCE (L4): one or more clean files from Stage 1. Feed as single file, batch, or full directory. All filtered against the same objective in one pass.
- `_config/exam-objectives/[x200_NNN].md` — REFERENCE (L3): the selected exam objective file for this run. This is the semantic anchor. Read it completely before beginning — it defines what counts as relevant.

**Objective file structure:** Each objective file contains the official Red Hat exam objective statement at the top, followed by content from official Red Hat study guides that directly addresses that objective. A passage is relevant if it would help a candidate understand, prepare for, or execute that specific objective on the exam.

---

## Relevance Definition

A passage is relevant if it meets at least one of these criteria:

**Direct match:** The passage explicitly covers a concept, command, configuration, or procedure that the exam objective names or requires.

**Prerequisite match:** The passage covers knowledge required before the objective can be executed — e.g., understanding what a volume group is before creating one.

**Failure mode match:** The passage covers what goes wrong when executing this objective — common errors, incorrect approaches, or exam traps.

**A passage is NOT relevant if:**
- It mentions a keyword from the objective but is about a different context (e.g., "partition" in a networking context when the objective is about storage partitions)
- It is general Linux knowledge with no specific connection to this objective
- It covers a different exam objective entirely

When relevance is borderline: **include it.** Stage 3 has the Diataxis compass to determine quadrant placement. Stage 2 errs toward inclusion.

---

## Tool Stack

### First Pass — Keyword Scan

**Tool:** `ripgrep` (`rg`)

`ripgrep` is the right tool here — faster than `grep` on large file sets, Unicode-aware, outputs matches with surrounding context. Fully deterministic, zero cost.

```bash
# Installation (Ubuntu 24)
sudo apt install ripgrep

# Basic keyword search across all clean files
rg -i "keyword" 01_normalize/output/

# Search for multiple objective terms simultaneously
rg -i "lvm|logical volume|pvcreate|vgcreate|lvcreate|lvextend" 01_normalize/output/

# Output with context — 3 lines before and after each match
rg -i -B 3 -A 3 "lvm" 01_normalize/output/

# Save flagged matches as structured JSON (avoids fragile -- delimiter parsing)
rg -i --json "term1|term2|term3" 01_normalize/output/ > 02_map/input/flagged_matches.jsonl
```

Extract key terms from the objective file before running. Search each major term. Flag broadly — do not filter at this step. Relevance judgment is Haiku's job.

---

### Second Pass — Relevance Judgment

**Tool:** Haiku 4.5 via Anthropic Batch API

**Why Haiku 4.5:** Relevance judgment against a well-defined objective is structured pattern-recognition — Haiku handles it accurately. The objective filter file gives explicit context. At $0.50/$2.50 per million tokens (Batch pricing), classifying 200 flagged passages averaging 400 tokens each costs approximately $0.05 per objective run.

**Why Batch API:** Stage 2 is asynchronous. The 50% Batch discount applies. Submit all flagged passages for one objective in a single batch — full automation, no manual review gate.

**Prompt caching:** The system prompt and objective statement are identical for every passage in a run. Cache both. After the first call, cached content costs 10% of standard input rate.

```python
import anthropic
import json

client = anthropic.Anthropic()

# Load objective statement from _config/exam-objectives.md
with open(f"_config/exam-objectives/{objective_id}.md") as f:  # e.g. objective_id = "x200_101"
    objective_content = f.read()

RELEVANCE_SYSTEM_PROMPT = f"""You are a relevance filter for RHCSA Linux certification study material.

You will receive a passage from a study source. Your job is to determine whether
it is relevant to the following exam objective:

{objective_content}

Classify the passage as RELEVANT or IRRELEVANT.

RELEVANT: The passage directly addresses the objective, covers a required
prerequisite, or describes a failure mode when executing this objective.

IRRELEVANT: The passage mentions a keyword from the objective but is about
a different context, covers a different objective entirely, or is general
Linux knowledge with no specific connection to this objective.

When uncertain: classify as RELEVANT. Downstream stages handle granularity.

Respond with ONLY valid JSON: {{"classification": "RELEVANT"}} or {{"classification": "IRRELEVANT"}}"""

# Parse flagged matches from ripgrep --json output
# Each line is a JSON object with type "match" or "context" or "begin"/"end"
import json as json_lib

passages = []  # list of (source_filename, passage_text) tuples

with open("02_map/input/flagged_matches.jsonl") as f:
    current_lines = []
    current_file = None
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            obj = json_lib.loads(line)
        except json_lib.JSONDecodeError:
            continue
        obj_type = obj.get("type")
        if obj_type == "begin":
            current_file = obj["data"]["path"]["text"]
            current_lines = []
        elif obj_type in ("match", "context"):
            current_lines.append(obj["data"]["lines"]["text"].rstrip())
        elif obj_type == "end":
            if current_lines and current_file:
                passages.append((current_file, "\n".join(current_lines)))
            current_lines = []
            current_file = None

# Build batch — one request per passage
requests = []
for i, (source_file, passage_text) in enumerate(passages):
    requests.append({
        "custom_id": f"passage-{i}",
        "params": {
            "model": "claude-haiku-4-5-20251001",
            "max_tokens": 32,
            "system": RELEVANCE_SYSTEM_PROMPT,
            "messages": [{
                "role": "user",
                "content": passage_text
            }]
        }
    })

# Submit single batch for the full objective run
batch = client.messages.batches.create(requests=requests)
print(f"Batch submitted: {batch.id}")
print(f"Passages submitted: {len(requests)}")

# Poll until complete
import time
while True:
    status = client.messages.batches.retrieve(batch.id)
    if status.processing_status == "ended":
        break
    time.sleep(10)

# Collect RELEVANT passages and write output
relevant_passages = []
for result in client.messages.batches.results(batch.id):
    if result.result.type == "succeeded":
        response_text = result.result.message.content[0].text
        classification = json.loads(response_text).get("classification")
        if classification == "RELEVANT":
            idx = int(result.custom_id.split("-")[1])
            relevant_passages.append((idx, passages[idx]))

# Sort by original order
relevant_passages.sort(key=lambda x: x[0])
print(f"Relevant: {len(relevant_passages)} / {len(passages)} passages")

# Write collated output file with source attribution comments
import os
from datetime import date

os.makedirs("02_map/output", exist_ok=True)

# Determine objective slug from the loaded objective file
# Convention: use the filename without extension, e.g. x200_101 from x200_101.md
objective_slug = objective_id  # Already set when loading the objective file

output_path = f"02_map/output/{objective_slug}_mapped-passages.md"
with open(output_path, "w") as f:
    # Header
    f.write(f"# Mapped Passages: {objective_slug}\n\n")
    f.write(f"**Objective:** {objective_content.splitlines()[0]}\n\n")
    f.write("---\n\n")
    # Passages with source attribution
    for idx, (source_file, passage_text) in relevant_passages:
        f.write(f"<!-- Source: {source_file} -->\n")
        f.write(passage_text.strip())
        f.write("\n\n---\n\n")
    # Extraction summary
    f.write(f"## Extraction Summary\n\n")
    f.write(f"- Files scanned: {len(set(sf for sf, _ in passages))}\n")
    f.write(f"- Passages flagged by ripgrep: {len(passages)}\n")
    f.write(f"- Passages classified RELEVANT by Haiku: {len(relevant_passages)}\n")
    f.write(f"- Batch ID: {batch.id}\n")
    f.write(f"- Run date: {date.today()}\n")

print(f"Output written: {output_path}")
```

---

## Process

1. **Load the objective.** Read the selected objective file from `_config/exam-objectives/[x200_NNN].md` completely. Identify the official objective statement, key concepts it names, commands it implies, and scope boundaries.

2. **First pass — keyword scan.** Build a keyword list from the objective statement. Run `ripgrep` against all clean files in `01_normalize/output/` with `-B 3 -A 3` context flags. Save all flagged output to `02_map/input/flagged_matches.jsonl`. Note: `02_map/input/` holds both source references and this intermediate file — the source files remain in `01_normalize/output/` and are read directly by ripgrep; only the JSON matches file is written here.

3. **Second pass — relevance judgment.** Parse flagged passages from the ripgrep output. Submit all passages as a single Haiku 4.5 Batch API call. Wait for completion. Collect all passages classified RELEVANT.

4. **Extract and collate.** Write each RELEVANT passage to the output file in original order. Include a source reference comment above each passage: `<!-- Source: [filename] -->`. Do not summarize, paraphrase, or rewrite — raw signal only.

5. **Self-check** before writing final output:
   - Does the collated file contain enough conceptual content to write an Explanation? If thin (under 500 words), re-check borderline exclusions from the batch results.
   - Are there obvious gaps? (e.g., for an LVM objective, `pvcreate` passages exist but nothing about `lvcreate`) — re-run ripgrep for missing terms.
   - Spot-check five random passages — are they actually about this objective?

6. **Write output** with objective header and extraction summary.

---

## Output

- **Format:** Single `.md` file — collated raw passages with source reference comments
- **Write to:** `02_map/output/[objective-slug]_mapped-passages.md`
- **Must include:**
  - Objective header at top: `# Mapped Passages: [objective-slug]` + official objective statement
  - Source reference comment above every passage: `<!-- Source: [filename] -->`
  - All RELEVANT passages — complete and unmodified
  - Extraction summary at bottom: total files scanned, passages flagged by ripgrep, passages classified RELEVANT by Haiku, batch ID for traceability
- **Must NOT include:**
  - Summarized or paraphrased content — raw passages only
  - Passages from a different exam objective
  - Duplicate passages (same content from multiple sources — keep clearest version, note duplicate)
  - Stage 1 formatting noise that slipped through — strip on extraction
  - Diataxis classification or interpretation — that is Stage 3's job

---

## Done Looks Like

A single `[objective-slug]_mapped-passages.md` in `02_map/output/` containing collated raw passages, each with a source reference comment, covering concepts, commands, procedures, and failure modes relevant to the selected objective — with a batch ID and extraction summary at the bottom.

---

## Common Failure Modes

**Failure 1 — Too few passages (ripgrep keyword list too narrow).**
What goes wrong: Key terms from the objective were not included in the ripgrep search, leaving gaps in the collated output.
How to detect: Collated file under 500 words, or missing obvious concepts for this objective.
How to fix: Expand the keyword list. Add synonyms, related commands, and prerequisite terms. Re-run ripgrep, resubmit batch.

**Failure 2 — Too many IRRELEVANT passages slipping through (Haiku over-inclusive).**
What goes wrong: Passages mentioning objective keywords in a different context are classified RELEVANT.
How to detect: Collated file contains passages clearly about a different objective or domain.
How to fix: Add explicit exclusion examples to the system prompt for this objective. Resubmit batch for the affected passages only.

**Failure 3 — Passages summarized instead of extracted.**
What goes wrong: Operator condenses or paraphrases passages before collating.
How to detect: Collated passages read differently from source files — different phrasing, shorter, missing details.
How to fix: Re-extract from original clean files. Raw passages only — Stage 3 transforms.

**Failure 4 — Multiple objectives mixed in one output file.**
What goes wrong: Operator runs two objectives in one pass.
How to detect: Output file contains passages clearly addressing two different objectives.
How to fix: One objective per run. One output file per objective.

**Failure 5 — Batch submitted file-by-file instead of as one batch.**
What goes wrong: Multiple batch IDs instead of one per run. Loses 50% discount, slower.
How to detect: More batch IDs in logs than objective runs.
How to fix: Parse all flagged passages first, submit all in a single `client.messages.batches.create()` call.
