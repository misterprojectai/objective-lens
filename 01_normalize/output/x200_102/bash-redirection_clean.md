<!-- Source: 01_normalize/input/x200_102/bash-redirection.pdf | Cleaned: 2026-05-08 -->

Bash is the shell, or command language interpreter, for the gnu operating system. The name is an acronym for the ' `Bourne-Again SHell` ', a pun on Stephen Bourne, the author of the direct ancestor of the current Unix shell `sh` , which appeared in the Seventh Edition Bell Labs Research version of Unix.

Bash is largely compatible with `sh` and incorporates useful features from the Korn shell `ksh` and the C shell `csh` . It is intended to be a conformant implementation of the ieee posix Shell and Tools portion of the ieee posix specification (ieee Standard 1003.1). It offers functional improvements over `sh` for both interactive and programming use.

While the gnu operating system provides other shells, including a version of `csh` , Bash is the default shell. Like other gnu software, Bash is quite portable. It currently runs on nearly every version of Unix and a few other operating systems _−_ independently-supported ports exist for ms-dos, os/2, and Windows platforms.

At its base, a shell is simply a macro processor that executes commands. The term macro processor means functionality where text and symbols are expanded to create larger expressions.

A Unix shell is both a command interpreter and a programming language. As a command interpreter, the shell provides the user interface to the rich set of gnu utilities. The programming language features allow these utilities to be combined. Files containing commands can be created, and become commands themselves. These new commands have the same status as system commands in directories such as `/bin` , allowing users or groups to establish custom environments to automate their common tasks.

Shells may be used interactively or non-interactively. In interactive mode, they accept input typed from the keyboard. When executing non-interactively, shells execute commands read from a file.

A shell allows execution of gnu commands, both synchronously and asynchronously. The shell waits for synchronous commands to complete before accepting more input; asynchronous commands continue to execute in parallel with the shell while it reads and executes additional commands. The _redirection_ constructs permit fine-grained control of the input and output of those commands. Moreover, the shell allows control over the contents of commands' environments.

Shells also provide a small set of built-in commands ( _builtins_ ) implementing functionality impossible or inconvenient to obtain via separate utilities. For example, `cd` , `break` , `continue` , and `exec` cannot be implemented outside of the shell because they directly manipulate the shell itself. The `history` , `getopts` , `kill` , or `pwd` builtins, among others, could be implemented in separate utilities, but they are more convenient to use as builtin commands. All of the shell builtins are described in subsequent sections.

While executing commands is essential, most of the power (and complexity) of shells is due to their embedded programming languages. Like any high-level language, the shell provides variables, flow control constructs, quoting, and functions.

Shells offer features geared specifically for interactive use rather than to augment the programming language. These interactive features include job control, command line editing, command history and aliases. Each of these features is described in this manual.

`POSIX` A family of open system standards based on Unix. Bash is primarily concerned with the Shell and Utilities portion of the posix 1003.1 standard.

- `blank` A space or tab character.

`builtin` A command that is implemented internally by the shell itself, rather than by an executable program somewhere in the file system.

## `control operator`

A `token` that performs a control function. It is a `newline` or one of the following: ' `||` ', ' `&&` ', ' `&` ', ' `;` ', ' `;;` ', ' `;&` ', ' `;;&` ', ' `|` ', ' `|&` ', ' `(` ', or ' `)` '.

## `exit status`

The value returned by a command to its caller. The value is restricted to eight bits, so the maximum value is 255.

- `field` A unit of text that is the result of one of the shell expansions. After expansion, when executing a command, the resulting fields are used as the command name and arguments.

- `filename` A string of characters used to identify a file.

`job` A set of processes comprising a pipeline, and any processes descended from it, that are all in the same process group.

- `job control`

A mechanism by which users can selectively stop (suspend) and restart (resume) execution of processes.

## `metacharacter`

A character that, when unquoted, separates words. A metacharacter is a `space` , `tab` , `newline` , or one of the following characters: ' `|` ', ' `&` ', ' `;` ', ' `(` ', ' `)` ', ' `<` ', or ' `>` '.

- `name` A `word` consisting solely of letters, numbers, and underscores, and beginning with a letter or underscore. `Name` s are used as shell variable and function names. Also referred to as an `identifier` .

- `operator` A `control operator` or a `redirection operator` . See Section 3.6 [Redirections], page 38, for a list of redirection operators. Operators contain at least one unquoted `metacharacter` .

## `process group`

A collection of related processes each having the same process group id.

## `process group ID`

A unique identifier that represents a `process group` during its lifetime.

## `reserved word`

