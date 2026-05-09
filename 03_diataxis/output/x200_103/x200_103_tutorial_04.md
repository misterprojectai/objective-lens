---
title: "Control Repetition and Use Extended Regular Expressions"
type: tutorial
quadrant:
  practical_theoretical: practical
  work_study: study
exam_objective: x200_103
tutorial_index: 4
version: "1.0"
status: draft
---

# Control Repetition and Use Extended Regular Expressions

In this tutorial, we will build patterns that express variable-length text using quantifiers, and we will rewrite the same pattern in both Basic Regular Expression (BRE) and Extended Regular Expression (ERE) syntax to experience the dialect difference directly. Along the way, we will work with `*`, `\+`, `\?`, and brace intervals in BRE, then rewrite them using `+`, `?`, and braces under `grep -E`.

---

## Prerequisites

Before starting, ensure you have:

- A RHEL 9 terminal with a non-root user account that can run `grep`
- Completed Tutorial 3 of this series, or equivalent familiarity with anchors (`^`, `$`) and character classes (`[0-9]`, `[[:alpha:]]`)

---

## What We'll Build

By the end of this tutorial, we will have a working practice file and a complete set of quantifier patterns applied to it — first written in BRE using plain `grep`, then rewritten in ERE using `grep -E`. The final state of the terminal will confirm that both dialects produce identical matches against the same input:

```
## BRE result
b:abc
b:abbc
b:abbbc

## ERE result — identical lines
b:abc
b:abbc
b:abbbc
```

---

## Step 1: Create the practice file

First, we create a file that gives us clear, predictable input for every quantifier pattern we will test.

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

You should see the prompt return with no output. Verify the file exists:

```bash
cat ~/regex4.txt
```

You should see:

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

Notice that the file has predictable structure — each group of lines shares a prefix letter so we can see exactly which lines each pattern selects.

---

## Step 2: Match zero or more repetitions with `*`

Now that we have the file, we apply the `*` quantifier, which means zero or more of the preceding character. This works identically in BRE and ERE.

```bash
grep 'ab*c' ~/regex4.txt
```

You should see:

```
a:ac
b:abc
b:abbc
b:abbbc
c:abbbbc
```

Notice that the `a:ac` line matches even though it contains no `b` at all — because `*` requires zero or more occurrences, the pattern `ab*c` is satisfied by `ac` alone.

---

## Step 3: Require at least one repetition — BRE syntax with `\+`

Now we enforce that at least one `b` must appear. In BRE, the one-or-more quantifier is written `\+` — the backslash is required because plain `grep` treats `+` as a literal character.

```bash
grep 'ab\+c' ~/regex4.txt
```

You should see:

```
b:abc
b:abbc
b:abbbc
c:abbbbc
```

Notice that `a:ac` is gone — `\+` required at least one `b`, so the zero-`b` line no longer matches.

---

## Step 4: Make a character optional — BRE syntax with `\?`

Next, we make the `u` in `colour` optional so the pattern matches both British and American spellings. In BRE, the zero-or-one quantifier is `\?`.

```bash
grep 'colou\?r' ~/regex4.txt
```

You should see:

```
d:colour
d:color
```

Notice both spellings match. The `\?` tells the engine that `u` may appear once or not at all.

---

## Step 5: Match an exact count — BRE brace interval `\{n\}`

Now we use a brace interval to match exactly two digits in a row. In BRE, braces must be backslash-escaped.

```bash
grep 're\([0-9]\)\{2\}d' ~/regex4.txt
```

You should see:

```
f:re22d
```

Notice that `f:re2d` — with only one digit — is excluded. The `\{2\}` forced exactly two repetitions of the character class `\([0-9]\)`.

---

## Step 6: Match a range of repetitions — BRE brace interval `\{n,m\}`

Now we allow the `b` to appear between one and three times using a range interval.

```bash
grep 'ab\{1,3\}c' ~/regex4.txt
```

You should see:

```
b:abc
b:abbc
b:abbbc
```

Notice that `c:abbbbc` — with four `b` characters — is excluded because `\{1,3\}` caps the upper bound at three.

