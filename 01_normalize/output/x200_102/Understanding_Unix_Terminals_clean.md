<!-- Source: 01_normalize/input/x200_102/Understanding Unix Terminals.md | Cleaned: 2026-05-08 -->

# Understanding Unix Terminals, Shells, and Linux System Programming

## Chapter 3: Standard Input and Output - The Unix Convention

Here's where we get into one of the most fundamental conventions in Unix - one that affects literally every program you'll ever run on a Unix system. In Unix, we have this convention whereby processes, when they are started, expect to inherit from their parent two open file descriptors: file descriptor 0 and file descriptor 1.

Let's break down what these are: File descriptor 0 we call standard in, abbreviated as stdin. File descriptor 1 we call standard out, abbreviated as stdout. Now you might be wondering what a file descriptor actually is - think of it like a handle or reference number that a process uses to read from or write to an open file. When you open a file in Unix, you get back a small integer - that's your file descriptor - and you use that number in subsequent read and write operations.

In the usual case, processes expect stdin to be a file descriptor open for reading a terminal character device file, and stdout is expected to be open for writing that same terminal character device file. Let me put that in plain English: when a program starts up, it expects that file descriptor 0 is already set up so it can read keyboard input from a terminal, and file descriptor 1 is already set up so it can write text output to that same terminal.

So in practice, what does this mean for you as a programmer or system administrator? When a program wishes to read input from a terminal, it simply reads from stdin - its file descriptor 0. And when a program wishes to display text on that same terminal, it writes data to stdout. The program doesn't need to know which specific terminal device file it's connected to or even locate an appropriate terminal itself. It just uses these pre-opened file descriptors that it inherits.

### The Parent-Child File Descriptor Inheritance Model

Now be clear - this is what processes expect to inherit from their parent. Let me explain what I mean by "inherit from their parent" because this is crucial to understanding how Unix process creation works.

Recall that when a process forks in Unix - that is, when it creates a child process - the file descriptors from the parent get copied to the child. So the child process has all the same open file descriptors as the parent, pointing to the same files. This is automatic; it happens as part of the fork operation.

So the convention in Unix is that when programs wish to interact with a terminal, they usually don't locate an appropriate terminal themselves. They don't go searching through the file system looking for terminal device files. Instead, they just expect to inherit these file descriptors already open to an appropriate terminal from their parent process. Think of it like this: somewhere up the chain of parent processes, usually at system boot or when you log in, a terminal gets opened, and then every subsequent process you launch inherits access to that terminal through these standard file descriptors.

### Why Two Separate File Descriptors?

Now you may be wondering - and this is a really good question - why do we have two separate file descriptors, one for reading and one for writing? After all, couldn't we just use a single file descriptor for both reading and writing the terminal?

Well, first off, there's something I haven't explicitly mentioned yet in this coverage of Unix system calls: when you open a file, you can open it in a mode such that only reading is allowed, or only writing is allowed. That is definitely possible in Unix. You specify the mode when you call the open system call.

Still, that doesn't fully explain why we have two separate file descriptors when we could theoretically just get away with one file descriptor opened for both reading and writing. Here's the thing - this design choice is something that will become clear a bit later when we talk about what's called redirection. For now, just know that having separate file descriptors for input and output gives Unix tremendous flexibility in how it connects processes together and redirects their input and output streams. This separation is actually one of the key design decisions that makes Unix pipelines and I/O redirection so powerful and elegant.

## Chapter 15: I/O Redirection - Controlling Input and Output Streams

Before we understood I/O redirection from the terminal perspective - how those file descriptors 0, 1, and 2 represent stdin, stdout, and stderr. Now let's explore how to actually manipulate these streams when executing commands. Redirection is how you change where a command reads its input from and where it sends its output to.

Think of it like this: by default, commands read from your keyboard (stdin) and write to your screen (stdout for normal output, stderr for errors). Redirection lets you say "actually, read from this file instead" or "send the output to that file" or even "connect this command's output to that command's input." It's plumbing for data streams.

### Before the Command Executes

Here's something important to understand: redirection happens before the command executes. The shell sets up all the redirections first, then launches the command. This means redirections are processed left to right in the order they appear, and by the time your command runs, its file descriptors are already configured.

This ordering matters because you can do things like duplicate file descriptors, and the order determines what each descriptor points to at any given moment.

