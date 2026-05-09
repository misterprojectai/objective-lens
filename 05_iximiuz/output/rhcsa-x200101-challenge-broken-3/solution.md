# Solution: Fix the Broken $PATH Export in ~/.bash_profile

## What Was Broken

The init task introduced a subtle but devastating bug in `/home/laborant/.bash_profile`.
The `export` line was written as:

```bash
export PATH=/opt/tools/bin:$PATH >> /dev/null 2>&1
```

This looks like a valid `export` statement at a glance, but it is actually broken in a
non-obvious way. The `>> /dev/null 2>&1` appended to an `export` line is parsed by Bash
as a **file redirection on the export command itself**. Because `export` produces no
output, nothing meaningful is redirected — but more importantly, the **entire line is
treated as a command with a redirection**, and the `PATH` variable assignment inside the
export is silently discarded when the redirection token is encountered in a way that
corrupts the parsing of the variable value. The net result: `$PATH` is **not updated**.

## How to Diagnose

### Step 1 — Test a new login shell directly

```bash
bash --login -c 'echo $PATH | tr ":" "\n"'
```

If `/opt/tools/bin` is missing from the output, the problem is in the login shell
startup files.

### Step 2 — Check which command is not found

```bash
bash --login -c 'type greet'
```

Expected (broken): `bash: type: greet: not found`

### Step 3 — Inspect ~/.bash_profile carefully

```bash
cat ~/.bash_profile
```

Look at the `export PATH=` line very carefully. You will see:

```bash
export PATH=/opt/tools/bin:$PATH >> /dev/null 2>&1
```

The `>> /dev/null 2>&1` suffix is the culprit. It is a shell redirection appended
directly to the export command. Bash parses this as redirecting the output of the export
command to `/dev/null`, and the `$PATH` token after the redirection operator is treated
as part of the redirection target, not the variable expansion you intended.

### Step 4 — Verify no syntax error prevents loading

```bash
bash -n ~/.bash_profile
```

This will report no syntax error (the line is valid Bash — just logically broken), which
is exactly what makes this bug hard to spot.

### Step 5 — Confirm the variable is not set after sourcing

```bash
bash --login -c 'echo "PATH starts with: ${PATH%%:*}"'
```

If the first component is not `/opt/tools/bin`, the export failed.

## How to Fix

Edit `~/.bash_profile` and replace the broken export line with a correct one.

### Option A — Use a text editor

```bash
vi ~/.bash_profile
```

Find the line:

```bash
export PATH=/opt/tools/bin:$PATH >> /dev/null 2>&1
```

Change it to:

```bash
export PATH=/opt/tools/bin:$PATH
```

### Option B — Use sed in-place

```bash
sed -i 's|export PATH=/opt/tools/bin:\$PATH >> /dev/null 2>&1|export PATH=/opt/tools/bin:$PATH|' ~/.bash_profile
```

### Option C — Append a corrected line (and optionally remove the old one)

```bash
# Remove the broken line
sed -i '/export PATH=.*tools.*\/dev\/null/d' ~/.bash_profile
# Append the correct line
echo 'export PATH=/opt/tools/bin:$PATH' >> ~/.bash_profile
```

## How to Verify the Fix

### Verify the file contains the correct line

```bash
grep 'export PATH' ~/.bash_profile
```

Expected output (no redirection, no extra tokens after `$PATH`):

```
export PATH=/opt/tools/bin:$PATH
```

### Verify a new login shell picks up the directory

```bash
bash --login -c 'echo $PATH | tr ":" "\n" | grep tools'
```

Expected output:

```
/opt/tools/bin
```

### Verify the command is found in a new login shell

```bash
bash --login -c 'type greet'
```

Expected output:

```
greet is /opt/tools/bin/greet
```

### Open a full new login shell and confirm interactively

```bash
exec bash --login
type greet
greet
```

Expected:

```
greet is /opt/tools/bin/greet
Hello from /opt/tools/bin/greet
```

## Key Lesson

Shell redirections (`>`, `>>`) can be appended to almost any command in Bash, including
`export`. When you write:

```bash
export PATH=/opt/tools/bin:$PATH >> /dev/null 2>&1
```

Bash interprets `>> /dev/null` as a redirection of the `export` command's stdout. The
`2>&1` redirects stderr to stdout (which is now `/dev/null`). The `export` command's
output (nothing, for a variable assignment) is thrown away. Critically, the **value
assigned to PATH may be truncated or misinterpreted** depending on shell version because
the `>>` token interrupts the assignment parsing.

This is a realistic misconfiguration — a developer might copy-paste a `>> /dev/null 2>&1`
suffix from a cron job or script context and accidentally append it to an export line in
a profile file. The line looks correct at a glance, produces no error, but silently
fails to set the variable.