---
description: Shell operators for redirecting standard file descriptors (stdin, stdout, stderr) to files, devices, and other processes via pipelines — covers LPIC-1 exam objective 103.4.
icon: brackets-curly
---

# I/O Redirection and Pipelines Reference

{% hint style="info" %}
This reference covers all Bash redirection operators, pipeline operators, special device files, and `tee` usage for exam objective 103.4. Every operator and ordering rule appears in the tables below.
{% endhint %}

## Standard File Descriptors

| File Descriptor | Name | Abbreviation | Default Connection |
|---|---|---|---|
| `0` | Standard input | stdin | Keyboard |
| `1` | Standard output | stdout | Terminal display |
| `2` | Standard error | stderr | Terminal display |

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
| `>|` | — | Redirects stdout to a file, forcing overwrite even when `noclobber` is set. |
| `<<` | — | Here-document: redirects a multi-line literal block as stdin, terminated by a delimiter word. |
| `<<-` | — | Here-document variant: strips leading tab characters from input lines and the delimiter line. |
| `<<<` | — | Here-string: redirects a single string as stdin, with a newline appended. |
| `[n]<&digit-` | — | Moves input file descriptor `digit` to `n` (or fd 0 if `n` omitted); closes `digit` after duplication. |
| `[n]>&digit-` | — | Moves output file descriptor `digit` to `n` (or fd 1 if `n` omitted); closes `digit` after duplication. |
| `[n]<>` | — | Opens a file for both reading and writing on fd `n` (default fd 0). Creates file if absent. |

{% hint style="warning" %}
`&>` and `>&` are Bash-specific. Use `> file 2>&1` for POSIX-portable scripts. `|&` is also Bash-specific shorthand for `2>&1 |`.
{% endhint %}

{% hint style="danger" %}
`>` truncates an existing file to zero bytes before writing — even if the command produces no output. Using `>` alone with no command creates an empty file or silently destroys existing content.
{% endhint %}

## Pipeline Operators

| Operator | Description |
|---|---|
| `\|` | Connects stdout of the preceding command to stdin of the following command. Commands run in parallel as separate subprocesses. |
| `\|&` | Connects both stdout and stderr of the preceding command to stdin of the following command. Shorthand for `2>&1 \|`. |

## Syntax

{% tabs %}
{% tab title="Output Redirection" %}
{% code title="Syntax" %}
```bash
command [n]> file
command [n]>> file
```
{% endcode %}

{% code title="Example" %}
```bash
ls -l /etc > etclist.txt       # overwrite
date >> etclist.txt            # append
```
{% endcode %}
{% endtab %}

{% tab title="Input Redirection" %}
{% code title="Syntax" %}
```bash
command [n]< file
```
{% endcode %}

{% code title="Example" %}
```bash
wc -l < /etc/passwd
```
{% endcode %}
{% endtab %}

{% tab title="Stderr Redirection" %}
{% code title="Syntax" %}
```bash
command 2> file
command 2>> file
```
{% endcode %}

{% code title="Example" %}
```bash
find / -name "*.conf" 2> errors.txt
```
{% endcode %}
{% endtab %}

{% tab title="Combined stdout+stderr" %}
{% code title="Syntax" %}
```bash
command &> file
command > file 2>&1
command &>> file
command >> file 2>&1
```
{% endcode %}

{% code title="Example" %}
```bash
ls /nonexistent /etc &> all_output.txt
ls /nonexistent /etc > all_output.txt 2>&1
```
{% endcode %}
{% endtab %}

{% tab title="FD Duplication" %}
{% code title="Syntax" %}
```bash
command [n]>&digit
command [n]<&digit
```
{% endcode %}

{% code title="Example" %}
```bash
command > file 2>&1    # stderr duplicated to stdout's current target
command 1>&2           # stdout duplicated to stderr's current target
```
{% endcode %}
{% endtab %}
{% endtabs %}

{% tabs %}
{% tab title="Pipeline" %}
{% code title="Syntax" %}
```bash
command1 | command2 [| command3 ...]
command1 |& command2
```
{% endcode %}

{% code title="Example" %}
```bash
ps aux | grep sshd
ls /usr/bin | sort | uniq | wc -l
command |& grep error
```
{% endcode %}
{% endtab %}

{% tab title="Here-Document" %}
{% code title="Syntax" %}
```bash
command <<DELIMITER
  text
DELIMITER
```
{% endcode %}

{% code title="Example" %}
```bash
cat <<EOF
line one
line two
EOF
```
{% endcode %}
{% endtab %}

{% tab title="Here-String" %}
{% code title="Syntax" %}
```bash
command <<< "string"
```
{% endcode %}

{% code title="Example" %}
```bash
wc -c <<< "hello"
```
{% endcode %}
{% endtab %}
{% endtabs %}

