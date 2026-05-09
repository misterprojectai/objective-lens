#!/usr/bin/env python3
"""
Stage 5 - iximiuz Labs Tutorial Generator
Transforms Stage 3 Diataxis documents into production iximiuz tutorial format.

Reads from:  03_diataxis/output/<obj>/<obj>_tutorial_*.md
             03_diataxis/output/<obj>/<obj>_howto_*.md
Writes to:   05_iximiuz/output/<name>/index.md
             05_iximiuz/output/<name>/__static__/cover.png
Deploys via: labctl content create tutorial + labctl content push

Usage:
  python3 stage5_run.py x200_101              # all 12 docs
  python3 stage5_run.py x200_101 tutorial 1   # tutorial_01 only
  python3 stage5_run.py x200_101 howto 1      # howto_01 only
"""

import anthropic
import os
import re
import struct
import subprocess
import sys
import time
import zlib
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. Run: pip install pyyaml --break-system-packages")
    sys.exit(1)

# ── CONFIG ───────────────────────────────────────────────────────────────────

MODEL      = "claude-sonnet-4-6"
MAX_TOKENS = 16000

STAGE3_DIR = "03_diataxis/output"
STAGE5_DIR = "05_iximiuz/output"

# iximiuz platform reference — loaded into every Sonnet call
SKILL_FILE      = "_config/iximiuz-ref/iximiuz-CLAUDE.md"
# Canonical format sample — first 6000 chars used (token efficiency; full file is 52KB)
SAMPLE_TUTORIAL = "_config/iximiuz-ref/iximiuz-sample-tutorial.md"
SAMPLE_TRIM     = 6000

CATEGORY_NAMES = {
    "linux", "networking", "containers", "kubernetes",
    "programming", "observability", "security", "ci-cd",
    "generative-ai", "cloud", "iac"
}
FORBIDDEN_TAGS = CATEGORY_NAMES | {"ex200"}

# ── PNG GENERATION ───────────────────────────────────────────────────────────

def create_cover_png():
    """Create a minimal valid 1x1 white PNG as cover placeholder."""
    def chunk(ctype, data):
        c = ctype + data
        return struct.pack('>I', len(data)) + c + struct.pack('>I', zlib.crc32(c) & 0xffffffff)
    return (
        b'\x89PNG\r\n\x1a\n'
        + chunk(b'IHDR', struct.pack('>IIBBBBB', 1, 1, 8, 2, 0, 0, 0))
        + chunk(b'IDAT', zlib.compress(b'\x00\xff\xff\xff'))
        + chunk(b'IEND', b'')
    )

