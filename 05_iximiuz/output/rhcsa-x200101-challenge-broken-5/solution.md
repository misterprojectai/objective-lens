# Solution: Diagnosing and Removing a Shell Function That Shadows `sudo`

## What Was Broken and Why

The init task appended a Bash **shell function** named `sudo` to `/home/laborant/.bashrc`:

```bash
sudo() {
  echo "[sudo] running as $(whoami): $*" >> /tmp/.sudo_audit.log
  "$@"
}
export -f sudo
```

In Bash, **shell functions take precedence over external binaries** when a command name is looked
up. This means that every time `laborant` types `sudo somecommand`, Bash executes the *function*
instead of `/usr/bin/sudo`. The function runs the arguments directly as the current (unprivileged)
user and logs a convincing-looking audit line — making it appear that `sudo` ran normally.

The `export -f sudo` line exports the function to child shells, making it persist across subshells
spawned during the session. The definition survives login/logout because it lives in `.bashrc`.

This is exactly the misconfiguration class described in the how-to guide:
> "If `declare -f sudo` produces output — a shell function shadows the real `sudo` binary."

---

## How to Diagnose It

### Step 1 — Check what `sudo` resolves to

Log in (or `su -` to `laborant`) and run the type check:

```bash
type sudo
```

**Expected output on a broken system:**

```
sudo is a function
sudo ()
{
    echo "[sudo] running as $(whoami): $*" >> /tmp/.sudo_audit.log;
    "$@"
}
```

This immediately reveals a shell function is intercepting the command.

### Step 2 — Confirm with `declare -f`

```bash
declare -f sudo
```

Any output confirms a function definition exists in the current shell environment.

### Step 3 — Find the source file

```bash
grep -n 'sudo' ~/.bashrc ~/.bash_profile ~/.profile 2>/dev/null
```

This will show the lines in `.bashrc` where the function is defined. Note the line numbers — you
will need them to surgically remove the block.

### Step 4 — Inspect the audit log (curiosity check)

```bash
cat /tmp/.sudo_audit.log
```

This shows every `sudo` invocation that was silently intercepted — confirming how long the shadow
has been active.

---

## How to Fix It

You must remove the function definition from `.bashrc`. There are two clean approaches:

### Option A — Edit `.bashrc` manually with a text editor

```bash
vi /home/laborant/.bashrc
```

Find and delete the entire block:

```bash
# system audit helper - do not remove
sudo() {
  echo "[sudo] running as $(whoami): $*" >> /tmp/.sudo_audit.log
  "$@"
}
export -f sudo
```

Save and exit.

### Option B — Use `sed` to remove the block non-interactively

First, identify the line range (substitute actual line numbers):

```bash
grep -n 'sudo' /home/laborant/.bashrc
```

Then delete those lines — for example if the block spans lines 18–23:

```bash
sed -i '18,23d' /home/laborant/.bashrc
```

Or target by pattern (remove the comment line through the closing brace and export):

```bash
sed -i '/# system audit helper/,/^export -f sudo$/d' /home/laborant/.bashrc
```

### Step — Unset in the current session (optional but good practice)

The file fix takes effect on next login. To clean the *current* session immediately:

```bash
unset -f sudo
```

Verify the function is gone:

```bash
declare -f sudo    # should produce no output
type sudo          # should now say: sudo is /usr/bin/sudo
```

---

## How to Verify the Fix

### Check the file is clean

```bash
grep 'sudo()' /home/laborant/.bashrc || echo "Clean — no sudo() function found"
```

### Confirm the binary is reachable

```bash
type -P sudo
# Expected: /usr/bin/sudo
```

### Start a fresh login shell and re-audit

```bash
su - laborant -c 'type sudo; declare -f sudo'
```

Expected output:
```
sudo is /usr/bin/sudo
```

No function definition output from `declare -f sudo` means the environment is clean.

### Run a real privileged command to confirm

```bash
sudo id
# Expected: prompts for password, then returns uid=0(root) ...
```

---

## Key Takeaways for the RHCSA Exam

| Audit command | What it reveals |
|---|---|
| `type sudo` | Whether `sudo` is a binary, alias, or function |
| `declare -f sudo` | Full function body if a function shadow exists |
| `alias` | All active aliases — check for command overrides |
| `grep -rn 'sudo' ~/.bashrc ~/.bash_profile` | Source file and line of the definition |
| `unset -f funcname` | Remove a function from the current session |

The general rule: **always run `type <command>` before trusting that a command does what its name implies**, especially in security-sensitive contexts like privilege escalation.