A `word` that has a special meaning to the shell. Most reserved words introduce shell flow control constructs, such as `for` and `while` .

## `return status`

A synonym for `exit status` .

`signal` A mechanism by which a process may be notified by the kernel of an event occurring in the system.

## `special builtin`

A shell builtin command that has been classified as special by the posix standard.

`token` A sequence of characters considered a single unit by the shell. It is either a `word` or an `operator` .

`word` A sequence of characters treated as a unit by the shell. Words may not include unquoted `metacharacters` .

matches against shorter strings, or using arrays of strings instead of a single long string, may be faster.

## **3.5.9 Quote Removal**

After the preceding expansions, all unquoted occurrences of the characters ' `\` ', ' `'` ', and ' `"` ' that did not result from one of the above expansions are removed.

## **3.6 Redirections**

Before a command is executed, its input and output may be _redirected_ using a special notation interpreted by the shell. _Redirection_ allows commands' file handles to be duplicated, opened, closed, made to refer to different files, and can change the files the command reads from and writes to. Redirection may also be used to modify file handles in the current shell execution environment. The following redirection operators may precede or appear anywhere within a simple command or may follow a command. Redirections are processed in the order they appear, from left to right.

Each redirection that may be preceded by a file descriptor number may instead be preceded by a word of the form { _varname_ }. In this case, for each redirection operator except `>` &- and `<` &-, the shell will allocate a file descriptor greater than 10 and assign it to { _varname_ }. If `>` &- or `<` &- is preceded by { _varname_ }, the value of _varname_ defines the file descriptor to close. If { _varname_ } is supplied, the redirection persists beyond the scope of the command, allowing the shell programmer to manage the file descriptor's lifetime manually. The `varredir_close` shell option manages this behavior (see Section 4.3.2 [The Shopt Builtin], page 71).

In the following descriptions, if the file descriptor number is omitted, and the first character of the redirection operator is ' `<` ', the redirection refers to the standard input (file descriptor 0). If the first character of the redirection operator is ' `>` ', the redirection refers to the standard output (file descriptor 1).

The word following the redirection operator in the following descriptions, unless otherwise noted, is subjected to brace expansion, tilde expansion, parameter expansion, command substitution, arithmetic expansion, quote removal, filename expansion, and word splitting. If it expands to more than one word, Bash reports an error.

Note that the order of redirections is significant. For example, the command

```
ls>dirlist2>&1
```

directs both standard output (file descriptor 1) and standard error (file descriptor 2) to the file _dirlist_ , while the command

```
ls2>&1>dirlist
```

directs only the standard output to file _dirlist_ , because the standard error was made a copy of the standard output before the standard output was redirected to _dirlist_ .

Bash handles several filenames specially when they are used in redirections, as described in the following table. If the operating system on which Bash is running provides these special files, bash will use them; otherwise it will emulate them internally with the behavior described below.

```
/dev/fd/fd
```

If _fd_ is a valid integer, file descriptor _fd_ is duplicated.

## `/dev/stdin`

File descriptor 0 is duplicated.

## `/dev/stdout`

File descriptor 1 is duplicated.

## `/dev/stderr`

File descriptor 2 is duplicated.

## `/dev/tcp/` _`host`_ `/` _`port`_

If _host_ is a valid hostname or Internet address, and _port_ is an integer port number or service name, Bash attempts to open the corresponding TCP socket.

## `/dev/udp/` _`host`_ `/` _`port`_

If _host_ is a valid hostname or Internet address, and _port_ is an integer port number or service name, Bash attempts to open the corresponding UDP socket.

A failure to open or create a file causes the redirection to fail.

Redirections using file descriptors greater than 9 should be used with care, as they may conflict with file descriptors the shell uses internally.

## **3.6.1 Redirecting Input**

Redirection of input causes the file whose name results from the expansion of _word_ to be opened for reading on file descriptor `n` , or the standard input (file descriptor 0) if `n` is not specified.

The general format for redirecting input is:

## `[` _`n`_ `]<` _`word`_

## **3.6.2 Redirecting Output**

Redirection of output causes the file whose name results from the expansion of _word_ to be opened for writing on file descriptor _n_ , or the standard output (file descriptor 1) if _n_ is not specified. If the file does not exist it is created; if it does exist it is truncated to zero size.

The general format for redirecting output is:

## `[` _`n`_ `]>[|]` _`word`_

If the redirection operator is ' `>` ', and the `noclobber` option to the `set` builtin has been enabled, the redirection will fail if the file whose name results from the expansion of _word_ exists and is a regular file. If the redirection operator is ' `>|` ', or the redirection operator is ' `>` ' and the `noclobber` option is not enabled, the redirection is attempted even if the file named by _word_ exists.

