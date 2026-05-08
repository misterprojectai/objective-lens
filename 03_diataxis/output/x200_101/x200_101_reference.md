---
title: "Bash Shell and Command Syntax Reference"
type: reference
quadrant:
  practical_theoretical: theoretical
  work_study: work
exam_objective: "x200_101"
version: "1.0"
status: draft
---

# Bash Shell and Command Syntax Reference

Bash (Bourne-Again SHell) is the default interactive shell on Red Hat Enterprise Linux, a POSIX-conformant command interpreter and macro processor that provides the user interface to the Linux operating system.

---

## Overview

`bash` is a user-space process that reads input from a terminal, file, or string; parses it into commands; and communicates with the Linux kernel via system calls to execute those commands. It is both a command interpreter and a programming language. Bash is the default shell on RHEL 9 and is part of the GNU project. It descends from the Bourne shell (`sh`) and incorporates features from the Korn shell (`ksh`) and C shell (`csh`).

Shell sessions are classified by two independent axes:

| Axis | Values |
|---|---|
| Interactivity | Interactive / Non-interactive |
| Login state | Login shell / Non-login shell |

---

## Syntax

### Command Structure

```
command [-short_options] [--long-option[=value]] [argument ...]
```

| Notation | Meaning |
|---|---|
| `[ ]` | Optional element |
| `< >` | Required element |
| `\|` | Mutually exclusive alternatives |
| `...` | Element is repeatable |

### Simple Command Form

```
command [argument ...]
```

The first word is the command name. Remaining words are arguments. Words are separated by unquoted metacharacters.

### Pipeline Form

```
command1 | command2
command1 |& command2
```

`|` connects stdout of `command1` to stdin of `command2`. `|&` connects both stdout and stderr of `command1` to stdin of `command2`.

### List Forms

```
command1 ; command2
command1 & command2
command1 && command2
command1 || command2
```

| Operator | Behaviour |
|---|---|
| `;` | Execute sequentially; return status of last command |
| `&` | Execute `command1` asynchronously in a subshell |
| `&&` | Execute `command2` only if `command1` returns exit status 0 |
| `\|\|` | Execute `command2` only if `command1` returns non-zero exit status |

---

## Option Forms

Options modify command behaviour. Two forms exist:

| Form | Syntax | Example |
|---|---|---|
| Short option | Single hyphen + single letter | `ls -l` |
| Short options combined | Single hyphen + multiple letters | `ls -la` |
| Long option | Double hyphen + word | `uname --kernel-release` |
| Long option with value | Double hyphen + word + `=` + value | `--output=file.txt` |

Short options may be stacked (combined) after a single hyphen where the command supports it. Long option names are case-sensitive. A `--` argument signals the end of option processing; subsequent arguments are treated as operands regardless of leading hyphens.

---

## Shell Metacharacters

Unquoted metacharacters separate words and have special meaning to the shell.

| Character | Class | Function |
|---|---|---|
| space, tab | Blank | Word separator |
| `\n` | Newline | Command terminator |
| `\|` | Operator | Pipeline |
| `&` | Operator | Background / AND-list component |
| `;` | Operator | Sequential command separator |
| `(` `)` | Operator | Subshell grouping |
| `<` `>` | Operator | Redirection |
| `#` | Comment | Introduces a comment; remainder of line ignored |

---

## Quoting Mechanisms

