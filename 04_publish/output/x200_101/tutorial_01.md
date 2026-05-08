---
description: >-
  Open an interactive Bash shell on RHEL three ways — GNOME terminal, virtual
  console, and SSH — and confirm your shell identity at each checkpoint.
icon: graduation-cap
---

# Tutorial 1: Open Your First Shell Session on RHEL

In this tutorial, you will open an interactive Bash shell three different ways: through a GNOME terminal, through a virtual console, and through an SSH connection. Along the way, you will read the prompt to confirm who you are, where you are, and which shell is running.

{% hint style="info" %}
**Before you begin, you need:**

* A running RHEL 9 system with an active GNOME desktop session and a user account with a known password
* The IP address of your RHEL system and network access to it (required for the SSH step)
{% endhint %}

By the end of this tutorial, you will have confirmed Bash as your active shell in all three session types. The final verification produces this single line:

```
/bin/bash
```

{% stepper %}
{% step %}
#### Open a Terminal from the GNOME Desktop

Right-click on the empty desktop and select **Open Terminal**, or press the **Super** key, type `terminal`, and press **Enter** to launch GNOME Terminal.

When the window opens, you should see a prompt in this form:

```
[student@rhel9 ~]$
```

Your own username and hostname will appear in place of `student` and `rhel9`, but the structure is identical. The `$` at the end confirms you are operating as a regular (non-root) user.
{% endstep %}

{% step %}
#### Read the Prompt Components

Print your current username to confirm the first component of the prompt:

```bash
echo $USER
```

{% code title="Output" %}
```
student
```
{% endcode %}

Now print the current working directory:

```bash
pwd
```

{% code title="Output" %}
```
/home/student
```
{% endcode %}

The `~` character in your prompt is shorthand for `/home/student`. The prompt reports your location at all times.
{% endstep %}

{% step %}
#### Confirm Which Shell Is Active

Print the shell assigned to your user account:

```bash
echo $SHELL
```

{% code title="Output" %}
```
/bin/bash
```
{% endcode %}

{% hint style="info" %}
This confirms that Bash is the default shell for your account. Keep this terminal open — you will return to it after the next two steps.
{% endhint %}
{% endstep %}

{% step %}
#### Switch to a Virtual Console

Press **Ctrl-Alt-F2** on your keyboard. The screen will switch away from the graphical desktop and display a full-screen login prompt:

```
Red Hat Enterprise Linux 9.x (Plow)
Kernel 5.14.0-xxx.el9.x86_64 on an x86_64

rhel9 login:
```

Type your username and press **Enter**, then enter your password when prompted. You should see:

```
[student@rhel9 ~]$
```

You now have an independent shell session running on `tty2`, with no graphical environment involved.

{% hint style="warning" %}
If the screen goes blank instead of showing the login prompt, your system may be configured to start virtual consoles on a different function key. Try **Ctrl-Alt-F3** or **Ctrl-Alt-F6**.
{% endhint %}
{% endstep %}

{% step %}
#### Confirm the Virtual Console Identity

Print the terminal device this session is using:

```bash
tty
```

{% code title="Output" %}
```
/dev/tty2
```
{% endcode %}

This confirms you are on the second virtual console. Now log out of this session cleanly:

```bash
exit
```

{% code title="Output" %}
```
rhel9 login:
```
{% endcode %}

Press **Ctrl-Alt-F1** to return to the GNOME desktop and the terminal window you opened in Step 1.
{% endstep %}

{% step %}
#### Open a Shell Session Over SSH

In the GNOME terminal from Step 1, connect to your RHEL system over SSH. Replace `192.168.1.100` with the actual IP address of your system:

```bash
ssh student@192.168.1.100
```

On first connection, SSH will present a host-key fingerprint prompt:

```
The authenticity of host '192.168.1.100 (192.168.1.100)' can't be established.
ED25519 key fingerprint is SHA256:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.
Are you sure you want to continue connecting (yes/no/[fingerprint])?
```

Type `yes` and press **Enter**, then enter your password when prompted. You should see:

```
[student@rhel9 ~]$
```

You now have a shell session delivered over an encrypted SSH connection.

{% hint style="warning" %}
You must type `yes` in full — `y` alone will not be accepted and the connection will abort.
{% endhint %}

<details>

<summary>If you see "Connection refused" instead of the fingerprint prompt</summary>

The SSH daemon may not be running on your RHEL system. On the system console or GNOME terminal, run:

```bash
sudo systemctl enable --now sshd
```

Then retry the `ssh` command.

</details>
{% endstep %}

{% step %}
#### Confirm the SSH Session Identity

Print the terminal device this SSH connection is using:

```bash
tty
```

{% code title="Output" %}
```
/dev/pts/0
```
{% endcode %}

The `pts` prefix (pseudo-terminal) distinguishes an SSH or terminal-emulator session from a hardware virtual console (`tty`). Now close the SSH session cleanly:

```bash
exit
```

{% code title="Output" %}
```
logout
Connection to 192.168.1.100 closed.
```
{% endcode %}

You are back at the GNOME terminal prompt.
{% endstep %}

{% step %}
#### Verify the Final System State

Run the shell confirmation one last time in the GNOME terminal, completing the contract set out at the beginning of this tutorial:

```bash
echo $SHELL
```

{% code title="Output" %}
```
/bin/bash
```
{% endcode %}
{% endstep %}
{% endstepper %}

***

{% hint style="success" %}
**You've completed the tutorial.** You have:

1. Opened an interactive Bash shell using the GNOME Terminal application
2. Read the prompt components to identify the current user and working directory
3. Confirmed the active shell using `echo $SHELL`
4. Switched to a virtual console with Ctrl-Alt-F2, logged in, and verified the session with `tty`
5. Returned to the desktop and opened a remote shell session using `ssh`
6. Confirmed the SSH session device type as a pseudo-terminal (`pts`)
7. Closed both the virtual console and SSH sessions cleanly using `exit`
{% endhint %}

***

## Next Steps

* [How-to: Access a Shell Prompt on RHEL](tutorial_01.md) — procedures for opening terminal sessions quickly in different scenarios
* [Explanation: Understanding the Linux Shell and Command Syntax](tutorial_01.md) — understand why the prompt looks the way it does, what `$SHELL` means, and how Bash fits into the Linux architecture
* [Reference: Bash Command Syntax and Options](tutorial_01.md) — complete specification of command structure and shell variables
