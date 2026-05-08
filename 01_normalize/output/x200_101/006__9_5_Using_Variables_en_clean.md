<!-- Source: 01_normalize/input/006. 9.5 Using Variables.en.srt | Cleaned: 2026-05-07 -->

The next feature of the bash shell
that you really should understand is the variable.

A variable is a label to
which a dynamic value can be assigned.

Variables are convenient for scripting,
and you define the variable

once and use in a
flexible way in different environments.

What's the idea behind that? Well, if you create
a script, you don't want hard coded values, you

want values to be defined in a variable, and
the script will pick up the value from the

variable whenever it is running. And that is
a nice way of making your scripts flexible.

But for now, let's not talk about scripts,
let's talk about system variables. They contain default

settings that are used by Linux and there's
a couple of them that are quite convenient.

Like the path variable, which
contains a list of directories

that I search for
binaries while executing a command.

I am writing $path, by the
way, because if you want to get

the value of a variable, you
put a dollar in front of it.

Another variable is dollar shell. Dollar shell
is the current shell that is used.

Environment variables can be
set for application use.

You use varname is
value to define your variable,

and then you can
use echo$varname to read.

Now, by default, variables are only known to the
current shell. If you want to define a variable that

is known in subshells as well, you need to
use export in front of it. Let me show you.

Let's start with env. Env is
for env environment and that is

showing the environment variables that
are in use by my system.

So echo dollar user, for instance, is giving my current
user ID that student or echo dollar path, which is

giving a list of directories where the bash shell is
checking for program files. When I run a program file.

Did I say the bash shell? Is that so? Well,
let's use echo dollar shell. Yeah, it's the bash shell.

Now, variables are used as system variables
and these are convenient. You can set them

yourself as well. Let's use color is
red. That's how you define a variable.

Next, if I want to refer to the variable echo
dollar color and there we can see the current value.

Now if I start a subshell, what is a subshell?
Well, that's a process that started from the current environment.

I'm going to run bash as subshell and then I'm
using echo dollar color and I don't see it anymore.

Let's get out of the subshell to
the parent shell and let's define the variable

in a way that it also exists
in the subshell. So export color is red.

And now I'm starting my subshell
again in echo dollar color and

there we can see that
it does exist in the subshell.

Now, setting variables yourself is not so useful
if you're not going to use them. This particularly

makes sense when you are going to work
with Bash shell scripts to automate tasks on Linux.