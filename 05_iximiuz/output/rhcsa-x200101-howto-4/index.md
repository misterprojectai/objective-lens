---
kind: tutorial

title: "Use Command History to Recall and Re-execute Commands"

description: |
  Master Bash command history for the RHCSA EX200 exam: display and search history,
  re-execute commands by number or prefix, edit recalled commands, delete sensitive
  entries, and control what gets saved to ~/.bash_history.

categories:
  - linux

tagz:
  - rhcsa
  - bash
  - history
  - shell
  - grep

createdAt: 2025-01-01
updatedAt: 2025-01-01

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
      # Seed the history file with known commands so learners have material to work with
      cat >> /home/laborant/.bash_history << 'EOF'
      ls -la /etc
      cat /etc/hostname
      echo "hello world"
      grep -r "root" /etc/passwd
      df -h
      free -m
      uptime
      whoami
      id
      pwd
      ls /var/log
      cat /etc/os-release
      echo "test output"
      ls -lh /home
      date
      EOF
      chown laborant:laborant /home/laborant/.bash_history

  verify_history_displayed:
    machine: rocky-01
    user: laborant
    run: |
      grep -qE '^[[:space:]]*(history|history [0-9]+)[[:space:]]*$' /home/laborant/.bash_history && exit 0 || exit 1
    hintcheck: |
      echo "Run: history   (or: history 20)"

  verify_bang_number_used:
    machine: rocky-01
    user: laborant
    run: |
      grep -qE '^[[:space:]]*![0-9]+[[:space:]]*$' /home/laborant/.bash_history && exit 0 || exit 1
    hintcheck: |
      echo "Run: history   to see line numbers, then run: !<number>   substituting a real number from your list"

  verify_bang_bang_used:
    machine: rocky-01
    user: laborant
    run: |
      grep -qE '^[[:space:]]*!![[:space:]]*$' /home/laborant/.bash_history && exit 0 || exit 1
    hintcheck: |
      echo "Run: !!   to repeat the last command"

  verify_bang_string_used:
    machine: rocky-01
    user: laborant
    run: |
      grep -qE '^[[:space:]]*!ls[[:space:]]*$' /home/laborant/.bash_history && exit 0 || exit 1
    hintcheck: |
      echo "Run: !ls   to re-execute the most recent command starting with 'ls'"

  verify_history_delete_used:
    machine: rocky-01
    user: laborant
    run: |
      grep -qE '^[[:space:]]*history -d [0-9]+[[:space:]]*$' /home/laborant/.bash_history && exit 0 || exit 1
    hintcheck: |
      echo "Run: history   to see entries, then: history -d <number>   with a real line number"

  verify_history_clear_used:
    machine: rocky-01
    user: laborant
    run: |
      grep -qE '^[[:space:]]*history -c[[:space:]]*$' /home/laborant/.bash_history && exit 0 || exit 1
    hintcheck: |
      echo "Run: history -c   to clear the in-memory history list"

  verify_histcontrol_checked:
    machine: rocky-01
    user: laborant
    run: |
      grep -qE '^[[:space:]]*echo \$HISTCONTROL[[:space:]]*$' /home/laborant/.bash_history && exit 0 || exit 1
    hintcheck: |
      echo "Run: echo \$HISTCONTROL   to see the current setting"

  verify_histcontrol_set:
    machine: rocky-01
    user: laborant
    run: |
      grep -qE '^[[:space:]]*export HISTCONTROL=ignoreboth[[:space:]]*$' /home/laborant/.bash_history && exit 0 || exit 1
    hintcheck: |
      echo "Run: export HISTCONTROL=ignoreboth"

  verify_space_prefix_used:
    machine: rocky-01
    user: laborant
    run: |
      # Check that HISTCONTROL includes ignorespace/ignoreboth AND a space-prefixed command was attempted
      # We verify the user set HISTCONTROL and used a leading-space command
      grep -qE '^[[:space:]]*export HISTCONTROL=ignoreboth[[:space:]]*$' /home/laborant/.bash_history && \
      grep -qE '^ echo ' /home/laborant/.bash_history && exit 0 || exit 1
    hintcheck: |
      echo "First ensure HISTCONTROL is set: export HISTCONTROL=ignoreboth   then run:  echo \"secret\"   (note the leading space)"

  verify_history_write_used:
    machine: rocky-01
    user: laborant
    run: |
      grep -qE '^[[:space:]]*history -w[[:space:]]*$' /home/laborant/.bash_history && exit 0 || exit 1
    hintcheck: |
      echo "Run: history -w   to flush in-memory history to ~/.bash_history"

  verify_history_tail:
    machine: rocky-01
    user: laborant
    run: |
      grep -qE '^[[:space:]]*tail -10 ~/.bash_history[[:space:]]*$' /home/laborant/.bash_history && exit 0 || exit 1
    hintcheck: |
      echo "Run: tail -10 ~/.bash_history"

