<!-- Source: 01_normalize/input/004. 9.3 Working with history.en.srt | Cleaned: 2026-05-07 -->

A very convenient feature
of BASH is history.

Any command that you type is stored in history,
and this history is updated to the bash history file

once you close your session. So anytime you exit,
the history file is updated. And the next time you

open a new session, you still have access to
the commands that were used in the previous session.

The history command is what you can
use to repeat commands from this file.

Use history C to
clear the current history.

Use history W to write the current history,
which shouldn't be necessary because it's normally done automatically.

And use history D to
delete a specific line from history.

Also, you can use control r for
the reverse isearch exclamation mark for followed

If I type history, I can see all the
commands that I have typed so far if I

want to save them. I use history W
to commit my current history to the history file.

Now, I like Control R.
Control R is the reverse isearch.

In this reverse isearch, if I'm looking for the
last awk command, for instance, I just type awk and

there we can see that it is searching backward
for the last command where it has found awg.

Now, this reverse isearch is
searching for a text pattern anywhere

in the command, not necessarily
at the start of the command.

If you want to repeat it,
you can use Control R and Ctrl

R and Ctrl R again until
you found the command that you wanted.

What do we have here? That's a command that is
not complete. So let me Control C that another convenient thing

that you can do in history is exclamation followed by
a number. I'm using exclamation 416 to repeat command 417 again.

Look at that, my
home directory has changed.

And that is the way
to remove commands from history.

I'm going to do that
on the relatively innocent command 417.

So I'm using history D417 and you might
be wondering, when do I ever need to

remove something from history? Well, that's very convenient
if you did something really silly or if

you have entered a clear text password and
you want to make sure that it is

not going to be saved. And that's
how you work with history. Very convenient feature.