#!/usr/bin/env python3
"""
Stage 4 - GitBook Publish (Sonnet-powered)
Transforms Stage 3 Diataxis documents into richly formatted GitBook markdown.

Sonnet 4.6 receives the full source document + complete GitBook block reference
loaded from _config/ + a per-document-type transformation contract. It reasons
through block selection to deliver an outstanding learning experience while
maintaining Diataxis purity and guaranteed rendering correctness.

Platform separation (HARD):
  04_publish/output/ -> GitBook liquid blocks ONLY
  Stage 5 handles iximiuz adaptation from Stage 3 source, never Stage 4 output.

Prerequisites:
  _config/gitbook-blocks.md   <- gitbook__documentation_blocks.md (official)
  _config/gitbook-skill.md    <- gitbook-external-editing-SKILL.md (skill)

Usage:
  python3 stage4_run.py 03_diataxis/output/x200_101
"""

import os
import re
import sys
import time
import subprocess
import anthropic

# ── Config ────────────────────────────────────────────────────────────────────

OUTPUT_BASE  = "04_publish/output"
GITBOOK_YAML = ".gitbook.yaml"
SUMMARY_FILE = "04_publish/output/SUMMARY.md"
MODEL        = "claude-sonnet-4-6"
MAX_TOKENS   = 16000   # raised from 8192 — large docs + rich block markup require headroom
MAX_RETRIES  = 3
RETRY_DELAYS = [5, 15, 30]  # seconds between retry attempts

# ── GitBook reference loader ──────────────────────────────────────────────────

GITBOOK_BLOCK_REFERENCE = ""  # populated by load_gitbook_reference()

GITBOOK_REF_FILES = [
    ("_config/gitbook-blocks.md", "GitBook Blocks — Official Documentation"),
    ("_config/gitbook-skill.md",  "GitBook External Editing Skill"),
]

# Appended to the assembled reference. Resolves conflicts between the two
# source files and states hard rendering rules unambiguously.
RENDERING_SAFETY_RULES = """

---

# Rendering Safety Rules — NEVER VIOLATE

CONFLICT RESOLUTION: The official GitBook documentation uses ### (H3) for step
headings inside stepper blocks. The skill file uses ## (H2). ### is canonical —
it matches the official documentation. Always use ### for step titles.

BLOCK CLOSING — every opened block MUST be closed:
  {% stepper %}      -> {% endstepper %}
  {% step %}         -> {% endstep %}
  {% hint ... %}     -> {% endhint %}
  {% tabs %}         -> {% endtabs %}
  {% tab ... %}      -> {% endtab %}
  {% columns %}      -> {% endcolumns %}
  {% column %}       -> {% endcolumn %}
  {% code ... %}     -> {% endcode %}
  {% content-ref %}  -> {% endcontent-ref %}
  <details>          -> </details>

NESTING RULES:
  - No steppers nested inside steppers (not supported)
  - No tabs nested inside tabs (not supported)
  - Hints inside steps: valid and encouraged
  - Code blocks inside hints and steps: valid
  - content-ref blocks inside hints: valid

FRONTMATTER:
  - Use bare --- delimiters ONLY. NEVER wrap frontmatter in ```yaml``` code fences.
  - description field is REQUIRED on every page. Write a real sentence — not a placeholder.
  - icon field is REQUIRED on every page. Use the icon specified in the contract.

PLATFORM:
  - NEVER use iximiuz MDC syntax (::simple-task, ::remark-box, ::hint-box, ::details-box)
  - This output is GitBook ONLY. iximiuz adaptation happens in Stage 5 from a different source.

QUALITY:
  - Every block must be semantically justified. No decorative blocks.
  - The document must be complete. Do not truncate content that was present in the source.
"""

