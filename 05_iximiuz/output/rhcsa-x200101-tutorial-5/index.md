---
kind: tutorial

title: Control Shell Expansion and Quoting

description: |
  Master Bash expansion and quoting on Rocky Linux 9. Observe how the shell
  expands variables, globs, and command substitutions before running commands —
  then take control using single quotes, double quotes, and backslash escaping.
  Essential knowledge for the RHCSA EX200 exam.

categories:
  - linux

tagz:
  - rhcsa
  - bash
  - shell
  - redirection
  - grep

createdAt: 2025-01-15
updatedAt: 2025-01-15

cover: __static__/cover.png

playground:
  name: rockylinux
  machines:
    - name: rocky-01
      resources:
        cpuCount: 2
        ramSize: 2Gi

tasks:
  init_history_flush:
    init: true
    machine: rocky-01
    user: laborant
    run: |
      echo 'PROMPT_COMMAND="history -a; $PROMPT_COMMAND"' >> /home/laborant/.bashrc
      chown laborant:laborant /home/laborant/.bashrc

  verify_working_dir:
    machine: rocky-01
    user: laborant
    run: |
      grep -q 'mkdir ~/expansion-demo' /home/laborant/.bash_history && \
      grep -q 'cd ~/expansion-demo' /home/laborant/.bash_history && \
      test -d /home/laborant/expansion-demo && \
      test -f /home/laborant/expansion-demo/file1.txt && \
      test -f /home/laborant/expansion-demo/file2.txt && \
      test -f /home/laborant/expansion-demo/file3.txt && \
      exit 0 || exit 1
    hintcheck: |
      echo "Run: mkdir ~/expansion-demo && cd ~/expansion-demo && touch file1.txt file2.txt file3.txt notes.md"

  verify_unquoted_variable:
    machine: rocky-01
    user: laborant
    run: |
      grep -qP 'WORD=.hello world.' /home/laborant/.bash_history && \
      grep -q 'echo $WORD' /home/laborant/.bash_history && \
      exit 0 || exit 1
    hintcheck: |
      echo 'Run: WORD="hello world" then echo $WORD'

  verify_word_splitting:
    machine: rocky-01
    user: laborant
    run: |
      grep -q "printf '<%s>\\\\n' \$WORD" /home/laborant/.bash_history && \
      exit 0 || exit 1
    hintcheck: |
      echo "Run: printf '<%s>\n' \$WORD"

  verify_single_quotes:
    machine: rocky-01
    user: laborant
    run: |
      grep -q "echo '\$WORD'" /home/laborant/.bash_history && \
      exit 0 || exit 1
    hintcheck: |
      echo "Run: echo '\$WORD'"

  verify_double_quotes:
    machine: rocky-01
    user: laborant
    run: |
      grep -q 'echo "\$WORD"' /home/laborant/.bash_history && \
      grep -q "printf '<%s>\\\\n' \"\$WORD\"" /home/laborant/.bash_history && \
      exit 0 || exit 1
    hintcheck: |
      echo 'Run: echo "$WORD" then printf '\''<%s>\n'\'' "$WORD"'

  verify_backslash:
    machine: rocky-01
    user: laborant
    run: |
      grep -q 'echo \\\$WORD' /home/laborant/.bash_history && \
      exit 0 || exit 1
    hintcheck: |
      echo 'Run: echo \$WORD'

  verify_command_sub:
    machine: rocky-01
    user: laborant
    run: |
      grep -qP 'echo "today is \$\(date' /home/laborant/.bash_history && \
      exit 0 || exit 1
    hintcheck: |
      echo 'Run: echo "today is $(date +%A)"'

  verify_glob_unquoted:
    machine: rocky-01
    user: laborant
    run: |
      grep -q 'echo \*.txt' /home/laborant/.bash_history && \
      exit 0 || exit 1
    hintcheck: |
      echo 'Run: echo *.txt  (from inside ~/expansion-demo)'

  verify_glob_quoted:
    machine: rocky-01
    user: laborant
    run: |
      grep -q "echo '\*.txt'" /home/laborant/.bash_history && \
      exit 0 || exit 1
    hintcheck: |
      echo "Run: echo '*.txt'"

  verify_summary:
    machine: rocky-01
    user: laborant
    run: |
      grep -q 'expansion demo complete' /home/laborant/.bash_history && \
      exit 0 || exit 1
    hintcheck: |
      echo "Run the printf summary block from Step 10."
---

# Control Shell Expansion and Quoting

::remark-box
---
kind: info
---
**Before running any commands:** click the **+** button in the terminal tab bar to open a new terminal tab. The playground history tracking activates in new sessions only. Commands run in the original tab will not register for task verification.
::

In this tutorial, we observe exactly what Bash does to a command line **before** it runs — expanding variables, globs, and command substitutions — and then take control of that process using single quotes, double quotes, and backslash escaping.

Understanding this is non-negotiable for the RHCSA exam. Misquoting a variable in a script or a `find` command is a silent, hard-to-debug error. After this tutorial, you will see what the shell sees.

---

## What We'll Build

