# Stage 5 — iximiuz Labs
**ICM Layer: L2 (Stage Contract)**

Generate and deploy interactive labs to iximiuz Labs from Stage 3 Diataxis documents. Stage 5 runs three scripts in sequence: `stage5_run.py` (tutorials), `stage5b_run.py` (challenges), and `build_manifest.py` (server name capture). All content deploys as private drafts. Manual publish is the final human gate.

**Dependency:** Stage 5 output feeds Stage 4 Pass B. Do not run `stage4b_run.py` until `build_manifest.py` has completed successfully for the objective.

---

## Inputs

### stage5_run.py — Tutorial Generator

- `03_diataxis/output/<obj>/<obj>_tutorial_*.md` — SOURCE (L4): Stage 3 tutorial documents. One iximiuz tutorial generated per file.
- `03_diataxis/output/<obj>/<obj>_howto_*.md` — SOURCE (L4): Stage 3 how-to documents. One iximiuz tutorial generated per file (how-tos become guided tutorials on iximiuz, not just reference pages).
- `_config/iximiuz-ref/iximiuz-CLAUDE.md` — REFERENCE (L3): Platform reference — task engine mechanics, labctl workflow, content structure rules, examiner daemon behavior.
- `_config/iximiuz-ref/iximiuz-sample-tutorial.md` — REFERENCE (L3): Canonical format sample. First 6000 characters used — covers all frontmatter fields and MDC component patterns.

### stage5b_run.py — Challenge Generator

- `03_diataxis/output/<obj>/<obj>_howto_*.md` — SOURCE (L4): Stage 3 how-to documents only. Each how-to produces two challenges: Format 1 (clean slate) and Format 2 (broken environment).
- `_config/iximiuz-ref/iximiuz-CLAUDE.md` — REFERENCE (L3): Platform reference.
- `_config/iximiuz-ref/iximiuz-sample-challenge.md` — REFERENCE (L3): Challenge format sample — `::simple-task`, `::user-input-task`, `::hint-box`, `hintcheck`, `failcheck` patterns.

### build_manifest.py — Server Name Capture

- `labctl content list --kind tutorial` — SOURCE: Live platform query. Returns all deployed tutorial names including hex suffixes.
- `labctl content list --kind challenge` — SOURCE: Live platform query. Returns all deployed challenge names.

---

## Process

### Step 1 — Generate tutorials (stage5_run.py)

```bash
python3 stage5_run.py <obj>              # all 12 tutorials
python3 stage5_run.py <obj> tutorial 1  # single doc
python3 stage5_run.py <obj> howto 3     # single doc
```

The script generates, validates, creates on server, and pushes in one run. Review the summary output — every line marked `⚠️` requires action before proceeding.

**Validation gates (script enforces these — failures block push):**
- `kind: tutorial` — no other value accepted
- `machine: rocky-01` — every task, no exceptions
- `cover: __static__/cover.png` — exact string
- `tagz`: max 5, no category names (`linux`, `containers`, etc.), no `ex200`
- `init_history_flush` task with PROMPT_COMMAND pattern — must be first task
- Every `verify_*` task paired with `::simple-task` in body
- No code fences inside YAML frontmatter
- No GitBook Liquid syntax

**When validation errors occur:** Do not manually edit generated files — regenerate the specific document:
```bash
python3 stage5_run.py <obj> tutorial 3  # regenerate tutorial_03 only
```

### Step 2 — Generate challenges (stage5b_run.py)

```bash
python3 stage5b_run.py <obj>           # all 12 challenges
python3 stage5b_run.py <obj> 4 clean   # howto_04 clean slate only
python3 stage5b_run.py <obj> 4 broken  # howto_04 broken environment only
```

**Challenge formats:**
- **Format 1 (clean slate):** Fresh Rocky Linux 9 system. Learner performs a task from scratch. Verification checks final system state — not history.
- **Format 2 (broken environment):** Init tasks create a specific misconfiguration. Learner diagnoses and fixes. Verification checks the fix is in place.

