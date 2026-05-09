---
kind: challenge

title: 'Shell History: Delete Sensitive Commands and Prevent Future Logging'

description: |
  Practice managing Bash history by removing a specific sensitive command from history and configuring the shell to prevent space-prefixed commands from being saved.

categories:
  - linux

tagz:
  - bash
  - shell-history
  - histcontrol
  - rhcsa

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
  init_populate_history:
    machine: rocky-01
    user: laborant
    init: true
    run: |
      # Populate ~/.bash_history with some realistic commands including a "sensitive" one
      cat >> /home/laborant/.bash_history << 'EOF'
      ls -la /etc
      cat /etc/hostname
      df -h
      echo "supersecret-api-key=abc123XYZ"
      uptime
      whoami
      ps aux
      EOF
      # Load history into memory for the session
      history -r /home/laborant/.bash_history 2>/dev/null || true

  verify_sensitive_command_removed:
    machine: rocky-01
    user: laborant
    run: |
      # Check that the sensitive command is NOT in ~/.bash_history
      if grep -q 'supersecret-api-key' /home/laborant/.bash_history; then
        echo "The sensitive command is still present in ~/.bash_history"
        exit 1
      fi
      echo "Sensitive command has been removed from ~/.bash_history"
    hintcheck: |
      echo "Check the file directly: grep 'supersecret-api-key' ~/.bash_history"
      echo "Make sure you have written the changes to disk after deleting the entry."

  verify_histcontrol_set:
    machine: rocky-01
    user: laborant
    run: |
      # Check that HISTCONTROL is set to include ignorespace or ignoreboth in ~/.bashrc
      if ! grep -E 'HISTCONTROL.*(ignorespace|ignoreboth)' /home/laborant/.bashrc; then
        echo "HISTCONTROL with ignorespace or ignoreboth not found in ~/.bashrc"
        exit 1
      fi
      # Verify it is actually active in a new shell
      val=$(bash -i -c 'echo $HISTCONTROL' 2>/dev/null)
      if [[ "$val" != *ignorespace* ]] && [[ "$val" != *ignoreboth* ]]; then
        echo "HISTCONTROL is set in ~/.bashrc but does not take effect in a new shell session (got: '$val')"
        exit 1
      fi
      echo "HISTCONTROL is correctly configured: $val"
    hintcheck: |
      echo "Check: grep HISTCONTROL ~/.bashrc"
      echo "The value must include 'ignorespace' or 'ignoreboth'."
      echo "It must be exported or set in ~/.bashrc so a new shell session picks it up."

  verify_history_written:
    machine: rocky-01
    user: laborant
    needs:
      - verify_sensitive_command_removed
    run: |
      # Confirm that other history entries (non-sensitive) are still present
      if ! grep -q 'uptime\|whoami\|ps aux\|df -h' /home/laborant/.bash_history; then
        echo "~/.bash_history appears to be empty or missing expected entries"
        echo "Only the sensitive command should have been removed, not the entire history"
        exit 1
      fi
      echo "History file looks correct — sensitive entry removed, other entries preserved"
    hintcheck: |
      echo "Use 'history -d <number>' to delete just the sensitive entry, not 'history -c' which clears everything."
      echo "After deleting, run 'history -w' to write changes to ~/.bash_history."
---

A junior sysadmin accidentally ran a command containing a secret API key, and the shell history now contains the string `supersecret-api-key=abc123XYZ`. You need to clean it up and make sure space-prefixed commands won't be logged in future sessions.

Complete the following tasks on `rocky-01` as the `laborant` user:

1. Remove the command containing `supersecret-api-key=abc123XYZ` from `~/.bash_history` (leave all other history entries intact).
2. Configure the shell so that commands prefixed with a space are not saved to history, and make this setting persistent across new login sessions.

::simple-task
---
:tasks: tasks
:name: verify_sensitive_command_removed
---
#active
The line containing `supersecret-api-key=abc123XYZ` must not appear in `~/.bash_history`.

#completed
Sensitive command removed from `~/.bash_history` ✓
::

::simple-task
---
:tasks: tasks
:name: verify_histcontrol_set
---
#active
`HISTCONTROL` must include `ignorespace` or `ignoreboth` in `~/.bashrc` and take effect in new shell sessions.

#completed
`HISTCONTROL` is correctly configured ✓
::

::simple-task
---
:tasks: tasks
:name: verify_history_written
---
#active
Other history entries (`uptime`, `whoami`, etc.) must still be present in `~/.bash_history` — only the sensitive line should be gone.

#completed
History file is intact with only the sensitive entry removed ✓
::

::hint-box
---
:summary: Hint 1 — Finding the entry
---
Use `history` to display the numbered list of commands. Look for the line containing the secret string. Note its number.
::

::hint-box
---
:summary: Hint 2 — Removing a single history entry
---
`history -d <number>` removes a single entry by its line number. After deleting, write the updated history to disk.
::

::hint-box
---
:summary: Hint 3 — Writing history to disk
---
In-memory changes to history are not saved automatically. Use `history -w` to flush the current in-memory history to `~/.bash_history`.
::

::hint-box
---
:summary: Hint 4 — Preventing space-prefixed commands from being logged
---
Set `HISTCONTROL=ignoreboth` (or `ignorespace`) in `~/.bashrc` and source the file so the setting is active immediately. The `ignorespace` value tells Bash to skip saving any command that begins with a space character.
::