## **3.6.3 Appending Redirected Output**

Redirection of output in this fashion causes the file whose name results from the expansion of _word_ to be opened for appending on file descriptor _n_ , or the standard output (file descriptor 1) if _n_ is not specified. If the file does not exist it is created.

The general format for appending output is:

## `[` _`n`_ `]>>` _`word`_

## **3.6.4 Redirecting Standard Output and Standard Error**

This construct allows both the standard output (file descriptor 1) and the standard error output (file descriptor 2) to be redirected to the file whose name is the expansion of _word_ .

There are two formats for redirecting standard output and standard error:

```
&>word
```

and

```
>&word
```

Of the two forms, the first is preferred. This is semantically equivalent to

```
>word2>&1
```

When using the second form, _word_ may not expand to a number or ' `-` '. If it does, other redirection operators apply (see Duplicating File Descriptors below) for compatibility reasons.

## **3.6.5 Appending Standard Output and Standard Error**

This construct allows both the standard output (file descriptor 1) and the standard error output (file descriptor 2) to be appended to the file whose name is the expansion of _word_ .

The format for appending standard output and standard error is:

```
&>>word
```

This is semantically equivalent to

```
>>word2>&1
```

(see Duplicating File Descriptors below).

## **3.6.6 Here Documents**

This type of redirection instructs the shell to read input from the current source until a line containing only _word_ (with no trailing blanks) is seen. All of the lines read up to that point are then used as the standard input (or file descriptor _n_ if _n_ is specified) for a command.

The format of here-documents is:

`[` _`n`_ `]<<[` _−_ `]` _`word here-document delimiter`_

No parameter and variable expansion, command substitution, arithmetic expansion, or filename expansion is performed on _word_ . If any part of _word_ is quoted, the _delimiter_ is the result of quote removal on _word_ , and the lines in the here-document are not expanded. If _word_ is unquoted, all lines of the here-document are subjected to parameter expansion, command substitution, and arithmetic expansion, the character sequence `\newline` is ignored, and ' `\` ' must be used to quote the characters ' `\` ', ' `$` ', and ' `'` '.

If the redirection operator is ' `<<-` ', then all leading tab characters are stripped from input lines and the line containing _delimiter_ . This allows here-documents within shell scripts to be indented in a natural fashion.

## **3.6.7 Here Strings**

A variant of here documents, the format is:

## `[` _`n`_ `]<<<` _`word`_

The _word_ undergoes tilde expansion, parameter and variable expansion, command substitution, arithmetic expansion, and quote removal. Filename expansion and word splitting are not performed. The result is supplied as a single string, with a newline appended, to the command on its standard input (or file descriptor _n_ if _n_ is specified).

## **3.6.8 Duplicating File Descriptors**

The redirection operator

## `[` _`n`_ `]<&` _`word`_

is used to duplicate input file descriptors. If _word_ expands to one or more digits, the file descriptor denoted by _n_ is made to be a copy of that file descriptor. If the digits in _word_ do not specify a file descriptor open for input, a redirection error occurs. If _word_ evaluates to ' `-` ', file descriptor _n_ is closed. If _n_ is not specified, the standard input (file descriptor 0) is used.

The operator

## `[` _`n`_ `]>&` _`word`_

is used similarly to duplicate output file descriptors. If _n_ is not specified, the standard output (file descriptor 1) is used. If the digits in _word_ do not specify a file descriptor open for output, a redirection error occurs. If _word_ evaluates to ' `-` ', file descriptor _n_ is closed. As a special case, if _n_ is omitted, and _word_ does not expand to one or more digits or ' `-` ', the standard output and standard error are redirected as described previously.

## **3.6.9 Moving File Descriptors**

## `[` _`n`_ `]<&` _`digit`_ `-`

moves the file descriptor _digit_ to file descriptor _n_ , or the standard input (file descriptor 0) if _n_ is not specified. _digit_ is closed after being duplicated to _n_ .

Similarly, the redirection operator

## `[` _`n`_ `]>&` _`digit`_ `-`

moves the file descriptor _digit_ to file descriptor _n_ , or the standard output (file descriptor 1) if _n_ is not specified.

## **3.6.10 Opening File Descriptors for Reading and Writing**

## `[` _`n`_ `]<>` _`word`_

causes the file whose name is the expansion of _word_ to be opened for both reading and writing on file descriptor _n_ , or on file descriptor 0 if _n_ is not specified. If the file does not exist, it is created.