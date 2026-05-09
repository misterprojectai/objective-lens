# Solution: Fix a Broken $PATH

## What Happened

During environment setup, this line was appended to `/home/laborant/.bashrc`:

```bash
export PATH=/home/laborant/bin
```

This overwrites the entire `$PATH` with a single directory that contains no standard system commands, so every new shell session loses access to `ls`, `cat`, `id`, and all other tools in `/usr/bin` and `/usr/sbin`.

## Diagnosing the Problem

Open a shell as `laborant` and inspect the current PATH:

```bash
echo $PATH
```

You'll see something like `/home/laborant/bin` — the standard directories are missing.

Confirm the breakage:

```bash
type ls
```

Output:
```
bash: type: ls: not found
```

Check `~/.bashrc` for the culprit:

```bash
cat ~/.bashrc
```

Near the bottom you'll find:
```bash
export PATH=/home/laborant/bin
```

## Fixing the Problem

### Option A — Edit ~/.bashrc with a text editor (recommended)

```bash
nano ~/.bashrc
```

Remove or comment out the broken line:
```bash
# export PATH=/home/laborant/bin
```

Save and exit. Then reload the file:

```bash
source ~/.bashrc
```

### Option B — Use sed to remove the offending line

First, restore PATH for the current session so you can use standard tools:

```bash
export PATH=/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:$HOME/.local/bin:$HOME/bin
```

Then delete the broken line from `~/.bashrc`:

```bash
sed -i '/^export PATH=\/home\/laborant\/bin$/d' ~/.bashrc
```

Reload:

```bash
source ~/.bashrc
```

### Option C — Append a corrected PATH after the broken one

If you prefer not to remove the line, you can override it by appending a correct `export PATH=` line **after** the broken one:

```bash
echo 'export PATH=/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:$HOME/.local/bin:$HOME/bin' >> ~/.bashrc
source ~/.bashrc
```

This works because shell files are processed top-to-bottom; the last assignment wins.

## Verification

```bash
echo $PATH
```

Expected output (order may vary):
```
/home/laborant/.local/bin:/home/laborant/bin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin
```

```bash
type ls
ls /tmp
id
```

All commands should resolve and execute without error.

Open a new terminal session to confirm the fix persists across logins:

```bash
bash --login -c 'echo $PATH && ls /tmp && id'
```