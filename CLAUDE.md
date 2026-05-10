# Objective Lens
**ICM Layer: L0 — Routing**

Five-stage pipeline: raw source material → Diataxis documentation → GitBook publish → iximiuz Labs.
Single operator command runs Stages 1–4. Stage 5 runs separately per objective after Stage 4 completes.

---

## Routing Table

| Task | Script / Location | Notes |
|---|---|---|
| Run Stages 1–4 | `run_pipeline.py <obj>` | Full pipeline: normalize → map → diataxis → publish |
| Run Stage 5 (tutorials) | `stage5_run.py <obj>` | iximiuz tutorials from Stage 3 output |
| Run Stage 5b (challenges) | `stage5b_run.py <obj>` | iximiuz challenges from Stage 3 how-tos |
| Build iximiuz manifest | `build_manifest.py <obj>` | Capture deployed server names after Stage 5/5b |
| Inject GitBook links | `stage4b_run.py <obj>` | Run after build_manifest — links GitBook ↔ iximiuz |
| Add source files | `01_normalize/input/<obj>/` | PDF, SRT, MD, TXT, HTML, DOCX |
| Add exam objective | `_config/exam-objectives/<obj>.md` | Required before pipeline run |
| Stage 1 contract | `01_normalize/CONTEXT.md` | Normalize — inputs, process, output, failure modes |
| Stage 2 contract | `02_map/CONTEXT.md` | Map — inputs, process, output, failure modes |
| Stage 3 contract | `03_diataxis/CONTEXT.md` | Diataxis — inputs, process, output, failure modes |
| Stage 4 contract | `04_publish/CONTEXT.md` | Publish + link injection — both passes documented |
| Stage 5 contract | `05_iximiuz/CONTEXT.md` | iximiuz tutorials, challenges, manifest |
| Diataxis rules | `_config/diataxis-rules.md` | Compass, quadrant laws, contamination patterns |
| Quality gates | `_config/quality-checks.md` | Pass/fail criteria for Stage 3 output |
| GitBook block syntax | `_config/gitbook-blocks.md` | Liquid block reference for Stage 4 |
| GitBook authoring skill | `_config/gitbook-skill.md` | Conventions, SUMMARY.md rules |
| iximiuz platform reference | `_config/iximiuz-ref/` | Task engine, labctl workflow, platform constraints |

---

## Stage 5 Run Order (per objective)

```
python3 stage5_run.py <obj>       # deploy 12 tutorials
python3 stage5b_run.py <obj>      # deploy 12 challenges
python3 build_manifest.py <obj>   # capture server names
python3 stage4b_run.py <obj>      # inject links into GitBook
```

---

## Naming Conventions

**Objective IDs:** `x200_NNN` — cert prefix + three-digit number.

**Stage 3 output:** `<obj>_<type>[_NN].md`
Examples: `x200_101_explanation.md`, `x200_101_tutorial_01.md`, `x200_101_howto_03.md`

**Stage 4 output:** `<type>[_NN].md` inside `04_publish/output/<obj>/`
Examples: `explanation.md`, `tutorial_01.md`, `howto_03.md`, `reference.md`

**Stage 5 output:** `rhcsa-{slug}-{type}-{N}` inside `05_iximiuz/output/`
Examples: `rhcsa-x200101-tutorial-1`, `rhcsa-x200101-challenge-broken-4`
iximiuz appends an 8-char hex suffix on create: `rhcsa-x200101-tutorial-1-75b72671`

---

## Rules

1. Stages run sequentially. Output of stage N feeds stage N+1.
2. `_config/` is reference only — never write working artifacts there.
3. GitBook is source of truth. All changes go through git push — never edit through the GitBook UI.
4. Stage 4 output uses GitBook Liquid blocks only. Stage 5 output uses iximiuz MDC only. Never mix.
5. Stage 5 content deploys as private draft. Manual publish from iximiuz Author Dashboard is the final gate.
