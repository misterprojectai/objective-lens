---
title: "Read and Set Shell Variables"
type: tutorial
exam_objective: x200_101
tutorial_index: 4
version: "1.0"
status: draft
---

# Read and Set Shell Variables

In this tutorial, we will read common environment variables, define our own shell variables, export them to child processes, and verify that child processes inherit the values we set. Along the way, we will work with `echo`, `env`, `export`, and `bash`.

---

## Prerequisites

Before starting, ensure you have:

- A shell prompt on a RHEL system (as a regular user — not root)
- Completion of Tutorial 3, or comfort issuing basic commands at the prompt

---

## What We'll Build

By the end of this tutorial, we will have read several built-in environment variables, created a custom shell variable, exported it, and confirmed that a child shell inherits it. The terminal will be in this state:

```
[student@rhel ~]$ echo $MYGREETING
Hello RHCSA
[student@rhel ~]$ bash -c 'echo $MYGREETING'
Hello RHCSA
```

---

## Step 1: Read Three Built-in Environment Variables

First, we use `echo` to read the values of three variables that the shell provides automatically.

```bash
echo $USER
```

You should see:

```
student
```

```bash
echo $SHELL
```

You should see:

```
/bin/bash
```

```bash
echo $PATH
```

You should see output similar to:

```
/home/student/.local/bin:/home/student/bin:/usr/local/bin:/usr/bin:/bin
```

Notice that each variable name is prefixed with `$` — that is the signal to the shell to substitute the variable's value before the command runs.

---

## Step 2: List All Environment Variables with env

Now that we have read individual variables, we use `env` to display every variable currently exported to the environment.

```bash
env
```

You should see several lines of output similar to:

```
SHELL=/bin/bash
HOME=/home/student
USER=student
PATH=/home/student/.local/bin:/home/student/bin:/usr/local/bin:/usr/bin:/bin
LANG=en_US.UTF-8
```

Notice that `USER`, `SHELL`, and `PATH` — the variables we just read — appear in this list. Everything shown here is inherited by any command this shell launches.

---

## Step 3: Create a Shell Variable

Now that we can read existing variables, we define our own.

```bash
MYGREETING="Hello RHCSA"
```

You should see:

```
[student@rhel ~]$
```

No output is produced — the shell accepts the assignment silently. We confirm the value is set:

```bash
echo $MYGREETING
```

You should see:

```
Hello RHCSA
```

Notice that `MYGREETING` is now available to this shell, but it has not yet been exported. A child process cannot see it yet.

---

## Step 4: Confirm the Variable Is Not Yet Inherited

Now that we have defined `MYGREETING`, we check what a child shell sees before we export it.

```bash
bash -c 'echo $MYGREETING'
```

You should see:

```

```

The output is an empty line. The child shell (`bash -c`) has no knowledge of `MYGREETING` because we have not exported it yet.

---

## Step 5: Export the Variable

Now that we have confirmed the variable is invisible to child processes, we export it.

```bash
export MYGREETING
```

You should see:

```
[student@rhel ~]$
```

Again, no output — the shell accepts the export silently. The variable is now marked for inclusion in the environment of every child process this shell launches.

---

## Step 6: Verify Inheritance in a Child Process

Now that `MYGREETING` is exported, we confirm that a child shell inherits it.

```bash
bash -c 'echo $MYGREETING'
```

You should see:

```
Hello RHCSA
```

Notice that the same value we set in the parent shell is now visible inside the child shell — this is environment inheritance in action.

---

## Step 7: Confirm the Complete Final State

Finally, we verify the complete state matches what we set out to build.

```bash
echo $MYGREETING
```

You should see:

```
Hello RHCSA
```

```bash
bash -c 'echo $MYGREETING'
```

You should see:

```
Hello RHCSA
```

Both the parent shell and the child shell return the value we defined. The system is in the state we described in **What We'll Build**.

---

## What We Accomplished

In this tutorial, we:

1. Read the values of built-in environment variables `$USER`, `$SHELL`, and `$PATH` using `echo`
2. Listed all exported environment variables using `env`
3. Defined a new shell variable `MYGREETING` with an assigned value
4. Confirmed that an unexported variable is invisible to child processes
5. Exported `MYGREETING` using `export`
6. Verified that a child process launched with `bash -c` inherits the exported variable

---

## Next Steps

Now that you have read and set shell variables, you might want to:

- [How-to: Persist Environment Variables Across Sessions](#) — make variables survive logout by writing them to `~/.bash_profile`
- [Explanation: Understanding the Linux Shell and Command Syntax](#) — understand why exported variables propagate to child processes but not to parent processes
- [Reference: Bash Command Syntax and Options](#) — see complete syntax for variable assignment, `export`, `env`, and `echo`