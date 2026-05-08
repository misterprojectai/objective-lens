---
title: "I/O Redirection and Pipelines Reference"
type: reference
quadrant:
  practical_theoretical: theoretical
  work_study: work
exam_objective: "x200_102"
version: "1.0"
status: draft
---

# I/O Redirection and Pipelines Reference

Shell operators that connect a process's standard file descriptors to files, devices, or other processes, substituting for the default keyboard (stdin) and terminal (stdout/stderr) connections.

---

## Overview

Every Linux process inherits three open file descriptors from the kernel at startup: standard input (fd 0), standard output (fd 1), and standard error (fd 2). By default, all three are connected to the terminal. The Bash shell interprets redirection operators and pipeline operators before executing a command, reconfiguring these file descriptors so that commands read from files or write to files and other processes without modification to the command itself.

Redirections are processed left to right in the order they appear on the command line. The `|` and `|&` pipeline operators connect processes through kernel pipe objects; commands in a pipeline execute in parallel as separate subprocesses.

---

## Standard File Descriptors

| File Descriptor | Name | Abbreviation | Default Connection |
|---|---|---|---|
| `0` | Standard input | stdin | Keyboard |
| `1` | Standard output | stdout | Terminal display |
| `2` | Standard error | stderr | Terminal display |

---

## Redirection Operators

| Operator | Full Form | Description |
|---|---|---|
| `>` | `1>` | Redirects stdout to a file. Creates the file if absent; truncates to zero bytes if present. |
| `>>` | `1>>` | Redirects stdout to a file in append mode. Creates the file if absent; adds to end if present. |
| `<` | `0<` | Redirects stdin from a file instead of the keyboard. |
| `2>` | — | Redirects stderr to a file. Creates the file if absent; truncates if present. |
| `2>>` | — | Redirects stderr to a file in append mode. |
| `&>` | `>&` | Redirects both stdout and stderr to a file. Equivalent to `> file 2>&1`. |
| `&>>` | — | Redirects both stdout and stderr to a file in append mode. Equivalent to `>> file 2>&1`. |
| `2>&1` | — | Duplicates stderr (fd 2) to the current target of stdout (fd 1). Order-dependent. |
| `1>&2` | — | Duplicates stdout (fd 1) to the current target of stderr (fd 2). |
| `>|` | — | Redirects stdout to a file, forcing overwrite even when the `noclobber` option is set. |
| `<<` | — | Here-document: redirects a multi-line literal block as stdin, terminated by a delimiter word. |
| `<<-` | — | Here-document variant: strips leading tab characters from input lines and the delimiter line. |
| `<<<` | — | Here-string: redirects a single string as stdin, with a newline appended. |
| `[n]<&digit-` | — | Moves input file descriptor `digit` to `n` (or fd 0 if `n` omitted); closes `digit` after duplication. |
| `[n]>&digit-` | — | Moves output file descriptor `digit` to `n` (or fd 1 if `n` omitted); closes `digit` after duplication. |
| `[n]<>` | — | Opens a file for both reading and writing on file descriptor `n` (default fd 0). Creates file if absent. |

---

## Pipeline Operators

| Operator | Description |
|---|---|
| `\|` | Connects stdout of the preceding command to stdin of the following command. Commands run in parallel as separate subprocesses. |
| `\|&` | Connects both stdout and stderr of the preceding command to stdin of the following command. Shorthand for `2>&1 \|`. |

---

## Syntax

### Output Redirection

```
command [n]> file
command [n]>> file
```

### Input Redirection

```
command [n]< file
```

### Stderr Redirection

```
command 2> file
command 2>> file
```

### Combined stdout and stderr

```
command &> file
command > file 2>&1
command &>> file
command >> file 2>&1
```

### File Descriptor Duplication

```
command [n]>&digit
command [n]<&digit
```

### Pipeline

```
command1 | command2 [| command3 ...]
command1 |& command2
```

### Here-Document

```
command <<DELIMITER
  text
DELIMITER
```

### Here-String

```
command <<< "string"
```

---

## Special Device Files

| Path | Description |
|---|---|
| `/dev/null` | Discard device. Accepts any data written to it and discards it silently. Reads return zero bytes. |
| `/dev/zero` | Returns a continuous stream of null bytes when read. |
| `/dev/stdin` | Symbolic reference to file descriptor 0 of the current process. |
| `/dev/stdout` | Symbolic reference to file descriptor 1 of the current process. |
| `/dev/stderr` | Symbolic reference to file descriptor 2 of the current process. |
| `/dev/fd/N` | Symbolic reference to file descriptor `N` of the current process. |
| `/dev/tty` | The controlling terminal of the current process. |
| `/dev/tty1` | Virtual console 1. Writable only by root or the user logged into that console. |

---

## The `tee` Command

