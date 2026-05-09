# Solution: Rebuild the Man Page Database with `mandb`

## What Was Broken and Why

The init task deleted the contents of `/var/cache/man/`, which is where the `whatis`
and `apropos` index database is stored. Without this database, both commands have
nothing to search and return `nothing appropriate` for every query.

The `man` command itself still works because it reads the raw groff/troff source
files directly from `/usr/share/man/`. But `whatis`, `apropos`, and `man -f` depend
entirely on the pre-indexed database — so they all fail silently.

---

## How to Diagnose It

### Step 1 — Reproduce the symptom

```bash
whatis ls
# ls: nothing appropriate.

apropos "list directory"
# list directory: nothing appropriate.

man -f ls
# ls: nothing appropriate.
```

All three commands fail. But `man ls` still opens a page — confirming the raw source
files are intact.

### Step 2 — Identify what these commands depend on

Recall from the how-to guide:

> If `apropos` returns `nothing appropriate`, the man page database may need rebuilding:
> `sudo mandb`

This is the key clue. The database, not the man pages themselves, is broken.

### Step 3 — Confirm the database is missing

```bash
ls /var/cache/man/
```

The directory is empty (or contains no `.db` files). On a healthy system you would
see subdirectories with `index.db` files inside.

```bash
find /var/cache/man -name '*.db' | head -5
# (no output)
```

This confirms the database has been wiped.

---

## How to Fix It

Rebuild the man page index database:

```bash
sudo mandb
```

The command scans all man page directories (typically under `/usr/share/man/` and
`/usr/local/share/man/`) and writes fresh index files into `/var/cache/man/`.

Expected output (abbreviated):

```
Purging old database entries in /usr/share/man...
Processing manual pages under /usr/share/man...
Updating index cache for path `/usr/share/man/man1'. Wait...done.
...
1845 man subdirectories contained newer manual pages.
12453 manual pages were added.
0 stale pages were removed.
```

---

## How to Verify the Fix

```bash
# 1. whatis should return a description
whatis ls
# ls (1)               - list directory contents

# 2. apropos should return matches
apropos "list directory"
# ls (1)               - list directory contents

# 3. man -f is identical to whatis
man -f ls
# ls (1)               - list directory contents

# 4. Confirm database files exist
find /var/cache/man -name '*.db' | head -3
# /var/cache/man/en/index.db
# /var/cache/man/index.db
```

All four checks passing confirms the man page database has been fully rebuilt and
the shell help tools are working correctly again.

---

## Key Takeaway

`whatis`, `apropos`, and `man -f` are database lookups — they search a pre-built
index, not the raw man page files. When the database is missing or stale, these
tools fail silently with `nothing appropriate`. The fix is always `sudo mandb` to
rebuild the index.