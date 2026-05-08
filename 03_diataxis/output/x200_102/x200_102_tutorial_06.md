---
title: "Split a Pipeline Stream with tee"
type: tutorial
quadrant:
  practical_theoretical: practical
  work_study: study
exam_objective: x200_102
tutorial_index: 6
version: "1.0"
status: draft
---

# Split a Pipeline Stream with tee

In this tutorial, we will use the `tee` command to capture an intermediate pipeline stream to a file while allowing data to continue flowing to the next command. Along the way, we will work with `ps`, `grep`, and `tee` to build a three-stage pipeline that saves a snapshot of its intermediate state.

---

## Prerequisites

Before starting, ensure you have:

- A RHEL 9 (or compatible) terminal session as a regular user
- Completion of Tutorial 5, or comfort running basic pipelines with `|`

---

## What We'll Build

By the end of this tutorial, you will have run a pipeline that lists all running processes, saves the full list to a file called `allprocs.txt`, and then filters the stream to show only SSH-related processes on screen. The system will be in this state:

```
$ cat allprocs.txt | wc -l
(a number greater than 0)

$ cat allprocs.txt | head -3
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1  0.0  0.3 171820 13200 ?        Ss   08:01   0:01 /usr/lib/systemd/systemd
root           2  0.0  0.0      0     0 ?        S    08:01   0:00 [kthreadd]
```

---

## Step 1: Run a plain pipeline without tee

First, we run a two-stage pipeline to confirm that `ps` output flows into `grep` and that SSH-related processes appear on screen. This establishes what the pipeline does before we insert `tee`.

```bash
ps aux | grep ssh
```

You should see output similar to:

```
root         892  0.0  0.1  15892  7104 ?        Ss   08:01   0:00 sshd: /usr/sbin/sshd -D [listener] 0 of 10-100 startups
user        1234  0.0  0.0   6408   720 pts/0    S+   09:14   0:00 grep --color=auto ssh
```

Notice that `grep` itself appears in the results — this is expected behaviour that you will see on every system.

---

## Step 2: Insert tee to capture the full process list

Now that we have confirmed the pipeline works, we insert `tee` between `ps` and `grep`. This saves every line that `ps` produces to `allprocs.txt` while simultaneously passing the same data forward to `grep`.

```bash
ps aux | tee allprocs.txt | grep ssh
```

You should see the same SSH-related output on screen as before:

```
root         892  0.0  0.1  15892  7104 ?        Ss   08:01   0:00 sshd: /usr/sbin/sshd -D [listener] 0 of 10-100 startups
user        1234  0.0  0.0   6408   720 pts/0    S+   09:14   0:00 grep --color=auto ssh
```

Notice that the screen output has not changed — `grep` still receives the full stream from `tee` exactly as if `tee` were not there.

---

## Step 3: Verify the file was written

Now that the pipeline has run, we confirm that `allprocs.txt` contains the complete, unfiltered output from `ps` — not just the SSH lines.

```bash
wc -l allprocs.txt
```

You should see a line count substantially larger than the number of SSH lines printed to screen, for example:

```
187 allprocs.txt
```

The file holds every process, while the screen showed only the filtered subset.

---

## Step 4: Inspect the beginning of the captured file

We examine the top of the file to confirm it contains the full `ps` header and process list, not just the grep results.

```bash
head -5 allprocs.txt
```

You should see:

```
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1  0.0  0.3 171820 13200 ?        Ss   08:01   0:01 /usr/lib/systemd/systemd
root           2  0.0  0.0      0     0 ?        S    08:01   0:00 [kthreadd]
root           3  0.0  0.0      0     0 ?        I<   08:01   0:00 [rcu_gp]
root           4  0.0  0.0      0     0 ?        I<   08:01   0:00 [rcu_par_gp]
```

The header row confirms we captured everything from `ps`, not only the lines that matched `grep`.

---

## Step 5: Run a second pipeline using the saved file to confirm independence

Finally, we verify the complete system state by searching the saved file directly with `grep`. This confirms the file is self-contained and can be queried independently of any running pipeline.

```bash
grep ssh allprocs.txt
```

You should see:

```
root         892  0.0  0.1  15892  7104 ?        Ss   08:01   0:00 sshd: /usr/sbin/sshd -D [listener] 0 of 10-100 startups
```

The SSH entry is present in the file, confirming that `tee` wrote the full unfiltered stream and the pipeline continued filtering normally.

---

## What We Accomplished

In this tutorial, we:

1. Ran a two-stage `ps | grep` pipeline to establish a baseline
2. Inserted `tee allprocs.txt` between `ps` and `grep` to split the stream, writing the full process list to a file while passing all data forward to `grep` unchanged
3. Verified with `wc -l` that the file contained the complete unfiltered output
4. Confirmed with `head` that the file holds the full `ps` header and process list
5. Queried the saved file independently with `grep` to confirm it is a complete, standalone record

---

## Next Steps

Now that you have built a pipeline that captures an intermediate stream, you might want to:

- [How-to: Build and Debug Multi-Stage Pipelines](#) — apply `tee` to inspect intermediate stages when a long pipeline produces unexpected results
- [Explanation: Understanding I/O Redirection and Pipelines](#) — understand why `tee` reads stdin and writes to both stdout and a file simultaneously
- [Reference: I/O Redirection Operators and File Descriptors](#) — see the complete `tee` syntax, including the `-a` append option