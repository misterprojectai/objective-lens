# Objective Lens
**ICM Layer: L0 — Routing**

Five-stage pipeline: raw technical content → Diataxis documentation → GitBook + iximiuz Labs.

---

## Routing Table

| Task | Go to | Read | Notes |
|---|---|---|---|
| Drop raw source files | `01_normalize/input/` | `01_normalize/CONTEXT.md` | PDFs, .txt, .md, transcripts |
| Select exam objective | `_config/exam-objectives/` | — | Choose objective file (e.g. x200_101.md) |
| Run objective mapping | `02_map/` | `02_map/CONTEXT.md` | One objective per run |
| Transform to Diataxis | `03_diataxis/` | `03_diataxis/CONTEXT.md` | Load templates as needed |
| Publish to GitBook | `04_publish/` | `04_publish/CONTEXT.md` | After Stage 3 gate passes |
| Adapt for iximiuz | `05_iximiuz/` | `05_iximiuz/CONTEXT.md` | After Stage 4 published |
| Check Diataxis rules | `_config/diataxis-rules.md` | — | Compass, contamination, quadrant laws |
| Run quality gate | `_config/quality-checks.md` | — | Before any file leaves Stage 3 |
| Use output templates | `_templates/` | — | explanation, tutorial, how-to, reference |

---

## Edge Cases

| Situation | Action |
|---|---|
| Source file unreadable | Remove from `input/`. Log and skip. Do not process. |
| Zero passages from mapping | Broaden keyword list. Do not force passages that don't match. |
| Diataxis contamination found | Extract to correct document. Never delete. Re-run gate. |
| Stage needs re-run | Clear that stage's `output/`. Re-run from updated input. |

---

## Rules

1. Stages run sequentially. Output of stage N is input for stage N+1.
2. Human reviews each stage boundary. Exception: Stage 2 is fully automated — spot-check recommended.
3. `_config/` and `_templates/` are reference only — never write working artifacts there.
4. No file leaves Stage 3 without passing `_config/quality-checks.md` in full.
5. Stage 4 (GitBook) is source of truth. Stage 5 (iximiuz) derives from it — never the reverse.

---

## Naming Convention

`[objective-slug]_[type].md` — e.g. `x200_101_shell-prompt_explanation.md`

Full pattern and examples in README.md.
