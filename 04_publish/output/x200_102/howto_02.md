---
description: Accumulate output from multiple command runs into a single persistent log file using the >> append redirection operator.
icon: wrench
---

# How to Append Output to a Log File Across Repeated Command Runs

{% hint style="info" %}
**Before you begin:**

- Write permission to the directory where the log file will be created
- A log file path decided in advance — this guide uses `~/command.log` throughout
{% endhint %}

{% stepper %}
{% step %}
### Create the log file with the first command run

Redirect the first command's output into the log file using `>>`. If the file does not exist, `>>` creates it. If it does exist, output is added to the end.

```bash
date >> ~/command.log
```

{% hint style="warning" %}
`>>` and `>` look nearly identical but behave oppositely. `>` overwrites the file on every run — destroying all previous entries. Always use `>>` when accumulating a log.
{% endhint %}
{% endstep %}

{% step %}
### Append output from a second command run

Run the same command again, or a different command, using `>>` to the same file.

```bash
date >> ~/command.log
{% endstep %}

{% step %}
### Append output from a third command

Continue appending as many times as needed. Each invocation adds to the end of the file without disturbing earlier content.

```bash
uptime >> ~/command.log
{% endstep %}

{% step %}
### Append from a command with arguments

Any command that produces stdout works with `>>`. Use the full command as you would normally, followed by `>> logfile`.

```bash
df -h >> ~/command.log
{% endstep %}

{% step %}
### Append a separator line between runs

When logging across multiple invocations, insert a blank line or timestamp separator to make entries distinguishable.

```bash
echo "---" >> ~/command.log
```

<details>
<summary>Separator alternatives</summary>

Use a timestamp separator for higher-precision logs:

```bash
date "+--- %Y-%m-%d %H:%M:%S ---" >> ~/command.log
```

Use a blank line to visually group entries without adding extra text:

```bash
echo "" >> ~/command.log
```

</details>
{% endstep %}
{% endstepper %}

## Verification

{% hint style="success" %}
**Confirm all runs accumulated without overwriting earlier entries:**

```bash
cat ~/command.log
```

The file contains output from every command run in sequence — no earlier entry is missing or overwritten.

To confirm line count grew with each append, run `wc -l` before and after a new append and verify the count increases:

```bash
wc -l ~/command.log
date >> ~/command.log
wc -l ~/command.log
```
{% endhint %}

## Troubleshooting

{% hint style="warning" %}
**Common problems and fixes:**

**Log file contains only the most recent run's output**
→ Cause: Used `>` instead of `>>` — each run overwrote the file.
→ Fix: Replace `>` with `>>` in the command.

---

**`>>` reports `Permission denied`**
→ Cause: The log file or its directory is not writable by the current user.
→ Fix: Write to a path you own, such as `~/` or `/tmp/`.

---

**Log file is empty after running the command**
→ Cause: The command produced no stdout — it may have written to stderr instead.
→ Fix: Append stderr explicitly, or combine both streams:

```bash
# Append stderr only
command 2>> ~/command.log

# Append both stdout and stderr
command >> ~/command.log 2>&1
---

**Entries from different runs run together with no separation**
→ Cause: No separator was appended between invocations.
→ Fix: Add a separator between runs:

```bash
echo "---" >> ~/command.log
# or
date >> ~/command.log
```
{% endhint %}