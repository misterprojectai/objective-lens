---
kind: challenge

title: "Fix the Broken PATH: Restore Missing System Directories"

description: |
  The `laborant` user can't run basic system commands — even `ls` is returning "command not found". Something is wrong with the shell environment. Investigate and fix the issue.

categories:
  - linux

tagz:
  - bash
  - path
  - shell
  - environment
  - troubleshooting

difficulty: medium

createdAt: 2025-01-30
updatedAt: 2025-01-30

cover: __static__/cover.png

playground:
  name: rockylinux
  machines:
    - name: rocky-01
      resources:
        cpuCount: 2
        ramSize: 2Gi

tasks:
  init_break_path:
    init: true
    machine: rocky-01
    run: |
      echo 'export PATH=/home/laborant/.local/bin:/home/laborant/bin' >> /home/laborant/.bashrc
      chown laborant:laborant /home/laborant/.bashrc

  verify_path_restored:
    machine: rocky-01
    user: laborant
    run: |
      CONFIGURED_PATH=$(grep -E '^export PATH=' /home/laborant/.bashrc | tail -1 | cut -d= -f2- | tr -d '"'"'"'')
      if echo "$CONFIGURED_PATH" | grep -qE '(^|:)/usr/bin(:|$)'; then
        :
      else
        echo "FAIL: /usr/bin is not in the last PATH export in .bashrc"
        exit 1
      fi
      if echo "$CONFIGURED_PATH" | grep -qE '(^|:)/usr/sbin(:|$)'; then
        :
      else
        echo "FAIL: /usr/sbin is not in the last PATH export in .bashrc"
        exit 1
      fi
    hintcheck: |
      echo "=== Last PATH export in .bashrc ==="
      grep 'PATH' /home/laborant/.bashrc | tail -5
      echo ""
      echo "=== Expected to find /usr/bin and /usr/sbin in the PATH ==="
    failcheck: |
      [ -f /home/laborant/.bashrc ] || {
        echo ".bashrc has been deleted — the environment cannot be recovered. Restart the challenge."
        exit 1
      }
---

The `laborant` user reports that basic commands like `ls`, `cat`, and `grep` all fail with **"command not found"** after logging in. Even simple navigation seems broken. The issue appeared after some recent shell configuration changes.

Investigate the problem on `rocky-01` and restore the shell environment so that standard system commands work again.

::simple-task
---
:tasks: tasks
:name: verify_path_restored
---
#active
The `.bashrc` file must have a `PATH` export that includes both `/usr/bin` and `/usr/sbin`.

#completed
PATH restored ✓
::

::hint-box
---
:summary: Hint 1 — Where to start
---
When commands like `ls` suddenly fail with "command not found", the shell can't locate executables. Start by printing the current value of the variable that controls where the shell searches for programs.
::

::hint-box
---
:summary: Hint 2 — Where the problem lives
---
Check the user's shell startup file for any lines that set or export `PATH`. Look at what directories are actually listed there — something important may be missing.
::

::hint-box
---
:summary: Hint 3 — The exact command to reveal it
---
Run `grep 'PATH' /home/laborant/.bashrc` to see every line that modifies the PATH. Then compare what you see against a healthy RHEL PATH like `/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:$HOME/.local/bin:$HOME/bin`.
::