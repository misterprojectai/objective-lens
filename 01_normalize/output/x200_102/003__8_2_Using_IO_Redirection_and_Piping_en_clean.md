<!-- Source: 01_normalize/input/x200_102/003. 8.2 Using IO Redirection and Piping.en.srt | Cleaned: 2026-05-08 -->

about I/O Redirection and Piping.

Redirection is used to manipulate

input and output of commands.

And there are three ways of doing it:

standard input, also known as the zero.

The zero is for the file descriptor,

and the file descriptor is
something used internally

by the Linux kernel to
take care of redirection.

And the zero is always
your standard input.

And the standard input normally represents

your keyboard attached to your computer.

And if you want to get
information from somewhere else,

well, there is a smaller than redirector.

Now, the thing with the
smaller than redirector

because many commands don't
need a smaller than redirector

to take their input from
a file for instance,

But standard input redirectors
are just not used that often.

That's not the case for
standard output redirector.

The standard output redirector,

normally your standard output.

That's your screen, your terminal
attached to your computer

and results of commands
are sent to your computer.

And you can redirect it
using a greater than sign.

So if you use ls greater then to ~ myfile

then it'll create myfile
in your home directory.

Do notice that a single greater than sign

will override destination
if it already exists.

if you don't want to override but append

then you use a double redirect.

That will add it to the end of the file.

Also convenient is the option
to redirect standard error.

In order to redirect standard
error, you use 2 greater than

in which the 2 is the file descriptor 2

and the greater than will send it

wherever you want to send it.

Like right here, for
instance, where we use

2 greater than dev null. dev
null is a discard device.

Anything you send to the dev
null device will be discarded.

don't see any error messages
while running commands.

which is using ampersand greater than.

Now what is ampersand greater than?

That will represent the standard output

as well as the standard error.

to the dev null device, but you might want

to capture all that
information in a specific file.

sort smaller than etc services

to use etc services as the
thing that we want sort.

And yeah, the smaller than
is just redirecting the

the input from the
keyboards to etc services.

But ls greater than, lsfile
is a more convincing example.

What do we get? We get
no output on screen.

We get output in lsfile.

Which is the list of files just generated.

Now, if I use who greater than to lsfile

then I'm doing an, a standard
output redirection again.

And after checking the contents of lsfile

you have seen that who
command has overwritten.

And if you don't want
to override but append

then you should use a double redirect.

The double redirect, as you
can see is adding the output

of the command to the
file we just created.

Now, how about the error messages?

Well, let me do grab a root on etc start.

Many, many permission
denied is a directory

which are error messages.

And if you don't care
about the error messages.

2 greater than dev null.

And that will make sure that you only see

the regular output. Now, what is happening

if you make that ampersand greater than.

Ampersand greater than dev null

is showing nothing at
all. That might be useful

for processes that are
supposed to be running

in the background

but not for interactive
commands, like grep.

So let me create outfile and
write the output to outfile.

And there we can see the, the output

including the error messages.

We have the file descriptor 1 as well as

as the file descriptor 2

both being sent to outfile.
Let's go check out piping.

So a pipe is used to send
the output of one command

to be used as input for a second command.

Like ps aux, grab http. Where ps aux is

showing a lot of running
processes and grep http is

filtering out the lines
that contain the text http.

In combination with the pipe,
you might see the tee command.

The tee command combines
redirection and piping.

It allows you to write
the output to somewhere

and at the same time, use it
as input for another command

like ps aux, tee psfile, pipe grep ssh.

So to start with ps aux, ps aux.

Which by the way, is
another BSD style commands.

This command is showing a list

of all the processes currently running.

or not SSH is running well,
this is what you can do.

This is an ordinary pipe
as we have already seen.

Now, how does that work with, with tee?

Well, I am going to pipe to tee.

psfile or whatever you wanna call it.

And then I'm going to pipe to grep SSH.

Here we can see the
result of the grep SSH,

but at the same time,
it has created psfile.

So in psfile, we have the ps aux

and the grep SSH is working on the ps aux.

The tee is really like
the uppercase letter T.

It's sending you two different directions

to a file as well as to the pipe

where it is further treated by grep SSH.

This tee can be handy

if you want to have an
additional opportunity to

analyze what exactly was happening

before you applied the
command after the pipe.