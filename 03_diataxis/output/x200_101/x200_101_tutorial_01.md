---
title: "Open Your First Shell Session on RHEL"
type: tutorial
exam_objective: x200_101
tutorial_index: 1
version: "1.0"
status: draft
---

# Open Your First Shell Session on RHEL

In this tutorial, we will open an interactive Bash shell three different ways: through a GNOME terminal, through a virtual console, and through an SSH connection. Along the way, we will read the prompt to confirm who we are, where we are, and which shell is running.

---

## Prerequisites

Before starting, ensure you have:

- A running RHEL 9 system with a GNOME desktop session active and a user account with a known password
- Network access to the RHEL system and its IP address (needed for the SSH step)

---

## What We'll Build

By the end of this tutorial, we will have opened a Bash shell three different ways and confirmed the shell identity in each one. The final verification will look like this:

```
/bin/bash
```

That single line — the output of `echo $SHELL` — confirms that Bash is the active shell for our user account.

---

## Step 1: Open a Terminal from the GNOME Desktop

First, we open a terminal emulator window from the GNOME desktop.

Right-click on the empty desktop and select **Open Terminal**, or press the **Super** key, type `terminal`, and press **Enter** to launch the GNOME Terminal application.

When the window opens, you should see:

```
[student@rhel9 ~]$
```

The prompt will reflect your own username and hostname instead of `student` and `rhel9`, but the structure is identical. Notice the `$` at the end — this confirms we are operating as a regular (non-root) user.

---

## Step 2: Read the Prompt Components

Now that we have a prompt, we confirm each piece of it by printing our username and current directory.

```bash
echo $USER
```

You should see:

```
student
```

Now print the current directory:

```bash
pwd
```

You should see:

```
/home/student
```

Notice that the `~` character in the prompt is shorthand for `/home/student`. The prompt is telling us our location at all times.

---

## Step 3: Confirm Which Shell Is Active

Now that we can read the prompt, we confirm which shell is running this session.

```bash
echo $SHELL
```

You should see:

```
/bin/bash
```

This tells us the default shell assigned to our user account is Bash. Keep this terminal open — we will return to it after the next two steps.

---

## Step 4: Switch to a Virtual Console

Now we open a second shell session using a virtual console — a full-screen text terminal independent of the GNOME desktop.

Press **Ctrl-Alt-F2** on the keyboard.

The screen will switch away from the graphical desktop. You should see:

```
Red Hat Enterprise Linux 9.x (Plow)
Kernel 5.14.0-xxx.el9.x86_64 on an x86_64

rhel9 login:
```

Type your username and press **Enter**, then type your password when prompted. You should see:

```
[student@rhel9 ~]$
```

We now have an independent shell session running on `tty2`, with no graphical environment involved.

---

## Step 5: Confirm the Virtual Console Identity

Now that we are logged in on the virtual console, we confirm which terminal device this session is using.

```bash
tty
```

You should see:

```
/dev/tty2
```

This confirms we are on the second virtual console. Now log out of this session cleanly.

```bash
exit
```

You should see the login prompt return:

```
rhel9 login:
```

Press **Ctrl-Alt-F1** to return to the GNOME desktop and the terminal window we opened in Step 1.

---

## Step 6: Open a Shell Session Over SSH

Now that we have used the desktop terminal and a virtual console, we open a third session using SSH — the method used whenever the system has no graphical display or is accessed remotely.

In the GNOME terminal from Step 1, run the following command, replacing `192.168.1.100` with the actual IP address of your RHEL system:

```bash
ssh student@192.168.1.100
```

You should see:

```
The authenticity of host '192.168.1.100 (192.168.1.100)' can't be established.
ED25519 key fingerprint is SHA256:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.
Are you sure you want to continue connecting (yes/no/[fingerprint])?
```

Type `yes` and press **Enter**. Enter your password when prompted. You should see:

```
[student@rhel9 ~]$
```

We now have a shell session delivered over an encrypted SSH connection.

---

## Step 7: Confirm the SSH Session Identity

Now that we are in the SSH session, we confirm which terminal device this connection is using.

```bash
tty
```

You should see:

```
/dev/pts/0
```

The `pts` prefix (pseudo-terminal) distinguishes an SSH or terminal-emulator session from a hardware virtual console (`tty`). Now close the SSH session cleanly.

```bash
exit
```

You should see:

```
logout
Connection to 192.168.1.100 closed.
```

We are back at the GNOME terminal prompt.

---

## Step 8: Verify the Final System State

Finally, we confirm our shell identity one last time in the GNOME terminal, completing the contract we set out in **What We'll Build**.

```bash
echo $SHELL
```

You should see:

```
/bin/bash
```

---

## What We Accomplished

In this tutorial, we:

1. Opened an interactive Bash shell using the GNOME Terminal application
2. Read the prompt components to identify the current user and working directory
3. Confirmed the active shell using `echo $SHELL`
4. Switched to a virtual console with Ctrl-Alt-F2, logged in, and verified the session with `tty`
5. Returned to the desktop and opened a remote shell session using `ssh`
6. Confirmed the SSH session device type as a pseudo-terminal (`pts`)
7. Closed both the virtual console and SSH sessions cleanly using `exit`

---

## Next Steps

Now that you have opened shell sessions three different ways, you might want to:

- [How-to: Access a Shell Prompt on RHEL](#) — procedures for opening terminal sessions quickly in different scenarios
- [Explanation: Understanding the Linux Shell and Command Syntax](#) — understand why the prompt looks the way it does, what `$SHELL` means, and how Bash fits into the Linux architecture
- [Reference: Bash Command Syntax and Options](#) — complete specification of command structure and shell variables