---
kind: tutorial

title: "How to Identify and Modify $PATH for Command Availability"

description: |
  Learn how to inspect $PATH, add a directory for the current shell session,
  and persist the change in ~/.bash_profile so it survives a new login shell.
  A core skill for RHCSA EX200 exam objective 101.

categories:
  - linux

tagz:
  - rhcsa
  - bash
  - shell
  - permissions

createdAt: 2025-06-01
updatedAt: 2025-06-01

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

  init_create_myapp_dir:
    init: true
    machine: rocky-01
    needs:
      - init_history_flush
    run: |
      mkdir -p /opt/myapp/bin
      cat > /opt/myapp/bin/mycommand << 'EOF'
      #!/bin/bash
      echo "mycommand from /opt/myapp/bin"
      EOF
      chmod +x /opt/myapp/bin/mycommand
      chown -R laborant:laborant /opt/myapp

  verify_inspected_path:
    machine: rocky-01
    user: laborant
    run: |
      grep -qE 'echo \$PATH' /home/laborant/.bash_history && exit 0 || exit 1
    hintcheck: |
      echo "Run: echo \$PATH"

  verify_path_with_tr:
    machine: rocky-01
    user: laborant
    run: |
      grep -qE "echo \\\$PATH.*tr.*':'" /home/laborant/.bash_history || \
      grep -q "tr ':' '\\\n'" /home/laborant/.bash_history && exit 0 || exit 1
    hintcheck: |
      echo "Run: echo \$PATH | tr ':' '\n'"

  verify_grep_path:
    machine: rocky-01
    user: laborant
    run: |
      grep -q 'grep.*opt/myapp/bin' /home/laborant/.bash_history && exit 0 || exit 1
    hintcheck: |
      echo "Run: echo \$PATH | tr ':' '\n' | grep '/opt/myapp/bin'"

  verify_export_path_session:
    machine: rocky-01
    user: laborant
    run: |
      grep -qE "export PATH=.*opt/myapp/bin.*\\\$PATH|export PATH=\\\$PATH.*opt/myapp/bin" /home/laborant/.bash_history && exit 0 || exit 1
    hintcheck: |
      echo "Run: export PATH=/opt/myapp/bin:\$PATH"

  verify_persisted_bash_profile:
    machine: rocky-01
    user: laborant
    run: |
      grep -q 'opt/myapp/bin' /home/laborant/.bash_profile && exit 0 || exit 1
    hintcheck: |
      echo "Add the export line to ~/.bash_profile:"
      echo "  echo 'export PATH=/opt/myapp/bin:\$PATH' >> ~/.bash_profile"

  verify_login_shell_path:
    machine: rocky-01
    user: laborant
    run: |
      grep -qE "bash --login" /home/laborant/.bash_history && exit 0 || exit 1
    hintcheck: |
      echo "Run: bash --login -c 'echo \$PATH | tr \":\" \"\n\"'"

  verify_path_contains_myapp:
    machine: rocky-01
    user: laborant
    run: |
      su - laborant -c 'echo $PATH' | grep -q '/opt/myapp/bin' && exit 0 || exit 1
    hintcheck: |
      echo "Make sure ~/.bash_profile contains: export PATH=/opt/myapp/bin:\$PATH"
      echo "Check with: grep opt/myapp/bin ~/.bash_profile"
---

# How to Identify and Modify $PATH for Command Availability

::remark-box
---
kind: info
---
**Before running any commands:** click the **+** button in the terminal tab bar to open a new terminal tab. The playground history tracking activates in new sessions only. Commands run in the original tab will not register for task verification.
::

This tutorial walks you through inspecting `$PATH`, adding a directory for the current shell session, and persisting that change so it survives a new login shell. On the RHCSA EX200 exam you may need to make a custom command findable without knowing its full path — this is how.

The playground has already created `/opt/myapp/bin/mycommand` for you to work with.

