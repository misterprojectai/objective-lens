---
description: Use the dot wildcard, bracket expressions, and POSIX named character classes to match variable or constrained single characters in grep patterns.
icon: graduation-cap
---

# Match Character Sets and Wildcards in grep Patterns

{% hint style="info" %}
**Prerequisites**

- A RHEL 9 (or compatible) terminal with a normal user account
- Completion of Tutorial 2: Anchor grep Matches to the Start and End of Lines, or equivalent familiarity with `^` and `$` anchors
{% endhint %}

{% stepper %}
{% step %}
### Match Any Single Character with the Dot Wildcard

Search `/etc/passwd` for any three-character sequence that begins with `r` and ends with `t`.

```bash
grep 'r.t' /etc/passwd
```

{% code title="Output" %}
```
operator:x:11:0:operator:/root:/sbin/nologin
```
{% endcode %}

The dot matched the letter `o` — it will match any single character in that position, including digits, spaces, or punctuation.
{% endstep %}

{% step %}
### Confirm the Dot Is Not the Shell Wildcard

Verify that single-quoting the pattern prevents the shell from expanding the dot before `grep` sees it.

```bash
grep 'r.t' /etc/passwd | wc -l
```

{% code title="Output" %}
```
1
```
{% endcode %}

The shell left the dot inside the single quotes untouched. `grep` received the pattern `r.t` and applied its own matching engine to it.

{% hint style="warning" %}
Always single-quote grep patterns. Without quotes, the shell may expand special characters — such as `*` or `?` — before grep sees them, producing unexpected behaviour.
{% endhint %}
{% endstep %}

{% step %}
### Use a Bracket Expression to Constrain the Character

Apply a bracket expression to restrict which characters qualify in a match. Search for `eth` followed by exactly one digit in `/var/log/messages`.

```bash
grep 'eth[0-9]' /var/log/messages
```

{% code title="Output" %}
```
Nov 16 07:41:00 rhel9 kernel: e1000 0000:00:03.0 eth0: Intel(R) PRO/1000 Network
Nov 16 07:41:00 rhel9 kernel: e1000 0000:00:08.0 eth1: Intel(R) PRO/1000 Network
```
{% endcode %}

Lines containing the word `method` are not shown — `[0-9]` restricts the fourth character to digits only, excluding alphabetic characters that follow `eth` in that word.

<details>
<summary>If /var/log/messages does not exist on your system</summary>

Use the systemd journal as an equivalent source:

```bash
journalctl -k | grep 'eth[0-9]'
```

This filters kernel messages only and applies the same bracket expression pattern.

</details>
{% endstep %}

{% step %}
### Invert the Bracket Expression to Exclude Digits

Flip the previous logic by searching for `eth` followed by any character that is **not** a digit.

```bash
grep 'eth[^0-9]' /var/log/messages
```

{% code title="Output" %}
```
Nov  6 09:27:36 rhel9 pulseaudio[1738]: E: [pulseaudio] bluez5-util.c: GetManagedObjects() failed: org.freedesktop.DBus.Error.ServiceUnknown: ...ethernet...
```
{% endcode %}

{% hint style="info" %}
If no output appears, that means no lines matching `eth` followed by a non-digit exist in your log. That is a valid result — the pattern itself is correct.
{% endhint %}

{% hint style="warning" %}
The `^` character inside a bracket expression means **negation**. Outside a bracket expression, `^` anchors the pattern to the start of a line. Context determines meaning.
{% endhint %}
{% endstep %}

{% step %}
### Use a POSIX Named Class to Match Any Digit

Replace the `[0-9]` range with the portable POSIX named class `[:digit:]`. Search `/etc/passwd` for any line containing a digit.

```bash
grep '[[:digit:]]' /etc/passwd | head -3
```

{% code title="Output" %}
```
root:x:0:0:root:/root:/bin/bash
bin:x:1:1:bin:/bin:/sbin/nologin
daemon:x:2:2:daemon:/sbin:/sbin/nologin
```
{% endcode %}

