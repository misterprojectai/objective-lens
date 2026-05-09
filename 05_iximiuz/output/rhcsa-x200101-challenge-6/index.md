---
kind: challenge

title: 'RHCSA Prep: Quoting and Escaping Special Characters in Shell Commands'

description: |
  Master Bash quoting forms — single quotes, double quotes, backslash escaping, and ANSI-C quoting — to correctly handle filenames and arguments containing spaces, glob characters, dollar signs, and newlines.

categories:
  - linux

tagz:
  - bash
  - quoting
  - shell
  - rhcsa-prep
  - special-characters

difficulty: hard

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
  init_create_workdir:
    machine: rocky-01
    user: laborant
    init: true
    run: |
      mkdir -p /home/laborant/quote-test
      chown laborant:laborant /home/laborant/quote-test

  verify_four_files:
    machine: rocky-01
    user: laborant
    needs:
      - init_create_workdir
    hintcheck: |
      echo "Files found in ~/quote-test:"
      ls -1 /home/laborant/quote-test 2>/dev/null || echo "(directory is empty or missing)"
      echo ""
      echo "Expected exactly these four filenames:"
      echo "  report 2024.txt"
      echo "  report 2025.txt"
      echo "  costs [final].csv"
      echo "  price\$list.txt"
    run: |
      DIR=/home/laborant/quote-test
      [ -f "${DIR}/report 2024.txt" ]    || { echo "Missing: 'report 2024.txt'";    exit 1; }
      [ -f "${DIR}/report 2025.txt" ]    || { echo "Missing: 'report 2025.txt'";    exit 1; }
      [ -f "${DIR}/costs [final].csv" ]  || { echo "Missing: 'costs [final].csv'";  exit 1; }
      [ -f "${DIR}/price\$list.txt" ]    || { echo "Missing: 'price\$list.txt'";    exit 1; }
      echo "All four files exist"

  verify_archive_exists:
    machine: rocky-01
    user: laborant
    needs:
      - init_create_workdir
    hintcheck: |
      echo "Looking for /home/laborant/quote-test/special-files.tar.gz ..."
      ls -lh /home/laborant/quote-test/special-files.tar.gz 2>/dev/null || echo "File not found."
      echo ""
      echo "The archive must contain all four files with their exact names."
      echo "Try: tar tzf /home/laborant/quote-test/special-files.tar.gz"
    run: |
      ARCHIVE=/home/laborant/quote-test/special-files.tar.gz
      [ -f "${ARCHIVE}" ] || { echo "Archive not found: ${ARCHIVE}"; exit 1; }

      tar tzf "${ARCHIVE}" > /tmp/archive_contents.txt 2>&1 \
        || { echo "Cannot read archive"; exit 1; }

      grep -qF 'report 2024.txt'   /tmp/archive_contents.txt || { echo "Archive missing: 'report 2024.txt'";   exit 1; }
      grep -qF 'report 2025.txt'   /tmp/archive_contents.txt || { echo "Archive missing: 'report 2025.txt'";   exit 1; }
      grep -qF 'costs [final].csv' /tmp/archive_contents.txt || { echo "Archive missing: 'costs [final].csv'"; exit 1; }
      grep -qF 'price$list.txt'    /tmp/archive_contents.txt || { echo "Archive missing: 'price\$list.txt'";   exit 1; }
      echo "Archive is correct"

  verify_summary_file:
    machine: rocky-01
    user: laborant
    needs:
      - init_create_workdir
    hintcheck: |
      echo "Looking for /home/laborant/quote-test/summary.txt ..."
      cat /home/laborant/quote-test/summary.txt 2>/dev/null || echo "File not found or empty."
      echo ""
      echo "The file must contain exactly four lines — one per filename — produced by"
      echo "iterating with a for loop that uses double quotes around the loop variable."
    run: |
      SUMMARY=/home/laborant/quote-test/summary.txt
      [ -f "${SUMMARY}" ] || { echo "summary.txt not found"; exit 1; }

      grep -qF 'report 2024.txt'   "${SUMMARY}" || { echo "summary.txt missing: 'report 2024.txt'";   exit 1; }
      grep -qF 'report 2025.txt'   "${SUMMARY}" || { echo "summary.txt missing: 'report 2025.txt'";   exit 1; }
      grep -qF 'costs [final].csv' "${SUMMARY}" || { echo "summary.txt missing: 'costs [final].csv'"; exit 1; }
      grep -qF 'price$list.txt'    "${SUMMARY}" || { echo "summary.txt missing: 'price\$list.txt'";   exit 1; }

      LINE_COUNT=$(wc -l < "${SUMMARY}")
      [ "${LINE_COUNT}" -eq 4 ] || { echo "summary.txt must have exactly 4 lines, found ${LINE_COUNT}"; exit 1; }
      echo "summary.txt is correct"

  verify_ansi_file:
    machine: rocky-01
    user: laborant
    needs:
      - init_create_workdir
    hintcheck: |
      echo "Looking for /home/laborant/quote-test/notes.txt ..."
      cat -A /home/laborant/quote-test/notes.txt 2>/dev/null || echo "File not found."
      echo ""
      echo "The file must contain a literal tab character between 'Status' and 'OK',"
      echo "and 'it'\''s ready' (with a real apostrophe) on a second line."
      echo "Use ANSI-C quoting \$'...' to embed \\t (tab) and \\' (apostrophe)."
    run: |
      NOTES=/home/laborant/quote-test/notes.txt
      [ -f "${NOTES}" ] || { echo "notes.txt not found"; exit 1; }

      # Line 1: must contain a literal tab between Status and OK
      grep -qP 'Status\tOK' "${NOTES}" \
        || { echo "Line 1 must contain a literal tab between 'Status' and 'OK'"; exit 1; }

      # Line 2: must contain the apostrophe form "it's ready"
      grep -qF "it's ready" "${NOTES}" \
        || { echo "Line 2 must contain: it's ready"; exit 1; }

      echo "notes.txt is correct"
