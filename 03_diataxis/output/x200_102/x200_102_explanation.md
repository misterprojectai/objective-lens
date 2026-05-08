---
title: "Understanding I/O Redirection and Pipelines"
type: explanation
quadrant:
  practical_theoretical: theoretical
  work_study: study
exam_objective: "x200_102"
version: "1.0"
status: draft
---

# Understanding I/O Redirection and Pipelines

Every Linux command operates within an invisible framework that determines where it reads its input and where it sends its output. Most users never think about this framework — they just see text appearing on a screen. But understanding what is actually happening underneath is what separates someone who can type commands from someone who can compose them into powerful, flexible solutions. This document explains the conceptual model behind standard input, output, and error; why that model exists; and how redirection and pipelines exploit it.

---

## Background

The conceptual foundation of I/O redirection traces back to the earliest days of Unix in the early 1970s. Before Unix, programs were written to interact with specific hardware devices directly. A program that wanted to read from a terminal had to know about that terminal. A program that wrote to a printer had to know about that printer. This made programs rigid — tightly coupled to the devices they were written for.

Unix broke that coupling with a radical simplification: the kernel presents every source and destination of data as a file. Terminals, keyboards, printers, disks, and even inter-process communication channels are all treated through the same interface. A program does not need to know whether it is reading from a keyboard or a file on disk — it simply reads. A program does not need to know whether it is writing to a screen or a pipe feeding another process — it simply writes.

This unification, captured in the phrase "everything is a file," created the precondition for I/O redirection. If all data sources and destinations look the same to a program, then the shell can freely substitute one for another without the program noticing or caring.

Ken Thompson developed Standard Input/Output (STDIO) as part of the infrastructure needed to implement pipes on early Unix. Doug McIlroy invented the pipe mechanism itself, and the Unix philosophy that emerged around these tools — write programs that do one thing well, write programs to work together, write programs to handle text streams — became the guiding design principle that RHEL inherits directly today.

---

## How I/O Redirection Works

### The Three Standard Streams

When the Linux kernel starts any process, it automatically opens three communication channels for that process, identified by small integers called file descriptors:

- **File descriptor 0** — standard input (stdin): the channel from which the process reads its input. By default, connected to the keyboard.
- **File descriptor 1** — standard output (stdout): the channel to which the process writes its normal output. By default, connected to the terminal display.
- **File descriptor 2** — standard error (stderr): the channel to which the process writes error messages and diagnostics. By default, also connected to the terminal display.

The key insight is that programs do not read "from the keyboard" or write "to the screen." They read from file descriptor 0 and write to file descriptors 1 and 2. What those file descriptors are actually connected to is the shell's concern, not the program's. The program is entirely unaware of the substitution.

This is analogous to a telephone call where the speaker doesn't know or care whether the listener is in the same room, across the country, or being recorded. The speaker simply speaks into the receiver; the connection infrastructure handles everything else.

### How the Shell Performs Redirection

Redirection is a shell-level operation. When you write a command with a redirection operator, the shell interprets that operator before the command even starts. The sequence is:

1. The shell parses the command line and identifies any redirection operators.
2. The shell manipulates the file descriptors — opening files, connecting pipes, or pointing descriptors at `/dev/null`.
3. Only then does the shell launch the command, with the file descriptors already configured.

The command receives its inherited file descriptors as if they had always pointed where the shell directed them. From the program's perspective, nothing unusual has happened.

Redirections are processed left to right in the order they appear. This ordering has practical consequences, particularly when combining multiple redirections, because each redirection affects the state of file descriptors at that moment in the sequence.

### The Redirection Operators

The shell provides operators that correspond to the three standard streams:

**Output redirection (`>`)** replaces the destination of stdout. The specified file is created if it does not exist; if it exists, its contents are completely overwritten. The `>` operator is equivalent to `1>` — the `1` is the file descriptor number and is implicit when omitted.

**Append redirection (`>>`)** also redirects stdout to a file, but instead of truncating the file first, it positions the write pointer at the end of the existing content. New output accumulates without destroying what was already there. This is the appropriate operator for log files and any situation where data must be preserved across multiple invocations.

**Input redirection (`<`)** replaces the source of stdin. The specified file is opened for reading and connected to file descriptor 0. The command reads from that file as if it were reading from the keyboard. This is equivalent to `0<`.