---

# Use Command History to Recall and Re-execute Commands

::remark-box
---
kind: info
---
**Before running any commands:** click the **+** button in the terminal tab bar to open a new terminal tab. The playground history tracking activates in new sessions only. Commands run in the original tab will not register for task verification.
::

The Bash history mechanism is one of the highest-value efficiency tools on the RHCSA exam. Under time pressure, being able to recall, edit, and re-execute a previous command in seconds — instead of retyping it — makes a measurable difference. This lab walks you through every technique you need, including how to keep sensitive commands out of the history file.

---

## Step 1 — Display the history list with line numbers

The `history` builtin prints every command in the current session's in-memory list, each prefixed by a sequential number. Those numbers are your handles for direct re-execution.

```bash
history
```

To limit output to the most recent entries, pass a count:

```bash
history 20
```

Scroll through the output. Notice that commands are numbered from 1 at the top. Every history expansion operator you will use in the next steps references these numbers.

::simple-task
---
:tasks: tasks
:name: verify_history_displayed
---
#active
Run `history` (or `history 20`) and review the numbered list.

#completed
History displayed successfully ✓
::

---

## Step 2 — Re-execute a command by history number

Once you know a command's number from the list, you can run it instantly with `!<number>`:

```bash
!5
```

Replace `5` with any number from your own history list. The shell expands the token, prints the resolved command, and executes it.

::remark-box
---
kind: warning
---
Bang-number expansion executes immediately with **no confirmation prompt**. Always verify the intended command with `history` first, especially before re-running anything that modifies files or services.
::

::simple-task
---
:tasks: tasks
:name: verify_bang_number_used
---
#active
Run `history`, pick a safe entry (e.g. one that just lists files), and re-execute it with `!<number>`.

#completed
Command re-executed by number ✓
::

---

## Step 3 — Re-execute the last command with `!!`

`!!` expands to the entire previous command line. It is most useful when you forgot to prefix a command with `sudo`:

```bash
!!
```

Or:

```bash
sudo !!
```

When you run `sudo !!`, the shell first expands `!!` to the text of the previous command, then `sudo` runs that expanded string. The expanded command is echoed to the terminal before execution so you can see exactly what ran.

::simple-task
---
:tasks: tasks
:name: verify_bang_bang_used
---
#active
Run `!!` to repeat your last command.

#completed
Last command repeated with `!!` ✓
::

---

## Step 4 — Re-execute the most recent command matching a string prefix

`!string` finds the most recent history entry that **began** with `string` and re-executes it:

```bash
!ls
```

This is useful for quickly replaying a long command (e.g., a complex `find` or `grep`) without scrolling through the list — as long as you remember how it started.

::remark-box
---
kind: warning
---
Like `!number`, `!string` executes immediately. If multiple commands share the same prefix, the **most recent** match runs. Confirm with `history | grep ^ls` first when in doubt.
::

::simple-task
---
:tasks: tasks
:name: verify_bang_string_used
---
#active
Run `!ls` to re-execute the most recent command that started with `ls`.

#completed
Prefix-based re-execution used ✓
::

---

## Step 5 — Search history interactively with Ctrl-R

For longer or less predictable commands, interactive reverse search is faster than scrolling:

1. Press **Ctrl-R** at an empty prompt.
2. Type a substring — the most recent matching command appears.
3. Press **Ctrl-R** again to cycle to the next older match.
4. Press **Enter** to execute, or **Ctrl-G** to cancel without running anything.

