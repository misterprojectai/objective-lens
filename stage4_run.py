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
  python3 stage4_run.py x200_102
"""

import os
import re
import sys
import time
import subprocess
import anthropic

# ── Config ────────────────────────────────────────────────────────────────────

SOURCE_BASE  = "03_diataxis/output"
OUTPUT_BASE  = "04_publish/output"
GITBOOK_YAML = ".gitbook.yaml"
SUMMARY_FILE = "04_publish/output/SUMMARY.md"
MODEL        = "claude-sonnet-4-6"
MAX_TOKENS   = 16000
MAX_RETRIES  = 3
RETRY_DELAYS = [5, 15, 30]

# ── GitBook reference loader ──────────────────────────────────────────────────

GITBOOK_BLOCK_REFERENCE = ""  # populated by load_gitbook_reference()

GITBOOK_REF_FILES = [
    ("_config/gitbook-blocks.md", "GitBook Blocks — Official Documentation"),
    ("_config/gitbook-skill.md",  "GitBook External Editing Skill"),
]

RENDERING_SAFETY_RULES = """

---

# Rendering Safety Rules — NEVER VIOLATE

CONFLICT RESOLUTION: The official GitBook documentation uses ### (H3) for step
headings inside stepper blocks. The skill file uses ## (H2). ### is canonical.
Always use ### for step titles inside {% step %} blocks.

CODE FENCE RULES:
  - Every ``` opening MUST have a matching ``` closing. Count them.
  - NEVER place --- as content on its own line inside a code block. GitBook
    interprets --- as a horizontal rule, breaking out of the fence.
  - NEVER produce two consecutive code blocks with no content between them.
  - NEVER leave raw output text (unindented, no fence) between two code blocks.

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
  - No steppers nested inside steppers
  - No tabs nested inside tabs
  - Hints inside steps: valid and encouraged
  - Code blocks inside hints and steps: valid

FRONTMATTER:
  - Use bare --- delimiters ONLY. NEVER wrap in ```yaml``` fences.
  - description field REQUIRED. Write a real sentence — not a placeholder.
  - icon field REQUIRED. Use the icon specified in the contract.

PLATFORM:
  - NEVER use iximiuz MDC syntax (::simple-task, ::remark-box, ::hint-box)
  - This output is GitBook ONLY.

