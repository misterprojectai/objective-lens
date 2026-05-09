---
kind: challenge

title: 'RHCSA Prep: The sudo Command Isn''t What It Seems'

description: |
  The `laborant` user is reporting that something feels wrong when running administrative tasks.
  Commands invoked via `sudo` appear to succeed, but the results are unexpected — files end up in
  the wrong place and critical system binaries seem to behave differently than documented.
  Investigate the shell environment, diagnose the root cause, and fix it permanently.

categories:
  - linux

tagz:
  - rhcsa
  - shell
  - environment
  - path
  - debugging

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
  init_break_environment:
    init: true
    machine: rocky-01
    run: |
      # Create a fake 'sudo' shell function that shadows the real sudo binary
      # It silently invokes the command as the current user (no privilege escalation)
      # and logs the attempt to a hidden file to make it look like it worked
      cat >> /home/laborant/.bashrc << 'EOF'

      # system audit helper - do not remove
      sudo() {
        echo "[sudo] running as $(whoami): $*" >> /tmp/.sudo_audit.log
        "$@"
      }
      export -f sudo
      EOF
      chown laborant:laborant /home/laborant/.bashrc

  verify_sudo_function_removed:
    machine: rocky-01
    user: root
    run: |
      # Check that the shell function definition is gone from .bashrc
      if grep -q 'sudo()' /home/laborant/.bashrc; then
        echo "The sudo() shell function is still defined in .bashrc"
        exit 1
      fi
      # Also check .bash_profile and .profile for good measure
      if grep -q 'sudo()' /home/laborant/.bash_profile 2>/dev/null; then
        echo "The sudo() shell function is still defined in .bash_profile"
        exit 1
      fi
      if grep -q 'sudo()' /home/laborant/.profile 2>/dev/null; then
        echo "The sudo() shell function is still defined in .profile"
        exit 1
      fi
    hintcheck: |
      echo "=== Checking for sudo() function in shell startup files ==="
      grep -n 'sudo' /home/laborant/.bashrc || echo "Not found in .bashrc"
      grep -n 'sudo' /home/laborant/.bash_profile 2>/dev/null || echo "Not found in .bash_profile"
      declare -f sudo 2>/dev/null && echo "sudo() function is ACTIVE in current shell" || echo "No sudo() function in current environment"

  verify_sudo_function_not_active:
    machine: rocky-01
    user: laborant
    run: |
      # Source .bashrc in a non-interactive way — check the function is gone
      # We do this by grepping, not by sourcing (Rocky non-interactive guard)
      if grep -q 'sudo()' /home/laborant/.bashrc; then
        echo "sudo() function still present in .bashrc"
        exit 1
      fi
      # Verify real sudo is reachable: type -P finds binaries only (not functions)
      SUDO_BIN=$(type -P sudo 2>/dev/null)
      if [ -z "$SUDO_BIN" ]; then
        echo "sudo binary not found in PATH"
        exit 1
      fi
      echo "sudo binary is at: $SUDO_BIN"
    hintcheck: |
      echo "=== Current shell function check ==="
      declare -f sudo 2>/dev/null && echo "WARNING: sudo() function is shadowing the binary" || echo "No sudo() function active"
      echo ""
      echo "=== .bashrc sudo-related lines ==="
      grep -n 'sudo' /home/laborant/.bashrc | head -20
      echo ""
      echo "=== type sudo output ==="
      type sudo 2>&1
    failcheck: |
      # Catastrophic: .bashrc was deleted entirely
      if [ ! -f /home/laborant/.bashrc ]; then
        echo ".bashrc has been deleted — the environment cannot be recovered without restarting the challenge"
        exit 1
      fi
---

The `laborant` user is raising an alarm: when they run `sudo <command>`, everything *looks* like
it works — no errors, no permission denied — but the commands are not actually running with root
privileges. Files that should be owned by root end up owned by `laborant`. Privileged operations
complete silently without requiring a password. Something in the shell environment is intercepting
`sudo` before the real binary ever runs.

Investigate the shell environment on `rocky-01`, find what is shadowing the `sudo` command, trace
it to its source, and fix it permanently so that future login sessions behave correctly.

::simple-task
---
:tasks: tasks
:name: verify_sudo_function_removed
---
#active
Remove whatever is shadowing `sudo` from all shell startup files for the `laborant` user.

#completed
The `sudo` shadow has been removed from all startup files ✓
::

::simple-task
---
:tasks: tasks
:name: verify_sudo_function_not_active
---
#active
Confirm that the real `sudo` binary is reachable and no function override remains.

#completed
Real `sudo` binary is accessible and no function override is present ✓
::

::hint-box
---
:summary: Hint 1 — Where to start
---
The RHCSA audit procedure says: before trusting any command, check what the shell *thinks* that
command is. Start with the command that's behaving strangely.
::

::hint-box
---
:summary: Hint 2 — What to check
---
There is more than one way for a shell to intercept a command name: aliases, shell functions, and
`$PATH` ordering. The `type` builtin tells you which mechanism is active. Try `type sudo` in the
`laborant` user's interactive shell.
::

::hint-box
---
:summary: Hint 3 — Finding the source
---
Once you know *what* is intercepting `sudo`, find *where* it is defined. Use:

```bash
grep -n 'sudo' ~/.bashrc ~/.bash_profile ~/.profile 2>/dev/null
```

Shell functions injected via startup files survive across sessions. The fix must remove the
definition from the file — unsetting it in the current session alone is not enough.
::