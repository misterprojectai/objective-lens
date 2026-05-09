---
kind: tutorial

title: "Open Your First Shell Session on RHEL"

description: |
  Learn to open an interactive Bash shell three different ways on a RHEL 9 system:
  through a terminal emulator, through a virtual console, and over SSH.
  Along the way, read the shell prompt to confirm who you are, where you are,
  and which shell is running — core skills tested on the RHCSA EX200 exam.

categories:
  - linux

tagz:
  - rhcsa
  - bash
  - shell
  - ssh
  - tty

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

  verify_echo_user:
    machine: rocky-01
    user: laborant
    run: |
      grep -q 'echo $USER' /home/laborant/.bash_history && exit 0 || exit 1
    hintcheck: |
      echo "Run: echo \$USER"

  verify_pwd:
    machine: rocky-01
    user: laborant
    run: |
      grep -q 'pwd' /home/laborant/.bash_history && exit 0 || exit 1
    hintcheck: |
      echo "Run: pwd"

  verify_echo_shell:
    machine: rocky-01
    user: laborant
    run: |
      grep -q 'echo $SHELL' /home/laborant/.bash_history && exit 0 || exit 1
    hintcheck: |
      echo "Run: echo \$SHELL"

  verify_tty:
    machine: rocky-01
    user: laborant
    run: |
      grep -q 'tty' /home/laborant/.bash_history && exit 0 || exit 1
    hintcheck: |
      echo "Run: tty"

  verify_ssh_loopback:
    machine: rocky-01
    user: laborant
    run: |
      grep -q 'ssh laborant@localhost' /home/laborant/.bash_history && exit 0 || exit 1
    hintcheck: |
      echo "Run: ssh laborant@localhost"

  verify_ssh_tty:
    machine: rocky-01
    user: laborant
    run: |
      # Check that 'tty' was run at least twice (once locally, once in SSH session)
      count=$(grep -c '^tty$' /home/laborant/.bash_history 2>/dev/null || echo 0)
      [ "$count" -ge 2 ] && exit 0 || exit 1
    hintcheck: |
      echo "Inside your SSH session, run: tty"
      echo "You should see output like /dev/pts/1"

  verify_final_shell:
    machine: rocky-01
    user: laborant
    run: |
      # Confirm echo $SHELL was run at least twice (step 3 and final step)
      count=$(grep -c 'echo $SHELL' /home/laborant/.bash_history 2>/dev/null || echo 0)
      [ "$count" -ge 2 ] && exit 0 || exit 1
    hintcheck: |
      echo "Run: echo \$SHELL"
      echo "You should see: /bin/bash"

---

# Open Your First Shell Session on RHEL

In this tutorial, you will open an interactive Bash shell **three different ways**: through a terminal emulator, by inspecting virtual console devices, and through an SSH loopback connection. Along the way, you will read the prompt to confirm who you are, where you are, and which shell is running.

These are foundational skills for the RHCSA EX200 exam. Every other exam task assumes you can open a reliable shell session and orient yourself within it.

::remark-box
---
:kind: info
---
The source material for this tutorial covers GNOME Terminal and physical virtual console switching (Ctrl-Alt-F2). The iximiuz Labs playground is a **headless server** — no graphical desktop is present. The equivalent skills are demonstrated using a direct terminal session and an SSH loopback connection, which is exactly how you will work on a remote RHEL system in practice and on the exam.
::

---

## What You Will Build

By the end of this tutorial, you will have:

- Read a Bash prompt and understood every component of it
- Confirmed your active shell, username, and working directory from the command line
- Identified the terminal device your session is using with `tty`
- Opened a second shell session over SSH and confirmed it uses a pseudo-terminal (`pts`)
- Closed sessions cleanly with `exit`

The final verification will look like this:

```
/bin/bash
```

That single line — the output of `echo $SHELL` — confirms that Bash is the active shell for your user account.

---

## Step 1 — Read the Prompt

