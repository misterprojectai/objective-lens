# TEMPLATE: Reference
<!-- TYPE: reference | QUADRANT: theoretical + work | PLATFORM: GitBook only -->
<!-- PURPOSE: Describe the machinery. Austere, factual, complete. -->
<!-- "READ IN BATH" TEST: FAILS. Reference is consulted while working. -->
<!-- COMPASS CHECK: Theoretical (knowledge)? Yes. Work (applying skill)? Yes. → Reference confirmed. -->
<!-- WRITE THIS FOURTH. Derived from Explanation: what machinery does this concept operate on? -->

---
title: "[Component/Command/Concept] Reference"
type: reference
quadrant:
  practical_theoretical: theoretical
  work_study: work
exam_objective: "[x200_NNN]"
version: "1.0"
status: draft
---

# [Component/Command/Concept] Reference

<!-- IRON LAW: Describe only. Never instruct, guide, or explain. -->
<!-- IRON LAW: Obligation is to accuracy and completeness, not to the reader's comfort. -->
<!-- IRON LAW: Consistent structure across all reference entries. Predictability is the feature. -->
<!-- NEUTRAL TITLE: "[Subject] Reference" — not "How to Use X" or "Understanding X" -->

[One-sentence factual description of what this is. No opinion. No judgment.]

---

## Overview

<!-- Brief structural context. Where does this fit in the RHEL/Linux system? -->
<!-- State what it is, not what to do with it. -->

`[Component]` is a [type] that [primary function]. It belongs to [parent subsystem/package].

---

## Syntax

<!-- Exact usage pattern. Every argument, every option shown in standard notation. -->
<!-- [ ] = optional, < > = required, | = OR, ... = repeatable -->

```
[component] [OPTIONS] <REQUIRED_ARG> [OPTIONAL_ARG]
```

---

## Commands / Subcommands

<!-- If the subject is a tool with subcommands, list them here. -->
<!-- One-sentence neutral description per entry. No instructions. -->

| Command | Description |
|---|---|
| `[subcommand]` | [Factual description of what it does] |
| `[subcommand]` | [Factual description of what it does] |

---

## Options / Flags

<!-- Every option the exam tests. Factual description only. -->
<!-- No "use this when..." — that's how-to guidance. Just describe what it does. -->

| Option | Type | Default | Description |
|---|---|---|---|
| `[flag]` | [type] | [default or "None"] | [Factual description] |
| `[flag]` | [type] | [default or "None"] | [Factual description] |

---

## Parameters

<!-- If the subject accepts configuration parameters (e.g., /etc/sshd_config directives) -->

| Parameter | Type | Valid Values | Default | Description |
|---|---|---|---|---|
| `[param]` | [type] | [values] | [default] | [Factual description] |

---

## Files and Paths

<!-- Configuration files, log files, binary locations relevant to this subject. -->

| Path | Purpose |
|---|---|
| `[/path/to/file]` | [What it is — not what to do with it] |
| `[/path/to/file]` | [What it is] |

---

## Exit Codes / Return Values

<!-- For commands: what numeric codes mean. -->
<!-- For functions: what return values mean. -->

| Code | Meaning |
|---|---|
| `0` | [Factual meaning] |
| `1` | [Factual meaning] |
| `[N]` | [Factual meaning] |

---

## Examples

<!-- PERMITTED: Brief examples that illustrate usage. -->
<!-- NOT PERMITTED: Tutorial-style teaching with narrative. -->
<!-- Format: one-line comment explaining what this demonstrates, then the command. -->

Basic usage:

```bash
# [What this demonstrates]
[minimal example]
```

With optional parameters:

```bash
# [What this demonstrates]
[example with key options]
```

---

## Notes and Constraints

<!-- Restrictions, required conditions, version requirements, known behaviors. -->
<!-- Explicit and objective only. No guidance or opinion. -->

- [Constraint or note stated factually]
- [Version requirement: "Requires RHEL 9 / Rocky Linux 9"]
- [Known behavior: "Returns null if X is not present"]

---

## See Also

<!-- Related reference entries, man pages, related concepts. -->

- [`[related command]`](link) — [one-line factual description]
- `man [topic]` — [what the man page covers]
- [Link to Explanation: conceptual background]
- [Link to How-to: practical application]

---
<!-- CONTAMINATION CHECK BEFORE PUBLISHING:
  [ ] Title names subject neutrally — no "How to" or "Understanding"
  [ ] Zero instructions ("to use X, first do Y")
  [ ] Zero opinion ("this is the best approach")
  [ ] Zero explanation ("this works because...")
  [ ] Parameters/options in tables, not prose
  [ ] Consistent structure with other Reference docs in this pipeline
  [ ] Examples illustrate only — no tutorial narrative
  [ ] Notes section contains only factual constraints, not guidance
-->