# TEMPLATE: How-to Guide
<!-- TYPE: how-to | QUADRANT: practical + work | PLATFORM: GitBook + iximiuz (separate versions built in Stage 4/5) -->
<!-- PURPOSE: Help a competent user accomplish a specific real-world task. -->
<!-- "READ IN BATH" TEST: FAILS. Requires doing at a terminal. -->
<!-- COMPASS CHECK: Both questions required. Action (practical)? Yes. Application (work)? Yes. → How-to confirmed. -->
<!-- WRITE THIS THIRD. Derived from Explanation: what practical tasks does this concept enable? -->
<!-- TITLE RULE: Must begin with "How to..." — no exceptions. -->
<!-- THIS IS THE CONTENT TEMPLATE. Platform formatting is applied in Stage 4/5, not here. -->
<!-- NOTE: Troubleshooting table uses 3 columns (Problem | Cause | Solution) — improvement over source scaffold's
     2-column version, validated through prior pipeline experience. The Cause column prevents fix attempts
     without diagnosis. -->

---
title: "How to [Accomplish Specific Task]"
type: how-to
quadrant:
  practical_theoretical: practical
  work_study: work
exam_objective: "[x200_NNN]"
version: "1.0"
status: draft
---

# How to [Accomplish Specific Task]

<!-- IRON LAW: Assume competence. The reader knows what they want. Get them there. -->
<!-- IRON LAW: No teaching. No explaining why. Only showing how. -->
<!-- IRON LAW: Every step is an action. Not a concept. Not background. An action. -->
<!-- CONTRACT: "If you do this, you will get that." — guaranteed when followed correctly. -->

This guide shows you how to [specific outcome in one sentence].

---

## Before You Begin

<!-- NOT prerequisites for learning — practical requirements for doing. -->
<!-- State the system state that must exist before this guide can be followed. -->

Ensure you have:

- [Practical requirement — specific access, permission, or existing configuration]
- [State the system must be in: e.g., "A volume group with at least 500M free space"]

---

## Steps

### 1. [First Action — imperative verb + object]

<!-- Direct. Imperative mood. No narrative. No teaching. -->

[Action instruction — one sentence, imperative.]

```bash
[exact command]
```

<!-- Brief contextual note ONLY if omitting it causes blocking failure — one sentence maximum. -->
> **Note:** [Brief practical warning only if blocking failure is likely — otherwise delete this line.]

---

### 2. [Second Action]

[Action instruction.]

If you want [variation A], use:

```bash
[command for variation A]
```

If you want [variation B], use:

```bash
[command for variation B]
```

---

### 3. [Third Action]

<!-- Continue pattern: action + command. No explanation. No theory. -->

[Action instruction.]

```bash
[exact command]
```

---

### N. [Final Action]

[Final instruction.]

```bash
[final command]
```

---

## Verification

<!-- Always present. Never skip. -->
<!-- The exam grades system state. This trains the right habit. -->

To confirm [task] completed successfully:

```bash
[verification command]
```

Expected result:

```
[exact expected output]
```

---

## Troubleshooting

<!-- Common, predictable issues only. Three columns: Problem | Cause | Solution. -->
<!-- The Cause column prevents blind fix attempts — forces diagnosis before action. -->

| Problem | Cause | Solution |
|---|---|---|
| [Symptom] | [Why it happens] | [Exact fix] |
| [Symptom] | [Why it happens] | [Exact fix] |

---

## Related

- [Link to Reference: complete options and parameters]
- [Link to Explanation: understand why this works]
- [Link to related How-to if applicable]

---
<!-- CONTAMINATION CHECK BEFORE PUBLISHING (Diataxis purity only — platform checks are Stage 4/5):
  [ ] Title begins "How to..."
  [ ] Every step is an action, not a concept
  [ ] Zero explanation paragraphs ("this works because...")
  [ ] Zero complete reference tables (brief inline notes only)
  [ ] Verification step present with exact expected output
  [ ] No tutorial narrative ("now that we have...")
  [ ] No "you should understand" language
  [ ] Troubleshooting table present (3 columns: Problem | Cause | Solution)
  [ ] No iximiuz MDC components (::simple-task etc.) — platform formatting is Stage 4/5
  [ ] No GitBook liquid blocks ({% hint %} etc.) — platform formatting is Stage 4/5
-->