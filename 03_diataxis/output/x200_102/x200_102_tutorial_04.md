---
title: "Combine stdout and stderr into a Single Destination"
type: tutorial
quadrant:
  practical_theoretical: practical
  work_study: study
exam_objective: x200_102
tutorial_index: 4
version: "1.0"
status: draft
---

# Combine stdout and stderr into a Single Destination

In this tutorial, we will capture both stdout and stderr into a single file using two different forms: `&>` and `> file 2>&1`. Along the way, we will work with a command that produces both kinds of output simultaneously, observe the ordering difference between the two forms, and confirm the result in each case.

---

## Prerequisites

Before starting, ensure you have:

- A RHEL 9 (or compatible) terminal session with a regular user account
- Completion of Tutorial 3, or familiarity with redirecting stdout and stderr separately with `>` and `2>`

---

## What We'll Build

By the end of this tutorial, you will have run the same command four times — twice with `&>` and twice with `> file 2>&1` — and confirmed that both forms capture all output into a single file. The system will be in this state:

```
$ cat combined.txt
/etc/hosts
ls: cannot access '/no/such/path': No such file or directory

$ cat combined2.txt
/etc/hosts
ls: cannot access '/no/such/path': No such file or directory
```

Both files contain identical content: one line of normal output followed by one error message.

---

## Step 1: Create a command that produces both stdout and stderr

First, we need a command that generates both streams at once. We will use `ls` with one valid path and one invalid path — the valid path produces stdout, and the invalid path produces stderr.

```bash
ls /etc/hosts /no/such/path
```

You should see:

```
ls: cannot access '/no/such/path': No such file or directory
/etc/hosts
```

Notice that both lines appear on the terminal. The error message and the normal result are mixed together on screen because both streams default to the terminal display.

---

## Step 2: Redirect both streams using `&>`

Now that we have a command producing both streams, we redirect everything to a single file using `&>`.

```bash
ls /etc/hosts /no/such/path &> combined.txt
```

You should see:

```
```

Nothing appears on the terminal. Both stdout and stderr have been captured into `combined.txt`.

---

## Step 3: Verify the contents of combined.txt

Now we read back what was captured.

```bash
cat combined.txt
```

You should see:

```
ls: cannot access '/no/such/path': No such file or directory
/etc/hosts
```

Notice that both the error message and the normal output are present in the file. Neither stream was lost.

---

## Step 4: Redirect both streams using `> file 2>&1`

Now we produce the same result using the older, explicit form. This form redirects stdout to the file first, then makes stderr point to wherever stdout is now pointing.

```bash
ls /etc/hosts /no/such/path > combined2.txt 2>&1
```

You should see:

```
```

Again, nothing appears on the terminal. Both streams have been captured.

---

## Step 5: Verify the contents of combined2.txt

```bash
cat combined2.txt
```

You should see:

```
ls: cannot access '/no/such/path': No such file or directory
/etc/hosts
```

Notice that the output is identical to `combined.txt`. Both operators achieve the same result for this command.

---

## Step 6: Observe the ordering difference — the wrong way

The `2>&1` form is sensitive to the order of redirections. We will now write the redirections in the wrong order and observe what happens.

```bash
ls /etc/hosts /no/such/path 2>&1 > combined3.txt
```

You should see:

```
ls: cannot access '/no/such/path': No such file or directory
```

The error message appears on the terminal rather than in the file. Only stdout was captured.

---

## Step 7: Verify that combined3.txt contains only stdout

```bash
cat combined3.txt
```

You should see:

```
/etc/hosts
```

Notice that only the normal output went into the file. When `2>&1` appears before `> file`, stderr is pointed at wherever stdout is at that moment — which is still the terminal. Then stdout is redirected to the file, but stderr has already been locked to the terminal. The `&>` form avoids this problem entirely because it sets both streams simultaneously.

---

## Step 8: Confirm the final state of all three files

Finally, we verify the complete state of what we have built.

```bash
cat combined.txt combined2.txt combined3.txt
```

You should see:

```
ls: cannot access '/no/such/path': No such file or directory
/etc/hosts
ls: cannot access '/no/such/path': No such file or directory
/etc/hosts
/etc/hosts
```

`combined.txt` and `combined2.txt` each hold both streams. `combined3.txt` holds only stdout — confirming the ordering difference in the explicit form.

---

## What We Accomplished

In this tutorial, we:

1. Ran a command that produced output on both stdout and stderr simultaneously
2. Captured both streams into a single file using the `&>` operator
3. Captured both streams into a single file using the `> file 2>&1` form
4. Demonstrated the ordering failure that occurs when `2>&1` is placed before `>` in the explicit form
5. Verified each result with `cat` to confirm what was captured and what was not

---

## Next Steps

Now that you have captured both output streams into a single destination, you might want to:

- [How-to: Redirect Command Output in Common Administrative Tasks](#) — apply combined redirection in logging and scripting patterns
- [Explanation: Understanding I/O Redirection and Pipelines](#) — understand why ordering matters in `> file 2>&1` and how the shell processes redirections left to right
- [Reference: I/O Redirection Operators and File Descriptors](#) — see the complete syntax for `&>`, `>&`, `&>>`, and `2>&1`