# ── FILE I/O ─────────────────────────────────────────────────────────────────

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def write_binary(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as f:
        f.write(data)

# ── FRONTMATTER ──────────────────────────────────────────────────────────────

def extract_frontmatter(content):
    """
    Returns (fm_dict, error_str).
    fm_dict is {} and error_str is set if YAML parse fails.
    """
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return {}, "No frontmatter block found"
    try:
        fm = yaml.safe_load(match.group(1)) or {}
        return fm, None
    except yaml.YAMLError as e:
        return {}, str(e)

def strip_preamble(content):
    """Strip any text Sonnet prepends before the opening --- frontmatter."""
    lines = content.splitlines(keepends=True)
    for i, line in enumerate(lines):
        if line.strip() == '---':
            return ''.join(lines[i:])
    return content

# ── DOCUMENT DISCOVERY ───────────────────────────────────────────────────────

def build_name(obj_id, doc_type, index):
    """Build iximiuz content name: rhcsa-x200101-tutorial-1"""
    slug = obj_id.replace('_', '')
    return f"rhcsa-{slug}-{doc_type}-{index}"

def get_stage3_docs(obj_id, filter_type=None, filter_index=None):
    """Return ordered list of docs to process (tutorials then howtos)."""
    stage3_dir = Path(STAGE3_DIR) / obj_id
    docs = []
    for glob, doc_type, index_key in [
        (f"{obj_id}_tutorial_*.md", "tutorial", "tutorial_index"),
        (f"{obj_id}_howto_*.md",    "howto",    "howto_index"),
    ]:
        for path in sorted(stage3_dir.glob(glob)):
            fm, _ = extract_frontmatter(read_file(path))
            index  = fm.get(index_key) or fm.get('tutorial_index') or fm.get('howto_index', 1)
            docs.append({
                'path':        path,
                'frontmatter': fm,
                'type':        doc_type,
                'index':       index,
                'name':        build_name(obj_id, doc_type, index),
            })
    if filter_type:
        docs = [d for d in docs if d['type'] == filter_type]
    if filter_index:
        docs = [d for d in docs if d['index'] == filter_index]
    return docs

# ── SERVER NAME DETECTION ────────────────────────────────────────────────────

def get_server_name(base_name, pause=1):
    """
    Get actual server name after create.
    iximiuz appends an 8-char hex suffix: base-name-a1b2c3d4.
    Tutorials and how-tos are both kind=tutorial on iximiuz.
    """
    if pause:
        time.sleep(pause)
    result = subprocess.run(
        ['labctl', 'content', 'list', '--kind', 'tutorial'],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        return None
    hex_pat = re.compile(rf'^{re.escape(base_name)}-[0-9a-f]{{8}}$')
    for line in result.stdout.splitlines():
        line = line.strip()
        if line.startswith('name:'):
            name = line.split(':', 1)[1].strip()
            if name == base_name or hex_pat.match(name):
                return name
    return None

# ── SYSTEM PROMPT ────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are an expert Linux educator and iximiuz Labs content author.
You produce production-quality interactive labs for the RHCSA EX200 certification.

The learner gets a live Rocky Linux 9 terminal in their browser.
Every step they take is verified in real time.
Every mistake gets a diagnostic hint before they get stuck.
When they finish, they have proven they can perform the skill — not just read about it.

## Quality Standard

Outstanding — not acceptable, not good. Outstanding.
A learner completing this lab must feel:
- Clear on what they did and why it matters for the exam
- Confident they can reproduce it under exam conditions
- That the lab anticipated every failure point and had help ready

---

## HARD CONSTRAINTS — VIOLATIONS BREAK THE PLATFORM

### kind
Always: `kind: tutorial` — no other value accepted.

### Machine Name
Playground is `rockylinux`. Machine name is ALWAYS `rocky-01`.
Never `node-01`, never `server`, never anything else.
Every `machine:` field in every task must be `rocky-01`.

### cover
Always: `cover: __static__/cover.png` — exact string, no variations.

### tagz
- Maximum 5 tags — platform hard limit, exceeding causes push failure
- MUST NOT contain: linux, networking, containers, kubernetes, programming,
  observability, security, ci-cd, generative-ai, cloud, iac, ex200
- Good RHCSA tags: rhcsa, bash, shell, ssh, tty, history, redirection, grep, etc.

### NO GitBook syntax
Never use: {%, %}, {% stepper %}, {% hint %}, {% tabs %}, {% code %}
These are GitBook-only and will not render on iximiuz.

### NO code fences inside YAML frontmatter
Never put ``` inside the frontmatter block — it breaks YAML parsing and
causes push failure. Code examples belong in the markdown body only.

### task/component pairing — STRICT
Every `verify_*` and `input_*` task in frontmatter MUST have a paired
`::simple-task` or `::user-input-task` in the markdown body. No exceptions.

### ::remark-box kinds
Valid: `info`, `warning`, `error` — never `danger` (GitBook only).

### ::image-box :src
Filename only — NO `__static__/` prefix in :src.
Correct:   `:src: image.png`
Wrong:     `:src: __static__/image.png`

---

## YAML SAFETY RULES — run: block scripts

### No heredocs
YAML run: blocks cannot contain heredoc syntax. The bare `EOF` marker on its
own line breaks YAML parsing.

WRONG:
  run: |
    cat << 'EOF' >> ~/.bashrc
    export VAR=value
    EOF

CORRECT:
  run: |
    echo 'export VAR=value' >> /home/laborant/.bashrc

### No unquoted special characters in YAML values
Avoid unquoted: `[`, `]`, `*`, `{`, `}`, `?`, `|`, `>`, `!`, `%`, `@`, `&`
These are YAML metacharacters. Use double-quoted strings when values contain them.

---

## NEW TERMINAL TAB (REQUIRED)

The iximiuz playground opens a terminal tab BEFORE init tasks complete.
The first terminal tab will NOT have the PROMPT_COMMAND set — history
verification will silently fail if learners run commands there.

At the VERY START of the tutorial body (first content after frontmatter),
before any sections or steps, add this EXACT block:

::remark-box
---
kind: info
---
**Before running any commands:** click the **+** button in the terminal tab
bar to open a new terminal tab. The playground's history tracking activates
in new sessions only. Commands run in the original tab will not register for
task verification.
::

---

## Playground Template

```yaml
playground:
  name: rockylinux
  machines:
    - name: rocky-01
      resources:
        cpuCount: 2
        ramSize: 2Gi
```

## init_history_flush — EXACT PATTERN, NO VARIATIONS

Every tutorial MUST have this as the FIRST task:

```yaml
tasks:
  init_history_flush:
    init: true
    machine: rocky-01
    user: laborant
    run: |
      echo 'PROMPT_COMMAND="history -a; $PROMPT_COMMAND"' >> /home/laborant/.bashrc
      chown laborant:laborant /home/laborant/.bashrc
```

This writes history after EVERY command. Without it, history is only written
on session exit and all verification tasks will fail.

## History-Based Verification Pattern

```yaml
  verify_command_ran:
    machine: rocky-01
    user: laborant
    run: |
      grep -q 'the_command' /home/laborant/.bash_history && exit 0 || exit 1
    hintcheck: |
      echo "Run: the_command"
      echo "Make sure you are in the new terminal tab (Term 2)."
```

## ::simple-task Pattern (required for every verify_ task)

```markdown
::simple-task
---
:tasks: tasks
:name: verify_command_ran
---
#active
Run `the_command` and observe the output.

#completed
Done — you ran the command successfully 🎉
::
```

---

## Transformation Rules

SOURCE: A Diataxis document — technically correct, well-structured content.
TARGET: A live Rocky Linux 9 interactive lab.

KEEP: All technical content, step sequence, commands, expected outputs.

ADD:
- YAML frontmatter with playground + task definitions
- New terminal tab remark-box at the very top of the body (REQUIRED)
- `::simple-task` for every meaningful step (paired with frontmatter task)
- init tasks to pre-stage the environment
- `::hint-box` for predictable failure points
- `::remark-box` for critical warnings and exam insights
- `::details-box` for optional deep-dives

ADAPT:
- GNOME/graphical steps → skip or note as context only (playground is headless)
- SSH to remote host → use SSH loopback: `ssh laborant@localhost`
- Prompts `[student@rhel9 ~]$` → show as `[laborant@rocky-01 ~]$`

---

## Output Format

Produce ONLY the complete index.md content.
No explanation, no preamble, no trailing commentary.
Output starts with `---` frontmatter and ends with the last line of markdown."""

# ── PROMPT BUILDER ───────────────────────────────────────────────────────────

def build_prompt(doc, skill_content, sample_content):
    source = read_file(doc['path'])
    name   = doc['name']
    dtype  = doc['type']

    return f"""Transform this Stage 3 Diataxis {dtype} document into a production iximiuz Labs tutorial.

## Output content name: `{name}`

## iximiuz Platform Reference (task engine, labctl workflow, content structure)

{skill_content}

---

## Format Sample (MDC syntax — note: sample uses k3s playground, ignore its machine names)

{sample_content[:SAMPLE_TRIM]}

---

## Source Document to Transform

{source}

---

Produce the complete `index.md` for `{name}`.
Start with `---` frontmatter. No preamble. No trailing commentary.

HARD CONSTRAINT CHECKLIST:
- kind: tutorial
- machine: rocky-01 everywhere
- tagz: max 5, no forbidden tags
- cover: __static__/cover.png
- init_history_flush: PROMPT_COMMAND pattern, first task
- New terminal tab ::remark-box: FIRST thing in the body
- Every verify_* task paired with ::simple-task in body
- No GitBook liquid syntax
- No code fences (```) inside frontmatter
- No heredocs in run: blocks"""

# ── VALIDATION ───────────────────────────────────────────────────────────────

def validate(content, name):
    errors   = []
    warnings = []

    if not content.startswith('---'):
        errors.append("Does not start with frontmatter ---")
        return errors, warnings

    # Explicit YAML parse check — report the actual error, not just missing fields
    fm, yaml_err = extract_frontmatter(content)
    if yaml_err and not fm:
        errors.append(f"YAML parse failure: {yaml_err}")
        return errors, warnings

    # Required fields
    if fm.get('kind') != 'tutorial':
        errors.append(f"kind='{fm.get('kind')}' must be 'tutorial'")
    if not fm.get('title'):
        errors.append("Missing title")
    if not fm.get('description'):
        errors.append("Missing description")
    if not fm.get('categories'):
        errors.append("Missing categories")
    if not fm.get('tagz'):
        errors.append("Missing tagz")
    if not fm.get('createdAt'):
        errors.append("Missing createdAt")
    if not fm.get('cover'):
        errors.append("Missing cover")
    elif not str(fm['cover']).startswith('__static__/'):
        errors.append(f"cover must start with __static__/ — got '{fm['cover']}'")

    # tagz
    tagz = [str(t) for t in (fm.get('tagz') or [])]
    if len(tagz) > 5:
        errors.append(f"tagz has {len(tagz)} — max 5")
    bad = [t for t in tagz if t in FORBIDDEN_TAGS]
    if bad:
        errors.append(f"tagz contains forbidden tags: {bad}")

    # Tasks
    tasks = fm.get('tasks') or {}

    # Machine name check
    for tname, tdef in tasks.items():
        if isinstance(tdef, dict):
            m = tdef.get('machine', '')
            if m and m != 'rocky-01':
                errors.append(f"Task '{tname}': machine='{m}' must be 'rocky-01'")

    # init_history_flush
    if 'init_history_flush' not in tasks:
        errors.append("Missing init_history_flush task")
    else:
        idf = tasks['init_history_flush']
        if isinstance(idf, dict) and 'PROMPT_COMMAND' not in idf.get('run', ''):
            errors.append("init_history_flush missing PROMPT_COMMAND pattern")

    # task/component pairing
    for tname in tasks:
        if tname.startswith(('verify_', 'input_')):
            if f':name: {tname}' not in content:
                errors.append(f"Task '{tname}' has no paired ::simple-task or ::user-input-task")

    # Platform separation
    if '{%' in content or '%}' in content:
        errors.append("Contains GitBook liquid syntax — platform violation")

    # Fence inside frontmatter
    end_fm = content.find('\n---\n', 4)
    if end_fm > 0 and '```' in content[:end_fm]:
        errors.append("Code fence (```) inside frontmatter — will cause push failure")

    # New terminal tab remark-box
    body_start = content.find('\n---\n', 4)
    if body_start > 0:
        body_head = content[body_start:body_start + 400]
        if '::remark-box' not in body_head:
            warnings.append("New terminal tab ::remark-box not found near start of body")

    # MDC balance
    opens = content.count('::')
    if opens % 2 != 0:
        warnings.append(f"Odd :: count ({opens}) — check for unclosed MDC blocks")

    # image-box __static__ prefix
    if ':src: __static__/' in content:
        warnings.append("::image-box :src contains __static__/ prefix — filename only")

    return errors, warnings

# ── SONNET CALL ──────────────────────────────────────────────────────────────

def call_sonnet(client, prompt, attempt=1):
    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        )
        if response.stop_reason == "max_tokens":
            print("  WARNING: hit max_tokens — output may be truncated")
        return response.content[0].text
    except anthropic.RateLimitError:
        if attempt <= 3:
            wait = 30 * attempt
            print(f"  Rate limit — waiting {wait}s ({attempt}/3)")
            time.sleep(wait)
            return call_sonnet(client, prompt, attempt + 1)
        raise

# ── LABCTL ───────────────────────────────────────────────────────────────────

def labctl_create(name, output_dir):
    """Create tutorial on server. Returns actual server name (with hex suffix)."""
    result = subprocess.run(
        ['labctl', 'content', 'create', 'tutorial', name, '--dir', output_dir],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        stderr = result.stderr.lower()
        if any(x in stderr for x in ('already exists', 'conflict', 'exist')):
            print(f"  Already exists — detecting server name...")
            actual = get_server_name(name)
            if actual:
                print(f"  Server name: {actual}")
                return actual
            return name
        print(f"  ERROR create: {result.stderr.strip()}")
        return None

    actual = get_server_name(name)
    if actual and actual != name:
        print(f"  Server name: {actual}")
    else:
        actual = actual or name
        print(f"  Created: {actual}")
    return actual

def labctl_push(actual_name, output_dir):
    """Push content to server using actual server name."""
    result = subprocess.run(
        ['labctl', 'content', 'push', 'tutorial', actual_name,
         '--dir', output_dir, '--force'],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"  ERROR push: {result.stderr.strip()}")
        return False
    print(f"  Pushed ✓")
    return True

# ── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 stage5_run.py <obj_id> [type] [index]")
        print("       python3 stage5_run.py x200_101")
        print("       python3 stage5_run.py x200_101 tutorial 1")
        print("       python3 stage5_run.py x200_101 howto 1")
        sys.exit(1)

    obj_id       = sys.argv[1].strip()
    filter_type  = sys.argv[2].strip() if len(sys.argv) > 2 else None
    filter_index = int(sys.argv[3]) if len(sys.argv) > 3 else None

    if '_' not in obj_id and len(obj_id) == 7:
        obj_id = obj_id[:4] + '_' + obj_id[4:]

    print(f"\n{'='*60}")
    print(f"Stage 5 — iximiuz Labs: {obj_id}")
    if filter_type:
        print(f"Filter: {filter_type} {filter_index or 'all'}")
    print(f"{'='*60}\n")

    stage3_dir = Path(STAGE3_DIR) / obj_id
    if not stage3_dir.exists():
        print(f"ERROR: Stage 3 output not found: {stage3_dir}")
        print(f"Run:   python3 stage3_run.py 02_map/output/{obj_id}/{obj_id}_mapped-passages.md")
        sys.exit(1)

    for fpath in [SKILL_FILE, SAMPLE_TUTORIAL]:
        if not Path(fpath).exists():
            print(f"ERROR: Config file not found: {fpath}")
            sys.exit(1)

    print("Loading reference files...")
    skill_content  = read_file(SKILL_FILE)
    sample_content = read_file(SAMPLE_TUTORIAL)

    docs = get_stage3_docs(obj_id, filter_type, filter_index)
    if not docs:
        print(f"ERROR: No documents found matching filter")
        sys.exit(1)

    print(f"Processing {len(docs)} document(s):")
    for d in docs:
        print(f"  [{d['type']:8s}] {d['path'].name} → {d['name']}")

    client  = anthropic.Anthropic()
    results = []
    cover   = create_cover_png()

    for i, doc in enumerate(docs, 1):
        name       = doc['name']
        output_dir = str(Path(STAGE5_DIR) / name)
        index_path = str(Path(output_dir) / "index.md")
        cover_path = str(Path(output_dir) / "__static__" / "cover.png")

        print(f"\n[{i}/{len(docs)}] {doc['path'].name} → {name}")
        print(f"  Calling Sonnet 4.6...")

        prompt  = build_prompt(doc, skill_content, sample_content)
        raw     = call_sonnet(client, prompt)
        content = strip_preamble(raw)

        errors, warnings = validate(content, name)
        if errors:
            print(f"  ERRORS ({len(errors)}):")
            for e in errors:
                print(f"    ✗ {e}")
        if warnings:
            for w in warnings:
                print(f"    ⚠ {w}")
        if not errors and not warnings:
            print(f"  Validation passed ✓")

        os.makedirs(Path(output_dir) / "__static__", exist_ok=True)
        actual_name = labctl_create(name, output_dir)
        created     = actual_name is not None

        write_file(index_path, content)
        write_binary(cover_path, cover)

        pushed = labctl_push(actual_name, output_dir) if created else False

        results.append({
            'name':        name,
            'actual_name': actual_name,
            'source':      doc['path'].name,
            'errors':      errors,
            'warnings':    warnings,
            'pushed':      pushed,
        })

        if i < len(docs):
            time.sleep(2)

    # ── Summary ──────────────────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print(f"Stage 5 Complete — {obj_id}")
    print(f"{'='*60}")

    n_clean    = sum(1 for r in results if not r['errors'])
    n_deployed = sum(1 for r in results if r['pushed'])

    print(f"Processed:  {len(results)}")
    print(f"No errors:  {n_clean}/{len(results)}")
    print(f"Deployed:   {n_deployed}/{len(results)}")

    print(f"\nResults:")
    for r in results:
        ok    = "✅" if r['pushed'] else "⚠️ "
        issue = f" [{len(r['errors'])} errors]" if r['errors'] else ""
        warn  = f" [{len(r['warnings'])} warnings]" if r['warnings'] else ""
        sname = f" ({r['actual_name']})" if r['actual_name'] and r['actual_name'] != r['name'] else ""
        print(f"  {ok} {r['name']}{sname}{issue}{warn}")

    if any(r['errors'] for r in results):
        print(f"\nError details:")
        for r in results:
            if r['errors']:
                print(f"  {r['name']}:")
                for e in r['errors']:
                    print(f"    ✗ {e}")

    if n_deployed < len(results):
        print(f"\nRetry failed deploys:")
        for r in results:
            if not r['pushed'] and r['actual_name']:
                d = str(Path(STAGE5_DIR) / r['name'])
                print(f"  labctl content push tutorial {r['actual_name']} --dir {d} --force")

    print(f"\nNext: python3 build_manifest.py {obj_id}")
    print(f"View: https://labs.iximiuz.com/tutorials")


if __name__ == "__main__":
    main()
