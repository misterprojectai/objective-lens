---
description: >-
  Read built-in environment variables, define your own shell variables, export
  them, and confirm that child processes inherit the values you set.
icon: graduation-cap
---

# Tutorial 4: Read and Set Shell Variables

{% hint style="info" %}
**Before you start:** You need a shell prompt on a RHEL system logged in as a regular user (not root), and comfort issuing basic commands at the prompt (Tutorial 3 or equivalent).
{% endhint %}

By the end of this tutorial, your terminal will be in this state:

```bash
[student@rhel ~]$ echo $MYGREETING
Hello RHCSA
[student@rhel ~]$ bash -c 'echo $MYGREETING'
Hello RHCSA
```

{% stepper %}
{% step %}
#### Read Three Built-in Environment Variables

Use `echo` to read the values of three variables the shell provides automatically.

```bash
echo $USER
```

{% hint style="success" %}
**Output**

```
student
```
{% endhint %}

```bash
echo $SHELL
```

{% hint style="success" %}
**Output**

```
/bin/bash
```
{% endhint %}

```bash
echo $PATH
```

{% hint style="success" %}
**Output**

```
/home/student/.local/bin:/home/student/bin:/usr/local/bin:/usr/bin:/bin
```
{% endhint %}

{% hint style="warning" %}
Every variable name must be prefixed with `$` — that is the signal to the shell to substitute the variable's value before the command runs.
{% endhint %}
{% endstep %}

{% step %}
#### List All Environment Variables with env

Use `env` to display every variable currently exported to the environment.

```bash
env
```

{% hint style="success" %}
**Output** (excerpt)

```
SHELL=/bin/bash
HOME=/home/student
USER=student
PATH=/home/student/.local/bin:/home/student/bin:/usr/local/bin:/usr/bin:/bin
LANG=en_US.UTF-8
```
{% endhint %}

`USER`, `SHELL`, and `PATH` — the variables you just read — appear in this list. Everything shown here is inherited by any command this shell launches.
{% endstep %}

{% step %}
#### Create a Shell Variable

Define your own variable with an assignment statement.

```bash
MYGREETING="Hello RHCSA"
```

No output is produced — the shell accepts the assignment silently. Confirm the value is set:

```bash
echo $MYGREETING
```

{% hint style="success" %}
**Output**

```
Hello RHCSA
```
{% endhint %}

{% hint style="warning" %}
Do not put spaces around the `=` sign. `MYGREETING = "Hello RHCSA"` will fail — the shell interprets it as a command named `MYGREETING` with arguments.
{% endhint %}

`MYGREETING` is now available to this shell, but it has not yet been exported. A child process cannot see it yet.
{% endstep %}

{% step %}
#### Confirm the Variable Is Not Yet Inherited

Check what a child shell sees before you export the variable.

```bash
bash -c 'echo $MYGREETING'
```

{% hint style="success" %}
**Output**

```
```

An empty line is the correct result here. The child shell has no knowledge of `MYGREETING` because it has not been exported yet.
{% endhint %}

{% hint style="warning" %}
Use **single quotes** around `'echo $MYGREETING'`. Double quotes would cause the parent shell to expand `$MYGREETING` before passing the string to `bash -c`, defeating the test.
{% endhint %}

<details>

<summary>If you see `Hello RHCSA` instead of an empty line</summary>

Your shell session may have a previous export of `MYGREETING` from an earlier run. Unset it and start this step again:

```bash
unset MYGREETING
MYGREETING="Hello RHCSA"
bash -c 'echo $MYGREETING'
```

You should now see an empty line.

</details>
{% endstep %}

{% step %}
#### Export the Variable

Mark `MYGREETING` for inclusion in the environment of every child process this shell launches.

```bash
export MYGREETING
```

No output is produced — the shell accepts the export silently. The variable is now part of the exported environment.
{% endstep %}

{% step %}
#### Verify Inheritance in a Child Process

Confirm that a child shell now inherits the exported variable.

```bash
bash -c 'echo $MYGREETING'
```

{% hint style="success" %}
**Output**

```
Hello RHCSA
```

The same value set in the parent shell is now visible inside the child shell — this is environment inheritance in action.
{% endhint %}
{% endstep %}

{% step %}
#### Confirm the Complete Final State

Verify the complete state matches what was set out to build.

```bash
echo $MYGREETING
```

{% hint style="success" %}
**Output**

```
Hello RHCSA
```
{% endhint %}

```bash
bash -c 'echo $MYGREETING'
```

{% hint style="success" %}
**Output**

```
Hello RHCSA
```
{% endhint %}

Both the parent shell and the child shell return the value you defined.
{% endstep %}
{% endstepper %}

{% hint style="success" %}
**You've completed the tutorial.** In this session you:

1. Read the values of built-in environment variables `$USER`, `$SHELL`, and `$PATH` using `echo`
2. Listed all exported environment variables using `env`
3. Defined a new shell variable `MYGREETING` with an assigned value
4. Confirmed that an unexported variable is invisible to child processes
5. Exported `MYGREETING` using `export`
6. Verified that a child process launched with `bash -c` inherits the exported variable
{% endhint %}

## Next Steps

* [How-to: Persist Environment Variables Across Sessions](tutorial_04.md) — make variables survive logout by writing them to `~/.bash_profile`
* [Explanation: Understanding the Linux Shell and Command Syntax](tutorial_04.md) — understand why exported variables propagate to child processes but not to parent processes
* [Reference: Bash Command Syntax and Options](tutorial_04.md) — see complete syntax for variable assignment, `export`, `env`, and `echo`

## Practice This Lab

{% embed url="https://labs.iximiuz.com/tutorials/rhcsa-x200101-tutorial-4-6ee7a152" %}

