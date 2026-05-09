---
kind: tutorial

title: "Diagnose and Fix a 'command not found' Error"

description: |
  Walk through every root cause of a Bash 'command not found' error — typo,
  broken $PATH, uninstalled package, missing execute bit — and apply the
  correct fix. Essential diagnostic skill for the RHCSA EX200 exam.

categories:
  - linux

tagz:
  - rhcsa
  - bash
  - shell
  - permissions
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

  init_break_environment:
    init: true
    machine: rocky-01
    needs:
      - init_history_flush
    run: |
      # Create a script with missing execute bit for Step 6
      cat > /usr/local/bin/greet << 'EOF'
      #!/bin/bash
      echo "Hello from greet!"
      EOF
      chmod 644 /usr/local/bin/greet
      chown root:root /usr/local/bin/greet

  verify_type_typo:
    machine: rocky-01
    user: laborant
    run: |
      grep -q 'type tpye\|type gti\|type whihc\|type ipconfig\|type mdkir\|type mkdri' \
        /home/laborant/.bash_history && exit 0 || exit 1
    hintcheck: |
      echo "Run: type tpye"

  verify_type_ls:
    machine: rocky-01
    user: laborant
    run: |
      grep -q 'type ls' /home/laborant/.bash_history && exit 0 || exit 1
    hintcheck: |
      echo "Run: type ls"

  verify_echo_path:
    machine: rocky-01
    user: laborant
    run: |
      grep -q 'echo \$PATH\|echo "${PATH}"' /home/laborant/.bash_history && exit 0 || exit 1
    hintcheck: |
      echo "Run: echo \$PATH"

  verify_export_path:
    machine: rocky-01
    user: laborant
    run: |
      grep -q 'export PATH=' /home/laborant/.bash_history && exit 0 || exit 1
    hintcheck: |
      echo "Run: export PATH=/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:\$HOME/.local/bin:\$HOME/bin"

  verify_which_git:
    machine: rocky-01
    user: laborant
    run: |
      grep -q 'which git' /home/laborant/.bash_history && exit 0 || exit 1
    hintcheck: |
      echo "Run: which git"

  verify_dnf_provides:
    machine: rocky-01
    user: laborant
    run: |
      grep -q 'dnf provides git\|dnf provides /usr/bin/git' \
        /home/laborant/.bash_history && exit 0 || exit 1
    hintcheck: |
      echo "Run: dnf provides git"

  verify_ls_greet:
    machine: rocky-01
    user: laborant
    run: |
      grep -q 'ls -l /usr/local/bin/greet' /home/laborant/.bash_history && exit 0 || exit 1
    hintcheck: |
      echo "Run: ls -l /usr/local/bin/greet"

  verify_chmod_greet:
    machine: rocky-01
    user: laborant
    run: |
      stat -c '%a' /usr/local/bin/greet | grep -q '755\|111\|744\|755' && exit 0
      # Check permission string has execute bit
      ls -l /usr/local/bin/greet | grep -q '^-..x' && exit 0 || exit 1
    hintcheck: |
      echo "Run: sudo chmod +x /usr/local/bin/greet"

  verify_type_greet:
    machine: rocky-01
    user: laborant
    run: |
      grep -q 'type greet' /home/laborant/.bash_history && exit 0 || exit 1
    hintcheck: |
      echo "Run: type greet"
---

# Diagnose and Fix a 'command not found' Error

::remark-box
---
kind: info
---
**Before running any commands:** click the **+** button in the terminal tab bar to open a new terminal tab. The playground history tracking activates in new sessions only. Commands run in the original tab will not register for task verification.
::

Every Linux admin eventually sees this:

```
bash: git: command not found
```

The message is the same regardless of cause — but the fix is different every time. This lab walks you through a systematic diagnostic sequence that works for every variant of this error. Master this flow and you will never stare at `command not found` and wonder where to start.

On the RHCSA exam you may encounter broken environments or need to install missing tools. This exact sequence applies.

---

## What you'll practise

1. Using `type` to detect typos and classify commands
2. Inspecting and repairing `$PATH`
3. Using `which` to locate executables on disk
4. Using `dnf provides` to find and install missing packages
5. Checking and fixing missing execute permissions

---

## Step 1 — Check for a Typo Using `type`

Before assuming anything is broken, rule out a simple spelling mistake.

The `type` built-in asks Bash: *"How would you run this word?"* It searches aliases, functions, builtins, and then `$PATH` — in that order. If none of them match, Bash tells you immediately.

