<!-- Source: 01_normalize/input/more-1.md | Cleaned: 2026-05-07 -->

# more(1) - Linux manual page

# more(1) — Linux manual page

more - display the contents of a file in a terminal

**more** \[options\] _file_ ...

**more** is a filter for paging through text one screenful at a time.
       This version is especially primitive. Users should realize that
       [less(1)](../man1/less.1.html) provides [more(1)](../man1/more.1.html) emulation plus extensive enhancements.

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
           details. Also, note that the environment variable's value will
           be overridden if any of these options are set.

[less(1)](../man1/less.1.html), **vi**(1)