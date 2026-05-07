# Quality Checks — Diataxis Layer
**ICM Layer: L3 — Reference (do not transform)**
**Used by:** Stage 3 (03_diataxis/CONTEXT.md) before any file moves to Stage 4

---

## How to Use This File

Run these checks on every document produced in Stage 3 before it leaves `03_diataxis/output/`. Each check is binary: Pass or Fail. No partial credit. A single Fail blocks the document from Stage 4.

If a check fails: fix the document, re-run all checks for that quadrant, then proceed.

---

## Explanation Quality Gate

**File:** `[objective-slug]_explanation.md`

### Diataxis Purity

| Check | Pass Criteria | Result |
|---|---|---|
| Compass confirmed | Both questions answered: Cognition (theoretical) + Acquisition (study) → Explanation | |
| Title passes "About X" test | "About [title]" reads naturally | |
| "Read in bath" test | Readable without a terminal — no commands required to follow along | |
| Zero procedures | No numbered steps, no "run this command to..." as primary content | |
| Zero reference tables | No parameters, flags, or option tables as primary content | |
| Perspective present | Trade-offs and alternatives discussed with judgment, not just listed | |
| Analogies used | At least one analogy bridges abstract concept to concrete understanding | |

### Structure Completeness

| Section | Required | Present |
|---|---|---|
| Opening paragraph (conceptual question established) | Yes | |
| Background / historical context | Yes | |
| How [Topic] Works (conceptual model) | Yes | |
| Why This Design (rationale + trade-offs) | Yes | |
| Trade-offs table | Yes | |
| Common Misconceptions | Yes | |
| Relationship to [Related Concept] | Yes | |
| Further Reading (links to Tutorial, How-to, Reference) | Yes | |

### Cross-Links

| Link | Present |
|---|---|
| Link to Tutorial | |
| Link to How-to | |
| Link to Reference | |

**EXPLANATION GATE: All checks Pass → proceed to Stage 4**

---

## Tutorial Quality Gate

**File:** `[objective-slug]_tutorial.md`

### Diataxis Purity

| Check | Pass Criteria | Result |
|---|---|---|
| Compass confirmed | Both questions answered: Action (practical) + Acquisition (study) → Tutorial | |
| Single path only | Zero alternatives, zero "you could also" | |
| Zero explanation paragraphs | No "the reason this works is..." content | |
| Zero reference tables | No parameter tables or complete flag listings | |
| "We" language throughout | Tutor and learner working together — not "you should" | |
| Every step has expected output | "You should see:" block present for every step | |
| Iron Law held | Every step produces a visible, meaningful result | |

### Structure Completeness

| Section | Required | Present |
|---|---|---|
| Action-oriented title (Build/Create/Configure) | Yes | |
| Opening sentence stating concrete outcome | Yes | |
| Prerequisites (minimal, absolute only) | Yes | |
| What We'll Build (end state shown before step 1) | Yes | |
| Numbered steps with commands | Yes | |
| Each step has "You should see:" block | Yes | |
| What We Accomplished (past tense, actions) | Yes | |
| Next Steps (links outward, no new teaching) | Yes | |

### Cross-Links

| Link | Present |
|---|---|
| Link to How-to | |
| Link to Explanation | |
| Link to Reference | |

### Platform Readiness (Stage 3 scope only)

| Check | Pass Criteria | Result |
|---|---|---|
| No platform formatting in content | Zero `{% stepper %}`, `{% hint %}`, `::simple-task` in body text — platform formatting applied in Stage 4/5 | |
| Internal Diataxis frontmatter present | `type`, `quadrant`, `version`, `status` fields present — pipeline tracking metadata | |

**TUTORIAL GATE: All checks Pass → proceed to Stage 4**

---

## How-to Quality Gate

**File:** `[objective-slug]_how-to.md` (or `_how-to-01.md`, `_how-to-02.md` if multiple tasks)

### Diataxis Purity

| Check | Pass Criteria | Result |
|---|---|---|
| Compass confirmed | Both questions answered: Action (practical) + Application (work) → How-to | |
| Title begins "How to..." | Exact format enforced | |
| Every step is an action | No conceptual content as a step | |
| Zero explanation paragraphs | No "this works because..." | |
| Zero complete reference tables | Brief inline notes permitted, full tables not | |
| Competence assumed | No teaching, no background — reader is competent | |
| Contract language | Reads as "if you do this, you get that" | |

