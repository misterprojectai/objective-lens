---
title: "Control Shell Expansion and Quoting"
type: tutorial
exam_objective: x200_101
tutorial_index: 5
version: "1.0"
status: draft
---

# Control Shell Expansion and Quoting

In this tutorial, we will observe exactly what Bash does to a command line before it runs — expanding variables, globs, and command substitutions — and then take control of that process using single quotes, double quotes, and backslash escaping. Along the way, we will work with `echo`, variable assignment, wildcard patterns, and command substitution.

---

## Prerequisites

Before starting, ensure you have:

- A logged-in shell prompt on an RHEL system (either directly or via SSH)
- Completion of Tutorial 4: Navigate the Filesystem with Absolute and Relative Paths, or equivalent familiarity with moving between directories

---

## What We'll Build

By the end of this tutorial, we will have run a controlled sequence of commands that demonstrates Bash expansion in action and shows precisely how quoting suppresses it. The final verification step will produce this output:

```
--- expansion demo complete ---
unquoted variable : hello world
single-quoted     : $WORD
double-quoted     : hello world
backslash-escaped : $WORD
command sub result: today is a weekday or weekend
glob unquoted     : file1.txt file2.txt file3.txt
glob single-quoted: *.txt
```

---

## Step 1: Create a Working Directory and Practice Files

First, we create a temporary working directory and populate it with files we will use to observe glob expansion.

```bash
mkdir ~/expansion-demo
cd ~/expansion-demo
touch file1.txt file2.txt file3.txt notes.md
```

You should see:

```
(no output)
```

Confirm the files are there:

```bash
ls
```

You should see:

```
file1.txt  file2.txt  file3.txt  notes.md
```

This confirms our working directory is ready.

---

## Step 2: Observe Unquoted Variable Expansion

Now that we have a working directory, we assign a variable and let Bash expand it without any quoting.

```bash
WORD="hello world"
echo $WORD
```

You should see:

```
hello world
```

Notice that Bash replaced `$WORD` with the value `hello world` before passing anything to `echo`. The shell performed this substitution invisibly, before the command ran.

---

## Step 3: Observe Word Splitting on the Unquoted Variable

Now we see what word splitting does to an unquoted variable containing spaces.

```bash
printf '<%s>\n' $WORD
```

You should see:

```
<hello>
<world>
```

Notice that `$WORD` was split into two separate arguments — `hello` and `world` — because the space inside the value acts as a word separator when the variable is unquoted. Bash treated the two words as two distinct arguments to `printf`.

---

## Step 4: Suppress All Expansion with Single Quotes

Now we place the variable reference inside single quotes to prevent expansion entirely.

```bash
echo '$WORD'
```

You should see:

```
$WORD
```

Notice that the dollar sign and the variable name were passed to `echo` as literal characters. Single quotes preserve everything between them exactly as typed — no variable expansion, no word splitting, no interpretation of any kind.

---

## Step 5: Allow Variable Expansion Inside Double Quotes

Now we use double quotes, which allow variable expansion but protect against word splitting.

```bash
echo "$WORD"
```

You should see:

```
hello world
```

Now pass the double-quoted variable to `printf` so we can see the word-splitting difference clearly:

```bash
printf '<%s>\n' "$WORD"
```

You should see:

```
<hello world>
```

Notice that this time `printf` received the value as a single argument. Double quotes preserved the spaces inside the variable's value, preventing word splitting while still allowing Bash to expand `$WORD`.

---

## Step 6: Escape a Single Character with a Backslash

Now we use a backslash to suppress the special meaning of just one character at a time.

```bash
echo \$WORD
```

You should see:

```
$WORD
```

Notice that the backslash cancelled the special meaning of the `$` immediately following it. Bash treated `$WORD` as a literal string, exactly as single quotes would — but for a single character rather than an entire span of text.

---

## Step 7: Observe Command Substitution

Now we use command substitution, which lets Bash run a command and insert its output into the command line.

```bash
echo "today is $(date +%A)"
```

You should see output resembling:

```
today is Tuesday
```

The day name will match whichever day you run this. Notice that `$(date +%A)` was replaced by the output of the `date` command before `echo` received anything. Command substitution happens inside double quotes — double quotes suppress word splitting and glob expansion but leave `$()` and `$` active.

---

## Step 8: Observe Glob Expansion Unquoted

Now we observe how Bash expands a wildcard pattern when it is unquoted.

```bash
echo *.txt
```

You should see:

```
file1.txt file2.txt file3.txt
```

Notice that Bash replaced `*.txt` with the names of all matching files before passing them to `echo`. The shell performed this glob expansion — not the `echo` command itself.

---

## Step 9: Suppress Glob Expansion with Single Quotes

Now we prevent glob expansion by placing the pattern inside single quotes.

```bash
echo '*.txt'
```

You should see:

```
*.txt
```

Notice that the asterisk was passed as a literal character. Single quotes completely disabled glob expansion, just as they disabled variable expansion in Step 4.

---

## Step 10: Verify the Complete Demonstration

Finally, we run a single summary command that collects all the results we have produced into one readable block, confirming everything works as expected.

```bash
printf '%s\n' \
  "--- expansion demo complete ---" \
  "unquoted variable : $WORD" \
  'single-quoted     : $WORD' \
  "double-quoted     : $WORD" \
  "backslash-escaped : \$WORD" \
  "command sub result: today is $(date +%A | sed 's/Saturday\|Sunday/a weekend day/;t;s/.*/a weekday/')" \
  "glob unquoted     : $(echo *.txt)" \
  'glob single-quoted: *.txt'
```

You should see:

```
--- expansion demo complete ---
unquoted variable : hello world
single-quoted     : $WORD
double-quoted     : hello world
backslash-escaped : $WORD
command sub result: today is a weekday or weekend
glob unquoted     : file1.txt file2.txt file3.txt
glob single-quoted: *.txt
```

The day classification in your output will reflect the actual day you ran the tutorial.

---

## What We Accomplished

In this tutorial, we:

1. Created practice files to serve as glob expansion targets
2. Assigned a variable and observed Bash expand it before command execution
3. Observed word splitting split a space-containing value into separate arguments
4. Suppressed all expansion using single quotes and confirmed literal output
5. Used double quotes to allow variable expansion while preventing word splitting
6. Escaped a single character with a backslash to suppress its special meaning
7. Observed command substitution replace `$()` with live command output inside double quotes
8. Observed glob expansion replace `*.txt` with matching filenames
9. Suppressed glob expansion with single quotes and confirmed literal output
10. Verified all expansion behaviours in a single summary output

---

## Next Steps

Now that you have seen Bash expansion and quoting in action, you might want to:

- [How-to: Quote arguments correctly to prevent word splitting errors](#) — apply these quoting rules in real administrative commands
- [How-to: Use command substitution to build dynamic commands](#) — practical patterns for capturing command output in variables and arguments
- [Explanation: Understanding the Linux Shell and Command Syntax](#) — the full conceptual model behind why Bash expansion works the way it does
- [Reference: Bash Command Syntax and Options](#) — complete specification of quoting rules, expansion types, and special characters