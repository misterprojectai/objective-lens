# Mapped Passages: x200_102

**Objective:** 1.2 Use input-output redirection (>, >>, |, 2>, etc.)

**Run date:** 2026-05-08

---

<!-- Source: 01_normalize/output/x200_102/003__8_2_Using_IO_Redirection_and_Piping_en_clean.md -->

about I/O Redirection and Piping.

---

<!-- Source: 01_normalize/output/x200_102/003__8_2_Using_IO_Redirection_and_Piping_en_clean.md -->

Redirection is used to manipulate

---

<!-- Source: 01_normalize/output/x200_102/003__8_2_Using_IO_Redirection_and_Piping_en_clean.md -->

standard input, also known as the zero.

---

<!-- Source: 01_normalize/output/x200_102/003__8_2_Using_IO_Redirection_and_Piping_en_clean.md -->

by the Linux kernel to
take care of redirection.

---

<!-- Source: 01_normalize/output/x200_102/003__8_2_Using_IO_Redirection_and_Piping_en_clean.md -->

And the zero is always
your standard input.

---

<!-- Source: 01_normalize/output/x200_102/003__8_2_Using_IO_Redirection_and_Piping_en_clean.md -->

to take their input from
a file for instance,

---

<!-- Source: 01_normalize/output/x200_102/003__8_2_Using_IO_Redirection_and_Piping_en_clean.md -->

The standard output redirector,

---

<!-- Source: 01_normalize/output/x200_102/003__8_2_Using_IO_Redirection_and_Piping_en_clean.md -->

normally your standard output.

---

<!-- Source: 01_normalize/output/x200_102/003__8_2_Using_IO_Redirection_and_Piping_en_clean.md -->

And you can redirect it
using a greater than sign.

---

<!-- Source: 01_normalize/output/x200_102/003__8_2_Using_IO_Redirection_and_Piping_en_clean.md -->

So if you use ls greater then to ~ myfile

---

<!-- Source: 01_normalize/output/x200_102/003__8_2_Using_IO_Redirection_and_Piping_en_clean.md -->

will override destination
if it already exists.

---

<!-- Source: 01_normalize/output/x200_102/003__8_2_Using_IO_Redirection_and_Piping_en_clean.md -->

if you don't want to override but append

---

<!-- Source: 01_normalize/output/x200_102/003__8_2_Using_IO_Redirection_and_Piping_en_clean.md -->

then you use a double redirect.

---

<!-- Source: 01_normalize/output/x200_102/003__8_2_Using_IO_Redirection_and_Piping_en_clean.md -->

That will add it to the end of the file.

---

<!-- Source: 01_normalize/output/x200_102/003__8_2_Using_IO_Redirection_and_Piping_en_clean.md -->

Also convenient is the option
to redirect standard error.

---

<!-- Source: 01_normalize/output/x200_102/003__8_2_Using_IO_Redirection_and_Piping_en_clean.md -->

In order to redirect standard
error, you use 2 greater than

---

<!-- Source: 01_normalize/output/x200_102/003__8_2_Using_IO_Redirection_and_Piping_en_clean.md -->

in which the 2 is the file descriptor 2

---

<!-- Source: 01_normalize/output/x200_102/003__8_2_Using_IO_Redirection_and_Piping_en_clean.md -->

2 greater than dev null. dev
null is a discard device.

---

<!-- Source: 01_normalize/output/x200_102/003__8_2_Using_IO_Redirection_and_Piping_en_clean.md -->

Anything you send to the dev
null device will be discarded.

---

<!-- Source: 01_normalize/output/x200_102/003__8_2_Using_IO_Redirection_and_Piping_en_clean.md -->

which is using ampersand greater than.

---

<!-- Source: 01_normalize/output/x200_102/003__8_2_Using_IO_Redirection_and_Piping_en_clean.md -->

Now what is ampersand greater than?

---

<!-- Source: 01_normalize/output/x200_102/003__8_2_Using_IO_Redirection_and_Piping_en_clean.md -->

as well as the standard error.

---

<!-- Source: 01_normalize/output/x200_102/003__8_2_Using_IO_Redirection_and_Piping_en_clean.md -->

to the dev null device, but you might want

---

<!-- Source: 01_normalize/output/x200_102/003__8_2_Using_IO_Redirection_and_Piping_en_clean.md -->

to capture all that
information in a specific file.

---

<!-- Source: 01_normalize/output/x200_102/003__8_2_Using_IO_Redirection_and_Piping_en_clean.md -->

What do we get? We get
no output on screen.

---

<!-- Source: 01_normalize/output/x200_102/003__8_2_Using_IO_Redirection_and_Piping_en_clean.md -->

Now, if I use who greater than to lsfile

---

<!-- Source: 01_normalize/output/x200_102/003__8_2_Using_IO_Redirection_and_Piping_en_clean.md -->

then I'm doing an, a standard
output redirection again.

---

<!-- Source: 01_normalize/output/x200_102/003__8_2_Using_IO_Redirection_and_Piping_en_clean.md -->

And if you don't want
to override but append

---

<!-- Source: 01_normalize/output/x200_102/003__8_2_Using_IO_Redirection_and_Piping_en_clean.md -->

The double redirect, as you
can see is adding the output

---

<!-- Source: 01_normalize/output/x200_102/003__8_2_Using_IO_Redirection_and_Piping_en_clean.md -->

of the command to the
file we just created.

---

<!-- Source: 01_normalize/output/x200_102/003__8_2_Using_IO_Redirection_and_Piping_en_clean.md -->

Now, how about the error messages?

---

<!-- Source: 01_normalize/output/x200_102/003__8_2_Using_IO_Redirection_and_Piping_en_clean.md -->

the regular output. Now, what is happening

---

<!-- Source: 01_normalize/output/x200_102/003__8_2_Using_IO_Redirection_and_Piping_en_clean.md -->

So let me create outfile and
write the output to outfile.

---

<!-- Source: 01_normalize/output/x200_102/003__8_2_Using_IO_Redirection_and_Piping_en_clean.md -->

including the error messages.

---

<!-- Source: 01_normalize/output/x200_102/003__8_2_Using_IO_Redirection_and_Piping_en_clean.md -->

We have the file descriptor 1 as well as

---

<!-- Source: 01_normalize/output/x200_102/003__8_2_Using_IO_Redirection_and_Piping_en_clean.md -->

as the file descriptor 2

---

<!-- Source: 01_normalize/output/x200_102/003__8_2_Using_IO_Redirection_and_Piping_en_clean.md -->

So a pipe is used to send
the output of one command

---

<!-- Source: 01_normalize/output/x200_102/003__8_2_Using_IO_Redirection_and_Piping_en_clean.md -->

to be used as input for a second command.

---

<!-- Source: 01_normalize/output/x200_102/003__8_2_Using_IO_Redirection_and_Piping_en_clean.md -->

In combination with the pipe,
you might see the tee command.

---

<!-- Source: 01_normalize/output/x200_102/003__8_2_Using_IO_Redirection_and_Piping_en_clean.md -->

The tee command combines
redirection and piping.

---

<!-- Source: 01_normalize/output/x200_102/003__8_2_Using_IO_Redirection_and_Piping_en_clean.md -->

It allows you to write
the output to somewhere

---

<!-- Source: 01_normalize/output/x200_102/003__8_2_Using_IO_Redirection_and_Piping_en_clean.md -->

and at the same time, use it
as input for another command

---

<!-- Source: 01_normalize/output/x200_102/003__8_2_Using_IO_Redirection_and_Piping_en_clean.md -->

like ps aux, tee psfile, pipe grep ssh.

---

<!-- Source: 01_normalize/output/x200_102/003__8_2_Using_IO_Redirection_and_Piping_en_clean.md -->

Well, I am going to pipe to tee.

---

<!-- Source: 01_normalize/output/x200_102/003__8_2_Using_IO_Redirection_and_Piping_en_clean.md -->

And then I'm going to pipe to grep SSH.

---

<!-- Source: 01_normalize/output/x200_102/003__8_2_Using_IO_Redirection_and_Piping_en_clean.md -->

to a file as well as to the pipe

---

<!-- Source: 01_normalize/output/x200_102/003__8_2_Using_IO_Redirection_and_Piping_en_clean.md -->

analyze what exactly was happening

---

<!-- Source: 01_normalize/output/x200_102/CertGuide_clean.md -->

## I/O Re di rect ion

---

<!-- Source: 01_normalize/output/x200_102/CertGuide_clean.md -->

‐ By de fault, when a com mand is ex e cuted, it shows its re sults on the screen of the com puter you are work ing on. The com puter mon i tor is used as the stan dard des ti na tion for out put, which is also re ferred to as STD OUT. The shell also has de fault stan dard des ti na tions to send er ror mes sages to (STDERR) and to ac cept in put (STDIN). Ta ble 2-2 gives an over view of all three.

---

<!-- Source: 01_normalize/output/x200_102/CertGuide_clean.md -->

Ta ble 2-2 Stan dard In put, Out put, and Er ror Over view

---

<!-- Source: 01_normalize/output/x200_102/CertGuide_clean.md -->

|Name|De fault Des ti na tion|Use in Re di rect ion|File De scrip tor Num ber||
|---|---|---|---|---|
|STDIN|Com puter key board|< (same as 0<)|0||
|||||49|

---

<!-- Source: 01_normalize/output/x200_102/CertGuide_clean.md -->

||Name<br>De fault Des ti na tion<br>Use in Re di rect ion<br>File De scrip tor Num ber<br>STD OUT<br>Com puter mon i tor<br>> (same as 1>)<br>1<br>STDERR<br>Com puter mon i tor<br>2><br>2|
|---|---|
|||
|||
|||

---

<!-- Source: 01_normalize/output/x200_102/CertGuide_clean.md -->

So if you run a com mand, that com mand would ex pect in put from the key board, and it would nor mally send its out put to the mon i tor of your com puter with out mak ing a dis tinc tion be tween nor mal out put and er rors. Some com mands, how ever, are started in the back ground and not from a cur rent ter mi nal ses sion, so these com mands do not have a mon i tor or con sole ses sion to send their out put to, and they do not lis ten to key board in put to ac cept their stan dard in put. That is where re di rect ion comes in handy. Re di rect ion is also use ful if you want to work with in put from an al ter na tive lo ca tion, such as a file.

---

<!-- Source: 01_normalize/output/x200_102/CertGuide_clean.md -->

Pro grams started from the com mand line have no idea what they are read ing from or writ ing to. They just read from what the Linux ker nel calls file de scrip tor 0 if they want to read from stan dard in put, and they write to file de scrip tor num ber 1 to dis play non-er ror out put (also known as "stan dard out put") and to file de scrip ‐ tor 2 if they have er ror mes sages to be out put. By de fault, these fle de scrip tors are con nected to the key board and the screen. If you use re di rect ion sym bols such as <, >, and |, the shell con nects the file de scrip tors to files or other com mands. Let's first look at the redi rec tors < and >. Later we dis cuss pipes (the | sym bol). Ta ‐ ble 2-3 shows the most com mon redi rec tors that are used from the Bash shell.

---

<!-- Source: 01_normalize/output/x200_102/CertGuide_clean.md -->

## Ta ble 2-3 Com mon Bash Redi rec tors

---

<!-- Source: 01_normalize/output/x200_102/CertGuide_clean.md -->

|Redi rec tor|Ex pla na tion|
|---|---|
|> (same as 1>)|Redi rects STD OUT. If re di rect ion is to afle, the cur rent con tents of thatfle are over writ ten.|
|>> (same as 1>>)|Redi rects STD OUT in ap pend mode. If out put is writ ten to afle, the out put is ap pended to thatfle.|
|2>|Redi rects STDERR.|
|2>&1|Redi rects STDERR to the same des ti na tion as STD OUT. No tice that this has to be used in com bi na tion with nor mal out put re di rect ion, as inls whuhiu > er rout 2>&1.|
|< (same as 0<)|Redi rects STDIN.|

---

<!-- Source: 01_normalize/output/x200_102/CertGuide_clean.md -->

In I/O re di rect ion, files can be used to re place the de fault STDIN, STD OUT, and STDERR. You can also re di rect to de vice fles. A de vice file on Linux is a file that is used to ac cess spe cific hard ware. Your hard disk, for in stance, can be re ferred to as /dev/sda in most cases, the con sole of your server is known as /dev/con sole or /dev/tty1, and if you want to dis card a com mand's out put, you can re di rect to /dev/null. Note that to ac cess most de vice files, you need to have root priv i leges.

---

<!-- Source: 01_normalize/output/x200_102/CertGuide_clean.md -->

## Us ing Pipes

---

<!-- Source: 01_normalize/output/x200_102/CertGuide_clean.md -->

Whereas an I/O redi rec tor is used as an al ter na tive for a key board and com puter mon i tor, a pipe can be used to catch the out put of one com mand and use that as in put for a sec ond com mand. If a user runs the com mand ls, for in stance, the out put of the com mand is shown on screen, be cause the screen is the de fault STD OUT. If the user uses ls | less, the com mands ls and less are started in par al lel. The stan dard out put of the ls com mand is con nected to the stan dard in put of less. Ev ery ‐ thing that ls writes to the stan dard out put will be come avail able for read ing from stan dard in put in less. The re sult is that the out put of ls is shown in the less pager, where the user can browse up and down through the re sults eas ily.

---

<!-- Source: 01_normalize/output/x200_102/CertGuide_clean.md -->

As a Linux ad min is tra tor, you will use pipes a lot. Us ing pipes makes Linux a flex i ble op er at ing sys tem; by com bin ing mul ti ple com mands us ing pipes, you can cre ‐ ate "su per" com mands that make al most any thing pos si ble. In Ex er cise 2-2, you use I/O redi rec tors and pipes.

---

<!-- Source: 01_normalize/output/x200_102/CertGuide_clean.md -->

Ex er cise 2-2 Us ing I/O Re di rect ion and Pipes

---

<!-- Source: 01_normalize/output/x200_102/CertGuide_clean.md -->

3. Type ls > /dev/null. This redi rects STD OUT to the null de vice, with the re sult that you will not see it.

---

<!-- Source: 01_normalize/output/x200_102/CertGuide_clean.md -->

4. Type ls il we hgi > /dev/null. This com mand shows a "no such file or di rec tory" mes sage on screen. You see the mes sage be cause it is not STD OUT, but rather an er ror mes sage that is writ ten to STDERR.

---

<!-- Source: 01_normalize/output/x200_102/CertGuide_clean.md -->

5. Type ls il we hgi 2> /dev/null. Now you will no longer see the er ror mes sage.

---

<!-- Source: 01_normalize/output/x200_102/CertGuide_clean.md -->

6. Type ls il we hgi /etc 2> /dev/null. This shows the con tents of the /etc folder while hid ing the er ror mes sage.

---

<!-- Source: 01_normalize/output/x200_102/CertGuide_clean.md -->

7. Type ls il we hgi /etc 2> /dev/null > out put. In this com mand, you still write the er ror mes sage to /dev/null while send ing STD OUT to a file with the name out ‐ put that will be cre ated in your home di rec tory.

---

<!-- Source: 01_normalize/output/x200_102/CertGuide_clean.md -->

9. Type echo hello > out put. This over writes the con tents of the out put file. Ver ify this by us ing cat out put again.

---

<!-- Source: 01_normalize/output/x200_102/CertGuide_clean.md -->

10. Type ls >> out put. This ap pends the re sult of the ls com mand to the out put file. Type cat out put to ver ify.

---

<!-- Source: 01_normalize/output/x200_102/CertGuide_clean.md -->

12. Type ls -R /. | less. This shows the same re sult, but in the less pager, where you can scroll up and down us ing the ar row keys on your key board.

---

<!-- Source: 01_normalize/output/x200_102/CertGuide_clean.md -->

14. Type ls > /dev/tty1. This gives an er ror mes sage be cause you are ex e cut ing the com mand as an or di nary user, and or di nary users can not ad dress de vice files di rectly (un less you were logged in to tty1). Only the user root has per mis sion to write to de vice files di rectly.

---

<!-- Source: 01_normalize/output/x200_102/CertGuide_clean.md -->

51

---

<!-- Source: 01_normalize/output/x200_102/David_Both_clean.md -->

STDIO was developed by Ken Thompson[7] as a part of the infrastructure required to implement pipes on early versions of Unix. Programs that implement STDIO use standardized file handles for input and output rather than files that are stored on a disk or other recording media. STDIO is best described as a buffered data stream, and its primary function is to stream data from the output of one program, file, or device to the input of another program, file, or device. Data streams are the raw materials upon which the core utilities and many other CLI tools perform their work. As its name implies, a data stream is a stream of data being passed from one file, device, or program to another using STDIO.

---

<!-- Source: 01_normalize/output/x200_102/David_Both_clean.md -->

This tenet explores the use of pipes to connect streams of data from one utility program to another using STDIO. The function of these programs is to transform the data in some manner. You will also learn about the use of redirection to redirect the data to a file.

---

<!-- Source: 01_normalize/output/x200_102/David_Both_clean.md -->

Data streams can be manipulated by using pipes to insert transformers into the stream. Each transformer program is used by the SysAdmin to perform some transformational operation on the data in the stream, thus changing its contents in some manner. Redirection can then be used at the end of the pipeline to direct the data stream to a file. As has already been mentioned, that file could be an actual data file on the hard drive or a device file such as a drive partition, a printer, a terminal, a pseudo-terminal, or any other device connected to a computer.

---

<!-- Source: 01_normalize/output/x200_102/David_Both_clean.md -->

I use the term "transform" in conjunction with these programs because the primary task of each is to transform the incoming data from STDIO in a specific way as intended by the SysAdmin and to send the transformed data to STDOUT for possible use by another transformer program or redirection to a file.

---

<!-- Source: 01_normalize/output/x200_102/David_Both_clean.md -->

The ability to manipulate these data streams using these small yet powerful transformer programs is central to the power of the Linux command-line interface. Many of the Linux core utilities are transformer programs and use STDIO.

---

<!-- Source: 01_normalize/output/x200_102/David_Both_clean.md -->

This is one of the most important concepts that makes Linux especially flexible and powerful: everything is a file. That is, everything can be the source of a data stream, the target of a data stream, or in many cases both. In this course you will explore what "everything is a file" really means and learn to use that to your great advantage as a SysAdmin.

---

<!-- Source: 01_normalize/output/x200_102/David_Both_clean.md -->

How to create a new logical volume (LV) for use in the experiments in this chapter How to use pipes, STDIO, and many of the core utilities to manipulate text data streams How to redirect data streams to and from files

---

<!-- Source: 01_normalize/output/x200_102/David_Both_clean.md -->

Everything in Linux revolves around streams of data – particularly text streams.

---

<!-- Source: 01_normalize/output/x200_102/David_Both_clean.md -->

