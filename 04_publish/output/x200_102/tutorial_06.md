---
description: Use the tee command to split a pipeline stream, capturing intermediate output to a file while passing data through to the next command unchanged.
icon: graduation-cap
---

# Split a Pipeline Stream with tee

{% hint style="info" %}
**Prerequisites**

- A RHEL 9 (or compatible) terminal session as a regular user
- Completion of Tutorial 5, or comfort running basic pipelines with `|`
{% endhint %}

By the end of this tutorial, you will have run a pipeline that lists all running processes, saves the full list to a file called `allprocs.txt`, and then filters the stream to show only SSH-related processes on screen.

{% stepper %}
{% step %}
### Run a plain pipeline without tee

Run a two-stage pipeline to confirm that `ps` output flows into `grep` and that SSH-related processes appear on screen. This establishes what the pipeline does before we insert `tee`.

```bash
ps aux | grep ssh
```

{% hint style="success" %}
**Expected output**

```
root         892  0.0  0.1  15892  7104 ?        Ss   08:01   0:00 sshd: /usr/sbin/sshd -D [listener] 0 of 10-100 startups
user        1234  0.0  0.0   6408   720 pts/0    S+   09:14   0:00 grep --color=auto ssh
```

Notice that `grep` itself appears in the results — this is expected behaviour that you will see on every system.
{% endhint %}
{% endstep %}

{% step %}
### Insert tee to capture the full process list

Insert `tee` between `ps` and `grep`. This saves every line that `ps` produces to `allprocs.txt` while simultaneously passing the same data forward to `grep`.

```bash
ps aux | tee allprocs.txt | grep ssh
```

{% hint style="success" %}
**Expected output**

```
root         892  0.0  0.1  15892  7104 ?        Ss   08:01   0:00 sshd: /usr/sbin/sshd -D [listener] 0 of 10-100 startups
user        1234  0.0  0.0   6408   720 pts/0    S+   09:14   0:00 grep --color=auto ssh
```

The screen output has not changed — `grep` still receives the full stream from `tee` exactly as if `tee` were not there.
{% endhint %}

{% hint style="warning" %}
`tee` writes to `allprocs.txt` at the point it sits in the pipeline — between `ps` and `grep`. The file captures the full, unfiltered `ps` output, not the grep-filtered result. Position matters.
{% endhint %}
{% endstep %}

{% step %}
### Verify the file was written

Confirm that `allprocs.txt` contains the complete, unfiltered output from `ps` — not just the SSH lines.

```bash
wc -l allprocs.txt
```

{% hint style="success" %}
**Expected output**

```
187 allprocs.txt
```

The line count will be substantially larger than the number of SSH lines printed to screen. The file holds every process, while the screen showed only the filtered subset.
{% endhint %}

<details>
<summary>If you see 0 allprocs.txt or the file does not exist</summary>

The file was not written, which means `tee` did not run. Confirm you used the exact pipeline from Step 2:

```bash
ps aux | tee allprocs.txt | grep ssh
```

Common mistakes: omitting `tee`, reversing the order of `tee` and `grep`, or mistyping the filename. Re-run the command and then re-run `wc -l allprocs.txt`.

</details>
{% endstep %}

{% step %}
### Inspect the beginning of the captured file

Examine the top of the file to confirm it contains the full `ps` header and process list, not just the grep results.

```bash
head -5 allprocs.txt
```

{% hint style="success" %}
**Expected output**

```
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1  0.0  0.3 171820 13200 ?        Ss   08:01   0:01 /usr/lib/systemd/systemd
root           2  0.0  0.0      0     0 ?        S    08:01   0:00 [kthreadd]
root           3  0.0  0.0      0     0 ?        I<   08:01   0:00 [rcu_gp]
root           4  0.0  0.0      0     0 ?        I<   08:01   0:00 [rcu_par_gp]
```

The header row confirms we captured everything from `ps`, not only the lines that matched `grep`.
{% endhint %}
{% endstep %}

{% step %}
### Query the saved file independently

Search the saved file directly with `grep`. This confirms the file is self-contained and can be queried independently of any running pipeline.

```bash
grep ssh allprocs.txt
```

{% hint style="success" %}
**Expected output**

```
root         892  0.0  0.1  15892  7104 ?        Ss   08:01   0:00 sshd: /usr/sbin/sshd -D [listener] 0 of 10-100 startups
```

The SSH entry is present in the file, confirming that `tee` wrote the full unfiltered stream and the pipeline continued filtering normally. Note that the `grep` process itself does not appear here, because this search runs against the static file rather than live process output.
{% endhint %}
{% endstep %}
{% endstepper %}

{% hint style="success" %}
**What you accomplished**

In this tutorial, you:

1. Ran a two-stage `ps | grep` pipeline to establish a baseline
2. Inserted `tee allprocs.txt` between `ps` and `grep` to split the stream, writing the full process list to a file while passing all data forward to `grep` unchanged
3. Verified with `wc -l` that the file contained the complete unfiltered output
4. Confirmed with `head` that the file holds the full `ps` header and process list
5. Queried the saved file independently with `grep` to confirm it is a complete, standalone record
{% endhint %}

## Next Steps

- [How-to: Build and Debug Multi-Stage Pipelines](#) — apply `tee` to inspect intermediate stages when a long pipeline produces unexpected results
- [Explanation: Understanding I/O Redirection and Pipelines](#) — understand why `tee` reads stdin and writes to both stdout and a file simultaneously
- [Reference: I/O Redirection Operators and File Descriptors](#) — see the complete `tee` syntax, including the `-a` append option