| Mechanism | Syntax | Effect |
|---|---|---|
| Escape character | `\` | Preserves literal value of the immediately following character; `\newline` is treated as line continuation |
| Single quotes | `'string'` | Preserves literal value of every character within; no substitutions performed; a single quote cannot appear inside single quotes |
| Double quotes | `"string"` | Preserves literal value of all characters except `$`, `` ` ``, `\`, and (when history expansion is enabled) `!`; parameter and command substitution still occur |
| Dollar-single quotes | `$'string'` | Expands backslash-escape sequences within `string` |

---

## Command Types

The shell resolves a command name in this order:

| Priority | Type | Description |
|---|---|---|
| 1 | Alias | A name mapped to a command string via `alias` |
| 2 | Shell function | A named compound command defined in the shell |
| 3 | Shell builtin | A command implemented internally by the shell |
| 4 | External command | An executable located via `$PATH` lookup |

A full or relative path bypasses alias, function, and builtin lookup and directly specifies the executable.

---

## Shell Builtins Relevant to This Objective

| Builtin | Description |
|---|---|
| `cd` | Changes the current working directory; cannot be implemented as an external command |
| `echo` | Writes arguments to standard output |
| `exit` | Terminates the current shell session with an optional exit status |
| `export` | Marks variables for export to child process environments |
| `help` | Displays usage information for shell builtins |
| `history` | Displays or manipulates the command history list |
| `pwd` | Prints the current working directory |
| `type` | Reports how the shell would interpret a given name |
| `unset` | Removes a variable or function from the shell environment |
| `which` | Reports the path of an external command (not a builtin on all systems) |

---

## Key Shell Variables

| Variable | Description |
|---|---|
| `$PATH` | Colon-separated list of directories searched for external commands |
| `$HOME` | Absolute path of the current user's home directory |
| `$USER` | Username of the current user |
| `$SHELL` | Path of the current user's login shell as recorded in `/etc/passwd` |
| `$PS1` | Primary prompt string; displayed before each interactive command |
| `$PS2` | Secondary prompt string; displayed for multi-line command continuation |
| `$HISTFILE` | Path of the file where command history is saved on shell exit |
| `$HISTSIZE` | Maximum number of commands retained in the in-memory history list |
| `$?` | Exit status of the most recently executed foreground command |
| `$0` | Name or path of the currently running shell or script |
| `$$` | PID of the current shell process |

Variable values are accessed by prefixing the variable name with `$`. Assignment uses no `$`: `VARNAME=value`.

---

## Prompt Format (RHEL Default)

```
[username@hostname directory]$
[username@hostname directory]#
```

| Prompt Element | Meaning |
|---|---|
| `username` | Effective username of the logged-in user |
| `hostname` | Short hostname of the system |
| `directory` | Current working directory; `~` represents `$HOME` |
| `$` | Prompt character for regular (non-root) users |
| `#` | Prompt character for the root user (UID 0) |

---

## Keyboard Shortcuts

| Shortcut | Effect |
|---|---|
| `Ctrl+A` | Moves cursor to beginning of the command line |
| `Ctrl+E` | Moves cursor to end of the command line |
| `Ctrl+C` | Sends SIGINT to the foreground process; interrupts current command |
| `Ctrl+D` | Sends EOF; exits the current shell session if the line is empty |
| `Ctrl+L` | Clears the terminal screen; equivalent to `clear` |
| `Ctrl+U` | Deletes all text from the cursor to the beginning of the line |
| `Ctrl+R` | Initiates reverse incremental search of command history |
| `Up Arrow` | Recalls the previous command from history |
| `Down Arrow` | Recalls the next command from history |
| `Tab` | Triggers command and filename completion |

---

## Command History

| Syntax | Description |
|---|---|
| `history` | Displays the numbered command history list |
| `!n` | Re-executes history entry number `n` |
| `!!` | Re-executes the most recent command |
| `!string` | Re-executes the most recent command beginning with `string` |
| `!?string` | Re-executes the most recent command containing `string` |
| `Ctrl+R` | Incrementally searches history in reverse |

History is saved to `$HISTFILE` (default: `~/.bash_history`) when an interactive shell exits.

---

## Shell Access Methods

| Method | Description |
|---|---|
| Virtual console (tty) | Direct hardware terminal; accessed via `Ctrl+Alt+F1` through `Ctrl+Alt+F6`; devices `/dev/tty1`–`/dev/tty6` |
| Terminal emulator (pts) | Pseudo-terminal within a graphical desktop environment; device form `/dev/pts/N` |
| SSH remote session | Pseudo-terminal over network; established with `ssh [user@]host` |
| `bash` subshell | New Bash process launched from within an existing shell session |

---

## Files and Paths