**Error redirection (`2>`)** redirects stderr specifically, leaving stdout untouched. The `2` is the file descriptor number written explicitly because there is no shorthand omission for anything other than `0` and `1`. Error output can be separated from normal output, routed to a different file, or discarded entirely.

**Combined redirection (`&>`)** redirects both stdout and stderr to the same destination simultaneously. This is equivalent to the older, more explicit notation `> file 2>&1`, which redirects stdout to a file and then makes stderr a copy of wherever stdout is now pointing.

**The discard device (`/dev/null`)** is a special kernel device that accepts any data written to it and silently discards it, returning nothing when read. It functions as a universal sink. Redirecting unwanted output — particularly error messages from commands where errors are expected and irrelevant — to `/dev/null` is idiomatic Linux practice.

### How Pipelines Work

A pipeline connects the stdout of one command directly to the stdin of the next, without any intermediate file. The pipe character (`|`) instructs the shell to create a kernel pipe object between two processes.

The shell runs the commands in a pipeline in parallel, not sequentially. Both processes exist simultaneously. As the first command produces output and writes it to its stdout, that data flows through the pipe buffer and becomes available for the second command to read from its stdin. The second command can begin processing data before the first command has finished producing it. The shell waits for all commands in the pipeline to complete before proceeding.

A pipeline with three commands uses two pipe objects. Each command in the chain reads from the pipe to its left and writes to the pipe to its right, with the first command reading from its inherited stdin and the last command writing to its inherited stdout.

This composability is the engine of the Unix philosophy. Each command in a pipeline is a transformer: it receives a data stream, processes it in some defined way, and passes the result on. The shell's ability to wire these transformers together without any of them knowing about the others is what makes pipelines so flexible and powerful.

### The `tee` Command: Splitting the Stream

The `tee` command addresses a specific need that arises in pipeline work: sometimes you want to send data both to a file and onward through the pipeline simultaneously. `tee` reads from stdin and writes to two destinations at once — stdout (continuing the pipeline) and a named file. It functions like a plumbing T-junction, splitting the stream without interrupting it.

---

## Why This Design

The separation of stdout and stderr into two distinct file descriptors reflects a deliberate design decision. If a program's normal output and its error messages traveled through the same channel, you could not selectively suppress errors while capturing output, or log errors separately from results. Many real-world tasks require exactly this separation: a backup script that captures file listings to one location while routing permission errors to a log file; a find command that produces results while quietly discarding access-denied messages.

Keeping error messages on stderr also ensures they remain visible to the operator even when stdout has been redirected away. If both streams shared a single file descriptor, redirecting output to a file would also suppress error messages, leaving the operator with no indication that something had gone wrong.

The decision to make programs unaware of redirection — to let the shell handle stream configuration before the process starts — means that programs do not need to be written with redirection in mind. Any program that reads stdin and writes stdout automatically participates in pipelines and redirection without any special coding. This is why the same `grep` command works equally well reading a file, reading from a pipe, or reading redirected input.

The pipe mechanism itself was chosen over alternatives like temporary files because it eliminates latency and disk I/O. When two commands are connected with a pipe, data flows directly from one process to the other through an in-memory buffer. No file is written and then read back. The second command begins processing as soon as the first command produces any output, which is particularly significant when processing large data sets.

---

## Trade-offs and Considerations

I/O redirection and pipelines are not universally the right tool for every situation. Understanding where they excel and where they have limitations matters for real-world administration and for the RHCSA exam.

| Approach | Advantages | Disadvantages |
|---|---|---|
| Redirection to file (`>`, `>>`) | Persistent output; reusable; inspectable | Requires disk space; introduces latency; file must be managed |
| Pipeline (`\|`) | No disk I/O; in-memory; real-time processing; composable | Output is transient; pipeline failure modes can be subtle |
| Temporary file between commands | Easier debugging; intermediate state is inspectable | Clunky; requires cleanup; slower than pipes |

Some practitioners prefer redirecting to a file and then reading the file when debugging complex pipelines, because intermediate state becomes inspectable. This works well for troubleshooting but is exactly what pipelines were designed to avoid in production use — the complexity and overhead of managing temporary files.

