---
description: >-
  Locate usage information and option syntax for any command using the built-in
  help tools available at every RHEL shell prompt.
icon: wrench
---

# How-to 1: Get Help for Any Command at the Shell Prompt

{% hint style="info" %}
**Prerequisites**

* An active Bash shell prompt on an RHEL system
* The name of the command you want to investigate, or a topic keyword to search
{% endhint %}

{% stepper %}
{% step %}
#### Display a Command's Built-in Usage Summary

Run the command with `--help` to display a compact usage summary and available options.

```bash
ls --help
```

{% hint style="warning" %}
A small number of commands use `-h` instead of `--help`. If `--help` produces an error or exits immediately, try `-h`.
{% endhint %}
{% endstep %}

{% step %}
#### Open the Full Manual Page for a Command

Open the `man` page for complete documentation, including all options, argument syntax, and examples.

```bash
man ls
```

Navigate the manual page with these keys:

| Key            | Action                       |
| -------------- | ---------------------------- |
| `Space` or `f` | Scroll forward one page      |
| `b`            | Scroll back one page         |
| `/pattern`     | Search forward for text      |
| `n`            | Jump to next search match    |
| `q`            | Quit and return to the shell |
{% endstep %}

{% step %}
#### Read the Synopsis Section of a Man Page

Locate the **SYNOPSIS** section immediately below the **NAME** section. Interpret it using these conventions:

* **Bold** text — type exactly as shown
* _Underlined_ or _italic_ text — replace with your own value
* `[item]` — optional; omit if not needed
* `item...` — repeatable; provide one or more

For example, the synopsis for `ls`:

```
ls [OPTION]... [FILE]...
```

This means `ls` accepts zero or more options and zero or more file arguments, all optional.
{% endstep %}

{% step %}
#### Get a One-Line Description of a Command with whatis

Look up a brief description of any command without opening a full man page.

```bash
whatis ls
```

Expected output:

```
ls (1)               - list directory contents
```

Use `whatis` when you know a command name but want to confirm what it does before investigating further.

{% hint style="warning" %}
If `whatis` returns `nothing appropriate`, the man page database may be out of date. Run `sudo mandb` to rebuild it, then retry.
{% endhint %}
{% endstep %}

{% step %}
#### Determine the Type and Location of a Command

Confirm how the shell resolves a command — builtin, alias, or external executable — before reading its help.

```bash
type ls
type cd
type cat
```

* If `cd` reports as a shell builtin, use `help cd` for its documentation instead of `man cd`.
* If `ls` is aliased, `type` shows the alias expansion before you read its options.

For an external command, confirm the full path on disk:

```bash
which cat
```

{% hint style="warning" %}
Shell builtins such as `cd`, `echo`, and `pwd` have no standalone man page in some configurations. Always run `type <command>` first to determine the correct help source.
{% endhint %}
{% endstep %}

{% step %}
#### Search Man Pages by Topic with apropos

When you know what you want to do but not which command to use, search all man page descriptions by keyword.

```bash
apropos "list directory"
```

If `apropos` returns `nothing appropriate`, rebuild the man page database:

```bash
sudo mandb
```

<details>

<summary>Broadening an apropos search that returns no results</summary>

If rebuilding the database still returns nothing, the keyword may be too specific. Try shorter or more general terms:

```bash
apropos list
apropos directory
apropos copy
```

Combine results by running multiple searches and reviewing the section numbers in parentheses — `(1)` is user commands, `(5)` is file formats, `(8)` is admin commands.

</details>
{% endstep %}

{% step %}
#### Read Info Documentation for GNU Commands

For GNU tools such as `ls`, `grep`, and `tar`, read extended documentation with `info`.

```bash
info ls
```

Navigate with these keys: `n` (next node), `p` (previous node), `u` (up one level), `q` (quit).

{% hint style="info" %}
If a topic has no dedicated info page, `info` falls back to the man page automatically.
{% endhint %}
{% endstep %}
{% endstepper %}

## Verification

{% hint style="success" %}
**Confirm all help tools are functional** by running each command below and verifying it returns output without error:

```bash
ls --help | head -5
man -f ls
type ls
whatis ls
```

A `man -f` result identical to `whatis` output confirms the man page database is current and indexed.
{% endhint %}

## Troubleshooting

{% hint style="warning" %}
**Common problems and fixes**

**`whatis ls` returns `ls: nothing appropriate`** → Cause: Man page database is out of date or not yet built. → Fix: Run `sudo mandb` to rebuild, then retry.

***

**`command --help` exits immediately or shows an error** → Cause: Command does not support `--help`; may be a shell builtin. → Fix: Run `help commandname` for builtins, or `man commandname`.

***

**`man ls` displays `No manual entry for ls`** → Cause: The `man-pages` package is not installed. → Fix: Run `sudo dnf install man-pages man-db`.

***

**`apropos keyword` returns nothing** → Cause: Database not indexed, or keyword too specific. → Fix: Run `sudo mandb`, then try a broader keyword.

***

**`info command` shows a generic reader rather than the command's page** → Cause: No standalone info page exists for that command. → Fix: Fall back to `man commandname` or `commandname --help`.
{% endhint %}

## Test Yourself

{% embed url="https://labs.iximiuz.com/challenges/rhcsa-x200101-challenge-1-4e520bb5" %}

**Advanced — Broken Environment:** [Broken Environment Challenge →](https://labs.iximiuz.com/challenges/rhcsa-x200101-challenge-broken-1-7a6c4e17)
