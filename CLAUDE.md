# Objective Lens
**ICM Layer: L0 — Routing**

A five-stage content pipeline that transforms raw technical source material into publication-ready Diataxis documentation. Built for RHCSA — adaptable to any certification track.

---

## Structure

```
objective-lens/
├── 01_normalize/     ← Stage 1: Raw input → clean .md (signal only)
├── 02_map/           ← Stage 2: Clean files → passages mapped to exam objective
├── 03_diataxis/      ← Stage 3: Mapped passages → four Diataxis documents
├── 04_publish/       ← Stage 4: Diataxis docs → GitHub + GitBook (source of truth)
├── 05_iximiuz/       ← Stage 5: GitBook content → iximiuz Labs adaptation
├── _config/          ← L3: Rules, specs, quality gates (reference only)
└── _templates/       ← L3: Output structure templates (reference only)
```

---

## Routing Table

| Task | Go to | Read | Notes |
|---|---|---|---|
| Drop raw source files | `01_normalize/input/` | `01_normalize/CONTEXT.md` | PDFs, .txt, .md, transcripts |
| Select exam objective | `_config/exam-objectives/` | — | Choose objective file (e.g. x200_101.md), then run Stage 2 |
| Run objective mapping | `02_map/` | `02_map/CONTEXT.md` | One objective per run |
| Transform to Diataxis | `03_diataxis/` | `03_diataxis/CONTEXT.md` | Load templates as needed |
| Publish to GitBook | `04_publish/` | `04_publish/CONTEXT.md` | After Stage 3 gate passes |
| Adapt for iximiuz | `05_iximiuz/` | `05_iximiuz/CONTEXT.md` | After Stage 4 published |
| Check Diataxis rules | `_config/diataxis-rules.md` | — | Compass, contamination, quadrant laws |
| Run quality gate | `_config/quality-checks.md` | — | Before any file leaves Stage 3 |
| Use output templates | `_templates/` | — | explanation, tutorial, how-to, reference |

---

## Edge Case Routing

| Situation | Action |
|---|---|
| Source file unreadable / corrupt | Remove from `01_normalize/input/`. Log in `01_normalize/CONTEXT.md` notes. Do not process. |
| Objective mapping returns zero passages | Check objective filter file. Broaden search terms. Do not force passages that don't match. |
| Diataxis contamination found on review | Extract to correct document. Never delete. Re-run quality gate. |
| Single stage needs re-run on updated input | Clear that stage's `output/` directory. Re-run stage contract only. Downstream stages re-run from updated output. |

---

## Rules

1. Stages run sequentially. Output of stage N is input for stage N+1.
2. Human reviews output at each stage boundary before the next stage runs. Exception: Stage 2 is fully automated (ripgrep + Haiku Batch) — human spot-check of Stage 2 output is recommended but not a hard gate.
3. `_config/` and `_templates/` are reference only — never write working artifacts there.
4. No file leaves Stage 3 without passing `_config/quality-checks.md` in full.
5. Stage 4 (GitBook) is the source of truth. Stage 5 (iximiuz) derives from it — never the reverse.

---

## Naming Convention

```
Stage 1 output:  [source-slug]_clean.md
Stage 2 output:  [objective-slug]_mapped-passages.md
Stage 3 output:  [objective-slug]_explanation.md
                 [objective-slug]_tutorial.md
                 [objective-slug]_how-to.md  (or _how-to-01.md, _how-to-02.md)
                 [objective-slug]_reference.md
```

Example for x200_101 (shell prompt):
```
x200_101_shell-prompt_clean.md
x200_101_shell-prompt_mapped-passages.md
x200_101_shell-prompt_explanation.md
x200_101_shell-prompt_tutorial.md
x200_101_shell-prompt_how-to.md
x200_101_shell-prompt_reference.md
```
