#!/usr/bin/env python3
"""
Stage 5b - iximiuz Labs Challenge Generator
Derives Format 1 (clean slate) and Format 2 (broken environment) challenges
from Stage 3 Diataxis how-to documents.

Reads from:  03_diataxis/output/<obj>/<obj>_howto_*.md
Writes to:   05_iximiuz/output/<name>/index.md
             05_iximiuz/output/<name>/solution.md
             05_iximiuz/output/<name>/__static__/cover.png
Deploys via: labctl content create challenge + labctl content push

Usage:
  python3 stage5b_run.py x200_101                 # all 12 challenges
  python3 stage5b_run.py x200_101 4 clean         # howto_04 Format 1 only
  python3 stage5b_run.py x200_101 4 broken        # howto_04 Format 2 only
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

SKILL_FILE       = "_config/iximiuz-ref/iximiuz-CLAUDE.md"
SAMPLE_CHALLENGE = "_config/iximiuz-ref/iximiuz-sample-challenge.md"
SAMPLE_TRIM      = 5000  # token efficiency — full file is ~10KB

CATEGORY_NAMES = {
    "linux", "networking", "containers", "kubernetes",
    "programming", "observability", "security", "ci-cd",
    "generative-ai", "cloud", "iac"
}
FORBIDDEN_TAGS    = CATEGORY_NAMES | {"ex200"}
VALID_DIFFICULTIES = {"easy", "medium", "hard"}

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

def build_name(obj_id, index, fmt):
    """Build iximiuz content name: rhcsa-x200101-challenge-4 or -broken-4"""
    slug = obj_id.replace('_', '')
    if fmt == 'clean':
        return f"rhcsa-{slug}-challenge-{index}"
    return f"rhcsa-{slug}-challenge-broken-{index}"

def get_stage3_howtos(obj_id, filter_index=None):
    """Return ordered list of how-to docs to process."""
    stage3_dir = Path(STAGE3_DIR) / obj_id
    docs = []
    for path in sorted(stage3_dir.glob(f"{obj_id}_howto_*.md")):
        fm, _  = extract_frontmatter(read_file(path))
        index  = fm.get('howto_index', 1)
        docs.append({
            'path':        path,
            'frontmatter': fm,
            'index':       index,
            'difficulty':  fm.get('difficulty', 'intermediate'),
        })
    if filter_index:
        docs = [d for d in docs if d['index'] == filter_index]
    return docs

# ── SERVER NAME DETECTION ────────────────────────────────────────────────────

def get_server_name_challenge(base_name, pause=1):
    """
    Get actual server name after create.
    iximiuz appends an 8-char hex suffix: base-name-a1b2c3d4.
    Queries challenge list specifically.
    """
    if pause:
        time.sleep(pause)
    result = subprocess.run(
        ['labctl', 'content', 'list', '--kind', 'challenge'],
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

# ── DIFFICULTY MAPPING ───────────────────────────────────────────────────────

DIFFICULTY_MAP = {
    'foundational': 'easy',
    'beginner':     'easy',
    'easy':         'easy',
    'intermediate': 'medium',
    'medium':       'medium',
    'advanced':     'hard',
    'hard':         'hard',
}

def map_difficulty(raw, fmt):
    """Map Stage 3 difficulty string to iximiuz difficulty.
    Broken environment is always one level harder than clean slate."""
    base = DIFFICULTY_MAP.get(raw, 'medium')
    if fmt == 'broken':
        return 'medium' if base == 'easy' else 'hard'
    return base

# ── YAML SAFETY RULES BLOCK (shared between both system prompts) ──────────────

_YAML_SAFETY = """
## YAML SAFETY RULES — run: block scripts

### No heredocs
YAML run: blocks cannot contain heredoc syntax. The bare `EOF` marker on its
own line breaks YAML parsing and causes push failure.

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

