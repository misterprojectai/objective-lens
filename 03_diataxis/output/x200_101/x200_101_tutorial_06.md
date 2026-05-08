---
title: "Work Efficiently with Command History and Line Editing"
type: tutorial
exam_objective: x200_101
tutorial_index: 6
version: "1.0"
status: draft
---

# Work Efficiently with Command History and Line Editing

In this tutorial, we will build the habit of recalling, editing, and reissuing commands without retyping them. Along the way, we will work with the `history` command, incremental reverse search, history expansion operators, and Bash readline shortcuts.

---

## Prerequisites

Before starting, ensure you have:

- A Bash shell prompt on an RHEL system (the `$` prompt is visible)
- Completed at least a few minutes of prior command entry so the history list is populated

---

## What We'll Build

By the end of this tutorial, you will have recalled commands by number, by string prefix, and through reverse search; edited a command on the line before running it; and cleared and navigated the line using keyboard shortcuts. The session will demonstrate this final state:

```
$ history | tail -5
   96  ls -la /etc
   97  cat /etc/hostname
   98  ls -la /etc
   99  uname -r
  100  history | tail -5
$ 
```

Every technique we practise leaves a trace in that history list — a concrete record that the session's efficiency tools are working.

---

## Step 1: Display the History List

First, we view the current history list so we have reference numbers to work with.

```bash
history
```

You should see:

```
    1  whoami
    2  ls
    3  pwd
    4  uname -r
    5  ls -la /etc
    ...
```

Notice that each line carries a number. Those numbers are what we will use in the next steps to recall specific commands without retyping them.

---

## Step 2: Recall the Most Recent Command with `!!`

Now that we have a populated history list, we use `!!` to repeat the last command we ran — in this case, `history` itself.

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

Notice that Bash prints the expanded command (`history`) on its own line before running it. This confirmation appears every time a history expansion fires, so we always see what will execute before output appears.

---

## Step 3: Recall a Command by History Number with `!n`

Now we recall a specific command by its number. We will rerun the `uname -r` entry. Look at the number beside `uname -r` in your history output — it will match your session, so substitute that number for `4` if it differs.

```bash
!4
```

You should see:

```
uname -r
5.14.0-362.el9.x86_64
```

Notice again that Bash echoes the expanded command before its output. The kernel version string that follows confirms `uname -r` ran exactly as it appeared in the history list.

---

## Step 4: Recall a Command by String Prefix with `!string`

Now we recall the most recent command that starts with a particular string. We will re-execute the most recent `ls` command from our history.

```bash
!ls
```

You should see:

```
ls -la /etc
total 1092
drwxr-xr-x. 136 root root  8192 May  7 09:14 .
dr-xr-xr-x.  17 root root   224 Apr 15 08:02 ..
-rw-r--r--.   1 root root    16 Apr 15 08:02 adjtime
...
```

Notice that `!ls` matched `ls -la /etc` — the most recent command whose text begins with `ls` — not the shorter `ls` we typed earlier. Bash always selects the most recent match.

---

## Step 5: Search History Interactively with Ctrl-R

Now we use incremental reverse search to find a command by typing part of it — without knowing its history number.

Press **Ctrl-R** at the prompt. The prompt changes to:

```
(reverse-i-search)`':
```

Type `cat`:

```
(reverse-i-search)`cat': cat /etc/hostname
```

You should see the most recent command containing `cat` appear alongside your search string. Press **Enter** to run it.

You should see:

```
cat /etc/hostname
rhel9-lab.example.com
```

Notice that we found and ran the command without typing its full text or knowing its history number. If we had wanted a different match, pressing **Ctrl-R** again while the search was active would have stepped further back through the history.

---

## Step 6: Move the Cursor to the Start and End of a Line

Now we practise cursor navigation on a long command before running it. Type the following command but **do not press Enter yet**:

```bash
ls -la /etc/sysconfig/network-scripts
```

Press **Ctrl-A** to jump the cursor to the beginning of the line.

The cursor moves to just before `ls`. You should see the prompt with the cursor repositioned:

```
$ ls -la /etc/sysconfig/network-scripts
  ^
  cursor here
```

Now press **Ctrl-E** to jump to the end of the line.

```
$ ls -la /etc/sysconfig/network-scripts
                                        ^
                                        cursor here
```

Notice that neither keystroke altered the command text — they only moved the cursor. These two shortcuts work together to let us navigate to the edit point we need quickly on any command of any length. Now press **Enter** to run the command.

You should see:

```
total 4
drwxr-xr-x. 2 root root   6 Apr 15 08:02 .
drwxr-xr-x. 7 root root 134 Apr 15 08:02 ..
```

---

## Step 7: Delete from the Cursor to the Beginning of the Line with Ctrl-U

Now we practise clearing an in-progress command. Type the following but **do not press Enter**:

```bash
ls -la /etc/sysconfig
```

Press **Ctrl-U**.

You should see the entire line disappear, returning to a clean prompt:

```
$
```

Notice that Ctrl-U discards everything from the cursor position back to the start of the line. It is the fastest way to abandon a command that we have decided not to run, without reaching for the Backspace key.

---

## Step 8: Delete the Previous Word with Ctrl-W

Now we practise removing one argument at a time. Type the following but **do not press Enter**:

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

Notice that each press of Ctrl-W removes exactly one whitespace-delimited word to the left of the cursor. This lets us correct the end of a long command without erasing everything. Press **Ctrl-U** to clear the line before the next step.

---

## Step 9: Clear the Screen with Ctrl-L

Now we clear a cluttered terminal without losing our command history.

```bash
ls -la /etc
```

You should see the long `/etc` directory listing fill the screen. Now press **Ctrl-L**.

You should see the screen clear and a fresh prompt appear at the top:

```
$
```

Notice that the history list is still intact — Ctrl-L only clears the visible display. Run `history | tail -5` to confirm:

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

---

## What We Accomplished

In this tutorial, we:

1. Displayed the numbered history list with `history`
2. Re-executed the previous command using `!!`
3. Re-executed a specific command by number using `!n`
4. Re-executed the most recent matching command using `!string`
5. Found and ran a command interactively using Ctrl-R incremental reverse search
6. Moved the cursor to the start and end of a line using Ctrl-A and Ctrl-E
7. Discarded an in-progress command using Ctrl-U
8. Deleted the previous word using Ctrl-W
9. Cleared the terminal display using Ctrl-L while preserving history

---

## Next Steps

Now that you have built efficient command-line habits, you might want to:

- [How-to: Use Command History and Keyboard Shortcuts](#) — apply these techniques in real administrative scenarios
- [Explanation: Understanding the Linux Shell and Command Syntax](#) — understand why history and readline exist as part of the shell's interactive design
- [Reference: Bash Command Syntax and Options](#) — see the complete specification of history expansion operators and readline bindings