Run `type` against a deliberately misspelled command:

```bash
type tpye
```

You should see:

```
bash: type: tpye: not found
```

Bash found nothing matching `tpye`. Compare against the intended spelling, correct it, and retry.

::simple-task
---
:tasks: tasks
:name: verify_type_typo
---
#active
Run `type` against a misspelled command — for example: `type tpye`

#completed
Done — you used `type` to expose the typo 🎉
::

::remark-box
---
kind: info
---
`type` is a Bash **built-in** — it does not spawn a subprocess and it cannot be silenced by a broken `$PATH`. That makes it the safest first diagnostic tool.
::

---

## Step 2 — Confirm What `type` Reports for a Valid Command

Now run `type` against a command you know works, so you recognise each possible output:

```bash
type ls
```

| Output | Meaning |
|---|---|
| `ls is aliased to 'ls --color=auto'` | Alias — defined in your shell config; will work |
| `ls is /usr/bin/ls` | External executable found in `$PATH`; will work |
| `ls is a shell builtin` | Built into Bash; always works regardless of `$PATH` |
| `bash: type: ls: not found` | Nothing found — continue to Step 3 |

::simple-task
---
:tasks: tasks
:name: verify_type_ls
---
#active
Run `type ls` and read the output carefully.

#completed
Done — you can now interpret every possible `type` response 🎉
::

---

## Step 3 — Inspect `$PATH` for Missing Directories

If `type` returns `not found` for a command you believe is installed, the most common cause is a corrupted or overwritten `$PATH`.

Print it now:

```bash
echo $PATH
```

A healthy Rocky Linux 9 user `$PATH` looks like:

```
/home/laborant/.local/bin:/home/laborant/bin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin
```

The critical directories are `/usr/bin` and `/usr/sbin`. If either is absent, commands like `ls`, `cat`, and `grep` will silently disappear.

::simple-task
---
:tasks: tasks
:name: verify_echo_path
---
#active
Run `echo $PATH` and check that `/usr/bin` appears in the output.

#completed
Done — you've inspected your PATH 🎉
::

### Repair a broken `$PATH`

If `/usr/bin` is missing from your output, restore the default for this session:

```bash
export PATH=/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:$HOME/.local/bin:$HOME/bin
```

::simple-task
---
:tasks: tasks
:name: verify_export_path
---
#active
Run the `export PATH=...` command above to practise resetting a broken PATH.

#completed
Done — you can now recover from a broken PATH in any exam environment 🎉
::

::remark-box
---
kind: warning
---
This `export` fixes `$PATH` for the **current session only**. On the RHCSA exam, if a question broke your PATH in a startup file (such as `.bashrc`), you must also fix the file — otherwise the next login will break it again.
::

::details-box
---
:summary: Why does $PATH break?
---
The most common causes during an exam or on a misconfigured system:

- Someone ran `PATH=somedir` instead of `PATH=somedir:$PATH`, wiping all previous entries
- A `.bashrc` or `/etc/profile.d/` script overwrites `PATH` unconditionally
- The shell was started with `env -i` (empty environment)

If `echo $PATH` shows an empty string or only one directory, a script is almost certainly overwriting it.
::

---

## Step 4 — Use `which` to Locate the Executable on Disk

If `$PATH` looks correct but the command is still missing, use `which` to search each `$PATH` directory explicitly:

```bash
which git
```

Two possible outcomes:

- **`/usr/bin/git`** — the file exists on disk. The problem is likely a permissions issue. Jump to Step 6.
- **No output / `no git in (...)`** — the file is not present anywhere in `$PATH`. Proceed to Step 5 to install it.

::simple-task
---
:tasks: tasks
:name: verify_which_git
---
#active
Run `which git` — observe whether it returns a path or nothing.

#completed
Done — you used `which` to search your PATH directories 🎉
::

::hint-box
---
:summary: which returns nothing but I'm sure git is installed
---
Check whether `git` is installed somewhere **outside** your `$PATH`:

```bash
find /usr /opt /home -name git -type f 2>/dev/null
```

If it appears in a directory like `/usr/local/bin` that is absent from your `$PATH`, fix your PATH (Step 3) rather than reinstalling the package.
::

---

## Step 5 — Check Whether the Package Is Installed

When the executable is nowhere on disk, you need to find and install the package that provides it.

```bash
dnf provides git
```

This queries the RPM database and available repositories for any package that owns a file or capability named `git`. Typical output:

```
git-2.43.0-1.el9.x86_64 : Fast Version Control System
Repo        : appstream
Matched from:
Provide    : git = 2.43.0-1.el9
```

