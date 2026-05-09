---
description: >-
  Trace exactly how Bash resolves a command name by reading $PATH, classifying
  builtins, aliases, and external executables with type and which.
icon: graduation-cap
---

# Tutorial 3: Trace How the Shell Finds Commands

In this tutorial, we will trace exactly how Bash resolves a command name into something it can execute. Along the way, we will read and interpret `$PATH`, use `type` and `which` to locate commands, and distinguish shell builtins from external executables.

{% hint style="info" %}
**Prerequisites**

* A working Bash shell prompt on an RHEL system (covered in Tutorial 1)
* Ability to type commands and read their output (covered in Tutorial 2)
{% endhint %}

By the end of this tutorial, we will have traced the full resolution path for four commands — one builtin, one external, one alias, and one that does not exist.

{% stepper %}
{% step %}
#### Display the Current $PATH

Display the `$PATH` variable to see where the shell looks for commands.

```bash
echo $PATH
```

{% code title="Output" %}
```
/home/student/.local/bin:/home/student/bin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin
```
{% endcode %}

Each directory is separated by a colon. When you type a command name, the shell searches these directories from left to right, stopping as soon as it finds a match.
{% endstep %}

{% step %}
#### Read $PATH as a List

Make the raw value readable by replacing each colon with a newline.

```bash
echo $PATH | tr ':' '\n'
```

{% code title="Output" %}
```
/home/student/.local/bin
/home/student/bin
/usr/local/bin
/usr/bin
/usr/local/sbin
/usr/sbin
```
{% endcode %}

Notice that `/usr/bin` appears early in the list — this is where most standard commands such as `cat`, `ls`, and `grep` live on RHEL.
{% endstep %}

{% step %}
#### Identify a Shell Builtin

Check whether `cd` is found in `$PATH`.

```bash
type cd
```

{% code title="Output" %}
```
cd is a shell builtin
```
{% endcode %}

The shell did not search `$PATH` at all — `cd` is implemented inside Bash itself. The shell reports this immediately, before any directory lookup occurs.
{% endstep %}

{% step %}
#### Identify an External Executable

Check a command that does live on the filesystem.

```bash
type cat
```

{% code title="Output" %}
```
cat is /usr/bin/cat
```
{% endcode %}

The shell reports the full path to the executable. This tells us exactly which file ran when we typed `cat` — the shell found it in `/usr/bin`, the fourth directory in our `$PATH` list.
{% endstep %}

{% step %}
#### Identify an Alias

Check `ls`, which behaves differently from a plain executable on RHEL.

```bash
type ls
```

{% code title="Output" %}
```
ls is aliased to `ls --color=auto'
```
{% endcode %}

The shell resolved `ls` to an alias before checking `$PATH`. When we type `ls`, Bash expands it to `ls --color=auto` first, then locates the `ls` executable. This is why directory names appear in colour by default.
{% endstep %}

{% step %}
#### Confirm a Command's Location with which

Use `which` to confirm the filesystem location of `cat` independently from `type`.

```bash
which cat
```

{% code title="Output" %}
```
/usr/bin/cat
```
{% endcode %}

{% hint style="warning" %}
`which` searches only `$PATH` directories and reports only the file path — it does not tell you whether a command is a builtin or an alias. Use `type` for full resolution; use `which` when you need the filesystem path only.
{% endhint %}
{% endstep %}

{% step %}
#### Observe a Command That Cannot Be Found

Ask the shell to resolve a name that does not exist anywhere in its resolution sequence.

```bash
type foobar
```

{% code title="Output" %}
```
bash: type: foobar: not found
```
{% endcode %}

The shell reports `not found` rather than a file path. The shell checked builtins, aliases, and every directory in `$PATH` in order — and found nothing. This is the same error mechanism behind `command not found` messages.
{% endstep %}

{% step %}
#### Verify the Complete State

Run all checks together to confirm the final state matches what we set out to achieve.

```bash
type cd
type ls
type cat
type foobar
echo $PATH
which cat
```

{% code title="Output" %}
```
cd is a shell builtin
ls is aliased to `ls --color=auto'
cat is /usr/bin/cat
bash: type: foobar: not found
/home/student/.local/bin:/home/student/bin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin
/usr/bin/cat
```
{% endcode %}
{% endstep %}
{% endstepper %}

{% hint style="success" %}
**What you accomplished**

* Displayed and read `$PATH` to see the ordered list of directories the shell searches
* Used `type` to classify `cd` as a shell builtin, `ls` as an alias, and `cat` as an external executable
* Used `which` to confirm the filesystem location of an external command
* Observed the shell's `not found` response when no match exists at any stage of resolution
{% endhint %}

## Next Steps

<table data-view="cards"><thead><tr><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>How-to: Modify $PATH</strong></td><td>Add a custom command directory to make your own tools available as simple commands.</td><td><a href="tutorial_03.md">tutorial_03.md</a></td></tr><tr><td><strong>Explanation: Shell and Command Syntax</strong></td><td>Understand why builtins must live inside the shell and cannot be external programs.</td><td><a href="tutorial_03.md">tutorial_03.md</a></td></tr><tr><td><strong>Reference: Bash Command Syntax and Options</strong></td><td>See the complete resolution order and all <code>type</code> output formats.</td><td><a href="tutorial_03.md">tutorial_03.md</a></td></tr></tbody></table>

## Practice This Lab

{% embed url="https://labs.iximiuz.com/tutorials/rhcsa-x200101-tutorial-3-37774fed" %}