def load_gitbook_reference():
    global GITBOOK_BLOCK_REFERENCE
    parts = []
    missing = []

    for path, label in GITBOOK_REF_FILES:
        if os.path.exists(path):
            content = open(path, encoding="utf-8").read()
            parts.append("# " + label + "\n\n" + content)
            print("  Loaded: " + path + "  (" + str(len(content)) + " chars)")
        else:
            missing.append(path)

    if missing:
        print()
        print("ERROR: Required _config/ reference files not found.")
        print()
        for p in missing:
            print("  MISSING: " + p)
        print()
        print("Steps to fix:")
        print("  1. cp ~/Downloads/gitbook-blocks.md  _config/gitbook-blocks.md")
        print("  2. cp ~/Downloads/gitbook-skill.md   _config/gitbook-skill.md")
        print("  3. git add _config/gitbook-blocks.md _config/gitbook-skill.md")
        print("  4. git commit -m 'chore: add GitBook reference files to _config/'")
        print("  5. Re-run: python3 stage4_run.py 03_diataxis/output/x200_101")
        sys.exit(1)

    GITBOOK_BLOCK_REFERENCE = "\n\n---\n\n".join(parts) + RENDERING_SAFETY_RULES
    print("  Reference assembled: " + str(len(GITBOOK_BLOCK_REFERENCE)) + " chars total")
    print()

# ── Transformation system prompts ─────────────────────────────────────────────

EXPLANATION_SYSTEM = (
    "You are a GitBook formatting specialist producing world-class technical learning documentation.\n\n"
    "TASK: Transform the Diataxis Explanation document into richly formatted GitBook markdown "
    "that delivers an outstanding conceptual learning experience.\n\n"
    "WHAT AN EXPLANATION IS:\n"
    "- Conceptual — answers 'what is this' and 'why does it work this way'\n"
    "- Written to be READ, not executed\n"
    "- No numbered steps, no instructions, no 'do this now' language\n"
    "- Rich in context, mental models, design philosophy, trade-offs\n\n"
    "BLOCK STRATEGY:\n"
    "- Open with hint (info): state the exam objective and what this page covers in 2-3 sentences\n"
    "- Warning hints: inline for misconceptions, exam traps, commonly confused concepts\n"
    "- Success hints: key insights and 'aha moment' principles worth highlighting\n"
    "- Expandable <details>: deep dives that interrupt the reading flow — historical context, "
    "advanced nuance, edge cases — collapsed by default\n"
    "- Columns: two concepts best understood side-by-side "
    "(e.g. login shell vs non-login shell, interactive vs non-interactive)\n"
    "- Tabs: only for genuinely distinct conceptual paths (rare — think carefully before using)\n"
    "- Code blocks with title: illustrative examples embedded in the text\n"
    "- Quote blocks: key definitions or memorable principles\n"
    "- End with a section titled 'What to Do Next' containing content-ref blocks "
    "linking to all related tutorials and how-tos from this objective\n"
    "- NO stepper blocks — explanations are not procedural\n\n"
    "FRONTMATTER — produce exactly this structure with real content, no placeholders:\n"
    "---\n"
    "description: Write a real one-sentence description of what this specific page explains.\n"
    "icon: book-open\n"
    "---\n\n"
    "OUTPUT: Complete GitBook markdown document. No preamble, no commentary, no explanation of choices. "
    "Preserve all technical content from the source — do not omit sections."
)

TUTORIAL_SYSTEM = (
    "You are a GitBook formatting specialist producing world-class technical learning documentation.\n\n"
    "TASK: Transform the Diataxis Tutorial document into richly formatted GitBook markdown "
    "that delivers an outstanding guided-learning experience.\n\n"
    "WHAT A TUTORIAL IS:\n"
    "- Guided doing — the learner executes steps and sees real results\n"
    "- One clear path — no branching, no decisions required from the learner\n"
    "- Builds confidence through repeated successful completion\n"
    "- Verification at every meaningful checkpoint\n\n"
    "BLOCK STRATEGY:\n"
    "- Open with hint (info): prerequisites — what the reader needs before starting, stated tightly\n"
    "- The entire procedure lives inside ONE stepper block\n"
    "- Each step = one meaningful action with a clear ### heading as the step title\n"
    "- Inside each step:\n"
    "    - Tight imperative instruction (1-3 sentences maximum)\n"
    "    - Code block with bash language tag for every command the learner runs\n"
    "    - Titled code block ('Output') or success hint for expected output — REQUIRED at checkpoints\n"
    "    - Warning hint for syntax gotchas specific to that step\n"
    "    - Danger hint for destructive or privilege-escalating operations\n"
    "    - Tabs inside a step ONLY when the same action has two valid command forms (e.g. short/long flag)\n"
    "    - Expandable <details> for optional recovery paths ('If you see X instead, do Y')\n"
    "- Close with success hint AFTER the stepper: what the learner has accomplished\n\n"
    "FRONTMATTER — produce exactly this structure with real content, no placeholders:\n"
    "---\n"
    "description: Write a real one-sentence description of what the learner will be able to do.\n"
    "icon: graduation-cap\n"
    "---\n\n"
    "OUTPUT: Complete GitBook markdown document. No preamble, no commentary, no explanation of choices. "
    "Preserve all technical content from the source — do not omit steps or commands."
)

