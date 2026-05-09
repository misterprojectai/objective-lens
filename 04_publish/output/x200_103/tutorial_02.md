---
description: Learn to anchor grep patterns to line position using ^ and $ to restrict matches to the beginning or end of a line.
icon: graduation-cap
---

# Anchor Patterns to Line Position with ^ and $

{% hint style="info" %}
**Prerequisites**

- A terminal on a RHEL 9 system (or compatible) with read access to `/etc/passwd` and `/etc/shells`
- Completion of Tutorial 1: Search Files with grep — Basic Pattern Matching, or equivalent familiarity with invoking `grep` against a file
{% endhint %}

{% stepper %}
{% step %}
### Observe the Default — No Anchoring

Search `/etc/passwd` for the string `root` without any anchor to see how `grep` matches anywhere in the line.

```bash
grep 'root' /etc/passwd
```

{% code title="Output" %}
```
root:x:0:0:root:/root:/bin/bash
operator:x:11:0:operator:/root:/sbin/nologin
```
{% endcode %}

Both lines match — `root` appears at the very beginning of the first line and embedded inside the second line. Without an anchor, `grep` accepts a match at any position.
{% endstep %}

{% step %}
### Restrict Matches to the Beginning of a Line with ^

Add the `^` anchor to require the match at the start of the line.

```bash
grep '^root' /etc/passwd
```

{% code title="Output" %}
```
root:x:0:0:root:/root:/bin/bash
```
{% endcode %}

Only one line appears now. The `operator` line is gone because `root` does not begin that line — the anchor discarded it.

{% hint style="warning" %}
The `^` character means "start of line" only when it appears as the **first character** of the pattern. Inside a character class such as `[^a]`, it means "not" — an entirely different role.
{% endhint %}
{% endstep %}

{% step %}
### Restrict Matches to the End of a Line with $

Switch to the `$` anchor and search `/etc/passwd` for lines that end with `bash`.

```bash
grep 'bash$' /etc/passwd
```

{% code title="Output" %}
```
root:x:0:0:root:/root:/bin/bash
studentvm1:x:1000:1000::/home/studentvm1:/bin/bash
```
{% endcode %}

Every matching line ends with the characters `bash` immediately before the newline. Any account whose shell entry contains `bash` somewhere other than at the very end — or not at all — is absent from the output.

{% hint style="warning" %}
The `$` anchor matches the position **before** the newline at the end of the line, not after it. The newline character itself is not part of the match.
{% endhint %}
{% endstep %}

{% step %}
### See the $ Anchor at Work with /etc/shells

Apply the same `$` anchor against `/etc/shells`, which lists one valid shell path per line.

```bash
grep 'bash$' /etc/shells
```

{% code title="Output" %}
```
/bin/bash
/usr/bin/bash
```
{% endcode %}

Both entries end with `bash`. The `$` anchor ensures we match only lines whose final characters are `bash` — not lines that merely contain the string somewhere else.
{% endstep %}

{% step %}
### Apply ^ to /etc/shells to Match a Path Prefix

Use the `^` anchor to find only the shells whose path starts with `/bin`.

```bash
grep '^/bin' /etc/shells
```

{% code title="Output" %}
```
/bin/sh
/bin/bash
```
{% endcode %}

Notice that `/usr/bin/bash` is absent — its path begins with `/usr`, not `/bin`, so the `^` anchor excludes it.
{% endstep %}

{% step %}
### Combine ^ and $ to Match an Exact Line

Combine both anchors in a single pattern. When `^` and `$` appear together, the pattern must account for the entire line from first character to last.

```bash
grep '^/bin/bash$' /etc/shells
```

{% code title="Output" %}
```
/bin/bash
```
{% endcode %}

`/usr/bin/bash` does not appear. The leading `^` requires the line to start with `/bin/bash`, and the trailing `$` requires it to end there — only an exact match qualifies.
{% endstep %}

{% step %}
### Verify the Pattern ^$ Matches Only Blank Lines

Run the pattern with both anchors adjacent and nothing between them against `/etc/shells`.

```bash
grep '^$' /etc/shells
```

{% code title="Output" %}
```
(no output — /etc/shells contains no blank lines)
```
{% endcode %}

Run the same pattern against `/etc/passwd`.

```bash
grep '^$' /etc/passwd
```

{% code title="Output" %}
```
(no output — /etc/passwd contains no blank lines)
```
{% endcode %}

Both system files are well-formed with no blank lines. Confirm the pattern works by testing it against a file you control.

```bash
printf 'first\n\nthird\n' | grep '^$'
```

{% code title="Output" %}

{% endcode %}

One blank line is printed — the empty line between `first` and `third`. This confirms that `^$` matches a line that has zero characters between its start and end positions.

<details>
<summary>Why does printf produce a blank line here?</summary>

The format string `'first\n\nthird\n'` contains two consecutive `\n` escape sequences after `first`. The first `\n` ends the `first` line. The second `\n` produces a line that contains no characters at all — just a newline — which is exactly what `^$` matches: a start-of-line position immediately followed by an end-of-line position.

</details>
{% endstep %}
{% endstepper %}

{% hint style="success" %}
**What you accomplished**

In this tutorial, you:

1. Ran an unanchored search and observed that `grep` matches patterns at any position in a line
2. Applied `^` to restrict a match to the beginning of a line and filtered `/etc/passwd` to a single entry
3. Applied `$` to restrict a match to the end of a line and identified login-capable accounts by their shell suffix
4. Used `^` against `/etc/shells` to select only shells under a specific directory prefix
5. Combined `^` and `$` in one pattern to match a line's exact full content
6. Confirmed that `^$` selects only blank lines by constructing a controlled test case
{% endhint %}

## Next Steps

- [How-to: Filter Comment Lines and Blank Lines with grep](../how-to/filter-comments-blank-lines-grep.md) — apply `^` and `$` to strip noise from configuration file output
- [Explanation: Understanding grep and Regular Expressions](../explanation/grep-regex-explanation.md) — understand why anchors are zero-width assertions and how the matching engine processes them
- [Reference: grep Options and Regular Expression Syntax](../reference/grep-regex-reference.md) — see the complete anchor and pattern syntax in one place