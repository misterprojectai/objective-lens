---
kind: challenge

title: 'Persist a Custom Binary Directory in $PATH'

description: |
  A custom application has been installed to a non-standard location. Configure the laborant user's environment so the application's directory is permanently available in $PATH for all future login shells.

categories:
  - linux

tagz:
  - bash
  - path
  - shell-environment
  - bash-profile
  - rhcsa

difficulty: medium

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
  init_create_app:
    init: true
    machine: rocky-01
    user: root
    run: |
      mkdir -p /opt/myapp/bin
      cat > /opt/myapp/bin/myapp << 'EOF'
      #!/bin/bash
      echo "myapp v1.0 running"
      EOF
      chmod +x /opt/myapp/bin/myapp
      chown -R laborant:laborant /opt/myapp

  verify_path_persistent:
    machine: rocky-01
    user: laborant
    hintcheck: |
      PROFILE="$HOME/.bash_profile"
      BASHRC="$HOME/.bashrc"

      if grep -q '/opt/myapp/bin' "$BASHRC" && ! grep -q '/opt/myapp/bin' "$PROFILE"; then
        echo "Found /opt/myapp/bin in ~/.bashrc but not in ~/.bash_profile."
        echo "On Rocky Linux 9, login shells read ~/.bash_profile, not ~/.bashrc."
        echo "The PATH change must be in ~/.bash_profile to survive a new login shell."
        exit 0
      fi

      if ! grep -q '/opt/myapp/bin' "$PROFILE"; then
        echo "/opt/myapp/bin is not present in ~/.bash_profile."
        echo "Add an export line to ~/.bash_profile so the setting persists."
        exit 0
      fi

      LOGIN_PATH=$(bash --login -c 'echo $PATH')
      if ! echo "$LOGIN_PATH" | tr ':' '\n' | grep -q '^/opt/myapp/bin$'; then
        echo "~/.bash_profile contains the directory, but a new login shell does not pick it up."
        echo "Check ~/.bash_profile for syntax errors: bash -n ~/.bash_profile"
        exit 0
      fi
    run: |
      PROFILE="$HOME/.bash_profile"

      # The export line must be in ~/.bash_profile
      grep -q '/opt/myapp/bin' "$PROFILE" || {
        echo "/opt/myapp/bin not found in ~/.bash_profile"
        exit 1
      }

      # A new login shell must actually have the directory in PATH
      LOGIN_PATH=$(bash --login -c 'echo $PATH')
      echo "$LOGIN_PATH" | tr ':' '\n' | grep -q '^/opt/myapp/bin$' || {
        echo "/opt/myapp/bin not present in PATH of a new login shell"
        exit 1
      }

  verify_command_found:
    needs:
      - verify_path_persistent
    machine: rocky-01
    user: laborant
    hintcheck: |
      LOGIN_PATH=$(bash --login -c 'echo $PATH')
      if ! echo "$LOGIN_PATH" | tr ':' '\n' | grep -q '^/opt/myapp/bin$'; then
        echo "/opt/myapp/bin is not in the login shell PATH."
        echo "Fix verify_path_persistent first."
        exit 0
      fi
      echo "PATH looks correct. Make sure /opt/myapp/bin/myapp exists and is executable."
    run: |
      # The command must be locatable via PATH in a login shell
      bash --login -c 'type myapp' || {
        echo "myapp not found via PATH in a new login shell"
        exit 1
      }

      FOUND=$(bash --login -c 'type -P myapp')
      [ "$FOUND" = "/opt/myapp/bin/myapp" ] || {
        echo "myapp resolves to '$FOUND', expected /opt/myapp/bin/myapp"
        exit 1
      }
---

A custom application binary has been placed at `/opt/myapp/bin/myapp` on `rocky-01`.

The `laborant` user needs to be able to run `myapp` by name in any future login shell — without specifying the full path and without any manual setup after logging in.

Complete the following tasks on `rocky-01` as the `laborant` user.

::simple-task
---
:tasks: tasks
:name: verify_path_persistent
---
#active
`/opt/myapp/bin` is added to `$PATH` persistently in `~/.bash_profile`, and a new login shell has the directory in its `$PATH`.

#completed
`/opt/myapp/bin` is permanently in `$PATH` for login shells ✓
::

::simple-task
---
:tasks: tasks
:name: verify_command_found
---
#active
Running `type myapp` in a new login shell resolves to `/opt/myapp/bin/myapp`.

#completed
`myapp` is found via `$PATH` in a new login shell ✓
::

::hint-box
---
:summary: Hint 1 — Where to look
---
The shell searches for commands in directories listed in the `$PATH` variable. Inspect your current `$PATH` to understand what's already there and what needs to be added.
::

::hint-box
---
:summary: Hint 2 — Making it permanent
---
A change made with `export PATH=...` in the terminal only lasts for the current session. To make it survive a new login, the export line must be written to a shell initialization file that login shells read automatically.
::

::hint-box
---
:summary: Hint 3 — Which file on Rocky Linux 9
---
On Rocky Linux 9, Bash login shells read `~/.bash_profile` at startup. Add the export line there. Use single quotes around the value so `$PATH` is not expanded immediately: `export PATH=/opt/myapp/bin:$PATH`
::

::hint-box
---
:summary: Hint 4 — Testing without logging out
---
You can test whether your change works without logging out:
```bash
bash --login -c 'echo $PATH | tr ":" "\n"'
```
If `/opt/myapp/bin` appears in the output, the change is persistent.
::