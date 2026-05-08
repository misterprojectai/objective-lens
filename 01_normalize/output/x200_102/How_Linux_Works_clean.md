<!-- Source: 01_normalize/input/x200_102/How Linux Works.pdf | Cleaned: 2026-05-08 -->

When you in stall Linux, you should cre ate at least one reg u lar user to be your per sonal ac count. For this chap ter, you should log in as the reg u lar user.

Af ter log ging in, open a shell win dow (of ten re ferred to as a _ter mi nal_ ). The eas i est way to do so from a GUI like Gnome or KDE is to open a ter mi nal ap pli ca tion, which starts a shell in side a new win dow. Once you've opened a shell, it should dis play a prompt at the top that usu ally ends with a dol lar sign ( `$` ). On Ubuntu, that prompt should look like _`name@host:path`_ `$` , and on Fe dora, it's `[` _`name@host path`_ `]$` , where _`name`_ is your user name, _`host`_ is the name of your ma chine, and _`path`_ is your cur rent work ing di rec tory (see Sec tion 2.4.1). If you're fa mil iar with Win dows, the shell win dow will look some thing like a DOS com mand prompt; in macOS the Ter mi nal ap pli ca tion is es sen tially the same as a Linux shell win dow.

This book con tains many com mands that you will type at a shell prompt. They all be gin with a sin gle `$` to de note the shell prompt. For ex am ple, type this com mand (just the part in bold, not the `$` ) and press EN TER:

- `$` **`echo Hello there.`**

_Many shell com mands in this book start with_ `#` _. You should run these com mands as the su pe ruser (root), so they re quire ex tra cau tion. The best prac tice when run ning them is to use_ `sudo` _in or der to pro vide some pro tec tion and a log that you can look up later for pos si ble er rors. You'll see how to do this in Sec tion 2.20._

```
$ cat /etc/passwd
```

This com mand dis plays the con tents of the _/etc/passwd_ sys tem in for ma tion file and then re turns your shell prompt. Don't worry about what _this_ file does right now; you'll learn all about it in Chap ter 7. Com mands usu ally be gin with a pro gram to run and may be fol lowed by _ar gu ments_ that tell the pro gram what to op er ate on and how to do so. Here, the pro gram is `cat` , and there is one ar gu ment, `/etc/passwd` . Many ar gu ments are `-` op tions that mod ify the de fault be hav ior of a pro gram and typ i cally be gin with a dash ( ). You'll see this shortly in the dis cus sion of `ls` . There are some ex cep tions that don't fol low this nor mal com mand struc ture, how ever, such as shell built-ins and the tem po rary use of en vi ron ment vari ables.

The `cat` pro gram is one of the eas i est in Unix to un der stand; it sim ply out puts the con tents of one or more files or an ‐ other source of in put. The gen eral syn tax of a `cat` com mand is as fol lows:

- `$` **`cat`** _**`file1 file2`**_ **`...`**

When you run this com mand, `cat` prints the con tents of _`file1`_ , _`file2`_ , and any other files that you spec ify as ar gu ments (de noted by `...` in the pre ced ing ex am ple), and then ex its. The pro gram is called `cat` be cause it per forms con cate na tion when it prints the con tents of more than one file. There are many ways to run `cat` ; let's use it to ex plore Unix I/O.

Unix pro cesses use I/O _streams_ to read and write data. Pro cesses read data from in put streams and write data to out ‐ put streams. Streams are very flex i ble. For ex am ple, the source of an in put stream can be a file, a de vice, a ter mi nal win dow, or even the out put stream from an other process.

To see an in put stream at work, en ter **`cat`** (with no ar gu ments) and press EN TER. This time, you won't get any im me ‐ di ate out put, and you won't get your shell prompt back be cause `cat` is still run ning. Now type any thing and press EN ‐ TER at the end of each line. When used like this, the `cat` com mand re peats any line that you type. Once you're suffi ‐ ciently bored, press CTRL-D on an empty line to ter mi nate `cat` and re turn to the shell prompt.

The rea son `cat` adopts an in ter ac tive be hav ior here has to do with streams. When you don't spec ify an in put file ‐ name, `cat` reads from the _stan dard in put_ stream pro vided by the Linux ker nel rather than a stream con nected to a file. In this case, the stan dard in put is con nected to the ter mi nal where you run `cat` .

