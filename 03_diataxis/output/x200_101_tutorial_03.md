---
title: "Trace How the Shell Finds Commands"
type: tutorial
exam_objective: x200_101
tutorial_index: 3
version: "1.0"
status: draft
---

# Trace How the Shell Finds Commands

In this tutorial, we will trace exactly how Bash resolves a command name into something it can execute. Along the way, we will read and interpret `$PATH`, use `type` and `which` to locate commands, and distinguish shell builtins from external executables.

---

## Prerequisites

Before starting, ensure you have:

- A working Bash shell prompt on an RHEL system (covered in Tutorial 1)
- Ability to type commands and read their output (covered in Tutorial 2)

---

## What We'll Build

By the end of this tutorial, we will have traced the full resolution path for four commands — one builtin, one external, one alias, and one that does not exist. The terminal will show this verified state:

```
$ type cd
cd is a shell builtin
$ type ls
ls is aliased to `ls --color=auto'
$ type cat
cat is /usr/bin/cat
$ type foobar
bash: type: foobar: not found
$ echo $PATH
/home/student/.local/bin:/home/student/bin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin
$ which cat
/usr/bin/cat
```

---

## Step 1: Display the Current $PATH

First, we display the `$PATH` variable to see where the shell looks for commands.

```bash
echo $PATH
```

You should see:

```
/home/student/.local/bin:/home/student/bin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin
```

Notice that each directory is separated by a colon. When you type a command name, the shell searches these directories from left to right, stopping as soon as it finds a match.

---

## Step 2: Read $PATH as a List

Now that we have the raw value, we make it readable by replacing each colon with a newline.

```bash
echo $PATH | tr ':' '\n'
```

You should see:

```
/home/student/.local/bin
/home/student/bin
/usr/local/bin
/usr/bin
/usr/local/sbin
/usr/sbin
```

Notice that `/usr/bin` appears early in the list — this is where most standard commands such as `cat`, `ls`, and `grep` live on RHEL.

---

## Step 3: Identify a Shell Builtin

Now that we understand what `$PATH` contains, we check whether `cd` is found there.

```bash
type cd
```

You should see:

```
cd is a shell builtin
```

Notice that the shell did not search `$PATH` at all — `cd` is implemented inside Bash itself. The shell reports this immediately, before any directory lookup occurs.

---

## Step 4: Identify an External Executable

Next, we check a command that does live on the filesystem.

```bash
type cat
```

You should see:

```
cat is /usr/bin/cat
```

Notice that the shell reports the full path to the executable. This tells us exactly which file ran when we typed `cat` — the shell found it in `/usr/bin`, the third directory in our `$PATH` list.

---

## Step 5: Identify an Alias

Now we check `ls`, which behaves differently from a plain executable on RHEL.

```bash
type ls
```

You should see:

```
ls is aliased to `ls --color=auto'
```

Notice that the shell resolved `ls` to an alias before checking `$PATH`. When we type `ls`, Bash expands it to `ls --color=auto` first, then locates the `ls` executable. This is why directory names appear in colour by default.

---

## Step 6: Confirm a Command's Location with which

Now that `type` has shown us the resolved path for `cat`, we use `which` to confirm that location independently.

```bash
which cat
```

You should see:

```
/usr/bin/cat
```

Notice that `which` searches only `$PATH` directories and reports only the file path — it does not tell us whether a command is a builtin or an alias. That is why we use `type` for full resolution and `which` when we need the filesystem path only.

---

## Step 7: Observe a Command That Cannot Be Found

Finally, we ask the shell to resolve a name that does not exist anywhere in its resolution sequence.

```bash
type foobar
```

You should see:

```
bash: type: foobar: not found
```

Notice that the shell reports `not found` rather than a file path. The shell checked builtins, aliases, and every directory in `$PATH` in order — and found nothing. This is the same error mechanism behind `command not found` messages.

---

## Step 8: Verify the Complete State

Finally, we run all four `type` checks and the `echo $PATH` together to confirm the state matches what we set out to achieve.

```bash
type cd
type ls
type cat
type foobar
echo $PATH
which cat
```

You should see:

```
cd is a shell builtin
ls is aliased to `ls --color=auto'
cat is /usr/bin/cat
bash: type: foobar: not found
/home/student/.local/bin:/home/student/bin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin
/usr/bin/cat
```

---

## What We Accomplished

In this tutorial, we:

1. Displayed and read `$PATH` to see the ordered list of directories the shell searches
2. Used `type` to classify `cd` as a shell builtin, `ls` as an alias, and `cat` as an external executable
3. Used `which` to confirm the filesystem location of an external command
4. Observed the shell's `not found` response when no match exists at any stage of resolution

---

## Next Steps

Now that you have traced how the shell resolves commands, you might want to:

- [How-to: Modify $PATH to Add a Custom Command Directory](#) — apply this knowledge to make your own tools available as simple commands
- [Explanation: Understanding the Linux Shell and Command Syntax](#) — understand why builtins must live inside the shell and cannot be external programs
- [Reference: Bash Command Syntax and Options](#) — see the complete resolution order and all `type` output formats