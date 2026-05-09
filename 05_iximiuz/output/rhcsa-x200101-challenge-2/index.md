---
kind: challenge

title: 'Fix a Broken $PATH So Commands Work Again'

description: |
  The laborant user's PATH has been corrupted, causing common commands to fail with "command not found". Diagnose and fix the broken PATH so that standard system commands work again.

categories:
  - linux

tagz:
  - bash
  - path
  - shell
  - troubleshooting

difficulty: easy

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
  init_break_path:
    machine: rocky-01
    init: true
    run: |
      # Overwrite PATH in laborant's .bashrc so it is permanently broken
      cat >> /home/laborant/.bashrc << 'EOF'

      # DO NOT REMOVE - system configuration
      export PATH=/home/laborant/bin
      EOF

  verify_ls_works:
    machine: rocky-01
    user: laborant
    hintcheck: |
      echo "Try: echo \$PATH"
      echo "Check whether /usr/bin is present in the output."
    run: |
      bash -i -c 'ls /tmp' 2>/dev/null || exit 1

  verify_path_has_usr_bin:
    machine: rocky-01
    user: laborant
    hintcheck: |
      echo "The PATH must include /usr/bin."
      echo "Check your ~/.bashrc for any export PATH= lines."
    run: |
      PATH_VAL=$(bash -i -c 'echo $PATH' 2>/dev/null)
      echo "$PATH_VAL" | grep -q '/usr/bin' || exit 1

  verify_path_has_usr_sbin:
    machine: rocky-01
    user: laborant
    hintcheck: |
      echo "The PATH must also include /usr/sbin."
      echo "Both /usr/bin and /usr/sbin are expected in a healthy RHEL PATH."
    run: |
      PATH_VAL=$(bash -i -c 'echo $PATH' 2>/dev/null)
      echo "$PATH_VAL" | grep -q '/usr/sbin' || exit 1

  verify_fix_is_persistent:
    machine: rocky-01
    user: laborant
    hintcheck: |
      echo "The fix must survive a new login shell."
      echo "Set the correct PATH in ~/.bashrc so it persists across sessions."
    run: |
      # Check that a brand new login shell can still find ls and id
      bash --login -c 'ls /tmp && id' 2>/dev/null || exit 1
---

The `laborant` user's `~/.bashrc` has been modified and now sets a broken `$PATH`, causing standard commands like `ls`, `cat`, and `id` to fail with `command not found` in every new shell session.

Fix the `PATH` permanently so that:
- Standard system commands (`ls`, `cat`, `id`, etc.) work in new shell sessions
- `/usr/bin` and `/usr/sbin` are present in `$PATH`
- The fix persists across logins (i.e., survives opening a new terminal)

Complete the task on **rocky-01** as the `laborant` user.

::simple-task
---
:tasks: tasks
:name: verify_ls_works
---
#active
`ls` works in a new shell session for the `laborant` user

#completed
`ls` works correctly ✓
::

::simple-task
---
:tasks: tasks
:name: verify_path_has_usr_bin
---
#active
`/usr/bin` is present in `$PATH` for the `laborant` user

#completed
`/usr/bin` found in `$PATH` ✓
::

::simple-task
---
:tasks: tasks
:name: verify_path_has_usr_sbin
---
#active
`/usr/sbin` is present in `$PATH` for the `laborant` user

#completed
`/usr/sbin` found in `$PATH` ✓
::

::simple-task
---
:tasks: tasks
:name: verify_fix_is_persistent
---
#active
The PATH fix persists in a new login shell

#completed
Fix is persistent across login sessions ✓
::

::hint-box
---
:summary: Hint 1 — Where to look
---
Shell environment variables set at login come from configuration files in the user's home directory. Start by examining what's in `~/.bashrc`.
::

::hint-box
---
:summary: Hint 2 — Diagnosing the problem
---
Run `echo $PATH` in your current session. If you see only `/home/laborant/bin` or similar, the PATH has been overwritten. Look for a line near the bottom of `~/.bashrc` that starts with `export PATH=`.
::

::hint-box
---
:summary: Hint 3 — Fixing the PATH
---
Remove or edit the broken `export PATH=` line in `~/.bashrc`. A healthy Rocky Linux 9 PATH for a regular user looks like:

```
/home/laborant/.local/bin:/home/laborant/bin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin
```

You can restore it with:
```bash
export PATH=/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:$HOME/.local/bin:$HOME/bin
```

Then make it permanent by updating `~/.bashrc`.
::