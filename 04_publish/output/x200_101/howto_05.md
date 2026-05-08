---
description: Inspect and document the active shell, user identity, environment variables, and $PATH state before executing privileged or deployment commands, and detect unexpected variable overrides.
icon: wrench
---

# How to Audit the Shell Environment Before Running Administrative Tasks

{% hint style="info" %}
**Prerequisites:**
- A Bash shell prompt on an RHEL system — either a regular user session or an escalated session via `sudo -i` or `su -`
- Read access to `/etc/environment`, `/etc/profile.d/`, and `~/.bashrc` if you need to trace variable origins
{% endhint %}

{% stepper %}
{% step %}
### Confirm the active shell and shell version

Verify which shell binary is running and its version before trusting any shell-specific behaviour.

```bash
echo $SHELL
bash --version
```

Cross-check that the running process is actually Bash, not a shell substituted by a script or `su` invocation:

```bash
ps -p $$
```

{% hint style="warning" %}
`echo $SHELL` reports the login shell, not necessarily the currently executing shell. If a script invoked a different shell, `ps -p $$` will reveal the discrepancy.
{% endhint %}
{% endstep %}

{% step %}
### Confirm the effective user identity

Verify who the shell believes you are — both the login identity and the effective user.

```bash
whoami
id
```

If you have escalated with `sudo -i` or `su -`, confirm the target identity carried over:

```bash
echo $USER
echo $LOGNAME
echo $HOME
```

{% hint style="warning" %}
`whoami` reports the effective UID only. `id` reports UID, GID, and all supplementary groups — use `id` when group membership matters for the task. After `sudo -i`, `$USER` may still reflect the invoking user even though the effective UID is root.
{% endhint %}
{% endstep %}

{% step %}
### Capture all exported environment variables

Dump the full exported environment to a baseline snapshot before making changes.

```bash
env | sort
```

To save the snapshot for comparison after the task:

```bash
env | sort > /tmp/env-before.txt
```

{% hint style="warning" %}
`env` shows only **exported** variables. Shell-local variables and functions are not captured here — proceed to the next step to capture those.
{% endhint %}
{% endstep %}

{% step %}
### Capture all shell variables, including unexported ones

`env` shows only exported variables. Use `set` to include shell-local variables and functions that may shadow or interfere with commands.

```bash
set | sort
```

To save for later comparison:

```bash
set | sort > /tmp/set-before.txt
```

{% hint style="warning" %}
`set` output includes shell function definitions. A function with the same name as a system command will silently intercept that command. Review function definitions carefully in the output.
{% endhint %}
{% endstep %}

{% step %}
### Inspect and validate $PATH

Display the current `$PATH` as a readable list to check for unexpected directories.

```bash
echo $PATH | tr ':' '\n'
```

On an escalated session, confirm the path is appropriate for the privilege level. A root shell must not inherit a user's local `~/bin` path for privileged commands:

```bash
echo $PATH | tr ':' '\n' | grep -E '^/home|\.local'
```

{% hint style="warning" %}
If the grep command above returns **any output**, a user-owned directory is present in a privileged shell's `$PATH`. Do not proceed with administrative commands until this is resolved — a malicious or misconfigured binary in a user directory could be executed instead of the intended system binary.
{% endhint %}

<details>
<summary>Why a user-owned directory appears in a root $PATH</summary>

This typically occurs when `sudo -i` is called without `env_reset` enforced in `/etc/sudoers`, or when `sudo su` is used instead of `sudo -i`. The `sudo su` invocation spawns a root shell that inherits the invoking user's exported environment, including `$PATH`. Using `sudo -i` directly and verifying `/etc/sudoers` contains `Defaults env_reset` prevents this.

</details>
{% endstep %}

{% step %}
### Detect variable overrides that shadow standard commands

Check whether any environment variables or shell definitions are overriding commands or altering critical behaviour.

**Check for a `$PATH` missing standard system directories:**

```bash
echo $PATH | tr ':' '\n' | grep -c '^/usr/bin$'
```

Expected result: `1`. A result of `0` means `/usr/bin` is absent from `$PATH`.

**Check for aliases hiding commands you are about to run:**

```bash
type sudo
type useradd
type passwd
```

If any returns `is aliased to`, list all active aliases:

```bash
alias
```

**Check for shell functions that shadow commands:**