## Redirection Ordering Rules

> Redirections are evaluated **left to right** before the command executes. The target of a file descriptor **at the moment of duplication** determines the result.

| Command | Behavior |
|---|---|
| `command > file 2>&1` | stdout goes to `file`; stderr then duplicated to current stdout (the file). **Both streams go to `file`.** |
| `command 2>&1 > file` | stderr duplicated to current stdout (terminal); stdout then redirected to `file`. **stderr remains on terminal.** |

{% hint style="danger" %}
`2>&1` must appear **after** the stdout redirection (`> file`). Reversed order sends stderr to the terminal, not to the file. This is the most common redirection mistake on the exam.
{% endhint %}

## Pipeline Exit Status

| Condition | Exit Status |
|---|---|
| Default (no `pipefail`) | Exit status of the **last** command in the pipeline. |
| `pipefail` enabled (`set -o pipefail`) | Exit status of the last (rightmost) command to exit non-zero; or `0` if all succeed. |
| Pipeline preceded by `!` | Logical negation of the exit status as described above. |
| Asynchronous pipeline (`&`) | `0` immediately upon launching. |

## Special Device Files

| Path | Description |
|---|---|
| `/dev/null` | Discard device. Accepts any data written to it and discards silently. Reads return zero bytes. |
| `/dev/zero` | Returns a continuous stream of null bytes when read. |
| `/dev/stdin` | Symbolic reference to file descriptor 0 of the current process. |
| `/dev/stdout` | Symbolic reference to file descriptor 1 of the current process. |
| `/dev/stderr` | Symbolic reference to file descriptor 2 of the current process. |
| `/dev/fd/N` | Symbolic reference to file descriptor `N` of the current process. |
| `/dev/tty` | The controlling terminal of the current process. |
| `/dev/tty1` | Virtual console 1. Writable only by root or the user logged into that console. |

## The `tee` Command

| Syntax | Description |
|---|---|
| `command \| tee file` | Reads stdin; writes simultaneously to stdout and to `file`. Overwrites `file` if present. |
| `command \| tee -a file` | Reads stdin; writes simultaneously to stdout and appends to `file`. |

{% code title="Example" %}
```bash
ps aux | tee processes.txt | grep ssh
```
{% endcode %}

## Examples

{% code title="Discard stderr; show stdout only" %}
```bash
find / -name "*.conf" 2> /dev/null
```
{% endcode %}

{% code title="Discard all output" %}
```bash
command > /dev/null 2>&1
```
{% endcode %}

{% code title="Force overwrite with noclobber set" %}
```bash
ls >| existing_file.txt
```
{% endcode %}

{% code title="Combine redirection and pipeline" %}
```bash
grep "FAILED" < syslog | sort > failures.txt
```
{% endcode %}

{% code title="tee: branch a pipeline to file and next command" %}
```bash
ps aux | tee processes.txt | grep ssh
```
{% endcode %}

## Constraints and Gotchas

<details>

<summary>Shell subshell and variable scoping rules</summary>

Each command in a multi-command pipeline executes in its own subshell (separate process). Variable assignments inside a pipeline segment do not persist in the parent shell unless the `lastpipe` shell option is enabled and job control is inactive.

The implicit stderr-to-stdout redirection performed by `|&` occurs after any redirections specified within `command1`.

</details>

<details>

<summary>File descriptor numbering limits</summary>

File descriptors greater than 9 used in redirections may conflict with file descriptors used internally by the shell. Use descriptors 0–9 in shell scripts unless you have explicit need and awareness of shell internals.

</details>

<details>

<summary>Word expansion on redirection targets</summary>

The word following a redirection operator undergoes brace expansion, tilde expansion, parameter expansion, command substitution, arithmetic expansion, quote removal, filename expansion, and word splitting. If it expands to more than one word, Bash reports an ambiguous redirect error.

</details>

<details>

<summary>noclobber option behavior</summary>

The `noclobber` shell option (`set -o noclobber`) prevents `>` from overwriting existing regular files. Use `>|` to force overwrite when `noclobber` is active. The `>` operator still truncates the file to zero bytes before writing even without `noclobber`.

</details>

<details>

<summary>Device file access restrictions</summary>

`/dev/tty1` and other virtual console device files require root privileges to write to directly from a non-root user not logged into that console.

</details>

{% hint style="info" %}
Redirections are processed by the shell before the command executes. The command has no visibility into whether its file descriptors have been redirected.
{% endhint %}

## See Also

| Reference | Description |
|---|---|
| `man bash` §3.6, §3.2.3 | Bash manual sections on Redirections and Pipelines |
| `man tee` | `tee` command reference |
| `man 7 pipe` | Linux kernel pipe mechanism |
| `man 2 open` | `open()` system call and file descriptor behavior |
| `man 2 dup2` | File descriptor duplication system call |