### Basic Input Redirection

The `<` operator redirects input. It opens a file for reading and connects it to the command's standard input (file descriptor 0).

**Format:** `[n]<word`

If you don't specify `n`, it defaults to 0 (stdin). The `word` undergoes all the normal shell expansions (brace, tilde, parameter, command substitution, arithmetic expansion, quote removal, and filename expansion), and the result must be a single filename.

```bash
# Read input from file instead of keyboard
sort < unsorted.txt

# Explicit file descriptor (same as above since 0 is default)
sort 0< unsorted.txt

# Use with other commands
wc -l < /etc/passwd  # Count lines in passwd file
```

### Basic Output Redirection

The `>` operator redirects output. It opens a file for writing and connects it to the command's standard output (file descriptor 1). If the file doesn't exist, it's created. If it exists, it's truncated to zero size (overwritten).

**Format:** `[n]>[|]word`

Again, if you don't specify `n`, it defaults to 1 (stdout).

```bash
# Write output to file
ls > directory_list.txt

# Explicit file descriptor
ls 1> directory_list.txt

# Overwrite protection with noclobber
set -o noclobber       # Enable overwrite protection
ls > existing.txt      # This will FAIL if existing.txt exists
ls >| existing.txt     # This FORCES overwrite even with noclobber set
set +o noclobber       # Disable overwrite protection
```

The `noclobber` option is a safety feature - when enabled, `>` won't overwrite existing files. Use `>|` to override this protection when you really want to clobber a file.

### Appending Output

The `>>` operator appends output to a file instead of overwriting it. If the file doesn't exist, it's created.

**Format:** `[n]>>word`

```bash
# Append to log file
echo "Process started" >> application.log
echo "Step 1 complete" >> application.log
echo "Step 2 complete" >> application.log

# All three lines are now in application.log, in order
```

This is essential for logging - you almost never want to overwrite your log file, you want to add new entries to it.

### Redirecting Both stdout and stderr

Often you want to redirect both standard output and standard error to the same place. Bash provides convenient syntax for this:

**Format 1 (preferred):** `&>word`
**Format 2:** `>&word`

Both forms redirect both stdout (fd 1) and stderr (fd 2) to the same file.

```bash
# Capture both output and errors
command &> all_output.txt

# This is equivalent to:
command > all_output.txt 2>&1

# Appending both stdout and stderr
command &>> all_output.log
```

The `&>` syntax is cleaner and more intuitive than `> file 2>&1`, though the latter works and you'll see it in older scripts.

### Duplicating File Descriptors

Sometimes you need to make one file descriptor a copy of another. This is how you redirect stderr to wherever stdout is going, or vice versa.

**Input duplication:** `[n]<&word`
**Output duplication:** `[n]>&word`

If `word` expands to one or more digits, file descriptor `n` becomes a copy of that descriptor. If `word` is `-`, descriptor `n` is closed.

```bash
# Redirect stderr to wherever stdout is going
command 2>&1

# Redirect stderr to wherever stdout is going, then redirect stdout to file
command > output.txt 2>&1
# Now both stdout and stderr go to output.txt

# WRONG order - doesn't work as intended:
command 2>&1 > output.txt  
# This redirects stderr to the CURRENT stdout (the terminal),
# THEN redirects stdout to the file
# So stderr still goes to terminal, only stdout goes to file

# Close a file descriptor
exec 3>&-  # Close file descriptor 3
```

The order matters! `> output.txt 2>&1` is NOT the same as `2>&1 > output.txt`. Redirections are processed left to right, so:
- `> output.txt 2>&1`: stdout to file first, then stderr to wherever stdout goes (the file)
- `2>&1 > output.txt`: stderr to wherever stdout currently goes (terminal), then stdout to file

### Moving File Descriptors

Related to duplicating, you can move a file descriptor, which duplicates it and then closes the original:

**Input:** `[n]<&digit-`
**Output:** `[n]>&digit-`

Note the hyphen after the digit. This moves the descriptor instead of just copying it.

```bash
# Move file descriptor 3 to descriptor 4, close 3
exec 4<&3-

# After this, descriptor 4 points to what 3 pointed to, and 3 is closed
```

This is useful in advanced fd manipulation, particularly when you're managing multiple file descriptors in complex scripts.

### Opening Files for Reading and Writing

