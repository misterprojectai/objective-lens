<!-- Source: 01_normalize/input/002. 9.1 Understanding the Shell and Other Core Linux Components.en.srt | Cleaned: 2026-05-07 -->

It is good to see the shell in the
context of how an operating system is typically organized.

So it all
starts with the hardware.

The hardware in your computer
is what you want to use.

Now the main layer to interface the
hardware is the kernel and the kernel is

using drivers, also known as kernel modules
that allow you to communicate with the hardware.

But the kernel by itself
is inaccessible for the user.

And that is why in order to
provide the user interface there is a shell.

So at any time you type commands, you type your
commands right here. So this is the world of the user.

Now the shell needs to send
instructions to the kernel and there is

a very important component involved here
and that is C library libc.

And the C library provides system
calls and these system calls are low

level system instructions that allow your
shell to communicate with the kernel.

And that is how commands are
dealt with in a Linux environment.