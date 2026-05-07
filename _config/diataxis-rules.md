# Diataxis Rules
**ICM Layer: L3 — Reference (do not transform)**
**Source authority: Diátaxis.docx, Applying_Diátaxis.docx, Understanding_Diátaxis.docx, diataxis_documentation_engineer.md, and quadrant principle docs**

---

## What Diataxis Is

A systematic approach to technical documentation. It identifies four distinct user needs and four corresponding forms of documentation, placing them in a systematic relationship.

From Ancient Greek: *dia* ("across") + *taxis* ("arrangement").

The framework solves three problems simultaneously:
- **Content** — what to write
- **Style** — how to write it
- **Architecture** — how to organize it

---

## The Two Dimensions

Diataxis is built on exactly two dimensions of craft. Not three, not five. Two.

**Dimension 1: Action / Cognition**
- Action = practical steps, doing, hands-on
- Cognition = theoretical knowledge, concepts, thinking

**Dimension 2: Acquisition / Application**
- Acquisition = study, learning, building skill
- Application = work, using skill, accomplishing tasks

These two dimensions define four and only four quadrants. The number is not arbitrary — it is complete.

---

## The Compass (Classification Method)

**Both questions must always be answered.** The compass is a 2×2 matrix — a single answer gives you half an axis, not a quadrant. Never classify based on one question alone.

**Q1: Action (practical, doing) or Cognition (theoretical, thinking)?**
**Q2: Acquisition (study, building skill) or Application (work, using skill)?**

Answer both. The intersection is the quadrant.

| | Acquisition (Study) | Application (Work) |
|---|---|---|
| **Action (Practical)** | TUTORIAL | HOW-TO |
| **Cognition (Theoretical)** | EXPLANATION | REFERENCE |

**Vocabulary mapping** (official Diataxis terms → simplified equivalents used in this pipeline):
- Action = Practical = doing
- Cognition = Theoretical = thinking/understanding
- Acquisition = Study = learning/building skill
- Application = Work = using existing skill

Apply the compass at the sentence level, not just document level. A paragraph that gives step-by-step instructions inside an Explanation document is contamination — regardless of where the document is filed.

**The compass is most useful when your intuition feels wrong.** If you're troubled by doubt while classifying, stop and apply both questions explicitly before proceeding.

---

## The Four Quadrants — Definitive Rules

### TUTORIAL — Practical + Study
**Orientation:** Learning-oriented. A guided experience.
**The teacher's contract:** Take full responsibility for learner success. Every step must work, every time, for every user. No exceptions.
**Primary question answered:** "What will I learn to do?"
**"Read in bath" test:** FAILS. Tutorials require hands-on doing. Cannot be read away from the product.

**Iron laws:**
- One path only. No alternatives, no options, no "you could also."
- Minimize explanation. Theory belongs in Explanation documents.
- Every step produces a visible, meaningful result.
- State expected output explicitly: "You should see:" — not "you should get something similar to."
- Use "we" language. Tutor and learner do this together.
- Narrative continuity: "Now that we have X, we will do Y."
- Anticipate common mistakes. Provide correction in real-time.

**What it contains:**
- Clear goal stated at the beginning (show end state first)
- Prerequisites — minimal, only absolute requirements
- Numbered steps with expected outputs
- Confirmation prompts between steps
- "What we accomplished" summary
- Next steps linking outward

**What it MUST NOT contain:**
- Extended explanation of why commands work
- Choices or alternative approaches
- Parameter tables or flag listings
- Opinion or judgment
- Anything that doesn't advance the single learning path

---

### HOW-TO — Practical + Work
**Orientation:** Goal-oriented. Problem-solving directions.
**The practitioner's contract:** Assume competence. Get them to the goal efficiently.
**Primary question answered:** "How do I accomplish X?"
**"Read in bath" test:** FAILS. How-tos require doing.

