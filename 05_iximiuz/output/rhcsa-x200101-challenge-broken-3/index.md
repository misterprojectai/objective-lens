---
kind: challenge

title: 'Fix the Broken $PATH: Custom Commands No Longer Found After Login'

description: |
  The `laborant` user's custom directory `/opt/tools/bin` was working fine last week.
  Now, after every login, the commands in that directory are not found — even though
  they worked in the previous session. Someone touched the shell profile and now the
  $PATH change doesn't survive a new login shell.

categories:
  - linux

tagz:
  - bash
  - path
  - shell-profile
  - bash-profile
  - environment

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
  init_setup_tools_dir:
    init: true
    machine: rocky-01
    run: |
      # Create the custom tools directory and a fake binary
      mkdir -p /opt/tools/bin
      cat > /opt/tools/bin/greet << 'EOF'
      #!/bin/bash
      echo "Hello from /opt/tools/bin/greet"
      EOF
      chmod +x /opt/tools/bin/greet

      # Set up a legitimate-looking ~/.bash_profile that has the PATH export
      # BUT write it to ~/.bashrc instead (the wrong file for login shells)
      # AND make ~/.bash_profile exist but silently broken by redirecting to /dev/null
      cat > /home/laborant/.bash_profile << 'EOF'
      # .bash_profile — loaded by login shells
      # Source user environment
      if [ -f ~/.bashrc ]; then
        source ~/.bashrc
      fi
      export PATH=/opt/tools/bin:$PATH >> /dev/null 2>&1
      EOF
      chown laborant:laborant /home/laborant/.bash_profile

  verify_path_persists:
    machine: rocky-01
    run: |
      # Check /opt/tools/bin is in bash_profile with a correct export (no redirection)
      grep -E '^export PATH=.*\/opt\/tools\/bin.*\$PATH\s*$' /home/laborant/.bash_profile || {
        echo "FAIL: /opt/tools/bin is not correctly exported in ~/.bash_profile"
        echo "The export line must not have any redirection or extra tokens after \$PATH"
        exit 1
      }

      # Make sure the export line doesn't have >> or > on the same line
      if grep -E '^export PATH=.*\/opt\/tools\/bin' /home/laborant/.bash_profile | grep -qE '>'; then
        echo "FAIL: The export line has a redirection (>> or >) — it is broken"
        exit 1
      fi

      # Verify a login shell actually picks up /opt/tools/bin
      result=$(sudo -u laborant bash --login -c 'echo $PATH')
      echo "$result" | grep -q '/opt/tools/bin' || {
        echo "FAIL: A new login shell for laborant does not have /opt/tools/bin in \$PATH"
        echo "Current PATH in login shell: $result"
        exit 1
      }

      # Verify the greet command is found in a login shell
      sudo -u laborant bash --login -c 'type greet' > /dev/null 2>&1 || {
        echo "FAIL: 'greet' command is not found in a new login shell"
        exit 1
      }
    hintcheck: |
      echo "=== Contents of ~/.bash_profile ==="
      cat /home/laborant/.bash_profile
      echo ""
      echo "=== Login shell PATH ==="
      sudo -u laborant bash --login -c 'echo $PATH | tr ":" "\n"' 2>/dev/null || echo "(login shell failed)"
      echo ""
      echo "=== Checking for /opt/tools/bin ==="
      grep -n 'tools' /home/laborant/.bash_profile || echo "(not found)"
    failcheck: |
      [ -f /home/laborant/.bash_profile ] || {
        echo "FATAL: ~/.bash_profile has been deleted — the challenge cannot be solved"
        exit 1
      }
---

The `laborant` user reports that the `greet` command from `/opt/tools/bin` was working
fine in a previous session, but **after every new login the command is not found**:

```
-bash: greet: command not found
```

The user remembers that `/opt/tools/bin` was added to `$PATH` somewhere in the shell
profile files. Something about that configuration is now broken.

Investigate the shell startup files on `rocky-01`, diagnose the exact problem, and fix it
so that `/opt/tools/bin` is correctly added to `$PATH` in every new login shell.

::simple-task
---
:tasks: tasks
:name: verify_path_persists
---
#active
`/opt/tools/bin` must be correctly exported in `~/.bash_profile` and present in `$PATH` for every new login shell.

#completed
Fixed ✓ — `/opt/tools/bin` is correctly in `$PATH` for login shells.
::

::hint-box
---
:summary: Hint 1 — Where to start
---
Shell startup files are loaded in a specific order depending on whether the shell is a
login shell or an interactive non-login shell. Start by looking at which files exist in
the `laborant` home directory and what they contain.
::

::hint-box
---
:summary: Hint 2 — Which file is responsible for login shells
---
On Rocky Linux (and RHEL), `~/.bash_profile` is sourced by **login shells**.
`~/.bashrc` is sourced by **interactive non-login shells**. Check whether the `PATH`
export is in the right file.
::

::hint-box
---
:summary: Hint 3 — Look very carefully at the export line
---
Even if the export line is in the correct file, it may be syntactically valid Bash but
functionally broken. Read every character on the line that sets `PATH`. Shell
redirections (`>`, `>>`) appended to an `export` statement silently misdirect the
output — the variable is never actually set.
::