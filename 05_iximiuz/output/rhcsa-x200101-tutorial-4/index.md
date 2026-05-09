---
kind: tutorial

title: Read and Set Shell Variables

description: |
  Practice reading built-in environment variables, creating your own shell variables,
  exporting them to child processes, and verifying inheritance — essential skills
  for the RHCSA EX200 exam.

categories:
  - linux

tagz:
  - rhcsa
  - bash
  - shell

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

  verify_echo_user:
    machine: rocky-01
    user: laborant
    run: |
      grep -q 'echo $USER\|echo \$USER' /home/laborant/.bash_history && exit 0 || exit 1
    hintcheck: |
      echo "Run: echo \$USER"

  verify_echo_shell:
    machine: rocky-01
    user: laborant
    run: |
      grep -q 'echo $SHELL\|echo \$SHELL' /home/laborant/.bash_history && exit 0 || exit 1
    hintcheck: |
      echo "Run: echo \$SHELL"

  verify_echo_path:
    machine: rocky-01
    user: laborant
    run: |
      grep -q 'echo $PATH\|echo \$PATH' /home/laborant/.bash_history && exit 0 || exit 1
    hintcheck: |
      echo "Run: echo \$PATH"

  verify_env_ran:
    machine: rocky-01
    user: laborant
    run: |
      grep -qx 'env' /home/laborant/.bash_history && exit 0 || exit 1
    hintcheck: |
      echo "Run: env"

  verify_mygreeting_set:
    machine: rocky-01
    user: laborant
    run: |
      grep -q 'MYGREETING' /home/laborant/.bash_history && exit 0 || exit 1
    hintcheck: |
      echo 'Run: MYGREETING="Hello RHCSA"'

  verify_mygreeting_exported:
    machine: rocky-01
    user: laborant
    run: |
      grep -q 'export MYGREETING' /home/laborant/.bash_history && exit 0 || exit 1
    hintcheck: |
      echo "Run: export MYGREETING"

  verify_child_inheritance:
    machine: rocky-01
    user: laborant
    run: |
      grep -q "bash -c 'echo \$MYGREETING'" /home/laborant/.bash_history && exit 0 || exit 1
    hintcheck: |
      echo "Run: bash -c 'echo \$MYGREETING'"
---
```

# Read and Set Shell Variables

In this tutorial, you will read common environment variables, define your own shell variable, export it to child processes, and verify that child processes inherit the value you set. Along the way you will work with `echo`, `env`, `export`, and `bash`.

These skills appear directly on the RHCSA EX200 exam — understanding the difference between a shell variable and an exported environment variable is tested both in isolation and as a prerequisite for configuring services and scripts.

::remark-box
---
kind: info
---
**Before running any commands:** click the **+** button in the terminal tab bar to open a new terminal tab. The playground history tracking activates in new sessions only. Commands run in the original tab will not register for task verification.
::

---

## What You Will Build

By the end of this tutorial, the terminal will be in this state:

```
[laborant@rocky-01 ~]$ echo $MYGREETING
Hello RHCSA
[laborant@rocky-01 ~]$ bash -c 'echo $MYGREETING'
Hello RHCSA
```

Both the parent shell and a child shell return the value you defined — this is environment inheritance in action.

---

## Step 1: Read Three Built-in Environment Variables

The shell provides a set of variables automatically. Use `echo` to read three of them.

```bash
echo $USER
```

Expected output:

```
laborant
```

```bash
echo $SHELL
```

Expected output:

```
/bin/bash
```

```bash
echo $PATH
```

Expected output (similar to):

```
/home/laborant/.local/bin:/home/laborant/bin:/usr/local/bin:/usr/bin:/bin
```

Each variable name is prefixed with `$` — that is the signal to the shell to substitute the variable's value before the command runs.

::remark-box
---
kind: info
---
`$USER`, `$SHELL`, and `$PATH` are **environment variables** — they were exported by the login session and are visible to every command this shell launches.
::

::simple-task
---
:tasks: tasks
:name: verify_echo_user
---
#active
Run `echo $USER` and observe your username.

#completed
Done — `$USER` read successfully ✓
::

::simple-task
---
:tasks: tasks
:name: verify_echo_shell
---
#active
Run `echo $SHELL` and observe the path to your shell binary.

#completed
Done — `$SHELL` read successfully ✓
::

::simple-task
---
:tasks: tasks
:name: verify_echo_path
---
#active
Run `echo $PATH` and observe the colon-separated list of directories.

#completed
Done — `$PATH` read successfully ✓
::

---

## Step 2: List All Environment Variables with `env`

Now use `env` to display every variable currently exported to the environment.

```bash
env
```

You will see many lines. Look for the variables you just read:

```
SHELL=/bin/bash
HOME=/home/laborant
USER=laborant
PATH=/home/laborant/.local/bin:/home/laborant/bin:/usr/local/bin:/usr/bin:/bin
LANG=en_US.UTF-8
```

Everything shown here is inherited by any command this shell launches.

::hint-box
---
:summary: I see too many lines — how do I find a specific variable?
---
Pipe `env` through `grep`:

```bash
env | grep PATH
```

This filters the output to lines that contain `PATH`.
::

::simple-task
---
:tasks: tasks
:name: verify_env_ran
---
#active
Run `env` to list all exported environment variables.

#completed
Done — `env` output reviewed ✓
::

---

## Step 3: Create a Shell Variable

Define your own variable.

```bash
MYGREETING="Hello RHCSA"
```

No output is produced — the shell accepts the assignment silently. Confirm the value is set:

```bash
echo $MYGREETING
```

Expected output:

```
Hello RHCSA
```

::remark-box
---
kind: warning
---
`MYGREETING` is now a **shell variable** — it lives only in this shell session. It has **not** been exported, so a child process cannot see it yet.
::

::simple-task
---
:tasks: tasks
:name: verify_mygreeting_set
---
#active
Run `MYGREETING="Hello RHCSA"` to create the shell variable, then confirm with `echo $MYGREETING`.

#completed
Done — `MYGREETING` is defined ✓
::

---

## Step 4: Confirm the Variable Is Not Yet Inherited

Check what a child shell sees before you export `MYGREETING`.

```bash
bash -c 'echo $MYGREETING'
```

Expected output:

```

