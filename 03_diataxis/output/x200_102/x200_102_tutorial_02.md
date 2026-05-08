---
title: "Redirect stdin from a File with <"
type: tutorial
quadrant:
  practical_theoretical: practical
  work_study: study
exam_objective: x200_102
tutorial_index: 2
version: "1.0"
status: draft
---

# Redirect stdin from a File with <

In this tutorial, we will supply file content as standard input to a command using the `<` operator. Along the way, we will create a text file, redirect it into `wc`, and confirm that the command reads from the file rather than the keyboard.

---

## Prerequisites

Before starting, ensure you have:

- A terminal session on a RHEL 9 system (local or remote)
- Ability to run commands as a regular user — no root required

---

## What We'll Build

By the end of this tutorial, we will have created a text file and fed it to two commands using `<`. The final verification will show this state:

```
$ wc -l < ~/words.txt
5
$ sort < ~/words.txt
apple
banana
cherry
date
elderberry
```

---

## Step 1: Create a file to use as input

First, we create a small text file that we will redirect into commands in the steps that follow.

```bash
printf 'cherry\nbanana\ndate\napple\nelderberry\n' > ~/words.txt
```

You should see:

```
(no output)
```

The shell creates `~/words.txt` and writes five fruit names, one per line. No output on screen means the redirection worked correctly.

---

## Step 2: Confirm the file exists and contains five lines

Now that we have `~/words.txt`, we verify its contents before redirecting it anywhere.

```bash
cat ~/words.txt
```

You should see:

```
cherry
banana
date
apple
elderberry
```

Notice that the five lines appear in the order we wrote them — unsorted, exactly as entered.

---

## Step 3: Count lines by redirecting the file into wc

Now we redirect `~/words.txt` into `wc -l`. The `<` operator connects the file to `wc`'s standard input instead of the keyboard.

```bash
wc -l < ~/words.txt
```

You should see:

```
5
```

Notice that `wc` reports the count without printing a filename. When `wc` reads from standard input — whether keyboard or file — it has no filename to display, so only the number appears.

---

## Step 4: Sort the file by redirecting it into sort

Now that we have confirmed `wc` reads from the redirected file, we pass the same file to `sort` using `<`.

```bash
sort < ~/words.txt
```

You should see:

```
apple
banana
cherry
date
elderberry
```

Notice that `sort` receives the five lines from the file and returns them in alphabetical order. The original file is unchanged — `sort` only reads from it.

---

## Step 5: Verify the original file is unchanged

Finally, we verify the complete system state — the file still contains the original, unsorted content, and both redirect operations produced their expected results without modifying it.

```bash
cat ~/words.txt
```

You should see:

```
cherry
banana
date
apple
elderberry
```

The file content is identical to what we saw in Step 2. Redirecting a file into a command as standard input never modifies the source file.

---

## What We Accomplished

In this tutorial, we:

1. Created a five-line text file using `printf` and output redirection
2. Confirmed the file contents with `cat`
3. Redirected the file into `wc -l` using `<` to count lines without typing a filename argument
4. Redirected the same file into `sort` using `<` to produce alphabetically ordered output
5. Verified that the source file remained unchanged after both redirect operations

---

## Next Steps

Now that you can redirect standard input from a file, you might want to:

- [How-to: Redirect Command Output in Common Administrative Tasks](#) — apply input and output redirection together in real administration scenarios
- [Understanding I/O Redirection and Pipelines](#) — learn why the shell substitutes file descriptors before a command starts, and what that means for `<`, `>`, and `|`
- [Reference: I/O Redirection Operators and File Descriptors](#) — see the complete syntax for all redirection operators including `0<` and its equivalents