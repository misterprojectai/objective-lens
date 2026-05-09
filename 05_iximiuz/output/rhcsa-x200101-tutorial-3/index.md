---
kind: tutorial

title: "Trace How the Shell Finds Commands"

description: |
  Learn exactly how Bash resolves a command name into something it can execute.
  Read and interpret $PATH, use `type` and `which` to locate commands, and
  distinguish shell builtins from external executables — essential RHCSA skills.

categories:
  - linux

tagz:
  - rhcsa
  - bash
  - shell
  - grep
  - permissions

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

  verify_echo_path:
    machine: rocky-01
    user: laborant
    run: |
      grep -q 'echo $PATH\|echo \$PATH' /home/laborant/.bash_history && exit 0 || exit 1
    hintcheck: |
      echo "Run: echo \$PATH"

  verify_tr_path:
    machine: rocky-01
    user: laborant
    run: |
      grep -q "tr ':' '\\\\n'\|tr \":\" \"\\\\n\"" /home/laborant/.bash_history && exit 0 || exit 1
    hintcheck: |
      echo "Run: echo \$PATH | tr ':' '\n'"

  verify_type_cd:
    machine: rocky-01
    user: laborant
    run: |
      grep -q 'type cd' /home/laborant/.bash_history && exit 0 || exit 1
    hintcheck: |
      echo "Run: type cd"

  verify_type_cat:
    machine: rocky-01
    user: laborant
    run: |
      grep -q 'type cat' /home/laborant/.bash_history && exit 0 || exit 1
    hintcheck: |
      echo "Run: type cat"

  verify_type_ls:
    machine: rocky-01
    user: laborant
    run: |
      grep -q 'type ls' /home/laborant/.bash_history && exit 0 || exit 1
    hintcheck: |
      echo "Run: type ls"

  verify_which_cat:
    machine: rocky-01
    user: laborant
    run: |
      grep -q 'which cat' /home/laborant/.bash_history && exit 0 || exit 1
    hintcheck: |
      echo "Run: which cat"

  verify_type_foobar:
    machine: rocky-01
    user: laborant
    run: |
      grep -q 'type foobar' /home/laborant/.bash_history && exit 0 || exit 1
    hintcheck: |
      echo "Run: type foobar"
---

# Trace How the Shell Finds Commands

In this tutorial, you will trace exactly how Bash resolves a command name into something it can execute. Along the way, you will read and interpret `$PATH`, use `type` and `which` to locate commands, and distinguish shell builtins from external executables.

::remark-box
---
kind: info
---
**Before running any commands:** click the **+** button in the terminal tab bar to open a new terminal tab. The playground history tracking activates in new sessions only. Commands run in the original tab will not register for task verification.
::

---

## Prerequisites

Before starting, ensure you have:

- A working Bash shell prompt (you are logged in as `laborant` on `rocky-01`)
- Ability to type commands and read their output

---

## What You Will Build

By the end of this tutorial, you will have traced the full resolution path for four commands — one builtin, one external, one alias, and one that does not exist. The terminal will show this verified state:

```
[laborant@rocky-01 ~]$ type cd
cd is a shell builtin
[laborant@rocky-01 ~]$ type ls
ls is aliased to `ls --color=auto'
[laborant@rocky-01 ~]$ type cat
cat is /usr/bin/cat
[laborant@rocky-01 ~]$ type foobar
bash: type: foobar: not found
[laborant@rocky-01 ~]$ echo $PATH
/home/laborant/.local/bin:/home/laborant/bin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin
[laborant@rocky-01 ~]$ which cat
/usr/bin/cat
```

---

## Step 1 — Display the Current $PATH

First, display the `$PATH` variable to see where the shell looks for commands.

```bash
echo $PATH
```

You should see something like:

```
/home/laborant/.local/bin:/home/laborant/bin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin
```

Each directory is separated by a colon. When you type a command name, the shell searches these directories **from left to right**, stopping as soon as it finds a match.

::remark-box
---
kind: info
---
`$PATH` is an environment variable — the dollar sign tells Bash to substitute its value. Without the `$`, you would literally print the string `PATH`.
::

::simple-task
---
:tasks: tasks
:name: verify_echo_path
---
#active
Run `echo $PATH` and observe the colon-separated list of directories.

#completed
Done — you displayed `$PATH` successfully 🎉
::

---

## Step 2 — Read $PATH as a List

Now make the raw value readable by replacing each colon with a newline.

```bash
echo $PATH | tr ':' '\n'
```

You should see each directory on its own line:

```
/home/laborant/.local/bin
/home/laborant/bin
/usr/local/bin
/usr/bin
/usr/local/sbin
/usr/sbin
```

Notice that `/usr/bin` appears early in the list — this is where most standard commands such as `cat`, `ls`, and `grep` live on Rocky Linux (and RHEL).

::remark-box
---
kind: info
---
`tr` is the **translate** command. Here it reads from standard input (the output of `echo $PATH`) and replaces every `:` character with a newline character `\n`, printing each directory on a separate line.
::

::simple-task
---
:tasks: tasks
:name: verify_tr_path
---
#active
Run `echo $PATH | tr ':' '\n'` to display each PATH directory on its own line.

#completed
Done — you split `$PATH` into a readable list 🎉
::

---

## Step 3 — Identify a Shell Builtin

Now that you understand what `$PATH` contains, check whether `cd` is found there.

```bash
type cd
```

You should see:

```
cd is a shell builtin
```

The shell did **not** search `$PATH` at all — `cd` is implemented inside Bash itself. The shell reports this immediately, before any directory lookup occurs.

::remark-box
---
kind: warning
---
**Exam relevance:** `cd` cannot exist as an external program. Changing the current directory must happen inside the shell process itself — an external program would run in a child process and its directory change would not affect the parent shell. Knowing this distinction can appear in RHCSA questions about shell behaviour.
::

::simple-task
---
:tasks: tasks
:name: verify_type_cd
---
#active
Run `type cd` and observe that it reports `cd is a shell builtin`.

#completed
Done — you confirmed `cd` is a shell builtin 🎉
::

---

## Step 4 — Identify an External Executable

Next, check a command that does live on the filesystem.

```bash
type cat
```

You should see:

```
cat is /usr/bin/cat
```

The shell reports the full path to the executable. This tells you exactly which file ran when you typed `cat` — the shell found it in `/usr/bin`, one of the directories in your `$PATH` list.

::simple-task
---
:tasks: tasks
:name: verify_type_cat
---
#active
Run `type cat` and observe the full filesystem path reported.

#completed
Done — you located `cat` as an external executable 🎉
::

---

## Step 5 — Identify an Alias

Now check `ls`, which behaves differently from a plain executable on Rocky Linux.

```bash
type ls
```

You should see:

```
ls is aliased to `ls --color=auto'
```

