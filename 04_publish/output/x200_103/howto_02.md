---
description: Use grep's -n, -l, and -c flags to control output format — showing line numbers, filenames only, or match counts — when auditing configuration files or scanning logs.
icon: wrench
---

# How to Control grep Output Format with -n, -l, and -c

{% hint style="info" %}
**Prerequisites**

- Read access to `/etc` and at least one log directory such as `/var/log`
- A pattern to search for — examples below use `PermitRootLogin` for config auditing and `error` for log scanning
{% endhint %}

{% stepper %}
{% step %}
### Show line numbers alongside matching lines with -n

Run grep with `-n` to prefix each match with its line number in the file.

```bash
grep -n 'PermitRootLogin' /etc/ssh/sshd_config
```

```
Expected output format:
```

```
38:#PermitRootLogin prohibit-password
```

```
To scan multiple files recursively and still see line numbers:
```

```bash
grep -rn 'PermitRootLogin' /etc/ssh/
```
{% endstep %}

{% step %}
### List only filenames that contain a match with -l

Use `-l` to suppress line content and print only the name of each file that contains at least one match.

```bash
grep -rl 'PermitRootLogin' /etc/ssh/
```

```
To audit which configuration files across a directory contain a directive:
```

```bash
grep -rl 'MaxAuthTries' /etc/
```

{% hint style="info" %}
`-l` stops processing each file after the first match, making it faster than a full scan when only file discovery matters.
{% endhint %}

{% hint style="warning" %}
Do not combine `-l` with `-h`. The `-h` flag suppresses filenames and directly conflicts with `-l`, producing no output.
{% endhint %}
{% endstep %}

{% step %}
### Count matches per file with -c

Use `-c` to print the number of matching lines in each file rather than the lines themselves.

```bash
grep -c 'error' /var/log/messages
```

```
To count across multiple log files at once:
```

```bash
grep -c 'error' /var/log/messages*
```

```
Expected output format:
```

```
/var/log/messages:4
/var/log/messages-20240101:11
/var/log/messages-20240108:0
```

{% hint style="warning" %}
Files with zero matches appear as `filename:0` — they are **not** omitted from output. Pipe to `less` when scanning many files to avoid flooding the terminal: `grep -c 'pattern' /var/log/messages* | less`
{% endhint %}
{% endstep %}

{% step %}
### Combine flags to refine output

Combine `-i` with any output flag to make the search case-insensitive.

Count case-insensitive matches for `error` across all rotated logs:

```bash
grep -ic 'error' /var/log/messages*
```

```
List only files containing a case-insensitive match:
```

```bash
grep -ril 'error' /var/log/
```
{% endstep %}
{% endstepper %}

## Verification

{% hint style="success" %}
**Confirm each flag produces distinct output against the same pattern.**

Run all three commands against `/etc/passwd`:

```bash
grep -c 'nologin' /etc/passwd
grep -l 'nologin' /etc/passwd
grep -n 'nologin' /etc/passwd | head -3
```

Expected results:
- `-c` returns a single integer (e.g., `23`)
- `-l` returns the filename (`/etc/passwd`)
- `-n` returns numbered lines (e.g., `2:daemon:x:2:2:Daemon:/sbin:/sbin/nologin`)

If all three commands run without error and produce output in those formats, the flags are working correctly.
{% endhint %}

## Troubleshooting

{% hint style="warning" %}
**Common problems and fixes**

**`-c` reports `0` for a file you expect to match**
→ Pattern is case-sensitive and case does not match. Add `-i` to make the search case-insensitive.

**`-l` lists no files despite matches being visible with plain grep**
→ `-l` was combined with `-h`, which suppresses filenames. Remove `-h`; it conflicts with `-l`.

**`-n` line numbers are absent when piping output**
→ Some tools reset line-buffering and strip prefixes. Pipe through `cat` first, or redirect grep output to a file and inspect it directly.

**`grep -c` across many files floods the terminal**
→ No pager applied. Pipe to `less`:

```bash
grep -c 'pattern' /var/log/messages* | less
```

**Permission denied errors interrupt a recursive scan**
→ Files in `/etc` or `/var/log` require elevated access. Prefix the command with `sudo`.
{% endhint %}

## Related

- **Reference:** grep options and output flags — grep how-to reference sheet (How-to 5 of 5)
- **Explanation:** Understanding grep and Regular Expressions
- **How-to 1 of 5:** How to Filter Files and Pipelines with Basic grep Patterns
- **How-to 3 of 5:** How to Write Basic Regular Expressions with grep