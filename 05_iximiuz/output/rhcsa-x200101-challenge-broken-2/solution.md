# Solution: Fix the Broken PATH in `.bashrc`

## What Was Broken and Why

The init task appended the following line to `/home/laborant/.bashrc`:

```bash
export PATH=/home/laborant/.local/bin:/home/laborant/bin
```

This **completely overwrites** the `$PATH` variable, discarding all the standard system directories like `/usr/bin`, `/usr/sbin`, `/usr/local/bin`, and `/usr/local/sbin`. Because the shell finds executables by searching `$PATH` left-to-right, removing `/usr/bin` means commands like `ls`, `cat`, `grep`, `which`, and virtually every other standard system utility become unreachable — resulting in "command not found" errors for nearly everything.

---

## How to Diagnose It

### Step 1: Check what `$PATH` currently contains

Log in (or `su - laborant`) and run:

```bash
echo $PATH
```

A broken output looks like:

```
/home/laborant/.local/bin:/home/laborant/bin
```

Notice that `/usr/bin` and `/usr/sbin` are completely absent. This is the smoking gun.

### Step 2: Confirm the command is missing from PATH

Try to locate a command explicitly:

```bash
type ls
```

Output:
```
bash: type: ls: not found
```

Or:

```bash
/usr/bin/ls
```

This works because you bypassed `$PATH` by giving the full path. This confirms the binary exists — it's just not findable through `$PATH`.

### Step 3: Find where the broken PATH is set

Inspect the shell startup file:

```bash
grep 'PATH' /home/laborant/.bashrc
```

You will see the culprit line at the bottom:

```bash
export PATH=/home/laborant/.local/bin:/home/laborant/bin
```

This line **replaces** the entire `$PATH` rather than appending to it (which would use `$PATH:new_dir`).

---

## How to Fix It

You need to either remove the bad line or add a corrected `PATH` export after it. The cleanest approach is to append the correct definition so it overrides the broken one:

```bash
echo 'export PATH=/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:$HOME/.local/bin:$HOME/bin' >> /home/laborant/.bashrc
```

Alternatively, open `.bashrc` in an editor (use the full path since `vi` might not be in your current broken PATH):

```bash
/usr/bin/vi /home/laborant/.bashrc
```

Find the offending line:

```bash
export PATH=/home/laborant/.local/bin:/home/laborant/bin
```

And change it to the correct value:

```bash
export PATH=/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:$HOME/.local/bin:$HOME/bin
```

---

## How to Verify the Fix

### Check the file directly:

```bash
grep 'export PATH=' /home/laborant/.bashrc | tail -1
```

You should see `/usr/bin` and `/usr/sbin` in the output.

### Start a new login shell and test:

```bash
su - laborant
ls
type ls
echo $PATH
```

Expected output from `type ls`:

```
ls is aliased to 'ls --color=auto'
```

And `echo $PATH` should show something like:

```
/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/home/laborant/.local/bin:/home/laborant/bin
```

Standard system commands now resolve correctly.

---

## Key Takeaway

The difference between:

```bash
export PATH=/some/dir          # REPLACES PATH entirely — dangerous!
export PATH=$PATH:/some/dir    # APPENDS to PATH — safe
```

is critical. Overwriting `$PATH` without including the system directories is a common misconfiguration that renders a shell nearly unusable. Always preserve existing `$PATH` entries unless you intentionally want to isolate the environment.