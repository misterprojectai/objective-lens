---
title: "Redirect stdout to a File with > and >>"
type: tutorial
exam_objective: x200_102
tutorial_index: 1
version: "1.0"
status: draft
---

# Redirect stdout to a File with > and >>

In this tutorial, we will capture command output into a file and then add more output to that same file without overwriting it. Along the way, we will work with the `>` operator, the `>>` operator, and the `cat` command to verify results.

---

## Prerequisites

Before starting, ensure you have:

- A terminal on a RHEL 9 system (or compatible Linux environment) where you can run commands as a regular user
- A home directory you can write files to

---

## What We'll Build

By the end of this tutorial, you will have a file called `~/rhcsa_output.txt` that contains the output of two commands appended one after the other. The system will be in this state:

```
$ cat ~/rhcsa_output.txt
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

The file will contain the directory listing of `/` twice — once written with `>`, once appended with `>>`.

---

## Step 1: Confirm the starting point

First, we check that no file called `rhcsa_output.txt` already exists in our home directory.

```bash
ls ~/rhcsa_output.txt
```

You should see:

```
ls: cannot access '/home/user/rhcsa_output.txt': No such file or directory
```

If you see that error, we are clear to proceed. If the file does exist, remove it with `rm ~/rhcsa_output.txt` before continuing.

---

## Step 2: Write command output to a new file with >

Now we redirect the output of `ls /` into a new file instead of the screen.

```bash
ls / > ~/rhcsa_output.txt
```

You should see:

```
```

No output appears on screen. Notice that the shell returns immediately to the prompt with no response — this confirms that stdout was redirected away from the terminal and into the file.

---

## Step 3: Verify the file was created and contains output

Now we read the file back to confirm it captured the directory listing.

```bash
cat ~/rhcsa_output.txt
```

You should see:

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

The listing that would have appeared on screen is now stored in the file.

---

## Step 4: Overwrite the file by running > again

Now we run a second redirect to the same file to observe what `>` does to existing content.

```bash
echo "overwritten" > ~/rhcsa_output.txt
```

You should see:

```
```

Again, no screen output. Now we check what is in the file.

```bash
cat ~/rhcsa_output.txt
```

You should see:

```
overwritten
```

Notice that the entire previous directory listing is gone. The `>` operator truncated the file and replaced its contents the moment the shell processed the redirect.

---

## Step 5: Restore the file with the directory listing

Now we put our directory listing back so we have a meaningful base to append to.

```bash
ls / > ~/rhcsa_output.txt
```

You should see:

```
```

Verify the content is restored:

```bash
cat ~/rhcsa_output.txt
```

You should see:

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

---

## Step 6: Append a second listing to the file with >>

Now we run the same command a second time, this time using `>>` so the output is added to what is already there.

```bash
ls / >> ~/rhcsa_output.txt
```

You should see:

```
```

---

## Step 7: Verify the complete final state

Finally, we verify the complete file contents match what we set out to build.

```bash
cat ~/rhcsa_output.txt
```

You should see:

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

The directory listing appears twice. The first block was written by `>` in Step 5. The second block was appended by `>>` in Step 6. The original content was preserved.

---

## What We Accomplished

In this tutorial, we:

1. Redirected the output of `ls /` to a new file using `>`
2. Confirmed that running `>` a second time completely overwrites the file's existing contents
3. Restored the file and appended a second copy of the output using `>>`
4. Verified that `>>` adds to the end of existing content without destroying it

---

## Next Steps

Now that you have captured and appended command output to a file, you might want to:

- [How-to: Redirect Command Output in Common Administrative Tasks](#) — apply `>` and `>>` to real log collection and report generation tasks
- [Understanding I/O Redirection and Pipelines](#) — learn why `>` truncates on open and how the shell sets up file descriptors before the command runs
- [Reference: I/O Redirection Operators and File Descriptors](#) — see the complete operator syntax including `2>`, `&>`, and `>>`