Data streams are the raw materials upon which the core utilities and many other CLI tools perform their work. As its name implies, a data stream is a stream of data – text data – being passed from one file, device, or program to another using Standard Input/Output (STDIO). This chapter introduces the use of pipes to connect streams of data from one filter program to another using STDIO. You will learn that the function of these programs is to transform the data in some manner. You will also learn about the use of redirection to redirect the data to a file. A filter is defined as _A program that processes an input data stream into an output data stream in some well-defined way, and does no I/O to anywhere else except possibly on error conditions; one designed to be used as a stage in a pipeline._ —The Free On-line Dictionary of Computing (FOLDOC) Data streams can be manipulated by inserting one or more filter programs into the stream using pipes. Each filter is used by the SysAdmin to perform some operation on the data in the stream, thus changing its contents in some welldefined manner. Redirection can then be used at the end of the pipeline to direct the data stream to a file. As has already been mentioned, that file could be an actual data file on the hard drive or a device file such as a drive partition, a printer, a terminal, a pseudo-terminal, or any other device[1] connected to a computer. The ability to manipulate these data streams using these small yet powerful filters is central to the power of the Linux command-line interface. Many of the core utilities are filter programs and use STDIO. I recently Googled "data stream," and most of the top hits are concerned with processing huge amounts of streaming data in single entities such as streaming video and audio or financial institutions processing streams consisting of huge numbers of individual transactions. This is not what we are talking about here although the concept is the same, and a case could be made that current applications use the stream processing functions of Linux as the model for processing many types of data. In the Linux world, a stream is a flow of text data that originates at some source; the stream may flow to one or more programs that transform it in some way, and then it may be stored in a file or displayed in a terminal session. As a SysAdmin your job is intimately associated with manipulating the creation and flow of these data streams. In this chapter we will explore data streams – what they are, how to create them, and a little bit about how to use them. **Text Streams: A Universal Interface** The use of Standard Input/Output (STDIO) for program input and output is a key foundation of the Linux way of doing things. STDIO was first developed for Unix and has found its way into most other operating systems since then, including DOS, Windows, and Linux. _This is the Unix philosophy: Write programs that do one thing and do it well. Write programs to work together. Write programs to handle text streams, because that is a universal interface._ —Doug McIlroy, Basics of the Unix Philosophy[2][,][3]

---

<!-- Source: 01_normalize/output/x200_102/David_Both_clean.md -->

STDIO was developed by Ken Thompson[4] as a part of the infrastructure required to implement pipes on early versions of Unix. Programs that implement STDIO use standardized file handles for input and output rather than files that are stored on a disk or other recording media. STDIO is best described as a buffered data stream, and its primary function is to stream data from the output of one program, file, or device to the input of another program, file, or device. **STDIO File Handles** There are three STDIO data streams, each of which is automatically opened as a file at the startup of a program – well, those programs that use STDIO. Each STDIO data stream is associated with a file handle, which is just a set of metadata that describes the attributes of the file. File handles 0, 1, and 2 are explicitly defined by convention and long practice as STDIN, STDOUT, and STDERR, respectively. **STDIN** , file handle 0, is standard input, which is usually input from the keyboard. STDIN can be redirected from any file including device files instead of the keyboard. It is not common to need to redirect STDIN, but it can be done. **STDOUT** , file handle 1, is standard output, which sends the data stream to the terminal by default. It is common to redirect STDOUT to a file or to pipe it to another program for further processing. **STDERR** is associated with file handle 2. The data stream for STDERR is also usually sent to the terminal. If STDOUT is redirected to a file, STDERR continues to be displayed on the screen. This ensures that when the data stream itself is not displayed on the terminal, that STDERR is, thus, ensuring that the user will see any errors resulting from execution of the program. STDERR can also be redirected to the same or passed on to the next filter program in a pipeline. STDIO is implemented in a standard C library header file, stdio.h, which can be included in the source code of programs so that it can be compiled into the resulting executable.

---

<!-- Source: 01_normalize/output/x200_102/David_Both_clean.md -->

`[root@studentvm1 ~]#` **`systemctl daemon-reload`** The last step is to mount the new filesystem: `[root@studentvm1 ~]#` **`mount /test ; lsblk`** `NAME                       MAJ:MIN RM  SIZE RO TYPE MOUNTPOINTS sda                          8:0    0   60G  0 disk |-sda1                       8:1    0    1M  0 part |-sda2                       8:2    0    1G  0 part /boot |-sda3                       8:3    0    1G  0 part /boot/efi `-sda4                       8:4    0   58G  0 part |-fedora_studentvm1-root 253:0    0    2G  0 lvm  / |-fedora_studentvm1-usr  253:1    0   15G  0 lvm  /usr |-fedora_studentvm1-tmp  253:2    0    5G  0 lvm  /tmp |-fedora_studentvm1-var  253:3    0   10G  0 lvm  /var |-fedora_studentvm1-home 253:4    0    2G  0 lvm  /home `-fedora_studentvm1-test 253:5    0  500M  0 lvm  /test sr0                         11:0    1 50.5M  0 rom zram0                      252:0    0    8G  0 disk [SWAP] [root@studentvm1 ~]#` Enter and run the following command-line program to create some files with content on the drive. We use the dmesg command simply to provide data for the files to contain. The contents don't matter so much as just the fact that each file has some content: `[root@studentvm1 ~]#` **`cd /test`** `[root@studentvm1 test]#` **`for I in 0 1 2 3 4 5 6 7 8 9 ; do dmesg > file$I.txt ; done`**

---

<!-- Source: 01_normalize/output/x200_102/David_Both_clean.md -->

Most of the core utilities use STDIO as their output stream, and those that generate data streams, rather than acting to transform the data stream in some way, can be used to create the data streams that we will use for our experiments. Data streams can be as short as one line or even a single character and as long as needed.[9]

---

<!-- Source: 01_normalize/output/x200_102/David_Both_clean.md -->

The output from this command is a short data stream that is displayed on STDOUT, the console or terminal session that you are logged into.

---

<!-- Source: 01_normalize/output/x200_102/David_Both_clean.md -->

```
[student@studentvm1 test]$ yes 123465789-abcdefg
123465789-abcdefg
123465789-abcdefg
123465789-abcdefg
123465789-abcdefg
123465789-abcdefg
123465789-abcdefg
123465789-abcdefg
1234^C
```

---

<!-- Source: 01_normalize/output/x200_102/David_Both_clean.md -->

I haven't talked about pipes yet, but as a SysAdmin, or someone who wants to become one, you should know how to use them. The following CLI program will supply the response of "y" to each request by the rm command and will delete all of the files in the PWD.

---

<!-- Source: 01_normalize/output/x200_102/David_Both_clean.md -->

- `[root@studentvm1 test]#` **`yes | rm file*txt ; ll`**

---

<!-- Source: 01_normalize/output/x200_102/David_Both_clean.md -->

```
[root@studentvm1 test]# for I in `seq 0 9` ; do dmesg > file$I.txt ; done ; ll
```

---

<!-- Source: 01_normalize/output/x200_102/David_Both_clean.md -->

Place this terminal session somewhere on your desktop so that you can see it; then, as root open another terminal session and run the command shown in the following. Depending upon the size of your USB filesystem, the time to fill it may vary, but it should be quite fast on a small-capacity test volume. The first time I tested this, it took 18 minutes and 55 seconds on my system with a 4GB USB device. Note that we are redirecting a long data stream. Watch the /dev/sdb1 filesystem on /test as it fills up:

---

<!-- Source: 01_normalize/output/x200_102/David_Both_clean.md -->

```
[root@studentvm1 test]# yes 123456789-abcdefgh >> /test/testfile.txt
yes: standard output: No space left on device
[root@studentvm1 test]#
```

---

<!-- Source: 01_normalize/output/x200_102/David_Both_clean.md -->

```
[root@studentvm1 ~]# dd if=/dev/sda4 bs=512 count=2000 | less
```

---

<!-- Source: 01_normalize/output/x200_102/David_Both_clean.md -->

Page down until you see something like this:

---

<!-- Source: 01_normalize/output/x200_102/David_Both_clean.md -->

Perform this experiment as the student user. Enter this command to print an unending stream of random data to STDIO:

---

<!-- Source: 01_normalize/output/x200_102/David_Both_clean.md -->

Use **Ctrl-C** to break out and stop the stream of data. You may need to use **Ctrl-C** multiple times. If you are extremely paranoid, the **`shred`** command can be used to overwrite individual files as well as partitions and complete drives. It can write over the device as many times as needed for you to feel secure, with multiple passes using both random data and specifically sequenced patterns of data designed to prevent even the most sensitive equipment from recovering any data from the hard drive. As with other utilities that use random data, the random stream is supplied by the /dev/urandom device. Random data is also used as the input seed to programs that generate random passwords and random data and numbers for use in scientific and statistical calculations. We will cover randomness and other interesting data sources in a bit more detail in Volume 2, Chapter 22. **Pipe Dreams** Pipes are critical to our ability to do the amazing things on the command line, so much so that I think it is important to recognize that they were invented by Douglas McIlroy[12] during the early days of Unix. Thanks, Doug! The Princeton University website has a fragment of an interview[13] with McIlroy in which he discusses the creation of the pipe and the beginnings of the Unix Philosophy. Notice the use of pipes in the simple command-line program shown in Experiment 9-10 that lists each logged-in user a single time no matter how many logins they have active.

---

<!-- Source: 01_normalize/output/x200_102/David_Both_clean.md -->

## **EXPERIMENT 9-10: INTRODUCING PIPES**

---

<!-- Source: 01_normalize/output/x200_102/David_Both_clean.md -->

`[student@studentvm1 test]$` **`w | tail -n +3 | awk '{print $1}' | sort | uniq`** `root student [student@studentvm1 test]$` The results from this command produce two lines of data that show that the users root and student are both logged in. It does not show how many times each user is logged in. Pipes – represented by the vertical bar ( | ) – are the syntactical glue, the operator, that connects these command-line utilities together. Pipes allow the standard output from one command to be "piped," that is, streamed from the standard output of one command to the standard input of the next command. The |& operator can be used to pipe STDERR along with STDOUT to STDIN of the next command. This is not always desirable, but it does offer flexibility in the ability to record the STDERR data stream for the purposes of problem determination. A string of programs connected with pipes is called a pipeline. Think about how this program would have to work if we could not pipe the data stream from one command to the next. The first command would perform its task on the data, and then the output from that command would have to be saved in a file. The next command would have to read the stream of data from the intermediate file and perform its modification of the data stream, sending its own output to a new, temporary data file. The third command would have to take its data from the second temporary data file and perform its own manipulation of the data stream and then store the resulting data stream in yet another temporary file. At each step the data file names would have to be transferred from one command to the next in some way. I cannot even stand to think about that because it is so complex. Remember that simplicity rocks! **Building Pipelines** When I am doing something new, solving a new problem, I usually do not just type in a complete bash command pipeline from scratch, as in Experiment 9-10 off the top of my head. I usually start with just one or two commands in the pipeline and build from there by adding more commands to further process the data stream. This allows me to view the state of the data stream after each of the commands in the pipeline and make corrections as they are needed. In Experiment 9-11 you should enter the command shown on each line and run it as shown to see the results. This will give you a feel for how you can build up complex pipelines in stages. **EXPERIMENT 9-11: BUILDING A PIPELINE** Enter the commands as shown on each line. Observe the changes in the data stream as each new filter utility is inserted to the data stream using the pipe. Log in as root to two of the Linux virtual consoles and as the student user to two additional virtual consoles, and open several terminal sessions on the desktop. This should give plenty of data for this experiment: `[student@studentvm1 test]$` **`w`** `[student@studentvm1 test]$` **`w | tail -n +3`** `[student@studentvm1 test]$` **`w | tail -n +3 | awk '{print $1}'`** `[student@studentvm1 test]$` **`w | tail -n +3 | awk '{print $1}' | sort`** `[student@studentvm1 test]$` **`w | tail -n +3 | awk '{print $1}' | sort | uniq`**

---

<!-- Source: 01_normalize/output/x200_102/David_Both_clean.md -->

It is possible to build up very complex pipelines that can transform the data stream using many different utilities that work with STDIO.

---

<!-- Source: 01_normalize/output/x200_102/David_Both_clean.md -->

## **Redirection**

---

<!-- Source: 01_normalize/output/x200_102/David_Both_clean.md -->

Redirection is the capability to redirect the STDOUT data stream of a program to a file instead of to the default target of the display. The "greater than" ( > ) character, a.k.a. "gt", is the syntactical symbol for redirection. Experiment 9-12 shows how to redirect the output data stream of the `df -h` command to the file diskusage.txt.

---

<!-- Source: 01_normalize/output/x200_102/David_Both_clean.md -->

**EXPERIMENT 9-12: REDIRECTING STDOUT**

---

<!-- Source: 01_normalize/output/x200_102/David_Both_clean.md -->

Redirecting the STDOUT of a command can be used to create a file containing the results from that command:

---

<!-- Source: 01_normalize/output/x200_102/David_Both_clean.md -->

```
[student@studentvm1 test]$ df -h > diskusage.txt
```

---

<!-- Source: 01_normalize/output/x200_102/David_Both_clean.md -->

There is no output to the terminal from this command unless there is an error. This is because the STDOUT data stream is redirected to the file and STDERR is still directed to the STDOUT device, which is the display. You can view the contents of the file you just created using this next command: `[student@studentvm1 test]$` **`cat diskusage.txt`** `Filesystem                          Size  Used Avail Use% Mounted on devtmpfs                            2.0G     0  2.0G   0% /dev tmpfs                               2.0G     0  2.0G   0% /dev/shm tmpfs                               2.0G  1.2M  2.0G   1% /run tmpfs                               2.0G     0  2.0G   0% /sys/fs/cgroup /dev/mapper/fedora_studentvm1-root  2.0G   49M  1.8G   3% / /dev/mapper/fedora_studentvm1-usr    15G  3.8G   11G  27% /usr /dev/sda1                           976M  185M  724M  21% /boot /dev/mapper/fedora_studentvm1-tmp   4.9G   21M  4.6G   1% /tmp /dev/mapper/fedora_studentvm1-var   9.8G  504M  8.8G   6% /var /dev/mapper/fedora_studentvm1-home  2.0G  7.3M  1.8G   1% /home tmpfs                               395M  8.0K  395M   1% /run/user/1000 tmpfs                               395M     0  395M   0% /run/user/0 /dev/sdb1                            60M  440K   59M   1% /test [student@studentvm1 test]$`

---

<!-- Source: 01_normalize/output/x200_102/David_Both_clean.md -->

When using the > symbol for redirection, the specified file is created if it does not already exist. If it already does exist, the contents are overwritten by the data stream from the command. You can use double greater than symbols, >>, to append the new data stream to any existing content in the file as illustrated in Experiment 9-13.

---

<!-- Source: 01_normalize/output/x200_102/David_Both_clean.md -->

## **EXPERIMENT 9-13: APPENDING REDIRECTED DATA STREAMS**

---

<!-- Source: 01_normalize/output/x200_102/David_Both_clean.md -->

This command appends the new data stream to the end of the existing file:

---

<!-- Source: 01_normalize/output/x200_102/David_Both_clean.md -->

`[student@studentvm1 test]$` **`df -h >> diskusage.txt`** You can use cat and/or less to view the diskusage.txt file in order to verify that the new data was appended to the end of the file. The < (less than) symbol redirects data to the STDIN of the program. You might want to use this method to input data from a file to STDIN of a command that does not take a file name as an argument but that does use STDIN. Although input sources can be redirected to STDIN, such as a file that is used as input to **`grep`** , it is generally not necessary as **`grep`** also takes a file name as an argument to specify the input source. Most other commands also take a file name as an argument for their input source. One example of using redirection to STDIN is with the **`od`** command as shown in Experiment 9-14. The -N 50 option prevents the output from continuing forever. You could use Ctrl-C to terminate the output data stream if you don't use the -N option to limit it.

---

<!-- Source: 01_normalize/output/x200_102/David_Both_clean.md -->

