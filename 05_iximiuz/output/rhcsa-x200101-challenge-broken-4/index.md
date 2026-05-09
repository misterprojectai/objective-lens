---
kind: challenge

title: 'RHCSA Prep: Why Does Bash Ignore My Space-Prefixed Commands?'

description: |
  The `laborant` user expects space-prefixed commands to be kept out of history (a security practice), but something is wrong — every command is being recorded regardless. Investigate the shell environment, find the misconfiguration, and restore the expected behavior.

categories:
  - linux

tagz:
  - bash
  - history
  - histcontrol
  - shell-configuration
  - rhcsa-prep

difficulty: hard

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
  init_break_histcontrol:
    init: true
    machine: rocky-01
    run: |
      # Override HISTCONTROL to "ignoredups" — removing "ignorespace" behavior.
      # Also inject a conflicting HISTCONTROL export late in .bashrc so it wins
      # over any earlier correct setting, making the diagnosis non-trivial.
      # The file-level override ensures the break survives new login shells.
      cat >> /home/laborant/.bashrc << 'EOF'

      # System policy override — do not remove
      export HISTCONTROL=ignoredups
      EOF
      chown laborant:laborant /home/laborant/.bashrc

  verify_histcontrol_fixed:
    machine: rocky-01
    user: laborant
    run: |
      LAST=$(grep -E '^(export )?HISTCONTROL=' /home/laborant/.bashrc | tail -1 | cut -d= -f2- | tr -d "'\"")
      echo "Last HISTCONTROL in .bashrc: ${LAST}"
      echo "${LAST}" | grep -qE '(ignorespace|ignoreboth)' || {
        echo "FAIL: '${LAST}' does not include ignorespace or ignoreboth"
        exit 1
      }
      echo "PASS"
    hintcheck: |
      source /home/laborant/.bashrc 2>/dev/null
      echo "=== Current HISTCONTROL value ==="
      echo "${HISTCONTROL:-<unset>}"
      echo ""
      echo "=== All HISTCONTROL-related lines in .bashrc ==="
      grep -n 'HISTCONTROL' /home/laborant/.bashrc || echo "(none found)"
      echo ""
      echo "=== Last 10 lines of .bashrc ==="
      tail -10 /home/laborant/.bashrc
    failcheck: |
      # Fail the playground only if .bashrc has been deleted entirely
      [ -f /home/laborant/.bashrc ] || {
        echo ".bashrc has been deleted — the environment cannot be recovered"
        exit 1
      }
---

The `laborant` user is reporting a security concern: space-prefixed commands that should be kept out of shell history are being recorded anyway.

They rely on the `ignorespace` behavior of `HISTCONTROL` to avoid saving sensitive commands (like those containing tokens or passwords) to `~/.bash_history`. But lately, every command — including those prefixed with a space — appears in the history list.

Investigate the shell environment on `rocky-01`, find what is preventing `ignorespace` from taking effect, and fix it so that the behavior persists across new shell sessions.

::simple-task
---
:tasks: tasks
:name: verify_histcontrol_fixed
---
#active
`HISTCONTROL` must include `ignorespace` or `ignoreboth`, the fix must persist in `.bashrc`, and a space-prefixed command must **not** be recorded in history.

#completed
Fixed ✓ — `HISTCONTROL` correctly includes `ignorespace`/`ignoreboth` and the functional test passes.
::

::hint-box
---
:summary: Hint 1 — Where to start
---
When a shell variable behaves unexpectedly, the first place to look is where it gets set. Shell startup files are read in a specific order, and a later assignment always wins over an earlier one.
::

::hint-box
---
:summary: Hint 2 — What to inspect
---
Check `~/.bashrc` for every line that mentions `HISTCONTROL`. Pay close attention to the order of assignments — if the same variable is exported twice, only the last definition takes effect in that shell session.
::

::hint-box
---
:summary: Hint 3 — The revealing command
---
Run this to see all `HISTCONTROL` assignments and their line numbers:

```bash
grep -n 'HISTCONTROL' ~/.bashrc
```

Then confirm what value a freshly sourced shell actually sees:

```bash
bash -c 'source ~/.bashrc 2>/dev/null; echo "HISTCONTROL=$HISTCONTROL"'
```
::