**Additional validation gates for challenges:**
- `difficulty: easy|medium|hard` — required, no other values
- Format 2 must have at least one `init: true` task to create the broken state
- `run:` blocks: no heredocs, no bare `EOF` markers, no unquoted YAML metacharacters
- Persistence verification: always `grep -E '^(export )?VAR=' /home/laborant/.bashrc | tail -1` — never `source ~/.bashrc` in non-interactive subshells (Rocky Linux non-interactive guard blocks it)
- `solution.md` must contain actual solution content — not the fallback placeholder

**When YAML parse failures occur** (special chars in shell scripts breaking frontmatter):
```bash
# Delete the broken server entry
labctl content remove challenge <actual-name-with-hex>
# Regenerate
python3 stage5b_run.py <obj> 6 broken
```

### Step 3 — Build manifest (build_manifest.py)

```bash
python3 build_manifest.py <obj>           # standard
python3 build_manifest.py <obj> --verbose # print full JSON
```

Verify manifest output counts match expected deployment:
- `tutorials: 6` — six tutorial items
- `howtos: 6` — six how-to items
- `challenges: 6` — six clean slate challenges
- `challenges_broken: 6` — six broken environment challenges

If any count is wrong, the corresponding script failed or a server entry has an unexpected name. Re-run the affected script, then re-run `build_manifest.py`.

### Step 4 — Review deployed content on iximiuz

Before marking Stage 5 complete, verify at least one tutorial and one challenge in the iximiuz Author Dashboard:

- Open the tutorial in draft mode — confirm playground boots, `::remark-box` appears at top prompting new terminal tab
- Open the challenge — confirm task counter shows, hint boxes render, difficulty badge is correct
- Start the tutorial — verify at least one `::simple-task` passes when the corresponding command is run in a new terminal tab
- Start the challenge — verify verification task passes when the correct solution is applied

**Do not publish from draft until review passes.** Every content item starts as private draft — this is the human quality gate. Publishing is manual and per-item from the iximiuz Author Dashboard.

### Step 5 — Publish content (manual, per-item)

In the iximiuz Author Dashboard at `https://labs.iximiuz.com/author`:

1. Open each draft tutorial or challenge
2. Go to access settings (three-dot menu or settings gear)
3. Set `canRead` to `["anyone"]` to make it publicly accessible via direct link
4. Platform catalog listing requires iximiuz team approval — setting `canList: ["anyone"]` signals intent but does not guarantee listing

**Publish order:** tutorials first, then challenges. Learners follow tutorials before attempting challenges.

---

## Output

- **Format:** iximiuz-flavored markdown with YAML frontmatter and MDC components
- **Write to:** `05_iximiuz/output/<content-name>/`
- **Content naming convention:**
  ```
  rhcsa-x200101-tutorial-1   through  rhcsa-x200101-tutorial-6
  rhcsa-x200101-howto-1      through  rhcsa-x200101-howto-6
  rhcsa-x200101-challenge-1  through  rhcsa-x200101-challenge-6
  rhcsa-x200101-challenge-broken-1  through  -broken-6
  ```
- **Per-content directory structure:**
  ```
  <content-name>/
    index.md           ← generated content + YAML frontmatter
    solution.md        ← challenges only — full diagnosis + fix walkthrough
    __static__/
      cover.png        ← 1×1 white PNG placeholder
  ```
- **Manifest:**
  ```
  05_iximiuz/output/<obj>-manifest.json
  ```
- **Must include in every tutorial:**
  - `kind: tutorial`, `cover: __static__/cover.png`, `playground: rockylinux / rocky-01`
  - `init_history_flush` as first task with PROMPT_COMMAND pattern
  - New terminal tab `::remark-box` as first element in body
  - Every `verify_*` task paired with `::simple-task` in body
  - `::hint-box` for every predictable failure point
- **Must include in every challenge:**
  - `kind: challenge`, `difficulty`, `cover: __static__/cover.png`, `playground: rockylinux / rocky-01`
  - Format 2: at least one `init: true` task creating the broken state
  - `solution.md` with actual content: what was broken, how to diagnose, how to fix, how to verify
  - Every `verify_*` task paired with `::simple-task` in body
