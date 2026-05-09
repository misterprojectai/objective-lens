---
kind: tutorial

title: "Audit the Shell Environment Before Running Administrative Tasks"

description: |
  Learn how to inspect and document the active shell, user identity, environment
  variables, and $PATH state before executing privileged commands — and how to
  detect unexpected variable overrides that could undermine a root session.

categories:
  - linux

tagz:
  - rhcsa
  - bash
  - shell
  - permissions

createdAt: 2025-01-01
updatedAt: 2025-01-01

cover: __static__/cover.png

playground:
  name: rockylinux
  machines:
    - name: rocky-01
      resources:
        cpuCount: 2
        ramSize: 2Gi

tasks:
  init_history_flush:
    init: true
    machine: rocky-01
    user: laborant
    run: |
      echo 'PROMPT_COMMAND="history -a; $PROMPT_COMMAND"' >> /home/laborant/.bashrc
      chown laborant:laborant /home/laborant/.bashrc

  verify_shell_version:
    machine: rocky-01
    user: laborant
    run: |
      grep -q 'bash --version' /home/laborant/.bash_history && exit 0 || exit 1
    hintcheck: |
      echo "Run: bash --version"

  verify_ps_self:
    machine: rocky-01
    user: laborant
    run: |
      grep -qE 'ps -p \$\$' /home/laborant/.bash_history && exit 0 || exit 1
    hintcheck: |
      echo "Run: ps -p \$\$"

  verify_id_command:
    machine: rocky-01
    user: laborant
    run: |
      grep -qE '^id$' /home/laborant/.bash_history && exit 0 || exit 1
    hintcheck: |
      echo "Run: id"

  verify_env_snapshot:
    machine: rocky-01
    user: laborant
    run: |
      grep -q 'env-before.txt' /home/laborant/.bash_history && \
        test -f /tmp/env-before.txt && exit 0 || exit 1
    hintcheck: |
      echo "Run: env | sort > /tmp/env-before.txt"

  verify_set_snapshot:
    machine: rocky-01
    user: laborant
    run: |
      grep -q 'set-before.txt' /home/laborant/.bash_history && \
        test -f /tmp/set-before.txt && exit 0 || exit 1
    hintcheck: |
      echo "Run: set | sort > /tmp/set-before.txt"

  verify_path_list:
    machine: rocky-01
    user: laborant
    run: |
      grep -qE "echo \\\$PATH.*tr.*:" /home/laborant/.bash_history && exit 0 || exit 1
    hintcheck: |
      echo "Run: echo \$PATH | tr ':' '\n'"

  verify_path_grep:
    machine: rocky-01
    user: laborant
    run: |
      grep -qE "grep -E.*home.*local" /home/laborant/.bash_history && exit 0 || exit 1
    hintcheck: |
      echo "Run: echo \$PATH | tr ':' '\\n' | grep -E '^/home|\\.local'"

  verify_type_sudo:
    machine: rocky-01
    user: laborant
    run: |
      grep -qE '^type sudo' /home/laborant/.bash_history && exit 0 || exit 1
    hintcheck: |
      echo "Run: type sudo"

  verify_declare_f:
    machine: rocky-01
    user: laborant
    run: |
      grep -qE '^declare -f' /home/laborant/.bash_history && exit 0 || exit 1
    hintcheck: |
      echo "Run: declare -f sudo"

  verify_grep_profile:
    machine: rocky-01
    user: laborant
    run: |
      grep -qE 'grep -r.*profile' /home/laborant/.bash_history && exit 0 || exit 1
    hintcheck: |
      echo "Run: grep -r 'VARIABLE_NAME' /etc/profile /etc/profile.d/ ~/.bashrc"

  verify_env_diff:
    machine: rocky-01
    user: laborant
    run: |
      grep -q 'env-after.txt' /home/laborant/.bash_history && \
        test -f /tmp/env-after.txt && exit 0 || exit 1
    hintcheck: |
      echo "Run: env | sort > /tmp/env-after.txt  then  diff /tmp/env-before.txt /tmp/env-after.txt"

  verify_final_check:
    machine: rocky-01
    user: laborant
    run: |
      grep -qE 'alias.*grep.*sudo' /home/laborant/.bash_history && exit 0 || exit 1
    hintcheck: |
      echo "Run the combined verification one-liner from Step 9."