---

A junior admin left a directory full of files with problematic names and no documentation.
Your job is to correctly handle those files using proper Bash quoting and escaping techniques.

Complete all four tasks below on `rocky-01` as the `laborant` user, working inside `~/quote-test`.

::simple-task
---
:tasks: tasks
:name: verify_four_files
---
#active
**Task 1 — Create four files with special characters in their names.**

Inside `~/quote-test`, create all four of these files (exact names required):
- `report 2024.txt` (space)
- `report 2025.txt` (space)
- `costs [final].csv` (square brackets)
- `price$list.txt` (dollar sign)

#completed
All four files exist with the correct names ✓
::

::simple-task
---
:tasks: tasks
:name: verify_archive_exists
---
#active
**Task 2 — Archive all four files into `special-files.tar.gz`.**

Create `~/quote-test/special-files.tar.gz` containing all four files.
Each file must appear in the archive under its exact original name (with spaces, brackets, and dollar sign intact).

#completed
Archive `special-files.tar.gz` contains all four files with correct names ✓
::

::simple-task
---
:tasks: tasks
:name: verify_summary_file
---
#active
**Task 3 — Generate `summary.txt` using a for loop with double-quoted variable expansion.**

Write a `for` loop that iterates over the four filenames and writes each one to `~/quote-test/summary.txt` (one filename per line, exactly four lines total).
The loop variable must be double-quoted when used so that filenames with spaces are handled as single tokens.

#completed
`summary.txt` contains exactly four lines with the correct filenames ✓
::

::simple-task
---
:tasks: tasks
:name: verify_ansi_file
---
#active
**Task 4 — Create `notes.txt` using ANSI-C quoting.**

Use `printf` with ANSI-C quoting (`$'...'`) to create `~/quote-test/notes.txt` with exactly two lines:
- Line 1: `Status` followed by a **literal tab character** followed by `OK`
- Line 2: `it's ready` (with a real apostrophe)

#completed
`notes.txt` contains a literal tab on line 1 and an apostrophe on line 2 ✓
::

::hint-box
---
:summary: Hint 1 — Task 1 (creating files)
---
Think about what the shell does to unquoted spaces and `$` before `touch` ever sees the arguments. Which quoting form stops all expansion?
::

::hint-box
---
:summary: Hint 2 — Task 1 (dollar sign gotcha)
---
Double quotes expand `$list` as a variable (almost certainly empty), giving you `price.txt` instead of `price$list.txt`. Single quotes suppress all expansion — use them for this filename.
::

::hint-box
---
:summary: Hint 3 — Task 2 (archiving special names)
---
When passing the filenames to `tar`, quote each one the same way you quoted them for `touch`. The shell still expands arguments before passing them to `tar`, so the same quoting rules apply.
::

::hint-box
---
:summary: Hint 4 — Task 3 (for loop with spaces)
---
Structure your loop like:
```bash
for f in 'name with space' 'other name'; do
  echo "$f"
done
```
Notice `"$f"` — without the double quotes the shell would split on spaces and treat each word as a separate argument.
::

::hint-box
---
:summary: Hint 5 — Task 4 (ANSI-C quoting)
---
ANSI-C quoting uses `$'...'` syntax. Inside it, `\t` becomes a real tab and `\'` becomes a real apostrophe. Example:
```bash
printf '%s\n' $'col1\tcol2'
printf '%s\n' $'it\'s ready'
```
Redirect the output to `notes.txt` using `>` and `>>` (or a single `printf` with two format strings).
::