- **Must NOT include in any content:**
  - GitBook Liquid syntax (`{% stepper %}`, `{% hint %}`, `{% tabs %}`, `{%`, `%}`)
  - Heredocs in `run:` blocks — use `echo`/`printf`
  - `source ~/.bashrc` in non-interactive subshell contexts
  - Code fences (` ``` `) inside YAML frontmatter
  - Category names in `tagz` (`linux`, `containers`, `kubernetes`, etc.)
  - `ex200` in `tagz`
  - More than 5 tags
  - Guided steps or solution hints in the challenge body — those go in `solution.md` and `::hint-box`

---

## Done Looks Like

`build_manifest.py` reports all four content sections at exactly the expected count (6+6+6+6 = 24 for a full objective), no `⚠️` errors in any script output, at least one tutorial and one challenge have been started in the iximiuz playground with tasks verified as passing, and all 24 items are deployed as drafts in the Author Dashboard ready for manual publish.

---

## Common Failure Modes

**Failure 1 — YAML parse failure from special characters in `run:` blocks.**
What goes wrong: Generated shell script in frontmatter contains `[`, `]`, `*`, heredoc `EOF`, or bare `'` characters that break YAML parsing. Script reports YAML parse failure and push is rejected by platform.
How to detect: Script summary shows `⚠️` with "YAML parse failure" error. labctl push error: "Unexpected front matter attribute."
How to fix: Delete the server entry with `labctl content remove <kind> <actual-name>`. Regenerate the specific document — the no-heredoc and YAML safety constraints in the system prompt prevent this on retry.

**Failure 2 — Broken environment challenge: persistence verification always fails.**
What goes wrong: Verification script uses `bash --norc -c 'source ~/.bashrc; echo $VAR'` to check persistence. Rocky Linux `.bashrc` has a non-interactive guard (`case $-`) that exits immediately in non-interactive shells, so `$VAR` is always empty and verification always fails even after a correct fix.
How to detect: Learner applies the correct fix and variable is set in their interactive shell, but the task counter never advances to pass.
How to fix: Replace the subshell sourcing pattern with direct file grep: `LAST=$(grep -E '^(export )?VAR=' /home/laborant/.bashrc | tail -1 | cut -d= -f2- | tr -d "'\"")`. Edit `05_iximiuz/output/<name>/index.md` to fix the `run:` block, then push: `labctl content push challenge <actual-name> --dir <dir> --force`.

**Failure 3 — Hash-match causes silent push skip.**
What goes wrong: `labctl content push` silently skips files whose content hash matches what is already on the server — local edits are not deployed.
How to detect: Push completes without error but changes are not visible on the platform.
How to fix: Always use `--force` flag on all pushes: `labctl content push <kind> <name> --dir <dir> --force`.

**Failure 4 — Manifest counts do not match deployment.**
What goes wrong: `build_manifest.py` reports fewer than expected items because some content failed to deploy, was deleted, or has an unexpected name pattern.
How to detect: `build_manifest.py` output shows a count below 6 for any section, or reports asymmetry warnings.
How to fix: Check `labctl content list --kind tutorial` and `--kind challenge` for missing entries. Re-run the affected script for the missing indices. Then re-run `build_manifest.py`.

**Failure 5 — labctl not authenticated.**
What goes wrong: All `labctl` commands fail with authentication error.
How to detect: Any labctl command returns "unauthorized" or similar auth error.
How to fix: `labctl auth login` — authenticates via browser. Verify with `labctl auth whoami`. Required before any Stage 5 run.

**Failure 6 — Verification task passes in operator terminal but not in task engine.**
What goes wrong: Operator runs the task's `run:` script manually and it exits 0, but the iximiuz task engine never marks the task as complete.
How to detect: Manual execution succeeds but task counter stays at 0/N in the UI after 30 seconds.
How to fix: The task engine runs as `user: laborant` on `machine: rocky-01`. Ensure the task's `machine:` and `user:` fields match. Confirm the action was performed in a new terminal tab (Term 2+), not the original tab opened before `init_history_flush` completed. Use the Tasks Dev Tools panel (bottom-right of playground) to see actual task output from the engine.
