---
title: "Match Character Sets and Wildcards in grep Patterns"
type: tutorial
quadrant:
  practical_theoretical: practical
  work_study: study
exam_objective: x200_103
tutorial_index: 3
version: "1.0"
status: draft
---

# Match Character Sets and Wildcards in grep Patterns

In this tutorial, we will build the skill of writing grep patterns that match variable or constrained single characters. Along the way, we will work with the dot wildcard, bracket expressions with ranges, and POSIX named character classes such as `[:alpha:]` and `[:digit:]`.

---

## Prerequisites

Before starting, ensure you have:

- A RHEL 9 (or compatible) terminal with a normal user account
- Completion of Tutorial 2: Anchor grep Matches to the Start and End of Lines, or equivalent familiarity with `^` and `$` anchors

---

## What We'll Build

By the end of this tutorial, we will have used four distinct pattern techniques against `/etc/passwd` and `/var/log/messages` (or the systemd journal as a fallback). The final verification step will produce output matching this session:

```
[student@rhel9 ~]$ grep 'r.t' /etc/passwd
operator:x:11:0:operator:/root:/sbin/nologin

[student@rhel9 ~]$ grep 'eth[0-9]' /var/log/messages
Nov 16 07:41:00 rhel9 kernel: e1000 0000:00:03.0 eth0: Intel(R) PRO/1000

[student@rhel9 ~]$ grep '[[:digit:]]' /etc/passwd | head -3
root:x:0:0:root:/root:/bin/bash
bin:x:1:1:bin:/bin:/sbin/nologin
daemon:x:2:2:daemon:/sbin:/sbin/nologin

[student@rhel9 ~]$ grep '^[[:upper:]]' /etc/passwd
```

The last command produces no output on a standard system — which is itself the expected result we will verify.

---

## Step 1: Match Any Single Character with the Dot Wildcard

First, we search `/etc/passwd` for any three-character sequence that begins with `r` and ends with `t`.

```bash
grep 'r.t' /etc/passwd
```

You should see:

```
operator:x:11:0:operator:/root:/sbin/nologin
```

Notice that the dot matched the letter `o` — it would match any single character in that position, including digits, spaces, or punctuation.

---

## Step 2: Confirm the Dot Is Not the Shell Wildcard

Now that we have seen the dot match one character inside a pattern, we confirm it is not expanded by the shell before `grep` sees it.

```bash
grep 'r.t' /etc/passwd | wc -l
```

You should see:

```
1
```

The shell left the dot inside the single quotes untouched. `grep` received the pattern `r.t` and applied its own matching engine to it.

---

## Step 3: Use a Bracket Expression to Constrain the Character

Now that we have seen the dot match any character, we apply a bracket expression to restrict which characters qualify. We search for `eth` followed by exactly one digit in `/var/log/messages`.

```bash
grep 'eth[0-9]' /var/log/messages
```

You should see lines similar to:

```
Nov 16 07:41:00 rhel9 kernel: e1000 0000:00:03.0 eth0: Intel(R) PRO/1000 Network
Nov 16 07:41:00 rhel9 kernel: e1000 0000:00:08.0 eth1: Intel(R) PRO/1000 Network
```

If `/var/log/messages` does not exist on your system, use this equivalent command instead:

```bash
journalctl -k | grep 'eth[0-9]'
```

Notice that lines containing the word `method` are not shown — the bracket expression `[0-9]` restricted the fourth character to digits only, excluding alphabetic characters that would follow `eth` in that word.

---

## Step 4: Invert the Bracket Expression to Exclude Digits

Now that we have matched lines where a digit follows `eth`, we flip that logic. We search for `eth` followed by any character that is not a digit.

```bash
grep 'eth[^0-9]' /var/log/messages
```

You should see lines that contain `eth` followed by a non-digit — for example, lines mentioning `method` or `ethernet`:

```
Nov  6 09:27:36 rhel9 pulseaudio[1738]: E: [pulseaudio] bluez5-util.c: GetManagedObjects() failed: org.freedesktop.DBus.Error.ServiceUnknown: ...ethernet...
```

If no output appears, that means no such lines exist in your log — that is a valid result. The pattern itself is correct.

---

## Step 5: Use a POSIX Named Class to Match Any Digit