{% hint style="warning" %}
The double bracket structure is required. The outer `[ ]` opens the bracket expression; the inner `[:digit:]` is the POSIX class name. Writing `grep '[:digit:]'` without the enclosing `[ ]` will either error or produce unexpected results.
{% endhint %}
{% endstep %}

{% step %}
### Use a POSIX Named Class to Match Alphabetic Characters

Apply the companion class `[[:alpha:]]` with an anchor. Search `/etc/passwd` for lines that begin with an uppercase letter.

```bash
grep '^[[:upper:]]' /etc/passwd
```

{% code title="Output" %}

{% endcode %}

No output is printed. Every account line in `/etc/passwd` begins with a lowercase letter. The empty result is the correct expected output — the pattern worked exactly as specified, and found no matches.

{% hint style="success" %}
An empty result from a correctly written pattern is meaningful data, not an error. Confirming zero matches is a valid and useful grep outcome.
{% endhint %}
{% endstep %}

{% step %}
### Combine a POSIX Class with the Dot Wildcard for a Precise Position Match

Build a more precise pattern by combining four leading dots with `[[:digit:]]`. Search for lines in `/etc/passwd` where the fifth character is a digit.

```bash
grep '^....[[:digit:]]' /etc/passwd
```

{% code title="Output" %}
```
sync:x:5:0:sync:/sbin:/bin/sync
halt:x:7:0:halt:/sbin:/sbin/halt
mail:x:8:12:mail:/var/spool/mail/sbin/nologin
```
{% endcode %}

Each leading dot matches exactly one character. Four dots require the first four positions to be occupied by any character, and `[[:digit:]]` then requires a digit in the fifth position.
{% endstep %}

{% step %}
### Verify the Complete Pattern Skill Set

Run all four pattern types in sequence to confirm each works as expected.

```bash
grep 'r.t' /etc/passwd
```

{% code title="Output" %}
```
operator:x:11:0:operator:/root:/sbin/nologin
```
{% endcode %}

```bash
grep 'eth[0-9]' /var/log/messages | head -2
```

{% code title="Output" %}
```
Nov 16 07:41:00 rhel9 kernel: e1000 0000:00:03.0 eth0: Intel(R) PRO/1000 Network
Nov 16 07:41:00 rhel9 kernel: e1000 0000:00:08.0 eth1: Intel(R) PRO/1000 Network
```
{% endcode %}

```bash
grep '[[:digit:]]' /etc/passwd | head -3
```

{% code title="Output" %}
```
root:x:0:0:root:/root:/bin/bash
bin:x:1:1:bin:/bin:/sbin/nologin
daemon:x:2:2:daemon:/sbin:/sbin/nologin
```
{% endcode %}

```bash
grep '^[[:upper:]]' /etc/passwd
```

{% hint style="success" %}
The final command produces no output — every account line in `/etc/passwd` begins with a lowercase letter. No output is the correct expected result.
{% endhint %}
{% endstep %}
{% endstepper %}

{% hint style="success" %}
**Tutorial complete.** You have now:

1. Used the dot wildcard to match any single character within a pattern
2. Confirmed that single-quoting patterns prevents shell expansion of the dot
3. Used a bracket expression with a range `[0-9]` to constrain character matching to digits only
4. Inverted a bracket expression with `[^0-9]` to exclude digits from a match
5. Replaced a range expression with the POSIX named class `[[:digit:]]` for portable digit matching
6. Applied `[[:upper:]]` with an anchor to verify that no `/etc/passwd` lines begin with an uppercase letter
7. Combined four leading dots with `[[:digit:]]` to match on a specific character position within a line
{% endhint %}

## Next Steps

- [How-to: Filter Log Files with grep](../how-to/filter-logs-grep.md) — apply these patterns to real log analysis tasks
- [Tutorial 4: Match Repeated Characters with grep Quantifiers](../tutorials/grep-quantifiers.md) — extend single-character patterns to variable-length sequences
- [Explanation: Understanding grep and Regular Expressions](../explanation/grep-regex-explanation.md) — understand why POSIX classes are more portable than range expressions like `[a-z]`
- [Reference: grep Options and Regular Expression Syntax](../reference/grep-regex-reference.md) — see the complete list of POSIX named classes