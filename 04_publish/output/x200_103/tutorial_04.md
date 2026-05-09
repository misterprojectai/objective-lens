---
description: Build quantifier patterns in Basic and Extended Regular Expression syntax, then confirm that BRE and ERE produce identical matches from identical input.
icon: graduation-cap
---

# Control Repetition and Use Extended Regular Expressions

{% hint style="info" %}
**Prerequisites**

- A RHEL 9 terminal with a non-root user account that can run `grep`
- Completed Tutorial 3 of this series, or equivalent familiarity with anchors (`^`, `$`) and character classes (`[0-9]`, `[[:alpha:]]`)
{% endhint %}

{% stepper %}
{% step %}
### Create the practice file

Create a file that gives you clear, predictable input for every quantifier pattern you will test.

```bash
cat > ~/regex4.txt <<'EOF'
a:ac
b:abc
b:abbc
b:abbbc
c:abbbbc
d:colour
d:color
e:reed
e:red
f:re2d
f:re22d
g:start123end
g:start1end
EOF
```

```
You should see the prompt return with no output. Verify the file exists:
```

```bash
cat ~/regex4.txt
```

{% code title="Output" %}
```
a:ac
b:abc
b:abbc
b:abbbc
c:abbbbc
d:colour
d:color
e:reed
e:red
f:re2d
f:re22d
g:start123end
g:start1end
```
{% endcode %}

Notice that the file has predictable structure — each group of lines shares a prefix letter so you can see exactly which lines each pattern selects.
{% endstep %}

{% step %}
### Match zero or more repetitions with `*`

Apply the `*` quantifier, which means zero or more of the preceding character. This works identically in BRE and ERE.

```bash
grep 'ab*c' ~/regex4.txt
```

{% code title="Output" %}
```
a:ac
b:abc
b:abbc
b:abbbc
c:abbbbc
```
{% endcode %}

{% hint style="info" %}
The `a:ac` line matches even though it contains no `b` at all — because `*` requires zero or more occurrences, the pattern `ab*c` is satisfied by `ac` alone.
{% endhint %}
{% endstep %}

{% step %}
### Require at least one repetition — BRE syntax with `\+`

Enforce that at least one `b` must appear. In BRE, the one-or-more quantifier is written `\+` — the backslash is required because plain `grep` treats `+` as a literal character.

```bash
grep 'ab\+c' ~/regex4.txt
```

{% code title="Output" %}
```
b:abc
b:abbc
b:abbbc
c:abbbbc
```
{% endcode %}

{% hint style="info" %}
The `a:ac` line is gone — `\+` required at least one `b`, so the zero-`b` line no longer matches.
{% endhint %}

{% hint style="warning" %}
In BRE (plain `grep`), writing `+` without a backslash treats the `+` as a literal character, not a quantifier. The pattern `ab+c` in BRE searches for the exact string `ab+c`. Step 10 demonstrates this boundary directly.
{% endhint %}
{% endstep %}

{% step %}
### Make a character optional — BRE syntax with `\?`

Make the `u` in `colour` optional so the pattern matches both British and American spellings. In BRE, the zero-or-one quantifier is `\?`.

```bash
grep 'colou\?r' ~/regex4.txt
```

{% code title="Output" %}
```
d:colour
d:color
```
{% endcode %}

{% hint style="info" %}
Both spellings match. The `\?` tells the engine that `u` may appear once or not at all.
{% endhint %}
{% endstep %}

{% step %}
### Match an exact count — BRE brace interval `\{n\}`

Use a brace interval to match exactly two digits in a row. In BRE, braces must be backslash-escaped.

```bash
grep 're\([0-9]\)\{2\}d' ~/regex4.txt
```

{% code title="Output" %}
```
f:re22d
```
{% endcode %}

{% hint style="info" %}
The line `f:re2d` — with only one digit — is excluded. The `\{2\}` forced exactly two repetitions of the character class `\([0-9]\)`.
{% endhint %}

{% hint style="warning" %}
In BRE, both the braces and the grouping parentheses require backslash-escaping: `\(`, `\)`, `\{`, `\}`. Omitting any backslash causes the character to be treated as a literal.
{% endhint %}
{% endstep %}

{% step %}
### Match a range of repetitions — BRE brace interval `\{n,m\}`

Allow the `b` to appear between one and three times using a range interval.

```bash
grep 'ab\{1,3\}c' ~/regex4.txt
```

{% code title="Output" %}
```
b:abc
b:abbc
b:abbbc
```
{% endcode %}

{% hint style="info" %}
The line `c:abbbbc` — with four `b` characters — is excluded because `\{1,3\}` caps the upper bound at three.
{% endhint %}
{% endstep %}

