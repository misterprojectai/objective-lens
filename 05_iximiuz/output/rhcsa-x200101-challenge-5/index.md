---
kind: challenge

title: 'Audit the Shell Environment: Detect a Shadowed Command'

description: |
  A system administrator must verify the shell environment is clean before performing privileged tasks. Practice detecting and resolving command aliases and shell function overrides that can silently hijack administrative commands.

categories:
  - linux

tagz:
  - shell
  - bash
  - environment
  - rhcsa
  - audit

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
  init_poison_environment:
    machine: rocky-01
    init: true
    run: |
      # Add a dangerous alias for sudo in laborant's bashrc
      echo "alias sudo='echo ALIAS_TRIGGERED && sudo'" >> /home/laborant/.bashrc

      # Add a shell function that shadows useradd
      cat >> /home/laborant/.bashrc << 'EOF'
      useradd() {
        echo "FUNCTION_TRIGGERED: useradd blocked"
      }
      export -f useradd
      EOF

      # Ensure changes are owned correctly
      chown laborant:laborant /home/laborant/.bashrc

  verify_alias_removed:
    machine: rocky-01
    user: laborant
    hintcheck: |
      if grep -q "alias sudo=" /home/laborant/.bashrc; then
        echo "The alias definition is still present in ~/.bashrc."
        echo "You need to remove the line that defines the sudo alias from the file."
      else
        echo "The alias is gone from ~/.bashrc - good!"
        echo "Make sure it's also not defined in any other sourced file."
      fi
    run: |
      # Check the alias is not in any startup file
      grep -r 'alias sudo=' /home/laborant/.bashrc \
        /home/laborant/.bash_profile \
        /home/laborant/.bash_login 2>/dev/null && exit 1

      # Verify the alias is not active in a new shell session
      bash --login -c 'alias sudo 2>&1' | grep -q 'alias sudo=' && exit 1

      exit 0

  verify_function_removed:
    machine: rocky-01
    user: laborant
    hintcheck: |
      if grep -q 'useradd()' /home/laborant/.bashrc; then
        echo "The useradd function definition is still present in ~/.bashrc."
        echo "Remove the entire shell function block from the file."
      else
        echo "The function definition looks gone from ~/.bashrc."
        echo "Check whether it's still active in a new shell: bash --login -c 'declare -f useradd'"
      fi
    run: |
      # Check no function definition exists in startup files
      grep -r 'useradd()' /home/laborant/.bashrc \
        /home/laborant/.bash_profile \
        /home/laborant/.bash_login 2>/dev/null && exit 1

      grep -r 'export -f useradd' /home/laborant/.bashrc \
        /home/laborant/.bash_profile \
        /home/laborant/.bash_login 2>/dev/null && exit 1

      # Verify no function is active in a new login shell
      bash --login -c 'declare -f useradd' 2>/dev/null | grep -q 'useradd' && exit 1

      exit 0

  verify_path_contains_usr_bin:
    machine: rocky-01
    user: laborant
    hintcheck: |
      CURRENT_PATH=$(bash --login -c 'echo $PATH')
      echo "Current PATH in a new login shell: $CURRENT_PATH"
      echo ""
      echo "Check whether /usr/bin is present:"
      echo "$CURRENT_PATH" | tr ':' '\n' | grep -c '^/usr/bin$'
    run: |
      # Check /usr/bin is present in PATH for a new login shell
      COUNT=$(bash --login -c 'echo $PATH | tr ":" "\n" | grep -c "^/usr/bin$"')
      [ "$COUNT" -lt 1 ] && echo "/usr/bin missing from PATH" && exit 1
      exit 0
---

The `laborant` user's shell environment on `rocky-01` has been tampered with — a dangerous `sudo` alias and a `useradd` shell function have been injected into `~/.bashrc`, and you must clean them up before any administrative work can proceed safely.

Complete the following tasks on `rocky-01` as the `laborant` user.

::simple-task
---
:tasks: tasks
:name: verify_alias_removed
---
#active
Remove the `sudo` alias from `~/.bashrc` so it is no longer active in new login shell sessions.

#completed
The `sudo` alias has been removed ✓
::

::simple-task
---
:tasks: tasks
:name: verify_function_removed
---
#active
Remove the `useradd` shell function from `~/.bashrc` so it no longer shadows the real `useradd` binary in new login shell sessions.

#completed
The `useradd` shell function has been removed ✓
::

::simple-task
---
:tasks: tasks
:name: verify_path_contains_usr_bin
---
#active
Confirm that `/usr/bin` remains present in `$PATH` for new login shell sessions (do not break the standard `$PATH`).

#completed
`/usr/bin` is present in `$PATH` ✓
::

::hint-box
---
:summary: Hint 1 — How to detect what's wrong
---
Use `type sudo` and `declare -f useradd` in an interactive session to confirm whether a command is aliased or shadowed by a shell function.
::

::hint-box
---
:summary: Hint 2 — Where to look
---
The injected definitions live in `~/.bashrc`. Open it with a text editor and look for lines containing `alias sudo=` and a `useradd()` function block.
::

::hint-box
---
:summary: Hint 3 — What to remove
---
Delete the `alias sudo='...'` line and the entire `useradd() { ... }` function block including the `export -f useradd` line. Save the file, then open a new shell to verify the changes took effect.
::

::hint-box
---
:summary: Hint 4 — How to verify your fix
---
In a new shell session, run:
```bash
alias sudo 2>&1
declare -f useradd
echo $PATH | tr ':' '\n' | grep '^/usr/bin$'
```
The first two commands should produce no output. The third should print `/usr/bin`.
::