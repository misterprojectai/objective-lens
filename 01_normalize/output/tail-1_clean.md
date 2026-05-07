<!-- Source: 01_normalize/input/tail-1.md | Cleaned: 2026-05-07 -->

# tail(1) - Linux manual page

# tail(1) — Linux manual page

tail - output the last part of files

**tail** \[_OPTION_\]... \[_FILE_\]...

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