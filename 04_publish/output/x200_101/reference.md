---
description: Complete syntax, options, metacharacters, variables, builtins, and startup file reference for the Bash shell on RHEL 9, covering exam objective x200_101.
icon: brackets-curly
---

# Bash Shell and Command Syntax Reference

{% hint style="info" %}
This reference covers Bash command structure, quoting, metacharacters, shell variables, builtins, keyboard shortcuts, history syntax, exit codes, and startup file load order for RHEL 9 — exam objective x200\_101.
{% endhint %}

## Command Structure

{% code title="Syntax" %}
```
command [-short_options] [--long-option[=value]] [argument ...]
```
{% endcode %}

| Notation | Meaning |
|---|---|
| `[ ]` | Optional element |
| `< >` | Required element |
| `\|` | Mutually exclusive alternatives |
| `...` | Element is repeatable |

### Pipeline Syntax

{% code title="Syntax" %}
```
command1 | command2
command1 |& command2
```
{% endcode %}

| Operator | Behaviour |
|---|---|
| `\|` | Connects stdout of `command1` to stdin of `command2` |
| `\|&` | Connects both stdout and stderr of `command1` to stdin of `command2` |

### List Operators

{% code title="Syntax" %}
```
command1 ; command2
command1 & command2
command1 && command2
command1 || command2
```
{% endcode %}

| Operator | Behaviour |
|---|---|
| `;` | Execute sequentially; return status of last command |
| `&` | Execute `command1` asynchronously in a subshell |
| `&&` | Execute `command2` only if `command1` returns exit status 0 |
| `\|\|` | Execute `command2` only if `command1` returns non-zero exit status |

{% code title="Example" %}
```bash
# Sequential execution
date ; whoami

# Execute second command only if first succeeds
mkdir /tmp/testdir && echo "created"

# Execute second command only if first fails
cd /nonexistent || echo "directory not found"

# Run a command in the background
sleep 60 &
```
{% endcode %}

---

## Option Forms

| Form | Syntax | Example |
|---|---|---|
| Short option | Single hyphen + single letter | `ls -l` |
| Short options combined | Single hyphen + multiple letters | `ls -la` |
| Long option | Double hyphen + word | `uname --kernel-release` |
| Long option with value | Double hyphen + word + `=` + value | `--output=file.txt` |

{% tabs %}
{% tab title="Short flags" %}
```bash
uname -r
ls -la
```
{% endtab %}

{% tab title="Long flags" %}
```bash
uname --kernel-release
ls --all -l
```
{% endtab %}
{% endtabs %}

{% hint style="warning" %}
A `--` argument signals the end of option processing; all subsequent arguments are treated as operands regardless of leading hyphens. Long option names are case-sensitive.
{% endhint %}

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

{% hint style="warning" %}
An unquoted `#` begins a comment in non-interactive shells and in interactive shells where `interactive_comments` is enabled (the default on RHEL).
{% endhint %}

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

The shell resolves a command name in this priority order:

| Priority | Type | Description |
|---|---|---|
| 1 | Alias | A name mapped to a command string via `alias` |
| 2 | Shell function | A named compound command defined in the shell |
| 3 | Shell builtin | A command implemented internally by the shell |
| 4 | External command | An executable located via `$PATH` lookup |

{% hint style="info" %}
A full or relative path bypasses alias, function, and builtin lookup and directly specifies the executable.
{% endhint %}

{% code title="Example" %}
```bash
# Report how the shell resolves a command name
type ls

# Identify which external binary a command name resolves to
which bash
```
{% endcode %}

---

## Shell Builtins

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

{% code title="Syntax" %}
```bash
# Read a variable
echo $VARNAME

# Assign a variable (no $ on left-hand side)
VARNAME=value

# Export to child processes
export VARNAME=value
```
{% endcode %}

{% hint style="warning" %}
`$PATH` does not include the current directory (`.`) by default on RHEL. Executing a file in the current directory requires an explicit `./filename` prefix.
{% endhint %}

---

## Prompt Format

{% code title="Syntax" %}
```
[username@hostname directory]$
[username@hostname directory]#
```
{% endcode %}

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

{% code title="Example" %}
```bash
# Display command history
history

# Re-execute the most recent command beginning with "ssh"
!ssh

# Re-execute the previous command
!!
```
{% endcode %}