```
(reverse-i-search)`host': cat /etc/hostname
```

::remark-box
---
kind: info
---
Ctrl-R is not verified automatically (it is interactive and leaves no distinct history token). Practice it now — it is faster than any other recall method once you build the muscle memory. On the exam, use it to recall `systemctl`, `firewall-cmd`, or `semanage` commands you have already issued earlier in the session.
::

::details-box
---
:summary: "Ctrl-R key reference"
---
| Key | Action |
|---|---|
| `Ctrl-R` | Open reverse search / cycle to next older match |
| `Enter` | Execute the currently displayed command |
| `Ctrl-G` | Cancel search, return to empty prompt |
| `Esc` | Accept the match into the line editor without executing |
| `Ctrl-A` | Move cursor to beginning of the recalled line |
| `Ctrl-E` | Move cursor to end of the recalled line |
| `Alt-B` / `Alt-F` | Move backward / forward one word |
::

---

## Step 6 — Recall and edit a command before executing

Use the **Up** and **Down** arrow keys to navigate through history. When you reach the command you want, use readline shortcuts to edit it before pressing Enter:

| Key | Action |
|---|---|
| `Ctrl-A` | Move cursor to beginning of line |
| `Ctrl-E` | Move cursor to end of line |
| `Ctrl-U` | Delete from cursor to beginning of line |
| `Alt-B` / `Alt-F` | Move backward / forward one word |

This technique is ideal when you want to run the same command against a different file or with a slightly different flag. There is nothing to verify here — practice navigating to a previous command, modifying one token, and executing it.

---

## Step 7 — Delete a specific entry from history

Remove a single entry by its line number. This is the standard way to prevent a sensitive command (containing a password or token) from persisting in the history file:

First, identify the line number:

```bash
history
```

Then delete it:

```bash
history -d 42
```

Replace `42` with the actual line number from your list.

::remark-box
---
kind: warning
---
After each `history -d`, all subsequent entries **renumber** (shift up by one). Always run `history` again before the next deletion to get the current numbers.
::

::simple-task
---
:tasks: tasks
:name: verify_history_delete_used
---
#active
Run `history`, identify a line number, then run `history -d <number>` to remove that entry.

#completed
Entry deleted from history ✓
::

---

## Step 8 — Clear the entire in-memory history list

To wipe all history entries from the current session's memory in one operation:

```bash
history -c
```

This does **not** immediately update `~/.bash_history` on disk. The file is overwritten (with an empty list) only when the session writes history — either on logout or via `history -w`. To clear both memory and file together:

```bash
history -c && history -w
```

::simple-task
---
:tasks: tasks
:name: verify_history_clear_used
---
#active
Run `history -c` to clear the in-memory history list.

#completed
In-memory history cleared ✓
::

::remark-box
---
kind: info
---
After `history -c`, your current session's history is gone. The init task for this lab pre-seeded `~/.bash_history` so you still have entries on disk. Open a fresh terminal tab after clearing to see an empty in-memory list.
::

---

## Step 9 — Check and set HISTCONTROL

`HISTCONTROL` governs which commands Bash records. The values relevant to the exam:

| Value | Behaviour |
|---|---|
| `ignorespace` | Commands prefixed by one or more spaces are not saved |
| `ignoredups` | Consecutive duplicate commands are not saved |
| `ignoreboth` | Both of the above |
| `erasedups` | All earlier duplicates are removed whenever a command is added |

Check the current setting:

```bash
echo $HISTCONTROL
```

::simple-task
---
:tasks: tasks
:name: verify_histcontrol_checked
---
#active
Run `echo $HISTCONTROL` to see the current value.

#completed
HISTCONTROL value checked ✓
::

If the output does not include `ignorespace` or `ignoreboth`, set it now:

```bash
export HISTCONTROL=ignoreboth
```

::simple-task
---
:tasks: tasks
:name: verify_histcontrol_set
---
#active
Run `export HISTCONTROL=ignoreboth` to enable ignorespace and ignoredups for this session.

#completed
HISTCONTROL configured ✓
::

To make this permanent, add the line to `~/.bashrc`.

---

## Step 10 — Prevent a command from being saved to history

With `HISTCONTROL` set to `ignoreboth` (or `ignorespace`), any command prefixed by **one or more spaces** is silently omitted from history:

```bash
 echo "my-secret-token"