QUALITY:
  - Every block must be semantically justified. No decorative blocks.
  - Do not truncate content from the source document.
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
        print("These files must exist in _config/ before Stage 4 can run:")
        print("  _config/gitbook-blocks.md  — GitBook blocks official documentation")
        print("  _config/gitbook-skill.md   — GitBook external editing skill")
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
    "- Expandable <details>: deep dives that interrupt reading flow — collapsed by default\n"
    "- Columns: two concepts best understood side-by-side\n"
    "- Tabs: only for genuinely distinct conceptual paths (rare)\n"
    "- Code blocks with title: illustrative examples embedded in text\n"
    "- Quote blocks: key definitions or memorable principles\n"
    "- End with 'What to Do Next' section using content-ref blocks linking to all related "
    "tutorials, how-tos, and the reference from this objective\n"
    "- NO stepper blocks — explanations are not procedural\n\n"
    "CRITICAL — CODE FENCE SAFETY:\n"
    "- Count every ``` you open. Every one must be closed.\n"
    "- If an illustrative example contains --- on its own line, place it inside a titled "
    "{% code %} block, NOT a plain fenced block. The --- will break a plain fence.\n"
    "- Never place raw output text between two code blocks without a fence around it.\n\n"
    "FRONTMATTER — real content, no placeholders:\n"
    "---\n"
    "description: One real sentence describing what this page explains.\n"
    "icon: book-open\n"
    "---\n\n"
    "OUTPUT: Complete GitBook markdown. No preamble, no commentary. "
    "Preserve all technical content from the source."
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
    "- Open with hint (info): prerequisites — what the reader needs, stated tightly\n"
    "- The entire procedure lives inside ONE stepper block\n"
    "- Each step = one meaningful action with a clear ### heading as the step title\n"
    "- Inside each step:\n"
    "    - Tight imperative instruction (1-3 sentences maximum)\n"
    "    - Code block with bash language tag for every command\n"
    "    - Titled code block ('Output') or success hint for expected output — REQUIRED at checkpoints\n"
    "    - Warning hint for syntax gotchas specific to that step\n"
    "    - Danger hint for destructive or privilege-escalating operations\n"
    "    - Tabs inside a step ONLY for two valid command forms (short/long flag)\n"
    "    - Expandable <details> for optional recovery paths\n"
    "- Close with success hint AFTER the stepper: what the learner has accomplished\n\n"
    "CRITICAL — CODE FENCE SAFETY:\n"
    "- Count every ``` you open. Every one must be closed.\n"
    "- If expected output contains --- on its own line, use a titled {% code %} block "
    "instead of a plain fence. Plain fences break on ---.\n"
    "- Do NOT produce an intro preview block before the stepper. The stepper already "
    "shows all expected output inline. Any prose like 'this tutorial will produce...' "
    "followed by a code block MUST be removed — it breaks GitBook rendering.\n"
    "- Never place raw output text (numbers, paths, unindented lines) outside a fence.\n\n"
    "FRONTMATTER — real content, no placeholders:\n"
    "---\n"
    "description: One real sentence — what the learner will be able to do.\n"
    "icon: graduation-cap\n"
    "---\n\n"
    "OUTPUT: Complete GitBook markdown. No preamble, no commentary. "
    "Preserve all technical content from the source."
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
    "    - Warning hint for syntax traps or silent failure modes\n"
    "    - Danger hint for destructive operations only\n"
    "    - Tabs for short/long flag variants or RHEL version differences\n"
    "    - Expandable <details> for edge cases\n"
    "- After the stepper: Verification section — success hint with commands + expected output\n"
    "- After verification: Troubleshooting section — warning hint with symptom -> cause -> fix\n\n"
    "CRITICAL — CODE FENCE SAFETY:\n"
    "- Count every ``` you open. Every one must be closed.\n"
    "- If a command or output contains --- on its own line, use a titled {% code %} block "
    "instead of a plain fence. Plain fences break on ---.\n"
    "- Never produce two consecutive code blocks with nothing between them.\n"
    "- Never place raw output text outside a fence.\n\n"
    "FRONTMATTER — real content, no placeholders:\n"
    "---\n"
    "description: One real sentence — the specific task this guide accomplishes.\n"
    "icon: wrench\n"
    "---\n\n"
    "OUTPUT: Complete GitBook markdown. No preamble, no commentary. "
    "Preserve all steps, verification, and troubleshooting from the source."
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
    "- Titled code blocks ('Example'): usage examples immediately following syntax\n"
    "- Warning hints: deprecated options, dangerous flags, exam-critical gotchas\n"
    "- Tabs: show the same construct with short and long flag variants\n"
    "- Expandable <details>: exhaustive option tables rarely needed at a glance\n"
    "- NO stepper blocks — reference is not procedural\n"
    "- Convert prose to tables where meaning is preserved\n\n"
    "CRITICAL — CODE FENCE SAFETY:\n"
    "- Count every ``` you open. Every one must be closed.\n"
    "- If a syntax example contains --- on its own line, use a titled {% code %} block.\n"
    "- Never produce two consecutive code blocks with nothing between them.\n\n"
    "FRONTMATTER — real content, no placeholders:\n"
    "---\n"
    "description: One real sentence — what commands and syntax this reference covers.\n"
    "icon: brackets-curly\n"
    "---\n\n"
    "OUTPUT: Complete GitBook markdown. No preamble, no commentary. "
    "Every command, option, and example from the source must appear."
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
            parts = line.split(":", 1)
            meta[parts[0].strip()] = parts[1].strip()
    return meta

def strip_yaml_fences(text):
    """Remove ```yaml fences that models sometimes wrap frontmatter in."""
    text = re.sub(r'^```(?:yaml)?\s*\n(---)', r'\1', text, flags=re.MULTILINE)
    text = re.sub(r'^(---)\s*\n```\s*$', r'\1', text, flags=re.MULTILINE)
    return text

def strip_markdown_fence(text):
    """Remove full-document ```markdown wrapper that models occasionally produce."""
    text = text.strip()
    if re.match(r'^```(?:markdown|md)?\s*\n', text):
        text = re.sub(r'^```(?:markdown|md)?\s*\n', '', text)
        text = re.sub(r'\n```\s*$', '', text)
    return text

