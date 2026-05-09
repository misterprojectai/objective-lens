---
kind: tutorial

title: "Work Efficiently with Command History and Line Editing"

description: |
  Master Bash command history and readline shortcuts on Rocky Linux 9.
  Learn to recall, search, and edit commands using !!, !n, !string, Ctrl-R,
  Ctrl-A/E, Ctrl-U/W, and Ctrl-L — essential efficiency skills for the RHCSA EX200 exam.

categories:
  - linux

tagz:
  - rhcsa
  - bash
  - history
  - shell
  - readline

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

  init_seed_history:
    init: true
    machine: rocky-01
    user: laborant
    needs:
      - init_history_flush
    run: |
      su - laborant -c 'bash -i -c "
        history -r
        HISTFILE=/home/laborant/.bash_history
        history -s whoami
        history -s ls
        history -s pwd
        history -s \"uname -r\"
        history -s \"ls -la /etc\"
        history -s \"cat /etc/hostname\"
        history -s \"ls -la /etc\"
        history -w
      "'

  verify_history_displayed:
    machine: rocky-01
    user: laborant
    run: |
      grep -q 'history' /home/laborant/.bash_history && exit 0 || exit 1
    hintcheck: |
      echo "Run the 'history' command to display the numbered history list."

  verify_bangbang_used:
    machine: rocky-01
    user: laborant
    run: |
      grep -q '^!!' /home/laborant/.bash_history && exit 0 || exit 1
    hintcheck: |
      echo "Type !! and press Enter to repeat the last command."

  verify_bang_number_used:
    machine: rocky-01
    user: laborant
    run: |
      grep -qE '^![0-9]+' /home/laborant/.bash_history && exit 0 || exit 1
    hintcheck: |
      echo "Run a command by history number, e.g. !4 (use the number beside 'uname -r' in your history list)."

  verify_bang_string_used:
    machine: rocky-01
    user: laborant
    run: |
      grep -qE '^!ls' /home/laborant/.bash_history && exit 0 || exit 1
    hintcheck: |
      echo "Use !ls to re-execute the most recent command starting with 'ls'."

  verify_ctrl_a_e_command:
    machine: rocky-01
    user: laborant
    run: |
      grep -q 'ls -la /etc/sysconfig/network-scripts' /home/laborant/.bash_history && exit 0 || exit 1
    hintcheck: |
      echo "Type 'ls -la /etc/sysconfig/network-scripts', practice Ctrl-A and Ctrl-E, then press Enter to run it."

  verify_ctrl_l_history_tail:
    machine: rocky-01
    user: laborant
    run: |
      grep -qE 'history.*tail' /home/laborant/.bash_history && exit 0 || exit 1
    hintcheck: |
      echo "Run: history | tail -5"
---

# Work Efficiently with Command History and Line Editing

In this tutorial, you will build the habit of recalling, editing, and reissuing commands without retyping them. You will work with the `history` command, incremental reverse search, history expansion operators, and Bash readline shortcuts — all of which are tested on the RHCSA EX200 exam.

::remark-box
---
kind: info
---
**Before running any commands:** click the **+** button in the terminal tab bar to open a new terminal tab. The playground history tracking activates in new sessions only. Commands run in the original tab will not register for task verification.
::

---

## What We'll Build

By the end of this tutorial, you will have recalled commands by number, by string prefix, and through reverse search; edited a command on the line before running it; and cleared and navigated the line using keyboard shortcuts. The session will reach this final state:

```
$ history | tail -5
   96  ls -la /etc
   97  cat /etc/hostname
   98  ls -la /etc
   99  uname -r
  100  history | tail -5
```

Every technique leaves a trace in the history list — a concrete record that the shell's efficiency tools are working.

---

## Step 1: Display the History List

View the current history list so you have reference numbers to work with.

```bash
history
```

You should see output similar to:

```
    1  whoami
    2  ls
    3  pwd
    4  uname -r
    5  ls -la /etc
    6  cat /etc/hostname
    7  ls -la /etc
```

Each line carries a number. Those numbers are what you will use in the next steps to recall specific commands without retyping them.

::remark-box
---
kind: info
---
**Exam tip:** The `history` command is your starting point whenever you need to recall what you ran in a session. On the exam, you will frequently need to re-run slightly modified versions of earlier commands — knowing the number saves retyping.
::

::simple-task
---
:tasks: tasks
:name: verify_history_displayed
---
#active
Run `history` to display the numbered command history list.

#completed
History displayed — you can see the numbered list 🎉
::

---

## Step 2: Recall the Most Recent Command with `!!`

Use `!!` to repeat the last command you ran — in this case, `history` itself.