_Press ing CTRL-D on an empty line stops the cur rent stan dard in put en try from the ter mi nal with an EOF (end-offile) mes sage (and of ten ter mi nates a pro gram). Don't con fuse this with CTRL-C, which usu ally ter mi nates a pro ‐ gram re gard less of its in put or out put._

_Stan dard out put_ is sim i lar. The ker nel gives each process a stan dard out put stream where it can write its out put. The `cat` com mand al ways writes its out put to the stan dard out put. When you ran `cat` in the ter mi nal, the stan dard out put was con nected to that ter mi nal, so that's where you saw the out put.

Stan dard in put and out put are of ten ab bre vi ated as _stdin_ and _std out_ . Many com mands op er ate as `cat` does; if you don't spec ify an in put file, the com mand reads from stdin. Out put is a lit tle diff er ent. Some pro grams (like `cat` ) send out put only to std out, but oth ers have the op tion to send out put di rectly to files.

There is a third stan dard I/O stream, called _stan dard er ror_ . You'll see it in Sec tion 2.14.1.

One of the best fea tures of stan dard streams is that you can eas ily ma nip u late them to read and write to places other than the ter mi nal, as you'll learn in Sec tion 2.14. In par tic u lar, you'll learn how to con nect streams to files and other pro cesses.

The `ls` com mand lists the con tents of a di rec tory. The de fault is the cur rent di rec tory, but you can add any di rec tory or file as an ar gu ment, and there are many use ful op tions. For ex am ple, use `ls -l` for a de tailed (long) list ing and `ls -F` to dis play file type in for ma tion. Here is a sam ple long list ing; it in cludes the owner of the file (col umn 3), the group (col ‐ umn 4), the file size (col umn 5), and the mod i fi ca tion date/time (be tween col umn 5 and the file name):

```
$ ls -l
total 3616
-rw-r--r-- 1 juser users 3804    May 28 10:40  abusive.c
-rw-r--r-- 1 juser users 4165    Aug 13 10:01  battery.zip
-rw-r--r-- 1 juser users 131219  Aug 13 10:33  beav_1.40-13.tar.gz
-rw-r--r-- 1 juser users 6255    May 20 14:34  country.c
drwxr-xr-x 2 juser users 4096    Jul 17 20:00  cs335
-rwxr-xr-x 1 juser users 7108    Jun 16 13:05  dhry
-rw-r--r-- 1 juser users 11309   Aug 13 10:26  dhry.c
-rw-r--r-- 1 juser users 56      Jul  9 15:30  doit
drwxr-xr-x 6 juser users 4096    Feb 20 13:51  dw
drwxr-xr-x 3 juser users 4096    Jul  1 16:05  hough-stuff
```

You'll learn more about col umn 1 of this out put in Sec tion 2.17. You can ig nore col umn 2 for now; it's the num ber of hard links to the file and is ex plained in Sec tion 4.6.

In its sim plest form, `cp` copies files. For ex am ple, to copy _`file1`_ to _`file2`_ , en ter this:

- `$` **`cp`** _**`file1 file2`**_

You can also copy a file to an other di rec tory, keep ing the same file name in that di rec tory:

- `$` **`cp`** _**`file dir`**_

To copy more than one file to a di rec tory (folder) named _`dir`_ , try some thing like this ex am ple, which copies three files:

- `$` **`cp`** _**`file1 file2 file3 dir`**_

The `mv` (move) com mand works much like `cp` . In its sim plest form, it re names a file. For ex am ple, to re name _`file1`_ to _`file2`_ , en ter this:

```
$ mv file1file2
```

You can also use `mv` to move files to other di rec to ries in the same way as `cp` .

## _**2.3.4 touch**_

The `touch` com mand can cre ate a file. If the tar get file al ready ex ists, `touch` doesn't change the file, but it does up date the file's mod i fi ca tion time stamp. For ex am ple, to cre ate an empty file, en ter this:

- `$` **`touch`** _**`file`**_

Then run **`ls -l`** on that file. You should see out put like the fol low ing, where the date and time in di cate when you ran

`touch` :

```
$ ls -l file
-rw-r--r-- 1 juser users 0  May 21 18:32  file
```

To see a time stamp up date, wait at least a minute and then run the same `touch` com mand again. The time stamp re ‐ turned by `ls -l` will up date.

## _**2.3.5 rm**_

The `rm` com mand deletes (re moves) a file. Af ter you re move a file, it's usu ally gone from your sys tem and gen er ally can ‐ not be un deleted un less you re store it from a backup.