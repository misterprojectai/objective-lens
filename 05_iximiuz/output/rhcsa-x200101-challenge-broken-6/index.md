---
kind: challenge

title: 'RHCSA Prep: Fix the Broken Script That Processes Special-Character Filenames'

description: |
  A shell script that processes files with spaces and special characters in their names is producing "No such file or directory" errors even though the files exist. Diagnose the quoting bug and fix the script so it runs without errors.

categories:
  - linux

tagz:
  - bash
  - quoting
  - shell-scripting
  - special-characters
  - rhcsa-prep

difficulty: hard

createdAt: 2025-01-28
updatedAt: 2025-01-28

cover: __static__/cover.png

playground:
  name: rockylinux
  machines:
    - name: rocky-01
      resources:
        cpuCount: 2
        ramSize: 2Gi

tasks:
  init_break_environment:
    init: true
    machine: rocky-01
    run: |
      mkdir -p /home/laborant/reports
      touch '/home/laborant/reports/report 2024.txt'
      touch '/home/laborant/reports/report 2025.txt'
      touch '/home/laborant/reports/costs [final].csv'
      touch '/home/laborant/reports/price$list.txt'
      printf '#!/bin/bash\n' > /home/laborant/process_reports.sh
      printf 'YEAR=2024\n' >> /home/laborant/process_reports.sh
      printf 'echo "Processing: report $YEAR.txt"\n' >> /home/laborant/process_reports.sh
      printf 'wc -l /home/laborant/reports/report $YEAR.txt\n' >> /home/laborant/process_reports.sh
      printf 'echo "Processing: costs [final].csv"\n' >> /home/laborant/process_reports.sh
      printf 'wc -l /home/laborant/reports/costs [final].csv\n' >> /home/laborant/process_reports.sh
      printf 'echo "Processing: price$list.txt"\n' >> /home/laborant/process_reports.sh
      printf 'wc -l /home/laborant/reports/"price$list.txt"\n' >> /home/laborant/process_reports.sh
      chmod +x /home/laborant/process_reports.sh
      chown -R laborant:laborant /home/laborant/reports /home/laborant/process_reports.sh

  verify_script_runs_clean:
    machine: rocky-01
    user: root
    run: |
      OUTPUT=$(sudo -u laborant bash /home/laborant/process_reports.sh 2>&1)
      echo "$OUTPUT"
      echo "$OUTPUT" | grep -qi "no such file" && exit 1
      echo "$OUTPUT" | grep -qi "cannot access" && exit 1
      echo "$OUTPUT" | grep -qi "ambiguous redirect" && exit 1
      echo "$OUTPUT" | grep -c "Processing:" | grep -q "^3$" || exit 1
      exit 0
    hintcheck: |
      OUTPUT=$(sudo -u laborant bash /home/laborant/process_reports.sh 2>&1)
      echo "--- Script output ---"
      echo "$OUTPUT"
      echo "--- Script content ---"
      cat /home/laborant/process_reports.sh
    failcheck: |
      [ -f /home/laborant/process_reports.sh ] || {
        echo "process_reports.sh has been deleted — restart the challenge"
        exit 1
      }
      [ -d /home/laborant/reports ] || {
        echo "reports directory has been deleted — restart the challenge"
        exit 1
      }

  verify_files_intact:
    machine: rocky-01
    user: root
    run: |
      [ -f '/home/laborant/reports/report 2024.txt' ] || exit 1
      [ -f '/home/laborant/reports/report 2025.txt' ] || exit 1
      [ -f '/home/laborant/reports/costs [final].csv' ] || exit 1
      [ -f '/home/laborant/reports/price$list.txt' ] || exit 1
    hintcheck: |
      echo "Files present in /home/laborant/reports/:"
      ls -1 /home/laborant/reports/
    failcheck: |
      [ -d /home/laborant/reports ] || {
        echo "reports directory is gone — restart the challenge"
        exit 1
      }
---

The `laborant` user has a script at `~/process_reports.sh` that is supposed to process report files sitting in `~/reports/`. When run, the script throws "No such file or directory" errors — even though `ls ~/reports/` clearly shows the files are there.

The files have names like `report 2024.txt`, `costs [final].csv`, and `price$list.txt`.

Investigate why the script fails, fix the quoting bugs in `process_reports.sh`, and make it run without any errors.

::simple-task
---
:tasks: tasks
:name: verify_files_intact
---
#active
All four original files still exist in `~/reports/`

#completed
Files intact ✓
::

::simple-task
---
:tasks: tasks
:name: verify_script_runs_clean
---
#active
`~/process_reports.sh` runs without any "No such file or directory" errors and processes all three files

#completed
Script runs clean ✓
::

::hint-box
---
:summary: Hint 1 — Where to start
---
Run the script and read the error messages carefully. Then open the script and look at each `wc -l` line — compare how the filenames are quoted (or not quoted) against what the shell actually sees.
::

::hint-box
---
:summary: Hint 2 — What to check for each filename
---
There are three separate quoting problems, each involving a different special character: a space (` `), square brackets (`[` `]`), and a dollar sign (`$`). Check each `wc -l` invocation independently and consider which quoting form is appropriate for each case.
::

::hint-box
---
:summary: Hint 3 — The exact command that reveals the shell's view
---
Use `printf '%q ' <argument>` to see the shell-safe representation of what each argument will expand to before the command runs. For the dollar-sign filename in particular, try the difference between `printf '%q\n' "price$list.txt"` and `printf '%q\n' 'price$list.txt'` to see which form preserves the literal `$`.
::