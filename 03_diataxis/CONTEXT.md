# Stage 3 — Diataxis Transformation
**ICM Layer: L2 (Stage Contract)**

Transform objective-mapped content passages into four pure Diataxis documents. Explanation is the anchor. All other quadrants derive from it.

---

## Inputs

- `02_map/output/[objective-slug]_mapped-passages.md` — SOURCE (L4): collated passages extracted and filtered against the selected RHCSA objective. This is raw signal. Transform it.
- `_config/diataxis-rules.md` — REFERENCE (L3): the complete Diataxis rule set. Load and apply. Do not deviate.
- `_templates/explanation.md` — REFERENCE (L3): structural template for Explanation output.
- `_templates/tutorial.md` — REFERENCE (L3): structural template for Tutorial output.
- `_templates/how-to.md` — REFERENCE (L3): structural template for How-to output.
- `_templates/reference.md` — REFERENCE (L3): structural template for Reference output.

**Do not load all inputs at once.** Work sequentially. Load templates as needed per document.

---

## Process

### Step 1: Classify All Passages Before Writing Anything

Read the full `_mapped-passages.md` file. Before generating a single word of output, run the compass on every passage.

For each passage, apply in order:
1. Is this content practical (doing) or theoretical (understanding)?
2. Is this content for study (acquiring skill) or work (applying skill)?

Assign each passage to exactly one quadrant: Tutorial, How-to, Reference, or Explanation.

**Document the classification.** Write a classification header in your working notes (not in the output file) listing which passages map to which quadrant. If a passage clearly belongs to two quadrants, split it — extract the theoretical portion to Explanation, the procedural portion to How-to or Tutorial.

---

### Step 2: Write the Explanation First

Load `_templates/explanation.md`. Apply `_config/diataxis-rules.md` → Explanation rules.

The Explanation document is the conceptual anchor for this objective. Write it completely before touching any other quadrant.

**What to include:** All theoretical passages classified in Step 1. The "why" of the objective. Historical or architectural context. Design decisions and trade-offs. Mental models. Common misconceptions.

**What to exclude:** Any step-by-step content. Any command-as-primary-content. Any flag tables. Any "how do I do this" language.

**Test before proceeding:** Does this pass the "read in bath" test? Can it be read away from a terminal? If not, procedures have leaked in. Extract and route them.

---

### Step 3: Write the Tutorial

Load `_templates/tutorial.md`. Apply `_config/diataxis-rules.md` → Tutorial rules.

Derive the Tutorial from the completed Explanation. Ask: what can be taught through guided doing that builds understanding of this concept?

**One path only.** Choose the most common, most instructive, most exam-relevant path. Every step must produce a visible result. Every step must have an explicit "You should see:" block.

**What to include:** All practical-study passages from Step 1. The primary use case for this objective executed step by step.

**What to exclude:** Explanation of why commands work (link to Explanation instead). Alternative approaches. Complete flag listings.

---

### Step 4: Write the How-to

Load `_templates/how-to.md`. Apply `_config/diataxis-rules.md` → How-to rules.

Derive the How-to from the completed Explanation. Ask: what practical tasks does a competent operator need to perform with this concept?

Write one How-to per distinct real-world task. If the objective maps to multiple distinct tasks (e.g., "extend LVM" and "shrink LVM" are different enough to warrant separate guides), produce multiple How-to files numbered sequentially.

**What to include:** All practical-work passages from Step 1. Task-focused instructions. Conditional variants ("if you want X, do Y"). Verification step. Troubleshooting table.

**What to exclude:** Why anything works. Tutorial narrative. Complete option references.

---

### Step 5: Write the Reference

Load `_templates/reference.md`. Apply `_config/diataxis-rules.md` → Reference rules.

Derive the Reference from the completed Explanation. Ask: what machinery (commands, options, files, parameters, exit codes) does this concept operate on that needs complete factual description?

**What to include:** All theoretical-work passages from Step 1. Complete command syntax. All options and flags the exam tests. Relevant file paths. Exit codes. Brief illustrative examples.

**What to exclude:** Instructions. Guidance. Opinion. Tutorial narrative. Explanation of design decisions.

---

### Step 6: Run Contamination Check on All Four Documents

For each completed document, apply the contamination checklist from `_config/diataxis-rules.md` → "Quality Gate" section.

For any contamination found:
- **Do not delete the content.** Extract it and route it to the correct document.
- Critical contamination (step-by-step in Explanation, theory dump in Tutorial) must be resolved before this stage produces output.
- Medium/low contamination must be noted for the next review cycle.

---

## Output

**Format:** Four `.md` files per RHCSA objective run. One per Diataxis quadrant.

**Write to:** `03_diataxis/output/`

**Naming convention:**
```
[objective-slug]_explanation.md
[objective-slug]_tutorial.md
[objective-slug]_how-to.md          (or _how-to-01.md, _how-to-02.md if multiple tasks)
[objective-slug]_reference.md
```

Example for x200_101 (shell prompt):
```
x200_101_shell-prompt_explanation.md
x200_101_shell-prompt_tutorial.md
x200_101_shell-prompt_how-to.md
x200_101_shell-prompt_reference.md
```

**Must include in every file:**
- Complete frontmatter (title, type, quadrant, exam_objective, version, status)
- All template sections populated — no `[placeholder]` text remaining
- Contamination checklist completed (embedded as comments at bottom of file)
- Cross-links to all three companion documents

**Must NOT include in any file:**
- Unfilled template placeholders
- Guidance comments from the template (lines beginning with `<!-- `)
- Content from a different quadrant
- Platform-specific formatting (no `{% stepper %}`, no `::simple-task` — that is Stage 4/5 work)
- Confidence reports or self-assessment scores embedded in the content body

---

## Done Looks Like

Four `.md` files in `03_diataxis/output/` — each pure to its quadrant, each passing its contamination checklist, each cross-linked to the other three, each with complete frontmatter and no placeholder text remaining.

---

## Common Failure Modes

**Failure 1: Writing Tutorial before Explanation is complete.**
Symptom: Tutorial contains explanation paragraphs that "felt necessary." Fix: finish Explanation first, then strip those paragraphs from Tutorial and link to Explanation instead.

**Failure 2: Explanation contaminated with procedures.**
Symptom: Explanation contains numbered steps or "run this command" language. Fix: extract procedures. Route them to How-to or Tutorial. Replace with a link.

**Failure 3: How-to and Tutorial covering the same ground.**
Symptom: Tutorial and How-to have nearly identical steps. Fix: Tutorial teaches a beginner through a single complete learning path. How-to gives a competent operator direct task instructions. If they're the same, the Tutorial is probably a How-to in disguise. Reclassify with the compass.

**Failure 4: Reference contains instruction.**
Symptom: Reference has sentences like "to use this command, first..." Fix: move procedural language to How-to. Replace with neutral factual description.

**Failure 5: Passages left unclassified and omitted.**
Symptom: Mapped passages contain good signal that doesn't appear in any of the four output documents. Fix: every passage in the input must land somewhere. If it doesn't fit any quadrant, that is a classification failure — re-run the compass on that passage.