---

# Audit the Shell Environment Before Running Administrative Tasks

::remark-box
---
kind: info
---
**Before running any commands:** click the **+** button in the terminal tab bar to open a new terminal tab. The playground history tracking activates in new sessions only. Commands run in the original tab will not register for task verification.
::

On the RHCSA exam you will often need to execute privileged commands or switch between user contexts. A wrong `$PATH`, a lurking alias, or an inherited variable can silently alter the behaviour of those commands — causing subtle failures that are hard to debug under time pressure. This tutorial gives you a repeatable pre-flight checklist you can run in any shell session before touching anything critical.

---

## Step 1 — Confirm the Active Shell and Its Version

Before trusting any shell-specific behaviour, verify which shell binary is actually running and what version it is.

```bash
echo $SHELL
bash --version
```

`$SHELL` reports the login shell registered in `/etc/passwd`. The version string from `bash --version` tells you whether you can rely on features like process substitution or associative arrays.

Now cross-check that the *running process* is actually Bash — not a dash or sh substituted by a script or `su` invocation:

```bash
ps -p $$
```

`$$` expands to the PID of the current shell. The `CMD` column in the output should show `bash`.

::simple-task
---
:tasks: tasks
:name: verify_shell_version
---
#active
Run `bash --version` to confirm the Bash version in your session.

#completed
Done — you confirmed the Bash version 🎉
::

::simple-task
---
:tasks: tasks
:name: verify_ps_self
---
#active
Run `ps -p $$` to confirm the running shell process.

#completed
Done — shell process confirmed 🎉
::

::hint-box
---
:summary: "ps -p $$ shows 'sh' instead of 'bash'"
---
If the `CMD` column shows `sh`, your session was launched by a wrapper script that invoked `/bin/sh` rather than `/bin/bash`. Exit and re-open the terminal, or explicitly launch `bash` before continuing.
::

---

## Step 2 — Confirm the Effective User Identity

Verify who the shell believes you are — both the login identity and the effective user.

```bash
whoami
id
```

`whoami` reports the effective UID name. `id` reports the UID, GID, and all supplementary groups — always use `id` when group membership matters (for example, when checking access to the `wheel` group for `sudo`).

If you have escalated with `sudo -i` or `su -`, confirm the identity variables carried over:

```bash
echo $USER
echo $LOGNAME
echo $HOME
```

::remark-box
---
kind: warning
---
**Exam tip:** `$USER` can be wrong after `sudo`. Some sudoers configurations preserve the invoking user's `$USER` variable even after escalation. Always rely on `id` — not `$USER` — to determine your actual effective identity.
::

::simple-task
---
:tasks: tasks
:name: verify_id_command
---
#active
Run `id` to display your current UID, GID, and group memberships.

#completed
Done — identity confirmed with `id` 🎉
::

---

## Step 3 — Capture All Exported Environment Variables

Dump the full exported environment to a baseline snapshot **before** making any changes. You can then diff against it later to see what escalation or a script added or removed.

```bash
env | sort
```

Save the snapshot:

```bash
env | sort > /tmp/env-before.txt
```

::simple-task
---
:tasks: tasks
:name: verify_env_snapshot
---
#active
Run `env | sort > /tmp/env-before.txt` to save a baseline of exported variables.

#completed
Done — baseline snapshot saved 🎉
::

---

## Step 4 — Capture Shell-Local Variables Too

`env` only shows *exported* variables. Shell-local variables and functions are invisible to `env` but can still shadow or interfere with commands. Use `set` to see everything:

