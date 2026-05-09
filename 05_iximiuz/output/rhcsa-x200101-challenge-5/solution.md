# Solution: Audit the Shell Environment — Detect a Shadowed Command

## What Was Injected

The init task added two malicious definitions to `/home/laborant/.bashrc`:

1. An alias: `alias sudo='echo ALIAS_TRIGGERED && sudo'`
2. A shell function that blocks `useradd`:
   ```bash
   useradd() {
     echo "FUNCTION_TRIGGERED: useradd blocked"
   }
   export -f useradd
   ```

## Step 1 — Confirm the Problem

Open a shell as `laborant` and inspect the environment:

```bash
type sudo
```
Expected: `sudo is aliased to 'echo ALIAS_TRIGGERED && sudo'`

```bash
declare -f useradd
```
Expected: outputs the blocking function body.

## Step 2 — Identify the Source

Trace where the definitions came from:

```bash
grep -n 'alias sudo' ~/.bashrc
grep -n 'useradd' ~/.bashrc
```

Both definitions are in `~/.bashrc`.

## Step 3 — Remove the Alias

Open `~/.bashrc` in a text editor:

```bash
vi ~/.bashrc
```

Find and delete the line:
```
alias sudo='echo ALIAS_TRIGGERED && sudo'
```

## Step 4 — Remove the Shell Function

In the same file, locate and delete the entire block:
```bash
useradd() {
  echo "FUNCTION_TRIGGERED: useradd blocked"
}
export -f useradd
```

Save and close the file.

## Step 5 — Verify in a New Shell

Open a new login shell or re-source the file:

```bash
bash --login
```

Now verify the alias is gone:
```bash
alias sudo 2>&1
```
Expected: `bash: alias: sudo: not found` or no output.

Verify the function is gone:
```bash
declare -f useradd
```
Expected: no output.

Verify `/usr/bin` is still in `$PATH`:
```bash
echo $PATH | tr ':' '\n' | grep '^/usr/bin$'
```
Expected: `/usr/bin`

## Key Commands Used

| Command | Purpose |
|---|---|
| `type sudo` | Reveals whether `sudo` is a binary, alias, or function |
| `declare -f useradd` | Shows the function body if `useradd` is shadowed by a function |
| `alias` | Lists all active aliases in the current session |
| `grep -n 'pattern' ~/.bashrc` | Finds the line number of a suspicious definition |
| `bash --login -c 'declare -f useradd'` | Tests a clean login shell without entering it interactively |
| `echo $PATH \| tr ':' '\n'` | Displays PATH entries one per line for easy inspection |

## Why This Matters for RHCSA

On a real system, a compromised `~/.bashrc` or a shared profile script that aliases `sudo` or `useradd` can:

- Log credentials entered after `sudo`
- Silently block user creation while appearing to succeed
- Redirect commands to attacker-controlled binaries

Always audit the shell environment with `type`, `alias`, and `declare -f` before performing privileged tasks on an unfamiliar system.