You can open a file for both reading and writing on a single file descriptor:

**Format:** `[n]<>word`

```bash
# Open file for read/write on fd 3
exec 3<> datafile.txt

# Now you can both read from and write to fd 3
echo "New data" >&3  # Write to the file
read -u 3 line       # Read from the file
```

This is particularly useful when you need to both read and modify a file, or when working with device files that support bidirectional communication.

### Here Documents - Inline Input

Here documents let you embed multi-line input directly in your script instead of reading from a file. The shell reads input from the current source until it sees a line containing only the delimiter you specified.

**Format:**
```
[n]<<[-]delimiter
here-document content
delimiter
```

The delimiter can be any word. If any part of the delimiter is quoted, the here-document content is treated literally (no expansions). If the delimiter is unquoted, the content undergoes parameter expansion, command substitution, and arithmetic expansion (like inside double quotes).

```bash
# Basic here document
cat <<EOF
This is line 1
This is line 2
This is line 3

### Special File Names

Bash recognizes certain special filenames in redirections and handles them specially:

**`/dev/fd/N`** - Duplicate file descriptor N  
```bash
# Same as >&3
command >/dev/fd/3
```

**`/dev/stdin`** - Duplicate file descriptor 0 (standard input)
**`/dev/stdout`** - Duplicate file descriptor 1 (standard output)
**`/dev/stderr`** - Duplicate file descriptor 2 (standard error)

```bash
# Explicitly write to stderr
echo "Error message" >/dev/stderr
```

**`/dev/tcp/host/port`** - Open TCP connection
**`/dev/udp/host/port`** - Open UDP connection

```bash
# Simple HTTP request using /dev/tcp
exec 3<>/dev/tcp/www.example.com/80
echo -e "GET / HTTP/1.1\r\nHost: www.example.com\r\n\r\n" >&3
cat <&3

# Check if a port is open
timeout 2 bash -c "cat < /dev/tcp/localhost/22" && echo "Port 22 open"
```

If the OS provides these special files natively, Bash uses them. Otherwise, Bash emulates them internally.

### Advanced File Descriptor Management

You can use variable names instead of hard-coded numbers for file descriptors:

**Format:** `{varname}`

```bash
# Allocate a file descriptor >= 10 automatically
exec {myfd}>output.txt

# Now $myfd contains the file descriptor number
echo "Log entry" >&$myfd

# Close it using the variable
exec {myfd}>&-
```

This is safer than using hard-coded numbers because you avoid conflicts with descriptors the shell might be using internally. The `varredir_close` shell option controls whether these file descriptors persist beyond the command scope.

### Redirections in Practice

**Discarding output:**
```bash
# Discard all output
command >/dev/null 2>&1

# Discard only errors
command 2>/dev/null

# Discard only standard output
command >/dev/null
```

**Separating output and errors:**
```bash
# Send output to one file, errors to another
command >output.txt 2>errors.txt

# Different fds for output and error processing
some_command > >(process_output) 2> >(process_errors)
```

**Swapping stdout and stderr:**
```bash
# This is tricky - requires a temporary descriptor
command 3>&1 1>&2 2>&3 3>&-
# 3>&1: save stdout to fd 3
# 1>&2: redirect stdout to stderr
# 2>&3: redirect stderr to saved stdout (fd 3)
# 3>&-: close fd 3
```

**Logging with timestamps:**
```bash
{
    echo "Starting process"
    command1
    command2
    echo "Process complete"
} 2>&1 | while read line; do
    echo "$(date '+%Y-%m-%d %H:%M:%S') $line"
done >> application.log
```

**Keeping errors on screen while logging output:**
```bash
command 2>&1 | tee output.log
# Both stdout and stderr go through tee,
# appearing on screen AND in output.log
```

### Redirection Order and Semantics

The order of redirections is significant because they're processed left to right:

```bash
# Example 1: Both to file
ls >output.txt 2>&1
# Process: stdout to output.txt, then stderr to wherever stdout goes (output.txt)
# Result: Both in output.txt

# Example 2: Only stdout to file
ls 2>&1 >output.txt
# Process: stderr to wherever stdout currently goes (terminal),
#          then stdout to output.txt
# Result: stdout in output.txt, stderr to terminal