```bash
set | sort
```

Save this snapshot as well:

```bash
set | sort > /tmp/set-before.txt
```

::remark-box
---
kind: info
---
`set` output is verbose — it includes all shell functions. Pipe it through `grep -v '()$'` if you only want scalar variables. For the snapshot file, keeping functions included is useful because function shadows are a common source of surprises.
::

::simple-task
---
:tasks: tasks
:name: verify_set_snapshot
---
#active
Run `set | sort > /tmp/set-before.txt` to capture all shell variables and functions.

#completed
Done — full variable snapshot saved 🎉
::

---

## Step 5 — Inspect and Validate `$PATH`

Display the current `$PATH` as a readable list:

```bash
echo $PATH | tr ':' '\n'
```

Reading a colon-separated single line is error-prone. The `tr` command turns each `:` separator into a newline, giving you one directory per line.

::simple-task
---
:tasks: tasks
:name: verify_path_list
---
#active
Run `echo $PATH | tr ':' '\n'` to list each `$PATH` directory on its own line.

#completed
Done — `$PATH` listed cleanly 🎉
::

Now scan for user-owned directories that should not appear in a privileged shell:

```bash
echo $PATH | tr ':' '\n' | grep -E '^/home|\.local'
```

::simple-task
---
:tasks: tasks
:name: verify_path_grep
---
#active
Run the `grep -E '^/home|\.local'` pipeline above to check for user directories in `$PATH`.

#completed
Done — `$PATH` scanned for user directories 🎉
::

::remark-box
---
kind: warning
---
If the grep returns any output, a user-owned directory (e.g. `~/.local/bin` or `/home/laborant/bin`) is present in a privileged shell's `$PATH`. A rogue binary placed there could intercept any command you run as root. Investigate and clean `$PATH` before proceeding.
::

---

## Step 6 — Detect Variable Overrides That Shadow Standard Commands

Check that `/usr/bin` is present in `$PATH` — a result of `0` means it is missing:

```bash
echo $PATH | tr ':' '\n' | grep -c '^/usr/bin$'
```

Expected result: `1`.

Now check for **aliases** hiding commands you are about to run:

```bash
type sudo
type useradd
type passwd
```

If `type` returns `is aliased to`, the alias is intercepting that command. List all aliases to find the definition:

```bash
alias
```

Check for **shell functions** that shadow commands:

```bash
declare -f sudo
declare -f useradd
```

Any output here means a function is intercepting that command name — it will run *instead of* the real binary.

::simple-task
---
:tasks: tasks
:name: verify_type_sudo
---
#active
Run `type sudo` to check whether `sudo` is a real binary or an alias/function.

#completed
Done — `sudo` identity verified 🎉
::

::simple-task
---
:tasks: tasks
:name: verify_declare_f
---
#active
Run `declare -f sudo` to check for shell functions shadowing `sudo`.

#completed
Done — function shadow check complete 🎉
::

::hint-box
---
:summary: "type useradd returns 'useradd is a function'"
---
A shell function is intercepting `useradd`. Run `declare -f useradd` to inspect what it does, then `unset -f useradd` to remove it for the current session. Trace the definition's origin with `grep -r useradd /etc/profile.d/ ~/.bashrc`.
::

---

## Step 7 — Trace the Origin of a Suspicious Variable

If a variable holds an unexpected value, identify which startup file set it:

```bash
grep -r 'VARIABLE_NAME' /etc/profile /etc/profile.d/ ~/.bash_profile ~/.bashrc ~/.bash_login
```

Replace `VARIABLE_NAME` with the actual variable name. The file that contains the assignment is the source — edit or comment out the line there to make the fix permanent.

::simple-task
---
:tasks: tasks
:name: verify_grep_profile
---
#active
Run `grep -r 'VARIABLE_NAME' /etc/profile /etc/profile.d/ ~/.bashrc` (substituting a real variable name such as `PATH` or `HOME`).