```

> Note the leading space before `echo` — that is the critical part.

Run the command above, then check that it does **not** appear at the bottom of the history list:

```bash
history | tail -5
```

::simple-task
---
:tasks: tasks
:name: verify_space_prefix_used
---
#active
Ensure `HISTCONTROL=ignoreboth` is exported, then run ` echo "secret"` with a leading space.

#completed
Space-prefixed command correctly omitted from history ✓
::

::hint-box
---
:summary: "The space-prefixed command still appears in history"
---
`HISTCONTROL` must be set **before** the command is issued. Verify with `echo $HISTCONTROL` — it must show `ignorespace` or `ignoreboth`. If you set it in the same command line or in a subshell it will not apply to that command. Also confirm there are no conflicting HISTCONTROL settings in `~/.bashrc`.
::

---

## Step 11 — Write the current session history to disk immediately

By default, Bash appends in-memory history to `~/.bash_history` only when the session closes. Force an immediate write with:

```bash
history -w
```

This is useful before switching to another terminal where you want to access commands from the current session via `Ctrl-R` or `grep`.

::simple-task
---
:tasks: tasks
:name: verify_history_write_used
---
#active
Run `history -w` to flush the in-memory history to `~/.bash_history`.

#completed
History written to disk ✓
::

---

## Verification

Confirm the on-disk history file reflects recent work:

```bash
tail -10 ~/.bash_history
```

::simple-task
---
:tasks: tasks
:name: verify_history_tail
---
#active
Run `tail -10 ~/.bash_history` to inspect the last ten recorded commands.

#completed
History file confirmed ✓
::

The output should show the most recently written commands in order, with no gaps unless you deliberately deleted entries.

---

## Troubleshooting

::details-box
---
:summary: "Space-prefixed commands still appear in history"
---
`HISTCONTROL` does not include `ignorespace`. Run:

```bash
echo $HISTCONTROL
export HISTCONTROL=ignoreboth
```

To make it permanent, add `export HISTCONTROL=ignoreboth` to `~/.bashrc`.
::

::details-box
---
:summary: "`history -d` removes the wrong entry"
---
Line numbers shift down by one after every deletion. Run `history` again after each `history -d` to get the updated numbers before issuing the next deletion.
::

::details-box
---
:summary: "`!string` executes the wrong command"
---
Multiple commands share the same prefix; the most recent match may not be the intended one. Use `!number` from the explicit history list, or use `Ctrl-R` to visually confirm the match before executing.
::

::details-box
---
:summary: "`~/.bash_history` does not update after `history -c`"
---
`history -c` clears the in-memory list only. The file is written on session close or on explicit `history -w`. To clear both together:

```bash
history -c && history -w
```
::

::details-box
---
:summary: "Ctrl-R finds no match"
---
The command may have been deleted, or the in-memory list was cleared. Search the file directly:

```bash
grep 'pattern' ~/.bash_history
```
::

---

## What you practised — exam checklist

- `history` / `history N` — display numbered list
- `!N` — re-execute by number
- `!!` — repeat last command (and `sudo !!`)
- `!string` — re-execute by prefix
- `Ctrl-R` — interactive reverse search
- Arrow keys + readline shortcuts — recall and edit before executing
- `^old^new` — quick inline substitution on the previous command
- `history -d N` — delete a single entry
- `history -c` — clear in-memory list
- `history -w` — flush to disk immediately
- Leading space + `HISTCONTROL=ignoreboth` — suppress a command from history

These operations appear directly in RHCSA objectives under *"Use input/output redirection"* and the broader command-line proficiency requirement. Mastering them reduces keystrokes across every other objective.

---

## Related

- `man bash` — HISTORY section (search `/^HISTORY` inside the pager)
- `help history` — builtin reference
- How-to 3 of 6: Navigate Shell Documentation with `man`, `--help`, and `info`
```