HOWTO_SYSTEM = (
    "You are a GitBook formatting specialist producing world-class technical learning documentation.\n\n"
    "TASK: Transform the Diataxis How-to document into richly formatted GitBook markdown "
    "that delivers an outstanding task-execution experience.\n\n"
    "WHAT A HOW-TO IS:\n"
    "- Task-oriented — assumes the reader is competent and has a specific goal\n"
    "- Minimal explanation — the reader knows why, they need the precise how\n"
    "- Dense, efficient, no hand-holding\n"
    "- Verification and troubleshooting are essential, not optional\n\n"
    "BLOCK STRATEGY:\n"
    "- Open with hint (info): prerequisites ONLY — tight bullet list, no narrative\n"
    "- The entire procedure lives inside ONE stepper block\n"
    "- Each step = one action with a clear ### heading\n"
    "- Inside each step:\n"
    "    - Imperative action — no explanation unless critical to correctness\n"
    "    - Code block for every command\n"
    "    - Warning hint for syntax traps or silent failure modes in that step\n"
    "    - Danger hint for destructive operations only\n"
    "    - Tabs for short/long flag variants or RHEL version differences\n"
    "    - Expandable <details> for edge cases — present but not in the main flow\n"
    "- After the stepper: Verification section — success hint wrapping verification commands + expected output\n"
    "- After verification: Troubleshooting section — warning hint with symptom -> cause -> fix entries\n\n"
    "FRONTMATTER — produce exactly this structure with real content, no placeholders:\n"
    "---\n"
    "description: Write a real one-sentence description of the specific task this guide accomplishes.\n"
    "icon: wrench\n"
    "---\n\n"
    "OUTPUT: Complete GitBook markdown document. No preamble, no commentary, no explanation of choices. "
    "Preserve all technical content from the source — do not omit steps, verification, or troubleshooting."
)

REFERENCE_SYSTEM = (
    "You are a GitBook formatting specialist producing world-class technical learning documentation.\n\n"
    "TASK: Transform the Diataxis Reference document into richly formatted GitBook markdown "
    "that delivers an outstanding fast-lookup experience.\n\n"
    "WHAT A REFERENCE IS:\n"
    "- Consulted while working — the reader scans, not reads\n"
    "- Tables are the primary format — dense, accurate, complete\n"
    "- Zero instructions, zero opinion, zero narrative\n"
    "- Factual descriptions only\n\n"
    "BLOCK STRATEGY:\n"
    "- Open with hint (info): one sentence on what this reference covers and its exam scope\n"
    "- Tables as primary content — preserve all existing tables, enhance where justified\n"
    "- Titled code blocks ('Syntax'): formal syntax definitions opening each section\n"
    "- Titled code blocks ('Example'): usage examples immediately following syntax definitions\n"
    "- Warning hints: deprecated options, dangerous flags, exam-critical gotchas\n"
    "- Tabs: show the same construct with short and long flag variants side by side\n"
    "- Expandable <details>: exhaustive option tables that are complete but rarely needed at a glance\n"
    "- Quote blocks: formal definitions worth highlighting (e.g. POSIX definitions)\n"
    "- NO stepper blocks — reference is not procedural\n"
    "- Convert prose to tables where meaning is preserved or improved\n\n"
    "FRONTMATTER — produce exactly this structure with real content, no placeholders:\n"
    "---\n"
    "description: Write a real one-sentence description of what commands and syntax this reference covers.\n"
    "icon: brackets-curly\n"
    "---\n\n"
    "OUTPUT: Complete GitBook markdown document. No preamble, no commentary, no explanation of choices. "
    "Preserve all technical content from the source — every command, option, and example must appear."
)