By the end, a single summary command will produce this output:

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

Every line proves a different quoting behaviour. Let's build it step by step.

---

## Step 1 — Create a Working Directory and Practice Files

We need a controlled directory so glob patterns match only what we expect.

```bash
mkdir ~/expansion-demo
cd ~/expansion-demo
touch file1.txt file2.txt file3.txt notes.md
```

Confirm the files exist:

```bash
ls
```

Expected output:

```
file1.txt  file2.txt  file3.txt  notes.md
```

::remark-box
---
kind: info
---
All glob steps in this tutorial **must be run from inside `~/expansion-demo`**. If you open a new terminal tab mid-tutorial, `cd ~/expansion-demo` before continuing.
::

::simple-task
---
:tasks: tasks
:name: verify_working_dir
---
#active
Create `~/expansion-demo` and run `touch file1.txt file2.txt file3.txt notes.md` inside it.

#completed
Working directory confirmed — all three `.txt` files are present ✓
::

---

## Step 2 — Observe Unquoted Variable Expansion

Assign a variable whose value contains a space, then let Bash expand it unquoted.

```bash
WORD="hello world"
echo $WORD
```

Expected output:

```
hello world
```

Bash replaced `$WORD` with `hello world` **before** passing anything to `echo`. The substitution happened invisibly, at the shell level.

::hint-box
---
:summary: Variable assignment produced no output — is that normal?
---
Yes. Variable assignment (`VAR=value`) is silent by design. Only the subsequent `echo $WORD` produces output. If you see `-bash: WORD=hello world: command not found`, you accidentally added a space before the `=` sign. Run `WORD="hello world"` (no spaces around `=`).
::

::simple-task
---
:tasks: tasks
:name: verify_unquoted_variable
---
#active
Run `WORD="hello world"` then `echo $WORD`.

#completed
Variable assignment and unquoted expansion confirmed ✓
::

---

## Step 3 — Observe Word Splitting on an Unquoted Variable

Word splitting is what happens when Bash breaks an unquoted expansion on whitespace. Run this from **inside `~/expansion-demo`**:

```bash
printf '<%s>\n' $WORD
```

Expected output:

```
<hello>
<world>
```

`$WORD` expanded to `hello world`, then Bash split that on the space, producing **two separate arguments** to `printf`. This is word splitting in action.

::remark-box
---
kind: warning
---
Word splitting is a common source of bugs in shell scripts. When a variable might contain spaces, **always quote it** unless you explicitly want splitting. On the RHCSA exam, unquoted variables in paths or filenames will silently produce wrong results.
::

::simple-task
---
:tasks: tasks
:name: verify_word_splitting
---
#active
Run `printf '<%s>\n' $WORD` and observe that `hello` and `world` are separate arguments.

#completed
Word splitting demonstrated successfully ✓
::

---

## Step 4 — Suppress All Expansion with Single Quotes

Single quotes are the bluntest quoting tool: everything between them is treated as literal text.

```bash
echo '$WORD'
```

Expected output:

```
$WORD
```

The dollar sign and the variable name were passed to `echo` unchanged. No expansion, no word splitting, no interpretation of any kind.

::details-box
---
:summary: Can I put a single quote inside single quotes?
---
No — there is no escape sequence inside single quotes. The moment Bash sees the closing `'`, the quoted span ends. The workaround is to end the single-quoted span, escape a literal `'` with a backslash, then reopen: `'it'\''s fine'`. This is rarely needed in practice but good to know for scripts that build command strings.
::

::simple-task
---
:tasks: tasks
:name: verify_single_quotes
---
#active
Run `echo '$WORD'` and confirm the output is the literal string `$WORD`.

#completed
Single-quote suppression confirmed ✓
::

---

## Step 5 — Allow Variable Expansion Inside Double Quotes

Double quotes suppress word splitting and glob expansion, but they **still allow** variable expansion and command substitution.

```bash
echo "$WORD"
```

Expected output:

```
hello world
```

Now pass the double-quoted variable to `printf` to compare with Step 3:

```bash
printf '<%s>\n' "$WORD"
```

Expected output:

```
<hello world>
```

`printf` received the value as **one argument** this time. The double quotes preserved the space inside `$WORD`, preventing word splitting while still expanding the variable.

::remark-box
---
kind: info
---
The rule of thumb most RHCSA candidates adopt: **quote every variable with double quotes unless you have a specific reason not to.** This prevents word splitting and glob expansion from producing unexpected results, while still letting variable values through.
::

::simple-task
---
:tasks: tasks
:name: verify_double_quotes
---
#active
Run `echo "$WORD"` then `printf '<%s>\n' "$WORD"` and observe the difference from Step 3.

#completed
Double-quote behaviour confirmed ✓
::

---

## Step 6 — Escape a Single Character with a Backslash

A backslash cancels the special meaning of the **one character** that immediately follows it — a surgical alternative to quoting an entire span.

```bash
echo \$WORD
```

Expected output:

```
$WORD
```

The backslash stripped the special meaning from `$`, so `$WORD` was passed to `echo` as a literal string — same result as single quotes in Step 4, but applied to a single character rather than a span.

