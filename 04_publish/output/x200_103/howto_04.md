---
description: Search multiple files simultaneously using globs and recursive search, and display surrounding context lines around each match with grep context flags.
icon: wrench
---

# How to Search Across Multiple Files and Show Match Context

{% hint style="info" %}
**Prerequisites**

- Read access to the directory you intend to search (`/var/log` requires `sudo` for some files)
- A search pattern and a target directory or file glob in hand
{% endhint %}

{% stepper %}
{% step %}
### Search Multiple Files Using a Glob

Pass a glob pattern as the file argument to search all matching files in one command.

```bash
grep -i 'eth' /var/log/messages*
```

`grep` prefixes each matching line with the filename when more than one file is searched.
{% endstep %}

{% step %}
### Search a Directory Recursively

Use `-r` to descend into subdirectories and search every file under a given path.

```bash
grep -r 'eth' /var/log/
```

```
To restrict the recursive search to files matching a name pattern, use `--include`.
```

```bash
grep -r --include='*.conf' 'Listen' /etc/
```

{% hint style="warning" %}
Always quote the `--include` value. If the shell expands the glob before `grep` receives it, the pattern will match no files.
{% endhint %}
{% endstep %}

{% step %}
### Show Lines After Each Match with `-A`

Use `-A` followed by a number to print that many lines **after** each matching line.

```bash
grep -A 2 'error' /var/log/messages
```
{% endstep %}

{% step %}
### Show Lines Before Each Match with `-B`

Use `-B` followed by a number to print that many lines **before** each matching line.

```bash
grep -B 2 'error' /var/log/messages
```
{% endstep %}

{% step %}
### Show Lines Before and After Each Match with `-C`

Use `-C` followed by a number to print that many lines of context on **both sides** of each match.

```bash
grep -C 3 'error' /var/log/messages
```

{% hint style="info" %}
When multiple matches appear close together, `grep` merges the context blocks and separates distinct groups with a `--` separator line in the output.
{% endhint %}
{% endstep %}

{% step %}
### Combine Recursive Search with Context Flags

Use `-r` and a context flag together to locate relevant entries across an entire directory tree while preserving surrounding context.

```bash
grep -r -C 2 'failed' /var/log/
```

```
To also show the line number of each match, add `-n`.
```

```bash
grep -r -n -C 2 'failed' /var/log/
```
{% endstep %}
{% endstepper %}

## Verification

{% hint style="success" %}
**Confirm output format is correct**

Run the following command against a known file:

```bash
grep -r -n -C 1 'error' /var/log/messages*
```

Expected output characteristics:
- Match lines are prefixed with `filename:linenumber:`
- Context lines use `-` as the separator character between filename and line number (e.g., `filename-linenumber-`)
- Distinct match groups are separated by a `--` line
{% endhint %}

## Troubleshooting

{% hint style="warning" %}
**Common problems and fixes**

| Symptom | Cause | Fix |
|---|---|---|
| `grep: /var/log/messages: Permission denied` | File is owned by root; current user lacks read permission | Prepend `sudo` to the command |
| No output from a recursive search | Pattern or path is wrong, or no files contain the pattern | Verify the path with `ls`; test the pattern against a single known file first |
| Output floods the terminal with no context separators | `-C 0` or no context flag set | Add `-C 2` or appropriate `-A`/`-B` values; pipe through `less` for large results |
| Filenames not shown in output | Only one file matched — glob resolved to a single file | Add `-H` to force filename display regardless of match count |
| `--include` pattern matches no files | Shell expanded the glob before `grep` received it | Quote the value: `--include='*.conf'` |
{% endhint %}