**Iron laws:**
- Assume the user knows what they want and why. Never teach.
- Action only. No explanation of why something works.
- Conditional imperatives: "If you want X, do Y." "To achieve W, do Z."
- Brief contextual notes only where blocking failure is likely.
- Title must start with "How to..." — not "Setting Up..." or "Understanding..."
- Include variations concisely. State which is default.
- End with verification: "To confirm this worked:"

**What it contains:**
- Action-oriented title ("How to...")
- Practical prerequisites (access, permissions, existing state)
- Numbered steps — each an action, not a concept
- Conditional variants stated briefly
- Verification step
- Troubleshooting table (common issues + fixes)
- Related links

**What it MUST NOT contain:**
- Explanation of concepts or why things work
- Tutorial-style narrative ("Now that we...")
- Complete reference tables or flag listings
- Extended background or history
- Opinion or perspective

---

### REFERENCE — Theoretical + Work
**Orientation:** Information-oriented. Technical description.
**The reference contract:** Describe accurately and completely. Obligation is to accuracy, not to the reader.
**Primary question answered:** "What does X do / accept / return?"
**"Read in bath" test:** FAILS. Reference is consulted while working.

**Iron laws:**
- Describe only. Never instruct, guide, or explain.
- Austere, factual, neutral. No marketing language, no opinion.
- Follow the structure of the product, not user needs.
- Consistent format across all entries. Predictability is the feature.
- Examples are permitted — to illustrate only, not to teach.
- Warnings and limitations must be explicit: "Requires version 3.2+."

**What it contains:**
- Neutral title naming the subject: "[Component] Reference"
- One-sentence factual description
- Syntax / signature
- Parameters table (Parameter | Type | Required | Default | Description)
- Return values
- Errors / exit codes
- Brief illustrative examples (not tutorial-style)
- See also links

**What it MUST NOT contain:**
- Step-by-step instructions ("To use X, first do Y")
- Explanation of why things work the way they do
- Opinion or judgment ("This is the best approach")
- Tutorial narrative
- How-to guidance

---

### EXPLANATION — Theoretical + Study
**Orientation:** Understanding-oriented. Conceptual discussion.
**The explainer's contract:** Illuminate. Build mental models. Provide context, rationale, and perspective.
**Primary question answered:** "Why is it like this?" / "How does this work?"
**"Read in bath" test:** PASSES. Explanation is readable away from the product. It is reflective, not operational.

**Iron laws:**
- Discuss, don't instruct. No step-by-step content.
- Answer "why" and "how does this work" — not "how do I do this."
- Frame scope as "About X" — the title must pass the implicit "about" test.
- Opinion and perspective are not just permitted — they are expected. Weigh alternatives. Discuss trade-offs. Acknowledge multiple viewpoints.
- Analogies are a primary tool. Use them freely.
- Connect to broader context: historical reasons, design choices, relationships between concepts.
- Link to how-to guides when practical action is needed; never embed procedures.

**What it contains:**
- Opening that establishes what question this explanation addresses
- Background / historical context
- How the concept works (conceptual, not procedural)
- Why this design/approach (rationale, trade-offs)
- Alternatives and their trade-offs
- Common misconceptions
- Relationship to related concepts
- Further reading

**What it MUST NOT contain:**
- Step-by-step instructions of any kind
- Command syntax as primary content (brief illustration is permitted)
- Reference tables
- "Do this, then this, then this" structure
- Tutorial-style narrative

---

## Explanation as Anchor

In this pipeline, Explanation is always written first for each RHCSA objective.

**Why:** Explanation is the conceptual foundation. Once the "why" and "how it works" are deeply understood, the other three quadrants derive from it naturally:
- Tutorial = teach the concept through guided doing
- How-to = apply the concept to solve a real task
- Reference = describe the machinery the concept operates on

If the Explanation is weak, all three downstream documents are weak. Invest here first.

---

## Contamination — The Primary Failure Mode

Contamination is the mixing of one quadrant's content into a document of another type. It is the most common and most damaging failure mode in Diataxis documentation.

**Contamination is binary, not a spectrum.** A tutorial with one paragraph of explanation is a contaminated tutorial. It is not "mostly good."