::hint-box
---
:summary: The backslash itself disappeared from the output — why?
---
The backslash is a **quoting character**, not a printable character in this context. Bash consumes it during its quoting pass and does not pass it to the command. To print a literal backslash, escape it: `echo \\`.
::

::simple-task
---
:tasks: tasks
:name: verify_backslash
---
#active
Run `echo \$WORD` and confirm the output is the literal string `$WORD`.

#completed
Backslash escaping confirmed ✓
::

---

## Step 7 — Observe Command Substitution

Command substitution — `$(command)` — tells Bash to run a command and insert its standard output into the command line at that position.

```bash
echo "today is $(date +%A)"
```

Expected output (day name varies):

```
today is Tuesday
```

`$(date +%A)` was replaced by the output of the `date` command before `echo` received anything. Notice this happened **inside double quotes** — double quotes suppress word splitting and globs, but they leave `$()` and `$` active.

::simple-task
---
:tasks: tasks
:name: verify_command_sub
---
#active
Run `echo "today is $(date +%A)"` and observe the current day name in the output.

#completed
Command substitution confirmed ✓
::

---

## Step 8 — Observe Glob Expansion Unquoted

Make sure you are still inside `~/expansion-demo`:

```bash
echo *.txt
```

Expected output:

```
file1.txt file2.txt file3.txt
```

Bash replaced `*.txt` with the names of all matching files before passing them to `echo`. The `echo` command never saw the asterisk — only the expanded filenames.

::remark-box
---
kind: warning
---
If no files match an unquoted glob, Bash's default behaviour (on Rocky Linux 9) is to pass the literal pattern to the command. This can cause confusing errors. The `nullglob` shell option changes this behaviour — but that is beyond today's scope.
::

::simple-task
---
:tasks: tasks
:name: verify_glob_unquoted
---
#active
Run `echo *.txt` from inside `~/expansion-demo` and observe the three filenames in the output.

#completed
Unquoted glob expansion confirmed ✓
::

---

## Step 9 — Suppress Glob Expansion with Single Quotes

```bash
echo '*.txt'
```

Expected output:

```
*.txt
```

The asterisk was passed as a literal character. Single quotes disabled glob expansion just as they disabled variable expansion in Step 4.

::simple-task
---
:tasks: tasks
:name: verify_glob_quoted
---
#active
Run `echo '*.txt'` and confirm the output is the literal string `*.txt`.

#completed
Quoted glob suppression confirmed ✓
::

---

## Step 10 — Verify the Complete Demonstration

Run this single summary command that collects all the results into one readable block. Make sure you are inside `~/expansion-demo` and that `$WORD` is still set:

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

Expected output:

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

::hint-box
---
:summary: I see 'hello world' for the backslash-escaped line, not '$WORD'
---
Check whether you copied the command exactly. The key part is `"backslash-escaped : \$WORD"` — inside double quotes, `\$` escapes the dollar sign, producing a literal `$WORD` in the output. If you used single quotes for that argument you'd get the same result, but the whole point is demonstrating the backslash inside double quotes.
::

::hint-box
---
:summary: $WORD is blank or missing
---
The variable `WORD` is only set for your current shell session. If you opened a new terminal tab, you must reassign it: `WORD="hello world"`. Shell variables do not persist across sessions unless exported to the environment (with `export`) or set in a startup file like `.bashrc`.
::

::simple-task
---
:tasks: tasks
:name: verify_summary
---
#active
Run the `printf` summary block above and confirm all eight output lines appear correctly.

#completed
Complete expansion demonstration verified — all quoting behaviours confirmed ✓
::

---

## What We Accomplished

In this tutorial, we:

1. Created practice files to serve as glob expansion targets
2. Assigned a variable and observed Bash expand it before command execution
3. Observed word splitting break a space-containing value into separate arguments
4. Suppressed all expansion using single quotes and confirmed literal output
5. Used double quotes to allow variable expansion while preventing word splitting
6. Escaped a single character with a backslash to suppress its special meaning
7. Observed command substitution replace `$()` with live command output inside double quotes
8. Observed glob expansion replace `*.txt` with matching filenames
9. Suppressed glob expansion with single quotes and confirmed literal output
10. Verified all expansion behaviours in a single summary output

::remark-box
---
kind: info
---
**RHCSA exam insight:** Quoting errors are among the most common causes of silent failures in shell scripts and one-liners. The exam will test you on commands where an unquoted variable or glob produces wrong results. When in doubt: double-quote variables (`"$VAR"`), single-quote literals (`'pattern'`), and backslash-escape individual special characters (`\$`).
::

---

## Next Steps

- **Apply these rules in practice** — try using `find`, `grep`, and `sed` with quoted and unquoted patterns to see how quoting affects those commands on real system files
- **Explore `set -x`** — run `set -x` before a command sequence to see exactly how Bash expands each word before execution; run `set +x` to turn it off
- **Learn about `export`** — variables set in one shell session are lost when the session ends; `export WORD="hello world"` makes the variable available to child processes
```