{% step %}
### Switch to ERE — rewrite `\+` as `+` with `grep -E`

Rewrite the BRE `\+` pattern from Step 3 in ERE syntax. Under `grep -E`, the backslash is no longer needed — `+` is special by default.

```bash
grep -E 'ab+c' ~/regex4.txt
```

{% code title="Output" %}
```
b:abc
b:abbc
b:abbbc
c:abbbbc
```
{% endcode %}

{% hint style="info" %}
The output is identical to Step 3. The only difference is notation: ERE uses `+` where BRE required `\+`.
{% endhint %}
{% endstep %}

{% step %}
### Rewrite `\?` as `?` in ERE

Rewrite the optional-character pattern from Step 4 using ERE.

```bash
grep -E 'colou?r' ~/regex4.txt
```

{% code title="Output" %}
```
d:colour
d:color
```
{% endcode %}

{% hint style="warning" %}
In ERE, `?` is special without a backslash. Writing `\?` in ERE would attempt to escape a special character, which produces unintended behavior. Drop the backslash when switching from BRE to ERE.
{% endhint %}
{% endstep %}

{% step %}
### Rewrite the exact-count interval in ERE

Rewrite the two-digit interval from Step 5. In ERE, braces do not need backslash-escaping.

```bash
grep -E 're[0-9]{2}d' ~/regex4.txt
```

{% code title="Output" %}
```
f:re22d
```
{% endcode %}

{% hint style="info" %}
The pattern is cleaner — no backslashes around the braces, and no backslashes around the character class group. ERE makes brace intervals more readable for complex patterns.
{% endhint %}
{% endstep %}

{% step %}
### Confirm BRE/ERE dialect separation — the critical test

Run the same apparent pattern under plain `grep` and under `grep -E` to confirm that `+` means something different in each dialect.

First, run under plain `grep` — BRE mode, where `+` is a literal character:

```bash
grep 'ab+c' ~/regex4.txt
```

{% hint style="info" %}
No output. In BRE, `+` is not a quantifier — it is a literal plus sign. The engine searched for the exact character sequence `a`, `b`, `+`, `c`, which does not appear in the file.
{% endhint %}

Now run the same pattern under `grep -E`:

```bash
grep -E 'ab+c' ~/regex4.txt
```

{% code title="Output" %}
```
b:abc
b:abbc
b:abbbc
c:abbbbc
```
{% endcode %}

{% hint style="warning" %}
The same pattern text produces no output in BRE and full quantifier behavior in ERE. This is the dialect boundary — the character `+` changes meaning depending on which mode `grep` is operating in.
{% endhint %}
{% endstep %}

{% step %}
### Verify the final state

Confirm that the BRE and ERE versions of the one-or-more-b pattern produce identical results by running both and comparing.

```bash
echo "## BRE result"
grep 'ab\+c' ~/regex4.txt

echo ""
echo "## ERE result — identical lines"
grep -E 'ab+c' ~/regex4.txt
```

{% code title="Output" %}
```
## BRE result
b:abc
b:abbc
b:abbbc
c:abbbbc

## ERE result — identical lines
b:abc
b:abbc
b:abbbc
c:abbbbc
```
{% endcode %}

Both commands produce identical matching lines from identical input. The difference between BRE and ERE is purely notational — the underlying matching engine is the same.
{% endstep %}
{% endstepper %}

{% hint style="success" %}
**You have completed this tutorial.** You can now:

1. Create a practice file with predictable input for quantifier testing
2. Apply the `*` quantifier to match zero or more repetitions in both BRE and ERE
3. Apply the `\+` quantifier (BRE) to require one or more repetitions
4. Apply the `\?` quantifier (BRE) to make a character optional
5. Apply brace intervals `\{n\}` and `\{n,m\}` (BRE) to specify exact and ranged counts
6. Rewrite all three quantifiers in ERE syntax using `grep -E` — dropping the backslash prefixes
7. Confirm that `+` without a backslash is a literal character in BRE and a quantifier in ERE
{% endhint %}

## Next Steps

- [How-to: Filter Log Files with grep](../how-to/filter-logs-grep.md) — apply quantifier patterns to real log analysis tasks
- [How-to: Use Extended Regular Expressions with grep -E](../how-to/grep-extended-regex.md) — combine `+`, `?`, brace intervals, and alternation in ERE
- [Explanation: Understanding grep and Regular Expressions](../explanation/grep-regex-explanation.md) — understand why BRE and ERE exist as separate dialects and how the matching engine interprets quantifiers
- [Reference: grep Options and Regular Expression Syntax](../reference/grep-regex-reference.md) — see the complete quantifier syntax for BRE, ERE, and PCRE side by side