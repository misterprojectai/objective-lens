# Objective Lens

A five-stage content pipeline that transforms raw technical source material into publication-ready Diataxis documentation — published to GitBook as source of truth and adapted to iximiuz Labs as hands-on content.

Built for RHCSA EX200. The pipeline is cert-agnostic — swap the objective filter file and run it against any certification track.

---

## The Problem This Solves

Raw study material — PDFs, transcripts, notes, blog posts — contains signal for every exam objective simultaneously. It is noisy, unstructured, and in multiple formats. None of it is publication-ready.

The Objective Lens isolates one exam objective at a time, strips the noise, maps the relevant signal, and transforms it into four Diataxis documents: Explanation (the conceptual anchor), Tutorial (guided doing), How-to (practical task execution), and Reference (complete factual description). These go to GitBook. The Tutorial and How-to are then adapted for iximiuz Labs as hands-on interactive content.

---

## Pipeline Overview

```
Raw input (PDF, .txt, .md, transcripts)
    ↓  Stage 1: Normalize
Clean .md files — signal only, noise removed
    ↓  Stage 2: Map
Raw passages relevant to selected exam objective
    ↓  Stage 3: Diataxis transformation
Four documents: Explanation → Tutorial → How-to → Reference
    ↓  Stage 4: Publish
GitHub (backend) + GitBook (frontend) — source of truth
    ↓  Stage 5: iximiuz
Tutorial → iximiuz Tutorial
How-to → iximiuz Challenge / How-to
```

---

## Folder Structure

```
objective-lens/
├── CLAUDE.md                    ← Routing (Claude Code)
├── README.md                    ← This file
├── 01_normalize/
│   ├── CONTEXT.md               ← Stage 1 contract
│   ├── input/                   ← Drop raw files here
│   └── output/                  ← Clean files land here
├── 02_map/
│   ├── CONTEXT.md               ← Stage 2 contract
│   ├── input/                   ← Populated from Stage 1 output
│   └── output/                  ← Mapped passages per objective
├── 03_diataxis/
│   ├── CONTEXT.md               ← Stage 3 contract
│   ├── input/                   ← Populated from Stage 2 output
│   └── output/                  ← Four Diataxis docs per objective
├── 04_publish/
│   ├── CONTEXT.md               ← Stage 4 contract
│   ├── input/                   ← Populated from Stage 3 output
│   └── output/                  ← Publication-ready files
├── 05_iximiuz/
│   ├── CONTEXT.md               ← Stage 5 contract
│   ├── input/                   ← Populated from Stage 4 output
│   └── output/                  ← iximiuz-formatted content
├── _config/
│   ├── diataxis-rules.md        ← Diataxis framework rules (all four quadrants)
│   ├── quality-checks.md        ← Per-document pass/fail gates for Stage 3
│   ├── exam-objectives/         ← RHCSA EX200 objective files (one per objective)
│   ├── gitbook-specs.md         ← GitBook formatting rules (Stage 4)
│   └── iximiuz-specs.md         ← iximiuz platform rules (Stage 5)
└── _templates/
    ├── explanation.md           ← Explanation output template
    ├── tutorial.md              ← Tutorial output template
    ├── how-to.md                ← How-to output template
    └── reference.md             ← Reference output template
```

---

## How to Run a Pipeline Pass

### Step 1 — Normalize

Drop source files into `01_normalize/input/`. Run Stage 1 following `01_normalize/CONTEXT.md`. Clean files land in `01_normalize/output/`.

Review output. Every file should be readable plain text with no formatting artifacts.

### Step 2 — Map

Select the exam objective file from `_config/exam-objectives/` (e.g., `_config/exam-objectives/x200_101.md`). Stage 2 reads clean files directly from `01_normalize/output/` — no copying required. Run Stage 2 following `02_map/CONTEXT.md`. Mapped passages land in `02_map/output/`.

Review output. Every passage should directly address the selected objective.

### Step 3 — Diataxis Transformation

Copy mapped passages into `03_diataxis/input/`. Run Stage 3 following `03_diataxis/CONTEXT.md`. Load templates from `_templates/` as needed. Four documents land in `03_diataxis/output/`.

**Before proceeding:** run every document through `_config/quality-checks.md`. All gates must pass. No exceptions.

### Step 4 — Publish

Copy Stage 3 output into `04_publish/input/`. Run Stage 4 following `04_publish/CONTEXT.md`. Commits to GitHub. GitBook syncs automatically.

Review live GitBook pages before proceeding to Stage 5.

### Step 5 — iximiuz Adaptation

Pull Tutorial and How-to documents from GitBook-published content. Run Stage 5 following `05_iximiuz/CONTEXT.md`. Push to iximiuz Labs via `labctl`.

Verify tasks in iximiuz playground before marking objective complete.

---

## Config Files Reference

| File | Purpose | Used in Stage |
|---|---|---|
| `diataxis-rules.md` | Compass, quadrant iron laws, contamination patterns | 3 |
| `quality-checks.md` | Pass/fail gates for all four quadrant documents | 3 |
| `exam-objectives/x200_NNN.md` | One file per RHCSA objective — filter for Stage 2 *(pending — add before Stage 2 runs)* | 2 |
| `gitbook-specs.md` | Block syntax, SUMMARY.md rules, formatting constraints | 4 |
| `iximiuz-specs.md` | Frontmatter schema, MDC components, platform constraints | 5 |

---

## Certification Track Adaptation

To run this pipeline against a different certification (RHCE, LFCS, CKA, etc.):

1. Replace contents of `_config/exam-objectives/` with the new certification's objective files
2. Update `_config/iximiuz-specs.md` if the platform environment changes (e.g., different playground OS)
3. All other pipeline stages remain identical

The Diataxis framework, GitBook publishing, and iximiuz adaptation are cert-agnostic. Only the objective filter changes.

---

*Built using Interpretable Context Methodology — each stage has one job, each file does one thing, human reviews at every handoff.*