---

## Step 7: Switch to ERE — rewrite `\+` as `+` with `grep -E`

Now we rewrite the BRE `\+` pattern from Step 3 in ERE syntax. Under `grep -E`, the backslash is no longer needed — `+` is special by default.

```bash
grep -E 'ab+c' ~/regex4.txt
```

You should see:

```
b:abc
b:abbc
b:abbbc
c:abbbbc
```

Notice the output is identical to Step 3. The only difference is notation: ERE uses `+` where BRE required `\+`.

---

## Step 8: Rewrite `\?` as `?` in ERE

Now we rewrite the optional-character pattern from Step 4 using ERE.

```bash
grep -E 'colou?r' ~/regex4.txt
```

You should see:

```
d:colour
d:color
```

The output is identical to Step 4. In ERE, `?` is special without a backslash — writing `\?` in ERE would attempt to escape a special character, which is not what we want.

---

## Step 9: Rewrite the exact-count interval in ERE

Now we rewrite the two-digit interval from Step 5. In ERE, braces do not need backslash escaping.

```bash
grep -E 're[0-9]{2}d' ~/regex4.txt
```

You should see:

```
f:re22d
```

Notice the pattern is cleaner — no backslashes around the braces, and no backslashes around the character class group. ERE makes brace intervals more readable for complex patterns.

---

## Step 10: Confirm BRE/ERE dialect separation — the critical test

Now we run the same apparent pattern under plain `grep` and under `grep -E` to confirm that `+` means something different in each dialect.

First, run this under plain `grep` — BRE mode, where `+` is a literal character:

```bash
grep 'ab+c' ~/regex4.txt
```

You should see:

```
```

No output. In BRE, `+` is not a quantifier — it is a literal plus sign. The engine searched for the string `ab+c` (the character sequence a, b, literal-plus, c), which does not appear in the file.

Now run the same pattern under `grep -E`:

```bash
grep -E 'ab+c' ~/regex4.txt
```

You should see:

```
b:abc
b:abbc
b:abbbc
c:abbbbc
```

Notice the difference: the same pattern text produces no output in BRE and full quantifier behavior in ERE. This is the dialect boundary — the character `+` changes meaning depending on which mode `grep` is operating in.

---

## Step 11: Verify the final state

Finally, we confirm that our BRE and ERE versions of the one-or-more-b pattern produce identical results by running both and comparing.

```bash
echo "## BRE result"
grep 'ab\+c' ~/regex4.txt

echo ""
echo "## ERE result — identical lines"
grep -E 'ab+c' ~/regex4.txt
```

You should see:

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

Both commands produce identical matching lines from identical input. The difference between BRE and ERE is purely notational — the underlying matching engine is the same.

---

## What We Accomplished

In this tutorial, we:

1. Created a practice file with predictable input for quantifier testing
2. Applied the `*` quantifier to match zero or more repetitions in both BRE and ERE
3. Applied the `\+` quantifier (BRE) to require one or more repetitions
4. Applied the `\?` quantifier (BRE) to make a character optional
5. Applied brace intervals `\{n\}` and `\{n,m\}` (BRE) to specify exact and ranged counts
6. Rewrote all three quantifiers in ERE syntax using `grep -E` — dropping the backslash prefixes
7. Confirmed that `+` without a backslash is a literal character in BRE and a quantifier in ERE

---

## Next Steps

Now that you have controlled repetition in both BRE and ERE, you might want to:

- [How-to: Filter Log Files with grep](../how-to/filter-logs-grep.md) — apply quantifier patterns to real log analysis tasks
- [How-to: Use Extended Regular Expressions with grep -E](../how-to/grep-extended-regex.md) — combine `+`, `?`, brace intervals, and alternation in ERE
- [Explanation: Understanding grep and Regular Expressions](../explanation/grep-regex-explanation.md) — understand why BRE and ERE exist as separate dialects and how the matching engine interprets quantifiers
- [Reference: grep Options and Regular Expression Syntax](../reference/grep-regex-reference.md) — see the complete quantifier syntax for BRE, ERE, and PCRE side by side