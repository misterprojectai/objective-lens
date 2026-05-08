---
description: Redirect stderr to /dev/null to silence error messages from any command while leaving stdout fully intact.
icon: wrench
---

# How to Silence Error Messages While Preserving Normal Output

{% hint style="info" %}
**Before you begin:**

- A terminal session on a RHEL 9 system where you can run commands as a regular user
- A command that produces both normal output and error messages — for example, `ls` with a mix of valid and invalid paths
{% endhint %}

{% stepper %}
{% step %}
### Identify a command that produces stderr

Run the command without any redirection to confirm it generates both stdout and stderr.

```bash
ls /etc /no-such-dir
```

Both the directory listing and the error message appear on screen. The next step discards only the error.
{% endstep %}

{% step %}
### Redirect stderr to /dev/null

Append `2>/dev/null` to the command to discard all error output.

```bash
ls /etc /no-such-dir 2>/dev/null
```

Only the `/etc` directory listing appears. The error message for `/no-such-dir` is silently discarded.

{% hint style="warning" %}
**Syntax trap:** There must be no spaces between `2`, `>`, and `/dev/null`. Writing `2> /dev/null` (with a space) will still work, but `2 >/dev/null` (space before `>`) will not — the shell interprets `2` as a separate argument.
{% endhint %}
{% endstep %}

{% step %}
### Preserve stdout in a file while still discarding stderr

Combine stdout redirection with `2>/dev/null` to capture normal output to a file and discard errors simultaneously.

```bash
ls /etc /no-such-dir > ~/output.txt 2>/dev/null
```

Normal output goes to `~/output.txt`; error messages are discarded; nothing appears on screen.

{% hint style="warning" %}
**Order matters:** `2>/dev/null` must follow the stdout redirection. Placing it before `>` changes the shell's interpretation of the redirections and produces incorrect behavior.
{% endhint %}
{% endstep %}

{% step %}
### Apply the pattern to any command that generates unwanted errors

The pattern `command 2>/dev/null` works with any command. A common use case is suppressing "Permission denied" messages during `find` searches across the filesystem.

```bash
find / -name "*.conf" 2>/dev/null
```

`find` outputs matching file paths to stdout normally; all "Permission denied" errors are silenced.

<details>
<summary>What if the errors still appear after adding 2>/dev/null?</summary>

Some tools write messages to stdout rather than stderr. To determine which stream carries the messages, test with:

```bash
find / -name "*.conf" 2>&1 >/dev/null
```

If the messages appear with this command, they are on stdout and cannot be suppressed with `2>/dev/null`. You would need to filter them with `grep -v` or handle them differently.

</details>
{% endstep %}
{% endstepper %}

## Verification

{% hint style="success" %}
**Confirm stderr is discarded and stdout is intact:**

```bash
ls /etc/hosts /no-such-path 2>/dev/null
```

Expected result: only `/etc/hosts` appears — no error message for `/no-such-path`.

**Confirm stdout capture worked when redirecting to a file:**

```bash
wc -l ~/output.txt
```

Expected result: a non-zero line count matching the `/etc` directory listing.
{% endhint %}

## Troubleshooting

{% hint style="warning" %}
**Symptom → Cause → Fix**

**Error messages still appear on screen**
Cause: `2>/dev/null` was omitted or mistyped.
Fix: Verify the exact syntax — `2>/dev/null` with no spaces between `2`, `>`, and `/dev/null`.

---

**Normal output is also missing**
Cause: `&>/dev/null` was used instead of `2>/dev/null`.
Fix: `&>` discards both stdout and stderr. Use `2>/dev/null` to discard only stderr.

---

**Output file is empty**
Cause: Stdout was accidentally redirected to `/dev/null` instead of the target file.
Fix: Check the command — ensure `>` points to your target file, not `/dev/null`.

---

**`find` still shows some permission errors**
Cause: In some edge cases, the errors appear on stdout rather than stderr.
Fix: Confirm with `find ... 2>&1 >/dev/null` to identify which stream carries the messages.
{% endhint %}

## Related

- [Reference: I/O Redirection Operators and File Descriptors](x200_102-reference.md)
- [Explanation: Understanding I/O Redirection and Pipelines](x200_102-explanation.md)
- [How to Redirect stderr to a File](x200_102-howto-4.md)