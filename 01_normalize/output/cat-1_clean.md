<!-- Source: 01_normalize/input/cat-1.md | Cleaned: 2026-05-07 -->

# cat(1) - Linux manual page

# cat(1) — Linux manual page

_CAT_(1)                        User Commands                        _CAT_(1)

cat - concatenate files and print on the standard output

**cat** \[_OPTION_\]... \[_FILE_\]...

Concatenate FILE(s) to standard output.

With no FILE, or when FILE is -, read standard input.

**\-A**, **\--show-all**
              equivalent to **\-vET**

**\-b**, **\--number-nonblank**
              number nonempty output lines, overrides **\-n**

**\-e**     equivalent to **\-vE**

**\-E**, **\--show-ends**
              display $ at end of each line

**\-n**, **\--number**
              number all output lines

**\-s**, **\--squeeze-blank**
              suppress repeated empty output lines

**\-t**     equivalent to **\-vT**

**\-T**, **\--show-tabs**
              display TAB characters as ^I

**\-u**     (ignored)

**\-v**, **\--show-nonprinting**
              use ^ and M- notation, except for LFD and TAB

**\--help** display this help and exit

**\--version**
              output version information and exit

cat f - g
              Output f's contents, then standard input, then g's
              contents.

cat    Copy standard input to standard output.

[tac(1)](../man1/tac.1.html)