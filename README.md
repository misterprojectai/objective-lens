# Objective Lens

A content pipeline that transforms raw technical source material into publication-ready Diataxis documentation and hands-on interactive labs.

**Published simultaneously to:**
- **GitBook** — knowledge layer (explanation, reference, tutorials, how-tos)
- **iximiuz Labs** — hands-on layer (guided tutorials, practice challenges, broken environment challenges)

Built for RHCSA EX200. The pipeline is cert-agnostic — swap the objective filter and run it against any certification track.

---

## What One Objective Produces

Per exam objective, the pipeline generates:

| Platform | Content | Count |
|---|---|---|
| GitBook | Explanation, Reference, 6 Tutorials, 6 How-tos | 14 docs |
| iximiuz | Guided tutorials (from tutorials) | 6 |
| iximiuz | Guided tutorials (from how-tos) | 6 |
| iximiuz | Practice challenges — clean slate | 6 |
| iximiuz | Practice challenges — broken environment | 6 |
| **Total** | | **38 items** |

---

## Pipeline Architecture

```
Raw input (PDF, .txt, .md, transcripts)
    ↓
Stage 1  stage1_run.py          Normalize — extract signal, remove noise
    ↓
Stage 2  stage2_run.py          Map — isolate passages for selected objective
    ↓
Stage 3  stage3_run.py          Diataxis — transform into 4 document types
    ↓
Stage 4  stage4_run.py          Publish — write to GitBook via GitHub sync
    ↓
Stage 4b stage4b_run.py         Link — inject iximiuz embeds into GitBook pages
    ↓
Stage 5  stage5_run.py          Labs — generate iximiuz tutorials (12 per objective)
Stage 5b stage5b_run.py         Challenges — generate iximiuz challenges (12 per objective)
         build_manifest.py      Manifest — capture deployed server names
    ↓
Stage 4b stage4b_run.py         Run again — links now available, inject into GitBook
```

Stages 1–4 run sequentially via `run_pipeline.py`. Stages 5/5b/manifest/4b run separately per objective after Stage 4 completes.

---

## Scripts Reference

| Script | Purpose | Model |
|---|---|---|
| `run_pipeline.py` | Orchestrates Stages 1–4 for one objective | — |
| `stage1_run.py` | Normalizes raw source files | Haiku 4.5 Batch |
| `stage2_run.py` | Maps passages to exam objective | Haiku 4.5 Batch |
| `stage3_run.py` | Generates Diataxis documents | Sonnet 4.6 |
| `stage4_run.py` | Publishes to GitBook via GitHub | Sonnet 4.6 |
| `stage4b_run.py` | Injects iximiuz links into GitBook | No LLM |
| `stage5_run.py` | Generates iximiuz tutorials from Stage 3 docs | Sonnet 4.6 |
| `stage5b_run.py` | Generates iximiuz challenges from how-to docs | Sonnet 4.6 |
| `build_manifest.py` | Queries labctl and builds server-name manifest | No LLM |

---

## How to Run a Full Objective

### Stages 1–4 (GitBook)

```bash
# Drop sources into 01_normalize/input/<obj_id>/
# Drop objective into _config/exam-objectives/<obj_id>.md
python3 run_pipeline.py x200_101
```

Review live GitBook pages before proceeding.

### Stage 5 (iximiuz tutorials)

```bash
python3 stage5_run.py x200_101          # all 12 tutorials
python3 stage5_run.py x200_101 tutorial 1  # single doc
python3 stage5_run.py x200_101 howto 3    # single doc
```

All content deploys as **private draft** on iximiuz. Manually publish from the Author Dashboard when ready.

### Stage 5b (iximiuz challenges)

```bash
python3 stage5b_run.py x200_101          # all 12 challenges
python3 stage5b_run.py x200_101 4 clean  # howto_04 clean slate only
python3 stage5b_run.py x200_101 4 broken # howto_04 broken environment only
```

### Build manifest

```bash
python3 build_manifest.py x200_101           # standard
python3 build_manifest.py x200_101 --verbose # print full JSON
```

### Stage 4b (GitBook↔iximiuz links)

```bash
python3 stage4b_run.py x200_101
```

