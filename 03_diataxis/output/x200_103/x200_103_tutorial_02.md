---
title: "Anchor Patterns to Line Position with ^ and $"
type: tutorial
exam_objective: x200_103
tutorial_index: 2
version: "1.0"
status: draft
---

# Anchor Patterns to Line Position with ^ and $

In this tutorial, we will build the skill of writing positional patterns using the `^` and `$` anchors to restrict matches to the beginning or end of a line. Along the way, we will work with `/etc/passwd` and `/etc/shells` to observe exactly how anchor placement changes which lines qualify.

---

## Prerequisites

Before starting, ensure you have:

- A terminal on a RHEL 9 system (or compatible) with read access to `/etc/passwd` and `/etc/shells`
- Completion of Tutorial 1: Search Files with grep — Basic Pattern Matching, or equivalent familiarity with invoking `grep` against a file

---

## What We'll Build

By the end of this tutorial, we will have run six anchored searches and observed how each anchor constrains the match to a specific position in the line. The final verification will confirm both anchors working together to match exact whole-line content:

```
$ grep '^$' /etc/shells
(no output — /etc/shells contains no blank lines)

$ grep '^/bin' /etc/shells
/bin/sh
/bin/bash

$ grep 'bash$' /etc/shells
/bin/bash
/usr/bin/bash

$ grep '^/bin/bash$' /etc/shells
/bin/bash
```

---

## Step 1: Observe the Default — No Anchoring

First, we search `/etc/passwd` for the string `root` without any anchor to see how `grep` matches anywhere in the line.

```bash
grep 'root' /etc/passwd
```

You should see:

```
root:x:0:0:root:/root:/bin/bash
operator:x:11:0:operator:/root:/sbin/nologin
```

Notice that both lines match — `root` appears at the very beginning of the first line and embedded inside the second line. This confirms that without an anchor, `grep` accepts a match at any position.

---

## Step 2: Restrict Matches to the Beginning of a Line with ^

Now that we have seen unanchored behavior, we add the `^` anchor to require the match at the start of the line.

```bash
grep '^root' /etc/passwd
```

You should see:

```
root:x:0:0:root:/root:/bin/bash
```

Notice that only one line appears now. The `operator` line is gone because `root` does not begin that line — the anchor discarded it.

---

## Step 3: Restrict Matches to the End of a Line with $

Now we switch to the `$` anchor and search `/etc/passwd` for lines that end with `bash`.

```bash
grep 'bash$' /etc/passwd
```

You should see output similar to:

```
root:x:0:0:root:/root:/bin/bash
studentvm1:x:1000:1000::/home/studentvm1:/bin/bash
```

Notice that every matching line ends with the characters `bash` immediately before the newline. Any account whose shell entry contains `bash` somewhere other than at the very end — or not at all — is absent from the output.

---

## Step 4: See the $ Anchor at Work with /etc/shells

Now we apply the same `$` anchor against `/etc/shells`, which lists one valid shell path per line.

```bash
grep 'bash$' /etc/shells
```

You should see:

```
/bin/bash
/usr/bin/bash
```

Notice that both entries end with `bash`. The `$` anchor ensures we match only lines whose final characters are `bash` — not lines that merely contain the string somewhere else.

---

## Step 5: Apply ^ to /etc/shells to Match a Path Prefix

Now we use the `^` anchor to find only the shells whose path starts with `/bin`.

```bash
grep '^/bin' /etc/shells
```

You should see:

```
/bin/sh
/bin/bash
```

Notice that `/usr/bin/bash` is absent — its path begins with `/usr`, not `/bin`, so the `^` anchor excludes it.

---

## Step 6: Combine ^ and $ to Match an Exact Line

We now combine both anchors in a single pattern. When `^` and `$` appear together, the pattern must account for the entire line from first character to last.

```bash
grep '^/bin/bash$' /etc/shells
```

You should see:

```
/bin/bash
```

Notice that `/usr/bin/bash` does not appear. The leading `^` requires the line to start with `/bin/bash`, and the trailing `$` requires it to end there — only an exact match qualifies.

---

## Step 7: Verify the Pattern ^$ Matches Only Blank Lines

Finally, we verify the edge case where both anchors are adjacent with nothing between them.

```bash
grep '^$' /etc/shells
```

You should see:

```
(no output)
```

Now run the same pattern against a file that does contain blank lines.

```bash
grep '^$' /etc/passwd
```

You should see:

```
(no output)
```

Both system files are well-formed with no blank lines. To confirm the pattern works as expected, we test it against a file we control.

```bash
printf 'first\n\nthird\n' | grep '^$'
```

You should see:

```

```

One blank line is printed — the empty line between `first` and `third`. This confirms that `^$` matches a line that has zero characters between its start and end positions.

---

## What We Accomplished

In this tutorial, we:

1. Ran an unanchored search and observed that `grep` matches patterns at any position in a line
2. Applied `^` to restrict a match to the beginning of a line and filtered `/etc/passwd` to a single entry
3. Applied `$` to restrict a match to the end of a line and identified login-capable accounts by their shell suffix
4. Used `^` against `/etc/shells` to select only shells under a specific directory prefix
5. Combined `^` and `$` in one pattern to match a line's exact full content
6. Confirmed that `^$` selects only blank lines by constructing a test case

---

## Next Steps

Now that you can anchor patterns to line position, you might want to:

- [How-to: Filter Comment Lines and Blank Lines with grep](../how-to/filter-comments-blank-lines-grep.md) — apply `^` and `$` to strip noise from configuration file output
- [Explanation: Understanding grep and Regular Expressions](../explanation/grep-regex-explanation.md) — understand why anchors are zero-width assertions and how the matching engine processes them
- [Reference: grep Options and Regular Expression Syntax](../reference/grep-regex-reference.md) — see the complete anchor and pattern syntax in one place