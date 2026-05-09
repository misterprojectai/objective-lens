---
description: >-
  Diagnose and fix a 'command not found' error by identifying whether the cause
  is a typo, broken PATH, missing package, or absent execute permission.
icon: wrench
---

# How-to 2: Diagnose and Fix a command not found Error

{% hint style="info" %}
**Before you begin:**

* A Bash shell prompt on an RHEL system
* Root or `sudo` access if the fix requires installing a package with `dnf`
{% endhint %}

{% stepper %}
{% step %}
#### Check for a Typo Using `type`

Run `type` against the command name you attempted.

```bash
type tpye
```

If the shell returns:

```
bash: type: tpye: not found
```

compare the spelling against the known correct command name. Re-run with the corrected spelling.
{% endstep %}

{% step %}
#### Confirm What `type` Reports for a Valid Command

Run `type` against the intended command to determine how the shell classifies it.

```bash
type ls
```

Interpret the result:

* `ls is aliased to 'ls --color=auto'` — command is an alias; it should work
* `ls is /usr/bin/ls` — command is an external executable; it should work
* `ls is a shell builtin` — command is built into Bash; it will always work
* `bash: type: ls: not found` — command is not found by any resolution method; continue to Step 3
{% endstep %}

{% step %}
#### Inspect `$PATH` for Missing Directories

Print the current `$PATH` to check whether expected directories are present.

```bash
echo $PATH
```

A healthy RHEL user `$PATH` looks like:

```
/home/student/.local/bin:/home/student/bin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin
```

If `/usr/bin` or `/usr/sbin` is absent, your `$PATH` has been corrupted or overwritten. Restore the default for this session:

```bash
export PATH=/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:$HOME/.local/bin:$HOME/bin
```

Re-run the original command. If it succeeds, the problem was a broken `$PATH`.

{% hint style="warning" %}
**Silent failure trap:** A truncated `$PATH` produces no error of its own — you only see `command not found` for commands whose directories were dropped. Always inspect `echo $PATH` before assuming the command is uninstalled.
{% endhint %}
{% endstep %}

{% step %}
#### Use `which` to Locate the Executable on Disk

If `$PATH` looks correct but the command is still not found, use `which` to search `$PATH` directories explicitly.

```bash
which git
```

* If `which` returns no output or a `no git in (...)` message — the executable does not exist anywhere in `$PATH`. Proceed to Step 5.
* If `which` returns a path such as `/usr/bin/git` — the executable exists. Proceed to Step 6 to check permissions.
{% endstep %}

{% step %}
#### Check Whether the Package Is Installed

Search for the package that provides the missing command.

```bash
dnf provides git
```

If the output shows an available package, install it:

```bash
sudo dnf install -y git
```

Re-run the original command after installation completes.

<details>

<summary>If you know the binary path but not the package name</summary>

Query by full path instead of command name:

```bash
dnf provides /usr/bin/git
```

If `dnf provides` returns no match, the package name may differ from the command name. Use keyword search instead:

```bash
dnf search <keyword>
```

</details>
{% endstep %}

{% step %}
#### Check Executable Permission on the File

If `which` found the file but the shell still refuses to run it, inspect the file's permissions.

```bash
ls -l /usr/bin/git
```

Look at the permission bits in the first column. A correctly permissioned file shows an `x` bit:

```
-rwxr-xr-x. 1 root root 3941240 Jan 15 12:00 /usr/bin/git
```

If the execute bit is missing (for example, `-rw-r--r--`), restore it:

```bash
sudo chmod +x /usr/bin/git
```

{% hint style="warning" %}
**Syntax trap:** Always supply the full path returned by `which` to `chmod`. Running `chmod +x git` without a path will fail unless you are already in the directory containing the binary.
{% endhint %}

{% hint style="danger" %}
**Destructive risk:** Applying `chmod` to a system binary changes its permissions system-wide. Confirm the path with `which` before running `sudo chmod`.
{% endhint %}
{% endstep %}
{% endstepper %}

## Verification

{% hint style="success" %}
**Confirm the command resolves correctly:**

```bash
type git
```

Expected output — the shell identifies the command as an external executable:

```
git is /usr/bin/git
```

Running the command itself completes without a `command not found` error.
{% endhint %}

## Troubleshooting

{% hint style="warning" %}
**Symptom → Cause → Fix**

**`type` returns `not found` even after correcting the spelling** Cause: Command is not installed and not on `$PATH`. Fix: Run `dnf provides <command>` and install the package.

***

**`/usr/bin` is absent from `echo $PATH` output** Cause: `$PATH` was overwritten in the current session. Fix: Run `export PATH=/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:$HOME/.local/bin:$HOME/bin`

***

**`which` finds the file but running it still fails with `Permission denied`** Cause: Execute bit is missing from the file. Fix: Run `sudo chmod +x <full-path-to-file>`

***

**Command works as root but not as a regular user** Cause: `/usr/sbin` is in root's `$PATH` but not the user's. Fix: Run the command with `sudo`, or add `/usr/sbin` to the user's `$PATH`.

***

**`dnf provides` returns no match** Cause: Package name differs from the command name. Fix: Run `dnf search <keyword>` to locate the correct package name.
{% endhint %}

## Test Yourself

{% embed url="https://labs.iximiuz.com/challenges/rhcsa-x200101-challenge-2-2f97f6e6" %}

**Advanced — Broken Environment:** [Broken Environment Challenge →](https://labs.iximiuz.com/challenges/rhcsa-x200101-challenge-broken-2-56ece41e)