Install the package:

```bash
sudo dnf install -y git
```

::simple-task
---
:tasks: tasks
:name: verify_dnf_provides
---
#active
Run `dnf provides git` to find the package that provides the `git` command.

#completed
Done — you can now trace any missing command back to its RPM package 🎉
::

::remark-box
---
kind: info
---
`dnf provides` also accepts full paths. If you know the binary path but not the package, run `dnf provides /usr/bin/git`. This is useful when a man page or script references an exact path and you need to know which package to install.
::

::hint-box
---
:summary: dnf provides returns no match
---
The command name and the package name often differ. Try a broader search:

```bash
dnf search git
```

This searches package names and descriptions. The correct package may be `git-core`, `perl-Git`, or something else entirely.
::

---

## Step 6 — Check Executable Permission on the File

This step covers a subtle failure: `which` finds the file, the package is installed, but running the command still fails.

The playground pre-created a script at `/usr/local/bin/greet` with the execute bit deliberately removed. Inspect it:

```bash
ls -l /usr/local/bin/greet
```

You should see something like:

```
-rw-r--r--. 1 root root 42 Jan 15 12:00 /usr/local/bin/greet
```

The permission string `-rw-r--r--` has no `x` anywhere. Bash cannot execute this file even though it exists and is in your `$PATH`.

::simple-task
---
:tasks: tasks
:name: verify_ls_greet
---
#active
Run `ls -l /usr/local/bin/greet` to inspect the missing execute bit.

#completed
Done — you spotted the missing execute permission 🎉
::

Restore the execute bit:

```bash
sudo chmod +x /usr/local/bin/greet
```

::simple-task
---
:tasks: tasks
:name: verify_chmod_greet
---
#active
Run `sudo chmod +x /usr/local/bin/greet` to restore the execute permission.

#completed
Done — the execute bit is restored 🎉
::

::remark-box
---
kind: info
---
`chmod +x` adds the execute bit for **owner, group, and other** simultaneously. On the RHCSA exam you may need finer control — for example `chmod u+x` adds it for the owner only. Know the difference.
::

---

## Verification — Confirm the Command Resolves

After working through whichever steps applied to your situation, always end with `type` to confirm resolution:

```bash
type greet
```

Expected output:

```
greet is /usr/local/bin/greet
```

Bash now classifies `greet` as an external executable at a known path. Run it to confirm end-to-end:

```bash
greet
```

Expected:

```
Hello from greet!
```

::simple-task
---
:tasks: tasks
:name: verify_type_greet
---
#active
Run `type greet` to confirm Bash now resolves the command correctly.

#completed
Done — the command resolves and executes successfully 🎉
::

---

## Troubleshooting Reference

| Symptom | Most Likely Cause | Fix |
|---|---|---|
| `type` returns `not found` even after correcting spelling | Command not installed, not on `$PATH` | `dnf provides <command>` then install |
| `/usr/bin` absent from `echo $PATH` output | `$PATH` overwritten in current session | `export PATH=/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:$HOME/.local/bin:$HOME/bin` |
| `which` finds the file but shell returns `Permission denied` | Execute bit missing | `sudo chmod +x <full-path>` |
| Command works as `root` but not as a regular user | `/usr/sbin` not in user's `$PATH` | Run with `sudo`, or add `/usr/sbin` to user's `$PATH` |
| `dnf provides` returns no match | Package name differs from command name | `dnf search <keyword>` |

---

## Diagnostic Flow Summary

```
command not found
       │
       ▼
type <command>  ──── typo? ──────────────────► fix spelling, retry
       │
       │ not found
       ▼
echo $PATH ──── /usr/bin missing? ──────────► export PATH=..., retry
       │
       │ PATH looks correct
       ▼
which <command> ──── no path returned? ─────► dnf provides, install
       │
       │ path returned
       ▼
ls -l <path> ──── no execute bit? ──────────► chmod +x, retry
       │
       │ bit present
       ▼
type <command>  (should now resolve)
```

---

## What to Remember for the Exam

- **`type` first, always.** It is a builtin, immune to a broken `$PATH`, and tells you exactly how Bash resolves a name.
- **`echo $PATH` is your second move** when `type` says not found. A wiped PATH silences almost every command at once.
- **`dnf provides`** traces any missing file back to its RPM package. Works with command names and full paths.
- **`chmod +x`** is the fix when the file exists but cannot be executed. The RHCSA exam occasionally presents scripts that need this step before they can run.
```