# Example 3: Redirection with command execution
cat < input.txt > output.txt
# Both redirections are set up BEFORE cat runs
# cat sees input.txt as stdin and output.txt as stdout
```

### Redirections and Shell Execution Environment

When you use redirections with the `exec` builtin, they affect the current shell's file descriptors, not just a command:

```bash
# Redirect all subsequent output to file
exec >output.txt

# Now everything prints to output.txt instead of terminal
echo "This goes to the file"
ls
# Even ls output goes to the file

# Restore stdout to terminal (assuming fd 6 was saved earlier)
exec 1>&6 6>&-
```

This is powerful for logging entire sections of a script or redirecting all output at once.

### Common Redirection Patterns

**Pattern 1: Silent execution (hide all output)**
```bash
command >/dev/null 2>&1
# Or using &>
command &>/dev/null
```

**Pattern 2: Append to log with both stdout and stderr**
```bash
command >> logfile.txt 2>&1
# Or using &>>
command &>> logfile.txt
```

**Pattern 3: Capture output in variable while showing errors**
```bash
output=$(command 2>&1)  # Captures both, errors mixed in
# OR
output=$(command 2>/dev/tty)  # Errors to terminal, only stdout captured
```

**Pattern 4: Process output and errors separately**
```bash
{ command 2>&1 1>&3 | error_processor; } 3>&1 | output_processor
# This is complex but powerful - errors go to error_processor,
# output goes to output_processor
```

**Pattern 5: Tee to both file and screen**
```bash
command 2>&1 | tee output.log
# Output appears on screen AND in file
```

So hopefully that makes sense - I/O redirection gives you complete control over where data flows. You can redirect input from files instead of keyboard, send output to files instead of screen, connect commands together with pipes, embed multi-line input with here documents, and manipulate file descriptors in sophisticated ways. Master these redirection techniques and you'll be able to build complex data processing pipelines and robust scripts that handle input and output exactly the way you need.

## Chapter 16: Pipelines - Composing Commands Together

Redirection in Unix makes possible another incredibly powerful trick called pipelining. This is one of those features that really demonstrates the elegance of Unix's design philosophy - the idea that you can compose small, focused programs together to accomplish complex tasks.

When in the shell we separate two commands with the pipe character (which is usually found on the same key as your backslash key - it's easy to mistake for a lowercase L, but it's not; it's a separate character, just a vertical bar: `|`), the shell will run these two commands in parallel. It will run them at the same time, and it will redirect the stdout of the first command such that it becomes the stdin of the second command.

Think of it like this: effectively, whatever the first command writes to stdout gets read as stdin by the second command. The data flows from one program to the next, like water flowing through a pipe. That's why we call it pipelining.

### Why We Need Pipe Files

Now you might wonder, why do we need this special pipe mechanism? The reason we have to involve a pipe is because processes can't read and write from each other like files. Processes simply can't do that directly - they're isolated from each other for security and stability. So we have to put a pipe in the middle to facilitate the communication.

### The Mechanics of Pipeline Execution

Looking at exactly what happens when you use a pipe, the sequence is quite elegant:

**Step 1: Create the Pipe** - First, the shell creates a pipe to connect the two processes. This is a special kernel object that acts as a buffer between the two programs.

**Step 2: Fork Twice** - Then the shell forks itself actually twice, creating two child processes.

**Step 3: Parent Waits** - The parent - the original shell process - waits for both of those children. It waits for both of them to complete before it gives you your prompt back.

**Step 4: Redirect First Command** - In one of the child processes, it redirects its stdout to the pipe (the newly created pipe), before it then executes the first command.

**Step 5: Redirect Second Command** - Meanwhile, the other child process redirects its stdin to the pipe before it executes the second command.

So again, these two commands execute in parallel. They're separate processes running concurrently, and the original shell process waits for both of them to terminate before it continues on its business. This parallel execution is important because it means data can flow through the pipe as it's being produced - the second command doesn't have to wait for the first to completely finish before it starts processing data.

### Multi-Stage Pipelines

When we pipe commands, we're not limited to piping just two commands together. We can pipe three or more, creating sophisticated data processing chains.

In the case of three commands, you'd end up with something like this:

```bash
command1 | command2 | command3
```

Here, the first command writes its stdout to a pipe, and then that pipe is read as stdin by the second command, which in turn writes its stdout to a second pipe, which is read as stdin by the third command.

So when we have three commands connected by two pipe characters, that actually represents two pipe files - two separate kernel pipe objects. Again, be clear that all of these commands connected by pipes are run in tandem, they're run in parallel, and the shell waits for all three to finish before it continues.

This composability is one of Unix's greatest strengths. You can take simple, single-purpose utilities and chain them together to solve complex problems without writing any custom code. Need to find all the unique IP addresses in a log file and count them? Pipe together `cat`, `grep`, `sort`, and `uniq`. It's like building with LEGO blocks - each piece does one thing well, and you combine them to build whatever you need.

## Chapter 17: Command Lists and Job Control

So moving forward, we need to be clear on terminology, because the shell has specific concepts for how commands are grouped and executed.

### Pipelines Defined

What in the shell we call a pipeline refers to either:
1. Just a single process executed on its own, or
2. Multiple commands separated by the pipe character (`|`), and therefore executed in tandem, connected by pipes

So even a single command like `ls` is technically a pipeline - it's just a pipeline with one stage. When you add pipe characters, you create a multi-stage pipeline.

### Command Lists and Termination

What we call a command list is one or more pipelines, separated and terminated by specific control characters:
- The semicolon character (`;`)
- Ampersand characters (`&`)
- The newline character

Most commonly, when we type commands interactively in the shell, we terminate each pipeline by simply typing Enter - that is, inserting a newline character - and then the shell executes that pipeline.

### Sequential Execution with Semicolons

If instead of a newline we separate pipelines with a semicolon, then the shell executes them one by one in sequence. So for example:

```bash
command1; command2; command3
```

The shell will first execute `command1` and wait for it to complete. Then it executes `command2` and waits for it to complete. Then it executes `command3` and waits for it to complete. Each pipeline runs to completion before the next one starts.

This is useful when you want to run several commands in sequence but don't want to wait for each one individually to finish before typing the next command. You can type them all on one line separated by semicolons.

### Background Execution with Ampersand

If instead we use an ampersand to separate or terminate pipelines, then what the shell does is very different. When a pipeline is terminated by an ampersand, the shell runs it in the background. The shell doesn't wait for it to finish - it immediately continues on to the next command or returns to the prompt.

```bash
long_running_task &
```

This is incredibly useful for long-running processes. Maybe you want to start a compilation that will take 10 minutes, but you don't want to sit there waiting - you want to continue doing other work in the same terminal. You just put an ampersand at the end of the command, and it runs in the background.

The background process still has its stdout and stdin connected to the terminal by default, which can sometimes cause confusing behavior where background process output appears in your terminal while you're typing other commands. In practice, you often want to redirect the output of background processes to files to keep your terminal clean.

### Built-in Commands and the Current Working Directory

Now let's talk about a different aspect of shell behavior - built-in commands. Recall that every process in Unix has associated with it a current working directory, or sometimes called the process working directory. The shell is a process, so it too has a current working directory.

When you run the built-in command `cd` followed by a directory path, you're changing the current working directory of the shell itself. For example:

```bash
cd /home/brian/projects
```

Now here's what's significant about this: any command we run from the shell inherits the current working directory of the shell itself. This is part of the process creation mechanism - when you fork, the child process inherits the parent's current working directory.

And this is significant because many commands will use the current working directory as a default argument for a file path when no file path argument is given. Like for example, the `ls` command - if we don't give it a program argument specifying a directory whose contents we wish to list, then the `ls` command assumes we wish to list the content of the current working directory.

So in fact, if you run `ls` with no arguments at all, then what it will print out is the contents of the current working directory of your shell. That's why `cd` followed by `ls` is such a common pattern - you change to a directory, then list its contents.

### The Echo Built-in Command

The built-in command `echo` simply prints all of its arguments to stdout. So here's an example:

```bash
echo foo 2348
```

This simply puts out to stdout the text "foo" and then space "2348". Now, of course, this may not seem useful at the command prompt, because why would you want the shell to just spit back at you exactly what you just typed?

Well, one way this is useful is that in various ways we haven't yet discussed, the shell, when we use certain special syntax in the arguments, processes the arguments such that what actually gets sent to the command is different from what you literally type. The `echo` command becomes a way to see what the shell actually did with your input after all its processing and expansion. It's a debugging and exploration tool.

For example, the dollar sign specially denotes the syntax for what's called variable expansion, which is what we'll explore next.