```bash
declare -f sudo
declare -f useradd
```

{% hint style="warning" %}
Any output from `declare -f <command>` means a shell function is intercepting that command name. The real binary will not execute until the function is removed with `unset -f <function-name>`. This is a common vector for privilege escalation or accidental misconfiguration.
{% endhint %}
{% endstep %}

{% step %}
### Trace the origin of a suspicious variable

If a variable holds an unexpected value, identify which startup file set it.

```bash
grep -r 'VARIABLE_NAME' /etc/profile /etc/profile.d/ ~/.bash_profile ~/.bashrc ~/.bash_login
```

Replace `VARIABLE_NAME` with the actual variable name. The file containing the assignment is the source.

{% hint style="warning" %}
Search for the variable name without the `$` prefix — you are looking for the assignment (`VARIABLE_NAME=`), not a reference to it. A reference search will produce false positives.
{% endhint %}

<details>
<summary>Startup file load order for reference</summary>

For a login shell (`sudo -i`, `su -`), Bash reads files in this order:
1. `/etc/profile`
2. `/etc/profile.d/*.sh` (sourced by `/etc/profile`)
3. `~/.bash_profile` (or `~/.bash_login`, then `~/.profile` if not found)

For a non-login interactive shell, Bash reads only `~/.bashrc`. An unexpected variable in an interactive non-login shell is most likely sourced from `~/.bashrc` or a file it sources.

</details>
{% endstep %}

{% step %}
### Compare the environment after escalation

After running `sudo -i` or `su -`, compare the current environment against the pre-escalation snapshot captured in Step 3.

```bash
env | sort > /tmp/env-after.txt
diff /tmp/env-before.txt /tmp/env-after.txt
```

Lines beginning with `>` are variables present **only in the escalated session**. Lines beginning with `<` were **dropped during escalation**.

{% hint style="warning" %}
`su -` resets the environment to the target user's defaults by design. Variables dropped during `su -` escalation are expected behaviour — do not re-export them without first confirming they are required and safe. Re-exporting unknown variables into a privileged session is a security risk.
{% endhint %}
{% endstep %}
{% endstepper %}

## Verification

{% hint style="success" %}
Run the following composite command to confirm the audit is complete and the environment is clean for privileged work:

```bash
id && echo $SHELL && echo $PATH | tr ':' '\n' | head -6 && alias | grep -E 'sudo|useradd|passwd' || echo "no critical aliases found"
```

**Expected result:**
- Effective UID matches the intended account
- Shell is `/bin/bash`
- `$PATH` shows only system directories for root sessions (no `/home/...` or `.local` paths)
- No critical command aliases are present (output ends with `no critical aliases found`)
{% endhint %}

## Troubleshooting

{% hint style="warning" %}
**`type sudo` returns `sudo is aliased to ...`**
- **Cause:** An alias was defined in `~/.bashrc` or a profile script
- **Fix:** Run `unalias sudo` in the current session; locate and remove the definition from its source file

---

**`$PATH` contains `/home/user/.local/bin` in a root shell**
- **Cause:** `sudo -i` inherited the invoking user's environment due to missing `env_reset`
- **Fix:** Verify `/etc/sudoers` contains `Defaults env_reset`; use `sudo -i` (not `sudo su`); re-audit after a clean `sudo -i` session

---

**`declare -f useradd` produces output**
- **Cause:** A shell function shadows the real `useradd` binary
- **Fix:** Unset the function with `unset -f useradd`; trace its origin with `grep -r useradd /etc/profile.d/ ~/.bashrc`

---

**`diff` shows a critical variable was dropped after `su -`**
- **Cause:** `su -` resets the environment to the target user's defaults — this is expected behaviour
- **Fix:** Re-export required variables explicitly after escalation, only after confirming they are safe to carry into the privileged session

---

**`/usr/bin` missing from `$PATH`**
- **Cause:** `$PATH` was overwritten without including standard directories
- **Fix:** Restore with:
  ```bash
  export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
  ```

---

**`echo $USER` shows wrong identity after `sudo -i`**
- **Cause:** `sudo` preserved the invoking user's `$USER` variable via an `env_keep` entry in `/etc/sudoers`
- **Fix:** Use `id` rather than `$USER` to determine effective identity; audit `/etc/sudoers` for `env_keep` entries and remove `USER` if present
{% endhint %}