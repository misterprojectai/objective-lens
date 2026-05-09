---
description: >-
  Practice constructing well-formed shell commands using command names, short
  options, combined options, and long options with values.
icon: graduation-cap
---

# Tutorial 2: Issue Commands with Correct Syntax

In this tutorial, you will build the skill of constructing well-formed commands using the command-name, options, and arguments structure. Along the way, you will work with `ls`, `uname`, and `date` — three commands that together let you practice short options, combined short options, and long options with and without values.

{% hint style="info" %}
**Prerequisites**

* A working shell prompt on an RHEL system (covered in Tutorial 1: Your First Commands at the Shell Prompt)
* The ability to type commands and press Enter to run them
{% endhint %}

By the end of this tutorial, you will have issued a series of correctly formed commands and observed exactly how the shell responds to each part of the command structure. The terminal will be in this state after the final step:

```
Sat May  7 14:32:00 UTC 2026
```

That output is the result of `date` with a long option — proof that you can construct the full range of command syntax the shell expects.

***

{% stepper %}
{% step %}
#### Run a Command with No Options or Arguments

Run `uname` by itself to see what a bare command name produces.

```bash
uname
```

{% code title="Output" %}
```
Linux
```
{% endcode %}

This confirms the shell found the `uname` executable, ran it, and printed its output. The command name alone is a complete, valid command.
{% endstep %}

{% step %}
#### Add a Short Option

Add a single short option to `uname`. Short options are a single letter preceded by one hyphen.

```bash
uname -r
```

{% code title="Output" %}
```
5.14.0-284.11.1.el9_2.x86_64
```
{% endcode %}

The `-r` option changed what `uname` reported — the kernel release — without changing the command name itself. The space between the command name and the option separates them as distinct tokens.
{% endstep %}

{% step %}
#### Combine Short Options

Combine two short options into a single token. Most commands accept combined short options written together after a single hyphen.

```bash
uname -sr
```

{% code title="Output" %}
```
Linux 5.14.0-284.11.1.el9_2.x86_64
```
{% endcode %}

The `-sr` token produces both the system name and the kernel release in one go. The shell passes the combined token to `uname`, which unpacks `-s` and `-r` as two separate instructions.

{% hint style="warning" %}
Not every command supports combined short options — this behaviour depends on how the program parses its arguments. Most standard RHEL utilities follow this convention.
{% endhint %}
{% endstep %}

{% step %}
#### Use Multiple Short Options Written Separately

Issue the same combination as two distinct option tokens to confirm both forms are equivalent.

```bash
uname -s -r
```

{% code title="Output" %}
```
Linux 5.14.0-284.11.1.el9_2.x86_64
```
{% endcode %}

The output is identical to Step 3. The shell passes each hyphenated token to `uname` as a separate argument; the program treats them the same way regardless of whether they arrived combined or separate.
{% endstep %}

{% step %}
#### Use a Long Option

Use a long option in place of its short equivalent. Long options begin with two hyphens followed by a descriptive word.

```bash
uname --kernel-release
```

{% code title="Output" %}
```
5.14.0-284.11.1.el9_2.x86_64
```
{% endcode %}

`--kernel-release` produces the same result as `-r` from Step 2. Long options are wordier but self-documenting — the option name describes exactly what it requests.

{% hint style="warning" %}
Long options require **two** hyphens (`--`). Using a single hyphen (`-kernel-release`) will produce an error or unexpected behaviour.
{% endhint %}
{% endstep %}

{% step %}
#### Use a Long Option That Requires a Value

Use `date` with the `--date` option to supply a value using the `--option=value` form.

```bash
date --date="next Monday"
```

{% code title="Output" %}
```
Mon May 12 00:00:00 UTC 2026
```
{% endcode %}

The `=` sign connects the option name to its value directly, with no spaces around it.

{% hint style="warning" %}
The value `"next Monday"` must be enclosed in quotes because it contains a space. Without the quotes, the shell splits `next` and `Monday` into two separate arguments and `date` will not receive the value it expects.
{% endhint %}

<details>

<summary>If you see "invalid date" instead of a date, do this</summary>

Your shell may have interpreted the string differently. Try single quotes instead:

```bash
date --date='next Monday'
```

Single quotes prevent the shell from performing any expansion on the enclosed string.

</details>
{% endstep %}

{% step %}
#### Use a Command with Both an Option and an Argument

Issue a command that takes both an option and an argument. An argument names the target the command acts on — separate from the options that modify its behaviour.

```bash
ls -l /etc
```

{% code title="Output" %}
```
total 1084
drwxr-xr-x.  3 root root     97 Apr 22 10:01 alternatives
drwxr-xr-x.  4 root root     78 Apr 22 10:02 audit
...
```
{% endcode %}

`-l` is the option (it changes the output format) and `/etc` is the argument (it names the target). The command name, the option, and the argument are each separated by a single space.
{% endstep %}

{% step %}
#### Verify the Full Syntax Pattern with `date`

Verify the complete command-structure pattern by running `date` with a long option, producing a known, predictable output.

```bash
date --utc
```

{% code title="Output" %}
```
Sat May  7 14:32:00 UTC 2026
```
{% endcode %}

A long option, no argument — the command is complete and well-formed. This matches the final state shown at the top of this tutorial.
{% endstep %}
{% endstepper %}

***

{% hint style="success" %}
**You've completed this tutorial.** You have now:

1. Run a bare command name and observed its output
2. Added a single short option using the `-r` form
3. Combined two short options into a single token using `-sr`
4. Written the same two options separately and confirmed identical output
5. Substituted a long option (`--kernel-release`) for its short equivalent
6. Supplied a value to a long option using the `--option=value` form
7. Issued a command with both an option and an argument, identifying each part
8. Verified the complete syntax pattern with a final `date` command
{% endhint %}

***

## Next Steps

Now that you have built the skill of constructing well-formed commands, continue with:

* [How-to: Get Help for Any Command](tutorial_02.md) — use `--help` and `man` to discover options for unfamiliar commands
* [Explanation: Understanding the Linux Shell and Command Syntax](tutorial_02.md) — understand why the shell parses commands the way it does
* [Reference: Bash Command Syntax and Options](tutorial_02.md) — see the complete specification of command structure and option conventions

## Practice This Lab

{% embed url="https://labs.iximiuz.com/tutorials/rhcsa-x200101-tutorial-2-31234c1c" %}