# ── Helpers ───────────────────────────────────────────────────────────────────

def read_file(path):
    with open(path, encoding="utf-8") as f:
        return f.read()

def write_file(path, content):
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def normalise_path(path):
    """Ensure forward slashes for SUMMARY.md compatibility."""
    return path.replace(os.sep, "/")

def extract_meta(text):
    """Extract key:value pairs from Diataxis frontmatter. Handles colons in values."""
    meta = {}
    if not text.startswith("---"):
        return meta
    end = text.find("---", 3)
    if end == -1:
        return meta
    for line in text[3:end].strip().splitlines():
        if ":" in line:
            parts = line.split(":", 1)  # split on first colon only — preserves colons in values
            meta[parts[0].strip()] = parts[1].strip()
    return meta

def strip_yaml_fences(text):
    """
    Remove ```yaml code fences that models sometimes wrap frontmatter in.
    Handles: ```yaml\n---\n...\n---\n``` and plain ```\n---\n...\n---\n```
    """
    text = re.sub(r'^```(?:yaml)?\s*\n(---)', r'\1', text, flags=re.MULTILINE)
    text = re.sub(r'^(---)\s*\n```\s*$', r'\1', text, flags=re.MULTILINE)
    return text

def strip_markdown_fence(text):
    """
    Remove full-document ```markdown ... ``` wrapper that models occasionally produce.
    Detects: text starts with ```markdown\n or ```\n and ends with \n```
    Only strips if the fence wraps the entire response.
    """
    text = text.strip()
    # Opening fence variants: ```markdown, ```md, or plain ```
    if re.match(r'^```(?:markdown|md)?\s*\n', text):
        # Strip opening fence line
        text = re.sub(r'^```(?:markdown|md)?\s*\n', '', text)
        # Strip closing ``` at end of document
        text = re.sub(r'\n```\s*$', '', text)
    return text

# ── Sonnet caller with retry ──────────────────────────────────────────────────

client = anthropic.Anthropic()

def call_sonnet(system_prompt, source_doc, label):
    print("  [" + label + "] Calling Sonnet 4.6...", end="", flush=True)

    user_prompt = (
        "Here is the Diataxis source document to transform:\n\n"
        "---BEGIN SOURCE---\n"
        + source_doc
        + "\n---END SOURCE---\n\n"
        "Here is the complete GitBook block reference — read it fully before making any block decisions:\n\n"
        + GITBOOK_BLOCK_REFERENCE
        + "\n\nTransform the source document into GitBook-formatted markdown. "
        "Reason carefully through which blocks best serve the learning experience "
        "for each section of this specific document. "
        "Apply all rendering safety rules without exception. "
        "Write real frontmatter values — not placeholders. "
        "Preserve all technical content from the source without omission. "
        "Output only the final GitBook document — no preamble, no commentary."
    )

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = client.messages.create(
                model=MODEL,
                max_tokens=MAX_TOKENS,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}]
            )
            result = strip_markdown_fence(response.content[0].text)
            result = strip_yaml_fences(result)
            print(" done (" + str(len(result)) + " chars)")

            # Early warning: document should start with frontmatter
            first_line = result.splitlines()[0] if result.splitlines() else ""
            if not first_line.startswith("---"):
                print("  [WARN] Output does not start with frontmatter (first line: " + repr(first_line[:60]) + ")")
                print("  [WARN] Check this file before proceeding — it may be malformed.")

            return result

        except Exception as e:
            if attempt < MAX_RETRIES:
                delay = RETRY_DELAYS[attempt - 1]
                print(" error (attempt " + str(attempt) + "/" + str(MAX_RETRIES) + ") — retrying in " + str(delay) + "s...")
                time.sleep(delay)
                print("  [" + label + "] Retrying...", end="", flush=True)
            else:
                print(" FAILED after " + str(MAX_RETRIES) + " attempts: " + str(e))
                sys.exit(1)

