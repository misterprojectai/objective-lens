---
description: Capture command output into a file using > and append additional output using >> without overwriting existing content.
icon: graduation-cap
---

# Redirect stdout to a File with > and >>

In this tutorial, you will capture command output into a file and then add more output to that same file without overwriting it. Along the way, you will work with the `>` operator, the `>>` operator, and the `cat` command to verify results.

{% hint style="info" %}
**Before you start, you need:**
- A terminal on a RHEL 9 system (or compatible Linux environment) where you can run commands as a regular user
- A home directory you can write files to
{% endhint %}

By the end of this tutorial, you will have a file called `~/rhcsa_output.txt` containing the output of two commands appended one after the other — the directory listing of `/` written once with `>` and again with `>>`.

---

{% stepper %}
{% step %}
### Confirm the starting point

Check that no file called `rhcsa_output.txt` already exists in your home directory.

```bash
ls ~/rhcsa_output.txt
```

{% code title="Output" %}
```
ls: cannot access '/home/user/rhcsa_output.txt': No such file or directory
```
{% endcode %}

If you see that error, you are clear to proceed.

<details>
<summary>The file already exists — what do I do?</summary>

Remove it before continuing:

```bash
rm ~/rhcsa_output.txt
```

Then re-run the `ls` check to confirm it is gone.

</details>
{% endstep %}

{% step %}
### Write command output to a new file with >

Redirect the output of `ls /` into a new file instead of the screen.

```bash
ls / > ~/rhcsa_output.txt
```

{% hint style="success" %}
No output appears on screen. The shell returns immediately to the prompt with no response — this confirms that stdout was redirected away from the terminal and into the file.
{% endhint %}
{% endstep %}

{% step %}
### Verify the file was created and contains output

Read the file back to confirm it captured the directory listing.

```bash
cat ~/rhcsa_output.txt
```

{% code title="Output" %}
```
bin
boot
dev
etc
home
lib
lib64
lost+found
media
mnt
opt
proc
root
run
sbin
srv
sys
tmp
usr
var
```
{% endcode %}

The listing that would have appeared on screen is now stored in the file.
{% endstep %}

{% step %}
### Overwrite the file by running > again

Run a second redirect to the same file to observe what `>` does to existing content.

```bash
echo "overwritten" > ~/rhcsa_output.txt
```

Again, no screen output. Now check what is in the file.

```bash
cat ~/rhcsa_output.txt
```

{% code title="Output" %}
```
overwritten
```
{% endcode %}

{% hint style="warning" %}
The entire previous directory listing is gone. The `>` operator truncated the file and replaced its contents the moment the shell processed the redirect — before the command on the left even ran.
{% endhint %}
{% endstep %}

{% step %}
### Restore the file with the directory listing

Put the directory listing back so you have a meaningful base to append to.

```bash
ls / > ~/rhcsa_output.txt
```

Verify the content is restored:

```bash
cat ~/rhcsa_output.txt
```

{% code title="Output" %}
```
bin
boot
dev
etc
home
lib
lib64
lost+found
media
mnt
opt
proc
root
run
sbin
srv
sys
tmp
usr
var
```
{% endcode %}
{% endstep %}

{% step %}
### Append a second listing to the file with >>

Run the same command a second time, this time using `>>` so the output is added to what is already there.

```bash
ls / >> ~/rhcsa_output.txt
```

{% hint style="success" %}
No output appears on screen. Unlike `>`, the `>>` operator does not truncate the file — it opens it for appending.
{% endhint %}
{% endstep %}

{% step %}
### Verify the complete final state

Confirm the complete file contents match what you set out to build.

```bash
cat ~/rhcsa_output.txt
```

{% code title="Output" %}
```
bin
boot
dev
etc
home
lib
lib64
lost+found
media
mnt
opt
proc
root
run
sbin
srv
sys
tmp
usr
var
bin
boot
dev
etc
home
lib
lib64
lost+found
media
mnt
opt
proc
root
run
sbin
srv
sys
tmp
usr
var
```
{% endcode %}

The directory listing appears twice. The first block was written by `>` in Step 5. The second block was appended by `>>` in Step 6. The original content was preserved.
{% endstep %}
{% endstepper %}

{% hint style="success" %}
**You did it.** In this tutorial you:

1. Redirected the output of `ls /` to a new file using `>`
2. Confirmed that running `>` a second time completely overwrites the file's existing contents
3. Restored the file and appended a second copy of the output using `>>`
4. Verified that `>>` adds to the end of existing content without destroying it
{% endhint %}

---

## Next Steps

Now that you have captured and appended command output to a file, you might want to explore:

- [How-to: Redirect Command Output in Common Administrative Tasks](#) — apply `>` and `>>` to real log collection and report generation tasks
- [Understanding I/O Redirection and Pipelines](#) — learn why `>` truncates on open and how the shell sets up file descriptors before the command runs
- [Reference: I/O Redirection Operators and File Descriptors](#) — see the complete operator syntax including `2>`, `&>`, and `>>`