### Contamination Severity Levels

**Critical — Breaks document purpose entirely:**
- Step-by-step instructions in Explanation (turns it into a how-to)
- Concept-heavy theory in Tutorial (breaks learning flow)
- Complete flag/option tables in Tutorial (reference dump)

**High — Significant user experience damage:**
- Alternative paths in Tutorial (decision paralysis)
- "Why this works" paragraphs in How-to (interrupts task flow)
- Opinion or guidance in Reference ("you should use...")
- Procedures embedded in Explanation

**Medium — Degrades quality:**
- Brief instruction in Explanation that could be a link
- Single flag table in How-to that could be in Reference
- Narrative tone in Reference

**Low — Minor inconsistency:**
- Single sentence of context in Tutorial beyond one-line rule
- Slightly wrong tone in Reference
- Missing link to companion document

### The Eight Primary Contamination Patterns

| Pattern | Appears In | Contamination Type | Severity |
|---|---|---|---|
| "The reason this works is…" paragraph | Tutorial | Explanation bleeding in | Critical |
| "You could also use X or Y" | Tutorial | How-to alternatives | Critical |
| Complete flag/parameter table | Tutorial | Reference dump | Critical |
| "This is based on the principle of…" | How-to | Explanation bleeding in | High |
| Step-by-step instructions | Explanation | How-to bleeding in | Critical |
| "You should use X because…" opinion | Reference | Explanation bleeding in | High |
| Optional paths with branching | Tutorial | How-to structure | High |
| Conceptual discussion mid-procedure | How-to | Explanation bleeding in | High |

---

## Platform Routing Rules

In this pipeline, Diataxis quadrant determines both platform destination and document format.

| Quadrant | Platform | Format |
|---|---|---|
| Tutorial | iximiuz Labs + GitBook (separate versions) | MDC components (iximiuz) / {% stepper %} (GitBook) |
| How-to | iximiuz Labs + GitBook (separate versions) | MDC components (iximiuz) / numbered steps (GitBook) |
| Reference | GitBook only | Standard markdown tables |
| Explanation | GitBook only | Prose, no MDC, no {% %} blocks |

**The separation rule:** Reference and Explanation never get iximiuz versions. They do not need hands-on verification tasks. They are reading material.

---

## Quality Gate

**Single source of truth:** `_config/quality-checks.md`

The complete pass/fail checklists for all four quadrants, cross-document integrity, and failure routing live in `_config/quality-checks.md`. Do not use any other checklist. Using this file for quality gate decisions risks using outdated criteria.

---

## Working Method in This Pipeline

1. Receive collated raw passages from Stage 2 (objective-mapped signal)
2. Classify each passage with the compass before writing anything
3. Write Explanation first — build the conceptual anchor
4. Derive Tutorial from Explanation: what can be taught through doing?
5. Derive How-to from Explanation: what practical tasks does this enable?
6. Derive Reference from Explanation: what machinery needs description?
7. Run contamination check on each document before passing to Stage 4
8. If contamination found: extract and route to correct document — never delete good content

---

## Diataxis as Guide, Not Plan

From `Applying_Diátaxis.docx` (official source): *"Diátaxis provides an approach to work that runs counter to much of the accepted wisdom in documentation. In particular, it discourages planning and top-down workflows, preferring instead small, responsive iterations from which overall patterns emerge."*

**What this means for this pipeline:**

The pipeline enforces sequential execution because deterministic stages produce consistent output. But within each stage, Diataxis should be applied iteratively — not all at once top-down.

When Stage 3 runs:
- Start with what you have. A partial Explanation is better than a perfect outline.
- Write, classify, discover contamination, extract, repeat.
- The four documents will not emerge perfectly formed on the first pass. They improve through iteration.
- Use the compass as a correction tool mid-writing, not just at the start.

**What this does NOT mean:**
- It does not mean the four quadrants are optional.
- It does not mean contamination is acceptable "for now."
- It does not mean you can skip the compass classification step.

The iterative philosophy applies to the writing process. The framework rules are non-negotiable.