# ── SUMMARY.md ────────────────────────────────────────────────────────────────

def build_summary_section(objective_id, file_map):
    """
    Path fix: .gitbook.yaml root: ./04_publish/output means SUMMARY.md paths
    must be relative to that root — strip OUTPUT_BASE prefix so paths read as
    x200_101/explanation.md not 04_publish/output/x200_101/explanation.md.

    Link text fix: strip surrounding quotes Sonnet may include in title metadata.
    """
    root_prefix = normalise_path(OUTPUT_BASE) + "/"
    lines = ["## RHCSA — " + objective_id, ""]
    for link_text, path in file_map:
        clean_text = link_text.strip('"\'\' ')
        clean_path = normalise_path(path)
        if clean_path.startswith(root_prefix):
            clean_path = clean_path[len(root_prefix):]
        lines.append("* [" + clean_text + "](" + clean_path + ")")
    lines.append("")
    return "\n".join(lines)

def update_summary(objective_id, section_text):
    marker = "## RHCSA — " + objective_id
    existing = read_file(SUMMARY_FILE) if os.path.exists(SUMMARY_FILE) else "# Summary\n\n"

    if marker in existing:
        pattern = re.compile(
            r'## RHCSA — ' + re.escape(objective_id) + r'.*?(?=^## |\Z)',
            re.MULTILINE | re.DOTALL
        )
        updated = pattern.sub(section_text, existing)
    else:
        updated = existing.rstrip("\n") + "\n\n" + section_text

    write_file(SUMMARY_FILE, updated)

# ── .gitbook.yaml bootstrapper ────────────────────────────────────────────────

def ensure_gitbook_yaml():
    if not os.path.exists(GITBOOK_YAML):
        write_file(GITBOOK_YAML,
            "root: ./\n\nstructure:\n  readme: ./README.md\n  summary: ./SUMMARY.md\n")
        print("  Created: " + GITBOOK_YAML)
    else:
        print("  Exists:  " + GITBOOK_YAML)

# ── Git ───────────────────────────────────────────────────────────────────────

def git_run(args, check=True):
    r = subprocess.run(["git"] + args, capture_output=True, text=True)
    if check and r.returncode != 0:
        print("  git " + " ".join(args) + " failed: " + r.stderr.strip())
        sys.exit(1)
    return r

