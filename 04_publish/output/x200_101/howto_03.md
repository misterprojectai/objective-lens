---
description: >-
  Inspect the current $PATH, add a directory for the current session, and
  persist the change so it survives a new login shell.
icon: wrench
---

# How-to 3: Identify and Modify PATH for Command Availability

{% hint style="info" %}
**Prerequisites**

* An interactive Bash shell as a regular user (not root)
* A target directory to add — either an existing one such as `/opt/myapp/bin` or a custom directory you have already created
{% endhint %}

{% stepper %}
{% step %}
#### Inspect the Current $PATH

Display the current search path:

```bash
echo $PATH
```

To read each directory on its own line:

```bash
echo $PATH | tr ':' '\n'
```

{% hint style="warning" %}
Note the order — the shell searches directories **left to right** and stops at the first match. Position matters when multiple directories contain a command with the same name.
{% endhint %}
{% endstep %}

{% step %}
#### Check Whether Your Directory Is Already in $PATH

Search for the target directory before making any change:

```bash
echo $PATH | tr ':' '\n' | grep '/opt/myapp/bin'
```

If the command returns no output, the directory is not in `$PATH` and must be added.
{% endstep %}

{% step %}
#### Add the Directory for the Current Session

{% tabs %}
{% tab title="Prepend (higher priority)" %}
If you want the directory searched **first** — taking priority over existing commands with the same name:

```bash
export PATH=/opt/myapp/bin:$PATH
```
{% endtab %}

{% tab title="Append (lower priority)" %}
If you want the directory searched **last** — existing commands take priority:

```bash
export PATH=$PATH:/opt/myapp/bin
```
{% endtab %}
{% endtabs %}

{% hint style="warning" %}
This change applies to the current shell session and any child processes only. It is lost when the session ends.
{% endhint %}

{% hint style="danger" %}
Never write `export PATH=/opt/myapp/bin` without including `$PATH`. This discards the entire existing search path, breaking access to standard system commands.
{% endhint %}
{% endstep %}

{% step %}
#### Persist the Change in \~/.bash\_profile

Append the export line to `~/.bash_profile`:

```bash
echo 'export PATH=/opt/myapp/bin:$PATH' >> ~/.bash_profile
```

{% hint style="warning" %}
Use **single quotes** so that `$PATH` is written literally into the file. The shell expands it at login time — not when this command runs. Double quotes would expand `$PATH` immediately, baking the current value into the file rather than inheriting the full path at each login.
{% endhint %}

<details>

<summary>Non-login interactive shells — also update ~/.bashrc</summary>

Many terminal emulators (GNOME Terminal, VS Code terminal, tmux) open non-login interactive shells that source `~/.bashrc` instead of `~/.bash_profile`. To cover both cases, add the same export line to `~/.bashrc`:

```bash
echo 'export PATH=/opt/myapp/bin:$PATH' >> ~/.bashrc
```

Or source `~/.bash_profile` from within `~/.bashrc`:

```bash
echo '[ -f ~/.bash_profile ] && source ~/.bash_profile' >> ~/.bashrc
```

</details>
{% endstep %}

{% step %}
#### Verify the Change Survives a New Login Shell

Force Bash to re-read the login profile without logging out:

```bash
bash --login -c 'echo $PATH | tr ":" "\n"'
```

Confirm `/opt/myapp/bin` appears in the output, then open a full new login shell to test the real-world case:

```bash
exec bash --login
echo $PATH | tr ':' '\n'
```
{% endstep %}
{% endstepper %}

## Verification

{% hint style="success" %}
**Confirm the directory is present and in the expected position:**

```bash
echo $PATH | tr ':' '\n' | grep -n '/opt/myapp/bin'
```

Expected: a low line number means early in the search order (prepended); a high number means late (appended).

**Confirm a command in the added directory is now found:**

```bash
type mycommand
```

Expected output:

```
mycommand is /opt/myapp/bin/mycommand
```
{% endhint %}

## Troubleshooting

{% hint style="warning" %}
**Command still not found after adding the directory** Symptom: running the command still returns `command not found` Cause: directory path not saved correctly, or typo in path Fix: run `echo $PATH | tr ':' '\n'` and confirm the exact path appears

***

**Change lost after opening a new terminal** Symptom: `$PATH` reverts to the original value in new terminals Cause: export added to `~/.bashrc` instead of `~/.bash_profile`, or the terminal opens a non-login shell Fix: verify the export line is in `~/.bash_profile`; for non-login interactive shells, also add it to `~/.bashrc`

***

**New login shell does not pick up the change** Symptom: `exec bash --login` does not include the new directory Cause: `~/.bash_profile` was not saved, or the file contains a syntax error that aborted loading Fix: run `bash --login -c 'echo loaded'` — if it fails silently, check for syntax errors with:

````bash
bash -n ~/.bash_profile
---

**Prepended directory is still searched after /usr/bin**
Symptom: the existing system command runs instead of the one in `/opt/myapp/bin`
Cause: `$PATH` was not included in the export — the old value was discarded
Fix: ensure the export contains `$PATH`:

```bash
export PATH=/opt/myapp/bin:$PATH
````

Not: `export PATH=/opt/myapp/bin`

***

**Permission denied running a command in the added directory** Symptom: shell finds the command but returns `Permission denied` Cause: the binary is not executable Fix:

```bash
chmod +x /opt/myapp/bin/mycommand
```
{% endhint %}
