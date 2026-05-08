---
title: "Build Pipelines with |"
type: tutorial
quadrant:
  practical_theoretical: practical
  work_study: study
exam_objective: x200_102
tutorial_index: 5
version: "1.0"
status: draft
---

# Build Pipelines with |

In this tutorial, we will chain commands together so that the stdout of one feeds directly into the stdin of the next. Along the way, we will work with `grep`, `sort`, `uniq`, `wc`, and `tee` — building pipelines one stage at a time until we have a working multi-command chain.

---

## Prerequisites

Before starting, ensure you have:

- A RHEL 9 terminal session as a regular user
- Basic familiarity with running single commands such as `ls`, `grep`, and `cat`

---

## What We'll Build

By the end of this tutorial, we will have built a four-command pipeline that extracts all unique login shells from `/etc/passwd`, counts how many users use each one, and captures an intermediate snapshot to a file — all without writing a single temporary file by hand. The final pipeline and its output will look like this:

```
$ cat /etc/passwd | grep -v '^#' | cut -d: -f7 | sort | uniq -c
      1 /bin/sync
      1 /sbin/halt
      1 /sbin/nologin
     ...
     22 /sbin/nologin
      1 /sbin/shutdown
```

And after inserting `tee` to capture an intermediate snapshot:

```
$ cat /etc/passwd | grep -v '^#' | cut -d: -f7 | tee /tmp/shells_raw.txt | sort | uniq -c
      1 /bin/sync
     ...
$ cat /tmp/shells_raw.txt | head -5
/bin/sync
/sbin/halt
/sbin/nologin
...
```

---

## Step 1: Run a Single Command and Observe Its Output

First, we run `cat /etc/passwd` on its own so we can see the raw data we are about to transform.

```bash
cat /etc/passwd
```

You should see:

```
root:x:0:0:root:/root:/bin/bash
bin:x:1:1:bin:/bin:/sbin/nologin
daemon:x:2:2:daemon:/sbin:/sbin/nologin
...
```

Notice that the file has many lines — one per user — and each line is colon-separated. The seventh colon-delimited field is the login shell.

---

## Step 2: Add a First Pipe to Filter Comments

Now that we can see the raw data, we pipe it through `grep` to drop any comment lines that begin with `#`.

```bash
cat /etc/passwd | grep -v '^#'
```

You should see:

```
root:x:0:0:root:/root:/bin/bash
bin:x:1:1:bin:/bin:/sbin/nologin
daemon:x:2:2:daemon:/sbin:/sbin/nologin
...
```

Notice that no lines starting with `#` appear in the output. The `|` character sent everything `cat` wrote to stdout directly into `grep`'s stdin.

---

## Step 3: Add a Second Pipe to Isolate the Shell Field

Now that we have a clean list of user entries, we pipe through `cut` to extract only the seventh field — the login shell.

```bash
cat /etc/passwd | grep -v '^#' | cut -d: -f7
```

You should see:

```
/bin/bash
/sbin/nologin
/sbin/nologin
/bin/sync
/sbin/shutdown
/sbin/halt
...
```

Notice that the output is now one shell path per line. Each pipe in the chain has narrowed the data stream further.

---

## Step 4: Add a Third Pipe to Sort the Output

Now that we have one shell per line, we pipe into `sort` so that identical shells are grouped together — which is required for the next step to work correctly.

```bash
cat /etc/passwd | grep -v '^#' | cut -d: -f7 | sort
```

You should see:

```
/bin/bash
/bin/bash
/bin/sync
/sbin/halt
/sbin/nologin
/sbin/nologin
/sbin/nologin
...
```

Notice that duplicate shell paths now appear next to each other in the stream.

---

## Step 5: Add a Fourth Pipe to Count Unique Values

Now that the stream is sorted, we pipe into `uniq -c` to collapse duplicates and prefix each line with a count.

```bash
cat /etc/passwd | grep -v '^#' | cut -d: -f7 | sort | uniq -c
```

You should see output similar to:

```
      2 /bin/bash
      1 /bin/sync
      1 /sbin/halt
     22 /sbin/nologin
      1 /sbin/shutdown
```

Notice that the pipeline has transformed raw file content into a frequency table — using only commands connected by pipes, with no intermediate files.

---

## Step 6: Insert tee to Capture an Intermediate Stage

Now that we have a working four-command pipeline, we insert `tee` between `cut` and `sort` to save the raw shell list to a file while the data continues flowing through the rest of the pipeline unchanged.

```bash
cat /etc/passwd | grep -v '^#' | cut -d: -f7 | tee /tmp/shells_raw.txt | sort | uniq -c
```

You should see the same final output as Step 5:

```
      2 /bin/bash
      1 /bin/sync
      1 /sbin/halt
     22 /sbin/nologin
      1 /sbin/shutdown
```

Notice that the pipeline result on screen is unchanged — `tee` copied the stream to the file without interrupting it.

---

## Step 7: Verify the Intermediate Snapshot

Finally, we verify that `tee` saved the intermediate data while the pipeline was running.

```bash
cat /tmp/shells_raw.txt | head -5
```

You should see:

```
/bin/bash
/bin/bash
/bin/sync
/sbin/halt
/sbin/nologin
```

This confirms that `/tmp/shells_raw.txt` contains the unsorted shell list that existed mid-pipeline, before `sort` and `uniq -c` processed it.

---

## What We Accomplished

In this tutorial, we:

1. Ran a single command and observed its raw stdout
2. Piped that output through `grep` to filter unwanted lines
3. Extended the pipeline with `cut` to isolate a single field from each line
4. Added `sort` to group identical values together in the stream
5. Added `uniq -c` to count occurrences and produce a frequency table
6. Inserted `tee` mid-pipeline to capture an intermediate snapshot without breaking the data flow
7. Verified the captured snapshot with a separate command

---

## Next Steps

Now that you have built and extended a multi-stage pipeline, you might want to:

- [How-to: Build and Debug Multi-Stage Pipelines](#) — apply this technique to real administrative tasks such as filtering logs and auditing process lists
- [Explanation: Understanding I/O Redirection and Pipelines](#) — understand why pipelines run commands in parallel and how the kernel connects their file descriptors
- [Reference: I/O Redirection Operators and File Descriptors](#) — see the complete operator syntax and the full behaviour of `tee`