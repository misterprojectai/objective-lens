# Solution: RHCSA Prep — Broken HISTCONTROL (ignorespace)

## What Was Broken and Why

The init task appended the following lines to `/home/laborant/.bashrc`:

```bash
# System policy override — do not remove
export HISTCONTROL=ignoredups
```

Because Bash reads `.bashrc` top-to-bottom, this late `export HISTCONTROL=ignoredups` **overwrites** any earlier correct value (such as `HISTCONTROL=ignoreboth` that Rocky Linux 9 ships by default). The result: the `ignorespace` feature is gone, and every command — including those prefixed with a space — gets recorded in history.

This is a realistic attack surface in production: a rogue snippet appended to a shell startup file, disguised as a "system policy," silently changes security-relevant behavior.

---

## How to Diagnose It

### Step 1 — Check the effective value of HISTCONTROL

```bash
echo $HISTCONTROL
```

Expected (broken) output:
```
ignoredups
```

This immediately tells you `ignorespace` is missing.

### Step 2 — Confirm the behavior

```bash
 echo "this-should-not-be-in-history"
history | tail -5
```

If the space-prefixed command appears in `history`, `ignorespace` is not active.

### Step 3 — Find all assignments in .bashrc

```bash
grep -n 'HISTCONTROL' ~/.bashrc
```

Sample output:
```
5:HISTCONTROL=ignoredups:ignorespace
...
47:export HISTCONTROL=ignoredups
```

Line 5 sets the correct value; line 47 (appended by the init task) overrides it with a value that only includes `ignoredups`. The last assignment wins.

### Step 4 — Inspect the tail of .bashrc

```bash
tail -15 ~/.bashrc
```

This reveals the injected block at the bottom of the file.

---

## How to Fix It

You have two equally valid approaches:

### Option A — Remove the rogue override (recommended)

Identify the line number of the bad `HISTCONTROL` assignment:

```bash
grep -n 'HISTCONTROL=ignoredups' ~/.bashrc
```

Then delete that line (example: line 47):

```bash
sed -i '47d' ~/.bashrc
```

Or delete the entire injected block (both the comment and the export):

```bash
grep -n 'System policy override\|HISTCONTROL=ignoredups' ~/.bashrc
# Then delete those line numbers, e.g., lines 46 and 47:
sed -i '46,47d' ~/.bashrc
```

### Option B — Append a correcting override after the bad one

If you cannot remove the injected line (e.g., it is truly policy-locked), append a correcting line that runs last:

```bash
echo 'export HISTCONTROL=ignoreboth' >> ~/.bashrc
```

`ignoreboth` is equivalent to `ignoredups:ignorespace` — it both deduplicates consecutive identical commands and suppresses space-prefixed commands.

### Option C — Replace the bad value in place

```bash
sed -i 's/^export HISTCONTROL=ignoredups$/export HISTCONTROL=ignoreboth/' ~/.bashrc
```

---

## How to Verify the Fix

### 1 — Source the updated file and check the variable

```bash
source ~/.bashrc
echo $HISTCONTROL
```

Expected output:
```
ignoreboth
```
(or any string that contains `ignorespace`)

### 2 — Confirm a new shell also gets the correct value

```bash
bash -c 'source ~/.bashrc 2>/dev/null; echo "HISTCONTROL=$HISTCONTROL"'
```

Expected:
```
HISTCONTROL=ignoreboth
```

### 3 — Functional test

```bash
source ~/.bashrc
 echo "secret-token-should-not-appear"
history | grep "secret-token"
```

If the grep returns nothing, `ignorespace` is working correctly and the challenge is solved.

### 4 — Confirm ~/.bash_history is also unaffected

```bash
history -w
grep "secret-token" ~/.bash_history
```

Should return nothing.

---

## Key Takeaways

| Concept | Detail |
|---|---|
| `HISTCONTROL=ignorespace` | Suppresses space-prefixed commands from history |
| `HISTCONTROL=ignoredups` | Suppresses consecutive duplicate commands only |
| `HISTCONTROL=ignoreboth` | Both behaviors combined (preferred on RHCSA) |
| `.bashrc` evaluation order | Last assignment wins — appended lines override earlier ones |
| Diagnosing overrides | `grep -n 'HISTCONTROL' ~/.bashrc` reveals all competing assignments |