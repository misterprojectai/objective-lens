# env(1) - Linux manual page

[man7.org](../../../index.html) > Linux > [man-pages](../index.html)

[Linux/UNIX system programming training](http://man7.org/training/)

---

# env(1) — Linux manual page

[NAME](#NAME) | [SYNOPSIS](#SYNOPSIS) | [DESCRIPTION](#DESCRIPTION) | [SCRIPT OPTION HANDLING](#SCRIPT_OPTION_HANDLING) | [NOTES](#NOTES) | [AUTHOR](#AUTHOR) | [REPORTING BUGS](#REPORTING_BUGS) | [COPYRIGHT](#COPYRIGHT) | [SEE ALSO](#SEE_ALSO) | [COLOPHON](#COLOPHON)

  

_ENV_(1)                        User Commands                        _ENV_(1)

## [](#NAME)NAME         [top](#top_of_page)

       env - run a program in a modified environment

## [](#SYNOPSIS)SYNOPSIS         [top](#top_of_page)

       **env** \[_OPTION_\]... \[_\-_\] \[_NAME=VALUE_\]... \[_COMMAND_ \[_ARG_\]...\]

## [](#DESCRIPTION)DESCRIPTION         [top](#top_of_page)

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

       **\--help** display this help and exit

       **\--version**
              output version information and exit

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

## [](#SCRIPT_OPTION_HANDLING)SCRIPT OPTION HANDLING         [top](#top_of_page)

       The **\-S** option allows specifying multiple arguments in a script.
       Running a script named **1.pl** containing the following first line:

              #!/usr/bin/env -S perl -w -T
              ...

       Will execute **perl -w -T 1.pl**

       Without the **'-S'** parameter the script will likely fail with:

              /usr/bin/env: 'perl -w -T': No such file or directory

       See the full documentation for more details.

## [](#NOTES)NOTES         [top](#top_of_page)

       POSIX's [exec(3p)](../man3/exec.3p.html) pages says:
              "many existing applications wrongly assume that they start
              with certain signals set to the default action and/or
              unblocked.... Therefore, it is best not to block or ignore
              signals across execs without explicit reason to do so, and
              especially not to block signals across execs of arbitrary
              (not closely cooperating) programs."

## [](#AUTHOR)AUTHOR         [top](#top_of_page)

       Written by Richard Mlynarik, David MacKenzie, and Assaf Gordon.

## [](#REPORTING_BUGS)REPORTING BUGS         [top](#top_of_page)

       Report bugs to: bug-coreutils@gnu.org
       GNU coreutils home page: <[https://www.gnu.org/software/coreutils/](https://www.gnu.org/software/coreutils/)\>
       General help using GNU software: <[https://www.gnu.org/gethelp/](https://www.gnu.org/gethelp/)\>
       Report any translation bugs to
       <[https://translationproject.org/team/](https://translationproject.org/team/)\>

## [](#COPYRIGHT)COPYRIGHT         [top](#top_of_page)

       Copyright © 2025 Free Software Foundation, Inc.  License GPLv3+:
       GNU GPL version 3 or later <[https://gnu.org/licenses/gpl.html](https://gnu.org/licenses/gpl.html)\>.
       This is free software: you are free to change and redistribute it.
       There is NO WARRANTY, to the extent permitted by law.

## [](#SEE_ALSO)SEE ALSO         [top](#top_of_page)

       [sigaction(2)](../man2/sigaction.2.html), [sigprocmask(2)](../man2/sigprocmask.2.html), [signal(7)](../man7/signal.7.html)

       Full documentation <[https://www.gnu.org/software/coreutils/env](https://www.gnu.org/software/coreutils/env)\>
       or available locally via: info '(coreutils) env invocation'

## [](#COLOPHON)COLOPHON         [top](#top_of_page)

       This page is part of the _coreutils_ (basic file, shell and text
       manipulation utilities) project.  Information about the project
       can be found at ⟨[http://www.gnu.org/software/coreutils/](http://www.gnu.org/software/coreutils/)⟩.  If you
       have a bug report for this manual page, see
       ⟨[http://www.gnu.org/software/coreutils/](http://www.gnu.org/software/coreutils/)⟩.  This page was obtained
       from the tarball coreutils-9.9.tar.xz fetched from
       ⟨[http://ftp.gnu.org/gnu/coreutils/](http://ftp.gnu.org/gnu/coreutils/)⟩ on 2026-01-16.  If you
       discover any rendering problems in this HTML version of the page,
       or you believe there is a better or more up-to-date source for the
       page, or you have corrections or improvements to the information
       in this COLOPHON (which is _not_ part of the original manual page),
       send a mail to man-pages@man7.org

GNU coreutils 9.9             November 2025                        _ENV_(1)

---

Pages that refer to this page: [pmpython(1)](../man1/pmpython.1.html),  [environ(7)](../man7/environ.7.html)

---

---

HTML rendering created 2026-01-16 by [Michael Kerrisk](https://man7.org/mtk/index.html), author of [_The Linux Programming Interface_](https://man7.org/tlpi/).

For details of in-depth **Linux/UNIX system programming training courses** that I teach, look [here](https://man7.org/training/).

Hosting by [jambit GmbH](https://www.jambit.com/index_en.html).

[![Cover of TLPI](https://man7.org/tlpi/cover/TLPI-front-cover-vsmall.png)](https://man7.org/tlpi/)

---

[![Web Analytics Made Easy -
StatCounter](https://c.statcounter.com/7422636/0/9b6714ff/1/)](https://statcounter.com/ "Web Analytics
Made Easy - StatCounter")