**EXPERIMENT 9-14: REDIRECTING STDIN** This experiment illustrates the use of redirection as input to STDIN: `[student@studentvm1 test]$` **`od -c -N 50 < /dev/urandom`** `0000000  331  203    _  307    ]    {  335  337    6  257  347         $    J    Z    U 0000020  245   \0    `   \b    8  307  261  207    K    :    }    S    \  276  344    ; 0000040  336  256  221  317  314  241  352    `  253  333  367  003  374  264  335    4 0000060    U   \n  347    (    h  263  354  251    u    H    ]  315  376    W  205   \0 0000100  323  263  024    %  355  003  214  354  343    \    a  254    #    `    {    _ 0000120    b  201  222    2  265    [  372  215  334  253  273  250    L    c  241  233 <snip>` It is much easier to understand the nature of the results when formatted using **`od`** (Octal Display), which formats the data stream in a way that is a bit more intelligible. Read the man page for **`od`** for more information.

---

<!-- Source: 01_normalize/output/x200_102/David_Both_clean.md -->

Redirection can be the source or the termination of a pipeline. Because it is so seldom needed as input, redirection is usually used as termination of a pipeline.

---

<!-- Source: 01_normalize/output/x200_102/David_Both_clean.md -->

- **EXPERIMENT 9-15: USING ECHO TO GENERATE TEXT STREAMS** Perform this experiment as the student user. This activity provides examples of some aspects of redirection not yet covered. The **`echo`** command is used to print text strings to STDOUT. Make your home directory the PWD and create a small text file:

---

<!-- Source: 01_normalize/output/x200_102/David_Both_clean.md -->

- `[student@studentvm1 test]$` **`echo "Hello world" > hello.txt`** Read the contents of the file by redirecting it to STDIN:

---

<!-- Source: 01_normalize/output/x200_102/David_Both_clean.md -->

- `[student@studentvm1 test]$` **`cat < hello.txt`** `Hello world [student@studentvm1 test]$` Add another line of text to the existing file:

---

<!-- Source: 01_normalize/output/x200_102/David_Both_clean.md -->

- `[student@studentvm1 test]$` **`echo "How are you?" >> hello.txt`** View the contents:

---

<!-- Source: 01_normalize/output/x200_102/David_Both_clean.md -->

- `[student@studentvm1 test]$` **`echo "Hello world" >> hello.txt ; ll`** Verify that the file was recreated using the ls and cat commands: Note that in this last case, the >> operator created the file because it did not exist. If it has already existed, the line would have been added at the end of the existing file as it was in step 4. Also notice the quotes are standard ASCII

---

<!-- Source: 01_normalize/output/x200_102/David_Both_clean.md -->

**Just grepping Around** The **`grep`** command is used to select lines that match a specified pattern from a stream of data. **`grep`** is one of the most commonly used filter utilities and can be used in some very creative and interesting ways. The **`grep`** command is one of the few that can correctly be called a filter because it does filter out all the lines of the data stream that you do not want; it leaves only the lines that you do want in the remaining data stream. According to Klaatu, my reviewer for Volume 3 of this course, "One of the classic Unix commands, developed way back in 1974 by Ken Thompson, is the Global Regular Expression Print (grep) command. It's so ubiquitous in computing that it's frequently used as a verb ('grepping through a file') and, depending on how geeky your audience, it fits nicely into real-world scenarios, too. (For example, 'I'll have to grep my memory banks to recall that information.') In short, grep is a way to search through a file for a specific pattern of characters. If that sounds like the modern Find function available in any word processor or text editor, then you've already experienced grep's effects on the computing industry."[14]

---

<!-- Source: 01_normalize/output/x200_102/David_Both_clean.md -->

**EXPERIMENT 9-16: INTRODUCING GREP** We need to create a file with some random data in it. We can use a tool that generates random passwords, but we first need to install it as root: **`dnf -y install pwgen`** Now as the student user, let's generate some random data and create a file with it. If the PWD is not /test, make it so. The following command creates a stream of 5000 lines of random data that are each 75 characters long and stores them in the random.txt file: **`pwgen 75 5000 > random.txt`** Considering that there are so many passwords, it is very likely that some character strings in them are the same. Use the grep command to locate some short, randomly selected strings from the last ten passwords on the screen. I saw the words "see" and "loop" in one of those ten passwords, so my command looked like this: **`grep see random.txt`** You can try that, but you should also pick some strings of your own to check. Short strings of two to four characters work best. Use the grep filter to locate all of the lines in the output from dmesg with CPU in them: **`dmesg | grep cpu`** List all of the directories in your home directory with the command **`ls -la | grep ^d`** This works because each directory has a "d" as the first character in a long listing. The caret ( ^ ) is used by grep and other tools to anchor the text being searched to the beginning of the line. To list all of the files that are not directories, reverse the meaning of the previous grep command with the -v option: **`ls -la | grep -v ^d`**

---

<!-- Source: 01_normalize/output/x200_102/David_Both_clean.md -->

It is only with the use of pipes, pagers, and redirection that many of the amazing and powerful tasks that can be performed on the Linux command line are possible. It is the pipes that transport STDIO data streams from one program or file to another. In this chapter you have learned that piping streams of data through one or more filter programs supports powerful and flexible manipulation of data in those streams.

---

<!-- Source: 01_normalize/output/x200_102/David_Both_clean.md -->

Each of the programs in the pipelines demonstrated in the experiments is small, and each does one thing well. They are also filters, that is, they take the standard input, process it in some way, and then send the result to the standard output. Implementation of these programs as filters to send processed data streams from their own standard output to the standard input of the other programs is complementary to and necessary for the implementation of pipes as a Linux tool.

---

<!-- Source: 01_normalize/output/x200_102/David_Both_clean.md -->

Do the following exercises to complete this chapter: 1. What is the function of the greater than symbol (> )? 2. Is it possible to append the content of a data stream to an existing file?

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

## **Chapter 1. Combining Commands**

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

What if you need to do something more complicated? Don't worry. Linux makes it easy to _combine commands_ so their individual features work together to accomplish your goal. This way of working yields a very different mindset about computing. Instead of asking "Which app should I launch?" to achieve some result, the question becomes "Which commands should I combine?"

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

You'll combine commands using _pipes_ , a Linux feature that connects the output of one command to the input of another. As I introduce each command ( wc , head , cut , grep , sort , and uniq ), I'll immediately demonstrate its use with pipes. Some examples will be practical for daily Linux use, while others are just toy examples to demonstrate an important feature.

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

## **Input, Output, and Pipes**

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

Most Linux commands read input from the keyboard, write output to the screen, or both. Linux has fancy names for this reading and writing:

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

_stdin (pronounced "standard input" or "standard in")_

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

The stream of input that Linux reads from your keyboard. When you type any command at a prompt, you're supplying data on stdin.

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

_stdout (pronounced "standard output" or "standard out")_

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

The stream of output that Linux writes to your display. When you run the ls command to print filenames, the results appear on stdout.

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

Now comes the cool part. You can connect the stdout of one command to the stdin of another, so the first command feeds the second. Let's begin with the familiar ls -l command to list a large directory, such as _/bin_ , in long format:

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

This directory contains far more files than your display has lines, so the output quickly scrolls off-screen. It's a shame that ls can't print the information one screenful at a time, pausing until you press a key to continue. But wait: another Linux command has that feature. The less command displays a file one screenful at a time:

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

You can connect these two commands because ls writes to stdout and less can read from stdin. Use a pipe to send the output of ls to the input of less :

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

$ **`ls -l /bin | less`**

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

This combined command displays the directory's contents one screenful at a time. The vertical bar ( | ) between the commands is the Linux pipe symbol.[1] It connects the first command's stdout to the next command's stdin. Any command line containing pipes is called a _pipeline_ .

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

Commands generally are not aware that they're part of a pipeline. ls believes it's writing to the display, when in fact its output has been redirected to less . And less believes it's reading from the keyboard when it's actually reading the output of ls .

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

Several simple commands treated as a unit, such as the pipeline ls -l /bin | less

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

Pipes are an essential part of Linux expertise. Let's dive into building your piping skills with a small set of Linux commands so no matter which ones you encounter later, you're ready to combine them.

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

The six commands— wc , head , cut , grep , sort , and uniq —have numerous options and modes of operation that I'll largely skip for now to focus on pipes. To learn more about any command, run the man command to display full documentation. For example:

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

$ **`wc animals.txt`** 7  51 325 animals.txt

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

Counting is such a useful, general-purpose task that the authors of wc designed the command to work with pipes. It reads from stdin if you omit the filename, and it writes to stdout. Let's use ls to list the contents of the current directory and pipe them to wc to count lines. This pipeline answers the question, "How many files are visible in my current directory?"

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

$ **`ls -1`** animals.txt myfile myfile2 test.py $ **`ls -1 | wc -l`** 4

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

The option -1 , which tells ls to print its results in a single column, is not strictly necessary here. To learn why I used it, see the sidebar "ls Changes Its Behavior When Redirected".

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

wc is the first command you've seen in this chapter, so you're a bit limited in what you can do with pipes. Just for fun, pipe the output of wc to itself, demonstrating that the same command can appear more than once in a pipeline. This combined command reports that the number of words in the output of wc is four: three integers and a filename:

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

$ **`wc animals.txt`** 7  51 325 animals.txt $ **`wc animals.txt | wc -w`** 4

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

$ **`wc animals.txt | wc -w | wc`** 1       1       2

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

## **LS CHANGES ITS BEHAVIOR WHEN REDIRECTED**

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

Unlike virtually every other Linux command, ls is aware of whether stdout is the screen or whether it's been redirected (to a pipe or otherwise). The reason is user-friendliness. When stdout is the screen, ls arranges its output in multiple columns for convenient reading:

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

When stdout is redirected, however, ls produces a single column. I'll demonstrate this by piping the output of ls to a command that simply reproduces its input, such as cat :[3]

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

$ **`ls /bin | cat`** bash bsd-csh bunzip2 busybox ⋮

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

$ **`ls`** animals.txt   myfile   myfile2    test.py $ **`ls | wc -l`** 4

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

By itself, head is handy for peeking at the top of a file when you don't care about the rest of the contents. It's a speedy and efficient command, even for very large files, because it needn't read the whole file. In addition, head writes to stdout, making it useful in pipelines. Count the number of words in the first three lines of _animals.txt_ :

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

$ **`head -n3 animals.txt | wc -w`** 20

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

head can also read from stdin for more pipeline fun. A common use is to reduce the output from another command when you don't care to see all of it, like a long directory listing. For example, list the first five filenames in the _/bin_ directory:

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

$ **`ls /bin | head -n5`** bash bsd-csh bunzip2 busybox bzcat

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

To shorten the output, pipe it to head to print only the first three lines:

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

$ **`cut -f2 animals.txt | head -n3`** Programming Python SSH, The Secure Shell Intermediate Perl

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

$ **`cut -f1,3 animals.txt | head -n3`** python 2010 snail 2005 alpaca 2012

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

or by numeric range:

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

$ **`cut -f2-4 animals.txt | head -n3`** Programming Python 2010 Lutz, Mark SSH, The Secure Shell 2005 Barrett, Daniel Intermediate Perl 2012 Schwartz, Randal

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

Now that you've seen the basic functionality, try something more practical with cut and pipes. Imagine that the _animals.txt_ file is thousands of lines long, and you need to extract just the authors' last names. First, isolate the fourth field, author name:

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

Then pipe the results to cut again, using the option -d (meaning "delimiter") to change the separator character to a comma instead of a tab, to isolate the authors' last names:

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

grep reads stdin and writes stdout, making it great for pipelines. Suppose you want to know how many subdirectories are in the large directory _/usr/lib_ . There is no single Linux command to provide that answer, so construct a pipeline. Begin with the ls -l command:

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

$ **`ls -l /usr/lib | cut -c1`** d d d - - ⋮

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

Then use grep to keep only the lines containing d :

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

$ **`ls -l /usr/lib | cut -c1 | grep d`** d d d ⋮

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

Finally, count lines with wc , and you have your answer, produced by a four-command pipeline— _/usr/lib_ contains 145 subdirectories:

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

$ **`ls -l /usr/lib | cut -c1 | grep d | wc -l`** 145

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

sort can order the lines alphabetically (the default) or numerically (with the -n option). I'll demonstrate this with pipelines that cut the third field in _animals.txt_ , the year of publication:

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

$ **`cut -f3 animals.txt`** _`Unsorted`_ 2010 2005 2012 2014 2009 2005 1999 $ **`cut -f3 animals.txt | sort -n`** _`Ascending`_ 1999 2005 2005 2009 2010 2012 2014 $ **`cut -f3 animals.txt | sort -nr`** _`Descending`_ 2014 2012 2010 2009 2005 2005 1999

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

To learn the year of the most recent book in _animals.txt_ , pipe the output of sort to the input of head and print just the first line:

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

$ **`cut -f3 animals.txt | sort -nr | head -n1`** 2014

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

sort and head are powerful partners when working with numeric data, one value per line. You can print the maximum value by piping the data to:

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

... | sort -nr | head -n1 and print the minimum value with: ... | sort -n | head -n1

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

$ **`head -n5 /etc/passwd | cut -d: -f1`** root daemon bin smith jones

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

and sort them:

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

$ **`head -n5 /etc/passwd | cut -d: -f1 | sort`** bin daemon jones root smith

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

$ **`cat /etc/passwd | cut -d: -f1 | sort`**

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

$ **`cut -d: -f1 /etc/passwd | grep -w jones`** jones $ **`cut -d: -f1 /etc/passwd | grep -w rutabaga`** _`(produces no output)`_

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

$ **`cut -f1 grades | sort`** A A A B B B B C C D F

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

$ **`cut -f1 grades | sort | uniq -c`** 3 A

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

$ **`cut -f1 grades | sort | uniq -c | sort -nr | head -n1`** 4 B

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

and there's your answer, thanks to a six-command pipeline—our longest yet. This sort of step-by-step pipeline construction is not just an educational exercise. It's how Linux experts actually work. Chapter 8 is devoted to this technique.

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

You can answer this question with a pipeline. You'll need another command, md5sum , which examines a file's contents and computes a 32-character string called a _checksum_ :

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

Duplicate checksums are easy to detect by eye when there are only three files, but what if you have three thousand? It's pipes to the rescue. Compute all the checksums, use cut to isolate the first 32 characters of each line, and sort the lines to make any duplicates adjacent:

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

$ **`md5sum *.jpg | cut -c1-32 | sort`** 1258012d57050ef6005739d0e6f6a257 146b163929b6533f02e91bdf21cb9563 146b163929b6533f02e91bdf21cb9563 17f339ed03733f402f74cf386209aeb3 ⋮

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

$ **`md5sum *.jpg | cut -c1-32 | sort | uniq -c`** 1 1258012d57050ef6005739d0e6f6a257 2 146b163929b6533f02e91bdf21cb9563 1 17f339ed03733f402f74cf386209aeb3 ⋮

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

$ **`md5sum *.jpg | cut -c1-32 | sort | uniq -c | sort -nr`** 3 f6464ed766daca87ba407aede21c8fcc

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

2 c7978522c58425f6af3f095ef1de1cd5

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

> 2 146b163929b6533f02e91bdf21cb9563

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

1 d8ad913044a51408ec1ed8a204ea9502 ⋮

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

- $ **`md5sum *.jpg | cut -c1-32 | sort | uniq -c | sort -nr | grep -v "      1 "`** 3 f6464ed766daca87ba407aede21c8fcc 2 c7978522c58425f6af3f095ef1de1cd5 2 146b163929b6533f02e91bdf21cb9563

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

Finally, you have your list of duplicate checksums, sorted by the number of occurrences, produced by a beautiful sixcommand pipeline. If it produces no output, there are no duplicate files.

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

$ **`md5sum *.jpg | grep 146b163929b6533f02e91bdf21cb9563`** 146b163929b6533f02e91bdf21cb9563  image001.jpg 146b163929b6533f02e91bdf21cb9563  image003.jpg

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

$ **`md5sum *.jpg | grep 146b163929b6533f02e91bdf21cb9563 | cut -c35-`** image001.jpg image003.jpg

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

## **Summary**

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

You've now seen the power of stdin, stdout, and pipes. They turn a small handful of commands into a collection of composable tools, proving that the whole is greater than the sum of the parts. _Any_ command that reads stdin or writes stdout can participate in pipelines.[6] As you learn more commands, you can apply the general concepts from this chapter to forge your own powerful combinations.

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

- 1 On US keyboards, the pipe symbol is on the same key as the backslash ( \ ), usually located between the Enter and Backspace keys or between the left Shift key and Z.

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

- 3 Depending on your setup, ls may also use other formatting features, such as color, when printing to the screen but not when redirected.

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

- 6 Some commands do not use stdin/stdout and therefore cannot read from pipes or write to pipes. Examples are mv and rm . Pipelines may incorporate these commands in other ways, however; you'll see examples in Chapter 8.

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

## **Redirecting Input and Output**

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

The shell controls the input and output of the commands it runs. You've already seen one example: pipes, which direct the stdout of one command to the stdin of another. The pipe syntax, | , is a feature of the shell.

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

Another shell feature is redirecting stdout to a file. For example, if you use grep to print matching lines from the _animals.txt_ file from Example 1-1, the command writes to stdout by default:

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

You can send that output to a file instead, using a shell feature called _output redirection_ . Simply add the symbol > followed by the name of a file to receive the output:

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

$ **`grep Perl animals.txt > outfile`** _`(displays no output)`_ $ **`cat outfile`** alpaca Intermediate Perl 2012 Schwartz, Randal

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

You have just redirected stdout to the file _outfile_ instead of the display. If the file _outfile_ doesn't exist, it's created. If it does exist, redirection overwrites its contents. If you'd rather append to the output file rather than overwrite it, use

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

the symbol >> instead:

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

$ **`grep Perl animals.txt > outfile`** _`Create or overwrite outfile`_ $ **`echo There was just one match >> outfile`** _`Append to outfile`_ $ **`cat outfile`** alpaca Intermediate Perl 2012 Schwartz, Randal There was just one match

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

Output redirection has a partner, _input redirection_ , that redirects stdin to come from a file instead of the keyboard. Use the symbol < followed by a filename to redirect stdin.

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

Many Linux commands that accept filenames as arguments, and read from those files, also read from stdin when run with no arguments. An example is wc for counting lines, words, and characters in a file:

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

$ **`wc animals.txt`** 7  51 325 animals.txt $ **`wc < animals.txt`** 7  51 325

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

## **STANDARD ERROR (STDERR) AND REDIRECTION**

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

In your day-to-day Linux use, you may notice that some output cannot be redirected by > , such as certain error messages. For example, ask cp to copy a file that doesn't exist, and it produces this error message:

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

$ **`cp nonexistent.txt file.txt`** cp: cannot stat 'nonexistent.txt': No such file or directory

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

If you redirect the output (stdout) of this cp command to a file, _errors_ , the message still appears on-screen:

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

$ **`cp nonexistent.txt file.txt > errors`** cp: cannot stat 'nonexistent.txt': No such file or directory

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

and the file _errors_ is empty:

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

Why does this happen? Linux commands can produce more than one stream of output. In addition to stdout, there is also stderr (pronounced "standard error" or "standard err"), a second stream of output that is traditionally reserved for error messages. The streams stderr and stdout look identical on the display, but internally they are separate. You can redirect stderr with the symbol 2> followed by a filename:

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

$ **`cp nonexistent.txt file.txt 2> errors`** $ **`cat errors`** cp: cannot stat 'nonexistent.txt': No such file or directory

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

2>> and append stderr to a file with followed by a filename:

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

$ **`cp nonexistent.txt file.txt 2> errors`** $ **`cp another.txt file.txt 2>> errors`** $ **`cat errors`** cp: cannot stat 'nonexistent.txt': No such file or directory cp: cannot stat 'another.txt': No such file or directory

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

To redirect both stdout and stderr to the same file, use &> followed by a filename:

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

$ **`echo This file exists > goodfile.txt`** _`Create a file`_ $ **`cat goodfile.txt nonexistent.txt &> all.output`** $ **`cat all.output`** This file exists cat: nonexistent.txt: No such file or directory

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

In the second command, wc is invoked with no arguments, so it reads from stdin, which is usually the keyboard. The shell, however, sneakily redirects stdin to come from _animals.txt_ instead. wc has no idea that the file _animals.txt_ exists.

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

The shell can redirect input and output in the same command:

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

$ **`wc < animals.txt > count`** $ **`cat count`**

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

and can even use pipes at the same time. Here, grep reads from redirected stdin and pipes the results to wc , which writes to redirected stdout, producing the file _count_ :

---

<!-- Source: 01_normalize/output/x200_102/Efficient_cli_clean.md -->

$ **`grep Perl < animals.txt | wc > count`** $ **`cat count`** 1       6      47

---

<!-- Source: 01_normalize/output/x200_102/How_Linux_Works_clean.md -->

When you run this com mand, `cat` prints the con tents of _`file1`_ , _`file2`_ , and any other files that you spec ify as ar gu ments (de noted by `...` in the pre ced ing ex am ple), and then ex its. The pro gram is called `cat` be cause it per forms con cate na tion when it prints the con tents of more than one file. There are many ways to run `cat` ; let's use it to ex plore Unix I/O.

---

<!-- Source: 01_normalize/output/x200_102/How_Linux_Works_clean.md -->

Unix pro cesses use I/O _streams_ to read and write data. Pro cesses read data from in put streams and write data to out ‐ put streams. Streams are very flex i ble. For ex am ple, the source of an in put stream can be a file, a de vice, a ter mi nal win dow, or even the out put stream from an other process.

---

<!-- Source: 01_normalize/output/x200_102/How_Linux_Works_clean.md -->

The rea son `cat` adopts an in ter ac tive be hav ior here has to do with streams. When you don't spec ify an in put file ‐ name, `cat` reads from the _stan dard in put_ stream pro vided by the Linux ker nel rather than a stream con nected to a file. In this case, the stan dard in put is con nected to the ter mi nal where you run `cat` .

---

<!-- Source: 01_normalize/output/x200_102/How_Linux_Works_clean.md -->

_Press ing CTRL-D on an empty line stops the cur rent stan dard in put en try from the ter mi nal with an EOF (end-offile) mes sage (and of ten ter mi nates a pro gram). Don't con fuse this with CTRL-C, which usu ally ter mi nates a pro ‐ gram re gard less of its in put or out put._

---

<!-- Source: 01_normalize/output/x200_102/How_Linux_Works_clean.md -->

_Stan dard out put_ is sim i lar. The ker nel gives each process a stan dard out put stream where it can write its out put. The `cat` com mand al ways writes its out put to the stan dard out put. When you ran `cat` in the ter mi nal, the stan dard out put was con nected to that ter mi nal, so that's where you saw the out put.

---

<!-- Source: 01_normalize/output/x200_102/How_Linux_Works_clean.md -->

Stan dard in put and out put are of ten ab bre vi ated as _stdin_ and _std out_ . Many com mands op er ate as `cat` does; if you don't spec ify an in put file, the com mand reads from stdin. Out put is a lit tle diff er ent. Some pro grams (like `cat` ) send out put only to std out, but oth ers have the op tion to send out put di rectly to files.

---

<!-- Source: 01_normalize/output/x200_102/How_Linux_Works_clean.md -->

There is a third stan dard I/O stream, called _stan dard er ror_ . You'll see it in Sec tion 2.14.1.

---

<!-- Source: 01_normalize/output/x200_102/How_Linux_Works_clean.md -->

One of the best fea tures of stan dard streams is that you can eas ily ma nip u late them to read and write to places other than the ter mi nal, as you'll learn in Sec tion 2.14. In par tic u lar, you'll learn how to con nect streams to files and other pro cesses.

---

<!-- Source: 01_normalize/output/x200_102/Learning_Modern_Linux_clean.md -->

Next up is the _shell_ , a pro gram that runs in side the ter mi nal and acts as a com mand in ter preter. The shell off ers in ‐ put and out put han dling via streams, sup ports vari ables, has some built-in com mands you can use, deals with com ‐ mand ex e cu tion and sta tus, and usu ally sup ports both in ter ac tive us age as well as scripted us age ("Script ing").

---

<!-- Source: 01_normalize/output/x200_102/Learning_Modern_Linux_clean.md -->

Let's start with the topic of in put (streams) and out put (streams), or I/O for short. How can you feed a pro gram some in put? How do you con trol where the out put of a pro gram lands, say, on the ter mi nal or in a file?

---

<!-- Source: 01_normalize/output/x200_102/Learning_Modern_Linux_clean.md -->

First off, the shell equips ev ery process with three de fault file de scrip tors (FDs) for in put and out put:

---

<!-- Source: 01_normalize/output/x200_102/Learning_Modern_Linux_clean.md -->

- stdin (FD 0)

---

<!-- Source: 01_normalize/output/x200_102/Learning_Modern_Linux_clean.md -->

- stdout (FD 1)

---

<!-- Source: 01_normalize/output/x200_102/Learning_Modern_Linux_clean.md -->

- stderr (FD 2)

---

<!-- Source: 01_normalize/output/x200_102/Learning_Modern_Linux_clean.md -->

These FDs are, as de picted in Fig ure 3-2, by de fault con nected to your screen and key board, re spec tively. In other words, un less you spec ify some thing else, a com mand you en ter in the shell will take its in put ( stdin ) from your key board, and it will de liver its out put ( stdout ) to your screen.

---

<!-- Source: 01_normalize/output/x200_102/Learning_Modern_Linux_clean.md -->

$ cat This is some input I type on the keyboard and read on the screen^C

---

<!-- Source: 01_normalize/output/x200_102/Learning_Modern_Linux_clean.md -->

If you don't want to use the de faults the shell gives you—for ex am ple, you don't want stderr to be out putted on the screen but want to save it in a file—you can re di rect the streams.

---

<!-- Source: 01_normalize/output/x200_102/Learning_Modern_Linux_clean.md -->

You re di rect the out put stream of a process us ing $FD> and <$FD , with $FD be ing the file de scrip tor—for ex am ple, 2> means re di rect the stderr stream. Note that 1> and > are the same since stdout is the de fault. If you want to re di ‐ rect both stdout and stderr , use &> , and when you want to get rid of a stream, you can use /dev/null .

---

<!-- Source: 01_normalize/output/x200_102/Learning_Modern_Linux_clean.md -->

$ curl https://example.com &> /dev/null

---

<!-- Source: 01_normalize/output/x200_102/Learning_Modern_Linux_clean.md -->

$ curl https://example.com > /tmp/content.txt 2> /tmp/curl-status $ head -3 /tmp/content.txt <!doctype html> <html> <head> $ cat /tmp/curl-status % Total % Received % Xferd Average Speed Time Time Time Current Dload Upload Total Spent Left Speed 100 1256 100 1256 0 0 3187 0 --:--:-- --:--:-- --:--:-3195 $ cat > /tmp/interactive-input.txt $ tr < /tmp/curl-status [A-Z] [a-z] % total % received % xferd average speed time time time current dload upload total spent left speed 100 1256 100 1256 0 0 3187 0 --:--:-- --:--:-- --:--:-3195

---

<!-- Source: 01_normalize/output/x200_102/Learning_Modern_Linux_clean.md -->

Dis card all out put by redi rect ing both stdout and stderr to _/dev/null_ . Re di rect the out put and sta tus to diff er ent files.

---

<!-- Source: 01_normalize/output/x200_102/Learning_Modern_Linux_clean.md -->

In ter ac tively en ter in put and save to file; use Ctrl+D to stop cap tur ing and store the con tent. Low er case all words, us ing the tr com mand that reads from stdin .

---

<!-- Source: 01_normalize/output/x200_102/Learning_Modern_Linux_clean.md -->

## _Pipe (_ | _)_

---

<!-- Source: 01_normalize/output/x200_102/Learning_Modern_Linux_clean.md -->

Con nects stdout of one process with the stdin of the next process, al low ing you to pass data with out hav ing to store it in files as a tem po rary place

---

<!-- Source: 01_normalize/output/x200_102/Learning_Modern_Linux_clean.md -->

## **PIPES AND THE UNIX PHI LOS O PHY**

---

<!-- Source: 01_normalize/output/x200_102/Learning_Modern_Linux_clean.md -->

Again, let's see some of the the o ret i cal con tent in ac tion. Let's try to fig ure out how many lines an HTML file con tains by down load ing it us ing curl and then pip ing the con tent to the wc tool:

---

<!-- Source: 01_normalize/output/x200_102/Learning_Modern_Linux_clean.md -->

$ curl https://example.com 2> /dev/null | \ wc -l 46

---

<!-- Source: 01_normalize/output/x200_102/Learning_Modern_Linux_clean.md -->

Use curl to down load the con tent from the URL, and dis card the sta tus that it out puts on stderr . (Note: in prac ‐ tice, you'd use the -s op tion of curl , but we want to learn how to ap ply our hard-gained knowl edge, right?) The stdout of curl is fed to stdin of wc , which counts the num ber of lines with the -l op tion.

---

<!-- Source: 01_normalize/output/x200_102/Learning_Modern_Linux_clean.md -->

$ set MY_VAR=42 $ set | grep MY_VAR _=MY_VAR=42 $ export MY_GLOBAL_VAR="fun with vars" $ set | grep 'MY_*' MY_GLOBAL_VAR='fun with vars' _=MY_VAR=42 $ env | grep 'MY_*' MY_GLOBAL_VAR=fun with vars $ bash $ echo $MY_GLOBAL_VAR fun with vars $ set | grep 'MY_*'

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

## **Pipes and Redirection**

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

In this chapter, you're going to learn how to harness one of the most powerful computing concepts in existence: pipes! Pipes can be used to connect commands, building up complex, customized flows that accomplish a specific task. By the end of the chapter, you'll be able to understand (or compose) something like this:

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

## `history | awk '{print $2}' | sort | uniq -c | sort -rn | head -n 10`

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

To really understand pipes, you need to first understand file descriptors and input/output redirection, so that's where we'll start. Some of the information in this chapter is quite dense; just take your time and try out all the examples to make sure you understand everything. The time you invest in learning these concepts now will save you many hours throughout your career.

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

- File descriptors

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

- Connecting commands together with pipes ( `|` )

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

- Practical pipe patterns Inspecting file descriptors

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

## **File descriptors**

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

You're probably familiar with file handles (also known as _file descriptors_ ) from your software engineering experience. If not, we

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

recommend you check out _Chapter 5, Introducing Files_ . In short, if your program needs to read or write a file on the operating system, opening that file gives you a "file handle" to it – a pointer, or reference, to that file object.

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

Because the operating system mediates all access to system resources like files, it tracks which file handles, or descriptors, your program is actively referencing.

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

But even if a process doesn't touch a single file on the operating system, it's got some file handles open. In Unix-like operating systems, every process has at least three file descriptors:

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

- `stdin` : standard input - or, `fd 0` ("file descriptor zero")

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

- `stdout` : standard output - or, `fd 1` ("file descriptor one")

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

- `stderr` : standard error - or, `fd 2` ("file descriptor two")

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

These first three file descriptors function as standard communication channels to (and from) a process. As a result, they exist in the same order for every process created on the system. The first always points to a file which will be used to read in input. The second points to a file that will be used for writing output. And the third references a file that will receive error output.

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

Optionally, after those first three standard file descriptors, there can be any number of other file descriptors/handles, based on what the program is doing. Your process could have:

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

## **What do these file descriptors reference?**

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

You now know, from the perspective of a process, what these file descriptors are used for:

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

- `0` ( `STDIN` ): get input from here

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

- `1` ( `STDOUT` ): put regular output here

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

- `2` ( `STDERR` ): put error output here

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

But if we zoom outside of a single process, which files are these file descriptors actually pointing to? Where does input come from, and where do output and errors get written to?

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

Let's use a Bash shell process as an example: by default, it takes input (STDIN) from your terminal (which is represented by a file on the filesystem). Bash prints output and errors to the same terminal. In essence, your entire shell session is happening via read and write operations to a single file. You'll learn much more about Bash in the next chapter, _Automating Tasks with Shell Scripts_ .

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

Let's look at this kind of input and output redirection in more detail.

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

## **Input and output redirection (or, playing with file descriptors for fun and profit)**

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

This knowledge comes in handy quite often during real-life development tasks: every time you want to avoid typing lots of input and take it from a file instead, or when you want to log the output of a program, and many more situations. When you create a process, you can control where its three standard file descriptors point, with powerful results.

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

## **Input redirection: <**

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

The `<` (less-than) symbol lets you control where a process gets its input from. For example, you're used to giving input to Bash with your keyboard, one command at a time. Let's try giving Bash input from a file, instead!

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

These are valid shell commands, as far as Bash is concerned, so I'm going to launch a new Bash process and use this file as standard input:

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

In this example, the program's standard output is still going back to our terminal, where we can read it. Let's change that now.

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

## **Output redirection: >**

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

We want to redirect `STDOUT` (file descriptor `1` ) to a file instead of a terminal, logging the output of each command instead of printing it out to the terminal in real time:

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

```
# bash < commands.txt > output.log
```

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

Notice that there is no visible output in the terminal now – because the `>` character has redirected output to `output.log` . Use `cat` to print out the log file and confirm that it contains the expected output:

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

Interestingly, you'll notice that because file descriptor `1` is standard output, writing `>` is the same as writing `1>` . You'll rarely see a `1` used, because it's assumed that standard output is being redirected. In other words:

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

```
date > mydate.log
is equivalent to writing
date 1> mydate.log
```

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

## **Use >> to append output without overwriting**

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

In the previous example, we created a log file by redirecting command output with `>` . If you run the example a few times, you'll notice that the log file doesn't grow at all. Each time you redirect output to a file with `> filename` , anything in that file will be overwritten.

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

To avoid that – as in the case of a long-lived log file that collects output from more than a single process or command – use `>>` (append). This will simply append to your output file, instead of overwriting its entire contents each time.

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

```
while true; do
    date >> /tmp/date.log
    sleep 1
done
```

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

In this example script, we create an infinite loop (while true; do [ ... ] done) which runs the date command. It redirects the output of this command to the `/tmp/date.log` file using `>>` , which appends the output to the file ( `>` would overwrite the file each time). Then, the script sleeps for one second, and starts again from the beginning.

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

```
→  ~ while true; do
    date >> /tmp/date.log
    sleep 1
done
^C%
→  ~ cat /tmp/date.log
Sat Jan  6 16:44:01 EST 2024
Sat Jan  6 16:44:02 EST 2024
Sat Jan  6 16:44:03 EST 2024
[ ... ]
Sat Jan  6 16:44:08 EST 2024
```

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

You'll use this kind of simple output redirection in all kinds of everyday situations, like creating an ad hoc log file for a quick debug script you throw together.

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

## **Error redirection with 2>**

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

Many command-line programs that have a lot of expected output will also output occasional errors – think of a `find` command that encounters occasional "permission denied" errors for directories you're not allowed to peek inside.

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

Although these kinds of errors are minor and expected, you don't want them mixed in with everything else, polluting your output. This becomes especially important when you're not using command-line tools interactively, but rather writing small scripts or larger programs that process the output of the commands you're running.

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

You've seen how to redirect Standard Input ( `fd 0` ) and Standard Output ( `fd 1` ). Let's look at how to redirect Standard Error ( `fd 2` ) using the `2>` (redirect file descriptor 2) syntax:

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

```
find /etc/ -name php.ini > /tmp/phpinis.log 2>/dev/null
```

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

This command searches for any files named `php.ini` inside the `/etc` directory tree. The files it finds ( `find` 's `STDOUT` ) are written to `/tmp/phpinis.log` , and any errors it encounters are ignored by sending them to a special file called `/dev/null` .

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

`/dev/null` is a special file-like object that returns zeros when you try to read from it and ignores anything written to it – it's used as a kind of garbage dump for output that engineers want to silence or ignore. You'll see it used quite often in scripts.

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

Now that you've seen input and output redirection, let's look at pipes, which put both of those concepts together: they redirect the output of one command to the input of another.

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

## **Connecting commands together with pipes (|)**

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

You've learned how to redirect each of the three standard file descriptors to various locations and seen why that's often useful. But what if, instead of just redirecting input and output to and from various files, you wanted to connect _multiple programs_ together?

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

On the command line, you can use the pipe character ( `|` ) to connect the output of one program to the input of another program. This is an extremely powerful paradigm that is heavily used in Unix and Linux to create custom sorting, filtering, and processing commands:

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

```
echo -e "some text \n treasure found \n some more text" | grep treasure
```

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

2. The pipe character streams that output (file descriptor 1) to the input of the next command (file descriptor 0), `grep` . `grep` 's input is now hooked up to the output of the previous command.

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

3. The `grep` command looks at each newline-delimited line in turn and finds a match for `treasure` on the second line. `grep` prints that second line to its standard output.

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

## **Multi-pipe commands**

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

```
history | awk '{print $2}' | sort | uniq -c | sort -rn | head -n 10 > /tmp/top10commands
```

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

Each pipe in this complex command simply takes the output of the previous command ( `STDOUT` ) and uses it as the input ( `STDIN` ) for the next command.

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

Piping the output of one command into the input of another is what enables these kinds of flows, filtering and sorting the data streaming between these commands without actually having to write any custom software. Just because there's no program called

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

## **Reading (and building) complex multi-pipe commands**

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

No matter how complex or magical some of the piped-together commands you encounter will seem, they were all built the same way: one command at a time. Whether you're trying to read a complex series of commands like this or creating one of your own, the process is the same:

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

3. Add the pipe and the command following it.

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

You'll see that even the scariest shell/pipe monstrosities become manageable when you apply this process. Always remember that you're just dealing with a data stream, which flows through the pipes from command to command, being shaped, modified, filtered, redirected, and transformed along the way.

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

Now that you've seen how the primitives of file descriptors are exposed as easy-to-use input and output redirection, let's look at some real-world examples of useful program combinations that rely on this composability that's built into Unix.

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

Before we jump into the kinds of wild combinations that you saw at the beginning of the chapter, let's look at some of the most common Unix helper tools that are used to filter, sort, and glue together these data streams you'll be creating on the command line.

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

```
echo "this is a space-delimited line" | cut -d " " -f4
space-delimited
```

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

```
→  ~ echo "this is a space-delimited line" | cut -d "-" -f1
this is a space
```

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

```
→  ~ echo "this is a space-delimited line" | cut -d "-" -f2
delimited line
```

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

```
# grep root /etc/passwd | cut -d ":" -f5
System Administrator
System Services
CVMS Root
```

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

```
# du -h | sort -rh
1.6M    .
1.3M    ./.git
1.2M    ./.git/objects
 60K    ./.git/hooks
 28K    ./.git/objects/d8
```

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

This is not what most users expect: there are 3 occurrences of `arch` in the file, but `uniq` shows two separate counts for the same word. To get the behavior you expect ( `uniq` should return output that doesn't contain any duplicate lines), your input must be sorted.

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

```
$ sort /tmp/sort1.txt | uniq -c
   1 alpine
   3 arch
```

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

```
$ sort /tmp/sortme.txt | uniq -c | sort -rn
```

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

```
# echo "foo bar baz" | wc -w
       3
```

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

```
# wc -l < /etc/passwd
     123
```

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

## **tee**

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

Sometimes, one copy of the data from standard input just isn't enough. `tee` copies standard input to standard output, while also making a copy in a file. As a software developer, I really like `tee` for two specific cases.

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

First, for debugging and logging: when I'm running scripts or programs that generate output, `tee` can be used to both display the output on the screen and log it to a file for later analysis. We're using the `echo` command here, but you'd likely be calling your own program before the first pipe here:

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

```
# echo "Hello" | tee /tmp/greetings.txt
Hello
# cat /tmp/greetings.txt
Hello
```

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

The second use case where `tee` comes in handy is for copying data from a pipeline like the ones we're learning to construct in this chapter. You can use `tee` to intercept this flow at any point in the pipe, and save/inspect the intermediate results without disrupting the pipeline.

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

Here's the "top 10 commands" example from earlier, but with `tee` inserted before limiting the results to just 10. This saves the full results in a temp file before we truncate them:

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

```
history | awk '{print $2}' | sort | uniq -c | sort -rn | tee /tmp/all_commands.txt | hea
```

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

```
# echo "two columns" | awk '{print $2}'
columns
```

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

## **Practical pipe patterns**

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

As mentioned before, longer multi-pipe commands are built iteratively – one command at a time. However, there are some useful patterns that you'll see re-used frequently.

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

Here's the pattern:

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

## `some_input | sort | uniq -c | sort -rn | head -n 3`

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

- The input is sorted alphabetically, and then run through `uniq -c` , which needs sorted input to work on.

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

## **curl | bash**

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

The `curl | bash` pattern is a common shortcut used in Linux to download and execute scripts directly from the internet. This method combines two powerful command-line tools: `curl` , which fetches the content from a URL, and `bash` , the shell interpreter, which executes the downloaded script. This pattern is a significant time-saver, allowing developers to quickly deploy applications or run scripts without manually downloading and then executing them.

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

Let's break this down, step by step:

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

2. `|` : The pipe symbol passes the output of the previous command ( `curl` ) as input to the next command ( `bash` ).

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

When you run commands that produce a lot of output, it's generally best practice to filter the output down to just what you need. The most common tool for this is called `grep` , and you can think of it as a highly configurable text search or string-matching function. Here's an example of what filtering might look like.

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

Here's a quick description of what's happening:

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

2. I'm then passing the results ( `|` ) to the `grep` utility and using that to search the results for the string `cwd` . There's only one line of results that contains the string `cwd` , so that's the only line that `grep` prints to the terminal.

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

- Occurrences of a username in a piped data stream

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

You've already seen `grep` used on files in this book (for example, `grep searchstring hello.txt` ), but it's also an invaluable filtering component in piped commands. Let's look at a practical example now.

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

## `tail -f /var/log/webapp/too_many_logs.log | grep "yourSearchRegex"`

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

`xargs` is a powerful utility that gives you the power of iteration (in other words, a "for" loop) inside of a single command. By default, `xargs` takes each (space, tab, newline, and end-of-file delimited) chunk of input it receives and executes the specified program using that chunk as input. For example, if you need to search for specific file content across `ONLY` the files returned by a certain `find` query, you can run this command:

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

## `find . -type f -name "*\.txt" | xargs grep "search_term"`

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

This command finds all files whose names end with `.txt` and then uses `xargs` to apply the `grep` command to each file individually. This pattern is handy for searching or modifying multiple files at once. Please be forewarned that `xargs` is a powerful – and _large_ – program, capable of doing many things (including string interpolation into the command it executes). We can't cover it all here, so please read the manpage and scour the internet for examples if you're in a situation where this kind of functionality would save the day.

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

This is a useful pattern that you saw applied at the beginning of the chapter, where I used it to filter a large command history to get a list of the "top X most popular commands run on this system." The core pattern is this:

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

```
(input stream) | sort | uniq –c | sort -rn
```

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

Useful for analyzing data, this pattern sorts the data from the input stream, deduplicates it while counting unique occurrences, and then performs a reverse numerical sort to give you the deduplicated data, with the most common lines first.

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

This is commonly truncated with `| head -n $NUMBER` to get only the top `$NUMBER` of results:

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

Then we sort so that duplicates of the same command occur next to each other in the stream. Then we remove those duplicates with `uniq` , adding a count of occurrences to each remaining one. Now we sort again – this time using `-rn` for a reverse numerical sort, which gives us the "top X" effect. Finally, we take the first 10 lines with head.

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

## `cat file.txt | awk '{print $2, $1}'`

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

## `sed 's/old/new/g' file.txt | tee file.txt.changed`

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

Although editing file content is an easy demonstration of this concept, `sed` is tremendously useful for transforming stream data as it zips from the output of one command to the input of the next:

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

```
(input stream) | sed 's/old/new/g' | (next command)
```

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

Although `pgrep` is a good utility for sending signals to all processes whose name matches a pattern, sometimes it's just not available on your system. You can cobble together similar functionality (and get much more specific with what you want to target, not just the name) by using this set of piped-together commands:

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

## `ps aux | grep "process_name" | awk '{print $2}' | xargs kill`

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

`ps` starts you off with a list of running processes, which `grep` filters to just those containing the pattern you're searching for. `awk` gets the second column (the process ID) for each matching line, and then feeds all matched lines to `xargs` (our quasi for loop), which executes `kill` on each PID. This sends a `SIGTERM` to each matching process and (hopefully) halts it.

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

Although many utilities have flags that let you do both, chaining together archiving and compression is another use case that makes sense. This gives you the added flexibility of adding additional chained commands. For example, if you want to add encryption, that's just a single additional piped command away:

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

```
tar cvf - /path/to/directory | gzip > backup.tar.gz
```

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

```
ssh user@mysql-server "mysqldump --add-drop-table database_name | gzip -9c" | gzip –d |
```

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

This is an especially fun example that logs into a database server using SSH, dumps out a database, compresses that data stream, shuttles it back to the local machine over SSH, decompresses it again, and finally dumps it into the local MySQL server.

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

## **Advanced: inspecting file descriptors**

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

In a process's `/proc` directory, that process's file descriptors are represented as symbolic links in a directory called `fd` . When you do a long listing on this `/proc/$PID/fd` directory, you'll see that `l` is the first character in the long listing, which denotes a special `link` file, as you'll recall from _Chapter 5_ , _Introducing Files_ .

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

Let's look at the file descriptors for an interactive Bash shell process running on my machine, which `ps aux | grep bash` tells me is PID 9:

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

```
root@server:/# ls -alh /proc/9/fd
total 0
dr-x------ 2 root root  0 Sep  1 19:16 .
dr-xr-xr-x 9 root root  0 Sep  1 19:16 ..
lrwx------ 1 root root 64 Sep  1 19:16 0 -> /dev/pts/1
lrwx------ 1 root root 64 Sep  1 19:16 1 -> /dev/pts/1
lrwx------ 1 root root 64 Sep  1 19:16 2 -> /dev/pts/1
lrwx------ 1 root root 64 Sep  5 00:46 255 -> /dev/pts/1
```

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

You'll notice that it's an interactive shell session: its standard input is coming from a virtual terminal ( `/dev/pts/1` ), and its standard error and output are going back to that same terminal. That checks out.

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

```
root@server:/# ps aux | grep vim
root       453  0.0  0.1  17232  9216 pts/1    S+   15:57   0:00 vim /tmp/hello.txt
root       458  0.0  0.0   2884  1536 pts/0    S+   15:58   0:00 grep --color=auto vim
```

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

```
lrwx------ 1 root root 64 Jan  7 15:58 0 -> /dev/pts/1
lrwx------ 1 root root 64 Jan  7 15:58 1 -> /dev/pts/1
lrwx------ 1 root root 64 Jan  7 15:58 2 -> /dev/pts/1
lrwx------ 1 root root 64 Jan  7 15:58 3 -> /tmp/.hello.txt.swp
```

---

<!-- Source: 01_normalize/output/x200_102/Software_Developer_clean.md -->

We can see that stdin ( `0` ), stdout ( `1` ), and stderr ( `2` ) are all pointing to a terminal device, just like a shell. And we also see that the editor has a file open, with file descriptor `3` linked to the file that vim is editing. When a process opens additional files, new file descriptors are created, and you can view them here.

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

## Chapter 3: Standard Input and Output - The Unix Convention

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

Here's where we get into one of the most fundamental conventions in Unix - one that affects literally every program you'll ever run on a Unix system. In Unix, we have this convention whereby processes, when they are started, expect to inherit from their parent two open file descriptors: file descriptor 0 and file descriptor 1.

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

Let's break down what these are: File descriptor 0 we call standard in, abbreviated as stdin. File descriptor 1 we call standard out, abbreviated as stdout. Now you might be wondering what a file descriptor actually is - think of it like a handle or reference number that a process uses to read from or write to an open file. When you open a file in Unix, you get back a small integer - that's your file descriptor - and you use that number in subsequent read and write operations.

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

In the usual case, processes expect stdin to be a file descriptor open for reading a terminal character device file, and stdout is expected to be open for writing that same terminal character device file. Let me put that in plain English: when a program starts up, it expects that file descriptor 0 is already set up so it can read keyboard input from a terminal, and file descriptor 1 is already set up so it can write text output to that same terminal.

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

So in practice, what does this mean for you as a programmer or system administrator? When a program wishes to read input from a terminal, it simply reads from stdin - its file descriptor 0. And when a program wishes to display text on that same terminal, it writes data to stdout. The program doesn't need to know which specific terminal device file it's connected to or even locate an appropriate terminal itself. It just uses these pre-opened file descriptors that it inherits.

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

### The Parent-Child File Descriptor Inheritance Model

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

Recall that when a process forks in Unix - that is, when it creates a child process - the file descriptors from the parent get copied to the child. So the child process has all the same open file descriptors as the parent, pointing to the same files. This is automatic; it happens as part of the fork operation.

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

So the convention in Unix is that when programs wish to interact with a terminal, they usually don't locate an appropriate terminal themselves. They don't go searching through the file system looking for terminal device files. Instead, they just expect to inherit these file descriptors already open to an appropriate terminal from their parent process. Think of it like this: somewhere up the chain of parent processes, usually at system boot or when you log in, a terminal gets opened, and then every subsequent process you launch inherits access to that terminal through these standard file descriptors.

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

### Why Two Separate File Descriptors?

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

Still, that doesn't fully explain why we have two separate file descriptors when we could theoretically just get away with one file descriptor opened for both reading and writing. Here's the thing - this design choice is something that will become clear a bit later when we talk about what's called redirection. For now, just know that having separate file descriptors for input and output gives Unix tremendous flexibility in how it connects processes together and redirects their input and output streams. This separation is actually one of the key design decisions that makes Unix pipelines and I/O redirection so powerful and elegant.

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

## Chapter 15: I/O Redirection - Controlling Input and Output Streams

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

Before we understood I/O redirection from the terminal perspective - how those file descriptors 0, 1, and 2 represent stdin, stdout, and stderr. Now let's explore how to actually manipulate these streams when executing commands. Redirection is how you change where a command reads its input from and where it sends its output to.

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

Think of it like this: by default, commands read from your keyboard (stdin) and write to your screen (stdout for normal output, stderr for errors). Redirection lets you say "actually, read from this file instead" or "send the output to that file" or even "connect this command's output to that command's input." It's plumbing for data streams.

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

Here's something important to understand: redirection happens before the command executes. The shell sets up all the redirections first, then launches the command. This means redirections are processed left to right in the order they appear, and by the time your command runs, its file descriptors are already configured.

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

This ordering matters because you can do things like duplicate file descriptors, and the order determines what each descriptor points to at any given moment.

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

### Basic Input Redirection

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

The `<` operator redirects input. It opens a file for reading and connects it to the command's standard input (file descriptor 0).

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

If you don't specify `n`, it defaults to 0 (stdin). The `word` undergoes all the normal shell expansions (brace, tilde, parameter, command substitution, arithmetic expansion, quote removal, and filename expansion), and the result must be a single filename.

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

```bash
# Read input from file instead of keyboard
sort < unsorted.txt

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

# Explicit file descriptor (same as above since 0 is default)
sort 0< unsorted.txt

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

# Use with other commands
wc -l < /etc/passwd  # Count lines in passwd file
```

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

### Basic Output Redirection

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

The `>` operator redirects output. It opens a file for writing and connects it to the command's standard output (file descriptor 1). If the file doesn't exist, it's created. If it exists, it's truncated to zero size (overwritten).

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

**Format:** `[n]>[|]word`

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

Again, if you don't specify `n`, it defaults to 1 (stdout).

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

```bash
# Write output to file
ls > directory_list.txt

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

# Explicit file descriptor
ls 1> directory_list.txt

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

# Overwrite protection with noclobber
set -o noclobber       # Enable overwrite protection
ls > existing.txt      # This will FAIL if existing.txt exists
ls >| existing.txt     # This FORCES overwrite even with noclobber set
set +o noclobber       # Disable overwrite protection
```

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

The `noclobber` option is a safety feature - when enabled, `>` won't overwrite existing files. Use `>|` to override this protection when you really want to clobber a file.

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

### Appending Output

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

The `>>` operator appends output to a file instead of overwriting it. If the file doesn't exist, it's created.

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

**Format:** `[n]>>word`

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

```bash
# Append to log file
echo "Process started" >> application.log
echo "Step 1 complete" >> application.log
echo "Step 2 complete" >> application.log

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

# All three lines are now in application.log, in order
```

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

This is essential for logging - you almost never want to overwrite your log file, you want to add new entries to it.

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

### Redirecting Both stdout and stderr

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

Often you want to redirect both standard output and standard error to the same place. Bash provides convenient syntax for this:

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

**Format 1 (preferred):** `&>word`
**Format 2:** `>&word`

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

Both forms redirect both stdout (fd 1) and stderr (fd 2) to the same file.

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

```bash
# Capture both output and errors
command &> all_output.txt

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

# This is equivalent to:
command > all_output.txt 2>&1

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

# Appending both stdout and stderr
command &>> all_output.log
```

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

The `&>` syntax is cleaner and more intuitive than `> file 2>&1`, though the latter works and you'll see it in older scripts.

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

### Duplicating File Descriptors

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

Sometimes you need to make one file descriptor a copy of another. This is how you redirect stderr to wherever stdout is going, or vice versa.

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

**Input duplication:** `[n]<&word`
**Output duplication:** `[n]>&word`

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

If `word` expands to one or more digits, file descriptor `n` becomes a copy of that descriptor. If `word` is `-`, descriptor `n` is closed.

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

```bash
# Redirect stderr to wherever stdout is going
command 2>&1

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

# Redirect stderr to wherever stdout is going, then redirect stdout to file
command > output.txt 2>&1
# Now both stdout and stderr go to output.txt

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

# WRONG order - doesn't work as intended:
command 2>&1 > output.txt  
# This redirects stderr to the CURRENT stdout (the terminal),
# THEN redirects stdout to the file
# So stderr still goes to terminal, only stdout goes to file

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

# Close a file descriptor
exec 3>&-  # Close file descriptor 3
```

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

The order matters! `> output.txt 2>&1` is NOT the same as `2>&1 > output.txt`. Redirections are processed left to right, so:
- `> output.txt 2>&1`: stdout to file first, then stderr to wherever stdout goes (the file)
- `2>&1 > output.txt`: stderr to wherever stdout currently goes (terminal), then stdout to file

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

### Moving File Descriptors

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

**Input:** `[n]<&digit-`
**Output:** `[n]>&digit-`

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

Note the hyphen after the digit. This moves the descriptor instead of just copying it.

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

```bash
# Move file descriptor 3 to descriptor 4, close 3
exec 4<&3-

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

This is useful in advanced fd manipulation, particularly when you're managing multiple file descriptors in complex scripts.

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

You can open a file for both reading and writing on a single file descriptor:

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

```bash
# Open file for read/write on fd 3
exec 3<> datafile.txt

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

# Now you can both read from and write to fd 3
echo "New data" >&3  # Write to the file
read -u 3 line       # Read from the file
```

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

```bash
# Basic here document
cat <<EOF
This is line 1
This is line 2
This is line 3

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

**`/dev/fd/N`** - Duplicate file descriptor N  
```bash
# Same as >&3
command >/dev/fd/3
```

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

**`/dev/stdin`** - Duplicate file descriptor 0 (standard input)
**`/dev/stdout`** - Duplicate file descriptor 1 (standard output)
**`/dev/stderr`** - Duplicate file descriptor 2 (standard error)

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

```bash
# Explicitly write to stderr
echo "Error message" >/dev/stderr
```

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

```bash
# Simple HTTP request using /dev/tcp
exec 3<>/dev/tcp/www.example.com/80
echo -e "GET / HTTP/1.1\r\nHost: www.example.com\r\n\r\n" >&3
cat <&3

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

### Advanced File Descriptor Management

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

```bash
# Allocate a file descriptor >= 10 automatically
exec {myfd}>output.txt

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

# Now $myfd contains the file descriptor number
echo "Log entry" >&$myfd

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

# Close it using the variable
exec {myfd}>&-
```

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

This is safer than using hard-coded numbers because you avoid conflicts with descriptors the shell might be using internally. The `varredir_close` shell option controls whether these file descriptors persist beyond the command scope.

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

### Redirections in Practice

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

**Discarding output:**
```bash
# Discard all output
command >/dev/null 2>&1

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

# Discard only errors
command 2>/dev/null

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

# Discard only standard output
command >/dev/null
```

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

**Separating output and errors:**
```bash
# Send output to one file, errors to another
command >output.txt 2>errors.txt

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

# Different fds for output and error processing
some_command > >(process_output) 2> >(process_errors)
```

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

**Swapping stdout and stderr:**
```bash
# This is tricky - requires a temporary descriptor
command 3>&1 1>&2 2>&3 3>&-
# 3>&1: save stdout to fd 3
# 1>&2: redirect stdout to stderr
# 2>&3: redirect stderr to saved stdout (fd 3)
# 3>&-: close fd 3
```

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

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

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

**Keeping errors on screen while logging output:**
```bash
command 2>&1 | tee output.log
# Both stdout and stderr go through tee,
# appearing on screen AND in output.log
```

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

### Redirection Order and Semantics

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

The order of redirections is significant because they're processed left to right:

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

```bash
# Example 1: Both to file
ls >output.txt 2>&1
# Process: stdout to output.txt, then stderr to wherever stdout goes (output.txt)
# Result: Both in output.txt

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

# Example 2: Only stdout to file
ls 2>&1 >output.txt
# Process: stderr to wherever stdout currently goes (terminal),
#          then stdout to output.txt
# Result: stdout in output.txt, stderr to terminal

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

# Example 3: Redirection with command execution
cat < input.txt > output.txt
# Both redirections are set up BEFORE cat runs
# cat sees input.txt as stdin and output.txt as stdout
```

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

### Redirections and Shell Execution Environment

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

When you use redirections with the `exec` builtin, they affect the current shell's file descriptors, not just a command:

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

```bash
# Redirect all subsequent output to file
exec >output.txt

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

# Now everything prints to output.txt instead of terminal
echo "This goes to the file"
ls
# Even ls output goes to the file

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

# Restore stdout to terminal (assuming fd 6 was saved earlier)
exec 1>&6 6>&-
```

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

This is powerful for logging entire sections of a script or redirecting all output at once.

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

### Common Redirection Patterns

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

**Pattern 1: Silent execution (hide all output)**
```bash
command >/dev/null 2>&1
# Or using &>
command &>/dev/null
```

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

**Pattern 2: Append to log with both stdout and stderr**
```bash
command >> logfile.txt 2>&1
# Or using &>>
command &>> logfile.txt
```

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

**Pattern 3: Capture output in variable while showing errors**
```bash
output=$(command 2>&1)  # Captures both, errors mixed in
# OR
output=$(command 2>/dev/tty)  # Errors to terminal, only stdout captured
```

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

**Pattern 4: Process output and errors separately**
```bash
{ command 2>&1 1>&3 | error_processor; } 3>&1 | output_processor
# This is complex but powerful - errors go to error_processor,
# output goes to output_processor
```

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

**Pattern 5: Tee to both file and screen**
```bash
command 2>&1 | tee output.log
# Output appears on screen AND in file
```

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

So hopefully that makes sense - I/O redirection gives you complete control over where data flows. You can redirect input from files instead of keyboard, send output to files instead of screen, connect commands together with pipes, embed multi-line input with here documents, and manipulate file descriptors in sophisticated ways. Master these redirection techniques and you'll be able to build complex data processing pipelines and robust scripts that handle input and output exactly the way you need.

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

## Chapter 16: Pipelines - Composing Commands Together

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

Redirection in Unix makes possible another incredibly powerful trick called pipelining. This is one of those features that really demonstrates the elegance of Unix's design philosophy - the idea that you can compose small, focused programs together to accomplish complex tasks.

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

When in the shell we separate two commands with the pipe character (which is usually found on the same key as your backslash key - it's easy to mistake for a lowercase L, but it's not; it's a separate character, just a vertical bar: `|`), the shell will run these two commands in parallel. It will run them at the same time, and it will redirect the stdout of the first command such that it becomes the stdin of the second command.

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

Think of it like this: effectively, whatever the first command writes to stdout gets read as stdin by the second command. The data flows from one program to the next, like water flowing through a pipe. That's why we call it pipelining.

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

Now you might wonder, why do we need this special pipe mechanism? The reason we have to involve a pipe is because processes can't read and write from each other like files. Processes simply can't do that directly - they're isolated from each other for security and stability. So we have to put a pipe in the middle to facilitate the communication.

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

### The Mechanics of Pipeline Execution

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

Looking at exactly what happens when you use a pipe, the sequence is quite elegant:

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

**Step 1: Create the Pipe** - First, the shell creates a pipe to connect the two processes. This is a special kernel object that acts as a buffer between the two programs.

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

**Step 4: Redirect First Command** - In one of the child processes, it redirects its stdout to the pipe (the newly created pipe), before it then executes the first command.

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

**Step 5: Redirect Second Command** - Meanwhile, the other child process redirects its stdin to the pipe before it executes the second command.

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

So again, these two commands execute in parallel. They're separate processes running concurrently, and the original shell process waits for both of them to terminate before it continues on its business. This parallel execution is important because it means data can flow through the pipe as it's being produced - the second command doesn't have to wait for the first to completely finish before it starts processing data.

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

### Multi-Stage Pipelines

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

When we pipe commands, we're not limited to piping just two commands together. We can pipe three or more, creating sophisticated data processing chains.

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

```bash
command1 | command2 | command3
```

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

Here, the first command writes its stdout to a pipe, and then that pipe is read as stdin by the second command, which in turn writes its stdout to a second pipe, which is read as stdin by the third command.

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

So when we have three commands connected by two pipe characters, that actually represents two pipe files - two separate kernel pipe objects. Again, be clear that all of these commands connected by pipes are run in tandem, they're run in parallel, and the shell waits for all three to finish before it continues.

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

This composability is one of Unix's greatest strengths. You can take simple, single-purpose utilities and chain them together to solve complex problems without writing any custom code. Need to find all the unique IP addresses in a log file and count them? Pipe together `cat`, `grep`, `sort`, and `uniq`. It's like building with LEGO blocks - each piece does one thing well, and you combine them to build whatever you need.

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

### Pipelines Defined

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

What in the shell we call a pipeline refers to either:
1. Just a single process executed on its own, or
2. Multiple commands separated by the pipe character (`|`), and therefore executed in tandem, connected by pipes

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

So even a single command like `ls` is technically a pipeline - it's just a pipeline with one stage. When you add pipe characters, you create a multi-stage pipeline.

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

The background process still has its stdout and stdin connected to the terminal by default, which can sometimes cause confusing behavior where background process output appears in your terminal while you're typing other commands. In practice, you often want to redirect the output of background processes to files to keep your terminal clean.

---

<!-- Source: 01_normalize/output/x200_102/Understanding_Unix_Terminals_clean.md -->

This simply puts out to stdout the text "foo" and then space "2348". Now, of course, this may not seem useful at the command prompt, because why would you want the shell to just spit back at you exactly what you just typed?

---

<!-- Source: 01_normalize/output/x200_102/bash-redirection_clean.md -->

A shell allows execution of gnu commands, both synchronously and asynchronously. The shell waits for synchronous commands to complete before accepting more input; asynchronous commands continue to execute in parallel with the shell while it reads and executes additional commands. The _redirection_ constructs permit fine-grained control of the input and output of those commands. Moreover, the shell allows control over the contents of commands' environments.

---

<!-- Source: 01_normalize/output/x200_102/bash-redirection_clean.md -->

A `token` that performs a control function. It is a `newline` or one of the following: ' `||` ', ' `&&` ', ' `&` ', ' `;` ', ' `;;` ', ' `;&` ', ' `;;&` ', ' `|` ', ' `|&` ', ' `(` ', or ' `)` '.

---

<!-- Source: 01_normalize/output/x200_102/bash-redirection_clean.md -->

A character that, when unquoted, separates words. A metacharacter is a `space` , `tab` , `newline` , or one of the following characters: ' `|` ', ' `&` ', ' `;` ', ' `(` ', ' `)` ', ' `<` ', or ' `>` '.

---

<!-- Source: 01_normalize/output/x200_102/bash-redirection_clean.md -->

- `operator` A `control operator` or a `redirection operator` . See Section 3.6 [Redirections], page 38, for a list of redirection operators. Operators contain at least one unquoted `metacharacter` .

---

<!-- Source: 01_normalize/output/x200_102/bash-redirection_clean.md -->

## **3.6 Redirections**

---

<!-- Source: 01_normalize/output/x200_102/bash-redirection_clean.md -->

Before a command is executed, its input and output may be _redirected_ using a special notation interpreted by the shell. _Redirection_ allows commands' file handles to be duplicated, opened, closed, made to refer to different files, and can change the files the command reads from and writes to. Redirection may also be used to modify file handles in the current shell execution environment. The following redirection operators may precede or appear anywhere within a simple command or may follow a command. Redirections are processed in the order they appear, from left to right.

---

<!-- Source: 01_normalize/output/x200_102/bash-redirection_clean.md -->

Each redirection that may be preceded by a file descriptor number may instead be preceded by a word of the form { _varname_ }. In this case, for each redirection operator except `>` &- and `<` &-, the shell will allocate a file descriptor greater than 10 and assign it to { _varname_ }. If `>` &- or `<` &- is preceded by { _varname_ }, the value of _varname_ defines the file descriptor to close. If { _varname_ } is supplied, the redirection persists beyond the scope of the command, allowing the shell programmer to manage the file descriptor's lifetime manually. The `varredir_close` shell option manages this behavior (see Section 4.3.2 [The Shopt Builtin], page 71).

---

<!-- Source: 01_normalize/output/x200_102/bash-redirection_clean.md -->

In the following descriptions, if the file descriptor number is omitted, and the first character of the redirection operator is ' `<` ', the redirection refers to the standard input (file descriptor 0). If the first character of the redirection operator is ' `>` ', the redirection refers to the standard output (file descriptor 1).

---

<!-- Source: 01_normalize/output/x200_102/bash-redirection_clean.md -->

The word following the redirection operator in the following descriptions, unless otherwise noted, is subjected to brace expansion, tilde expansion, parameter expansion, command substitution, arithmetic expansion, quote removal, filename expansion, and word splitting. If it expands to more than one word, Bash reports an error.

---

<!-- Source: 01_normalize/output/x200_102/bash-redirection_clean.md -->

Note that the order of redirections is significant. For example, the command

---

<!-- Source: 01_normalize/output/x200_102/bash-redirection_clean.md -->

```
ls>dirlist2>&1
```

---

<!-- Source: 01_normalize/output/x200_102/bash-redirection_clean.md -->

directs both standard output (file descriptor 1) and standard error (file descriptor 2) to the file _dirlist_ , while the command

---

<!-- Source: 01_normalize/output/x200_102/bash-redirection_clean.md -->

```
ls2>&1>dirlist
```

---

<!-- Source: 01_normalize/output/x200_102/bash-redirection_clean.md -->

directs only the standard output to file _dirlist_ , because the standard error was made a copy of the standard output before the standard output was redirected to _dirlist_ .

---

<!-- Source: 01_normalize/output/x200_102/bash-redirection_clean.md -->

If _fd_ is a valid integer, file descriptor _fd_ is duplicated.

---

<!-- Source: 01_normalize/output/x200_102/bash-redirection_clean.md -->

## `/dev/stdout`

---

<!-- Source: 01_normalize/output/x200_102/bash-redirection_clean.md -->

File descriptor 1 is duplicated.

---

<!-- Source: 01_normalize/output/x200_102/bash-redirection_clean.md -->

## `/dev/stderr`

---

<!-- Source: 01_normalize/output/x200_102/bash-redirection_clean.md -->

A failure to open or create a file causes the redirection to fail.

---

<!-- Source: 01_normalize/output/x200_102/bash-redirection_clean.md -->

Redirections using file descriptors greater than 9 should be used with care, as they may conflict with file descriptors the shell uses internally.

---

<!-- Source: 01_normalize/output/x200_102/bash-redirection_clean.md -->

## **3.6.1 Redirecting Input**

---

<!-- Source: 01_normalize/output/x200_102/bash-redirection_clean.md -->

Redirection of input causes the file whose name results from the expansion of _word_ to be opened for reading on file descriptor `n` , or the standard input (file descriptor 0) if `n` is not specified.

---

<!-- Source: 01_normalize/output/x200_102/bash-redirection_clean.md -->

The general format for redirecting input is:

---

<!-- Source: 01_normalize/output/x200_102/bash-redirection_clean.md -->

## **3.6.2 Redirecting Output**

---

<!-- Source: 01_normalize/output/x200_102/bash-redirection_clean.md -->

Redirection of output causes the file whose name results from the expansion of _word_ to be opened for writing on file descriptor _n_ , or the standard output (file descriptor 1) if _n_ is not specified. If the file does not exist it is created; if it does exist it is truncated to zero size.

---

<!-- Source: 01_normalize/output/x200_102/bash-redirection_clean.md -->

The general format for redirecting output is:

---

<!-- Source: 01_normalize/output/x200_102/bash-redirection_clean.md -->

## `[` _`n`_ `]>[|]` _`word`_

---

<!-- Source: 01_normalize/output/x200_102/bash-redirection_clean.md -->

If the redirection operator is ' `>` ', and the `noclobber` option to the `set` builtin has been enabled, the redirection will fail if the file whose name results from the expansion of _word_ exists and is a regular file. If the redirection operator is ' `>|` ', or the redirection operator is ' `>` ' and the `noclobber` option is not enabled, the redirection is attempted even if the file named by _word_ exists.

---

<!-- Source: 01_normalize/output/x200_102/bash-redirection_clean.md -->

## **3.6.3 Appending Redirected Output**

---

<!-- Source: 01_normalize/output/x200_102/bash-redirection_clean.md -->

Redirection of output in this fashion causes the file whose name results from the expansion of _word_ to be opened for appending on file descriptor _n_ , or the standard output (file descriptor 1) if _n_ is not specified. If the file does not exist it is created.

---

<!-- Source: 01_normalize/output/x200_102/bash-redirection_clean.md -->

The general format for appending output is:

---

<!-- Source: 01_normalize/output/x200_102/bash-redirection_clean.md -->

## `[` _`n`_ `]>>` _`word`_

---

<!-- Source: 01_normalize/output/x200_102/bash-redirection_clean.md -->

## **3.6.4 Redirecting Standard Output and Standard Error**

---

<!-- Source: 01_normalize/output/x200_102/bash-redirection_clean.md -->

This construct allows both the standard output (file descriptor 1) and the standard error output (file descriptor 2) to be redirected to the file whose name is the expansion of _word_ .

---

<!-- Source: 01_normalize/output/x200_102/bash-redirection_clean.md -->

There are two formats for redirecting standard output and standard error:

---

<!-- Source: 01_normalize/output/x200_102/bash-redirection_clean.md -->

```
&>word
```

---

<!-- Source: 01_normalize/output/x200_102/bash-redirection_clean.md -->

```
>&word
```

---

<!-- Source: 01_normalize/output/x200_102/bash-redirection_clean.md -->

```
>word2>&1
```

---

<!-- Source: 01_normalize/output/x200_102/bash-redirection_clean.md -->

When using the second form, _word_ may not expand to a number or ' `-` '. If it does, other redirection operators apply (see Duplicating File Descriptors below) for compatibility reasons.

---

<!-- Source: 01_normalize/output/x200_102/bash-redirection_clean.md -->

This construct allows both the standard output (file descriptor 1) and the standard error output (file descriptor 2) to be appended to the file whose name is the expansion of _word_ .

---

<!-- Source: 01_normalize/output/x200_102/bash-redirection_clean.md -->

The format for appending standard output and standard error is:

---

<!-- Source: 01_normalize/output/x200_102/bash-redirection_clean.md -->

```
&>>word
```

---

<!-- Source: 01_normalize/output/x200_102/bash-redirection_clean.md -->

This is semantically equivalent to

---

<!-- Source: 01_normalize/output/x200_102/bash-redirection_clean.md -->

```
>>word2>&1
```

---

<!-- Source: 01_normalize/output/x200_102/bash-redirection_clean.md -->

If the redirection operator is ' `<<-` ', then all leading tab characters are stripped from input lines and the line containing _delimiter_ . This allows here-documents within shell scripts to be indented in a natural fashion.

---

<!-- Source: 01_normalize/output/x200_102/bash-redirection_clean.md -->

The _word_ undergoes tilde expansion, parameter and variable expansion, command substitution, arithmetic expansion, and quote removal. Filename expansion and word splitting are not performed. The result is supplied as a single string, with a newline appended, to the command on its standard input (or file descriptor _n_ if _n_ is specified).

---

<!-- Source: 01_normalize/output/x200_102/bash-redirection_clean.md -->

The redirection operator

---

<!-- Source: 01_normalize/output/x200_102/bash-redirection_clean.md -->

is used to duplicate input file descriptors. If _word_ expands to one or more digits, the file descriptor denoted by _n_ is made to be a copy of that file descriptor. If the digits in _word_ do not specify a file descriptor open for input, a redirection error occurs. If _word_ evaluates to ' `-` ', file descriptor _n_ is closed. If _n_ is not specified, the standard input (file descriptor 0) is used.

---

<!-- Source: 01_normalize/output/x200_102/bash-redirection_clean.md -->

## `[` _`n`_ `]>&` _`word`_

---

<!-- Source: 01_normalize/output/x200_102/bash-redirection_clean.md -->

is used similarly to duplicate output file descriptors. If _n_ is not specified, the standard output (file descriptor 1) is used. If the digits in _word_ do not specify a file descriptor open for output, a redirection error occurs. If _word_ evaluates to ' `-` ', file descriptor _n_ is closed. As a special case, if _n_ is omitted, and _word_ does not expand to one or more digits or ' `-` ', the standard output and standard error are redirected as described previously.

---

<!-- Source: 01_normalize/output/x200_102/bash-redirection_clean.md -->

## `[` _`n`_ `]<&` _`digit`_ `-`

---

<!-- Source: 01_normalize/output/x200_102/bash-redirection_clean.md -->

moves the file descriptor _digit_ to file descriptor _n_ , or the standard input (file descriptor 0) if _n_ is not specified. _digit_ is closed after being duplicated to _n_ .

---

<!-- Source: 01_normalize/output/x200_102/bash-redirection_clean.md -->

Similarly, the redirection operator

---

<!-- Source: 01_normalize/output/x200_102/bash-redirection_clean.md -->

## `[` _`n`_ `]>&` _`digit`_ `-`

---

<!-- Source: 01_normalize/output/x200_102/bash-redirection_clean.md -->

moves the file descriptor _digit_ to file descriptor _n_ , or the standard output (file descriptor 1) if _n_ is not specified.

---

<!-- Source: 01_normalize/output/x200_102/bash-redirection_clean.md -->

causes the file whose name is the expansion of _word_ to be opened for both reading and writing on file descriptor _n_ , or on file descriptor 0 if _n_ is not specified. If the file does not exist, it is created.

---

<!-- Source: 01_normalize/output/x200_102/bash_c03_clean.md -->

## **3.2.3 Pipelines**

---

<!-- Source: 01_normalize/output/x200_102/bash_c03_clean.md -->

A `pipeline` is a sequence of one or more commands separated by one of the control operators ' `|` ' or ' `|&` '.

---

<!-- Source: 01_normalize/output/x200_102/bash_c03_clean.md -->

The format for a pipeline is

---

<!-- Source: 01_normalize/output/x200_102/bash_c03_clean.md -->

## `[time [-p]] [!]` _`command1`_ `[ | or |&` _`command2`_ `] ...`

---

<!-- Source: 01_normalize/output/x200_102/bash_c03_clean.md -->

The output of each command in the pipeline is connected via a pipe to the input of the next command. That is, each command reads the previous command's output. This connection is performed before any redirections specified by _command1_ .

---

<!-- Source: 01_normalize/output/x200_102/bash_c03_clean.md -->

If ' `|&` ' is the pipeline operator, _command1_ 's standard error, in addition to its standard output, is connected to _command2_ 's standard input through the pipe; it is shorthand for `2>&1 |` . This implicit redirection of the standard error to the standard output is performed after any redirections specified by _command1_ , consistent with that shorthand.

---

<!-- Source: 01_normalize/output/x200_102/bash_c03_clean.md -->

If a pipeline is not executed asynchronously (see Section 3.2.4 [Lists], page 11), the shell waits for all commands in the pipeline to complete.

---

<!-- Source: 01_normalize/output/x200_102/bash_c03_clean.md -->

Each command in a multi-command pipeline, where pipes are created, is executed in its own _subshell_ , which is a separate process (see Section 3.7.3 [Command Execution Environment], page 46). If the `lastpipe` option is enabled using the `shopt` builtin (see Section 4.3.2 [The Shopt Builtin], page 78), and job control is not active, the last element of a pipeline may be run by the shell process.

---

<!-- Source: 01_normalize/output/x200_102/bash_c03_clean.md -->

The exit status of a pipeline is the exit status of the last command in the pipeline, unless the `pipefail` option is enabled (see Section 4.3.1 [The Set Builtin], page 74). If `pipefail` is enabled, the pipeline's return status is the value of the last (rightmost) command to exit with a non-zero status, or zero if all commands exit successfully. If the reserved word ' `!` ' precedes the pipeline, the exit status is the logical negation of the exit status as described

---

<!-- Source: 01_normalize/output/x200_102/bash_c03_clean.md -->

above. If a pipeline is not executed asynchronously (see Section 3.2.4 [Lists], page 11), the shell waits for all commands in the pipeline to terminate before returning a value. The return status of an asynchronous pipeline is 0.

---

<!-- Source: 01_normalize/output/x200_102/bash_c03_clean.md -->

Compound commands are the shell programming language constructs. Each construct begins with a reserved word or control operator and is terminated by a corresponding reserved word or operator. Any redirections (see Section 3.6 [Redirections], page 41) associated with a compound command apply to all commands within that compound command unless explicitly overridden.

---

<!-- Source: 01_normalize/output/x200_102/cli_and_Shell_Scripting_clean.md -->

location (such as a file). Redirection can be used for input as well as output, redirecting a file to a command for input. This section describes what you need to do to use redirection in your shell scripts.

---

<!-- Source: 01_normalize/output/x200_102/cli_and_Shell_Scripting_clean.md -->

## **Output redirection**

---

<!-- Source: 01_normalize/output/x200_102/cli_and_Shell_Scripting_clean.md -->

The most basic type of redirection is sending output from a command to a file. The Bash shell uses the greater-than symbol ( `>` ) for this:

---

<!-- Source: 01_normalize/output/x200_102/cli_and_Shell_Scripting_clean.md -->

```
command> outputfile
```

---

<!-- Source: 01_normalize/output/x200_102/cli_and_Shell_Scripting_clean.md -->

Anything that would appear on the monitor from the command instead is stored in the output file specified:

---

<!-- Source: 01_normalize/output/x200_102/cli_and_Shell_Scripting_clean.md -->

```
$ date> test6
$ ls -l test6
-rw-r--r--    1 user     user           29 Jun 01 16:56 test6
$ cat test6
Mon Jun 01 16:56:58 EDT 2020
$
```

---

<!-- Source: 01_normalize/output/x200_102/cli_and_Shell_Scripting_clean.md -->

The redirect operator created the file `test6` (using the default `umask` settings) and redirected the output from the `date` command to the `test6` file. If the output file already exists, the redirect operator overwrites the existing file with the new file data:

---

<!-- Source: 01_normalize/output/x200_102/cli_and_Shell_Scripting_clean.md -->

```
$ who> test6
$ cat test6
rich     pts/0    Jun 01 16:55
$
```

---

<!-- Source: 01_normalize/output/x200_102/cli_and_Shell_Scripting_clean.md -->

Now the contents of the `test6` file contain the output from the `who` command.

---

<!-- Source: 01_normalize/output/x200_102/cli_and_Shell_Scripting_clean.md -->

Sometimes, instead of overwriting the file's contents, you may need to append output from a command to an existing file — for example, if you're creating a log file to document an action on the system. In this situation, you can use the `>>` double greater-than symbol ( ) to append data:

---

<!-- Source: 01_normalize/output/x200_102/cli_and_Shell_Scripting_clean.md -->

```
$ date>> test6
$ cat test6
rich     pts/0    Jun 01 16:55
Mon Jun 01 17:02:14 EDT 2020
$
```

---

<!-- Source: 01_normalize/output/x200_102/cli_and_Shell_Scripting_clean.md -->

The `test6` file still contains the original data from the `who` command processed earlier — plus now it contains the new output from the `date` command.

---

<!-- Source: 01_normalize/output/x200_102/cli_and_Shell_Scripting_clean.md -->

## **Input redirection**

---

<!-- Source: 01_normalize/output/x200_102/cli_and_Shell_Scripting_clean.md -->

Input redirection is the opposite of output redirection. Instead of taking the output of a command and redirecting it to a file, input redirection takes the content of a file and redirects it to a command.

---

<!-- Source: 01_normalize/output/x200_102/cli_and_Shell_Scripting_clean.md -->

The input redirection symbol is the less-than symbol ( `<` ):

---

<!-- Source: 01_normalize/output/x200_102/cli_and_Shell_Scripting_clean.md -->

```
command < inputfile
```

---

<!-- Source: 01_normalize/output/x200_102/cli_and_Shell_Scripting_clean.md -->

The easy way to remember this is that the command is always listed first in the command line, and the redirection symbol "points" to the way the data is flowing. The less-than symbol indicates that the data is flowing from the input file to the command.

---

<!-- Source: 01_normalize/output/x200_102/cli_and_Shell_Scripting_clean.md -->

Here's an example of using input redirection with the `wc` command:

---

<!-- Source: 01_normalize/output/x200_102/cli_and_Shell_Scripting_clean.md -->

```
$ wc < test6
      2      11      60
$
```

---

<!-- Source: 01_normalize/output/x200_102/cli_and_Shell_Scripting_clean.md -->

By redirecting a text file to the `wc` command, you can get a quick count of the lines, words, and bytes in the file. The example shows that there are 2 lines, 11 words, and 60 bytes in the `test6` file.

---

<!-- Source: 01_normalize/output/x200_102/cli_and_Shell_Scripting_clean.md -->

There's another method of input redirection, called _inline input redirection_ . This method allows you to specify the data for input redirection on the command line instead of in a file. This may seem somewhat odd at first, but there are a few applications for this process (such as those shown in the "Performing Math" section later).

---

<!-- Source: 01_normalize/output/x200_102/cli_and_Shell_Scripting_clean.md -->

`<<` The inline input redirection symbol is the double less-than symbol ( ). Besides this symbol, you must specify a text marker that delineates the beginning and end of the data used for input. You can use any string value for the text marker, but it must be the same at the beginning of the data and the end of the data:

---

<!-- Source: 01_normalize/output/x200_102/cli_and_Shell_Scripting_clean.md -->

```
command << marker
data
marker
```

---

<!-- Source: 01_normalize/output/x200_102/cli_and_Shell_Scripting_clean.md -->

```
$ wc << EOF
> test string 1
> test string 2
> test string 3
> EOF
      3       9      42
$
```

---

<!-- Source: 01_normalize/output/x200_102/cli_and_Shell_Scripting_clean.md -->

The secondary prompt continues to prompt for more data until you enter the string value for the text marker. The `wc` command performs the line, word, and byte counts of the data supplied by the inline input redirection.

---

<!-- Source: 01_normalize/output/x200_102/cli_and_Shell_Scripting_clean.md -->

## **Employing Pipes**

---

<!-- Source: 01_normalize/output/x200_102/cli_and_Shell_Scripting_clean.md -->

There are times when you need to send the output of one command to the input of another command. This is possible using redirection, but somewhat clunky:

---

<!-- Source: 01_normalize/output/x200_102/cli_and_Shell_Scripting_clean.md -->

```
$ rpm -qa> rpm.list
$ sort < rpm.list
abattis-cantarell-fonts-0.0.25-1.el7.noarch
abrt-2.1.11-52.el7.centos.x86_64
abrt-addon-ccpp-2.1.11-52.el7.centos.x86_64
abrt-addon-kerneloops-2.1.11-52.el7.centos.x86_64
abrt-addon-pstoreoops-2.1.11-52.el7.centos.x86_64
abrt-addon-python-2.1.11-52.el7.centos.x86_64
abrt-addon-vmcore-2.1.11-52.el7.centos.x86_64
abrt-addon-xorg-2.1.11-52.el7.centos.x86_64
abrt-cli-2.1.11-52.el7.centos.x86_64
abrt-console-notification-2.1.11-52.el7.centos.x86_64
...
```

---

<!-- Source: 01_normalize/output/x200_102/cli_and_Shell_Scripting_clean.md -->

Using the standard output redirection, the output was redirected from the `rpm` command to a file called `rpm.list` . After the command finished, the `rpm.list` file contained a list of all the installed software packages on this system. Next, input redirection was used to send the contents of the `rpm.list` file to the `sort` command to sort the package names alphabetically.

---

<!-- Source: 01_normalize/output/x200_102/cli_and_Shell_Scripting_clean.md -->

That was useful, but again, a somewhat clunky way of producing the information. Instead of redirecting the output of a command to a file, you can redirect the output to another command. This process is called _piping_ .

---

<!-- Source: 01_normalize/output/x200_102/cli_and_Shell_Scripting_clean.md -->

Like the command substitution backtick ( ``` ), the symbol for piping is not used often outside of shell scripting. The symbol is two vertical lines, one above the other. However, the pipe symbol often looks like a single vertical line in print ( `|` ). On a U.S. keyboard, it is usually on the same key as the backslash ( `\` ). The pipe is put between the commands to redirect the output from one to the other:

---

<!-- Source: 01_normalize/output/x200_102/cli_and_Shell_Scripting_clean.md -->

```
command1 | command2
```

---

<!-- Source: 01_normalize/output/x200_102/cli_and_Shell_Scripting_clean.md -->

Don't think of piping as running two commands back to back. The Linux system actually runs both commands at the same time, linking them together internally in the system. As the first command produces output, it's sent immediately to the second command. No intermediate files or buffer areas are used to transfer the data.

---

<!-- Source: 01_normalize/output/x200_102/cli_and_Shell_Scripting_clean.md -->

Now, using piping you can easily pipe the output of the `rpm` command directly to the `sort` command to produce your results:

---

<!-- Source: 01_normalize/output/x200_102/cli_and_Shell_Scripting_clean.md -->

```
$ rpm -qa | sort
abattis-cantarell-fonts-0.0.25-1.el7.noarch
abrt-2.1.11-52.el7.centos.x86_64
abrt-addon-ccpp-2.1.11-52.el7.centos.x86_64
abrt-addon-kerneloops-2.1.11-52.el7.centos.x86_64
abrt-addon-pstoreoops-2.1.11-52.el7.centos.x86_64
abrt-addon-python-2.1.11-52.el7.centos.x86_64
abrt-addon-vmcore-2.1.11-52.el7.centos.x86_64
abrt-addon-xorg-2.1.11-52.el7.centos.x86_64
abrt-cli-2.1.11-52.el7.centos.x86_64
abrt-console-notification-2.1.11-52.el7.centos.x86_64
...
```

---

<!-- Source: 01_normalize/output/x200_102/cli_and_Shell_Scripting_clean.md -->

Unless you're a (very) quick reader, you probably couldn't keep up with the output generated by this command. Because the piping feature operates in real time, as soon as the `rpm` command produces data, the `sort` command gets busy sorting it. By the time the `rpm` command finishes outputting data, the `sort` command already has the data sorted and starts displaying it on the monitor.

---

<!-- Source: 01_normalize/output/x200_102/cli_and_Shell_Scripting_clean.md -->

There's no limit to the number of pipes you can use in a command. You can continue piping the output of commands to other commands to refine your operation.

---

<!-- Source: 01_normalize/output/x200_102/cli_and_Shell_Scripting_clean.md -->

In this case, because the output of the `sort` command zooms by so quickly, you can use one of the text paging commands (such as `less` or `more` ) to force the output to stop at every screen of data:

---

<!-- Source: 01_normalize/output/x200_102/cli_and_Shell_Scripting_clean.md -->

## `$ rpm -qa | sort | more`

---

<!-- Source: 01_normalize/output/x200_102/cli_and_Shell_Scripting_clean.md -->

This command sequence runs the `rpm` command, pipes the output to the `sort` command, and then pipes that output to the `more` command to display the data, stopping after every screen of information. This now lets you pause and read what's on the display before continuing, as shown in Figure 11-1.

---

<!-- Source: 01_normalize/output/x200_102/cli_and_Shell_Scripting_clean.md -->

To get even fancier, you can use redirection along with piping to save your output to a file:

---

<!-- Source: 01_normalize/output/x200_102/cli_and_Shell_Scripting_clean.md -->

```
$ rpm -qa | sort> rpm.list
$ more rpm.list
abrt-1.1.14-1.fc14.i686
abrt-addon-ccpp-1.1.14-1.fc14.i686
abrt-addon-kerneloops-1.1.14-1.fc14.i686
abrt-addon-python-1.1.14-1.fc14.i686
abrt-desktop-1.1.14-1.fc14.i686
abrt-gui-1.1.14-1.fc14.i686
abrt-libs-1.1.14-1.fc14.i686
abrt-plugin-bugzilla-1.1.14-1.fc14.i686
abrt-plugin-logger-1.1.14-1.fc14.i686
abrt-plugin-runapp-1.1.14-1.fc14.i686
acl-2.2.49-8.fc14.i686
...
```

---

<!-- Source: 01_normalize/output/x200_102/cli_and_Shell_Scripting_clean.md -->

By far one of the most popular uses is piping the results of commands that produce long output to the `more` command. This is especially common with the `ls` command, as shown in Figure 11-2.

---

<!-- Source: 01_normalize/output/x200_102/cli_and_Shell_Scripting_clean.md -->

The `ls -l` command produces a long listing of all the files in the directory. For directories with lots of files, this can be quite a listing. By piping the output to the `more` command, you force the output to stop at the end of every screen of data.

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

6 RE DI RECT ION

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

In this les son we are go ing to un leash what may be the coolest fea ture of the com mand line. It's called I/O re di rect ion. The "I/O" stands for in put/out put, and with this fa cil ity you can re di rect the in put and out put of com mands

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

to and from files, as well as con nect mul ti ple com mands to gether into pow er ful com mand pipe lines. To show off this fa cil ity, we will in tro duce the fol low ing com mands:

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

**`uniq`** Re port or omit re peated lines **`grep`** Print lines match ing a pat tern **`wc`** Print new line, word, and byte counts for each file **`head`** Out put the first part of a file **`tail`** Out put the last part of a file **`tee`** Read from stan dard in put and write to stan dard out put and files

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

## Stan dard In put, Out put, and Er ror

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

Many of the pro grams that we have used so far pro duce out put of some kind. This out put of ten con sists of two types.

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

The pro gram's re sults; that is, the data the pro gram is de signed to pro duce Sta tus and er ror mes sages that tell us how the pro gram is get ting along

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

If we look at a com mand like `ls` , we can see that it dis plays its re sults and its er ror mes sages on the screen.

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

Keep ing with the Unix theme of "ev ery thing is a file," pro grams such as `ls` ac tu ally send their re sults to a spe cial file called standard out put (of ten ex pressed as std out) and their sta tus mes sages to an other file called stan dard er ror (stderr). By de fault, both stan dard out put and stan dard er ror are linked to the screen and not saved into a disk file.

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

In ad di tion, many pro grams take in put from a fa cil ity called stan dard in put (stdin), which is, by de fault, at tached to the key board.

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

I/O re di rect ion al lows us to change where out put goes and where in put comes from. Nor mally, out put goes to the screen and input comes from the key board, but with I/O re di rect ion, we can change that.

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

## Redi rect ing Stan dard Out put

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

I/O re di rect ion al lows us to re de fine where stan dard out put goes. To re di rect stan dard out put to an other file in stead of the screen, we use the `>` re di rect ion op er a tor fol lowed by the name of the file. Why would we want to do this? It's of ten use ful to store the output of a com mand in a file. For ex am ple, we could tell the shell to send the out put of the `ls` com mand to the file ls-out put.txt in stead of the screen.

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

```
[me@lin uxbox ~]$ ls -l /usr/bin > ls-out put.txt
```

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

Here, we cre ated a long list ing of the /usr/bin di rec tory and sent the re sults to the file ls-out put.txt. Let's ex am ine the redi rected out put of the com mand, shown here:

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

Good—a nice, large, text file. If we look at the file with `less` , we will see that the file ls-out put.txt does in deed con tain the re sults from our `ls` com mand.

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

ist.

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

```
[me@lin uxbox ~]$ ls -l /bin/usr > ls-out put.txt
```

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

We re ceived an er ror mes sage. This makes sense since we spec i fied the nonex is tent di rec tory /bin/usr, but why was the er ror mes sage dis played on the screen rather than be ing redi rected to the file ls-out put.txt? The an swer is that the `ls` pro gram does not send its er ror mes sages to stan dard out put. In stead, like most well-writ ten Unix pro grams, it sends its er ror mes sages to stan dard er ror. Be cause we redi rected only stan dard out put and not stan dard er ror, the er ror mes sage was still sent to the screen. We'll see how to re di rect stan dard er ror in just a minute, but first let's look at what hap pened to our out put file.

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

```
[me@lin uxbox ~]$ ls -l ls-out put.txt
-rw-rw-r-- 1 me   me   0 2018-02-01 15:08 ls-out put.txt
```

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

`>` The file now has zero length! This is be cause when we re di rect out put with the re di rect ion op er a tor, the des ti na tion file is always rewrit ten from the be gin ning. Be cause our `ls` com mand gen er ated no re sults and only an er ror mes sage, the re di rect ion op er a- tion started to re write the file and then stopped be cause of the er ror, re sult ing in its trun ca tion. In fact, if we ever need to ac tu ally trun cate a file (or cre ate a new, empty file), we can use a trick like this:

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

```
[me@lin uxbox ~]$ > ls-out put.txt
```

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

Sim ply us ing the re di rect ion op er a tor with no com mand pre ced ing it will trun cate an ex ist ing file or cre ate a new, empty file.

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

So, how can we ap pend redi rected out put to a file in stead of over writ ing the file from the be gin ning? For that, we use the `>>` redi rect ion op er a tor, like so:

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

```
[me@lin uxbox ~]$ ls -l /usr/bin >> ls-out put.txt
```

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

`>>` Us ing the op er a tor will re sult in the out put be ing ap pended to the file. If the file does not al ready ex ist, it is cre ated just as `>` though the op er a tor had been used. Let's put it to the test.

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

```
[me@lin uxbox ~]$ ls -l /usr/bin >> ls-out put.txt
[me@lin uxbox ~]$ ls -l /usr/bin >> ls-out put.txt
[me@lin uxbox ~]$ ls -l /usr/bin >> ls-out put.txt
[me@lin uxbox ~]$ ls -l ls-out put.txt
-rw-rw-r-- 1 me   me   503634 2018-02-01 15:45 ls-out put.txt
```

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

## Redi rect ing Stan dard Er ror

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

Redi rect ing stan dard er ror lacks the ease of a ded i cated re di rect ion op er a tor. To re di rect stan dard er ror, we must re fer to its file descrip tor. A pro gram can pro duce out put on any of sev eral num bered file streams. While we have re ferred to the first three of these file streams as stan dard in put, out put, and er ror, the shell ref er ences them in ter nally as file de scrip tors 0, 1, and 2, re spec tively. The shell pro vides a no ta tion for redi rect ing files us ing the file de scrip tor num ber. Be cause stan dard er ror is the same as file de scrip tor num ber 2, we can re di rect stan dard er ror with this no ta tion:

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

```
[me@lin uxbox ~]$ ls -l /bin/usr 2> ls-er ror.txt
```

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

The file de scrip tor 2 is placed im me di ately be fore the re di rect ion op er a tor to per form the re di rect ion of stan dard er ror to the file ls-er ror.txt.

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

## Redi rect ing Stan dard Out put and Stan dard Er ror to One File

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

There are cases in which we may want to cap ture all of the out put of a com mand to a sin gle file. To do this, we must re di rect both stan dard out put and stan dard er ror at the same time. There are two ways to do this. Shown here is the tra di tional way, which works with old ver sions of the shell:

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

```
[me@lin uxbox ~]$ ls -l /bin/usr > ls-out put.txt 2>&1
```

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

Us ing this method, we per form two redi rec tions. First we re di rect stan dard out put to the file ls-out put.txt, and then we re di rect file de scrip tor 2 (stan dard er ror) to file de scrip tor 1 (stan dard out put) us ing the no ta tion `2>&1` .

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

## NO TICE THAT THE OR DER OF THE REDI REC TIONS IS SIG NIF I CANT

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

The re di rect ion of stan dard er ror must al ways oc cur af ter redi rect ing stan dard out put or it doesn't work. The fol low ing ex ample redi rects stan dard er ror to the file ls-out put.txt:

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

```
>ls-out put.txt 2>&1
```

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

If the or der is changed to the fol low ing, then stan dard er ror is di rected to the screen:

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

```
2>&1 >ls-out put.txt
```

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

Re cent ver sions of `bash` pro vide a sec ond, more stream lined method for per form ing this com bined re di rect ion, shown here:

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

- `[me@lin uxbox ~]$` **`ls -l /bin/usr &> ls-out put.txt`**

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

In this ex am ple, we use the sin gle no ta tion `&>` to re di rect both stan dard out put and stan dard er ror to the file ls-out put.txt. You may also ap pend the stan dard out put and stan dard er ror streams to a sin gle file like so:

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

```
[me@lin uxbox ~]$ ls -l /bin/usr &>> ls-out put.txt
```

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

## Dis pos ing of Un wanted Out put

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

Some times "si lence is golden" and we don't want out put from a com mand; we just want to throw it away. This ap plies par tic u larly to er ror and sta tus mes sages. The sys tem pro vides a way to do this by redi rect ing out put to a spe cial file called /dev/null. This file is a sys tem de vice of ten re ferred to as a bit bucket, which ac cepts in put and does noth ing with it. To sup press er ror mes sages from a com mand, we do this:

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

```
[me@lin uxbox ~]$ ls -l /bin/usr 2> /dev/null
```

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

## Redi rect ing Stan dard In put

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

The `cat` com mand reads one or more files and copies them to stan dard out put like so:

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

```
[me@lin uxbox ~]$ cat ls-out put.txt
```

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

```
cat movie.mpeg.0* > movie.mpeg
```

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

This is all well and good, but what does this have to do with stan dard in put? Noth ing yet, but let's try some thing else. What hap pens if we en ter **`cat`** with no ar gu ments?

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

If `cat` is not given any ar gu ments, it reads from stan dard in put, and since stan dard in put is, by de fault, at tached to the key board, it's wait ing for us to type some thing! Try adding the fol low ing text and press ing EN TER:

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

```
[me@lin uxbox ~]$ cat
The quick brown fox jumped over the lazy dog.
The quick brown fox jumped over the lazy dog.
```

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

In the ab sence of file name ar gu ments, `cat` copies stan dard in put to stan dard out put, so we see our line of text re peated. We can use this be hav ior to cre ate short text files. Let's say we wanted to cre ate a file called lazy_ dog.txt con tain ing the text in our ex am ple. We would do this:

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

```
[me@lin uxbox ~]$ cat > lazy_ dog.txt
The quick brown fox jumped over the lazy dog.
```

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

Type the com mand fol lowed by the text we want to place in the file. Re mem ber to type CTRL-D at the end. Us ing the com mand line, we have im ple mented the world's dumb est word pro ces sor! To see our re sults, we can use `cat` to copy the file to std out again.

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

Now that we know how `cat` ac cepts stan dard in put, in ad di tion to file name ar gu ments, let's try redi rect ing stan dard in put.

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

```
[me@lin uxbox ~]$ cat < lazy_ dog.txt
The quick brown fox jumped over the lazy dog.
```

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

Us ing the `<` re di rect ion op er a tor, we change the source of stan dard in put from the key board to the file lazy_ dog.txt. We see that the re sult is the same as pass ing a sin gle file name ar gu ment. This is not par tic u larly use ful com pared to pass ing a file name ar gument, but it serves to demon strate us ing a file as a source of stan dard in put. Other com mands make bet ter use of stan dard in put, as we will soon see.

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

## Pipe lines

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

The ca pa bil ity of com mands to read data from stan dard in put and send to stan dard out put is uti lized by a shell fea ture called pipelines. Us ing the pipe op er a tor `|` , the stan dard out put of one com mand can be piped into the stan dard in put of an other.

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

```
com mand1 | com mand2
```

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

To fully demon strate this, we are go ing to need some com mands. Re mem ber how we said there was one we al ready knew that ac cepts stan dard in put? It's `less` . We can use `less` to dis play, page by page, the out put of any com mand that sends its re sults to standard out put.

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

```
[me@lin uxbox ~]$ ls -l /usr/bin | less
```

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

This is ex tremely handy! Us ing this tech nique, we can con ve niently ex am ine the out put of any com mand that pro duces stan dard out put.

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

Pipe lines are of ten used to per form com plex op er a tions on data. It is pos si ble to put sev eral com mands to gether into a pipe line. Fre quently, the com mands used this way are re ferred to as fil ters. Fil ters take in put, change it some how, and then out put it. The first one we will try is `sort` . Imag ine we wanted to make a com bined list of all the ex e cutable pro grams in /bin and /usr/bin, put them in sorted or der, and view the re sult ing list.

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

```
[me@lin uxbox ~]$ ls /bin /usr/bin | sort | less
```

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

Be cause we spec i fied two di rec to ries (/bin and /usr/bin), the out put of `ls` would have con sisted of two sorted lists, one for each direc tory. By in clud ing `sort` in our pipe line, we changed the data to pro duce a sin gle, sorted list.

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

## THE DIF FER ENCE BE TWEEN > AND |

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

At first glance, it may be hard to un der stand the re di rect ion per formed by the pipe line op er a tor `|` ver sus the re di rect ion op er a- tor `>` . Sim ply put, the re di rect ion op er a tor con nects a com mand with a file, while the pipe line op er a tor con nects the out put of one com mand with the in put of a sec ond com mand.

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

```
com mand1 > file1
com mand1 | com mand2
```

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

```
com mand1 > com mand2
```

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

```
# cd /usr/bin
# ls > less
```

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

The first com mand put him in the di rec tory where most pro grams are stored, and the sec ond com mand told the shell to over write the file less with the out put of the `ls` com mand. Since the /usr/bin di rec tory al ready con tained a file named less (the `less` pro gram), the sec ond com mand over wrote the less pro gram file with the text from `ls` , thus de stroy ing the `less` pro gram on his sys tem.

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

The les son here is that the re di rect ion op er a tor silently cre ates or over writes files, so you need to treat it with a lot of respect.

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

The `uniq` com mand is of ten used in con junc tion with `sort` . `uniq` ac cepts a sorted list of data from ei ther stan dard in put or a sin gle filename ar gu ment (see the `uniq` man page for de tails) and, by de fault, re moves any du pli cates from the list. So, to make sure our list has no du pli cates (that is, any pro grams of the same name that ap pear in both the /bin and /usr/bin di rec to ries), we will add `uniq` to our pipe line.

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

```
[me@lin uxbox ~]$ ls /bin /usr/bin | sort | uniq | less
```

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

In this ex am ple, we use `uniq` to re move any du pli cates from the out put of the `sort` com mand. If we want to see the list of du plicates in stead, we add the `-d` op tion to `uniq` like so:

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

```
[me@lin uxbox ~]$ ls /bin /usr/bin | sort | uniq -d | less
```

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

```
[me@lin uxbox ~]$ wc ls-out put.txt
 7902  64566 503634 ls-out put.txt
```

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

In this case, it prints out three num bers: lines, words, and bytes con tained in ls-out put.txt. Like our pre vi ous com mands, if ex e- cuted with out com mand line ar gu ments, `wc` ac cepts stan dard in put. The `-l` op tion lim its its out put to re port only lines. Adding it to a pipe line is a handy way to count things. To see the num ber of items we have in our sorted list, we can do this:

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

```
[me@lin uxbox ~]$ ls /bin /usr/bin | sort | uniq | wc -l

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

```

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

```
[me@lin uxbox ~]$ ls /bin /usr/bin | sort | uniq | grep zip
bun zip2
bzip2
gun zip
gzip
un zip
zip
zip cloak
zip grep
zip info
zip note
zip split
```

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

Some times you don't want all the out put from a com mand. You might want only the first few lines or the last few lines. The `head` com mand prints the first 10 lines of a file, and the `tail` com mand prints the last 10 lines. By de fault, both com mands print 10 lines of text, but this can be ad justed with the `-n` op tion.

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

```
[me@lin uxbox ~]$ head -n 5 ls-out put.txt
to tal 343496
-rwxr-xr-x 1 root root       31316 2017-12-05 08:58 [
-rwxr-xr-x 1 root root        8240 2017-12-09 13:39 411toppm
-rwxr-xr-x 1 root root      111276 2017-11-26 14:27 a2p
-rwxr-xr-x 1 root root       25368 2016-10-06 20:16 a52dec
[me@lin uxbox ~]$ tail -n 5 ls-out put.txt
-rwxr-xr-x 1 root root        5234 2017-06-27 10:56 znew
-rwxr-xr-x 1 root root         691 2015-09-10 04:21 zonetab2pot.py
-rw-r--r-- 1 root root         930 2017-11-01 12:23 zonetab2pot.pyc
-rw-r--r-- 1 root root         930 2017-11-01 12:23 zonetab2pot.pyo
lr wxr wxrwx 1 root root           6 2016-01-31 05:22 zsoe lim -> soe lim
```

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

These can be used in pipe lines as well:

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

```
[me@lin uxbox ~]$ ls /usr/bin | tail -n 5
znew
zonetab2pot.py
zonetab2pot.pyc
zonetab2pot.pyo
zsoe lim
```

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

```
[me@lin uxbox ~]$ tail -f /var/log/mes sages
Feb  8 13:40:05 twin4 dhclient: DHC PACK from 192.168.1.1
Feb  8 13:40:05 twin4 dhclient: bound to 192.168.1.4 -- re newal in 1652 sec onds.
Feb  8 13:55:32 twin4 mountd[3953]: /var/NFSv4/mu sicbox ex ported to both 192.168.1.0/24 and
twin7.lo cal do main in 192.168.1.0/24,twin7.lo cal do main
Feb  8 14:07:37 twin4 dhclient: DHCPRE QUEST on eth0 to 192.168.1.1 port 67
Feb  8 14:07:37 twin4 dhclient: DHC PACK from 192.168.1.1
Feb  8 14:07:37 twin4 dhclient: bound to 192.168.1.4 -- re newal in 1771 sec onds.
Feb  8 14:09:56 twin4 smartd[3468]: De vice: /dev/hda, SMART Pre fail ure At tribute: 8 Seek_ Time_
Per for mance changed from 237 to 236
Feb  8 14:10:37 twin4 mountd[3953]: /var/NFSv4/mu sicbox ex ported to both 192.168.1.0/24 and
twin7.lo cal do main in 192.168.1.0/24,twin7.lo cal do main
Feb  8 14:25:07 twin4 sshd(pam_u nix)[29234]: ses sion opened for user me by (uid=0)
Feb  8 14:25:36 twin4 su(pam_u nix)[29279]: ses sion opened for user root by me(uid=500)
```

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

## tee: Read from Stdin and Out put to Std out and Files

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

In keep ing with our plumb ing metaphor, Linux pro vides a com mand called `tee` that cre ates a "tee" fit ting on our pipe. The `tee` program reads stan dard in put and copies it to both stan dard out put (al low ing the data to con tinue down the pipe line) and to one or more files. This is use ful for cap tur ing a pipe line's con tents at an in ter me di ate stage of pro cess ing. Here we re peat one of our earlier ex am ples, this time in clud ing `tee` to cap ture the en tire di rec tory list ing to the file ls.txt be fore `grep` fil ters the pipe line's con tents:

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

```
[me@lin uxbox ~]$ ls /usr/bin | tee ls.txt | grep zip
bun zip2
bzip2
gun zip
gzip
un zip
zip
zip cloak
zip grep
zip info
zip note
zip split
```

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

As al ways, check out the doc u men ta tion of each of the com mands we have cov ered in this chap ter. We have seen only their most ba sic us age. They all have a num ber of in ter est ing op tions. As we gain Linux ex pe ri ence, we will see that the re di rect ion fea ture of

---

<!-- Source: 01_normalize/output/x200_102/cli_clean.md -->

the com mand line is ex tremely use ful for solv ing spe cial ized prob lems. There are many com mands that make use of stan dard in put and out put, and al most all com mand line pro grams use stan dard er ror to dis play their in for ma tive mes sages.

---

<!-- Source: 01_normalize/output/x200_102/libc_clean.md -->

Before you can read or write the contents of a file, you must establish a connection or communications channel to the file. This process is called _opening_ the file. You can open a file for reading, writing, or both.

---

<!-- Source: 01_normalize/output/x200_102/libc_clean.md -->

File descriptors provide a primitive, low-level interface to input and output operations. Both file descriptors and streams can represent a connection to a device (such as a terminal), or a pipe or socket for communicating with another process, as well as a normal file. But, if you want to do control operations that are specific to a particular kind of device, you must use a file descriptor; there are no facilities to use streams in this way. You must also

---

<!-- Source: 01_normalize/output/x200_102/libc_clean.md -->

use file descriptors if your program needs to do input or output in special modes, such as nonblocking (or polled) input (see Section 13.15 [File Status Flags], page 402).

---

<!-- Source: 01_normalize/output/x200_102/libc_clean.md -->

Since streams are implemented in terms of file descriptors, you can extract the file descriptor from a stream and perform low-level operations directly on the file descriptor. You can also initially open a connection as a file descriptor and then make a stream associated with that file descriptor.

---

<!-- Source: 01_normalize/output/x200_102/libc_clean.md -->

Streams and descriptors that are opened for _append access_ are treated specially for output: output to such files is _always_ appended sequentially to the _end_ of the file, regardless

---

<!-- Source: 01_normalize/output/x200_102/libc_clean.md -->

By contrast, if you open a descriptor and then duplicate it to get another descriptor, these two descriptors share the same file position: changing the file position of one descriptor will affect the other.

---

<!-- Source: 01_normalize/output/x200_102/libc_clean.md -->

```
FILE
```

---

<!-- Source: 01_normalize/output/x200_102/libc_clean.md -->

[Data Type]

---

<!-- Source: 01_normalize/output/x200_102/libc_clean.md -->

## **12.2 Standard Streams**

---

<!-- Source: 01_normalize/output/x200_102/libc_clean.md -->

When the `main` function of your program is invoked, it already has three predefined streams open and available for use. These represent the "standard" input and output channels that have been established for the process.

---

<!-- Source: 01_normalize/output/x200_102/libc_clean.md -->

The _standard input_ stream, which is the normal source of input for the program.

---

<!-- Source: 01_normalize/output/x200_102/libc_clean.md -->

`FILE * stdout` [Variable] The _standard output_ stream, which is used for normal output from the program.

---

<!-- Source: 01_normalize/output/x200_102/libc_clean.md -->

`FILE * stderr` [Variable] The _standard error_ stream, which is used for error messages and diagnostics issued by the program.

---

<!-- Source: 01_normalize/output/x200_102/libc_clean.md -->

On GNU systems, you can specify what files or processes correspond to these streams using the pipe and redirection facilities provided by the shell. (The primitives shells use to implement these facilities are described in Chapter 14 [File System Interface], page 418.)

---

<!-- Source: 01_normalize/output/x200_102/libc_clean.md -->

- ' `a` ' Open a file for append access; that is, writing at the end of file only. If the file already exists, its initial contents are unchanged and output to the stream is appended to the end of the file. Otherwise, a new, empty file is created.

---

<!-- Source: 01_normalize/output/x200_102/lpi_clean.md -->

## 2.5 File I/O Model

---

<!-- Source: 01_normalize/output/x200_102/lpi_clean.md -->

One of the distinguishing features of the I/O model on UNIX systems is the concept of universality of I/O. This means that the same system calls (open(), read(), write(), close(), and so on) are used to perform I/O on all types of files, including devices. (The kernel translates the application's I/O requests into appropriate file-system or device-driver operations that perform I/O on the target file or device.) Thus, a program employing these system calls will work on any type of file.

---

<!-- Source: 01_normalize/output/x200_102/lpi_clean.md -->

## File descriptors

---

<!-- Source: 01_normalize/output/x200_102/lpi_clean.md -->

Normally, a process inherits three open file descriptors when it is started by the shell: descriptor 0 is standard input, the file from which the process takes its input; descriptor 1 is standard output, the file to which the process writes its output; and descriptor 2 is standard error, the file to which the process writes error messages and notification of exceptional or abnormal conditions. In an interactive shell or program, these three descriptors are normally connected to the terminal. In the stdio library, these descriptors correspond to the file streams stdin, stdout, and stderr.

---

<!-- Source: 01_normalize/output/x200_102/lpi_clean.md -->

All system calls for performing I/O refer to open files using a file descriptor, a (usually small) nonnegative integer. File descriptors are used to refer to all types of open files, including pipes, FIFOs, sockets, terminals, devices, and regular files. Each process has its own set of file descriptors.

---

<!-- Source: 01_normalize/output/x200_102/lpi_clean.md -->

By convention, most programs expect to be able to use the three standard file descriptors listed in Table 4-1. These three descriptors are opened on the program's behalf by the shell, before the program is started. Or, more precisely, the program inherits copies of the shell's file descriptors, and the shell normally operates with these three file descriptors always open. (In an interactive shell, these three file descriptors normally refer to the terminal under which the shell is running.) If I/O redirections are specified on a command line, then the shell ensures that the file descriptors are suitably modified before starting the program.

---

<!-- Source: 01_normalize/output/x200_102/lpi_clean.md -->

|File descriptor|Purpose|POSIX name|stdiostream|
|---|---|---|---|
|0<br>1<br>2|standard input<br>standard output <br>standard error|`STDIN_FILENO`<br> `STDOUT_FILENO` <br>`STDERR_FILENO`|stdin<br> stdout<br> stderr|

---

<!-- Source: 01_normalize/output/x200_102/lpi_clean.md -->

When referring to these file descriptors in a program, we can use either the numbers (0, 1, or 2) or, preferably, the POSIX standard names defined in `<unistd.h>` .

---

<!-- Source: 01_normalize/output/x200_102/lpi_clean.md -->

## 4.2 Universality of I/O

---

<!-- Source: 01_normalize/output/x200_102/lpi_clean.md -->

`$` **`./copy /dev/tty b.txt`** Copy input from this terminal to a regular file

---

## Extraction Summary

- Objective: x200_102
- Source files scanned: 14
- Total paragraphs classified: 1573
- Paragraphs classified RELEVANT: 733
- Paragraphs filtered out: 840
- Parse errors (kept): 5
- Batch ID: msgbatch_01YKgYEtx6FBgsha6XSUNj8d
- Run date: 2026-05-08