The `tee` command bridges these approaches: it allows data to flow through a pipeline while simultaneously capturing an intermediate snapshot to a file, preserving both the efficiency of the pipeline and the debuggability of a stored intermediate result.

One consideration specific to error redirection is the ordering of `2>&1` versus `&>`. The `&>` form is cleaner and clearer for redirecting both streams to the same destination. The older `> file 2>&1` form appears extensively in scripts written before `&>` was widely available, so understanding both is necessary for reading existing automation on RHEL systems.

A subtle but important point: because each command in a multi-command pipeline runs in its own subshell, variable assignments and shell state changes made inside a pipeline do not persist after the pipeline completes. This is a source of genuine confusion for those who are deeply familiar with redirection operators but less aware of pipeline execution semantics.

---

## Common Misconceptions

**Misconception: stderr and stdout look different on the screen, so they must travel differently.**
In practice, both streams write to the same terminal by default, so their output appears identically on screen. The distinction exists only at the file descriptor level. The visual similarity masks the conceptual separation. This misconception leads users to assume that error messages will be redirected when they redirect stdout — they will not, because `>` only redirects file descriptor 1.

**Misconception: The `>` operator is safe to use freely because it only writes if there is output.**
The `>` operator truncates the destination file the moment the shell processes the redirection, before the command runs. If the command produces no output or fails immediately, the file still gets truncated to zero bytes. This behavior surprises administrators who redirect to an existing file expecting the original content to survive a failed command. The `>>` operator does not have this problem — it never truncates.

**Misconception: Commands in a pipeline run sequentially, one after the other.**
Pipelines run all commands in parallel. The shell creates all the processes and pipe connections, then all processes run concurrently. The second command does not wait for the first to finish — it begins reading from the pipe as soon as data is available. This parallel execution is what makes pipelines efficient for large data volumes but also means that if the second command exits early, the first command may receive a write error when it tries to send more data.

**Misconception: Piping and output redirection are interchangeable.**
The pipe operator (`|`) connects a command to another command. The redirection operator (`>`) connects a command to a file. Writing `command1 > command2` does not pipe the output of `command1` into `command2` — it redirects the output of `command1` to a file named `command2`, potentially destroying a program binary if a file with that name exists in the current directory.

**Misconception: `2>&1` and `&>` are exactly equivalent in all contexts.**
For simple cases, they produce the same result. However, `2>&1` redirects stderr to wherever stdout currently points at the moment that redirection is processed. The ordering within the command line matters. `command > file 2>&1` sends both streams to the file. `command 2>&1 > file` sends stderr to the terminal and stdout to the file, because stderr was duplicated from stdout before stdout was redirected. The `&>` form avoids this ordering ambiguity entirely.

---

## Relationship to Other Concepts

I/O redirection is the mechanism through which several other RHCSA topics operate. Shell scripting relies on redirection for logging, error handling, and reading configuration from files. Process management involves redirecting background process output to prevent it from appearing on the terminal during interactive sessions. System administration tasks — searching logs, filtering process lists, comparing file sets — are routinely accomplished through pipelines combining `grep`, `sort`, `awk`, `cut`, and similar filter programs.

Understanding file descriptors as the underlying mechanism also clarifies how tools like `find` with `-exec`, `xargs`, and command substitution interact with I/O. These constructs all manipulate the same three file descriptor channels at their core.

The "everything is a file" principle that makes redirection possible also underlies device file access (`/dev/sda`, `/dev/null`, `/dev/tty`), process file descriptors visible under `/proc`, and the pseudo-terminal infrastructure that enables terminal emulators. Recognizing that redirection is not a special case but an expression of this universal principle gives the concept far greater reach than its syntax alone would suggest.

---

## Further Reading

- [Tutorial: Hands-on Practice with I/O Redirection and Pipelines](#) — guided exercises building redirection and pipeline skills from scratch
- [How-to: Redirect Command Output in Common Administrative Tasks](#) — practical patterns for logging, error handling, and filtering
- [How-to: Build and Debug Multi-Stage Pipelines](#) — constructing complex pipelines step by step
- [Reference: I/O Redirection Operators and File Descriptors](#) — complete operator syntax, file descriptor numbering, and special devices
- [Bash Reference Manual — Redirections](https://www.gnu.org/software/bash/manual/bash.html#Redirections) — authoritative specification of all redirection operators