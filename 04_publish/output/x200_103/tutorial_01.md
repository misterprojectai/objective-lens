---
description: Use grep to filter lines from files and pipelines using literal string patterns, case-insensitive matching, and inverted selection.
icon: graduation-cap
---

# Filter Text Streams with Basic grep

{% hint style="info" %}
**Prerequisites**
- A RHEL 9 (or compatible) system with a terminal and shell access
- A non-root user account with `sudo` access, or direct access as root
{% endhint %}

{% stepper %}
{% step %}
### Search a File for a Literal String

Run `grep` against `/etc/passwd` to find every line containing the string `root`.

```bash
grep 'root' /etc/passwd
```

{% code title="Output" %}
```
root:x:0:0:root:/root:/bin/bash
operator:x:11:0:operator:/root:/sbin/nologin
```
{% endcode %}

Both lines appear because each one contains the characters `root` somewhere — `grep` searches the entire line regardless of position. All other lines in the file were discarded.
{% endstep %}

{% step %}
### Confirm That the Match Is Case-Sensitive by Default

Now that you have seen a basic match, confirm that `grep` treats uppercase and lowercase as different by default.

```bash
grep 'ROOT' /etc/passwd
```

{% hint style="success" %}
The shell returns to the prompt with no lines printed. The string `ROOT` in all capitals does not appear anywhere in `/etc/passwd`, so `grep` selects nothing and produces no output — confirming that matching is case-sensitive unless told otherwise.
{% endhint %}
{% endstep %}

{% step %}
### Use -i to Match Regardless of Case

Add the `-i` flag so that `grep` matches `ROOT`, `root`, `Root`, and any other capitalisation of that sequence.

```bash
grep -i 'ROOT' /etc/passwd
```

{% code title="Output" %}
```
root:x:0:0:root:/root:/bin/bash
operator:x:11:0:operator:/root:/sbin/nologin
```
{% endcode %}

{% hint style="info" %}
The output is identical to Step 1. The `-i` flag changes what `grep` matches, not what it prints — the original line text is preserved exactly as it appears in the file.
{% endhint %}
{% endstep %}

{% step %}
### Filter Pipeline Output with grep

Pipe `dmesg` output through `grep` and keep only lines that mention a network interface string.

```bash
dmesg | grep -i 'eth'
```

{% code title="Output (example — varies by system)" %}
```
[    1.234567] e1000 0000:00:03.0 eth0: (PCI:33MHz:32-bit)
[    1.235678] e1000 0000:00:03.0 eth0: Intel(R) PRO/1000 Network Connection
```
{% endcode %}

{% hint style="warning" %}
If your system uses a different interface naming scheme, you may see no output — that is expected. The pipeline mechanics still apply: `dmesg` produces many lines, `grep` receives all of them on standard input, and only matching lines pass through to the terminal.
{% endhint %}

<details>
<summary>No output? Verify the pipeline is working</summary>

If your system produces no `eth` results, confirm the pipeline itself is functioning by searching for CPU initialisation messages instead:

```bash
dmesg | grep -i 'cpu'
```

You should see one or more lines mentioning CPU initialisation. If output appears here, the pipeline is working correctly — your system simply uses a different network interface naming scheme.

</details>
{% endstep %}

{% step %}
### Invert the Match with -v to Exclude Lines

Use `-v` to reverse `grep`'s behaviour: instead of selecting lines that match, select lines that do not match. Filter `/etc/passwd` to hide every account that uses `nologin` as its shell.

```bash
grep -v 'nologin' /etc/passwd
```

{% code title="Output (varies by system)" %}
```
root:x:0:0:root:/root:/bin/bash
sync:x:5:0:sync:/sbin:/bin/sync
shutdown:x:6:0:shutdown:/sbin:/sbin/shutdown
halt:x:7:0:halt:/sbin:/sbin/halt
student:x:1000:1000::/home/student:/bin/bash
```
{% endcode %}

Every line containing `nologin` is gone — only accounts without that string in their entry remain.
{% endstep %}

{% step %}
### Verify All Four Forms of grep Invocation

Run all four forms in sequence to confirm the complete picture of what you have built.

```bash
grep 'root' /etc/passwd
echo "---"
grep -i 'ROOT' /etc/passwd
echo "---"
dmesg | grep -i 'cpu' | head -2
echo "---"
grep -v 'nologin' /etc/passwd
```

{% code title="Output" %}
```
root:x:0:0:root:/root:/bin/bash
operator:x:11:0:operator:/root:/sbin/nologin
# (grep -i ROOT)
root:x:0:0:root:/root:/bin/bash
operator:x:11:0:operator:/root:/sbin/nologin
# (dmesg | grep cpu)
(two lines from dmesg mentioning cpu)
# (grep -v nologin)
root:x:0:0:root:/root:/bin/bash
sync:x:5:0:sync:/sbin:/bin/sync
shutdown:x:6:0:shutdown:/sbin:/sbin/shutdown
halt:x:7:0:halt:/sbin:/sbin/halt
student:x:1000:1000::/home/student:/bin/bash
```
{% endcode %}

Each `grep` invocation demonstrates a distinct capability: file search, case-insensitive file search, pipeline filtering, and inverted matching.
{% endstep %}
{% endstepper %}

{% hint style="success" %}
**You've completed this tutorial.** You can now:

1. Run `grep` against a file to select lines containing a literal string
2. Confirm that `grep` is case-sensitive by default by attempting a mismatched-case search
3. Apply the `-i` flag to match a pattern regardless of capitalisation
4. Pipe command output through `grep` to filter a live data stream
5. Use `-v` to invert the match and exclude lines containing a specific string
{% endhint %}

## Next Steps

- **Tutorial 2: Anchor Patterns to Lines with ^ and $** — restrict where in a line a match is allowed to occur
- **How-to: Filter Log Files with grep** — apply these skills to real system log analysis
- **Explanation: Understanding grep and Regular Expressions** — understand why grep works the way it does, including the filter model and case behaviour
- **Reference: grep Options and Regular Expression Syntax** — see the complete list of flags and pattern syntax