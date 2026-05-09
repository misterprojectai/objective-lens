---
description: Filter /var/log/messages and dmesg output to lines matching a literal string or case-insensitive pattern using grep.
icon: wrench
---

# How to Search Log Files for Specific Events with grep

{% hint style="info" %}
**Prerequisites**

- Root or `sudo` access — required to read `/var/log/messages`
- A running RHEL 9 system with populated log files
{% endhint %}

{% stepper %}
{% step %}
### Search `/var/log/messages` for a literal string

Run `grep` against the log file with the string you want to find.

```bash
grep 'error' /var/log/messages
```

{% hint style="warning" %}
The match is case-sensitive. `error`, `Error`, and `ERROR` are treated as distinct strings.
{% endhint %}
{% endstep %}

{% step %}
### Search case-insensitively with `-i`

Add `-i` to match the string regardless of letter case.

```bash
grep -i 'error' /var/log/messages
```

This matches `error`, `Error`, `ERROR`, and any mixed-case variant.
{% endstep %}

{% step %}
### Filter `dmesg` output by piping through grep

Pipe `dmesg` into `grep` to search kernel ring buffer messages without writing to a file first.

```bash
dmesg | grep -i 'eth'
```

```
To search for a hardware event by component name:
```

```bash
dmesg | grep -i 'usb'
```
{% endstep %}

{% step %}
### Search across multiple rotated log files at once

Pass a glob to search all `messages*` files in `/var/log` in a single command.

```bash
cd /var/log && grep -i 'eth' messages*
```

Each matching line is prefixed with the filename it came from.
{% endstep %}

{% step %}
### Exclude irrelevant lines with `-v`

Invert the match to discard lines containing a known noisy string.

```bash
grep -v 'NetworkManager' /var/log/messages
```

```
Combine with a positive match by chaining pipes:
```

```bash
grep -i 'eth' /var/log/messages | grep -v 'NetworkManager'
```
{% endstep %}
{% endstepper %}

## Verification

{% hint style="success" %}
**Confirm grep is returning matches from the correct file:**

```bash
grep -i 'kernel' /var/log/messages | head -5
```

Expected result: five lines from `/var/log/messages`, each containing `kernel`, `Kernel`, or `KERNEL` in any position.
{% endhint %}

## Troubleshooting

{% hint style="warning" %}
**Common issues and fixes**

| Symptom | Cause | Fix |
|---|---|---|
| `Permission denied` when reading `/var/log/messages` | File is root-readable only | Prefix the command with `sudo` |
| No output from `grep -i 'eth' /var/log/messages` | No matching events in the current log file | Run `grep -i 'eth' /var/log/messages*` to include rotated archives |
| `grep: /var/log/messages: No such file or directory` | System uses the journal instead of a syslog file | Use `journalctl \| grep -i 'eth'` as an equivalent |
| Output floods the terminal | Pattern is too broad | Pipe through `head -20` or `less` to page the output |
{% endhint %}