```bash
!!
```

You should see:

```
history
    1  whoami
    2  ls
    3  pwd
    4  uname -r
    5  ls -la /etc
    ...
```

Bash prints the expanded command (`history`) on its own line before running it. This confirmation appears every time a history expansion fires, so you always see what will execute before output appears.

::remark-box
---
kind: warning
---
**Never use `!!` with `sudo` without checking first.** Running `sudo !!` re-executes the previous command with root privileges. Make sure you know what that previous command was before doing so.
::

::simple-task
---
:tasks: tasks
:name: verify_bangbang_used
---
#active
Type `!!` and press **Enter** to repeat the most recent command.

#completed
`!!` executed — history expansion is working 🎉
::

---

## Step 3: Recall a Command by History Number with `!n`

Recall a specific command by its number. You will rerun the `uname -r` entry. Look at the number beside `uname -r` in your history output — substitute that number for `4` if it differs in your session.

```bash
!4
```

You should see:

```
uname -r
5.14.0-362.el9.x86_64
```

Bash echoes the expanded command before its output. The kernel version string confirms `uname -r` ran exactly as it appeared in the history list.

::details-box
---
:summary: "How Bash finds the command number"
---
History numbers are assigned sequentially from the start of the shell session (or from where `HISTFILE` was last read). The number beside each entry in `history` output is the one you pass to `!n`. Numbers are stable within a session but reset when you start a new shell.
::

::simple-task
---
:tasks: tasks
:name: verify_bang_number_used
---
#active
Use `!n` (replacing `n` with the number beside `uname -r` in your history) to re-execute that command.

#completed
`!n` expansion worked — you recalled a command by number 🎉
::

---

## Step 4: Recall a Command by String Prefix with `!string`

Recall the most recent command that starts with a particular string. You will re-execute the most recent `ls` command from your history.

```bash
!ls
```

You should see:

```
ls -la /etc
total 1092
drwxr-xr-x. 136 root root  8192 May  7 09:14 .
...
```

`!ls` matched `ls -la /etc` — the most recent command whose text begins with `ls` — not the shorter `ls` typed earlier. Bash always selects the most recent match.

::remark-box
---
kind: warning
---
**`!string` runs without confirmation.** Unlike recalling a command and editing it, `!string` executes immediately. Double-check that the most recent matching command is the one you intend to run.
::

::simple-task
---
:tasks: tasks
:name: verify_bang_string_used
---
#active
Type `!ls` and press **Enter** to re-execute the most recent command beginning with `ls`.

#completed
`!ls` matched and ran — string prefix expansion is working 🎉
::

---

## Step 5: Search History Interactively with Ctrl-R

Use incremental reverse search to find a command by typing part of it — without knowing its history number.

Press **Ctrl-R** at the prompt. The prompt changes to:

```
(reverse-i-search)`':
```

Type `cat`:

```
(reverse-i-search)`cat': cat /etc/hostname
```

The most recent command containing `cat` appears alongside your search string. Press **Enter** to run it.

You should see:

```
cat /etc/hostname
rocky-01
```

You found and ran the command without typing its full text or knowing its history number.

::details-box
---
:summary: "Navigating multiple matches with Ctrl-R"
---
While the reverse-search prompt is active:

- Press **Ctrl-R** again to step further back through older matches.
- Press **Ctrl-G** or **Escape** to cancel the search and return to the normal prompt with the current search text pre-filled.
- Press **Ctrl-C** to cancel completely.

If you overshoot, **Ctrl-S** moves forward through matches (you may need to run `stty -ixon` first to unfreeze forward search on some terminals).
::

---

## Step 6: Move the Cursor to the Start and End of a Line

Practice cursor navigation on a long command before running it. Type the following command but **do not press Enter yet**:

```bash
ls -la /etc/sysconfig/network-scripts
```

Press **Ctrl-A** to jump the cursor to the beginning of the line.

The cursor moves to just before `ls`:

```
$ ls -la /etc/sysconfig/network-scripts
  ^
  cursor here
```

Now press **Ctrl-E** to jump to the end of the line:

```
$ ls -la /etc/sysconfig/network-scripts
                                        ^
                                        cursor here
```

Neither keystroke altered the command text — they only moved the cursor. These two shortcuts let you navigate to any edit point quickly, regardless of command length. Now press **Enter** to run the command.

You should see:

```
total 4
drwxr-xr-x. 2 root root   6 Apr 15 08:02 .
drwxr-xr-x. 7 root root 134 Apr 15 08:02 ..
```

::remark-box
---
kind: info
---
**Exam tip:** Ctrl-A and Ctrl-E are faster than holding the arrow keys across a 60-character path. Use them every time you need to prepend `sudo` to a command or correct a typo at the start of a long line.
::