def strip_tutorial_preview_block(text):
    """
    Remove intro preview code blocks from tutorial/howto output.
    These appear before {% stepper %} and break GitBook rendering when
    they contain --- as content or leave unclosed fences.
    """
    stepper_pos = text.find('{% stepper %}')
    if stepper_pos == -1:
        return text

    intro = text[:stepper_pos]
    rest  = text[stepper_pos:]

    # Remove fenced code block preceded by "will produce this..." sentence
    intro = re.sub(
        r'(will produce this (output|single line|result|following)[^\n]*)\n\n```[^`]*```\n\n',
        r'\1\n\n',
        intro, flags=re.DOTALL
    )
    intro = re.sub(
        r'(will produce this (output|single line|result|following)[^\n]*)\n```[^`]*```\n',
        r'\1\n',
        intro, flags=re.DOTALL
    )
    # Remove any remaining fenced code block in intro that would leave an odd fence count
    # (catches cases where the preview sentence varies)
    intro_fences = intro.count("```")
    if intro_fences % 2 != 0:
        # Find last endhint before stepper — strip everything after it
        last_endhint = intro.rfind("{% endhint %}")
        if last_endhint != -1:
            intro = intro[:last_endhint + len("{% endhint %}")] + "\n"

    return intro + rest

def fix_fence_issues(text):
    """
    Post-processor that fixes known GitBook code fence rendering failures.
    Runs on all document types after Sonnet output and after preview block stripping.

    Failure patterns handled:
    1. --- as last line inside a code block before another section marker.
       GitBook interprets --- as <hr> and breaks out of the fence.
       Fix: close the fence before the ---.

    2. Empty code block: ``` immediately followed by another ```.
       Fix: remove the empty block entirely.

    3. Consecutive code blocks with raw output text between them (no fence).
       Lines that are purely whitespace+numbers+words appearing between a closing
       fence and the next opening fence.
       Fix: wrap the raw output in a plain fence.
    """
    # Fix 1: --- as last meaningful line inside a code block
    # Pattern: code content\n---\n (where --- terminates the block early)
    text = re.sub(
        r'(```(?:bash|text|sh|plain)?\n(?:[^`]|\n)*?)\n---\n(\n```)',
        r'\1\n```\n\n---\n\2',
        text, flags=re.DOTALL
    )
    # Simpler form: content then ---\n with no closing fence on the --- line
    text = re.sub(
        r'(```[^\n]*\n(?:[^\n`][^\n]*\n)+)---\n(?!\n*```)',
        r'\1```\n\n---\n',
        text
    )

    # Fix 2: empty code blocks (``` immediately followed by ```)
    text = re.sub(r'```\n\n```\n', '\n', text)
    text = re.sub(r'```\n```\n', '\n', text)

    # Fix 3: raw output text between two code blocks
    # Pattern: closing ``` then blank line then lines of text then opening ```
    # The text lines must look like output (no markdown syntax)
    def wrap_raw_output(m):
        before = m.group(1)   # closing ```
        raw    = m.group(2)   # raw lines
        after  = m.group(3)   # opening ```bash etc
        # Only wrap if the raw block looks like command output (no ## headings, no {% %})
        if re.search(r'^#{1,3} |{%|<!--', raw, re.MULTILINE):
            return before + raw + after  # leave alone — it's real markdown
        return before + "\n```\n" + raw.strip() + "\n```\n\n" + after
    text = re.sub(
        r'(```\n)(\n(?:[^\n`#][^\n]*\n){1,20}\n)(```(?:bash|text|sh)?)',
        wrap_raw_output,
        text
    )

    return text