| Path | Purpose |
|---|---|
| `/bin/bash` | Bash executable binary |
| `/etc/passwd` | User account database; final field of each record specifies the user's login shell |
| `/etc/shells` | List of valid login shells available on the system |
| `/etc/profile` | System-wide startup file; sourced by login shells |
| `/etc/bashrc` | System-wide per-interactive-shell startup file; sourced for every non-login interactive shell and every subshell |
| `/etc/profile.d/*.sh` | Drop-in shell scripts sourced by `/etc/profile` at login |
| `~/.bash_profile` | User-level login shell startup file; sourced by login shells (checked before `~/.bash_login` and `~/.profile`) |
| `~/.bashrc` | User-level startup file; sourced by non-login interactive shells |
| `~/.bash_logout` | User-level file; sourced when a login shell exits |
| `~/.bash_history` | Default location of the persistent command history file |

### Login vs. Non-login Shell Startup File Order

| Shell type | Files sourced (in order) |
|---|---|
| Login interactive | `/etc/profile` → `/etc/profile.d/*.sh` → `~/.bash_profile` (or `~/.bash_login`, or `~/.profile`) |
| Non-login interactive | `/etc/bashrc` → `~/.bashrc` |
| Non-interactive | None by default (unless `$BASH_ENV` is set) |

---

## Exit Codes

| Code | Meaning |
|---|---|
| `0` | Success |
| `1` | General error |
| `2` | Misuse of shell builtins (incorrect syntax or invalid arguments) |
| `126` | Command found but not executable |
| `127` | Command not found |
| `128+n` | Command terminated by signal `n` |
| `130` | Command terminated by `Ctrl+C` (SIGINT, signal 2) |

The exit status of the most recently executed command is available in `$?`. The return value is restricted to 8 bits (0–255).

---

## Examples

```bash
# Display kernel name and release using short option
uname -r

# Display kernel name using long option
uname --kernel-release

# Combine short options: list all files in long format
ls -la

# Execute two commands sequentially
date ; whoami

# Execute second command only if first succeeds
mkdir /tmp/testdir && echo "created"

# Execute second command only if first fails
cd /nonexistent || echo "directory not found"

# Run a command in the background
sleep 60 &

# Display the value of an environment variable
echo $PATH

# Report how the shell resolves a command name
type ls

# Display command history
history

# Re-execute the most recent command beginning with "ssh"
!ssh

# Identify which external binary a command name resolves to
which bash
```

---

## Notes and Constraints

- Linux (and Bash) command names, options, arguments, and filenames are case-sensitive. `ls`, `LS`, and `Ls` are distinct.
- A space is required between a command name and its first option or argument; no space is permitted between a short option flag and its stacked companions (e.g., `-la` not `- la`).
- An unquoted `#` begins a comment in non-interactive shells and in interactive shells where `interactive_comments` is enabled (the default).
- Exit status values are restricted to integers 0–255; values outside this range are truncated modulo 256.
- The `$PATH` variable does not include the current directory (`.`) by default on RHEL; executing a file in the current directory requires an explicit `./filename` prefix.
- `/etc/bashrc` is a Red Hat–specific file; the upstream Bash equivalent is `/etc/bash.bashrc`.
- When invoked as `sh`, Bash enters POSIX compatibility mode and suppresses Bash-specific extensions.
- `~/.bash_profile` is sourced for login shells; `~/.bashrc` is sourced for non-login interactive shells. Starting a terminal emulator in a graphical environment typically opens a non-login interactive shell.
- Requires RHEL 9 / Rocky Linux 9.

---

## See Also

- `man bash` — Complete Bash reference manual
- `man builtins` — Description of Bash builtin commands
- `man sh` — POSIX shell specification reference
- `man 5 passwd` — Format of the `/etc/passwd` user database file
- `info bash` — GNU Info documentation for Bash
- `help <builtin>` — Usage information for individual shell builtins
- [Explanation: Understanding the Linux Shell and Command Syntax](../explanation/understanding-the-linux-shell-and-command-syntax.md) — Conceptual background for this reference