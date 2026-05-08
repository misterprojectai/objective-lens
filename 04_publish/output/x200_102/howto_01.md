---
description: Save the stdout of any command to a named file using shell redirection operators, with control over overwrite versus append behaviour.
icon: wrench
---

# How to Capture Command Output to a File for Later Inspection

{% hint style="info" %}
**Prerequisites**

- Write permission to the target directory
- The command whose output you want to capture is available on your system
{% endhint %}

{% stepper %}
{% step %}
### Redirect stdout to a new file

Run the command followed by `>` and the target filename.

```bash
command > /path/to/outputfile.txt
```

No output appears on the terminal. The shell creates the file if it does not exist.

{% hint style="warning" %}
`>` silently overwrites an existing file with no prompt or warning.
{% endhint %}
{% endstep %}

{% step %}
### Choose the right operator for your situation

Select the operator based on whether you need a fresh file or want to preserve existing content.

{% tabs %}
{% tab title="Create or overwrite" %}
Use `>` to create a new file or replace its contents entirely:

```bash
ls -lh /etc > ~/etc_listing.txt
```
{% endtab %}

{% tab title="Append" %}
Use `>>` to add output below any existing content:

```bash
ls -lh /var >> ~/etc_listing.txt
```
{% endtab %}
{% endtabs %}
{% endstep %}

{% step %}
### Redirect stdout while suppressing terminal display

The redirection syntax is identical regardless of the command. Only the command name changes.

```bash
df -h > ~/disk_report.txt
```

```bash
ps aux > ~/process_snapshot.txt
```
{% endstep %}

{% step %}
### Append a timestamp header before the command output

Write the timestamp first with `>>`, then append the command output below it.

```bash
date >> ~/disk_report.txt
df -h >> ~/disk_report.txt
```

<details>
<summary>Why run two separate commands instead of one?</summary>

`date` and `df -h` produce independent streams of stdout. There is no single command that combines them. Running each with `>>` in sequence appends both outputs to the same file in order, producing a timestamped report block you can repeat on a schedule.

</details>
{% endstep %}
{% endstepper %}

## Verification

{% hint style="success" %}
**Confirm the file was created and contains output**

```bash
ls -lh ~/disk_report.txt
cat ~/disk_report.txt
```

Expected result: `ls` reports a non-zero file size and `cat` displays the saved output, beginning with a timestamp line followed by the `df -h` output.
{% endhint %}

## Troubleshooting

{% hint style="warning" %}
**Common problems and fixes**

**`bash: /path/to/file: Permission denied`**
→ You do not have write permission to the target directory.
→ Use a path you own such as `~/filename.txt`, or check permissions with `ls -ld /target/dir`.

---

**Output file is empty**
→ The command produced no stdout — only stderr, or no output at all.
→ Run the command without redirection first to confirm it generates output.

---

**Existing file content was lost**
→ `>` overwrites without warning.
→ Use `>>` to append, or check the file before redirecting with `ls -lh filename`.

---

**Output appears on the terminal instead of going to the file**
→ A typo placed `>` before the command name, or the shell misread the operator.
→ Verify the syntax is `command > file`, not `> command file`.
{% endhint %}

## Related

- **Reference:** I/O Redirection Operators — complete syntax and file descriptor table
- **Explanation:** Understanding I/O Redirection and Pipelines — why stdout, stderr, and stdin exist as separate streams
- **How-to:** How to redirect stderr separately from stdout