{% hint style="info" %}
History is saved to `$HISTFILE` (default: `~/.bash_history`) when an interactive shell exits.
{% endhint %}

---

## Shell Access Methods

| Method | Description |
|---|---|
| Virtual console (tty) | Direct hardware terminal; accessed via `Ctrl+Alt+F1` through `Ctrl+Alt+F6`; devices `/dev/tty1`–`/dev/tty6` |
| Terminal emulator (pts) | Pseudo-terminal within a graphical desktop environment; device form `/dev/pts/N` |
| SSH remote session | Pseudo-terminal over network; established with `ssh [user@]host` |
| `bash` subshell | New Bash process launched from within an existing shell session |

---

## Session Types

| Axis | Values |
|---|---|
| Interactivity | Interactive / Non-interactive |
| Login state | Login shell / Non-login shell |

{% hint style="warning" %}
Starting a terminal emulator in a graphical environment typically opens a **non-login interactive shell**, not a login shell. `~/.bash_profile` is therefore not sourced; `~/.bashrc` is.
{% endhint %}

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

{% hint style="warning" %}
`/etc/bashrc` is a Red Hat–specific file. The upstream Bash equivalent is `/etc/bash.bashrc`.
{% endhint %}

### Startup File Load Order

| Shell type | Files sourced (in order) |
|---|---|
| Login interactive | `/etc/profile` → `/etc/profile.d/*.sh` → `~/.bash_profile` (or `~/.bash_login`, or `~/.profile`) |
| Non-login interactive | `/etc/bashrc` → `~/.bashrc` |
| Non-interactive | None by default (unless `$BASH_ENV` is set) |

<details>

<summary>Full startup file precedence notes</summary>

- `~/.bash_profile` is checked first; if found, `~/.bash_login` and `~/.profile` are not read.
- `~/.bash_login` is checked second, only if `~/.bash_profile` does not exist.
- `~/.profile` is checked last, only if neither `~/.bash_profile` nor `~/.bash_login` exist.
- `/etc/bashrc` is typically sourced from within `~/.bashrc`, not directly by Bash itself.
- Non-interactive shells (e.g., scripts) source neither `/etc/profile` nor `~/.bashrc` unless `$BASH_ENV` names a file to source.
- When invoked as `sh`, Bash enters POSIX compatibility mode and suppresses Bash-specific extensions.

</details>

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

{% hint style="warning" %}
Exit status values are restricted to integers 0–255. Values outside this range are truncated modulo 256. Access the last exit status with `$?`.
{% endhint %}

---

## Full Usage Examples

{% code title="Example" %}
```bash
# Display kernel release using short option
uname -r

# Display kernel release using long option
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
{% endcode %}

---

## Constraints and Exam-Critical Notes

<details>

<summary>Case sensitivity, spacing, and POSIX behaviour</summary>

- Linux command names, options, arguments, and filenames are **case-sensitive**. `ls`, `LS`, and `Ls` are distinct commands.
- A space is required between a command name and its first option or argument. No space is permitted between a short option flag and its stacked companions (e.g., `-la` not `- la`).
- An unquoted `#` begins a comment in non-interactive shells and in interactive shells where `interactive_comments` is enabled (the default on RHEL).
- Exit status values are restricted to integers 0–255; values outside this range are truncated modulo 256.
- `$PATH` does not include `.` by default on RHEL; use `./filename` to execute files in the current directory.
- `/etc/bashrc` is Red Hat–specific; upstream Bash uses `/etc/bash.bashrc`.
- When invoked as `sh`, Bash enters POSIX compatibility mode and suppresses Bash-specific extensions.
- `~/.bash_profile` is sourced for login shells; `~/.bashrc` is sourced for non-login interactive shells. Starting a terminal emulator in a graphical environment typically opens a non-login interactive shell.

</details>

---

## See Also

- `man bash` — Complete Bash reference manual
- `man builtins` — Description of Bash builtin commands
- `man sh` — POSIX shell specification reference
- `man 5 passwd` — Format of the `/etc/passwd` user database file
- `info bash` — GNU Info documentation for Bash
- `help <builtin>` — Usage information for individual shell builtins