def commit_and_push(objective_id, count):
    git_run(["add", "."])
    if not git_run(["status", "--porcelain"], check=False).stdout.strip():
        print("  Nothing to commit.")
        return
    msg = "feat: Stage 4 complete — GitBook publish " + objective_id + " (" + str(count) + " docs)"
    git_run(["commit", "-m", msg])
    print("  Committed: " + msg)
    push = git_run(["push", "origin", "main"], check=False)
    if push.returncode != 0:
        if "fetch first" in push.stderr or "rejected" in push.stderr:
            print("  Rejected — rebasing...")
            git_run(["pull", "--rebase", "origin", "main"])
            git_run(["push", "origin", "main"])
            print("  Pushed after rebase.")
        else:
            print("  Push failed: " + push.stderr.strip())
            sys.exit(1)
    else:
        print("  Pushed.")

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 stage4_run.py 03_diataxis/output/x200_101")
        sys.exit(1)

    input_prefix = sys.argv[1].rstrip("/")
    objective_id = os.path.basename(input_prefix)
    source_dir   = os.path.dirname(input_prefix)
    output_dir   = os.path.join(OUTPUT_BASE, objective_id)

    print("Stage 4 - GitBook Publish (Sonnet-powered)")
    print("Input:     " + input_prefix + "_*.md")
    print("Output:    " + output_dir + "/")
    print("Objective: " + objective_id)
    print("Model:     " + MODEL + "  (max_tokens=" + str(MAX_TOKENS) + ")")
    print()

    print("Loading GitBook reference from _config/...")
    load_gitbook_reference()

    all_src   = sorted([f for f in os.listdir(source_dir)
                        if f.startswith(objective_id) and f.endswith(".md")])
    exp_files = [f for f in all_src if "_explanation" in f]
    tut_files = sorted([f for f in all_src if "_tutorial_" in f])
    how_files = sorted([f for f in all_src if "_howto_" in f])
    ref_files = [f for f in all_src if "_reference" in f]

    print("Found: " + str(len(all_src)) + " source documents")
    print("  " + str(len(exp_files)) + " explanation  |  "
          + str(len(tut_files)) + " tutorial(s)  |  "
          + str(len(how_files)) + " how-to(s)  |  "
          + str(len(ref_files)) + " reference")
    print()

    if not exp_files or not ref_files:
        print("ERROR: Missing explanation or reference — cannot proceed.")
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)
    written = []

    # ── Explanation ───────────────────────────────────────────────────────────
    print("── Explanation " + "─" * 60)
    for fname in exp_files:
        text     = read_file(os.path.join(source_dir, fname))
        meta     = extract_meta(text)
        result   = call_sonnet(EXPLANATION_SYSTEM, text, "Explanation")
        out_path = os.path.join(output_dir, "explanation.md")
        write_file(out_path, result)
        written.append((meta.get("title", "Understanding the Shell"), out_path))
        print("  Written: " + out_path + "  (" + str(len(result)) + " chars)")
    print()

    # ── Reference ────────────────────────────────────────────────────────────
    print("── Reference " + "─" * 62)
    for fname in ref_files:
        text     = read_file(os.path.join(source_dir, fname))
        meta     = extract_meta(text)
        result   = call_sonnet(REFERENCE_SYSTEM, text, "Reference")
        out_path = os.path.join(output_dir, "reference.md")
        write_file(out_path, result)
        written.append((meta.get("title", "Command Reference"), out_path))
        print("  Written: " + out_path + "  (" + str(len(result)) + " chars)")
    print()

    # ── Tutorials ─────────────────────────────────────────────────────────────
    print("── Tutorials (" + str(len(tut_files)) + ") " + "─" * 58)
    for i, fname in enumerate(tut_files, start=1):
        text      = read_file(os.path.join(source_dir, fname))
        meta      = extract_meta(text)
        result    = call_sonnet(TUTORIAL_SYSTEM, text, "Tutorial " + str(i).zfill(2))
        out_path  = os.path.join(output_dir, "tutorial_" + str(i).zfill(2) + ".md")
        write_file(out_path, result)
        link_text = meta.get("title", "Tutorial " + str(i))
        written.append(("Tutorial " + str(i) + ": " + link_text, out_path))
        print("  Written: " + out_path + "  (" + str(len(result)) + " chars)")
    print()

    # ── How-tos ───────────────────────────────────────────────────────────────
    print("── How-tos (" + str(len(how_files)) + ") " + "─" * 60)
    for i, fname in enumerate(how_files, start=1):
        text      = read_file(os.path.join(source_dir, fname))
        meta      = extract_meta(text)
        result    = call_sonnet(HOWTO_SYSTEM, text, "How-to " + str(i).zfill(2))
        out_path  = os.path.join(output_dir, "howto_" + str(i).zfill(2) + ".md")
        write_file(out_path, result)
        link_text = meta.get("title", "How-to " + str(i))
        written.append(("How-to " + str(i) + ": " + link_text, out_path))
        print("  Written: " + out_path + "  (" + str(len(result)) + " chars)")
    print()

    # ── Infrastructure ────────────────────────────────────────────────────────
    print("── Infrastructure " + "─" * 57)
    ensure_gitbook_yaml()
    update_summary(objective_id, build_summary_section(objective_id, written))
    print("  Updated: " + SUMMARY_FILE)
    print()

    # ── Git ───────────────────────────────────────────────────────────────────
    print("── Git " + "─" * 68)
    commit_and_push(objective_id, len(written))
    print()

    # ── Final summary ─────────────────────────────────────────────────────────
    print("Stage 4 complete.")
    print()
    for _, path in written:
        print("  " + normalise_path(path) + "  (" + str(os.path.getsize(path)) + " bytes)")
    print()
    print("  Total: " + str(len(written)) + " documents")
    print()
    print("Run quality gate:")
    print("  python3 stage4_verify.py " + normalise_path(output_dir))
    print()
    print("Then verify GitBook rendered correctly at your space URL.")

if __name__ == "__main__":
    main()
