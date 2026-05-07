---
title: "Issue Commands with Correct Syntax"
type: tutorial
exam_objective: x200_101
tutorial_index: 2
version: "1.0"
status: draft
---

# Issue Commands with Correct Syntax

In this tutorial, we will build the skill of constructing well-formed commands using the command-name, options, and arguments structure. Along the way, we will work with `ls`, `uname`, and `date` — three commands that together let us practice short options, combined short options, and long options with and without values.

---

## Prerequisites

Before starting, ensure you have:

- A working shell prompt on an RHEL system (covered in Tutorial 1: Your First Commands at the Shell Prompt)
- The ability to type commands and press Enter to run them

---

## What We'll Build

By the end of this tutorial, you will have issued a series of correctly formed commands and observed exactly how the shell responds to each part of the command structure. The terminal will be in this state after our final step:

```
Sat May  7 14:32:00 UTC 2026
```

That output is the result of `date` with a long option and a value — proof that you can construct the full range of command syntax the shell expects.

---

## Step 1: Run a Command with No Options or Arguments

First, we run `uname` by itself to see what a bare command name produces.

```bash
uname
```

You should see:

```
Linux
```

This confirms the shell found the `uname` executable, ran it, and printed its output. The command name alone is a complete, valid command.

---

## Step 2: Add a Short Option

Now that we have seen a bare command, we add a single short option. Short options are a single letter preceded by one hyphen.

```bash
uname -r
```

You should see output similar to:

```
5.14.0-284.11.1.el9_2.x86_64
```

Notice that `-r` changed what `uname` reported — the kernel release — without changing the command name itself. The option is a separate token, but the space between the command name and the option is what separates them.

---

## Step 3: Combine Short Options

Now that we have used one short option, we combine two short options into a single token. Most commands accept combined short options written together after a single hyphen.

```bash
uname -sr
```

You should see:

```
Linux 5.14.0-284.11.1.el9_2.x86_64
```

Notice that `-sr` produces both the system name and the kernel release in one go. The shell passes the combined token to `uname`, which unpacks `-s` and `-r` as two separate instructions.

---

## Step 4: Use Multiple Short Options Written Separately

Now we issue the same combination written as two distinct options instead of one combined token, so we can see that both forms are equivalent.

```bash
uname -s -r
```

You should see:

```
Linux 5.14.0-284.11.1.el9_2.x86_64
```

The output is identical to Step 3. The shell passes each hyphenated token to `uname` as a separate argument; the program treats them the same way regardless of whether they arrived combined or separate.

---

## Step 5: Use a Long Option

Now that we have practiced short options, we use a long option. Long options begin with two hyphens followed by a descriptive word.

```bash
uname --kernel-release
```

You should see output similar to:

```
5.14.0-284.11.1.el9_2.x86_64
```

Notice that `--kernel-release` produces the same result as `-r` from Step 2. Long options are wordier but self-documenting — the option name describes exactly what it requests.

---

## Step 6: Use a Long Option That Requires a Value

Now we work with a long option that takes a value — the form `--option=value`. We use `date` with the `--date` option to ask it to interpret a specific date string.

```bash
date --date="next Monday"
```

You should see output similar to:

```
Mon May 12 00:00:00 UTC 2026
```

Notice the `=` sign connecting the option name to its value, with the value enclosed in quotes because it contains a space. Without the quotes, the shell would split `next` and `Monday` into two separate arguments and `date` would not receive the value it expects.

---

## Step 7: Use a Command with Both an Option and an Argument

Now that we have used options alone, we issue a command that takes both an option and an argument. An argument names the target the command acts on — separate from the options that modify its behaviour.

```bash
ls -l /etc
```

You should see a long listing of the `/etc` directory beginning with something like:

```
total 1084
drwxr-xr-x.  3 root root     97 Apr 22 10:01 alternatives
drwxr-xr-x.  4 root root     78 Apr 22 10:02 audit
...
```

Notice that `-l` is the option (it changes the output format) and `/etc` is the argument (it names the target). The command name, the option, and the argument are each separated by a single space.

---

## Step 8: Verify the Full Syntax Pattern with `date`

Finally, we verify the complete command-structure pattern by running `date` with a long option and a format value, producing a known, predictable output.

```bash
date --utc
```

You should see output similar to:

```
Sat May  7 14:32:00 UTC 2026
```

This matches the final state shown in **What We'll Build**. A long option, no argument — the command is complete and well-formed.

---

## What We Accomplished

In this tutorial, we:

1. Ran a bare command name and observed its output
2. Added a single short option using the `-r` form
3. Combined two short options into a single token using `-sr`
4. Wrote the same two options separately and confirmed identical output
5. Substituted a long option (`--kernel-release`) for its short equivalent
6. Supplied a value to a long option using the `--option=value` form
7. Issued a command with both an option and an argument, identifying each part
8. Verified the complete syntax pattern with a final `date` command

---

## Next Steps

Now that you have built the skill of constructing well-formed commands, you might want to:

- [How-to: Get Help for Any Command](#) — use `--help` and `man` to discover options for unfamiliar commands
- [Explanation: Understanding the Linux Shell and Command Syntax](#) — understand why the shell parses commands the way it does
- [Reference: Bash Command Syntax and Options](#) — see the complete specification of command structure and option conventions