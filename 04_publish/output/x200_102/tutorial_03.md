---
description: Redirect stderr to a file using 2>, separate stdout and stderr into independent files, and silence unwanted output with /dev/null.
icon: graduation-cap
---

# Redirect stderr with 2> and Discard Output with /dev/null

{% hint style="info" %}
**Before you start, you need:**
- A terminal logged in as a regular user on a RHEL 9 system
- A home directory you can write to
- Completion of Tutorial 1 (redirecting stdout with `>` and `>>`)
{% endhint %}

By the end of this tutorial, you will have run a command that produces both normal output and errors, captured each stream independently to its own file, and silenced all output using `/dev/null`. Your working directory will contain:

```
~/tutorial3/
├── output.txt        (contains the /etc directory listing)
├── errors.txt        (contains the "permission denied" error messages)
└── combined.txt      (contains both stdout and stderr together)
```

{% stepper %}
{% step %}
### Create a working directory

Create a dedicated directory for this tutorial and move into it.

```bash
mkdir ~/tutorial3 && cd ~/tutorial3
```

{% hint style="success" %}
**Expected output:** No output — the prompt returns immediately. This confirms the directory was created and is now your working location.
{% endhint %}
{% endstep %}

{% step %}
### Observe a command that produces both stdout and stderr

Run a command that generates both normal output and error messages at the same time.

```bash
ls /etc /fake-directory-xyz
```

{% hint style="success" %}
**Expected output:**
```
ls: cannot access '/fake-directory-xyz': No such file or directory
/etc:
adjtime
aliases
alternatives
...
```
{% endhint %}

Notice that the error message and the directory listing both appear mixed together on the screen. Both streams are currently going to the same place — your terminal.
{% endstep %}

{% step %}
### Redirect only stdout to a file

Redirect only the normal output — stdout — to a file, leaving errors on screen.

```bash
ls /etc /fake-directory-xyz > output.txt
```

{% hint style="success" %}
**Expected output:**
```
ls: cannot access '/fake-directory-xyz': No such file or directory
```
{% endhint %}

Only the error message appeared. The directory listing went silently into `output.txt` because `>` redirects only stdout (file descriptor 1). The error message uses a different channel — file descriptor 2 — and was not redirected.
{% endstep %}

{% step %}
### Confirm stdout was captured

Verify that the file received the normal output.

```bash
head -5 output.txt
```

{% hint style="success" %}
**Expected output:**
```
/etc:
adjtime
aliases
alternatives
audit
```

The normal output from `ls` is in the file. The error message never entered it.
{% endhint %}
{% endstep %}

{% step %}
### Redirect only stderr to a file

Redirect only the error output — stderr — to its own file using `2>`. The `2` is the file descriptor number for stderr.

```bash
ls /etc /fake-directory-xyz 2> errors.txt
```

{% hint style="success" %}
**Expected output:** The directory listing scrolls past on screen — no error message appears.
```
/etc:
adjtime
aliases
alternatives
...
```
{% endhint %}

The error went to `errors.txt`, while the normal listing continued to the terminal.

{% hint style="warning" %}
There must be **no space** between `2` and `>`. Writing `2 > errors.txt` is a syntax error — the shell will not interpret it as stderr redirection.
{% endhint %}
{% endstep %}

{% step %}
### Confirm stderr was captured

Verify that the errors file contains the error message.

```bash
cat errors.txt
```

{% hint style="success" %}
**Expected output:**
```
ls: cannot access '/fake-directory-xyz': No such file or directory
```

You have now captured stdout and stderr independently. The `2>` operator targets file descriptor 2 exclusively, leaving stdout undisturbed.
{% endhint %}
{% endstep %}

{% step %}
### Redirect stdout and stderr to separate files simultaneously

Combine both redirections in a single command, sending each stream to its own file at the same time.

```bash
ls /etc /fake-directory-xyz > output.txt 2> errors.txt
```

{% hint style="success" %}
**Expected output:** No output — the prompt returns immediately. Both streams were redirected away from the terminal.
{% endhint %}
{% endstep %}

{% step %}
### Verify both files were written

Check both files to confirm each received the correct stream.

```bash
echo "=== output.txt ===" && head -3 output.txt && echo "=== errors.txt ===" && cat errors.txt
```

{% hint style="success" %}
**Expected output:**
```
=== output.txt ===
/etc:
adjtime
aliases
=== errors.txt ===
ls: cannot access '/fake-directory-xyz': No such file or directory
```

Each stream landed in its own file, cleanly separated.
{% endhint %}
{% endstep %}

{% step %}
### Discard errors with /dev/null

Run the same command but silence the error output entirely by redirecting stderr to `/dev/null`, the system's discard device.

```bash
ls /etc /fake-directory-xyz 2> /dev/null
```

{% hint style="success" %}
**Expected output:** The directory listing with no error message.
```
/etc:
adjtime
aliases
alternatives
...
```
{% endhint %}

The error message was sent to `/dev/null` and silently discarded. `/dev/null` accepts anything written to it and throws it away immediately.
{% endstep %}

{% step %}
### Discard all output with &>

Redirect both stdout and stderr to `/dev/null` using the combined `&>` operator, producing complete silence.

```bash
ls /etc /fake-directory-xyz &> /dev/null
```

{% hint style="success" %}
**Expected output:** No output — the prompt returns immediately. Both streams were discarded. The command ran, produced output and errors, and all of it was silently consumed by `/dev/null`.
{% endhint %}

{% hint style="warning" %}
`&>` is a bash-specific operator. In POSIX `sh` scripts, use `> file 2>&1` instead for maximum portability.
{% endhint %}
{% endstep %}

{% step %}
### Capture both streams together with &>

Redirect both stdout and stderr into a single file using `&>`.

```bash
ls /etc /fake-directory-xyz &> combined.txt
```

{% hint style="success" %}
**Expected output:** No output — the prompt returns immediately.
{% endhint %}

Now verify the combined file contains both the error and the directory listing.

```bash
grep -E "cannot access|^/etc:" combined.txt
```

{% hint style="success" %}
**Expected output:**
```
ls: cannot access '/fake-directory-xyz': No such file or directory
/etc:
```

Both streams are present in the same file.
{% endhint %}
{% endstep %}

{% step %}
### Verify the complete final state

Verify that all three files exist in your working directory, matching the target layout shown at the top of this tutorial.

```bash
ls ~/tutorial3/
```

{% hint style="success" %}
**Expected output:**
```
combined.txt  errors.txt  output.txt
```
{% endhint %}
{% endstep %}
{% endstepper %}

{% hint style="success" %}
**You've completed this tutorial.** You can now:

1. Run a command that produces both normal output and error messages simultaneously
2. Redirect only stdout to a file using `>`, leaving errors on screen
3. Redirect only stderr to a file using `2>`, leaving normal output on screen
4. Redirect stdout and stderr to separate files simultaneously in a single command
5. Discard error output silently using `2> /dev/null`
6. Discard all output using `&> /dev/null`
7. Capture both stdout and stderr together into a single file using `&>`
{% endhint %}

## Next Steps

Where to go from here:

- **How-to: Redirect Command Output in Common Administrative Tasks** — apply stderr redirection in real administration scenarios such as `find` and cron
- **Explanation: Understanding I/O Redirection and Pipelines** — understand why stdout and stderr are separate streams and what file descriptors are
- **Reference: I/O Redirection Operators and File Descriptors** — see the complete operator syntax including `2>>`, `&>>`, and `2>&1`