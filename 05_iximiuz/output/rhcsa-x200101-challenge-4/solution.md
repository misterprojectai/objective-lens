# Solution: Shell History — Delete Sensitive Commands and Prevent Future Logging

## Overview

This challenge has two parts:
1. Delete a specific sensitive entry from `~/.bash_history` without wiping the entire history.
2. Configure `HISTCONTROL` so space-prefixed commands are excluded from history, persistently.

---

## Part 1: Remove the Sensitive History Entry

### Step 1 — View the history list with line numbers

```bash
history
```

Find the line containing `supersecret-api-key=abc123XYZ` and note its number (e.g., `4`).

You can also search directly:

```bash
history | grep supersecret-api-key
```

Example output:
```
    4  echo "supersecret-api-key=abc123XYZ"
```

### Step 2 — Delete the entry by number

```bash
history -d 4
```

> **Note:** If the number was different in your session, substitute it accordingly.

### Step 3 — Write the updated history to disk

```bash
history -w
```

This flushes the in-memory history (now without the deleted entry) to `~/.bash_history`.

### Verify the entry is gone

```bash
grep 'supersecret-api-key' ~/.bash_history
```

No output means the entry has been successfully removed.

---

## Part 2: Configure HISTCONTROL Persistently

### Step 1 — Add the setting to ~/.bashrc

```bash
echo 'export HISTCONTROL=ignoreboth' >> ~/.bashrc
```

`ignoreboth` combines two behaviours:
- `ignorespace` — skip commands that start with a space
- `ignoredups` — skip duplicate consecutive commands

Either `ignorespace` or `ignoreboth` satisfies the requirement.

### Step 2 — Apply the change to the current session

```bash
source ~/.bashrc
```

### Verify the setting is active

```bash
echo $HISTCONTROL
```

Expected output:
```
ignoreboth
```

### Test it

```bash
 echo "this command starts with a space"
history | tail -5
```

The space-prefixed `echo` command should **not** appear in the history output.

---

## Summary of Commands

```bash
# Find and delete the sensitive history entry
history | grep supersecret-api-key
history -d <number>
history -w

# Configure ignorespace persistently
echo 'export HISTCONTROL=ignoreboth' >> ~/.bashrc
source ~/.bashrc
```

---

## Why These Steps Work

| Action | Effect |
|--------|--------|
| `history -d N` | Removes entry N from the in-memory history list |
| `history -w` | Overwrites `~/.bash_history` with the current (modified) in-memory list |
| `HISTCONTROL=ignoreboth` in `~/.bashrc` | Ensures every new Bash session skips space-prefixed and duplicate commands |
| `source ~/.bashrc` | Activates the setting in the current session without requiring a logout |