Updates GitBook automatically:
- `explanation.md` — full hub with all 24 iximiuz items in 3 sections
- `tutorial_NN.md` — "Practice This Lab" embed at bottom of each page
- `howto_NN.md` — "Test Yourself" challenge embed + Advanced broken link
- `practice-labs.md` — new dedicated hub page (added to SUMMARY.md)

---

## Folder Structure

```
objective-lens/
├── CLAUDE.md                       ← Claude Code routing
├── README.md                       ← This file
├── run_pipeline.py                 ← Stages 1–4 orchestrator
├── stage1_run.py / stage1_verify.py
├── stage2_run.py / stage2_verify.py
├── stage3_run.py / stage3_verify.py
├── stage4_run.py / stage4_verify.py
├── stage4b_run.py                  ← GitBook iximiuz link injection
├── stage5_run.py                   ← iximiuz tutorial generator
├── stage5b_run.py                  ← iximiuz challenge generator
├── build_manifest.py               ← Manifest builder from deployed content
│
├── 01_normalize/
│   ├── CONTEXT.md
│   ├── input/                      ← Drop raw source files here
│   └── output/                     ← Clean normalized .md files
├── 02_map/
│   ├── CONTEXT.md
│   └── output/                     ← Objective-mapped passages
├── 03_diataxis/
│   ├── CONTEXT.md
│   └── output/                     ← Explanation, Tutorial×N, How-to×N, Reference
├── 04_publish/
│   ├── CONTEXT.md
│   └── output/                     ← GitBook-ready files (git-synced)
├── 05_iximiuz/
│   ├── CONTEXT.md
│   └── output/                     ← iximiuz content dirs + manifest JSON
│
└── _config/
    ├── diataxis-rules.md           ← Diataxis framework rules (Stage 3)
    ├── quality-checks.md           ← Pass/fail gates (Stage 3)
    ├── exam-objectives/            ← One .md file per RHCSA objective
    ├── gitbook-blocks.md           ← GitBook block syntax reference (Stage 4)
    ├── gitbook-skill.md            ← GitBook authoring skill (Stage 4)
    └── iximiuz-ref/                ← iximiuz platform reference docs (Stage 5)
        ├── iximiuz-CLAUDE.md
        ├── iximiuz-sample-tutorial.md
        ├── iximiuz-sample-challenge.md
        ├── iximiuz-challenge-authoring.md
        └── labctl-skill-*.md (15 files)
```

---

## iximiuz Platform Notes

**Playground:** Rocky Linux 9 (`rockylinux`), machine `rocky-01`, default user `laborant`

**Content types used:**
- `kind: tutorial` — tutorials and how-tos (both deploy as tutorials on iximiuz)
- `kind: challenge` — clean slate and broken environment challenges

**Deployment:**
- `labctl content create <kind> <name> --dir <dir>` before first push
- `labctl content push <kind> <actual-name> --dir <dir> --force`
- iximiuz appends an 8-char hex suffix to names on create — `build_manifest.py` captures these

**Hard constraints (non-negotiable):**
- `tagz`: max 5, no category names (`linux`, `kubernetes`, etc.), no `ex200`
- `cover`: must be `__static__/cover.png`
- No heredocs in YAML `run:` blocks — use `echo`/`printf`
- No `source ~/.bashrc` in non-interactive subshells on Rocky Linux (non-interactive guard)
- Persistence checks: `grep -E '^(export )?VAR=' ~/.bashrc | tail -1`

---

## Objective Status

| Objective | GitBook | iximiuz | Links |
|---|---|---|---|
| x200_101 Shell Prompt | ✅ 14 docs | ✅ 24 items | ✅ injected |
| x200_102 I/O Redirection | ✅ 14 docs | 🔲 | 🔲 |
| x200_103 grep and Regex | ✅ 11 docs | 🔲 | 🔲 |

---

## Certification Track Adaptation

To run against a different certification (RHCE, LFCS, CKA, etc.):

1. Replace `_config/exam-objectives/` with the new cert's objective files
2. Update the iximiuz playground name in `stage5_run.py` if a different OS is needed
3. All other pipeline stages are cert-agnostic

---

*Built using Interpretable Context Methodology (ICM) — each stage has one job, each script does one thing, human reviews gate every platform push.*
