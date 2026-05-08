<!-- Source: 01_normalize/input/006. 8.5 Using ssh to Connect to a Remote Server.en.srt | Cleaned: 2026-05-07 -->

In this video, I'll tell you about Secure Shell. That's
a solution that allows you to connect to a remote server.

So in order to connect to a
remote server, you need the SSH process

to be up and running, because
without this process, there's no remote access.

Typically, if you're on a desktop, you probably
have to install and enable the SSH server.

So to install it on Ubuntu you would
use sudo apt install openssh server and on

CentOS you need to use sudo dnf install
openssh server as well as sudo systemctl enable

now ssh d to activate the server
and to flag it for an automatic restart.

After doing so, use systemctl status SSHD
to verify that the SSH server is running.

And if this doesn't work because
you don't have systemctl, you can try

Service SSHD status. That's the old
way of verifying that services are running.

So starting with sudo systemctl status ssh
that is querying the systemd service. And as

you can see, systemctl status ssh, likewise
for SSH D is giving me unit SSH

service could not be found. That's because
this is an Ubuntu desktop and it's not

installed. So I need sudo apt
install openssh server to install it.

server package is installed and
it should also be automatically enabled.

And that is showing me what? Well, it's showing me
that it is loaded and the preset is enabled. That means

that after a reboot it will automatically come back and
it is triggered by SSH socket. Well, that's good enough.

That means that something
is listening on Port

22 and my Ubuntu
machine is now reachable.

In order to reach it, I
need IPA to find the IP address.

And there I can see
that my IP address is 192.168.29.1.38.

Well, an SSH client is what
you need to access the SSH server.

On Linux and macOS, it's very
easy. You use the native command line

ssh client that's just a command
that you run from a terminal.

On Windows, you need an
external program. Mobile xterm is commonly

By default, if you use the
SSH command line client, you use the

local user account. So you try
the same username on the remote server.

If you want to use a different user account, you
can use SSH userostname to connect as that specific user.

While you are using ssh, a specific command can
be specified as an argument, like SSH LISA at

remote host who am I? For instance, do notice
if you are running commands that there's a difference

between the following two commands. So, SSH user hostname
who am I greater than? Greater than who fell?

In SSH user hostname SH C who
am I greater than? Greater than who fell?

Does that sound familiar? Of course it does. We have
seen the same behavior if you run a command as

an argument to the sudo command and there's a shell
metacharacter like a redirect or a pipe inside the command.

I'm going to use
SSH student at 192168 29138.

Well, this is the first time I'm connecting with a remote host,
and that means that my local client doesn't know this remote host.

Next time that I'm connecting with this remote
host, we want to do an additional security check.

And in order to do so, we
have the remote host key fingerprint, and

that remote host key fingerprint is what
you see on the screen right here.

It's telling me it doesn't know about this key fingerprint.
And it's asking me if I want to store it. And

yes, I want to store it so that next time
we can verify verify the identity of the remote host.

Now it's asking for the remote user password.
So I'm entering the remote user password, and

So do whatever you want. And once you are done,
you type exit to return to your main operating system.

Related to the SSH
command there is scp.

SCP allows you
to securely copy files.

SCP is a convenient tool that
allows you to copy files from

the local computer to the remote
computer, or the other way around.

The basic command structure is SCP
etchost followed by the remote host IP

address colon some directories. So this
would copy to the TMP directory.

The only condition for SCP to work is that
your SSH server needs to be up and running.

As an alternative to
scp, rsync is commonly used

and rsync uses the
SSH server to synchronize files.

SAP is just a dumb
copy, it doesn't analyze anything.

Rsync synchronizes and that means that if
there are parts that didn't change, these

parts will not be synchronized at
all. And that makes it more efficient.

So you can use rsync for
directories and SCP for individual files.

You use a command like rsync AV
progress. That's nice because you will see a

progress indicator followed by documents, which in
this case will be the local directory.

Studentremote is identifying as which
user on which system and

home student that will synchronize
it to the remote system.

So I'm starting with an SCP
etchosts 219-216-829138 tmp and that will copy

over the host file to the
TMP directory on the remote host.

Then I'm going into documents and I
want to create a couple of files.

So val1 up to
100.txt and that's a lot

of vals. And now
we are going to use

rsync. So rsync minus
AV progress on documents.

And I want to synchronize
two students at 192.168.29.1.38 home student.

Then we need the password of the remote user
and there we can see that it has been synchronized.

So this shows how SCP can be used to copy
individual files and rsync can be used to synchronize complete directories.