#completed
Done — startup file search complete 🎉
::

::remark-box
---
kind: info
---
Common culprits for unexpected variable values: `/etc/profile.d/*.sh` scripts that ship with packages, and `~/.bashrc` blocks added by tools like `conda`, `nvm`, or `rbenv`. On a freshly provisioned exam machine these are less likely, but always worth a quick check.
::

---

## Step 8 — Compare the Environment After Escalation

After opening a new `sudo -i` session or running `su -`, compare the environment against the pre-escalation snapshot from Step 3:

```bash
env | sort > /tmp/env-after.txt
diff /tmp/env-before.txt /tmp/env-after.txt
```

Lines beginning with `>` are variables present **only** in the escalated session.
Lines beginning with `<` were present before escalation and were **dropped**.

::simple-task
---
:tasks: tasks
:name: verify_env_diff
---
#active
Run `env | sort > /tmp/env-after.txt` followed by `diff /tmp/env-before.txt /tmp/env-after.txt`.

#completed
Done — environment diff complete 🎉
::

::remark-box
---
kind: info
---
`su -` performs a full login and is expected to drop most of your previous variables — that is normal and desired. `sudo -i` also resets the environment but the exact variables preserved depend on the `env_reset` and `env_keep` settings in `/etc/sudoers`. If a required variable disappeared after escalation, re-export it explicitly.
::

---

## Step 9 — Run the Combined Pre-Flight Check

Run this one-liner to confirm the environment is clean for privileged work:

```bash
id && echo $SHELL && echo $PATH | tr ':' '\n' | head -6 && alias | grep -E 'sudo|useradd|passwd' || echo "no critical aliases found"
```

Expected result:
- `id` shows the intended effective UID
- `$SHELL` is `/bin/bash`
- The first six `$PATH` entries are all system directories (no `/home/...`)
- No aliases intercept `sudo`, `useradd`, or `passwd`

::simple-task
---
:tasks: tasks
:name: verify_final_check
---
#active
Run the combined one-liner above to verify your environment is clean.

#completed
Environment audit complete — you are ready for privileged work 🎉
::

---

## Troubleshooting Reference

| Problem | Cause | Solution |
|---|---|---|
| `type sudo` returns `sudo is aliased to ...` | Alias defined in `~/.bashrc` or a profile script | Run `unalias sudo` in the current session; remove the definition from its source file |
| `$PATH` contains `/home/user/.local/bin` in a root shell | `sudo -i` inherited the invoking user's environment | Verify `/etc/sudoers` has `env_reset` set; re-audit after a clean `sudo -i` |
| `declare -f useradd` produces output | A shell function shadows the real `useradd` binary | Unset with `unset -f useradd`; trace origin with `grep -r useradd /etc/profile.d/ ~/.bashrc` |
| `diff` shows critical variable dropped after `su -` | `su -` resets the environment to the target user's defaults | Expected; re-export required variables explicitly after escalation |
| `/usr/bin` missing from `$PATH` | `$PATH` was overwritten without including standard directories | Restore with `export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin` |
| `echo $USER` shows wrong identity after `sudo -i` | `sudo` preserved the invoking user's `$USER` variable | Use `id` to determine the effective identity; check `/etc/sudoers` for `env_keep` entries |

---

## What You Practised

- Confirming the active shell binary and version with `echo $SHELL`, `bash --version`, and `ps -p $$`
- Verifying effective identity with `whoami` and `id`
- Creating baseline snapshots of exported variables (`env`) and all shell variables (`set`)
- Parsing `$PATH` into a readable list and scanning for user-owned directories
- Detecting command overrides via `type`, `alias`, and `declare -f`
- Tracing variable origins through startup files with `grep -r`
- Diffing the environment before and after privilege escalation

These techniques map directly to RHCSA exam tasks that require you to manage users, files, and services as root — knowing your shell environment is clean is the first line of defence against hard-to-diagnose failures.
```