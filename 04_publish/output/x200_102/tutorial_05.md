---
description: Build a multi-stage shell pipeline using grep, cut, sort, uniq, and tee to extract and count login shells from /etc/passwd.
icon: graduation-cap
---

# Build Pipelines with |

In this tutorial, we will chain commands together so that the stdout of one feeds directly into the stdin of the next. We will work with `grep`, `sort`, `uniq`, `wc`, and `tee` — building pipelines one stage at a time until we have a working multi-command chain.

By the end, we will have built a four-command pipeline that extracts all unique login shells from `/etc/passwd`, counts how many users use each one, and captures an intermediate snapshot to a file — all without writing a single temporary file by hand.

{% hint style="info" %}
**Before you start, you need:**

- A RHEL 9 terminal session as a regular user
- Basic familiarity with running single commands such as `ls`, `grep`, and `cat`
{% endhint %}

## What We'll Build

The final pipeline and its output will look like this:

```bash
cat /etc/passwd | grep -v '^#' | cut -d: -f7 | sort | uniq -c
```

```
      1 /bin/sync
      1 /sbin/halt
     22 /sbin/nologin
      1 /sbin/shutdown
```

After inserting `tee` to capture an intermediate snapshot:

```bash
cat /etc/passwd | grep -v '^#' | cut -d: -f7 | tee /tmp/shells_raw.txt | sort | uniq -c
```

```
      1 /bin/sync
     22 /sbin/nologin
      1 /sbin/shutdown
```

```bash
cat /tmp/shells_raw.txt | head -5
```

```
/bin/sync
/sbin/halt
/sbin/nologin
...
---

{% stepper %}
{% step %}
### Run a Single Command and Observe Its Output

Run `cat /etc/passwd` on its own so you can see the raw data you are about to transform.

```bash
cat /etc/passwd
```

{% code title="Output" %}
```
root:x:0:0:root:/root:/bin/bash
bin:x:1:1:bin:/bin:/sbin/nologin
daemon:x:2:2:daemon:/sbin:/sbin/nologin
...
```
{% endcode %}

The file has many lines — one per user — and each line is colon-separated. The seventh colon-delimited field is the login shell.
{% endstep %}

{% step %}
### Add a First Pipe to Filter Comments

Pipe the output through `grep` to drop any comment lines that begin with `#`.

```bash
cat /etc/passwd | grep -v '^#'
```

{% code title="Output" %}
```
root:x:0:0:root:/root:/bin/bash
bin:x:1:1:bin:/bin:/sbin/nologin
daemon:x:2:2:daemon:/sbin:/sbin/nologin
...
```
{% endcode %}

No lines starting with `#` appear in the output. The `|` character sent everything `cat` wrote to stdout directly into `grep`'s stdin.

{% hint style="warning" %}
The pattern `'^#'` is single-quoted to prevent the shell from interpreting `^` or `#` as special characters. Always quote `grep` patterns that contain shell metacharacters.
{% endhint %}
{% endstep %}

{% step %}
### Add a Second Pipe to Isolate the Shell Field

Extend the pipeline with `cut` to extract only the seventh field — the login shell.

```bash
cat /etc/passwd | grep -v '^#' | cut -d: -f7
```

{% code title="Output" %}
```
/bin/bash
/sbin/nologin
/sbin/nologin
/bin/sync
/sbin/shutdown
/sbin/halt
...
```
{% endcode %}

The output is now one shell path per line. Each pipe in the chain has narrowed the data stream further.

{% hint style="warning" %}
`-d:` sets the delimiter to `:` and `-f7` selects the seventh field. If you omit `-d:`, `cut` defaults to tab-delimited input and will return the entire line unchanged.
{% endhint %}
{% endstep %}

{% step %}
### Add a Third Pipe to Sort the Output

Pipe into `sort` so that identical shells are grouped together — which is required for the next step to work correctly.

```bash
cat /etc/passwd | grep -v '^#' | cut -d: -f7 | sort
```

{% code title="Output" %}
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
{% endcode %}

Duplicate shell paths now appear next to each other in the stream. `uniq` in the next step only collapses adjacent duplicates, so this sort is mandatory.
{% endstep %}

{% step %}
### Add a Fourth Pipe to Count Unique Values

Pipe into `uniq -c` to collapse duplicates and prefix each line with a count.

```bash
cat /etc/passwd | grep -v '^#' | cut -d: -f7 | sort | uniq -c
```

{% code title="Output" %}
```
      2 /bin/bash
      1 /bin/sync
      1 /sbin/halt
     22 /sbin/nologin
      1 /sbin/shutdown
```
{% endcode %}

{% hint style="success" %}
The pipeline has transformed raw file content into a frequency table — using only commands connected by pipes, with no intermediate files written to disk.
{% endhint %}

{% hint style="warning" %}
`uniq -c` only merges adjacent identical lines. If you skip the `sort` step, duplicate shells that are not consecutive will each get their own count entry instead of being summed together.
{% endhint %}
{% endstep %}

{% step %}
### Insert tee to Capture an Intermediate Stage

Insert `tee` between `cut` and `sort` to save the raw shell list to a file while the data continues flowing through the rest of the pipeline unchanged.

```bash
cat /etc/passwd | grep -v '^#' | cut -d: -f7 | tee /tmp/shells_raw.txt | sort | uniq -c
```

{% code title="Output" %}
```
      2 /bin/bash
      1 /bin/sync
      1 /sbin/halt
     22 /sbin/nologin
      1 /sbin/shutdown
```
{% endcode %}

The pipeline result on screen is identical to Step 5 — `tee` copied the stream to the file without interrupting it.

<details>
<summary>If the output differs from Step 5</summary>

Check that you placed `tee /tmp/shells_raw.txt` between `cut -d: -f7` and `sort`, not at any other position in the pipeline. Moving `tee` changes which stage of the data it captures, but it must not break the chain — confirm that `sort | uniq -c` still follow it.

</details>
{% endstep %}

{% step %}
### Verify the Intermediate Snapshot

Confirm that `tee` saved the intermediate data while the pipeline was running.

```bash
cat /tmp/shells_raw.txt | head -5
```

{% code title="Output" %}
```
/bin/bash
/bin/bash
/bin/sync
/sbin/halt
/sbin/nologin
```
{% endcode %}

{% hint style="success" %}
`/tmp/shells_raw.txt` contains the unsorted shell list that existed mid-pipeline, before `sort` and `uniq -c` processed it. This confirms `tee` captured the stream at exactly the right stage.
{% endhint %}
{% endstep %}
{% endstepper %}

---

{% hint style="success" %}
**You've completed the tutorial.** You have:

1. Run a single command and observed its raw stdout
2. Piped that output through `grep` to filter unwanted lines
3. Extended the pipeline with `cut` to isolate a single field from each line
4. Added `sort` to group identical values together in the stream
5. Added `uniq -c` to count occurrences and produce a frequency table
6. Inserted `tee` mid-pipeline to capture an intermediate snapshot without breaking the data flow
7. Verified the captured snapshot with a separate command
{% endhint %}

## Next Steps

- [How-to: Build and Debug Multi-Stage Pipelines](#) — apply this technique to real administrative tasks such as filtering logs and auditing process lists
- [Explanation: Understanding I/O Redirection and Pipelines](#) — understand why pipelines run commands in parallel and how the kernel connects their file descriptors
- [Reference: I/O Redirection Operators and File Descriptors](#) — see the complete operator syntax and the full behaviour of `tee`