When you open your terminal on the playground, you already have a Bash shell session. Before running any commands, look at the prompt itself:

```
[laborant@rocky-01 ~]$
```

Every component carries meaning:

| Component | Meaning |
|---|---|
| `laborant` | The currently logged-in username |
| `rocky-01` | The hostname of this machine |
| `~` | The current directory — `~` is shorthand for your home directory |
| `$` | You are a regular (non-root) user — root would show `#` |

::remark-box
---
:kind: warning
---
On the RHCSA exam, the prompt will show the exam username and hostname. Always check the prompt before running any command — it is your primary orientation tool and will save you from running commands on the wrong machine.
::

---

## Step 2 — Confirm Your Username and Working Directory

Now confirm each piece of the prompt programmatically.

Print your current username:

```bash
echo $USER
```

You should see:

```
laborant
```

Print the full path of your current directory:

```bash
pwd
```

You should see:

```
/home/laborant
```

The `~` in the prompt is shorthand for `/home/laborant`. The prompt updates this dynamically as you change directories.

::simple-task
---
:tasks: tasks
:name: verify_echo_user
---
#active
Run `echo $USER` to print your current username.

#completed
✅ Done — you confirmed your username from the command line.
::

::simple-task
---
:tasks: tasks
:name: verify_pwd
---
#active
Run `pwd` to print your current working directory.

#completed
✅ Done — you confirmed your working directory.
::

---

## Step 3 — Confirm Which Shell Is Active

Now confirm which shell is running this session:

```bash
echo $SHELL
```

You should see:

```
/bin/bash
```

`$SHELL` holds the path of the **default login shell** assigned to your user account. This is stored in `/etc/passwd` and does not change between sessions unless an administrator modifies it.

::remark-box
---
:kind: info
---
`$SHELL` shows the default shell for your account. If you launch a different shell (e.g., `zsh` or `sh`) inside your session, `$SHELL` will still show `/bin/bash`. To see the shell of the current process, use `echo $0` or `readlink /proc/$$/exe`.
::

::simple-task
---
:tasks: tasks
:name: verify_echo_shell
---
#active
Run `echo $SHELL` to confirm which shell is your default.

#completed
✅ Done — your default shell is `/bin/bash`.
::

---

## Step 4 — Identify Your Terminal Device

Every shell session is attached to a terminal device. Run:

```bash
tty
```

You should see something like:

```
/dev/pts/0
```

This path identifies the **pseudo-terminal** (PTY) device your session is using. The `pts` prefix distinguishes a terminal-emulator or SSH session from a hardware virtual console.

::remark-box
---
:kind: info
---
**Virtual consoles vs. pseudo-terminals:**

On a physical RHEL system, pressing **Ctrl-Alt-F2** switches to a full-screen text console. That session uses a device like `/dev/tty2`. These are hardware (or kernel-emulated) consoles.

When you open a terminal emulator application, or connect via SSH, the kernel allocates a *pseudo-terminal pair* — a master side (used by the application) and a slave side (shown to the shell as `/dev/pts/N`). This is the device you will see in a playground or on any remote server.
::

::simple-task
---
:tasks: tasks
:name: verify_tty
---
#active
Run `tty` to see which terminal device your session is attached to.

#completed
✅ Done — you identified your terminal device.
::

---

## Step 5 — Open a Shell Session Over SSH

Now open a **second shell session** using SSH. On a real RHEL system this would target a remote IP address. Here, we use loopback (`localhost`) to demonstrate the same concept within the playground.

```bash
ssh laborant@localhost
```

You will see a host key prompt on your first connection:

```
The authenticity of host 'localhost (127.0.0.1)' can't be established.
ED25519 key fingerprint is SHA256:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.
Are you sure you want to continue connecting (yes/no/[fingerprint])?
```

Type `yes` and press **Enter**.

When prompted for a password, enter the `laborant` user password: `laborant`

You should arrive at a new prompt:

```
[laborant@rocky-01 ~]$
```