---

## Step 1 — Inspect the Current $PATH

The shell resolves command names by searching each directory listed in `$PATH` from left to right, stopping at the first match. Knowing what is already there — and in what order — is the starting point before making any change.

Display the current search path:

```bash
echo $PATH
```

The output is a colon-separated string that is hard to read at a glance. Pipe it through `tr` to see one directory per line:

```bash
echo $PATH | tr ':' '\n'
```

::remark-box
---
kind: info
---
Order matters. A directory at position 1 is searched before position 8. If two directories contain a binary with the same name, the one found first wins.
::

::simple-task
---
:tasks: tasks
:name: verify_inspected_path
---
#active
Run `echo $PATH` to display the current search path.

#completed
PATH inspected ✓
::

::simple-task
---
:tasks: tasks
:name: verify_path_with_tr
---
#active
Run `echo $PATH | tr ':' '\n'` to display each directory on its own line.

#completed
Directories listed one per line ✓
::

---

## Step 2 — Check Whether Your Directory Is Already in $PATH

Before modifying anything, confirm the directory is actually missing:

```bash
echo $PATH | tr ':' '\n' | grep '/opt/myapp/bin'
```

If the command returns no output, `/opt/myapp/bin` is not in `$PATH`. That is the expected result here — proceed to Step 3.

::simple-task
---
:tasks: tasks
:name: verify_grep_path
---
#active
Run `echo $PATH | tr ':' '\n' | grep '/opt/myapp/bin'` to check whether the directory is already present.

#completed
PATH checked for /opt/myapp/bin ✓
::

---

## Step 3 — Add the Directory for the Current Session

You have two options depending on the priority you need.

**Prepend** (new directory searched first — takes priority over any existing command of the same name):

```bash
export PATH=/opt/myapp/bin:$PATH
```

**Append** (new directory searched last — existing system commands take priority):

```bash
export PATH=$PATH:/opt/myapp/bin
```

For this exercise use the prepend form so `/opt/myapp/bin` appears at the front of the list.

::remark-box
---
kind: warning
---
This change applies to the current shell session and any child processes it spawns. It is **lost** when the terminal closes. Step 4 makes it permanent.
::

After running the export, confirm the directory is now present:

```bash
echo $PATH | tr ':' '\n'
```

::simple-task
---
:tasks: tasks
:name: verify_export_path_session
---
#active
Run `export PATH=/opt/myapp/bin:$PATH` to add the directory for this session.

#completed
Directory added to PATH for the current session ✓
::

::hint-box
---
:summary: The command is still not found after the export
---
Check for a typo in the path. Run `echo $PATH | tr ':' '\n'` and look for `/opt/myapp/bin` in the output. If the line is missing, re-run the export command exactly as shown. A common mistake is writing `export PATH=/opt/myapp/bin` (without `:\$PATH`), which **discards the entire original PATH** and leaves you with only that one directory.
::

---

## Step 4 — Persist the Change in ~/.bash_profile

Session exports disappear when the terminal closes. To make the change survive a new login shell, add the export line to `~/.bash_profile`:

```bash
echo 'export PATH=/opt/myapp/bin:$PATH' >> ~/.bash_profile
```

::remark-box
---
kind: warning
---
Use **single quotes** around the export line. Single quotes prevent the shell from expanding `$PATH` right now — you want the literal string written to the file so the shell expands it at login time against the then-current PATH value. Double quotes would expand `$PATH` immediately, hard-coding your current session's PATH into the file.
::

Confirm the line was written correctly:

```bash
grep 'opt/myapp/bin' ~/.bash_profile
```

::simple-task
---
:tasks: tasks
:name: verify_persisted_bash_profile
---
#active
Run `echo 'export PATH=/opt/myapp/bin:$PATH' >> ~/.bash_profile` to persist the change.

#completed
Export line written to ~/.bash_profile ✓
::