The shell resolved `ls` to an alias **before** checking `$PATH`. When you type `ls`, Bash expands it to `ls --color=auto` first, then locates the `ls` executable. This is why directory names appear in colour by default.

::remark-box
---
kind: info
---
**Resolution order:** Bash resolves command names in this order: aliases → functions → builtins → `$PATH` directories. The `type` command shows you at which stage the match was found.
::

::simple-task
---
:tasks: tasks
:name: verify_type_ls
---
#active
Run `type ls` and observe that it reports `ls is aliased to 'ls --color=auto'`.

#completed
Done — you confirmed `ls` is an alias 🎉
::

---

## Step 6 — Confirm a Command's Location with `which`

Now that `type` has shown the resolved path for `cat`, use `which` to confirm that location independently.

```bash
which cat
```

You should see:

```
/usr/bin/cat
```

`which` searches only `$PATH` directories and reports only the file path — it does **not** tell you whether a command is a builtin or an alias. That is why you use `type` for full resolution and `which` when you need the filesystem path specifically.

::hint-box
---
:summary: "`which` returns nothing or an unexpected path"
---
If `which cat` returns nothing, your `$PATH` may be minimal (e.g., in a restricted shell). Try `type cat` first — if it shows the path, your `PATH` is fine. If `which` still fails, install the `which` package: `sudo dnf install -y which`.
::

::simple-task
---
:tasks: tasks
:name: verify_which_cat
---
#active
Run `which cat` and confirm it prints `/usr/bin/cat`.

#completed
Done — you confirmed `cat`'s filesystem location with `which` 🎉
::

---

## Step 7 — Observe a Command That Cannot Be Found

Finally, ask the shell to resolve a name that does not exist anywhere in its resolution sequence.

```bash
type foobar
```

You should see:

```
bash: type: foobar: not found
```

The shell reports `not found` rather than a file path. The shell checked builtins, aliases, and every directory in `$PATH` in order — and found nothing. This is the same error mechanism behind the familiar `command not found` messages.

::remark-box
---
kind: info
---
The exit code of `type foobar` is **non-zero** (1). Scripts and conditions can use this: `if type somecmd &>/dev/null; then ...` is a portable way to test whether a command is available before using it.
::

::simple-task
---
:tasks: tasks
:name: verify_type_foobar
---
#active
Run `type foobar` and observe the `not found` response.

#completed
Done — you observed the shell's `not found` response 🎉
::

---

## Step 8 — Verify the Complete State

Run all checks together to confirm everything matches the goal state established at the start.

```bash
type cd
type ls
type cat
type foobar
echo $PATH
which cat
```

Expected output:

```
cd is a shell builtin
ls is aliased to `ls --color=auto'
cat is /usr/bin/cat
bash: type: foobar: not found
/home/laborant/.local/bin:/home/laborant/bin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin
/usr/bin/cat
```

All seven results confirm the complete resolution chain: alias → builtin → external executable → not found.

---

## What You Accomplished

In this tutorial, you:

1. Displayed and read `$PATH` to see the ordered list of directories the shell searches
2. Used `tr` to split `$PATH` into a readable per-line list
3. Used `type` to classify `cd` as a shell builtin, `ls` as an alias, and `cat` as an external executable
4. Used `which` to confirm the filesystem location of an external command
5. Observed the shell's `not found` response when no match exists at any stage of resolution

::remark-box
---
kind: info
---
**RHCSA exam tip:** On the exam, `type <command>` is the fastest way to diagnose why a command behaves unexpectedly — it tells you immediately whether you are running an alias, a function, a builtin, or an external binary. `which` is useful when you need to verify the exact file that will execute.
::

---

## Next Steps

Now that you have traced how the shell resolves commands, you might want to explore:

- **Modify `$PATH` to add a custom command directory** — apply this knowledge to make your own tools available as simple commands
- **Understanding shell builtins vs. external commands** — understand why builtins must live inside the shell and cannot be external programs
- **Bash command resolution order in detail** — see the complete resolution order including shell functions and keyword handling
```