The prompt looks identical — but this is a **new, independent shell session** delivered over an encrypted SSH connection.

::hint-box
---
:summary: SSH asks for a password and I don't know it
---
The default password for the `laborant` user on iximiuz Labs playgrounds is `laborant`. If that fails, try running `passwd` in your current session to set a new password before SSHing.
::

::hint-box
---
:summary: SSH says "Connection refused"
---
The SSH daemon may not be running. Check with: `systemctl status sshd`

If it is inactive, start it: `sudo systemctl start sshd`
::

::simple-task
---
:tasks: tasks
:name: verify_ssh_loopback
---
#active
Run `ssh laborant@localhost` to open a new shell session over SSH.

#completed
✅ Done — you opened a shell session over SSH.
::

---

## Step 6 — Confirm the SSH Session Identity

Now that you are inside the SSH session, run `tty` again:

```bash
tty
```

You should see something like:

```
/dev/pts/1
```

Notice the difference from Step 4:

| Session type | Example device |
|---|---|
| Physical virtual console | `/dev/tty2` |
| Terminal emulator / SSH | `/dev/pts/0`, `/dev/pts/1`, … |

The number after `pts/` increments with each new pseudo-terminal allocated. Your SSH session received a fresh PTY, separate from the one your outer terminal is using.

::remark-box
---
:kind: info
---
On the RHCSA exam, when a task says "log in via SSH," the examiner expects you to reach a working shell prompt. Knowing that the result is a `pts` device — not a `tty` device — helps you diagnose problems: if `tty` returns `not a tty`, your session has no terminal attached, which breaks interactive commands.
::

::simple-task
---
:tasks: tasks
:name: verify_ssh_tty
---
#active
Inside your SSH session, run `tty` to see the pseudo-terminal device for this connection.

#completed
✅ Done — you confirmed the SSH session is using a separate pseudo-terminal.
::

---

## Step 7 — Close the SSH Session and Verify Final Shell

Close the SSH session cleanly:

```bash
exit
```

You should see:

```
logout
Connection to localhost closed.
```

You are now back at your original terminal prompt. Confirm your shell one final time:

```bash
echo $SHELL
```

You should see:

```
/bin/bash
```

::simple-task
---
:tasks: tasks
:name: verify_final_shell
---
#active
Back in your original session, run `echo $SHELL` to confirm you are in Bash.

#completed
✅ Done — you confirmed the active shell after returning from SSH.
::

---

## What You Accomplished

In this tutorial, you:

1. **Read the Bash prompt** and identified its four components: username, hostname, current directory, and privilege indicator
2. **Confirmed your username** with `echo $USER` and your working directory with `pwd`
3. **Confirmed your default shell** with `echo $SHELL` — the result was `/bin/bash`
4. **Identified your terminal device** with `tty` — a `pts` device for terminal-emulator and SSH sessions
5. **Opened a second shell session over SSH** using `ssh laborant@localhost`, accepted the host key, and authenticated
6. **Confirmed the SSH session device** — a new `pts` number, independent of the first session
7. **Closed sessions cleanly** with `exit` and confirmed the logout message

---

## Key Commands Reference

| Command | What it shows |
|---|---|
| `echo $USER` | Current logged-in username |
| `echo $SHELL` | Default shell for this user account |
| `pwd` | Full path of current working directory |
| `tty` | Terminal device this session is attached to |
| `ssh user@host` | Open a new shell session over SSH |
| `exit` | Close the current session cleanly |

---

## Next Steps

Now that you can open and orient yourself in a Bash shell three different ways, continue with:

- **Accessing a Shell Prompt on RHEL** — quick procedures for opening terminal sessions in different scenarios, including sudo escalation
- **Understanding the Linux Shell and Command Syntax** — why the prompt looks the way it does, what `$SHELL` means, and how Bash fits into the Linux architecture
- **Bash Command Syntax and Options** — complete specification of command structure, shell variables, and quoting rules