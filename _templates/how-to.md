# TEMPLATE: How-to Guide
<!-- TYPE: how-to | QUADRANT: practical + work | PLATFORM: GitBook + iximiuz (separate versions) -->
<!-- PURPOSE: Help a competent user accomplish a specific real-world task. -->
<!-- "READ IN BATH" TEST: FAILS. How-tos require doing at a terminal. -->
<!-- COMPASS CHECK: Practical (doing)? Yes. Work (applying existing skill)? Yes. → How-to confirmed. -->
<!-- WRITE THIS THIRD. Derived from Explanation: what practical tasks does this concept enable? -->
<!-- NOTE: Title MUST begin with "How to..." — no exceptions. -->

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

This guide shows you how to [specific outcome in one sentence].

---

## Before You Begin

<!-- NOT prerequisites for learning — practical requirements for doing. -->
<!-- State the system state that must exist before this guide can be followed. -->

Ensure you have:

- [Practical requirement — specific access, permission, or existing configuration]
- [State the system must be in: "A volume group with at least 500M free space"]

---

## Steps

### 1. [First Action — imperative verb + object]

<!-- Direct. Imperative mood. No narrative. -->

[Action instruction — one sentence, imperative.]

```bash
[exact command]
```

<!-- Brief contextual note ONLY if blocking failure is likely — one sentence maximum. -->
<!-- Format: a blockquote or inline note, NOT a paragraph of explanation. -->

> **Note:** [Brief practical warning if and only if omitting it causes blocking failure.]

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

[Continue pattern: action + command. No explanation. No theory.]

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

<!-- How do they know it worked? Always present. Never skip. -->
<!-- The exam grades system state. Train this habit in every how-to. -->

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

<!-- Optional but strongly recommended. Common, predictable issues only. -->
<!-- Not comprehensive. If the issue is rare or complex, link elsewhere. -->

| Problem | Cause | Solution |
|---|---|---|
| [Symptom] | [Why it happens] | [Exact fix] |
| [Symptom] | [Why it happens] | [Exact fix] |

---

## Related

<!-- Link to companion documents. Close the loop. -->

- [Link to Reference: complete options and parameters]
- [Link to Explanation: understand why this works]
- [Link to related How-to if applicable]

---
<!-- CONTAMINATION CHECK BEFORE PUBLISHING:
  [ ] Title begins "How to..."
  [ ] Every step is an action, not a concept
  [ ] Zero explanation paragraphs ("this works because...")
  [ ] Zero complete reference tables (brief inline notes only)
  [ ] Verification step present
  [ ] No tutorial narrative ("now that we have...")
  [ ] No "you should understand" language
  [ ] GitBook version: numbered steps with {% hint %} for warnings
  [ ] iximiuz version: verification tasks in ::simple-task components
  [ ] iximiuz version: all Diataxis frontmatter stripped before push
-->
