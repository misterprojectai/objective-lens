---
title: "Redirect stderr with 2> and Discard Output with /dev/null"
type: tutorial
quadrant:
  practical_theoretical: practical
  work_study: study
exam_objective: x200_102
tutorial_index: 3
version: "1.0"
status: draft
---

# Redirect stderr with 2> and Discard Output with /dev/null

In this tutorial, we will build the skill of isolating error output from normal output using `2>`, routing errors to a separate file, and silencing unwanted output with `/dev/null`. Along the way, we will work with file descriptor 2, the `/dev/null` device, and the combined redirection operator `&>`.

---

## Prerequisites

Before starting, ensure you have:

- A terminal logged in as a regular user on a RHEL 9 system
- A home directory you can write to
- Completion of Tutorial 1 (redirecting stdout with `>` and `>>`)

---

## What We'll Build

By the end of this tutorial, you will have run a command that produces both normal output and errors, captured each stream independently to its own file, and silenced all output using `/dev/null`. The system will be in this state:

```
~/tutorial3/
├── output.txt        (contains the /etc directory listing)
├── errors.txt        (contains the "permission denied" error messages)
└── combined.txt      (contains both stdout and stderr together)
```

---

## Step 1: Create a working directory

First, we create a dedicated directory for this tutorial and move into it.

```bash
mkdir ~/tutorial3 && cd ~/tutorial3
```

You should see:

```
(no output — the prompt returns)
```

This confirms the directory was created and is now our working location.

---

## Step 2: Observe a command that produces both stdout and stderr

Now that we have our working directory, we run a command that generates both normal output and error messages at the same time.

```bash
ls /etc /fake-directory-xyz
```

You should see something like:

```
ls: cannot access '/fake-directory-xyz': No such file or directory
/etc:
adjtime
aliases
alternatives
...
```

Notice that the error message and the directory listing both appear mixed together on the screen. Both streams are currently going to the same place — your terminal.

---

## Step 3: Redirect only stdout to a file

Now that we can see both streams mixed on the terminal, we redirect only the normal output — stdout — to a file, leaving errors on screen.

```bash
ls /etc /fake-directory-xyz > output.txt
```

You should see:

```
ls: cannot access '/fake-directory-xyz': No such file or directory
```

Notice that only the error message appeared. The directory listing went silently into `output.txt` because `>` redirects only stdout (file descriptor 1). The error message uses a different channel — file descriptor 2 — and was not redirected.

---

## Step 4: Confirm stdout was captured

We verify that the file received the normal output.

```bash
head -5 output.txt
```

You should see:

```
/etc:
adjtime
aliases
alternatives
audit
```

The normal output from `ls` is in the file. The error message never entered it.

---

## Step 5: Redirect only stderr to a file

Now we redirect only the error output — stderr — to its own file, using `2>`. The `2` is the file descriptor number for stderr.

```bash
ls /etc /fake-directory-xyz 2> errors.txt
```

You should see the directory listing scroll past on screen:

```
/etc:
adjtime
aliases
alternatives
...
```

Notice that no error message appeared this time. The error went to `errors.txt`, while the normal listing continued to the terminal.

---

## Step 6: Confirm stderr was captured

We verify that the errors file contains the error message.

```bash
cat errors.txt
```

You should see:

```
ls: cannot access '/fake-directory-xyz': No such file or directory
```

We have now captured stdout and stderr independently. The `2>` operator targets file descriptor 2 exclusively, leaving stdout undisturbed.

---

## Step 7: Redirect stdout and stderr to separate files simultaneously

Now we combine both redirections in a single command, sending each stream to its own file at the same time.

```bash
ls /etc /fake-directory-xyz > output.txt 2> errors.txt
```

You should see:

```
(no output — the prompt returns immediately)
```

Nothing appeared on screen because both streams were redirected away from the terminal.

---

## Step 8: Verify both files were written

We check both files to confirm each received the correct stream.

```bash
echo "=== output.txt ===" && head -3 output.txt && echo "=== errors.txt ===" && cat errors.txt
```

You should see:

```
=== output.txt ===
/etc:
adjtime
aliases
=== errors.txt ===
ls: cannot access '/fake-directory-xyz': No such file or directory
```

Each stream landed in its own file, cleanly separated.

---

## Step 9: Discard errors with /dev/null

Now we run the same command but silence the error output entirely by redirecting stderr to `/dev/null`, the system's discard device.

```bash
ls /etc /fake-directory-xyz 2> /dev/null
```

You should see the directory listing with no error message:

```
/etc:
adjtime
aliases
alternatives
...
```

The error message was sent to `/dev/null` and silently discarded. `/dev/null` accepts anything written to it and throws it away immediately.

---

## Step 10: Discard all output with &>

Now we redirect both stdout and stderr to `/dev/null` using the combined `&>` operator, producing complete silence.

```bash
ls /etc /fake-directory-xyz &> /dev/null
```

You should see:

```
(no output — the prompt returns immediately)
```

Both streams were discarded. The command ran, produced output and errors, and all of it was silently consumed by `/dev/null`.

---

## Step 11: Capture both streams together with &>

Finally, we redirect both stdout and stderr into a single file using `&>`.

```bash
ls /etc /fake-directory-xyz &> combined.txt
```

You should see:

```
(no output — the prompt returns immediately)
```

Now we verify the combined file contains both the error and the directory listing.

```bash
grep -E "cannot access|^/etc:" combined.txt
```

You should see:

```
ls: cannot access '/fake-directory-xyz': No such file or directory
/etc:
```

Both streams are present in the same file.

---

## Step 12: Verify the complete final state

Finally, we verify that all three files exist in our working directory, matching the state shown in "What We'll Build."

```bash
ls ~/tutorial3/
```

You should see:

```
combined.txt  errors.txt  output.txt
```

---

## What We Accomplished

In this tutorial, we:

1. Ran a command that produces both normal output and error messages simultaneously
2. Redirected only stdout to a file using `>`, observing that errors remained on screen
3. Redirected only stderr to a file using `2>`, observing that normal output remained on screen
4. Redirected stdout and stderr to separate files simultaneously in a single command
5. Discarded error output silently using `2> /dev/null`
6. Discarded all output using `&> /dev/null`
7. Captured both stdout and stderr together into a single file using `&>`

---

## Next Steps

Now that you can route stdout and stderr independently, you might want to:

- [How-to: Redirect Command Output in Common Administrative Tasks](#) — apply stderr redirection in real administration scenarios such as find and cron
- [Explanation: Understanding I/O Redirection and Pipelines](#) — understand why stdout and stderr are separate streams and what file descriptors are
- [Reference: I/O Redirection Operators and File Descriptors](#) — see the complete operator syntax including `2>>`, `&>>`, and `2>&1`