def build_expected_file_map(source_dir, output_dir, exp_files, ref_files,
                             tut_files, how_files):
    """
    Pre-build the complete output file map so the explanation call has all
    real filenames available for content-ref blocks.
    """
    fmap = []
    for fname in exp_files:
        meta = extract_meta(read_file(os.path.join(source_dir, fname)))
        fmap.append((meta.get("title", "Understanding the Shell"),
                     os.path.join(output_dir, "explanation.md")))
    for fname in ref_files:
        meta = extract_meta(read_file(os.path.join(source_dir, fname)))
        fmap.append((meta.get("title", "Command Reference"),
                     os.path.join(output_dir, "reference.md")))
    for i, fname in enumerate(tut_files, start=1):
        meta = extract_meta(read_file(os.path.join(source_dir, fname)))
        link = "Tutorial " + str(i) + ": " + meta.get("title", "Tutorial " + str(i))
        fmap.append((link, os.path.join(output_dir,
                                        "tutorial_" + str(i).zfill(2) + ".md")))
    for i, fname in enumerate(how_files, start=1):
        meta = extract_meta(read_file(os.path.join(source_dir, fname)))
        link = "How-to " + str(i) + ": " + meta.get("title", "How-to " + str(i))
        fmap.append((link, os.path.join(output_dir,
                                        "howto_" + str(i).zfill(2) + ".md")))
    return fmap

# ── Sonnet caller with retry ──────────────────────────────────────────────────

client = anthropic.Anthropic()

