---
kind: challenge

title: 'Get Help: Use Shell Help Tools to Answer Questions About Commands'

description: |
  Practice using built-in shell help tools — man, whatis, type, and apropos — to locate information about commands without leaving the terminal.

categories:
  - linux

tagz:
  - rhcsa
  - man-pages
  - shell-help
  - command-line

difficulty: easy

createdAt: 2025-07-31
updatedAt: 2025-07-31

cover: __static__/cover.png

playground:
  name: rockylinux
  machines:
    - name: rocky-01
      resources:
        cpuCount: 2
        ramSize: 2Gi

tasks:
  verify_whatis_output:
    machine: rocky-01
    user: laborant
    run: |
      # Check that the learner wrote the whatis output for 'passwd' to the file
      [ -f /home/laborant/whatis-passwd.txt ] || exit 1
      grep -qi 'passwd' /home/laborant/whatis-passwd.txt || exit 1
      # The output must contain a section number (e.g., "(1)" or "(5)")
      grep -qE '\([0-9]+\)' /home/laborant/whatis-passwd.txt || exit 1
    hintcheck: |
      if [ ! -f /home/laborant/whatis-passwd.txt ]; then
        echo "The file /home/laborant/whatis-passwd.txt does not exist yet."
        echo "Run the whatis command and redirect its output to that file."
      else
        echo "File exists. Check its contents with: cat ~/whatis-passwd.txt"
        echo "It should contain the whatis output for the 'passwd' command."
      fi

  verify_command_type:
    machine: rocky-01
    user: laborant
    run: |
      # Check that the learner wrote the type output for 'cd' to the file
      [ -f /home/laborant/type-cd.txt ] || exit 1
      grep -qi 'builtin' /home/laborant/type-cd.txt || exit 1
    hintcheck: |
      if [ ! -f /home/laborant/type-cd.txt ]; then
        echo "The file /home/laborant/type-cd.txt does not exist yet."
        echo "Use the 'type' command to check what 'cd' is and save the result."
      else
        echo "File exists but content may be wrong."
        echo "Run: type cd"
        echo "The output should mention 'builtin'."
      fi

  verify_mandb_updated:
    machine: rocky-01
    user: root
    run: |
      # mandb should have been run (the database timestamp should be recent)
      # We check that the man page database exists and is populated
      ls /var/cache/man/ 2>/dev/null | grep -q . || exit 1
      # whatis should now work correctly
      whatis ls 2>/dev/null | grep -qiE 'list' || exit 1
    hintcheck: |
      echo "The man page database may need to be rebuilt."
      echo "Try running: sudo mandb"
      echo "Then verify with: whatis ls"
---

The `laborant` user needs to demonstrate proficiency with shell help tools on `rocky-01`.

Complete the following three tasks on `rocky-01`.

**Task 1:** Run `whatis passwd` and save its output to `/home/laborant/whatis-passwd.txt`.

**Task 2:** Run `type cd` and save its output to `/home/laborant/type-cd.txt`.

**Task 3:** Rebuild the man page database so that `whatis ls` returns a description containing the word "list".

::simple-task
---
:tasks: tasks
:name: verify_whatis_output
---
#active
`/home/laborant/whatis-passwd.txt` exists and contains the `whatis passwd` output (including a section number like `(1)` or `(5)`)

#completed
whatis output saved correctly ✓
::

::simple-task
---
:tasks: tasks
:name: verify_command_type
---
#active
`/home/laborant/type-cd.txt` exists and contains output showing that `cd` is a shell builtin

#completed
type output saved correctly ✓
::

::simple-task
---
:tasks: tasks
:name: verify_mandb_updated
---
#active
The man page database is up to date and `whatis ls` returns a description that includes the word "list"

#completed
Man page database rebuilt ✓
::

::hint-box
---
:summary: Hint 1 — Saving command output to a file
---
The shell's redirection operator `>` writes standard output to a file. For example: `somecommand > ~/output.txt`
::

::hint-box
---
:summary: Hint 2 — Finding what type of thing a command is
---
The `type` built-in tells you whether a name resolves to a shell builtin, an alias, a function, or an external file on disk.
::

::hint-box
---
:summary: Hint 3 — Fixing a broken whatis database
---
`whatis` reads from an indexed database. If it returns "nothing appropriate", the database is stale or missing. There is a command specifically for rebuilding this database — check its man page or try `apropos mandb`.
::

::hint-box
---
:summary: Hint 4 — Rebuilding the man page database
---
The command `mandb` regenerates the `whatis` database. You will need elevated privileges to run it: `sudo mandb`
::