::hint-box
---
:summary: I accidentally added it to ~/.bashrc instead of ~/.bash_profile
---
On Rocky Linux 9, a graphical or non-login interactive shell reads `~/.bashrc`, while a login shell reads `~/.bash_profile`. For the RHCSA exam, the expected location for PATH persistence is `~/.bash_profile`. You can add the line to both files to cover all shell types, but always ensure `~/.bash_profile` has it. Check with: `grep opt/myapp/bin ~/.bashrc ~/.bash_profile`
::

---

## Step 5 — Verify the Change Survives a New Login Shell

Force Bash to re-read the login profile without fully logging out:

```bash
bash --login -c 'echo $PATH | tr ":" "\n"'
```

Look for `/opt/myapp/bin` in the output. This simulates exactly what happens when a new login session starts.

::simple-task
---
:tasks: tasks
:name: verify_login_shell_path
---
#active
Run `bash --login -c 'echo $PATH | tr ":" "\n"'` to verify the change loads in a new login shell.

#completed
Login shell test executed ✓
::

::simple-task
---
:tasks: tasks
:name: verify_path_contains_myapp
---
#active
Confirm that `/opt/myapp/bin` appears in the PATH of a login shell (the platform checks this automatically).

#completed
/opt/myapp/bin confirmed in login shell PATH ✓
::

::hint-box
---
:summary: The login shell output does not show /opt/myapp/bin
---
Run `bash -n ~/.bash_profile` to check for syntax errors in the file. If the command reports an error, open the file and fix the offending line. If there are no syntax errors but the directory is still missing, verify the exact content of the file with `cat ~/.bash_profile` and confirm the export line reads exactly: `export PATH=/opt/myapp/bin:$PATH`
::

---

## Final Verification

Confirm the directory is present and in the expected position:

```bash
echo $PATH | tr ':' '\n' | grep -n '/opt/myapp/bin'
```

A low line number (e.g., `1`) means the directory was prepended and will be searched first. A high line number means it was appended.

Confirm the command in the added directory is now found by the shell:

```bash
type mycommand
```

Expected output:

```
mycommand is /opt/myapp/bin/mycommand
```

---

## Troubleshooting Reference

| Problem | Cause | Solution |
|---|---|---|
| Command still not found after adding directory | Typo in path or export not saved | Run `echo $PATH \| tr ':' '\n'` and confirm the exact path appears |
| Change lost after opening a new terminal | Export in `~/.bashrc` instead of `~/.bash_profile`, or terminal opens a non-login shell | Verify the export line is in `~/.bash_profile`; for non-login interactive shells, also add it to `~/.bashrc` |
| New login shell does not pick up the change | `~/.bash_profile` not saved, or syntax error aborted loading | Run `bash -n ~/.bash_profile` to check for syntax errors |
| Prepended directory is still searched after `/usr/bin` | `$PATH` was omitted from the export, discarding the old value | Use `export PATH=/opt/myapp/bin:$PATH`, not `export PATH=/opt/myapp/bin` |
| Permission denied running a command in the added directory | Binary is not executable | Run `chmod +x /opt/myapp/bin/mycommand` |

---

## What You Did

1. Inspected `$PATH` and read its directories one per line with `tr`
2. Checked whether a target directory was already present before modifying anything
3. Added a directory for the current session with `export PATH=...`
4. Persisted the change in `~/.bash_profile` using single-quoted `echo` redirection
5. Verified the change loads in a new login shell with `bash --login -c '...'`

These five steps are exactly what the RHCSA exam expects when you are asked to make a custom binary available by name without specifying its full path.

::remark-box
---
kind: info
---
**Exam tip:** On the RHCSA, `~/.bash_profile` is the correct file for login-shell PATH changes. If you are unsure whether the exam shell is a login shell or a non-login interactive shell, add the export line to **both** `~/.bash_profile` and `~/.bashrc` to be safe.
::
```