def call_sonnet(system_prompt, source_doc, label, file_map=None):
    print("  [" + label + "] Calling Sonnet 4.6...", end="", flush=True)

    file_map_section = ""
    if file_map:
        lines = ["\nThe following files exist in this objective's output directory.",
                 "Use ONLY these exact filenames in any content-ref blocks:\n"]
        for link_text, path in file_map:
            fname = os.path.basename(path)
            lines.append("  " + fname + "  —  " + link_text.strip("\"' "))
        file_map_section = "\n".join(lines) + "\n"

    user_prompt = (
        "Here is the Diataxis source document to transform:\n\n"
        "---BEGIN SOURCE---\n"
        + source_doc
        + "\n---END SOURCE---\n\n"
        + file_map_section
        + "Here is the complete GitBook block reference — read it fully before "
        "making any block decisions:\n\n"
        + GITBOOK_BLOCK_REFERENCE
        + "\n\nTransform the source document into GitBook-formatted markdown. "
        "Reason carefully through which blocks best serve the learning experience. "
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

            first_line = result.splitlines()[0] if result.splitlines() else ""
            if not first_line.startswith("---"):
                print("  [WARN] Output does not start with frontmatter: "
                      + repr(first_line[:60]))

            return result

        except Exception as e:
            if attempt < MAX_RETRIES:
                delay = RETRY_DELAYS[attempt - 1]
                print(" error (attempt " + str(attempt) + "/" + str(MAX_RETRIES)
                      + ") — retrying in " + str(delay) + "s...")
                time.sleep(delay)
                print("  [" + label + "] Retrying...", end="", flush=True)
            else:
                print(" FAILED after " + str(MAX_RETRIES) + " attempts: " + str(e))
                sys.exit(1)

# ── SUMMARY.md ────────────────────────────────────────────────────────────────

def build_summary_section(objective_id, file_map):
    """
    Build SUMMARY.md section for one objective.
    Paths are relative to .gitbook.yaml root (04_publish/output/) so strip
    the OUTPUT_BASE prefix: x200_101/explanation.md not 04_publish/output/...
    """
    root_prefix = normalise_path(OUTPUT_BASE) + "/"
    lines = ["## RHCSA — " + objective_id, ""]
    for link_text, path in file_map:
        clean_text = link_text.strip("\"' ")
        clean_path = normalise_path(path)
        if clean_path.startswith(root_prefix):
            clean_path = clean_path[len(root_prefix):]
        lines.append("* [" + clean_text + "](" + clean_path + ")")
    lines.append("")
    return "\n".join(lines)

def update_summary(objective_id, section_text):
    marker   = "## RHCSA — " + objective_id
    existing = read_file(SUMMARY_FILE) if os.path.exists(SUMMARY_FILE) \
               else "# Summary\n\n"

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

GITBOOK_YAML_CONTENT = (
    "root: ./04_publish/output\n\n"
    "structure:\n"
    "  readme: ./README.md\n"
    "  summary: ./SUMMARY.md\n"
)

def ensure_gitbook_yaml():
    if not os.path.exists(GITBOOK_YAML):
        write_file(GITBOOK_YAML, GITBOOK_YAML_CONTENT)
        print("  Created: " + GITBOOK_YAML)
    else:
        # Verify root is correct — warn if not
        content = read_file(GITBOOK_YAML)
        if "root: ./04_publish/output" not in content:
            print("  [WARN] .gitbook.yaml root may be incorrect:")
            print("         Expected: root: ./04_publish/output")
            print("         Found:    " + [l for l in content.splitlines()
                                            if "root:" in l][0] if "root:" in content
                  else "         No root: line found")
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
    msg = ("feat: Stage 4 complete — GitBook publish "
           + objective_id + " (" + str(count) + " docs)")
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

# ── Fence balance check (pre-commit gate) ────────────────────────────────────

def check_fence_balance(written):
    """
    Verify all written files have balanced markdown fences before committing.
    Returns list of (path, fence_count) for any unbalanced files.
    """
    unbalanced = []
    for _, path in written:
        content = read_file(path)
        count   = content.count("```")
        if count % 2 != 0:
            unbalanced.append((path, count))
    return unbalanced

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 stage4_run.py x200_102")
        sys.exit(1)

    objective_id = sys.argv[1].strip().rstrip("/")
    # Accept both bare objective ID and full prefix path
    if os.sep in objective_id or "/" in objective_id:
        objective_id = os.path.basename(objective_id)

    source_dir = os.path.join(SOURCE_BASE, objective_id)
    output_dir = os.path.join(OUTPUT_BASE, objective_id)

    print("Stage 4 - GitBook Publish (Sonnet-powered)")
    print("Objective: " + objective_id)
    print("Input:     " + source_dir + "/")
    print("Output:    " + output_dir + "/")
    print("Model:     " + MODEL + "  (max_tokens=" + str(MAX_TOKENS) + ")")
    print()

    if not os.path.isdir(source_dir):
        print("ERROR: Source directory not found: " + source_dir)
        print("Run Stage 3 first: python3 stage3_run.py "
              "02_map/output/" + objective_id + "/"
              + objective_id + "_mapped-passages.md")
        sys.exit(1)

    print("Loading GitBook reference from _config/...")
    load_gitbook_reference()

    # Discover source documents
    all_src   = sorted([f for f in os.listdir(source_dir)
                        if f.startswith(objective_id) and f.endswith(".md")])
    exp_files = [f for f in all_src if "_explanation" in f]
    tut_files = sorted([f for f in all_src if "_tutorial_" in f])
    how_files = sorted([f for f in all_src if "_howto_"    in f])
    ref_files = [f for f in all_src if "_reference"  in f]

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

    # Build complete file map before any Sonnet calls so explanation has
    # real filenames available for content-ref blocks
    expected_file_map = build_expected_file_map(
        source_dir, output_dir, exp_files, ref_files, tut_files, how_files
    )

    # ── Explanation ───────────────────────────────────────────────────────────
    print("── Explanation " + "─" * 60)
    for fname in exp_files:
        text     = read_file(os.path.join(source_dir, fname))
        meta     = extract_meta(text)
        result   = call_sonnet(EXPLANATION_SYSTEM, text, "Explanation",
                               file_map=expected_file_map)
        result   = fix_fence_issues(result)
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
        result   = fix_fence_issues(result)
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
        result    = strip_tutorial_preview_block(result)
        result    = fix_fence_issues(result)
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
        result    = strip_tutorial_preview_block(result)
        result    = fix_fence_issues(result)
        out_path  = os.path.join(output_dir, "howto_" + str(i).zfill(2) + ".md")
        write_file(out_path, result)
        link_text = meta.get("title", "How-to " + str(i))
        written.append(("How-to " + str(i) + ": " + link_text, out_path))
        print("  Written: " + out_path + "  (" + str(len(result)) + " chars)")
    print()

    # ── Pre-commit fence balance gate ─────────────────────────────────────────
    print("── Pre-commit fence check " + "─" * 49)
    unbalanced = check_fence_balance(written)
    if unbalanced:
        print("  [WARN] Unbalanced fences detected in " + str(len(unbalanced)) + " file(s):")
        for path, count in unbalanced:
            print("    " + normalise_path(path) + "  (" + str(count) + " fences — odd)")
        print("  These files may render incorrectly in GitBook.")
        print("  Run stage4_verify.py after push to confirm and fix.")
    else:
        print("  All " + str(len(written)) + " files: fences balanced")
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
