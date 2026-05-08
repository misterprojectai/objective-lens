<!-- Source: 01_normalize/input/env-1.md | Cleaned: 2026-05-07 -->

# env(1) - Linux manual page

# env(1) — Linux manual page

env - run a program in a modified environment

**env** \[_OPTION_\]... \[_\-_\] \[_NAME=VALUE_\]... \[_COMMAND_ \[_ARG_\]...\]

Set each NAME to VALUE in the environment and run COMMAND.

Mandatory arguments to long options are mandatory for short
       options too.

**\-a**, **\--argv0**\=_ARG_
              pass ARG as the zeroth argument of COMMAND

**\-i**, **\--ignore-environment**
              start with an empty environment

**\-0**, **\--null**
              end each output line with NUL, not newline

**\-u**, **\--unset**\=_NAME_
              remove variable from the environment

**\-C**, **\--chdir**\=_DIR_
              change working directory to DIR

**\-S**, **\--split-string**\=_S_
              process and split S into separate arguments; used to pass
              multiple arguments on shebang lines

**\--block-signal**\[=_SIG_\]
              block delivery of SIG signal(s) to COMMAND

**\--default-signal**\[=_SIG_\]
              reset handling of SIG signal(s) to the default

**\--ignore-signal**\[=_SIG_\]
              set handling of SIG signal(s) to do nothing

**\--list-signal-handling**
              list non default signal handling to standard error

**\-v**, **\--debug**
              print verbose information for each processing step

A mere - implies **\-i**.  If no COMMAND, print the resulting
       environment.

SIG may be a signal name like 'PIPE', or a signal number like
       '13'.  Without SIG, all known signals are included.  Multiple
       signals can be comma-separated.  An empty SIG argument is a no-op.

**Exit status:**
       125    if the env command itself fails

126    if COMMAND is found but cannot be invoked

127    if COMMAND cannot be found

-      the exit status of COMMAND otherwise

The **\-S** option allows specifying multiple arguments in a script.
       Running a script named **1.pl** containing the following first line:

#!/usr/bin/env -S perl -w -T
              ...

Will execute **perl -w -T 1.pl**

Without the **'-S'** parameter the script will likely fail with:

/usr/bin/env: 'perl -w -T': No such file or directory

POSIX's [exec(3p)](../man3/exec.3p.html) pages says:
              "many existing applications wrongly assume that they start
              with certain signals set to the default action and/or
              unblocked.... Therefore, it is best not to block or ignore
              signals across execs without explicit reason to do so, and
              especially not to block signals across execs of arbitrary
              (not closely cooperating) programs."

[sigaction(2)](../man2/sigaction.2.html), [sigprocmask(2)](../man2/sigprocmask.2.html), [signal(7)](../man7/signal.7.html)