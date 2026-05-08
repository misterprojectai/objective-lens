---
description: Capture both stdout and stderr into a single file using the `&>` operator and the `> file 2>&1` form, and understand why operator ordering matters.
icon: graduation-cap
---

# Combine stdout and stderr into a Single Destination

{% hint style="info" %}
**Prerequisites**

- A RHEL 9 (or compatible) terminal session with a regular user account
- Completion of Tutorial 3, or familiarity with redirecting stdout and stderr separately using `>` and `2>`
{% endhint %}

By the end of this tutorial, you will have run the same command four times — twice with `&>` and twice with `> file 2>&1` — and confirmed that both forms capture all output into a single file. You will also demonstrate the ordering failure that occurs when the explicit form is written incorrectly.

{% stepper %}
{% step %}
### Create a command that produces both stdout and stderr

Run `ls` with one valid path and one invalid path. The valid path writes to stdout; the invalid path writes to stderr.

```bash
ls /etc/hosts /no/such/path
```

{% code title="Output" %}
```
ls: cannot access '/no/such/path': No such file or directory
/etc/hosts
```
{% endcode %}

Both lines appear on the terminal because both streams default to the terminal display. This confirms we have a command that generates both streams simultaneously.
{% endstep %}

{% step %}
### Redirect both streams using `&>`

Redirect everything to a single file with the `&>` operator.

```bash
ls /etc/hosts /no/such/path &> combined.txt
```

{% hint style="success" %}
Nothing appears on the terminal — both stdout and stderr have been captured into `combined.txt`.
{% endhint %}
{% endstep %}

{% step %}
### Verify the contents of combined.txt

Read back what was captured.

```bash
cat combined.txt
```

{% code title="Output" %}
```
ls: cannot access '/no/such/path': No such file or directory
/etc/hosts
```
{% endcode %}

Both the error message and the normal output are present. Neither stream was lost.
{% endstep %}

{% step %}
### Redirect both streams using `> file 2>&1`

Produce the same result using the older, explicit form. This form redirects stdout to the file first, then makes stderr point to wherever stdout is now pointing.

```bash
ls /etc/hosts /no/such/path > combined2.txt 2>&1
```

{% hint style="success" %}
Nothing appears on the terminal — both streams have been captured into `combined2.txt`.
{% endhint %}

{% hint style="warning" %}
Order is critical in the explicit form. Writing `> file 2>&1` works because stderr is pointed at stdout's current destination (the file) after stdout has already been redirected. The wrong order is demonstrated in the next step.
{% endhint %}
{% endstep %}

{% step %}
### Verify the contents of combined2.txt

```bash
cat combined2.txt
```

{% code title="Output" %}
```
ls: cannot access '/no/such/path': No such file or directory
/etc/hosts
```
{% endcode %}

The output is identical to `combined.txt`. Both operators achieve the same result for this command.
{% endstep %}

{% step %}
### Observe the ordering failure — the wrong way

Write the redirections in the wrong order to see what happens when `2>&1` appears before `> file`.

```bash
ls /etc/hosts /no/such/path 2>&1 > combined3.txt
```

{% code title="Output" %}
```
ls: cannot access '/no/such/path': No such file or directory
```
{% endcode %}

{% hint style="warning" %}
The error message appears on the terminal rather than in the file. When `2>&1` is evaluated, stdout is still pointing at the terminal — so stderr is locked to the terminal at that moment. Then stdout is redirected to the file, but stderr is already set and does not follow. Only stdout ends up in the file.
{% endhint %}
{% endstep %}

{% step %}
### Verify that combined3.txt contains only stdout

```bash
cat combined3.txt
```

{% code title="Output" %}
```
/etc/hosts
```
{% endcode %}

Only the normal output went into the file. The `&>` form avoids this problem entirely because it sets both streams simultaneously rather than sequentially.
{% endstep %}

{% step %}
### Confirm the final state of all three files

Verify the complete state of everything built in this tutorial.

```bash
cat combined.txt combined2.txt combined3.txt
```

{% code title="Output" %}
```
ls: cannot access '/no/such/path': No such file or directory
/etc/hosts
ls: cannot access '/no/such/path': No such file or directory
/etc/hosts
/etc/hosts
```
{% endcode %}

`combined.txt` and `combined2.txt` each hold both streams. `combined3.txt` holds only stdout — confirming the ordering failure in the explicit form.
{% endstep %}
{% endstepper %}

{% hint style="success" %}
**You have completed this tutorial.** You can now:

1. Run a command that produces output on both stdout and stderr simultaneously
2. Capture both streams into a single file using the `&>` operator
3. Capture both streams into a single file using the `> file 2>&1` form
4. Explain why `2>&1` must appear after `>` in the explicit form — the shell processes redirections left to right, so position determines what stderr points to at the moment the redirection is evaluated
5. Verify captured output with `cat` to confirm what was and was not redirected
{% endhint %}

## Next Steps

- [How-to: Redirect Command Output in Common Administrative Tasks](#) — apply combined redirection in logging and scripting patterns
- [Explanation: Understanding I/O Redirection and Pipelines](#) — understand why ordering matters in `> file 2>&1` and how the shell processes redirections left to right
- [Reference: I/O Redirection Operators and File Descriptors](#) — see the complete syntax for `&>`, `>&`, `&>>`, and `2>&1`