| Syntax | Description |
|---|---|
| `command \| tee file` | Reads stdin; writes simultaneously to stdout and to `file`. Overwrites `file` if present. |
| `command \| tee -a file` | Reads stdin; writes simultaneously to stdout and appends to `file`. |

`tee` allows a pipeline to branch: the data stream continues to the next piped command while also being captured to a file at that intermediate stage.

---

## Pipeline Exit Status

| Condition | Exit Status |
|---|---|
| Default (no `pipefail`) | Exit status of the last command in the pipeline. |
| `pipefail` enabled (`set -o pipefail`) | Exit status of the last (rightmost) command to exit with a non-zero status; or `0` if all commands succeed. |
| Pipeline preceded by `!` | Logical negation of the exit status as described above. |
| Asynchronous pipeline (`&`) | `0` immediately upon launching. |

---

## Redirection Ordering Rules

Redirections are evaluated left to right before the command executes. The target of a file descriptor at the moment of duplication determines the result.

| Command | Behavior |
|---|---|
| `command > file 2>&1` | stdout to `file`; then stderr duplicated to current stdout (the file). Both streams go to `file`. |
| `command 2>&1 > file` | stderr duplicated to current stdout (terminal); then stdout redirected to `file`. stderr remains on terminal. |

---

## Examples

```bash
# Redirect stdout to a file, overwriting existing content
ls -l /etc > etclist.txt
```

```bash
# Append stdout to an existing file
date >> etclist.txt
```

```bash
# Redirect stderr to a file, display stdout on terminal
find / -name "*.conf" 2> errors.txt
```

```bash
# Redirect both stdout and stderr to the same file
ls /nonexistent /etc &> all_output.txt
```

```bash
# Traditional form: redirect both stdout and stderr to one file
ls /nonexistent /etc > all_output.txt 2>&1
```

```bash
# Discard stderr; display only stdout
find / -name "*.conf" 2> /dev/null
```

```bash
# Discard all output
command > /dev/null 2>&1
```

```bash
# Redirect stdin from a file
wc -l < /etc/passwd
```

```bash
# Pipe stdout of one command to stdin of next
ps aux | grep sshd
```

```bash
# Pipe both stdout and stderr to next command
command |& grep error
```

```bash
# Multi-stage pipeline
ls /usr/bin | sort | uniq | wc -l
```

```bash
# tee: write to file and continue pipeline
ps aux | tee processes.txt | grep ssh
```

```bash
# Combine redirection and pipeline
grep "FAILED" < syslog | sort > failures.txt
```

```bash
# Here-document
cat <<EOF
line one
line two
EOF
```

```bash
# Here-string
wc -c <<< "hello"
```

```bash
# Force overwrite with noclobber set
ls >| existing_file.txt
```

---

## Notes and Constraints

- Redirections are processed by the shell before the command executes; the command has no visibility into whether its file descriptors have been redirected.
- The `>` operator truncates an existing file to zero bytes before writing, even if the command produces no output.
- Using `>` alone with no preceding command truncates an existing file or creates a new empty file.
- The `noclobber` shell option (`set -o noclobber`) prevents `>` from overwriting existing regular files; `>|` overrides this protection.
- `2>&1` must appear after the stdout redirection (`> file`) to send both streams to the file; reversed order sends stderr to the terminal.
- `&>` and `>&` are Bash-specific; `> file 2>&1` is the POSIX-portable equivalent.
- Each command in a multi-command pipeline executes in its own subshell (separate process); variable assignments inside a pipeline segment do not persist in the parent shell unless the `lastpipe` shell option is enabled and job control is inactive.
- The `|&` operator is Bash-specific shorthand for `2>&1 |`.
- The implicit stderr-to-stdout redirection performed by `|&` occurs after any redirections specified within `command1`.
- File descriptors greater than 9 used in redirections may conflict with file descriptors used internally by the shell.
- `/dev/tty1` and other virtual console device files require root privileges to write to directly from a non-root user not logged into that console.
- Word following a redirection operator undergoes brace expansion, tilde expansion, parameter expansion, command substitution, arithmetic expansion, quote removal, filename expansion, and word splitting; if it expands to more than one word, Bash reports an error.
- Applies to RHEL 9 / Rocky Linux 9 with Bash as the interactive shell.

---

## See Also

- `man bash` — Bash manual; sections 3.6 (Redirections) and 3.2.3 (Pipelines)
- `man tee` — `tee` command reference
- `man 7 pipe` — Linux kernel pipe mechanism
- `man 2 open` — `open()` system call and file descriptor behavior
- `man 2 dup2` — file descriptor duplication system call
- [Explanation: Understanding I/O Redirection and Pipelines](explanation-io-redirection.md) — conceptual background on file descriptors, STDIO, and the Unix data stream model