---
description: Learn to control Bash shell expansion and quoting by observing how variables, globs, and command substitutions are processed — then suppressing them with single quotes, double quotes, and backslash escaping.
icon: graduation-cap
---

# Control Shell Expansion and Quoting

{% hint style="info" %}
**Prerequisites**

- A logged-in shell prompt on an RHEL system (either directly or via SSH)
- Completion of Tutorial 4: Navigate the Filesystem with Absolute and Relative Paths, or equivalent familiarity with moving between directories
{% endhint %}

By the end of this tutorial, you will have run a controlled sequence of commands that demonstrates Bash expansion in action and shows precisely how quoting suppresses it. The final verification step will produce this output as shown in the final step.

{% stepper %}
{% step %}
### Create a Working Directory and Practice Files

Create a temporary working directory and populate it with files to use as glob expansion targets.

```bash
mkdir ~/expansion-demo
cd ~/expansion-demo
touch file1.txt file2.txt file3.txt notes.md
```

Confirm the files are present:

```bash
ls
```

{% hint style="success" %}
**Expected output**

```
file1.txt  file2.txt  file3.txt  notes.md
```

Your working directory is ready.
{% endhint %}
{% endstep %}

{% step %}
### Observe Unquoted Variable Expansion

Assign a variable and let Bash expand it without any quoting.

```bash
WORD="hello world"
echo $WORD
```

{% hint style="success" %}
**Expected output**

```
hello world
```

Bash replaced `$WORD` with the value `hello world` before passing anything to `echo`. The shell performed this substitution invisibly, before the command ran.
{% endhint %}
{% endstep %}

{% step %}
### Observe Word Splitting on the Unquoted Variable

Pass the unquoted variable to `printf` to see what word splitting does to a value containing spaces.

```bash
printf '<%s>\n' $WORD
```

{% hint style="success" %}
**Expected output**

```
<hello>
<world>
```

`$WORD` was split into two separate arguments — `hello` and `world` — because the space inside the value acts as a word separator when the variable is unquoted. Bash treated the two words as two distinct arguments to `printf`.
{% endhint %}
{% endstep %}

{% step %}
### Suppress All Expansion with Single Quotes

Place the variable reference inside single quotes to prevent expansion entirely.

```bash
echo '$WORD'
```

{% hint style="success" %}
**Expected output**

```
$WORD
```

The dollar sign and the variable name were passed to `echo` as literal characters. Single quotes preserve everything between them exactly as typed — no variable expansion, no word splitting, no interpretation of any kind.
{% endhint %}
{% endstep %}

{% step %}
### Allow Variable Expansion Inside Double Quotes

Use double quotes, which allow variable expansion but protect against word splitting.

```bash
echo "$WORD"
```

{% hint style="success" %}
**Expected output**

```
hello world
```
{% endhint %}

Now pass the double-quoted variable to `printf` to see the word-splitting difference clearly:

```bash
printf '<%s>\n' "$WORD"
```

{% hint style="success" %}
**Expected output**

```
<hello world>
```

This time `printf` received the value as a single argument. Double quotes preserved the spaces inside the variable's value, preventing word splitting while still allowing Bash to expand `$WORD`.
{% endhint %}
{% endstep %}

{% step %}
### Escape a Single Character with a Backslash

Use a backslash to suppress the special meaning of just one character at a time.

```bash
echo \$WORD
```

{% hint style="success" %}
**Expected output**

```
$WORD
```

The backslash cancelled the special meaning of the `$` immediately following it. Bash treated `$WORD` as a literal string — exactly as single quotes would — but for a single character rather than an entire span of text.
{% endhint %}

{% hint style="warning" %}
The backslash only escapes the single character immediately following it. To escape multiple special characters, you must prefix each one individually, or use single quotes instead.
{% endhint %}
{% endstep %}

{% step %}
### Observe Command Substitution

Use command substitution to let Bash run a command and insert its output into the command line.

```bash
echo "today is $(date +%A)"
```

{% hint style="success" %}
**Expected output** (day name will match whichever day you run this)

```
today is Tuesday
```

`$(date +%A)` was replaced by the output of the `date` command before `echo` received anything. Command substitution happens inside double quotes — double quotes suppress word splitting and glob expansion but leave `$()` and `$` active.
{% endhint %}
{% endstep %}

{% step %}
### Observe Glob Expansion Unquoted

Pass an unquoted wildcard pattern to `echo` to observe how Bash expands it.

```bash
echo *.txt
```

{% hint style="success" %}
**Expected output**

```
file1.txt file2.txt file3.txt
```

Bash replaced `*.txt` with the names of all matching files before passing them to `echo`. The shell performed this glob expansion — not the `echo` command itself.
{% endhint %}
{% endstep %}

{% step %}
### Suppress Glob Expansion with Single Quotes

Place the wildcard pattern inside single quotes to prevent glob expansion.

```bash
echo '*.txt'
```

{% hint style="success" %}
**Expected output**

```
*.txt
```

The asterisk was passed as a literal character. Single quotes completely disabled glob expansion, just as they disabled variable expansion in the earlier step.
{% endhint %}
{% endstep %}

{% step %}
### Verify the Complete Demonstration

Run a single summary command that collects all the results into one readable block, confirming everything works as expected.

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

{% hint style="warning" %}
This command uses line continuations (`\`). The backslash must be the very last character on each continued line — no trailing space after it — or Bash will report a syntax error.
{% endhint %}

{% hint style="success" %}
**Expected output**

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
{% endhint %}
{% endstep %}
{% endstepper %}

{% hint style="success" %}
**Tutorial complete.** In this tutorial, you:

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
{% endhint %}

## Next Steps

- [How-to: Quote arguments correctly to prevent word splitting errors](#) — apply these quoting rules in real administrative commands
- [How-to: Use command substitution to build dynamic commands](#) — practical patterns for capturing command output in variables and arguments
- [Explanation: Understanding the Linux Shell and Command Syntax](#) — the full conceptual model behind why Bash expansion works the way it does
- [Reference: Bash Command Syntax and Options](#) — complete specification of quoting rules, expansion types, and special characters