### Structure Completeness

| Section | Required | Present |
|---|---|---|
| "How to..." title | Yes | |
| One-sentence outcome statement | Yes | |
| Before You Begin (practical requirements) | Yes | |
| Numbered steps (each an action) | Yes | |
| Verification step with exact expected output | Yes | |
| Troubleshooting table (3 columns: Problem \| Cause \| Solution) | Yes | |
| Related links | Yes | |

### Cross-Links

| Link | Present |
|---|---|
| Link to Reference | |
| Link to Explanation | |

### Platform Readiness (Stage 3 scope only)

| Check | Pass Criteria | Result |
|---|---|---|
| No platform formatting in content | Zero `{% hint %}`, `::simple-task` in body text — platform formatting applied in Stage 4/5 | |
| Internal Diataxis frontmatter present | `type`, `quadrant`, `version`, `status` fields present — pipeline tracking metadata | |

**HOW-TO GATE: All checks Pass → proceed to Stage 4**

---

## Reference Quality Gate

**File:** `[objective-slug]_reference.md`

### Diataxis Purity

| Check | Pass Criteria | Result |
|---|---|---|
| Compass confirmed | Both questions answered: Cognition (theoretical) + Application (work) → Reference | |
| Neutral title | "[Subject] Reference" — no "How to" or "Understanding" | |
| Zero instructions | No "to use X, first do Y" language | |
| Zero opinion | No "you should use..." or "this is the best approach" | |
| Zero explanation | No "this works because..." as primary content | |
| Consistent structure | Same section order as other Reference docs in pipeline | |
| Examples illustrate only | No tutorial-style narrative in examples section | |

### Structure Completeness

| Section | Required | Present |
|---|---|---|
| Neutral title ("[Subject] Reference") | Yes | |
| One-sentence factual description | Yes | |
| Syntax / signature | Yes (if applicable) | |
| Commands/Subcommands table | Yes (if applicable) | |
| Options/Flags table | Yes (if applicable) | |
| Files and Paths table | Yes (if applicable) | |
| Exit Codes / Return Values | Yes (if applicable) | |
| Examples (illustrative, not instructional) | Yes | |
| Notes and Constraints | Yes | |
| See Also links | Yes | |

### Cross-Links

| Link | Present |
|---|---|
| Link to Explanation | |
| Link to How-to | |

### Platform Readiness (Stage 3 scope only)

| Check | Pass Criteria | Result |
|---|---|---|
| No platform formatting in content | Zero `{% %}` blocks in body text — platform formatting applied in Stage 4 | |
| Internal Diataxis frontmatter present | `type`, `quadrant`, `version`, `status` fields present — pipeline tracking metadata | |

**REFERENCE GATE: All checks Pass → proceed to Stage 4**

---

## Cross-Document Integrity Gate

Run after all four documents pass their individual gates.

| Check | Pass Criteria | Result |
|---|---|---|
| All four documents present | explanation, tutorial, how-to, reference all exist in output/ | |
| Naming convention consistent | All use `[objective-slug]_[type].md` pattern | |
| No content duplicated | Same passage does not appear in two documents | |
| All cross-links reciprocal | If Tutorial links to Explanation, Explanation links back to Tutorial | |
| Exam objective consistent | All four documents reference the same `exam_objective` in frontmatter | |
| No placeholder text remaining | Zero `[placeholder]` or `[fill this in]` in any document | |
| Template guidance comments stripped | All `<!-- PURPOSE:`, `<!-- IRON LAW:`, `<!-- COMPASS CHECK:`, `<!-- CONTAMINATION CHECK` comment blocks removed | |
| Source attribution preserved | `<!-- Source: [filename] -->` comments retained — required for traceability | |

**CROSS-DOCUMENT GATE: All checks Pass → Stage 3 complete, hand off to Stage 4**

---

## Failure Routing

| Failure type | Action |
|---|---|
| Contamination found (any severity) | Extract content to correct document. Never delete. Re-run gate. |
| Missing section | Write the section. Re-run gate. |
| Broken cross-link | Add the link to both documents. Re-run gate. |
| Placeholder text remaining | Fill or remove. Re-run gate. |
| Wrong compass placement | Re-classify with both questions. Move content. Re-run gate. |
| Platform syntax found in content layer | Strip it. Platform formatting is Stage 4/5. Re-run gate. |