::simple-task
---
:tasks: tasks
:name: verify_ctrl_a_e_command
---
#active
Type `ls -la /etc/sysconfig/network-scripts`, practice **Ctrl-A** and **Ctrl-E** to move the cursor, then press **Enter** to run it.

#completed
Command executed — cursor navigation practised successfully 🎉
::

---

## Step 7: Delete from the Cursor to the Beginning of the Line with Ctrl-U

Practice clearing an in-progress command. Type the following but **do not press Enter**:

```bash
ls -la /etc/sysconfig
```

Press **Ctrl-U**.

The entire line disappears, returning to a clean prompt:

```
$
```

Ctrl-U discards everything from the cursor position back to the start of the line. It is the fastest way to abandon a command you have decided not to run, without reaching for the Backspace key repeatedly.

::remark-box
---
kind: info
---
**Ctrl-U vs Ctrl-C:** Ctrl-U clears only the typed-but-not-yet-submitted text. Ctrl-C cancels the entire line and also kills a running command. Use Ctrl-U when you want to start fresh on the same prompt without submitting anything.
::

---

## Step 8: Delete the Previous Word with Ctrl-W

Practice removing one argument at a time. Type the following but **do not press Enter**:

```bash
ls -la /etc/hostname
```

Press **Ctrl-W**.

You should see:

```
$ ls -la 
```

The argument `/etc/hostname` is gone, but `ls -la ` remains. Press **Ctrl-W** again.

You should see:

```
$ ls 
```

Each press of Ctrl-W removes exactly one whitespace-delimited word to the left of the cursor. This lets you correct the end of a long command without erasing everything. Press **Ctrl-U** to clear the line before the next step.

::details-box
---
:summary: "Ctrl-W vs Alt-Backspace — what counts as a 'word'?"
---
`Ctrl-W` treats any sequence of non-whitespace characters as a word, delimited by spaces. `Alt-Backspace` is readline's "backward-kill-word" and uses a slightly different word boundary definition that respects characters like `/` and `-`. For paths like `/etc/sysconfig/network-scripts`, `Alt-Backspace` stops at each `/`, while `Ctrl-W` removes the whole path at once.
::

---

## Step 9: Clear the Screen with Ctrl-L

Clear a cluttered terminal without losing your command history. First, produce some output to fill the screen:

```bash
ls -la /etc
```

The long `/etc` directory listing fills the screen. Now press **Ctrl-L**.

The screen clears and a fresh prompt appears at the top:

```
$
```

The history list is still intact — Ctrl-L only clears the visible display. Confirm this by running:

```bash
history | tail -5
```

You should see output similar to:

```
   96  ls -la /etc
   97  cat /etc/hostname
   98  ls -la /etc
   99  uname -r
  100  history | tail -5
```

This matches the final state shown in **What We'll Build**.

::simple-task
---
:tasks: tasks
:name: verify_ctrl_l_history_tail
---
#active
Run `ls -la /etc`, press **Ctrl-L** to clear the screen, then run `history | tail -5` to confirm history is intact.

#completed
Screen cleared and history confirmed — Ctrl-L works as expected 🎉
::

---

## Keyboard Shortcuts Reference

| Shortcut | Action |
|----------|--------|
| `!!` | Re-execute the previous command |
| `!n` | Re-execute command number *n* |
| `!string` | Re-execute most recent command starting with *string* |
| **Ctrl-R** | Incremental reverse history search |
| **Ctrl-A** | Move cursor to start of line |
| **Ctrl-E** | Move cursor to end of line |
| **Ctrl-U** | Delete from cursor to start of line |
| **Ctrl-W** | Delete the previous word |
| **Ctrl-L** | Clear the terminal screen |

---

## What We Accomplished

In this tutorial, you:

1. Displayed the numbered history list with `history`
2. Re-executed the previous command using `!!`
3. Re-executed a specific command by number using `!n`
4. Re-executed the most recent matching command using `!string`
5. Found and ran a command interactively using **Ctrl-R** incremental reverse search
6. Moved the cursor to the start and end of a line using **Ctrl-A** and **Ctrl-E**
7. Discarded an in-progress command using **Ctrl-U**
8. Deleted the previous word using **Ctrl-W**
9. Cleared the terminal display using **Ctrl-L** while preserving history

::remark-box
---
kind: info
---
**RHCSA exam reminder:** The exam is timed. Mastering these shortcuts is not optional — they are the difference between finishing with time to spare and running out of time. Practice until `!!`, `!string`, and **Ctrl-R** are muscle memory.
::
```