# tail(1) - Linux manual page

[man7.org](../../../index.html) > Linux > [man-pages](../index.html)

[Linux/UNIX system programming training](http://man7.org/training/)

---

# tail(1) — Linux manual page

[NAME](#NAME) | [SYNOPSIS](#SYNOPSIS) | [DESCRIPTION](#DESCRIPTION) | [AUTHOR](#AUTHOR) | [REPORTING BUGS](#REPORTING_BUGS) | [COPYRIGHT](#COPYRIGHT) | [SEE ALSO](#SEE_ALSO) | [COLOPHON](#COLOPHON)

  

_TAIL_(1)                       User Commands                       _TAIL_(1)

## [](#NAME)NAME         [top](#top_of_page)

       tail - output the last part of files

## [](#SYNOPSIS)SYNOPSIS         [top](#top_of_page)

       **tail** \[_OPTION_\]... \[_FILE_\]...

## [](#DESCRIPTION)DESCRIPTION         [top](#top_of_page)

       Print the last 10 lines of each FILE to standard output.  With
       more than one FILE, precede each with a header giving the file
       name.

       With no FILE, or when FILE is -, read standard input.

       Mandatory arguments to long options are mandatory for short
       options too.

       **\-c**, **\--bytes**\=_\[+\]NUM_
              output the last NUM bytes; or use **\-c** +NUM to output
              starting with byte NUM of each file

       **\-f**, **\--follow**\[=_{name|descriptor}_\]
              output appended data as the file grows; an absent option
              argument means 'descriptor'

       **\-F**     same as **\--follow**\=_name_ **\--retry**

       **\-n**, **\--lines**\=_\[+\]NUM_
              output the last NUM lines, instead of the last 10; or use
              **\-n** +NUM to skip NUM-1 lines at the start

       **\--max-unchanged-stats**\=_N_
              with **\--follow**\=_name_, reopen a FILE which has not changed
              size after N (default 5) iterations to see if it has been
              unlinked or renamed (this is the usual case of rotated log
              files); with inotify, this option is rarely useful

       **\--pid**\=_PID_
              with **\-f**, exit after PID no longer exists; can be repeated
              to watch multiple processes

       **\-q**, **\--quiet**, **\--silent**
              never output headers giving file names

       **\--retry**
              keep trying to open a file if it is inaccessible

       **\-s**, **\--sleep-interval**\=_N_
              with **\-f**, sleep for approximately N seconds (default 1.0)
              between iterations; with inotify and **\--pid**\=_P_, check process
              P at least once every N seconds

       **\-v**, **\--verbose**
              always output headers giving file names

       **\-z**, **\--zero-terminated**
              line delimiter is NUL, not newline

       **\--help** display this help and exit

       **\--version**
              output version information and exit

       NUM may have a multiplier suffix: b 512, kB 1000, K 1024, MB
       1000\*1000, M 1024\*1024, GB 1000\*1000\*1000, G 1024\*1024\*1024, and
       so on for T, P, E, Z, Y, R, Q.  Binary prefixes can be used, too:
       KiB=K, MiB=M, and so on.

       With **\--follow** (**\-f**), tail defaults to following the file
       descriptor, which means that even if a tail'ed file is renamed,
       tail will continue to track its end.  This default behavior is not
       desirable when you really want to track the actual name of the
       file, not the file descriptor (e.g., log rotation).  Use
       **\--follow**\=_name_ in that case.  That causes tail to track the named
       file in a way that accommodates renaming, removal and creation.

## [](#AUTHOR)AUTHOR         [top](#top_of_page)

       Written by Paul Rubin, David MacKenzie, Ian Lance Taylor, and Jim
       Meyering.

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

       [head(1)](../man1/head.1.html)

       Full documentation <[https://www.gnu.org/software/coreutils/tail](https://www.gnu.org/software/coreutils/tail)\>
       or available locally via: info '(coreutils) tail invocation'

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

GNU coreutils 9.9             November 2025                       _TAIL_(1)

---

Pages that refer to this page: [head(1)](../man1/head.1.html),  [pmcd(1)](../man1/pmcd.1.html),  [pmdalogger(1)](../man1/pmdalogger.1.html),  [pmdasystemd(1)](../man1/pmdasystemd.1.html),  [pmdaweblog(1)](../man1/pmdaweblog.1.html),  [pon(1)](../man1/pon.1.html)

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