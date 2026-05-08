---
description: Search, select, edit, and re-execute previous Bash commands using history, Ctrl-R, and history expansion operators, and remove sensitive commands from history.
icon: wrench
---

# How to Use Command History to Recall and Re-execute Commands

{% hint style="info" %}
**Prerequisites**

- An active Bash shell session with a populated history list (at least several prior commands issued)
- Write access to `~/.bash_history` (normal for any regular user or root in their own home directory)
{% endhint %}

{% stepper %}
{% step %}
### Display the history list with line numbers

Print the full history list to identify commands by number.

```bash
history
```

To limit output to the most recent entries:

```bash
history 20
```
{% endstep %}

{% step %}
### Re-execute a command by history number

Run any command from the list using its history number.

```bash
!42
```

Replace `42` with the number shown in the history list.
{% endstep %}

{% step %}
### Re-execute the last command with `!!`

Repeat the immediately preceding command.

```bash
!!
```

To repeat the last command with elevated privileges:

```bash
sudo !!
```
{% endstep %}

{% step %}
### Re-execute the most recent command matching a string prefix

Run the last command that began with a given string.

```bash
!ls
```

Replace `ls` with the prefix that matches the command you want.

{% hint style="warning" %}
`!string` executes immediately without confirmation. Verify the intended command in the history list first if the action is destructive.
{% endhint %}
{% endstep %}

{% step %}
### Search history interactively with Ctrl-R

Press `Ctrl-R` at the prompt and type a search string to find the most recent matching command.

```
(reverse-i-search)`cat': cat /etc/hostname
```

- Press `Ctrl-R` again to cycle to the next older match.
- Press `Enter` to execute the displayed command.
- Press `Ctrl-G` to cancel the search without executing.
{% endstep %}

{% step %}
### Recall and edit a command before executing

Use the Up arrow key to navigate to the command you want, then edit it on the command line before pressing Enter.

To move within the recalled line:

| Key | Action |
|---|---|
| `Ctrl-A` | Move cursor to beginning of line |
| `Ctrl-E` | Move cursor to end of line |
| `Ctrl-U` | Delete from cursor to beginning of line |
| `Alt-B` / `Alt-F` | Move backward / forward one word |
{% endstep %}

{% step %}
### Substitute a string in the previous command with `^`

Correct a typo or change one token in the last command without retyping the whole line.

```bash
^old^new
```

Example — if you just ran `cat /etc/hostnam`, correct it with:

```bash
^hostnam^hostname
```
{% endstep %}

{% step %}
### Delete a specific entry from history

Remove a single history entry by its line number to prevent sensitive commands from persisting.

```bash
history -d 42
```

Replace `42` with the line number of the command to remove.

{% hint style="warning" %}
After each deletion, line numbers of subsequent entries shift. Run `history` again to get current numbers before each successive `history -d`.
{% endhint %}

<details>
<summary>Deleting a range of entries</summary>

There is no native range-delete syntax. To delete multiple consecutive entries, use a loop — but note that line numbers shift after every deletion, so iterate from highest to lowest number to avoid chasing shifted indices:

```bash
for n in $(seq 50 -1 42); do history -d $n; done
```

Verify the result with `history` after the loop completes.

</details>
{% endstep %}

{% step %}
### Clear the entire in-memory history list

Remove all history entries from the current session's memory.

```bash
history -c
```

{% hint style="danger" %}
`history -c` clears in-memory history only. If the session closes normally afterward, the now-empty list will overwrite `~/.bash_history`. To clear both memory and file immediately, run `history -c && history -w`.
{% endhint %}
{% endstep %}

{% step %}
### Prevent a command from being saved to history

Prefix the command with one or more spaces. Bash omits space-prefixed commands from history when `HISTCONTROL` includes `ignorespace`.

```bash
 echo "my-secret-token"
```

To confirm this setting is active:

```bash
echo $HISTCONTROL
```

Expected value includes `ignorespace` or `ignoreboth`.

{% hint style="warning" %}
If `echo $HISTCONTROL` does not return `ignorespace` or `ignoreboth`, the space prefix will not suppress history recording. Activate it for the current session with `export HISTCONTROL=ignoreboth`, or add that line to `~/.bashrc` to persist it.
{% endhint %}
{% endstep %}

{% step %}
### Write the current session history to disk immediately

Force the in-memory history to be written to `~/.bash_history` without waiting for the session to close.

```bash
history -w
```
{% endstep %}
{% endstepper %}

## Verification

{% hint style="success" %}
**Confirm history operations are working correctly**

Check the last 10 in-memory history entries:

```bash
history | tail -10
```

Expected: the last 10 entries appear in the correct order with sequential line numbers.

Confirm a deleted entry is gone — the surrounding entries will have renumbered, verifiable by re-running `history`.

Confirm `~/.bash_history` reflects the current session:

```bash
tail -10 ~/.bash_history
```

Expected: output matches the most recently written commands.
{% endhint %}

## Troubleshooting

{% hint style="warning" %}
**Common problems and fixes**

**Space-prefixed commands still appear in history**
- Cause: `HISTCONTROL` does not include `ignorespace`
- Fix: Run `export HISTCONTROL=ignoreboth`, or add it to `~/.bashrc`

---

**`history -d` removes the wrong entry**
- Cause: Line numbers shift after each deletion
- Fix: Run `history` again after each deletion to get current numbers before the next `history -d`

---

**`!string` executes the wrong command**
- Cause: Multiple commands share the same prefix; the most recent match is not the intended one
- Fix: Use `!number` from the explicit history list instead, or use `Ctrl-R` to confirm the match visually before executing

---

**`~/.bash_history` does not update after `history -c`**
- Cause: `-c` clears in-memory history only; a subsequent session write overwrites the file with the now-empty list, but only after `history -w` or session close
- Fix: Run `history -c && history -w` together to clear both memory and file immediately

---

**`Ctrl-R` finds no match**
- Cause: The command is not in the in-memory history list, or was deleted
- Fix: Search `~/.bash_history` directly with `grep pattern ~/.bash_history`
{% endhint %}