# more(1) - Linux manual page

[man7.org](../../../index.html) > Linux > [man-pages](../index.html)

[Linux/UNIX system programming training](http://man7.org/training/)

---

# more(1) — Linux manual page

[NAME](#NAME) | [SYNOPSIS](#SYNOPSIS) | [DESCRIPTION](#DESCRIPTION) | [OPTIONS](#OPTIONS) | [COMMANDS](#COMMANDS) | [SECURITY](#SECURITY) | [ENVIRONMENT](#ENVIRONMENT) | [HISTORY](#HISTORY) | [AUTHORS](#AUTHORS) | [SEE ALSO](#SEE_ALSO) | [REPORTING BUGS](#REPORTING_BUGS) | [AVAILABILITY](#AVAILABILITY)

  

_MORE_(1)                       User Commands                       _MORE_(1)

## [](#NAME)NAME         [top](#top_of_page)

       more - display the contents of a file in a terminal

## [](#SYNOPSIS)SYNOPSIS         [top](#top_of_page)

       **more** \[options\] _file_ ...

## [](#DESCRIPTION)DESCRIPTION         [top](#top_of_page)

       **more** is a filter for paging through text one screenful at a time.
       This version is especially primitive. Users should realize that
       [less(1)](../man1/less.1.html) provides [more(1)](../man1/more.1.html) emulation plus extensive enhancements.

## [](#OPTIONS)OPTIONS         [top](#top_of_page)

       Options are also taken from the environment variable **MORE** (make
       sure to precede them with a dash (**\-**)) but command-line options
       will override those.

       **\-d**, **\--silent**
           Prompt with "\[Press space to continue, 'q' to quit.\]", and
           display "\[Press 'h' for instructions.\]" instead of ringing the
           bell when an illegal key is pressed.

       **\-l**, **\--logical**
           Do not pause after any line containing a **^L** (form feed).

       **\-e**, **\--exit-on-eof**
           Exit on End-Of-File, enabled by default if POSIXLY\_CORRECT
           environment variable is not set or if not executed on
           terminal.

       **\-f**, **\--no-pause**
           Count logical lines, rather than screen lines (i.e., long
           lines are not folded).

       **\-p**, **\--print-over**
           Do not scroll. Instead, clear the whole screen and then
           display the text. Notice that this option is switched on
           automatically if the executable is named **page**.

       **\-c**, **\--clean-print**
           Do not scroll. Instead, paint each screen from the top,
           clearing the remainder of each line as it is displayed.

       **\-s**, **\--squeeze**
           Squeeze multiple blank lines into one.

       **\-u**, **\--plain**
           Suppress underlining. This option is silently ignored as
           backwards compatibility.

       **\-n**, **\--lines** _number_
           Specify the _number_ of lines per screenful. The _number_ argument
           is a positive decimal integer. The **\--lines** option shall
           override any values obtained from any other source, such as
           number of lines reported by terminal.

       **\-**_number_
           A numeric option means the same as **\--lines** option argument.

       **+**_number_
           Start displaying each file at line _number_.

       **+**/_string_
           The _string_ to be searched in each file before starting to
           display it.

       **\-h**, **\--help**
           Display help text and exit.

       **\-V**, **\--version**
           Display version and exit.

## [](#COMMANDS)COMMANDS         [top](#top_of_page)

       Interactive commands for **more** are based on **vi**(1). Some commands
       may be preceded by a decimal number, called k in the descriptions
       below. In the following descriptions, **^X** means **control-X**.

       **h** or **?**
           Help; display a summary of these commands. If you forget all
           other commands, remember this one.

       **SPACE**
           Display next k lines of text. Defaults to current screen size.

       **z**
           Display next k lines of text. Defaults to current screen size.
           Argument becomes new default.

       **RETURN**
           Display next k lines of text. Defaults to 1. Argument becomes
           new default.

       **d** or **^D**
           Scroll k lines. Default is current scroll size, initially 11.
           Argument becomes new default.

       **q** or **Q** or **INTERRUPT**
           Exit.

       **s**
           Skip forward k lines of text. Defaults to 1.

       **f**
           Skip forward k screenfuls of text. Defaults to 1.

       **b** or **^B**
           Skip backwards k screenfuls of text. Defaults to 1. Only works
           with files, not pipes.

       **'**
           Go to the place where the last search started.

       **\=**
           Display current line number.

       **/pattern**
           Search for kth occurrence of regular expression. Defaults to
           1.

       **n**
           Search for kth occurrence of last regular expression. Defaults
           to 1.

       **!command** or **:!command**
           Execute _command_ in a subshell.

       **v**
           Start up an editor at current line. The editor is taken from
           the environment variable **VISUAL** if defined, or **EDITOR** if
           **VISUAL** is not defined, or defaults to **vi**(1) if neither **VISUAL**
           nor **EDITOR** is defined.

       **^L**
           Redraw screen.

       **:n**
           Go to kth next file. Defaults to 1.

       **:p**
           Go to kth previous file. Defaults to 1.

       **:f**
           Display current file name and line number.

       **.**
           Repeat previous command.

## [](#SECURITY)SECURITY         [top](#top_of_page)

       When either MORESECURE or PAGERSECURE is set, **more** will run in
       "secure" mode and effectively disable the following commands:

       **!command** or **:!command**
           Execute _command_ in a subshell.

       **v**
           Start up an editor.

## [](#ENVIRONMENT)ENVIRONMENT         [top](#top_of_page)

       The **more** command respects the following environment variables, if
       they exist:

       **MORE**
           This variable may be set with favored options to **more**.

       **SHELL**
           Current shell in use (normally set by the shell at login
           time).

       **TERM**
           The terminal type used by **more** to get the terminal
           characteristics necessary to manipulate the screen.

       **VISUAL**
           The editor the user prefers. Invoked when command key _v_ is
           pressed.

       **EDITOR**
           The editor of choice when **VISUAL** is not specified.

       **POSIXLY\_CORRECT**
           Disable exit-on-eof (see option **\-e** for more details).

       **MORESECURE**
           Run **more** in "secure" mode. See SECURITY for details.

       **PAGERSECURE**
           Equivalent to MORESECURE.

       **MORE\_SHELL\_LINES**
           Specify the _number_ of lines per screenful. It has the same
           effect as the **\-n** and **\--lines** options. See in OPTIONS for
           details. Also, note that the environment variable’s value will
           be overridden if any of these options are set.

## [](#HISTORY)HISTORY         [top](#top_of_page)

       The **more** command appeared in 3.0BSD. This man page documents **more**
       version 5.19 (Berkeley 6/29/88), which is currently in use in the
       Linux community. Documentation was produced using several other
       versions of the man page, and extensive inspection of the source
       code.

## [](#AUTHORS)AUTHORS         [top](#top_of_page)

       Eric Shienbrood, UC Berkeley.

       Modified by Geoff Peck, UCB to add underlining, single spacing.

       Modified by John Foderaro, UCB to add -c and MORE environment
       variable.

       Modified by Christian Goeschel Ndjomouo to add MORESECURE,
       PAGERSECURE and MORE\_SHELL\_LINES environment variables, and a
       SECURITY section

## [](#SEE_ALSO)SEE ALSO         [top](#top_of_page)

       [less(1)](../man1/less.1.html), **vi**(1)

## [](#REPORTING_BUGS)REPORTING BUGS         [top](#top_of_page)

       For bug reports, use the issue tracker
       <[https://github.com/util-linux/util-linux/issues](https://github.com/util-linux/util-linux/issues)\>.

## [](#AVAILABILITY)AVAILABILITY         [top](#top_of_page)

       The **more** command is part of the util-linux package which can be
       downloaded from Linux Kernel Archive
       <[https://www.kernel.org/pub/linux/utils/util-linux/](https://www.kernel.org/pub/linux/utils/util-linux/)\>. This page is
       part of the _util-linux_ (a random collection of Linux utilities)
       project. Information about the project can be found at 
       ⟨[https://www.kernel.org/pub/linux/utils/util-linux/](https://www.kernel.org/pub/linux/utils/util-linux/)⟩. If you have a
       bug report for this manual page, send it to
       util-linux@vger.kernel.org. This page was obtained from the
       project's upstream Git repository
       ⟨git://git.kernel.org/pub/scm/utils/util-linux/util-linux.git⟩ on
       2026-01-16. (At that time, the date of the most recent commit that
       was found in the repository was 2026-01-14.) If you discover any
       rendering problems in this HTML version of the page, or you
       believe there is a better or more up-to-date source for the page,
       or you have corrections or improvements to the information in this
       COLOPHON (which is _not_ part of the original manual page), send a
       mail to man-pages@man7.org

util-linux 2.42-start-1036-e... 2025-12-04                        _MORE_(1)

---

Pages that refer to this page: [bash(1)](../man1/bash.1.html),  [colcrt(1)](../man1/colcrt.1.html),  [dpkg(1)](../man1/dpkg.1.html),  [dpkg-query(1)](../man1/dpkg-query.1.html),  [homectl(1)](../man1/homectl.1.html),  [importctl(1)](../man1/importctl.1.html),  [journalctl(1)](../man1/journalctl.1.html),  [less(1)](../man1/less.1.html),  [localectl(1)](../man1/localectl.1.html),  [loginctl(1)](../man1/loginctl.1.html),  [machinectl(1)](../man1/machinectl.1.html),  [more(1)](../man1/more.1.html),  [portablectl(1)](../man1/portablectl.1.html),  [systemctl(1)](../man1/systemctl.1.html),  [systemd(1)](../man1/systemd.1.html),  [systemd-analyze(1)](../man1/systemd-analyze.1.html),  [systemd-inhibit(1)](../man1/systemd-inhibit.1.html),  [systemd-nspawn(1)](../man1/systemd-nspawn.1.html),  [systemd-vmspawn(1)](../man1/systemd-vmspawn.1.html),  [timedatectl(1)](../man1/timedatectl.1.html),  [updatectl(1)](../man1/updatectl.1.html),  [userdbctl(1)](../man1/userdbctl.1.html),  [readline(3)](../man3/readline.3.html),  [environ(7)](../man7/environ.7.html),  [systemd-tmpfiles(8)](../man8/systemd-tmpfiles.8.html)

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