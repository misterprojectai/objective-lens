---
kind: challenge

title: 'Broken Man Pages: whatis Returns Nothing Appropriate'

description: |
  The man page database on this system is broken — `whatis` and `apropos` return
  "nothing appropriate" for every query. Diagnose the root cause and restore full
  functionality of the shell help tools.

categories:
  - linux

tagz:
  - man-pages
  - whatis
  - apropos
  - mandb
  - rhcsa

difficulty: medium

createdAt: 2025-07-30
updatedAt: 2025-07-30

cover: __static__/cover.png

playground:
  name: rockylinux
  machines:
    - name: rocky-01
      resources:
        cpuCount: 2
        ramSize: 2Gi

tasks:
  init_break_mandb:
    init: true
    machine: rocky-01
    run: |
      # Wipe the man page database so whatis/apropos return nothing
      rm -rf /var/cache/man/*
      # Also corrupt the database index files if they exist in the fallback location
      rm -rf /usr/share/man/index.db 2>/dev/null || true
      # Prevent automatic rebuild by making the cache directory unwritable by root
      # (we'll restore that later — instead just leave the DB empty)
      # Ensure mandb binary is present but the DB is gone
      ls /usr/bin/mandb > /dev/null

  verify_whatis_works:
    machine: rocky-01
    run: |
      # whatis ls must return a real description, not "nothing appropriate"
      result=$(whatis ls 2>&1)
      echo "whatis ls output: $result"
      echo "$result" | grep -qi "nothing appropriate" && exit 1
      echo "$result" | grep -qi "list directory" || exit 1
    hintcheck: |
      echo "--- whatis ls output ---"
      whatis ls 2>&1
      echo ""
      echo "--- apropos ls output (first 3 lines) ---"
      apropos ls 2>&1 | head -3
      echo ""
      echo "--- /var/cache/man contents ---"
      ls /var/cache/man/ 2>&1 | head -10

  verify_apropos_works:
    machine: rocky-01
    run: |
      # apropos "list directory" must return at least one result
      result=$(apropos "list directory" 2>&1)
      echo "apropos output: $result"
      echo "$result" | grep -qi "nothing appropriate" && exit 1
      echo "$result" | grep -q "." || exit 1
    hintcheck: |
      echo "--- apropos 'list directory' output ---"
      apropos "list directory" 2>&1
      echo ""
      echo "--- man -f ls ---"
      man -f ls 2>&1

  verify_mandb_rebuilt:
    machine: rocky-01
    run: |
      # Confirm the database files actually exist now
      found=$(find /var/cache/man -name '*.db' -o -name 'index.db' 2>/dev/null | head -1)
      if [ -z "$found" ]; then
        echo "No database files found under /var/cache/man"
        exit 1
      fi
      echo "Database found: $found"
    hintcheck: |
      echo "--- /var/cache/man tree (depth 2) ---"
      find /var/cache/man -maxdepth 2 2>/dev/null | head -20
---

The `laborant` user is trying to use shell help tools to study for their RHCSA exam,
but something is wrong on `rocky-01`.

Every time they run `whatis` or `apropos`, they get the same useless response:

```
$ whatis ls
ls: nothing appropriate.

$ apropos "list directory"
list directory: nothing appropriate.
```

Even `man -f ls` returns nothing. The `man ls` command itself opens a page fine,
but the search and lookup tools are completely broken.

Investigate, diagnose, and fix the problem so that `whatis`, `apropos`, and `man -f`
all return meaningful results again.

::simple-task
---
:tasks: tasks
:name: verify_whatis_works
---
#active
`whatis ls` must return a description containing "list directory"

#completed
`whatis ls` works ✓
::

::simple-task
---
:tasks: tasks
:name: verify_apropos_works
---
#active
`apropos "list directory"` must return at least one result

#completed
`apropos "list directory"` works ✓
::

::simple-task
---
:tasks: tasks
:name: verify_mandb_rebuilt
---
#active
The man page database files must exist under `/var/cache/man`

#completed
Man page database rebuilt ✓
::

::hint-box
---
:summary: Hint 1 — Where to start
---
The `whatis` and `apropos` commands rely on a pre-built database of man page descriptions.
Check whether that database exists on this system.
::

::hint-box
---
:summary: Hint 2 — Where the database lives
---
Look inside `/var/cache/man/` — this is where the man page index database is stored.
If it is empty or missing, that explains why lookups fail.
::

::hint-box
---
:summary: Hint 3 — How to rebuild it
---
The command `sudo mandb` scans all installed man pages and rebuilds the index database.
Check the troubleshooting table in the how-to guide for the exact command.
::