Now that we have used `[0-9]` as a digit range, we replace it with the portable POSIX named class `[:digit:]`. We search `/etc/passwd` for any line containing a digit.

```bash
grep '[[:digit:]]' /etc/passwd | head -3
```

You should see:

```
root:x:0:0:root:/root:/bin/bash
bin:x:1:1:bin:/bin:/sbin/nologin
daemon:x:2:2:daemon:/sbin:/sbin/nologin
```

Notice the double bracket structure: the outer `[ ]` opens the bracket expression; the inner `[:digit:]` is the POSIX class name. Omitting the outer brackets is a common mistake — `grep` will error or produce unexpected results if only `[:digit:]` is written without the enclosing `[ ]`.

---

## Step 6: Use a POSIX Named Class to Match Alphabetic Characters

Now that we have used `[[:digit:]]`, we apply the companion class `[[:alpha:]]`. We search `/etc/passwd` for lines that begin with an uppercase letter.

```bash
grep '^[[:upper:]]' /etc/passwd
```

You should see:

```
```

No output is printed. Every account line in `/etc/passwd` begins with a lowercase letter. The empty result is the correct expected output — the pattern worked exactly as specified, and found no matches.

---

## Step 7: Combine a POSIX Class with Anchors for a Precise Pattern

Now that we have used `[[:upper:]]` alone, we combine it with what we already know about the dot to build a more precise pattern. We search for lines in `/etc/passwd` where the fifth character is a digit.

```bash
grep '^....[[:digit:]]' /etc/passwd
```

You should see lines where the fifth character is a digit:

```
sync:x:5:0:sync:/sbin:/bin/sync
halt:x:7:0:halt:/sbin:/sbin/halt
mail:x:8:12:mail:/var/spool/mail/sbin/nologin
```

Each leading dot matches exactly one character. Four dots require the first four positions to be occupied by any character, and `[[:digit:]]` then requires a digit in the fifth position.

---

## Step 8: Verify the Complete Pattern Skill Set

Finally, we run all four pattern types in sequence to confirm each works as expected. Run these commands one at a time:

```bash
grep 'r.t' /etc/passwd
```

```
operator:x:11:0:operator:/root:/sbin/nologin
```

```bash
grep 'eth[0-9]' /var/log/messages | head -2
```

```
Nov 16 07:41:00 rhel9 kernel: e1000 0000:00:03.0 eth0: Intel(R) PRO/1000 Network
Nov 16 07:41:00 rhel9 kernel: e1000 0000:00:08.0 eth1: Intel(R) PRO/1000 Network
```

```bash
grep '[[:digit:]]' /etc/passwd | head -3
```

```
root:x:0:0:root:/root:/bin/bash
bin:x:1:1:bin:/bin:/sbin/nologin
daemon:x:2:2:daemon:/sbin:/sbin/nologin
```

```bash
grep '^[[:upper:]]' /etc/passwd
```

```
```

All four outputs match what was shown in "What We'll Build." The skill set is confirmed.

---

## What We Accomplished

In this tutorial, we:

1. Used the dot wildcard to match any single character within a pattern
2. Confirmed that single-quoting patterns prevents shell expansion of the dot
3. Used a bracket expression with a range `[0-9]` to constrain character matching to digits only
4. Inverted a bracket expression with `[^0-9]` to exclude digits from a match
5. Replaced a range expression with the POSIX named class `[[:digit:]]` for portable digit matching
6. Applied `[[:upper:]]` with an anchor to verify that no `/etc/passwd` lines begin with an uppercase letter
7. Combined four leading dots with `[[:alpha:]]` to match on a specific character position within a line

---

## Next Steps

Now that you can match variable and constrained single characters in grep patterns, you might want to:

- [How-to: Filter Log Files with grep](../how-to/filter-logs-grep.md) — apply these patterns to real log analysis tasks
- [Tutorial 4: Match Repeated Characters with grep Quantifiers](../tutorials/grep-quantifiers.md) — extend single-character patterns to variable-length sequences
- [Explanation: Understanding grep and Regular Expressions](../explanation/grep-regex-explanation.md) — understand why POSIX classes are more portable than range expressions like `[a-z]`
- [Reference: grep Options and Regular Expression Syntax](../reference/grep-regex-reference.md) — see the complete list of POSIX named classes