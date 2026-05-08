---
description: Insert tee at a specific pipeline stage to snapshot a data stream to a file without interrupting downstream processing.
icon: wrench
---

# Capture an Intermediate Pipeline Stage to a File While Continuing Processing

{% hint style="info" %}
**Prerequisites**

- A terminal session on a RHEL 9 system with write access to `/tmp` or your home directory
- A pipeline where at least one command follows the stage you want to capture — `tee` requires a downstream consumer to be useful
{% endhint %}

{% stepper %}
{% step %}
### Identify the pipeline stage to capture

Choose the command whose output you want to preserve. `tee` reads from stdin and writes simultaneously to stdout and to a file — insert it immediately after the command whose output you need.

A three-stage pipeline without capture:

```bash
ps aux | grep -v grep | awk '{print $1}' | sort -u
```
{% endstep %}

{% step %}
### Insert tee after the target command

Place `tee` after the command whose output you want to snapshot, passing the destination filename as its argument. Data continues flowing to the next command unchanged.

```bash
ps aux | grep -v grep | tee /tmp/ps_snapshot.txt | awk '{print $1}' | sort -u
```

The terminal shows the final pipeline output. `/tmp/ps_snapshot.txt` receives the stream exactly as it existed after `grep -v grep`, before `awk` transformed it.

{% hint style="warning" %}
**Placement is critical.** Inserting `tee` after the wrong command captures the wrong stage. Verify the command immediately preceding `tee` is the one whose output you need.
{% endhint %}
{% endstep %}

{% step %}
### Append to an existing file instead of overwriting it

If the file already contains data you want to keep, use `tee -a`:

{% tabs %}
{% tab title="Append (-a)" %}
```bash
ps aux | grep -v grep | tee -a /tmp/ps_snapshot.txt | awk '{print $1}' | sort -u
```
{% endtab %}

{% tab title="Overwrite (default)" %}
```bash
ps aux | grep -v grep | tee /tmp/ps_snapshot.txt | awk '{print $1}' | sort -u
```
{% endtab %}
{% endtabs %}

{% hint style="warning" %}
Without `-a`, each pipeline run silently overwrites the file from the previous run with no error or warning.
{% endhint %}
{% endstep %}

{% step %}
### Capture multiple intermediate stages simultaneously

Insert additional `tee` calls at each stage you want to record:

```bash
cat /etc/passwd | tee /tmp/stage1_raw.txt | grep '/bin/bash' | tee /tmp/stage2_bash_users.txt | cut -d: -f1 | sort
```

- `/tmp/stage1_raw.txt` — receives the full file content
- `/tmp/stage2_bash_users.txt` — receives only the bash-user lines
- Terminal — shows the final sorted usernames

<details>
<summary>Naming snapshot files per run to avoid collisions</summary>

When running pipelines repeatedly and needing a separate snapshot per execution, append a timestamp to the filename:

```bash
ps aux | grep -v grep | tee /tmp/ps_snapshot_$(date +%s).txt | awk '{print $1}' | sort -u
```

Each run produces a uniquely named file such as `/tmp/ps_snapshot_1718000000.txt`.

</details>
{% endstep %}

{% step %}
### Suppress terminal output when you only want the file

If no commands follow `tee` and you want file-only output, redirect stdout to `/dev/null`:

```bash
ps aux | grep -v grep | tee /tmp/ps_snapshot.txt > /dev/null
```

{% hint style="warning" %}
Only use `> /dev/null` after `tee` when the file is the sole desired output. If commands follow `tee` in the pipeline, redirecting its stdout to `/dev/null` will starve those commands of input and break the pipeline.
{% endhint %}
{% endstep %}

{% step %}
### Capture a stage while also passing stderr through the pipeline

By default, `tee` only handles stdout. To include errors from the upstream command in the snapshot, merge stderr into stdout with `2>&1` before `tee`:

```bash
find /etc -name "*.conf" 2>&1 | tee /tmp/find_snapshot.txt | grep -c 'Permission denied'
```

- `/tmp/find_snapshot.txt` — contains both normal results and permission errors
- Terminal — shows only the count of permission-denied lines

<details>
<summary>Capturing stderr separately instead of merging</summary>

To keep stdout and stderr in separate snapshot files without merging:

```bash
find /etc -name "*.conf" 2>/tmp/find_errors.txt | tee /tmp/find_results.txt | wc -l
```

`/tmp/find_results.txt` receives stdout only. `/tmp/find_errors.txt` receives stderr only. The terminal shows the line count of successful results.

</details>
{% endstep %}
{% endstepper %}

## Verification

{% hint style="success" %}
**Confirm the snapshot was written and the pipeline continued independently**

Check that the snapshot file is non-empty:

```bash
wc -l /tmp/ps_snapshot.txt
```

The line count must be greater than zero and must match the number of lines produced by the upstream command — not the final pipeline output.

Compare snapshot size against final output to confirm they differ:

```bash
ps aux | grep -v grep | awk '{print $1}' | sort -u | wc -l
wc -l /tmp/ps_snapshot.txt
```

The snapshot count will be **larger** — it precedes `awk` and `sort -u` filtering, so it retains all lines that those commands would otherwise collapse or remove.
{% endhint %}

## Troubleshooting

{% hint style="warning" %}
**Symptom → Cause → Fix**

**`/tmp/ps_snapshot.txt` is empty after the pipeline runs**
Cause: The upstream command produced no output — a filter like `grep` eliminated everything.
Fix: Remove `tee` temporarily and run the pipeline only up to that stage to confirm upstream output exists.

---

**File content from a previous run is missing**
Cause: `tee` without `-a` overwrites the file on each run.
Fix: Use `tee -a` to append, or use a timestamp-suffixed filename per run: `tee /tmp/ps_snapshot_$(date +%s).txt`.

---

**Terminal shows no output but the file was written**
Cause: `tee` output was redirected to `/dev/null` unintentionally — check for `> /dev/null` after `tee`.
Fix: Remove `> /dev/null` if downstream processing is needed, or pipe to the next command instead.

---

**stderr messages appear on screen but not in the snapshot file**
Cause: `tee` only captures stdout; stderr bypasses it by default.
Fix: Merge streams with `2>&1` before `tee`, or redirect stderr separately with `2> errors.txt`.

---

**The snapshot file contains the final output, not the intermediate stage**
Cause: `tee` was inserted after the last command instead of at the target intermediate command.
Fix: Move `tee` to immediately after the command whose output you need to capture.

---

**Pipeline hangs after inserting `tee`**
Cause: The command after `tee` does not read from stdin — it ignores the pipe.
Fix: Verify the downstream command accepts stdin; replace it temporarily with `cat` to confirm data is flowing.
{% endhint %}