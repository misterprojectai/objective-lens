---
description: Recall, edit, and reissue Bash commands without retyping them using history expansion, reverse search, and readline keyboard shortcuts.
icon: graduation-cap
---

# Work Efficiently with Command History and Line Editing

{% hint style="info" %}
**Before you start, you need:**
- A Bash shell prompt on an RHEL system (the `$` prompt is visible)
- At least a few minutes of prior command entry so the history list is populated
{% endhint %}

By the end of this tutorial, you will have recalled commands by number, by string prefix, and through reverse search; edited a command on the line before running it; and cleared and navigated the line using keyboard shortcuts. The session will demonstrate this final state:

```bash
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

{% stepper %}
{% step %}
### Display the History List

View the current history list to get the reference numbers you will use in later steps.

```bash
history
```

{% code title="Output" %}
```
    1  whoami
    2  ls
    3  pwd
    4  uname -r
    5  ls -la /etc
    ...
```
{% endcode %}

Notice that each line carries a number. Those numbers are what you will use in the next steps to recall specific commands without retyping them.
{% endstep %}

{% step %}
### Recall the Most Recent Command with `!!`

Use `!!` to repeat the last command you ran — in this case, `history` itself.

```bash
!!
```

{% code title="Output" %}
```
history
    1  whoami
    2  ls
    3  pwd
    4  uname -r
    5  ls -la /etc
    ...
```
{% endcode %}

{% hint style="info" %}
Bash prints the expanded command (`history`) on its own line before running it. This confirmation appears every time a history expansion fires, so you always see what will execute before output appears.
{% endhint %}
{% endstep %}

{% step %}
### Recall a Command by History Number with `!n`

Recall a specific command by its number. You will rerun the `uname -r` entry.

Look at the number beside `uname -r` in your history output and substitute that number for `4` if it differs in your session.

```bash
!4
```

{% code title="Output" %}
```
uname -r
5.14.0-362.el9.x86_64
```
{% endcode %}

{% hint style="info" %}
Bash echoes the expanded command before its output. The kernel version string that follows confirms `uname -r` ran exactly as it appeared in the history list.
{% endhint %}
{% endstep %}

{% step %}
### Recall a Command by String Prefix with `!string`

Re-execute the most recent command that starts with a particular string — here, the most recent `ls` command.

```bash
!ls
```

{% code title="Output" %}
```
ls -la /etc
total 1092
drwxr-xr-x. 136 root root  8192 May  7 09:14 .
dr-xr-xr-x.  17 root root   224 Apr 15 08:02 ..
-rw-r--r--.   1 root root    16 Apr 15 08:02 adjtime
...
```
{% endcode %}

{% hint style="info" %}
`!ls` matched `ls -la /etc` — the most recent command whose text begins with `ls` — not the shorter `ls` typed earlier. Bash always selects the most recent match.
{% endhint %}
{% endstep %}

{% step %}
### Search History Interactively with Ctrl-R

Find a command by typing part of it — without knowing its history number.

Press **Ctrl-R** at the prompt. The prompt changes to:

```
(reverse-i-search)`':
```

Type `cat`:

```
(reverse-i-search)`cat': cat /etc/hostname
```

The most recent command containing `cat` appears alongside your search string. Press **Enter** to run it.

{% code title="Output" %}
```
cat /etc/hostname
rhel9-lab.example.com
```
{% endcode %}

{% hint style="info" %}
You found and ran the command without typing its full text or knowing its history number. If you want a different match, press **Ctrl-R** again while the search is active to step further back through the history.
{% endhint %}
{% endstep %}

{% step %}
### Move the Cursor to the Start and End of a Line

Practise cursor navigation on a long command before running it. Type the following but **do not press Enter yet**:

```bash
ls -la /etc/sysconfig/network-scripts
```

Press **Ctrl-A** to jump the cursor to the beginning of the line. The cursor moves to just before `ls`:

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

{% hint style="info" %}
Neither keystroke altered the command text — they only moved the cursor. These two shortcuts work together to let you navigate to any edit point quickly on a command of any length.
{% endhint %}

Press **Enter** to run the command.

{% code title="Output" %}
```
total 4
drwxr-xr-x. 2 root root   6 Apr 15 08:02 .
drwxr-xr-x. 7 root root 134 Apr 15 08:02 ..
```
{% endcode %}
{% endstep %}

{% step %}
### Delete from the Cursor to the Beginning of the Line with Ctrl-U

Practise clearing an in-progress command. Type the following but **do not press Enter**:

```bash
ls -la /etc/sysconfig
```

Press **Ctrl-U**.

{% hint style="success" %}
The entire line disappears, returning you to a clean prompt:

```
$
```
{% endhint %}

{% hint style="info" %}
Ctrl-U discards everything from the cursor position back to the start of the line. It is the fastest way to abandon a command you have decided not to run, without reaching for the Backspace key.
{% endhint %}
{% endstep %}

{% step %}
### Delete the Previous Word with Ctrl-W

Practise removing one argument at a time. Type the following but **do not press Enter**:

```bash
ls -la /etc/hostname
```

Press **Ctrl-W**.

{% hint style="success" %}
The argument `/etc/hostname` is gone, but `ls -la ` remains:

```
$ ls -la
```
{% endhint %}

Press **Ctrl-W** again.

{% hint style="success" %}
```
$ ls
```
{% endhint %}

{% hint style="info" %}
Each press of Ctrl-W removes exactly one whitespace-delimited word to the left of the cursor. This lets you correct the end of a long command without erasing everything.
{% endhint %}

Press **Ctrl-U** to clear the line before the next step.
{% endstep %}

{% step %}
### Clear the Screen with Ctrl-L

Clear a cluttered terminal without losing your command history. First, fill the screen:

```bash
ls -la /etc
```

The long `/etc` directory listing fills the screen. Now press **Ctrl-L**.

{% hint style="success" %}
The screen clears and a fresh prompt appears at the top:

```
$
```
{% endhint %}

{% hint style="info" %}
The history list is still intact — Ctrl-L only clears the visible display.
{% endhint %}

Confirm by running:

```bash
history | tail -5
```

{% code title="Output" %}
```
   96  ls -la /etc
   97  cat /etc/hostname
   98  ls -la /etc
   99  uname -r
  100  history | tail -5
```
{% endcode %}

This matches the final state shown at the top of this tutorial.
{% endstep %}
{% endstepper %}

---

{% hint style="success" %}
**You've completed the tutorial.** In this session you:

1. Displayed the numbered history list with `history`
2. Re-executed the previous command using `!!`
3. Re-executed a specific command by number using `!n`
4. Re-executed the most recent matching command using `!string`
5. Found and ran a command interactively using Ctrl-R incremental reverse search
6. Moved the cursor to the start and end of a line using Ctrl-A and Ctrl-E
7. Discarded an in-progress command using Ctrl-U
8. Deleted the previous word using Ctrl-W
9. Cleared the terminal display using Ctrl-L while preserving history
{% endhint %}

---

## Next Steps

Now that you have built efficient command-line habits, continue with:

- [How-to: Use Command History and Keyboard Shortcuts](#) — apply these techniques in real administrative scenarios
- [Explanation: Understanding the Linux Shell and Command Syntax](#) — understand why history and readline exist as part of the shell's interactive design
- [Reference: Bash Command Syntax and Options](#) — see the complete specification of history expansion operators and readline bindings