```

The output is an empty line. The child shell has no knowledge of `MYGREETING` because it has not been exported yet.

::hint-box
---
:summary: Why does the child shell print nothing?
---
When bash starts a child process, it only passes **exported** variables into that child's environment. A plain assignment like `MYGREETING="Hello RHCSA"` marks the variable as local to the current shell. The child shell receives no value for `MYGREETING`, so `$MYGREETING` expands to an empty string.
::

---

## Step 5: Export the Variable

Mark `MYGREETING` for inclusion in the environment of every child process this shell launches.

```bash
export MYGREETING
```

Again, no output — the shell accepts the export silently.

::remark-box
---
kind: info
---
You can combine assignment and export in a single step: `export MYGREETING="Hello RHCSA"`. Both forms are valid and appear on the exam.
::

::simple-task
---
:tasks: tasks
:name: verify_mygreeting_exported
---
#active
Run `export MYGREETING` to promote the variable to an environment variable.

#completed
Done — `MYGREETING` is now exported ✓
::

---

## Step 6: Verify Inheritance in a Child Process

Now that `MYGREETING` is exported, confirm that a child shell inherits it.

```bash
bash -c 'echo $MYGREETING'
```

Expected output:

```
Hello RHCSA
```

The same value you set in the parent shell is now visible inside the child shell — this is environment inheritance.

::simple-task
---
:tasks: tasks
:name: verify_child_inheritance
---
#active
Run `bash -c 'echo $MYGREETING'` and confirm the child shell prints `Hello RHCSA`.

#completed
Done — child process inherited `MYGREETING` ✓
::

---

## Step 7: Confirm the Complete Final State

Verify both the parent shell and a child shell return the expected value.

```bash
echo $MYGREETING
```

Expected output:

```
Hello RHCSA
```

```bash
bash -c 'echo $MYGREETING'
```

Expected output:

```
Hello RHCSA
```

Both commands return `Hello RHCSA` — the system is in the state described at the top of this tutorial.

::remark-box
---
kind: info
---
**Exam tip:** The export does **not** propagate upward. If you start a child shell, set a variable there, and export it, the parent shell will never see it. Variables flow **down** to children, never up to parents.
::

---

## What You Accomplished

In this tutorial, you:

1. Read the values of built-in environment variables `$USER`, `$SHELL`, and `$PATH` using `echo`
2. Listed all exported environment variables using `env`
3. Defined a new shell variable `MYGREETING` with an assigned value
4. Confirmed that an unexported variable is invisible to child processes
5. Exported `MYGREETING` using `export`
6. Verified that a child process launched with `bash -c` inherits the exported variable

::details-box
---
:summary: Why does export work this way?
---
Unix processes are created with `fork()` — the child receives a **copy** of the parent's environment at the moment of creation. The operating system copies only the exported variables table into the new process image. Changes made in the child after fork do not affect the parent, and variables that were never exported are never included in the copy.

This is why login shell configuration files (`~/.bash_profile`, `/etc/profile`) use `export` — any variable they want subshells and programs to see must be explicitly placed in the environment.
::

---

## Next Steps

- **Persist variables across sessions** — write `export MYGREETING="Hello RHCSA"` into `~/.bash_profile` and verify it survives logout
- **Unset a variable** — try `unset MYGREETING` and confirm `echo $MYGREETING` returns an empty line
- **Inspect a variable's export status** — run `declare -p MYGREETING` before and after `export` and compare the flags shown