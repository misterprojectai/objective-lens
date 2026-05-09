# Objective Lens
**ICM Layer: L0 — Routing**

Five-stage pipeline: raw source material → Diataxis documentation → GitBook publish.
Single operator command runs Stages 1–4 end to end.

---

## Operator Workflow

**To process a new exam objective:**

1. Drop source files into `01_normalize/input/<objective_id>/`
2. Drop the objective file into `_config/exam-objectives/<objective_id>.md`
3. Run: `python3 run_pipeline.py <objective_id>`

That is the complete operator interface. The pipeline handles everything through GitBook publish.

---

## Pipeline Stages

| Stage | Script | Input | Output | Model |
|---|---|---|---|---|
| 1 — Normalize | `stage1_run.py` | `01_normalize/input/<obj>/` | `01_normalize/output/<obj>/` | Haiku 4.5 Batch |
| 2 — Map | `stage2_run.py` | Stage 1 output + objective file | `02_map/output/<obj>/` | Haiku 4.5 Batch |
| 3 — Diataxis | `stage3_run.py` | Stage 2 output | `03_diataxis/output/<obj>/` | Sonnet 4.6 |
| 4 — Publish | `stage4_run.py` | Stage 3 output | `04_publish/output/<obj>/` | Sonnet 4.6 |
| 5 — iximiuz | `stage5_run.py` | Stage 3 output | `05_iximiuz/output/<obj>/` | TBD |

**Stage 5 is not yet built.** Stages 1–4 are production-ready.

---

## Routing Table

| Task | Location | Notes |
|---|---|---|
| Run full pipeline | `run_pipeline.py` | Single command: `python3 run_pipeline.py x200_103` |
| Add source files | `01_normalize/input/<objective_id>/` | PDF, SRT, MD, TXT, HTML, DOCX |
| Add exam objective | `_config/exam-objectives/<objective_id>.md` | Required before pipeline run |
| Review Diataxis output | `03_diataxis/output/<objective_id>/` | Stage 3 produces 14 documents per objective |
| Review GitBook output | `04_publish/output/<objective_id>/` | Stage 4 produces GitBook-formatted markdown |
| Check Diataxis rules | `_config/diataxis-rules.md` | Compass, contamination, quadrant laws |
| Check quality gates | `_config/quality-checks.md` | Used by Stage 3 verify |
| GitBook block reference | `_config/gitbook-blocks.md` | Loaded by Stage 4 at runtime |
| GitBook skill | `_config/gitbook-skill.md` | Loaded by Stage 4 at runtime |
| Document templates | `_templates/` | explanation, tutorial, how-to, reference |

---

## Directory Structure

```
01_normalize/
  input/<objective_id>/       ← operator drops sources here
  output/<objective_id>/      ← *_clean.md files (one per source)

02_map/
  output/<objective_id>/      ← *_mapped-passages.md (one per objective)

03_diataxis/
  output/<objective_id>/      ← *_explanation.md, *_tutorial_NN.md,
                                  *_howto_NN.md, *_reference.md

04_publish/
  output/
    SUMMARY.md                ← GitBook navigation (auto-updated by Stage 4)
    README.md                 ← GitBook homepage
    <objective_id>/           ← explanation.md, tutorial_NN.md,
                                  howto_NN.md, reference.md

05_iximiuz/
  output/<objective_id>/      ← not yet built

_config/
  exam-objectives/            ← one .md file per objective
  diataxis-rules.md
  quality-checks.md
  gitbook-blocks.md           ← required by Stage 4
  gitbook-skill.md            ← required by Stage 4

_templates/                   ← Diataxis document templates (read-only)
```

---

## Platform Separation (HARD)

| Platform | Source | Format |
|---|---|---|
| GitBook | Stage 4 output (`04_publish/`) | Liquid blocks: `{% stepper %}`, `{% hint %}`, etc. |
| iximiuz Labs | Stage 3 output (`03_diataxis/`) | MDC components: `::simple-task`, etc. |

**Stage 5 reads Stage 3 output directly — never Stage 4 output.**
GitBook is the source of truth for published content. iximiuz derives from Diataxis, not from GitBook.

---

## Verify Scripts

Each stage has a standalone verify script that can be run independently:

```bash
python3 stage1_verify.py 01_normalize/output/x200_103/
python3 stage2_verify.py 02_map/output/x200_103/x200_103_mapped-passages.md
python3 stage3_verify.py 03_diataxis/output/x200_103/x200_103
python3 stage4_verify.py 04_publish/output/x200_103
```

All return exit code 0 on pass, 1 on failure.

---

## Edge Cases

| Situation | Action |
|---|---|
| Source file unreadable | Remove from input dir. Stage 1 logs and skips. |
| Zero passages from Stage 2 | Wrong objective file or insufficient sources. Add more sources. |
| Stage 3 rate limit | Retry logic built in (3 attempts, 30s/60s backoff). |
| Stage 4 fence failures | `fix_fence_issues()` runs automatically post-generation. Check verify output. |
| GitBook write-back clobbers SUMMARY.md | Run `git pull --rebase origin main` then restore from git history. |
| Stage 4 verify fails after push | Fix failing files, run `stage4_verify.py`, commit and push manually. |

---

## Rules

1. Stages run sequentially. Output of stage N is input for stage N+1.
2. `_config/` and `_templates/` are reference only — never write working artifacts there.
3. GitBook is source of truth. Never edit published content through the GitBook UI when Git Sync is active — all changes go through Git on this machine.
4. Never delete pages through the GitBook UI. Use git to remove files and push.
5. Stage 4 (`04_publish/`) is GitBook liquid blocks only. Stage 5 (`05_iximiuz/`) is iximiuz MDC only. Never mix.

---

## Naming Conventions

**Stage 3 output:** `<objective_id>_<type>[_NN].md`
Examples: `x200_103_explanation.md`, `x200_103_tutorial_01.md`, `x200_103_howto_03.md`

**Stage 4 output:** `<type>[_NN].md` inside `04_publish/output/<objective_id>/`
Examples: `explanation.md`, `tutorial_01.md`, `howto_03.md`, `reference.md`

**Objective IDs:** `x200_NNN` — cert prefix + three-digit objective number.
