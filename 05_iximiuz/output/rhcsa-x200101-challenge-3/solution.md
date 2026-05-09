# Solution: Persist a Custom Binary Directory in $PATH

## Objective

Add `/opt/myapp/bin` to the `laborant` user's `$PATH` permanently so that `myapp` is available in every future login shell.

## Solution Steps

### 1. Inspect the current PATH

```bash
echo $PATH | tr ':' '\n'
```

Confirm that `/opt/myapp/bin` is not listed.

### 2. Verify the binary exists

```bash
ls -l /opt/myapp/bin/myapp
```

### 3. Add /opt/myapp/bin to ~/.bash_profile

Append the export line using single quotes so `$PATH` is written literally and expanded at login time:

```bash
echo 'export PATH=/opt/myapp/bin:$PATH' >> ~/.bash_profile
```

### 4. Verify the file was updated

```bash
tail -5 ~/.bash_profile
```

Expected output should include:
```
export PATH=/opt/myapp/bin:$PATH
```

### 5. Test the change in a new login shell

```bash
bash --login -c 'echo $PATH | tr ":" "\n"'
```

`/opt/myapp/bin` should appear near the top of the list.

### 6. Confirm myapp is found by the shell

```bash
bash --login -c 'type myapp'
```

Expected output:
```
myapp is /opt/myapp/bin/myapp
```

## Why ~/.bash_profile and Not ~/.bashrc?

On Rocky Linux 9 (and RHEL-family systems), Bash reads initialization files in this order:

| Shell type | Files read |
|---|---|
| Login shell | `~/.bash_profile` (which may source `~/.bashrc`) |
| Interactive non-login shell | `~/.bashrc` |

When a user logs in via SSH or the system console, Bash starts as a **login shell** and reads `~/.bash_profile`. Terminal emulators inside a desktop session typically open **non-login** shells and read `~/.bashrc`.

For the RHCSA exam context (SSH login), `~/.bash_profile` is the correct file. If you also need the setting in non-login shells (e.g., a new terminal tab), you can add the same line to `~/.bashrc` as well — but the verification here specifically tests login shell behavior.

## Common Mistakes

| Mistake | Result |
|---|---|
| Using `export PATH=...` directly in the terminal | Works for the current session only; lost on next login |
| Adding to `~/.bashrc` instead of `~/.bash_profile` | Fails for pure login shells (e.g., SSH) |
| Using double quotes: `export PATH="/opt/myapp/bin:$PATH"` | `$PATH` expands immediately to its current value — still works, but less portable and can cause issues if `$PATH` contains unusual characters |
| Forgetting to include `$PATH` in the new value | Replaces `$PATH` entirely; standard commands like `ls` and `cd` stop working |