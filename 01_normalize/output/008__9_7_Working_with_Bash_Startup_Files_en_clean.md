<!-- Source: 01_normalize/input/008. 9.7 Working with Bash Startup Files.en.srt | Cleaned: 2026-05-07 -->

In this video we'll
talk about bash startup files.

It starts with etcenvironment, which contains a list of variables.
And it's the first file that is processed while starting

bash on Reddit. It's not used, so you will
find it as an empty file. By the way, Etc.

Profile is an important file
that is executed while users login.

And in etc profile you will find
a configuration that applies to all users.

ETCprofile D is used as a drop
in directory that contains additional configuration files.

Now there are alternatives for the system
wide etc profile like the bashprofile in

the user home directory which can
be used as a user specific version.

Also convenient is bashlogout that's
processed when a user logs out.

So if you want to make sure that some cleanup is happening all
the time when a user logs out, make sure to tweak it right here.

And then there is etc bashrc
that's closely related to Etc profile.

Etc profile is
executed while users login.

An Etc BASHRC is processed every
time a sub shell is started.

Now what is the difference? Well, sometimes
in a distribution it's configured in a

way that there's not really a difference.
But bashrc is used in a subshell.

So within your current session you
type bash then etc bashrc is included.

An etc profile is only
when you are logging in.

Now you can use a
user specific file with the name

So let me start with less on
etc profile and there we can see etc

profile. And the most important thing that
I want you to realize is that really

it's a complex shell script with components
that you probably don't want to mess up.

Here for instance we have the history size variable
and that's embedded in a conditional loop. So what

do we have in a conditional loop? Well, that
is using a test zhist size, which means if

you don't have a variable hist size then
we to set the his size to 1000.

Now really consider this etc profile a read
only file if you want to modify it.

Etcprofile D is what you want
to use for the drop in files.

You can see drop in files with
the extension csh Ignore them. In a

bash environment it's the files with the
extension sh which are executed by bash.

But here also these files are typically
pretty complex and you shouldn't mess with

them. But if ever you want to
change something and add configuration, you can

put it right here and it will
be executed for all of you users.

How about the bashrc? Well, in the
bash RC we have all of this.

The difference is that this is system wide
functions and environment stuff goes in etc profile.

But probably the most important thing is that
you should not change the contents of this file.

If ever you want to apply
system wide settings, you use a custom

I'm using export. Color is green
and that's what I'm going to quit.

And from now on, the next time that these files are
processed, the custom SH is going to be processed as well.

So what happens when I type list?
Now look at that, my list command is

working and Echo$Co do we have it?
Well we have multiple variables starting with co

and color is giving me green
and that shows how it's normally processed.

Then there are these
hidden files in the user

home directory, bashprofile and
bashrc and likewise the bashlogout.

Normally you won't find too much in these configuration
files, but if there is anything you want to do

for your users, you can put it right here.
And that's how these shell startup files can be used.