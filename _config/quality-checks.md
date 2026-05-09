# Quality Checks — Diataxis Layer
**ICM Layer: L3 — Reference (do not transform)**
**Used by:** Stage 3 verify (`stage3_verify.py`) before any file moves to Stage 4

---

## How to Use This File

Run these checks on every document produced in Stage 3 before it leaves
`03_diataxis/output/`. Each check is binary: Pass or Fail. No partial credit.
A single Fail blocks the document from Stage 4.

If a check fails: fix the document, re-run all checks for that quadrant, then proceed.

---

## Pipeline Conventions

**Source attribution comments:** `<!-- Source: [filepath] -->` comments are STRIPPED
by Stage 3 during output writing (`strip_source_comments()` in `stage3_run.py`).
They do NOT appear in final Stage 3 output files. The "no source comments leaked"
checks in `stage3_verify.py` verify this stripping worked correctly.

**Platform formatting:** `{% stepper %}`, `{% hint %}`, `::simple-task` and all other
platform-specific blocks must NOT appear in Stage 3 output. Stage 3 produces
pure Diataxis markdown. Platform formatting is applied in Stage 4 (GitBook) and
Stage 5 (iximiuz) from the Stage 3 source — never in Stage 3 itself.

**Frontmatter:** All Stage 3 documents use bare `---` delimiters for YAML frontmatter.
Required fields: `title`, `type`, `exam_objective`, `version`, `status: draft`.

---

## Explanation Quality Gate

**File:** `<objective_id>_explanation.md`

### Diataxis Purity

| Check | Pass Criteria |
|---|---|
| Compass confirmed | Cognition (theoretical) + Acquisition (study) → Explanation |
| Title passes "About X" test | "About [title]" reads naturally |
| "Read in bath" test | Readable without a terminal — no commands required to follow |
| Zero procedures | No numbered steps, no "run this command to..." as primary content |
| Zero reference tables | No parameters, flags, or option tables as primary content |
| Perspective present | Trade-offs and alternatives discussed with judgment |
| Analogies used | At least one analogy bridges abstract concept to concrete understanding |

### Structure Completeness

| Section | Required |
|---|---|
| Opening paragraph (conceptual question established) | Yes |
| Background / historical context | Yes |
| How [Topic] Works (conceptual model) | Yes |
| Why This Design (rationale + trade-offs) | Yes |
| Common Misconceptions | Yes |
| Relationship to Other Objectives | Yes |
| Further Reading (links to Tutorial, How-to, Reference) | Yes |

### Frontmatter

| Field | Required value |
|---|---|
| `type` | `explanation` |
| `exam_objective` | matching objective ID |
| `status` | `draft` |

**EXPLANATION GATE: All checks Pass → proceed to Stage 4**

---

## Tutorial Quality Gate

**File:** `<objective_id>_tutorial_NN.md`

### Diataxis Purity

| Check | Pass Criteria |
|---|---|
| Compass confirmed | Action (practical) + Acquisition (study) → Tutorial |
| Single path only | Zero alternatives, zero "you could also" |
| Zero explanation paragraphs | No "the reason this works is..." content |
| Zero reference tables | No parameter tables or complete flag listings |
| "We" language throughout | Tutor and learner working together |
| Every step has expected output | "You should see:" present for every step |
| Iron Law held | Every step produces a visible, meaningful result |

### Structure Completeness

| Section | Required |
|---|---|
| Action-oriented title | Yes |
| Prerequisites (minimal, absolute only) | Yes |
| What We'll Build (end state shown before step 1) | Yes |
| Numbered steps with commands | Yes |
| Each step has "You should see:" block | Yes |
| What We Accomplished (past tense) | Yes |
| Next Steps (links outward) | Yes |

### Frontmatter

| Field | Required value |
|---|---|
| `type` | `tutorial` |
| `exam_objective` | matching objective ID |
| `tutorial_index` | integer |
| `status` | `draft` |

### Platform Readiness (Stage 3 scope only)

| Check | Pass Criteria |
|---|---|
| No platform formatting | Zero `{% stepper %}`, `{% hint %}`, `::simple-task` in body |
| No source comments | Zero `<!-- Source: -->` lines (stripped by stage3_run.py) |

