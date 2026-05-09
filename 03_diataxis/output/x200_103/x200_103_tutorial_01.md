---
title: "Filter Text Streams with Basic grep"
type: tutorial
quadrant:
  practical_theoretical: practical
  work_study: study
exam_objective: x200_103
tutorial_index: 1
version: "1.0"
status: draft
---

# Filter Text Streams with Basic grep

In this tutorial, we will use `grep` to filter lines from files and pipelines using literal string patterns and the `-i` case-insensitive flag. Along the way, we will work with standard input, file arguments, and the core mechanic of how `grep` selects matching lines and discards everything else.

---

## Prerequisites

Before starting, ensure you have:

- A RHEL 9 (or compatible) system with a terminal and shell access
- A non-root user account with `sudo` access, or direct access as root

---

## What We'll Build

By the end of this tutorial, we will have used `grep` in four distinct ways: searching a file directly, searching with case-insensitivity, filtering pipeline output, and inverting a match to exclude lines. The final verification step will produce output like this:

```
[student@rhel9 ~]$ grep 'root' /etc/passwd
root:x:0:0:root:/root:/bin/bash
operator:x:11:0:operator:/root:/sbin/nologin

[student@rhel9 ~]$ grep -i 'ROOT' /etc/passwd
root:x:0:0:root:/root:/bin/bash
operator:x:11:0:operator:/root:/sbin/nologin

[student@rhel9 ~]$ dmesg | grep -i 'eth'
(lines containing eth, ETH, Eth, or any mixed-case variant)

[student@rhel9 ~]$ grep -v 'nologin' /etc/passwd
root:x:0:0:root:/root:/bin/bash
sync:x:5:0:sync:/sbin:/bin/sync
shutdown:x:6:0:shutdown:/sbin:/sbin/shutdown
halt:x:7:0:halt:/sbin:/sbin/halt
(additional lines without nologin)
```

---

## Step 1: Search a File for a Literal String

First, we run `grep` against `/etc/passwd` to find every line containing the string `root`.

```bash
grep 'root' /etc/passwd
```

You should see:

```
root:x:0:0:root:/root:/bin/bash
operator:x:11:0:operator:/root:/sbin/nologin
```

Notice that both lines appear because each one contains the characters `root` somewhere — `grep` searches the entire line regardless of position. All other lines in the file were discarded.

---

## Step 2: Confirm That the Match Is Case-Sensitive by Default

Now that we have seen a basic match, we confirm that `grep` treats uppercase and lowercase as different by default.

```bash
grep 'ROOT' /etc/passwd
```

You should see:

```
(no output)
```

The shell returns to the prompt with no lines printed. The string `ROOT` in all capitals does not appear anywhere in `/etc/passwd`, so `grep` selects nothing and produces no output. This confirms that matching is case-sensitive unless we tell it otherwise.

---

## Step 3: Use -i to Match Regardless of Case

Now we add the `-i` flag so that `grep` matches `ROOT`, `root`, `Root`, and any other capitalisation of that sequence.

```bash
grep -i 'ROOT' /etc/passwd
```

You should see:

```
root:x:0:0:root:/root:/bin/bash
operator:x:11:0:operator:/root:/sbin/nologin
```

Notice that the output is identical to Step 1. The `-i` flag changes what `grep` matches, not what it prints — the original line text is preserved exactly as it appears in the file.

---

## Step 4: Filter Pipeline Output with grep

Now that we have searched a file directly, we filter the output of another command through `grep`. We pipe `dmesg` output and keep only lines that mention a network interface string.

```bash
dmesg | grep -i 'eth'
```

You should see output similar to:

```
[    1.234567] e1000 0000:00:03.0 eth0: (PCI:33MHz:32-bit)
[    1.235678] e1000 0000:00:03.0 eth0: Intel(R) PRO/1000 Network Connection
```

If your system uses a different interface naming scheme, you may see no output — that is expected. The important observation is the pipeline mechanics: `dmesg` produces many lines, `grep` receives all of them on standard input, and only the matching lines pass through to the terminal.

If you see no output, try this alternative to confirm the pipeline itself is working:

```bash
dmesg | grep -i 'cpu'
```

You should see one or more lines mentioning CPU initialisation.

---

## Step 5: Invert the Match with -v to Exclude Lines

Now we use `-v` to reverse `grep`'s behaviour: instead of selecting lines that match, we select lines that do not match. We filter `/etc/passwd` to hide every account that uses `nologin` as its shell.

```bash
grep -v 'nologin' /etc/passwd
```

You should see output similar to:

```
root:x:0:0:root:/root:/bin/bash
sync:x:5:0:sync:/sbin:/bin/sync
shutdown:x:6:0:shutdown:/sbin:/sbin/shutdown
halt:x:7:0:halt:/sbin:/sbin/halt
student:x:1000:1000::/home/student:/bin/bash
```

The exact lines will vary by system. Notice that every line containing `nologin` is gone — only accounts without that string in their entry remain.

---

## Step 6: Verify All Four Forms of grep Invocation

Finally, we run all four forms in sequence to confirm the complete picture of what we have built.

```bash
grep 'root' /etc/passwd
echo "---"
grep -i 'ROOT' /etc/passwd
echo "---"
dmesg | grep -i 'cpu' | head -2
echo "---"
grep -v 'nologin' /etc/passwd
```

You should see:

```
root:x:0:0:root:/root:/bin/bash
operator:x:11:0:operator:/root:/sbin/nologin
---
root:x:0:0:root:/root:/bin/bash
operator:x:11:0:operator:/root:/sbin/nologin
---
(two lines from dmesg mentioning cpu)
---
root:x:0:0:root:/root:/bin/bash
sync:x:5:0:sync:/sbin:/bin/sync
shutdown:x:6:0:shutdown:/sbin:/sbin/shutdown
halt:x:7:0:halt:/sbin:/sbin/halt
student:x:1000:1000::/home/student:/bin/bash
```

Each `grep` invocation demonstrates a distinct capability: file search, case-insensitive file search, pipeline filtering, and inverted matching.

---

## What We Accomplished

In this tutorial, we:

1. Ran `grep` against a file to select lines containing a literal string
2. Confirmed that `grep` is case-sensitive by default by attempting a mismatched-case search
3. Applied the `-i` flag to match a pattern regardless of capitalisation
4. Piped command output through `grep` to filter a live data stream
5. Used `-v` to invert the match and exclude lines containing a specific string

---

## Next Steps

Now that you have the foundational `grep` invocation working, you might want to:

- [Tutorial 2: Anchor Patterns to Lines with ^ and $](./grep-regex-tutorial-2-anchors.md) — restrict where in a line a match is allowed to occur
- [How-to: Filter Log Files with grep](../how-to/filter-logs-grep.md) — apply these skills to real system log analysis
- [Explanation: Understanding grep and Regular Expressions](../explanation/grep-regex-explanation.md) — understand why grep works the way it does, including the filter model and case behaviour
- [Reference: grep Options and Regular Expression Syntax](../reference/grep-regex-reference.md) — see the complete list of flags and pattern syntax