### No code fences inside YAML frontmatter
Never put ``` inside the frontmatter block. Code examples belong in the
markdown body only.

## CRITICAL — Rocky Linux .bashrc Non-Interactive Guard

Rocky Linux .bashrc starts with a non-interactive guard:
  case $-
    *i*) ;;
      *) return;;
  esac

This causes `source ~/.bashrc` to exit immediately in non-interactive subshells.

WRONG — always fails on Rocky Linux:
  bash --norc --noprofile -c 'source /home/laborant/.bashrc; echo $VAR'
  bash -c 'source ~/.bashrc 2>/dev/null; echo $VAR'

CORRECT — grep the file directly for persistence checks:
  LAST=$(grep -E '^(export )?VARNAME=' /home/laborant/.bashrc | tail -1 | cut -d= -f2- | tr -d "'\\"")
  echo "$LAST" | grep -qE 'expected_value' || exit 1
"""

# ── SYSTEM PROMPTS ───────────────────────────────────────────────────────────

SYSTEM_PROMPT_CLEAN = """You are an expert Linux educator producing RHCSA exam preparation challenges for iximiuz Labs.

You generate FORMAT 1 challenges: CLEAN SLATE TASKS.

The learner gets a fresh Rocky Linux 9 system and a task statement. No steps, no guidance.
They either know how to do it or they look it up. Automated verification checks final system state.

## What a Challenge Is

A challenge is NOT a tutorial. No steps, no explanations in the body.
The body contains ONLY:
1. One sentence: what the situation is
2. The task statement: exactly what the learner must do
3. ::simple-task or ::user-input-task blocks (one per verification task)
4. ::hint-box blocks (optional, numbered, progressive — vague to specific)

The challenge body must be SHORT — 50 to 150 lines maximum.
The solution goes in solution.md — NOT in the challenge body.

## Hard Constraints

- kind: challenge — FIXED, no exceptions
- difficulty: easy, medium, or hard — required field
- cover: __static__/cover.png — exact string
- machine: rocky-01 — always
- Max 5 tagz, no category names, no ex200
- NO init tasks unless needed to pre-stage the environment
- NO guided steps in the body
- NO GitBook liquid syntax ({%, %})
- Verification tasks check OUTCOME (file exists, setting active, command works)
- Every verify_/input_ task in frontmatter MUST have a paired ::simple-task in body
""" + _YAML_SAFETY + """
## Verification Pattern — State-Based (NOT history-based)

```yaml
  verify_setting_persistent:
    machine: rocky-01
    user: laborant
    run: |
      LAST=$(grep -E '^(export )?VARNAME=' /home/laborant/.bashrc | tail -1 | cut -d= -f2- | tr -d "'\\"")
      echo "$LAST" | grep -qE 'expected_value' || exit 1
    hintcheck: |
      echo "Check: grep VARNAME ~/.bashrc"
```

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

## Challenge Body Template

```markdown
The `laborant` user needs to [situation description].

Complete the following task on `rocky-01`.

::simple-task
---
:tasks: tasks
:name: verify_task_name
---
#active
What needs to be true when complete.

#completed
Confirmed ✓
::

::hint-box
---
:summary: Hint 1
---
Vague hint pointing toward the right area.
::

::hint-box
---
:summary: Hint 2
---
More specific hint.
::
```

## Output Format

Produce two sections separated by ===SOLUTION===:

Section 1: complete index.md starting with ---
Section 2: complete solution.md content

Example:
---
[frontmatter]
---
[challenge body]
===SOLUTION===
[solution.md content]"""


SYSTEM_PROMPT_BROKEN = """You are an expert Linux educator producing RHCSA exam preparation challenges for iximiuz Labs.

You generate FORMAT 2 challenges: BROKEN ENVIRONMENT DIAGNOSIS.

Init tasks deliberately misconfigure the Rocky Linux 9 system. The learner gets a symptom
description only. They investigate, diagnose, and fix the problem. Verification checks the fix.

## What Makes This Format Valuable

This mirrors real production work and the RHCSA exam.
The learner is told WHAT is wrong (symptom) but not WHY or HOW to fix it.
They use skills from the corresponding tutorial/how-to to diagnose.

## Hard Constraints

- kind: challenge — FIXED
- difficulty: medium or hard (broken environment is never easy)
- cover: __static__/cover.png
- machine: rocky-01 always
- Max 5 tagz, no category names, no ex200
- The init task CREATES the broken state
- The verify task checks the FIX is in place
- failcheck ONLY if the learner does something irreversible
- NO guided steps in body
- NO GitBook liquid syntax
""" + _YAML_SAFETY + """
## Init Task Pattern — Creates the Break

```yaml
tasks:
  init_break_environment:
    init: true
    machine: rocky-01
    run: |
      echo 'export HISTSIZE=0' >> /home/laborant/.bashrc
      echo 'export HISTFILESIZE=0' >> /home/laborant/.bashrc
      chown laborant:laborant /home/laborant/.bashrc
```

## Verify Task Pattern — Checks the Fix

```yaml
  verify_fixed:
    machine: rocky-01
    user: laborant
    run: |
      LAST=$(grep -E '^(export )?HISTSIZE=' /home/laborant/.bashrc | tail -1 | cut -d= -f2- | tr -d "'\\"")
      [ -n "$LAST" ] && [ "$LAST" != "0" ] || exit 1
    hintcheck: |
      echo "Current last HISTSIZE assignment:"
      grep 'HISTSIZE' /home/laborant/.bashrc | tail -3
```

## failcheck Pattern — Only for Catastrophic User Actions

```yaml
    failcheck: |
      [ -f /home/laborant/.bashrc ] || {
        echo ".bashrc deleted — restart the challenge"
        exit 1
      }
```

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

## Challenge Body Template

```markdown
The `laborant` user is reporting: [symptom description — realistic, no cause given].

Investigate and fix the issue on `rocky-01`.

::simple-task
---
:tasks: tasks
:name: verify_fixed
---
#active
[What needs to be true when fixed]

#completed
Fixed ✓
::

::hint-box
---
:summary: Hint 1
---
Where to start looking (not what to look for).
::

::hint-box
---
:summary: Hint 2
---
What to check specifically.
::

::hint-box
---
:summary: Hint 3
---
The exact command that reveals the problem.
::
```

## Output Format

Produce two sections separated by ===SOLUTION===:

Section 1: complete index.md starting with ---
Section 2: complete solution.md explaining:
  1. What was broken and why the init task created that state
  2. How to diagnose it (commands to run)
  3. How to fix it (exact commands)
  4. How to verify the fix"""

# ── PROMPT BUILDERS ──────────────────────────────────────────────────────────

def build_prompt_clean(doc, skill_content, sample_content):
    source     = read_file(doc['path'])
    name       = doc['name_clean']
    difficulty = doc['difficulty_clean']

    return f"""Generate a FORMAT 1 (clean slate) challenge for iximiuz Labs.

## Output content name: `{name}`
## Difficulty: `{difficulty}`

## Platform Reference (task engine, content structure)

{skill_content}

---

## Sample Challenge Format (MDC syntax reference)

{sample_content[:SAMPLE_TRIM]}

---

## Source How-to Document (the skills this challenge tests)

{source}

---

Generate challenge `{name}` at difficulty `{difficulty}`.
The task must be completable using skills taught in the source document.
A learner who completed the tutorial and how-to should be able to pass this.

Output:
[complete index.md]
===SOLUTION===
[complete solution.md]

Start immediately with --- frontmatter. No preamble."""


def build_prompt_broken(doc, skill_content, sample_content):
    source     = read_file(doc['path'])
    name       = doc['name_broken']
    difficulty = doc['difficulty_broken']

    return f"""Generate a FORMAT 2 (broken environment) challenge for iximiuz Labs.

## Output content name: `{name}`
## Difficulty: `{difficulty}`

## Platform Reference (task engine, content structure)

{skill_content}

---

## Sample Challenge Format (MDC syntax reference)

{sample_content[:SAMPLE_TRIM]}

---

## Source How-to Document (the skills this challenge tests)

{source}

---

Generate challenge `{name}` at difficulty `{difficulty}`.
Introduce exactly ONE specific misconfiguration via an init task.
The break must be diagnosable using skills from the source document.
The symptom description must be realistic — what a user would actually report.
Use echo/printf in init tasks, never heredocs.
Use grep to check persistence, never source ~/.bashrc in subshells.

Output:
[complete index.md]
===SOLUTION===
[complete solution.md]

Start immediately with --- frontmatter. No preamble."""

# ── OUTPUT SPLITTING ─────────────────────────────────────────────────────────

def split_output(raw):
    """Split Sonnet output into (index_md, solution_md).
    Warns if separator is absent — indicates Sonnet skipped the solution."""
    content = strip_preamble(raw)
    if '===SOLUTION===' in content:
        parts = content.split('===SOLUTION===', 1)
        return parts[0].strip() + '\n', parts[1].strip()
    print("  WARNING: ===SOLUTION=== separator absent — solution.md will be empty")
    return content, "Solution was not generated. Regenerate with stage5b_run.py."

# ── VALIDATION ───────────────────────────────────────────────────────────────

def validate(content, name, fmt, output_dir):
    errors   = []
    warnings = []

    if not content.startswith('---'):
        errors.append("Does not start with frontmatter ---")
        return errors, warnings

    # Explicit YAML parse check
    fm, yaml_err = extract_frontmatter(content)
    if yaml_err and not fm:
        errors.append(f"YAML parse failure: {yaml_err}")
        return errors, warnings

    # Required fields
    if fm.get('kind') != 'challenge':
        errors.append(f"kind='{fm.get('kind')}' must be 'challenge'")
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

    diff = fm.get('difficulty', '')
    if diff not in VALID_DIFFICULTIES:
        errors.append(f"difficulty='{diff}' must be easy, medium, or hard")

    # tagz
    tagz = [str(t) for t in (fm.get('tagz') or [])]
    if len(tagz) > 5:
        errors.append(f"tagz has {len(tagz)} — max 5")
    bad = [t for t in tagz if t in FORBIDDEN_TAGS]
    if bad:
        errors.append(f"tagz contains forbidden tags: {bad}")

    # Tasks
    tasks = fm.get('tasks') or {}

    # Machine name
    for tname, tdef in tasks.items():
        if isinstance(tdef, dict):
            m = tdef.get('machine', '')
            if m and m != 'rocky-01':
                errors.append(f"Task '{tname}': machine='{m}' must be 'rocky-01'")

    # Format 2 must have at least one init task
    init_tasks = [k for k, v in tasks.items()
                  if isinstance(v, dict) and v.get('init') is True]
    if fmt == 'broken' and not init_tasks:
        errors.append("Format 2 challenge must have at least one init task")

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

    # solution.md existence
    solution_path = Path(output_dir) / "solution.md"
    if solution_path.exists():
        sol = solution_path.read_text()
        if "Solution was not generated" in sol:
            warnings.append("solution.md contains fallback text — regenerate if quality matters")
    else:
        warnings.append("solution.md not written yet")

    # MDC balance
    opens = content.count('::')
    if opens % 2 != 0:
        warnings.append(f"Odd :: count ({opens}) — check for unclosed MDC blocks")

    return errors, warnings

# ── SONNET CALL ──────────────────────────────────────────────────────────────

def call_sonnet(client, system_prompt, user_prompt, attempt=1):
    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
        if response.stop_reason == "max_tokens":
            print("  WARNING: hit max_tokens — output may be truncated")
        return response.content[0].text
    except anthropic.RateLimitError:
        if attempt <= 3:
            wait = 30 * attempt
            print(f"  Rate limit — waiting {wait}s ({attempt}/3)")
            time.sleep(wait)
            return call_sonnet(client, system_prompt, user_prompt, attempt + 1)
        raise

# ── LABCTL ───────────────────────────────────────────────────────────────────

def labctl_create(kind, name, output_dir):
    """Create content on server. Returns actual server name (with hex suffix)."""
    result = subprocess.run(
        ['labctl', 'content', 'create', kind, name, '--dir', output_dir],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        stderr = result.stderr.lower()
        if any(x in stderr for x in ('already exists', 'conflict', 'exist')):
            print(f"  Already exists — detecting server name...")
            actual = get_server_name_challenge(name)
            if actual:
                print(f"  Server name: {actual}")
                return actual
            return name
        print(f"  ERROR create: {result.stderr.strip()}")
        return None

    actual = get_server_name_challenge(name)
    if actual and actual != name:
        print(f"  Server name: {actual}")
    else:
        actual = actual or name
        print(f"  Created: {actual}")
    return actual

def labctl_push(kind, actual_name, output_dir):
    """Push content to server."""
    result = subprocess.run(
        ['labctl', 'content', 'push', kind, actual_name,
         '--dir', output_dir, '--force'],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"  ERROR push: {result.stderr.strip()}")
        return False
    print(f"  Pushed ✓")
    return True

# ── PROCESS ONE CHALLENGE ────────────────────────────────────────────────────

def process_challenge(client, doc, fmt, skill_content, sample_content, cover):
    name       = doc[f'name_{fmt}']
    diff       = doc[f'difficulty_{fmt}']
    output_dir = str(Path(STAGE5_DIR) / name)
    index_path = str(Path(output_dir) / "index.md")
    solution_path = str(Path(output_dir) / "solution.md")
    cover_path = str(Path(output_dir) / "__static__" / "cover.png")

    print(f"\n  [{fmt.upper()}] → {name} ({diff})")
    print(f"    Calling Sonnet 4.6...")

    if fmt == 'clean':
        sys_prompt   = SYSTEM_PROMPT_CLEAN
        user_prompt  = build_prompt_clean(doc, skill_content, sample_content)
    else:
        sys_prompt   = SYSTEM_PROMPT_BROKEN
        user_prompt  = build_prompt_broken(doc, skill_content, sample_content)

    raw = call_sonnet(client, sys_prompt, user_prompt)
    index_content, solution_content = split_output(raw)

    # Validate (solution not written yet — warns about it)
    errors, warnings = validate(index_content, name, fmt, output_dir)
    if errors:
        print(f"    ERRORS ({len(errors)}):")
        for e in errors:
            print(f"      ✗ {e}")
    if warnings:
        for w in warnings:
            if "solution.md not written yet" not in w:  # suppress pre-write warning
                print(f"      ⚠ {w}")
    if not errors:
        print(f"    Validation passed ✓")

    # Deploy
    os.makedirs(Path(output_dir) / "__static__", exist_ok=True)
    actual_name = labctl_create('challenge', name, output_dir)
    created     = actual_name is not None

    # Write files (overwrites scaffold)
    write_file(index_path, index_content)
    write_file(solution_path, solution_content)
    write_binary(cover_path, cover)

    pushed = labctl_push('challenge', actual_name, output_dir) if created else False

    return {
        'name':        name,
        'actual_name': actual_name,
        'fmt':         fmt,
        'difficulty':  diff,
        'errors':      errors,
        'warnings':    [w for w in warnings if "solution.md not written yet" not in w],
        'pushed':      pushed,
    }

# ── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 stage5b_run.py <obj_id> [howto_index] [clean|broken]")
        print("       python3 stage5b_run.py x200_101")
        print("       python3 stage5b_run.py x200_101 4 clean")
        print("       python3 stage5b_run.py x200_101 4 broken")
        sys.exit(1)

    obj_id       = sys.argv[1].strip()
    filter_index = int(sys.argv[2]) if len(sys.argv) > 2 else None
    filter_fmt   = sys.argv[3].strip() if len(sys.argv) > 3 else None

    if '_' not in obj_id and len(obj_id) == 7:
        obj_id = obj_id[:4] + '_' + obj_id[4:]

    print(f"\n{'='*60}")
    print(f"Stage 5b — iximiuz Challenges: {obj_id}")
    if filter_index:
        print(f"Filter: howto_{filter_index} {filter_fmt or 'both'}")
    print(f"{'='*60}\n")

    stage3_dir = Path(STAGE3_DIR) / obj_id
    if not stage3_dir.exists():
        print(f"ERROR: Stage 3 output not found: {stage3_dir}")
        sys.exit(1)

    for fpath in [SKILL_FILE, SAMPLE_CHALLENGE]:
        if not Path(fpath).exists():
            print(f"ERROR: Config file not found: {fpath}")
            sys.exit(1)

    print("Loading reference files...")
    skill_content  = read_file(SKILL_FILE)
    sample_content = read_file(SAMPLE_CHALLENGE)

    raw_docs = get_stage3_howtos(obj_id, filter_index)
    if not raw_docs:
        print(f"ERROR: No how-to docs found")
        sys.exit(1)

    # Enrich docs with names and difficulties
    docs = []
    for d in raw_docs:
        raw_diff = d['difficulty']
        docs.append({
            **d,
            'name_clean':        build_name(obj_id, d['index'], 'clean'),
            'name_broken':       build_name(obj_id, d['index'], 'broken'),
            'difficulty_clean':  map_difficulty(raw_diff, 'clean'),
            'difficulty_broken': map_difficulty(raw_diff, 'broken'),
        })

    # Build work list
    work = []
    for doc in docs:
        if not filter_fmt or filter_fmt == 'clean':
            work.append((doc, 'clean'))
        if not filter_fmt or filter_fmt == 'broken':
            work.append((doc, 'broken'))

    n_total = len(work)
    print(f"Generating {n_total} challenge(s) from {len(docs)} how-to(s):")
    for doc in docs:
        print(f"  howto_{doc['index']}: {doc['path'].name}")
        if not filter_fmt or filter_fmt == 'clean':
            print(f"    → {doc['name_clean']} ({doc['difficulty_clean']})")
        if not filter_fmt or filter_fmt == 'broken':
            print(f"    → {doc['name_broken']} ({doc['difficulty_broken']})")

    client  = anthropic.Anthropic()
    results = []
    cover   = create_cover_png()

    for i, (doc, fmt) in enumerate(work, 1):
        print(f"\n[{i}/{n_total}] howto_{doc['index']}")
        result = process_challenge(client, doc, fmt, skill_content, sample_content, cover)
        results.append(result)
        if i < n_total:
            time.sleep(2)

    # ── Summary ──────────────────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print(f"Stage 5b Complete — {obj_id}")
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
        print(f"  {ok} {r['name']}{sname} [{r['difficulty']}]{issue}{warn}")

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
                print(f"  labctl content push challenge {r['actual_name']} --dir {d} --force")

    print(f"\nNext: python3 build_manifest.py {obj_id}")
    print(f"View: https://labs.iximiuz.com/challenges")


if __name__ == "__main__":
    main()