**TUTORIAL GATE: All checks Pass → proceed to Stage 4**

---

## How-to Quality Gate

**File:** `<objective_id>_howto_NN.md`

### Diataxis Purity

| Check | Pass Criteria |
|---|---|
| Compass confirmed | Action (practical) + Application (work) → How-to |
| Title begins "How to..." | Exact format enforced |
| Every step is an action | No conceptual content as a step |
| Zero explanation paragraphs | No "this works because..." |
| Zero complete reference tables | Brief inline notes permitted, full tables not |
| Competence assumed | No teaching, no background — reader is competent |

### Structure Completeness

| Section | Required |
|---|---|
| "How to..." title | Yes |
| Before You Begin (practical requirements) | Yes |
| Numbered steps (each an action) | Yes |
| Verification step with expected output | Yes |
| Troubleshooting table (Problem \| Cause \| Solution) | Yes |
| Related links | Yes |

### Frontmatter

| Field | Required value |
|---|---|
| `type` | `how-to` |
| `exam_objective` | matching objective ID |
| `howto_index` | integer |
| `difficulty` | `foundational`, `intermediate`, or `advanced` |
| `status` | `draft` |

### Platform Readiness (Stage 3 scope only)

| Check | Pass Criteria |
|---|---|
| No platform formatting | Zero `{% hint %}`, `::simple-task` in body |
| No source comments | Zero `<!-- Source: -->` lines (stripped by stage3_run.py) |

**HOW-TO GATE: All checks Pass → proceed to Stage 4**

---

## Reference Quality Gate

**File:** `<objective_id>_reference.md`

### Diataxis Purity

| Check | Pass Criteria |
|---|---|
| Compass confirmed | Cognition (theoretical) + Application (work) → Reference |
| Neutral title | "[Subject] Reference" — no "How to" or "Understanding" |
| Zero instructions | No "to use X, first do Y" language |
| Zero opinion | No "you should use..." |
| Consistent structure | Same section order as other Reference docs |
| Examples illustrate only | No tutorial-style narrative in examples |

### Structure Completeness

| Section | Required |
|---|---|
| Neutral title ("[Subject] Reference") | Yes |
| One-sentence factual description | Yes |
| Syntax / signature | Yes (if applicable) |
| Options/Flags table | Yes (if applicable) |
| Examples (illustrative, not instructional) | Yes |
| Notes and Constraints | Yes |
| See Also links | Yes |

### Frontmatter

| Field | Required value |
|---|---|
| `type` | `reference` |
| `exam_objective` | matching objective ID |
| `status` | `draft` |

### Platform Readiness (Stage 3 scope only)

| Check | Pass Criteria |
|---|---|
| No platform formatting | Zero `{% %}` blocks in body |
| No source comments | Zero `<!-- Source: -->` lines (stripped by stage3_run.py) |

**REFERENCE GATE: All checks Pass → proceed to Stage 4**

---

## Cross-Document Integrity Gate

Run after all four documents pass their individual gates.

| Check | Pass Criteria |
|---|---|
| All documents present | explanation, tutorial(s), how-to(s), reference all exist |
| Document count within bounds | 3–7 tutorials, 3–7 how-tos |
| No content duplicated | Same passage does not appear verbatim in two documents |
| Exam objective consistent | All documents share the same `exam_objective` frontmatter value |
| No placeholder text | Zero `[placeholder]` or `[fill this in]` in any document |
| Template comments stripped | Zero `<!-- GUIDANCE -->`, `<!-- PURPOSE -->`, `<!-- IRON LAW -->` blocks |
| Difficulty progression logical | How-to difficulty: foundational → intermediate → advanced |

**CROSS-DOCUMENT GATE: All checks Pass → Stage 3 complete, hand off to Stage 4**

---

## Failure Routing

| Failure type | Action |
|---|---|
| Contamination found | Extract content to correct document. Never delete. Re-run gate. |
| Missing section | Write the section. Re-run gate. |
| Wrong compass placement | Re-classify. Move content. Re-run gate. |
| Platform syntax in content | Strip it — platform formatting belongs in Stage 4/5. Re-run gate. |
| Placeholder text remaining | Fill or remove. Re-run gate. |
