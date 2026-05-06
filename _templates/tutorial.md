# TEMPLATE: Tutorial
<!-- TYPE: tutorial | QUADRANT: practical + study | PLATFORM: GitBook + iximiuz (separate versions built in Stage 4/5) -->
<!-- PURPOSE: A guided learning experience. Teacher takes full responsibility for learner success. -->
<!-- "READ IN BATH" TEST: FAILS. This requires hands-on doing at a terminal. -->
<!-- COMPASS CHECK: Both questions required. Action (practical)? Yes. Acquisition (study)? Yes. → Tutorial confirmed. -->
<!-- WRITE THIS SECOND. Derived from the Explanation anchor. -->
<!-- THIS IS THE CONTENT TEMPLATE. Platform formatting ({% stepper %}, ::simple-task) is applied in Stage 4/5, not here. -->

---
title: "[Action-Oriented Title: Build/Create/Configure Your First X]"
type: tutorial
quadrant:
  practical_theoretical: practical
  work_study: study
exam_objective: "[x200_NNN]"
version: "1.0"
status: draft
---

# [Action-Oriented Title]

<!-- IRON LAW: One path only. No alternatives. No "you could also." -->
<!-- IRON LAW: Every step must produce a visible result, every time, for every user. -->
<!-- IRON LAW: Use "we" language throughout. Tutor and learner do this together. -->
<!-- IRON LAW: Minimize explanation. Theory is in the Explanation document — link, don't repeat. -->

In this tutorial, we will [concrete outcome the learner will achieve]. Along the way, we will work with [2-3 key concepts/commands they'll use].

---

## Prerequisites

<!-- MINIMAL. Only absolute requirements. No "nice to haves." -->
<!-- Every learner who meets these prerequisites must be able to complete every step. -->

Before starting, ensure you have:

- [Absolute requirement 1 — specific, not vague]
- [Absolute requirement 2]

---

## What We'll Build

<!-- Show the end state BEFORE step one. Let the learner visualize success. -->
<!-- This is the contract: follow every step, get this result. -->

By the end of this tutorial, you will have [concrete, verifiable outcome]. The system will be in this state:

```
[Expected final state — command output, file contents, or system configuration]
```

---

## Step 1: [First Concrete Action — verb + object]

<!-- ONE atomic action. ONE visible result. Confirm before proceeding. -->
<!-- Start with "First, we..." -->

First, we [action].

```bash
[exact command]
```

You should see:

```
[exact expected output]
```

[Optional: one sentence of confirmation — "This confirms that Z is now active."]
[If predictable failure: "If you see X instead of Y, [specific fix]."]

---

## Step 2: [Second Concrete Action]

<!-- "Now that we have [result from Step 1], we [next action]." -->
<!-- Maintain narrative continuity. Never jump without connecting. -->

Now that we have [result from Step 1], we [next action].

```bash
[exact command]
```

You should see:

```
[exact expected output]
```

Notice that [point out one important observation — connects action to understanding without explaining theory].

---

## Step 3: [Third Concrete Action]

<!-- Continue pattern: action → expected result → confirmation → optional observation -->

[Continue steps...]

```bash
[exact command]
```

You should see:

```
[exact expected output]
```

---

## Step N: [Final Action — verify complete system state]

<!-- The last step always verifies the complete system state. -->
<!-- Output must match what was shown in "What We'll Build." -->

Finally, we verify the complete configuration.

```bash
[verification command]
```

You should see:

```
[final expected output matching "What We'll Build"]
```

---

## What We Accomplished

<!-- Close the loop. Reinforce WHAT THEY DID — past tense, active voice, actions not concepts. -->

In this tutorial, we:

1. [Action completed — past tense verb + object]
2. [Action completed]
3. [Action completed]

---

## Next Steps

<!-- Link outward. Do NOT teach more here. -->

Now that you have [outcome], you might want to:

- [Link to How-to: apply this in a real scenario]
- [Link to Explanation: understand why this works]
- [Link to Reference: see complete command options]

---
<!-- CONTAMINATION CHECK BEFORE PUBLISHING (Diataxis purity only — platform checks are Stage 4/5):
  [ ] Zero explanation paragraphs ("the reason this works is...")
  [ ] Zero alternative paths ("you could also...")
  [ ] Zero parameter tables or flag listings
  [ ] "We" language used throughout
  [ ] Every step has an explicit "You should see:" block with exact output
  [ ] Single path to completion — no branching
  [ ] "What We Accomplished" section present
  [ ] Links to How-to, Explanation, Reference in Next Steps
  [ ] No iximiuz MDC components (::simple-task etc.) — platform formatting is Stage 4/5
  [ ] No GitBook liquid blocks ({% stepper %} etc.) — platform formatting is Stage 4/5
-->