---
description: Chain commands with pipes to search, sort, count, and transform text output in a single pass without intermediate files.
icon: wrench
---

# How to Filter and Process Command Output Using Pipelines

{% hint style="info" %}
**Prerequisites**

- A terminal session on a RHEL 9 system as a regular user
- The commands `grep`, `sort`, `uniq`, `wc`, `cut`, `head`, and `awk` available (all present in a standard RHEL 9 installation)
{% endhint %}

{% stepper %}
{% step %}
### Search command output with grep

Pipe any command into `grep` to filter lines matching a pattern.

```bash
ps aux | grep sshd
```

{% tabs %}
{% tab title="Case-insensitive match (-i)" %}
```bash
ps aux | grep -i ssh
```
{% endtab %}

{% tab title="Exclude matching lines (-v)" %}
```bash
ps aux | grep -v root
```
{% endtab %}
{% endtabs %}
{% endstep %}

{% step %}
### Count filtered results with wc -l

Append `wc -l` at the end of any pipeline to count the lines that reach it.

```bash
ps aux | grep -v root | wc -l
```

{% hint style="warning" %}
`wc -l` counts lines reaching it — if an earlier command in the pipeline produces no output, the count will be zero with no error message. Always verify the upstream stage produces output before adding `wc -l`.
{% endhint %}
{% endstep %}

{% step %}
### Sort output

Pipe into `sort` to arrange lines alphabetically or numerically.

{% tabs %}
{% tab title="Alphabetical" %}
```bash
cut -d: -f1 /etc/passwd | sort
```
{% endtab %}

{% tab title="Reverse alphabetical (-r)" %}
```bash
cut -d: -f1 /etc/passwd | sort -r
```
{% endtab %}

{% tab title="Numeric on a specific field (-n -t -k)" %}
```bash
cut -d: -f3 /etc/passwd | sort -n
```
{% endtab %}
{% endtabs %}
{% endstep %}

{% step %}
### Remove duplicate lines with uniq

Pipe **sorted** output into `uniq` to collapse consecutive duplicate lines.

```bash
cut -d: -f7 /etc/passwd | sort | uniq
```

To show each unique line with a count of appearances, use `-c`:

```bash
cut -d: -f7 /etc/passwd | sort | uniq -c
```

{% hint style="warning" %}
`uniq` only collapses **adjacent** duplicates. Always place `sort` immediately before `uniq` in the pipeline — skipping it produces silently incorrect output.
{% endhint %}
{% endstep %}

{% step %}
### Sort counted output to rank results

Sort the `uniq -c` output numerically to rank by frequency.

{% tabs %}
{% tab title="Least frequent first" %}
```bash
cut -d: -f7 /etc/passwd | sort | uniq -c | sort -n
```
{% endtab %}

{% tab title="Most frequent first (-rn)" %}
```bash
cut -d: -f7 /etc/passwd | sort | uniq -c | sort -rn
```
{% endtab %}
{% endtabs %}
{% endstep %}

{% step %}
### Limit output with head or tail

Restrict the pipeline to the first N lines with `head -n`:

```bash
cut -d: -f7 /etc/passwd | sort | uniq -c | sort -rn | head -5
```

To see only the last N lines, use `tail -n` instead:

```bash
cut -d: -f7 /etc/passwd | sort | uniq -c | sort -rn | tail -3
```
{% endstep %}

{% step %}
### Extract a specific field with cut or awk

Use `cut` when the delimiter is a single character:

```bash
grep '/bin/bash' /etc/passwd | cut -d: -f1
```

Use `awk` when you need more control over field splitting or output formatting:

```bash
ps aux | awk '{print $1, $11}' | sort | uniq
```

<details>
<summary>Choosing between cut and awk</summary>

`cut` is faster and simpler for fixed single-character delimiters. Use it for well-structured files like `/etc/passwd`.

`awk` handles variable-width whitespace (as in `ps aux` output), multiple field references in one pass, and custom output formatting. If `cut` produces unexpected results on whitespace-delimited input, switch to `awk`.

</details>

{% hint style="warning" %}
`awk` field indices start at `$1`, not `$0` — `$0` is the entire line. Specifying a field index higher than the number of columns in the input prints an empty string with no error.
{% endhint %}
{% endstep %}

{% step %}
### Capture intermediate output with tee

Insert `tee` at any point in a pipeline to write the stream to a file while passing it through to the next command:

```bash
cut -d: -f7 /etc/passwd | sort | tee /tmp/shells_sorted.txt | uniq -c | sort -rn
```

The full sorted list lands in `/tmp/shells_sorted.txt`; the counted and ranked output still appears on screen.

{% hint style="warning" %}
If a command **upstream** of `tee` fails, `tee` receives no data and the file will be empty — no error is raised. If `tee` file is empty after the run, test each stage individually left to right to isolate the failure.
{% endhint %}
{% endstep %}
{% endstepper %}

---

## Verification

{% hint style="success" %}
Run both commands to confirm the pipeline is working and the intermediate file was written:

```bash
cut -d: -f7 /etc/passwd | sort | tee /tmp/shells_sorted.txt | uniq -c | sort -rn | head -5
wc -l < /tmp/shells_sorted.txt
```

**Expected results:**
- The first command prints the five most common login shells ranked by frequency — each line shows a count followed by a shell path (e.g., `     20 /bin/bash`).
- The second command prints the total number of lines captured at the `tee` stage. This number **must be greater than zero**.
{% endhint %}

---

## Troubleshooting

{% hint style="warning" %}
**`uniq` output still contains duplicates**
→ Input was not sorted before `uniq`. Add `sort` immediately before `uniq` in the pipeline.

---

**`cut` produces unexpected fields**
→ Wrong delimiter specified with `-d`. Check the actual field separator with `cat -A file` and correct the `-d` argument.

---

**`awk` prints nothing**
→ Field index is out of range for the input. Run the pipeline without `awk` first and count visible columns manually.

---

**Pipeline hangs waiting for input**
→ A command earlier in the chain reads stdin and has no data to consume. Verify the first command in the chain generates output on its own before adding the pipe.

---

**`tee` file is empty after the pipeline runs**
→ A downstream command failed before `tee` received any data. Test each stage individually left to right to isolate the failing command.

---

**`sort -n` produces wrong order**
→ Non-numeric characters (such as leading spaces from `uniq -c`) confuse the sort. Use `sort -rn` — it handles leading whitespace from `uniq -c` correctly.
{% endhint %}