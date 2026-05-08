---
description: Supply file content as standard input to a command using the `<` operator on a RHEL 9 system.
icon: graduation-cap
---

# Redirect stdin from a File with `<`

In this tutorial, you will create a text file and feed it to two commands using `<`. You will see that the `<` operator connects a file to a command's standard input instead of the keyboard, and that redirecting a file never modifies it.

{% hint style="info" %}
**Prerequisites**

- A terminal session on a RHEL 9 system (local or remote)
- Ability to run commands as a regular user — no root required
{% endhint %}

By the end of this tutorial, both of these commands will produce their expected output:

```bash
wc -l < ~/words.txt
sort < ~/words.txt
```

{% code title="Target state" %}
```
5
---
apple
banana
cherry
date
elderberry
```
{% endcode %}

---

{% stepper %}
{% step %}
### Create a file to use as input

Run `printf` with output redirection to write five fruit names, one per line, into `~/words.txt`.

```bash
printf 'cherry\nbanana\ndate\napple\nelderberry\n' > ~/words.txt
```

{% hint style="success" %}
**Expected output:** none. No output on screen means the redirection worked correctly — the shell created `~/words.txt` and wrote the five lines into it.
{% endhint %}
{% endstep %}

{% step %}
### Confirm the file exists and contains five lines

Read the file back with `cat` to verify the contents before redirecting it anywhere.

```bash
cat ~/words.txt
```

{% code title="Output" %}
```
cherry
banana
date
apple
elderberry
```
{% endcode %}

The five lines appear in the order they were written — unsorted, exactly as entered.
{% endstep %}

{% step %}
### Count lines by redirecting the file into wc

Use `<` to connect `~/words.txt` to `wc -l`'s standard input instead of the keyboard.

```bash
wc -l < ~/words.txt
```

{% code title="Output" %}
```
5
```
{% endcode %}

{% hint style="info" %}
`wc` reports only the count — no filename appears. When `wc` reads from standard input (whether keyboard or file), it has no filename to display, so only the number is printed.
{% endhint %}
{% endstep %}

{% step %}
### Sort the file by redirecting it into sort

Pass the same file to `sort` using `<`. The operator works identically regardless of which command receives the input.

```bash
sort < ~/words.txt
```

{% code title="Output" %}
```
apple
banana
cherry
date
elderberry
```
{% endcode %}

`sort` receives the five lines from the file and returns them in alphabetical order. The original file is not touched — `sort` only reads from it.
{% endstep %}

{% step %}
### Verify the original file is unchanged

Confirm that both redirect operations left `~/words.txt` with its original, unsorted content.

```bash
cat ~/words.txt
```

{% code title="Output" %}
```
cherry
banana
date
apple
elderberry
```
{% endcode %}

{% hint style="success" %}
The file content is identical to what you saw in step 2. Redirecting a file into a command as standard input never modifies the source file.
{% endhint %}
{% endstep %}
{% endstepper %}

---

{% hint style="success" %}
**You completed this tutorial.** You have:

1. Created a five-line text file using `printf` and output redirection
2. Confirmed the file contents with `cat`
3. Redirected the file into `wc -l` using `<` to count lines without typing a filename argument
4. Redirected the same file into `sort` using `<` to produce alphabetically ordered output
5. Verified that the source file remained unchanged after both redirect operations
{% endhint %}

## Next Steps

- **How-to: Redirect Command Output in Common Administrative Tasks** — apply input and output redirection together in real administration scenarios
- **Understanding I/O Redirection and Pipelines** — learn why the shell substitutes file descriptors before a command starts, and what that means for `<`, `>`, and `|`
- **Reference: I/O Redirection Operators and File Descriptors** — see the complete syntax for all redirection operators including `0<` and its equivalents