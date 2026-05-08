---
description: Merge stdout and stderr into a single file using the `&>` shorthand and the portable `> file 2>&1` form.
icon: wrench
---

# How to Capture Both stdout and stderr to a Single File

{% hint style="info" %}
**Prerequisites**
- A terminal session as a regular user on a RHEL 9 system
- Write permission to the directory where you will create output files
{% endhint %}

{% stepper %}
{% step %}
### Confirm you have a command that produces both streams

Run the following command without any redirection to observe stdout and stderr appearing together on the terminal.

```bash
ls /etc/hosts /no/such/path
```

You will see the error message and the valid path result interleaved on screen — both streams are active.
{% endstep %}

{% step %}
### Capture both streams using `&>`

Redirect all output — both stdout and stderr — to a single file using the `&>` operator.

```bash
ls /etc/hosts /no/such/path &> ~/combined.txt
```

{% hint style="warning" %}
`&>` always **overwrites** the destination file. Use `&>>` to append instead.
{% endhint %}
{% endstep %}

{% step %}
### Capture both streams using `> file 2>&1`

Redirect stdout to the file first, then redirect stderr to the same destination as stdout using `2>&1`.

```bash
ls /etc/hosts /no/such/path > ~/combined2.txt 2>&1
```

{% hint style="warning" %}
**Order matters.** Writing `2>&1 > file` is wrong — it redirects stderr to the terminal (the current stdout target), then redirects stdout to the file. Always place `2>&1` **after** the file redirection.
{% endhint %}
{% endstep %}

{% step %}
### Append both streams to an existing file

To add both stdout and stderr to a file without overwriting it, use `&>>` or the append equivalent of the explicit form.

{% tabs %}
{% tab title="&>> shorthand" %}
```bash
ls /etc/hosts /no/such/path &>> ~/combined.txt
```
{% endtab %}

{% tab title="Explicit form" %}
```bash
ls /etc/hosts /no/such/path >> ~/combined.txt 2>&1
```
{% endtab %}
{% endtabs %}
{% endstep %}

{% step %}
### Discard both streams

To silence all output from a command, redirect both streams to `/dev/null`.

```bash
ls /etc/hosts /no/such/path &> /dev/null
```

<details>
<summary>Using the portable form with /dev/null</summary>

If your script targets `/bin/sh` (POSIX sh), which does not support `&>`, use the explicit form instead:

```bash
ls /etc/hosts /no/such/path > /dev/null 2>&1
```

This is fully portable across all POSIX shells.

</details>
{% endstep %}
{% endstepper %}

## Verification

{% hint style="success" %}
**Confirm both files contain output from both streams:**

```bash
cat ~/combined.txt
cat ~/combined2.txt
```

Each file should contain **both** of the following lines:

```
/etc/hosts
ls: cannot access '/no/such/path': No such file or directory
```

Neither file should be empty, and neither should contain only one of the two messages.
{% endhint %}

## Troubleshooting

{% hint style="warning" %}
**Symptom → Cause → Fix**

**File contains only the error message, not the normal output**
→ stdout was redirected to the file but stderr was not included
→ Replace `> file` with `&> file`, or add `2>&1` after the file redirection

---

**File contains only normal output; error still appears on screen**
→ `2>&1` was omitted or stderr was redirected separately
→ Use `&> file` or append `2>&1` to the end of `> file`

---

**`2>&1 > file` sends stderr to the terminal instead of the file**
→ Operand order is reversed — `2>&1` is evaluated before the file target is set
→ Rewrite as `> file 2>&1` with the file redirection first

---

**`&>` is not recognised by the shell**
→ Script uses `/bin/sh` (POSIX sh), which does not support `&>`
→ Use `> file 2>&1` instead — this form is portable across all POSIX shells

---

**Appending with `&>` overwrites the file**
→ `&>` is an overwrite operator
→ Use `&>>` to append, or use `>> file 2>&1`
{% endhint %}