<!-- Source: 01_normalize/input/x200_102/cli.pdf | Cleaned: 2026-05-08 -->

6 RE DI RECT ION

In this les son we are go ing to un leash what may be the coolest fea ture of the com mand line. It's called I/O re di rect ion. The "I/O" stands for in put/out put, and with this fa cil ity you can re di rect the in put and out put of com mands

to and from files, as well as con nect mul ti ple com mands to gether into pow er ful com mand pipe lines. To show off this fa cil ity, we will in tro duce the fol low ing com mands:

**`cat`** Con cate nate files **`sort`** Sort lines of text

**`uniq`** Re port or omit re peated lines **`grep`** Print lines match ing a pat tern **`wc`** Print new line, word, and byte counts for each file **`head`** Out put the first part of a file **`tail`** Out put the last part of a file **`tee`** Read from stan dard in put and write to stan dard out put and files

## Stan dard In put, Out put, and Er ror

Many of the pro grams that we have used so far pro duce out put of some kind. This out put of ten con sists of two types.

The pro gram's re sults; that is, the data the pro gram is de signed to pro duce Sta tus and er ror mes sages that tell us how the pro gram is get ting along

If we look at a com mand like `ls` , we can see that it dis plays its re sults and its er ror mes sages on the screen.

Keep ing with the Unix theme of "ev ery thing is a file," pro grams such as `ls` ac tu ally send their re sults to a spe cial file called standard out put (of ten ex pressed as std out) and their sta tus mes sages to an other file called stan dard er ror (stderr). By de fault, both stan dard out put and stan dard er ror are linked to the screen and not saved into a disk file.

In ad di tion, many pro grams take in put from a fa cil ity called stan dard in put (stdin), which is, by de fault, at tached to the key board.

I/O re di rect ion al lows us to change where out put goes and where in put comes from. Nor mally, out put goes to the screen and input comes from the key board, but with I/O re di rect ion, we can change that.

## Redi rect ing Stan dard Out put

I/O re di rect ion al lows us to re de fine where stan dard out put goes. To re di rect stan dard out put to an other file in stead of the screen, we use the `>` re di rect ion op er a tor fol lowed by the name of the file. Why would we want to do this? It's of ten use ful to store the output of a com mand in a file. For ex am ple, we could tell the shell to send the out put of the `ls` com mand to the file ls-out put.txt in stead of the screen.

```
[me@lin uxbox ~]$ ls -l /usr/bin > ls-out put.txt
```

Here, we cre ated a long list ing of the /usr/bin di rec tory and sent the re sults to the file ls-out put.txt. Let's ex am ine the redi rected out put of the com mand, shown here:

```
[me@lin uxbox ~]$ ls -l ls-out put.txt
```

```
-rw-rw-r-- 1 me   me   167878 2018-02-01 15:07 ls-out put.txt
```

Good—a nice, large, text file. If we look at the file with `less` , we will see that the file ls-out put.txt does in deed con tain the re sults from our `ls` com mand.

## `[me@lin uxbox ~]$` **`less ls-out put.txt`**

Now, let's re peat our re di rect ion test, but this time with a twist. We'll change the name of the di rec tory to one that does not ex-

ist.

```
[me@lin uxbox ~]$ ls -l /bin/usr > ls-out put.txt
```

```
ls: can not ac cess /bin/usr: No such file or di rec tory
```

We re ceived an er ror mes sage. This makes sense since we spec i fied the nonex is tent di rec tory /bin/usr, but why was the er ror mes sage dis played on the screen rather than be ing redi rected to the file ls-out put.txt? The an swer is that the `ls` pro gram does not send its er ror mes sages to stan dard out put. In stead, like most well-writ ten Unix pro grams, it sends its er ror mes sages to stan dard er ror. Be cause we redi rected only stan dard out put and not stan dard er ror, the er ror mes sage was still sent to the screen. We'll see how to re di rect stan dard er ror in just a minute, but first let's look at what hap pened to our out put file.

```
[me@lin uxbox ~]$ ls -l ls-out put.txt
-rw-rw-r-- 1 me   me   0 2018-02-01 15:08 ls-out put.txt
```

`>` The file now has zero length! This is be cause when we re di rect out put with the re di rect ion op er a tor, the des ti na tion file is always rewrit ten from the be gin ning. Be cause our `ls` com mand gen er ated no re sults and only an er ror mes sage, the re di rect ion op er a- tion started to re write the file and then stopped be cause of the er ror, re sult ing in its trun ca tion. In fact, if we ever need to ac tu ally trun cate a file (or cre ate a new, empty file), we can use a trick like this:

```
[me@lin uxbox ~]$ > ls-out put.txt
```

Sim ply us ing the re di rect ion op er a tor with no com mand pre ced ing it will trun cate an ex ist ing file or cre ate a new, empty file.

So, how can we ap pend redi rected out put to a file in stead of over writ ing the file from the be gin ning? For that, we use the `>>` redi rect ion op er a tor, like so:

```
[me@lin uxbox ~]$ ls -l /usr/bin >> ls-out put.txt
```

`>>` Us ing the op er a tor will re sult in the out put be ing ap pended to the file. If the file does not al ready ex ist, it is cre ated just as `>` though the op er a tor had been used. Let's put it to the test.

```
[me@lin uxbox ~]$ ls -l /usr/bin >> ls-out put.txt
[me@lin uxbox ~]$ ls -l /usr/bin >> ls-out put.txt
[me@lin uxbox ~]$ ls -l /usr/bin >> ls-out put.txt
[me@lin uxbox ~]$ ls -l ls-out put.txt
-rw-rw-r-- 1 me   me   503634 2018-02-01 15:45 ls-out put.txt
```

We re peated the com mand three times, re sult ing in an out put file three times as large.

## Redi rect ing Stan dard Er ror

Redi rect ing stan dard er ror lacks the ease of a ded i cated re di rect ion op er a tor. To re di rect stan dard er ror, we must re fer to its file descrip tor. A pro gram can pro duce out put on any of sev eral num bered file streams. While we have re ferred to the first three of these file streams as stan dard in put, out put, and er ror, the shell ref er ences them in ter nally as file de scrip tors 0, 1, and 2, re spec tively. The shell pro vides a no ta tion for redi rect ing files us ing the file de scrip tor num ber. Be cause stan dard er ror is the same as file de scrip tor num ber 2, we can re di rect stan dard er ror with this no ta tion:

```
[me@lin uxbox ~]$ ls -l /bin/usr 2> ls-er ror.txt
```

The file de scrip tor 2 is placed im me di ately be fore the re di rect ion op er a tor to per form the re di rect ion of stan dard er ror to the file ls-er ror.txt.

## Redi rect ing Stan dard Out put and Stan dard Er ror to One File

There are cases in which we may want to cap ture all of the out put of a com mand to a sin gle file. To do this, we must re di rect both stan dard out put and stan dard er ror at the same time. There are two ways to do this. Shown here is the tra di tional way, which works with old ver sions of the shell:

```
[me@lin uxbox ~]$ ls -l /bin/usr > ls-out put.txt 2>&1
```

Us ing this method, we per form two redi rec tions. First we re di rect stan dard out put to the file ls-out put.txt, and then we re di rect file de scrip tor 2 (stan dard er ror) to file de scrip tor 1 (stan dard out put) us ing the no ta tion `2>&1` .

## NO TICE THAT THE OR DER OF THE REDI REC TIONS IS SIG NIF I CANT

The re di rect ion of stan dard er ror must al ways oc cur af ter redi rect ing stan dard out put or it doesn't work. The fol low ing ex ample redi rects stan dard er ror to the file ls-out put.txt:

```
>ls-out put.txt 2>&1
```

If the or der is changed to the fol low ing, then stan dard er ror is di rected to the screen:

```
2>&1 >ls-out put.txt
```

Re cent ver sions of `bash` pro vide a sec ond, more stream lined method for per form ing this com bined re di rect ion, shown here:

- `[me@lin uxbox ~]$` **`ls -l /bin/usr &> ls-out put.txt`**

In this ex am ple, we use the sin gle no ta tion `&>` to re di rect both stan dard out put and stan dard er ror to the file ls-out put.txt. You may also ap pend the stan dard out put and stan dard er ror streams to a sin gle file like so:

```
[me@lin uxbox ~]$ ls -l /bin/usr &>> ls-out put.txt
```

## Dis pos ing of Un wanted Out put

Some times "si lence is golden" and we don't want out put from a com mand; we just want to throw it away. This ap plies par tic u larly to er ror and sta tus mes sages. The sys tem pro vides a way to do this by redi rect ing out put to a spe cial file called /dev/null. This file is a sys tem de vice of ten re ferred to as a bit bucket, which ac cepts in put and does noth ing with it. To sup press er ror mes sages from a com mand, we do this:

```
[me@lin uxbox ~]$ ls -l /bin/usr 2> /dev/null
```

## Redi rect ing Stan dard In put

Up to now, we haven't en coun tered any com mands that make use of stan dard in put (ac tu ally we have, but we'll re veal that sur prise a lit tle bit later), so we need to in tro duce one.

## cat: Con cate nate Files

The `cat` com mand reads one or more files and copies them to stan dard out put like so:

```
catfile name
```

In most cases, you can think of `cat` as be ing anal o gous to the `TYPE` com mand in DOS. You can use it to dis play files with out paging. For ex am ple, the fol low ing will dis play the con tents of the file ls-out put.txt:

```
[me@lin uxbox ~]$ cat ls-out put.txt
```

`cat` is of ten used to dis play short text files. Be cause `cat` can ac cept more than one file as an ar gu ment, it can also be used to join files to gether. Sup pose we have down loaded a large file that has been split into mul ti ple parts (mul ti me dia files are of ten split this way on Usenet), and we want to join them back to gether. If the files were named as fol lows:

```
movie.mpeg.001 movie.mpeg.002 ... movie.mpeg.099
```

we could join them back to gether with this com mand:

```
cat movie.mpeg.0* > movie.mpeg
```

Be cause wild cards al ways ex pand in sorted or der, the ar gu ments will be ar ranged in the cor rect or der.

This is all well and good, but what does this have to do with stan dard in put? Noth ing yet, but let's try some thing else. What hap pens if we en ter **`cat`** with no ar gu ments?

```
[me@lin uxbox ~]$ cat
```

Noth ing hap pens; it just sits there like it's hung. It might seem that way, but it's re ally do ing ex actly what it's sup posed to do.

If `cat` is not given any ar gu ments, it reads from stan dard in put, and since stan dard in put is, by de fault, at tached to the key board, it's wait ing for us to type some thing! Try adding the fol low ing text and press ing EN TER:

```
[me@lin uxbox ~]$ cat
The quick brown fox jumped over the lazy dog.
```

Next, type CTRL-D (i.e., hold down the CTRL key and press D) to tell `cat` that it has reached end of file (EOF) on stan dard in put.

```
[me@lin uxbox ~]$ cat
The quick brown fox jumped over the lazy dog.
The quick brown fox jumped over the lazy dog.
```

In the ab sence of file name ar gu ments, `cat` copies stan dard in put to stan dard out put, so we see our line of text re peated. We can use this be hav ior to cre ate short text files. Let's say we wanted to cre ate a file called lazy_ dog.txt con tain ing the text in our ex am ple. We would do this:

```
[me@lin uxbox ~]$ cat > lazy_ dog.txt
The quick brown fox jumped over the lazy dog.
```

Type the com mand fol lowed by the text we want to place in the file. Re mem ber to type CTRL-D at the end. Us ing the com mand line, we have im ple mented the world's dumb est word pro ces sor! To see our re sults, we can use `cat` to copy the file to std out again.

```
[me@lin uxbox ~]$ cat lazy_ dog.txt
The quick brown fox jumped over the lazy dog.
```

Now that we know how `cat` ac cepts stan dard in put, in ad di tion to file name ar gu ments, let's try redi rect ing stan dard in put.

```
[me@lin uxbox ~]$ cat < lazy_ dog.txt
The quick brown fox jumped over the lazy dog.
```

Us ing the `<` re di rect ion op er a tor, we change the source of stan dard in put from the key board to the file lazy_ dog.txt. We see that the re sult is the same as pass ing a sin gle file name ar gu ment. This is not par tic u larly use ful com pared to pass ing a file name ar gument, but it serves to demon strate us ing a file as a source of stan dard in put. Other com mands make bet ter use of stan dard in put, as we will soon see.

Be fore we move on, check out the man page for `cat` be cause it has sev eral in ter est ing op tions.

## Pipe lines

The ca pa bil ity of com mands to read data from stan dard in put and send to stan dard out put is uti lized by a shell fea ture called pipelines. Us ing the pipe op er a tor `|` , the stan dard out put of one com mand can be piped into the stan dard in put of an other.

```
com mand1 | com mand2
```

To fully demon strate this, we are go ing to need some com mands. Re mem ber how we said there was one we al ready knew that ac cepts stan dard in put? It's `less` . We can use `less` to dis play, page by page, the out put of any com mand that sends its re sults to standard out put.

```
[me@lin uxbox ~]$ ls -l /usr/bin | less
```

This is ex tremely handy! Us ing this tech nique, we can con ve niently ex am ine the out put of any com mand that pro duces stan dard out put.

## Fil ters

Pipe lines are of ten used to per form com plex op er a tions on data. It is pos si ble to put sev eral com mands to gether into a pipe line. Fre quently, the com mands used this way are re ferred to as fil ters. Fil ters take in put, change it some how, and then out put it. The first one we will try is `sort` . Imag ine we wanted to make a com bined list of all the ex e cutable pro grams in /bin and /usr/bin, put them in sorted or der, and view the re sult ing list.

```
[me@lin uxbox ~]$ ls /bin /usr/bin | sort | less
```

Be cause we spec i fied two di rec to ries (/bin and /usr/bin), the out put of `ls` would have con sisted of two sorted lists, one for each direc tory. By in clud ing `sort` in our pipe line, we changed the data to pro duce a sin gle, sorted list.

## THE DIF FER ENCE BE TWEEN > AND |

At first glance, it may be hard to un der stand the re di rect ion per formed by the pipe line op er a tor `|` ver sus the re di rect ion op er a- tor `>` . Sim ply put, the re di rect ion op er a tor con nects a com mand with a file, while the pipe line op er a tor con nects the out put of one com mand with the in put of a sec ond com mand.

```
com mand1 > file1
com mand1 | com mand2
```

```
com mand1 > com mand2
```

Here is an ac tual ex am ple sub mit ted by a reader who was ad min is ter ing a Linux-based server ap pli ance. As the su pe ruser, he did this:

```
# cd /usr/bin
# ls > less
```

The first com mand put him in the di rec tory where most pro grams are stored, and the sec ond com mand told the shell to over write the file less with the out put of the `ls` com mand. Since the /usr/bin di rec tory al ready con tained a file named less (the `less` pro gram), the sec ond com mand over wrote the less pro gram file with the text from `ls` , thus de stroy ing the `less` pro gram on his sys tem.

The les son here is that the re di rect ion op er a tor silently cre ates or over writes files, so you need to treat it with a lot of respect.

## uniq: Re port or Omit Re peated Lines

The `uniq` com mand is of ten used in con junc tion with `sort` . `uniq` ac cepts a sorted list of data from ei ther stan dard in put or a sin gle filename ar gu ment (see the `uniq` man page for de tails) and, by de fault, re moves any du pli cates from the list. So, to make sure our list has no du pli cates (that is, any pro grams of the same name that ap pear in both the /bin and /usr/bin di rec to ries), we will add `uniq` to our pipe line.

```
[me@lin uxbox ~]$ ls /bin /usr/bin | sort | uniq | less
```

In this ex am ple, we use `uniq` to re move any du pli cates from the out put of the `sort` com mand. If we want to see the list of du plicates in stead, we add the `-d` op tion to `uniq` like so:

```
[me@lin uxbox ~]$ ls /bin /usr/bin | sort | uniq -d | less
```

## wc: Print Line, Word, and Byte Counts

The `wc` (word count) com mand is used to dis play the num ber of lines, words, and bytes con tained in files. Here's an ex am ple:

```
[me@lin uxbox ~]$ wc ls-out put.txt
 7902  64566 503634 ls-out put.txt
```

In this case, it prints out three num bers: lines, words, and bytes con tained in ls-out put.txt. Like our pre vi ous com mands, if ex e- cuted with out com mand line ar gu ments, `wc` ac cepts stan dard in put. The `-l` op tion lim its its out put to re port only lines. Adding it to a pipe line is a handy way to count things. To see the num ber of items we have in our sorted list, we can do this:

```
[me@lin uxbox ~]$ ls /bin /usr/bin | sort | uniq | wc -l

```

## grep: Print Lines Match ing a Pat tern

`grep` is a pow er ful pro gram used to find text pat terns within files. It's used like this:

```
greppat ternfile name
```

When `grep` en coun ters a "pat tern" in the file, it prints out the lines con tain ing it. The pat terns that `grep` can match can be very com plex, but for now we will con cen trate on sim ple text matches. We'll cover the ad vanced pat terns, called reg u lar ex pres sions, in Chap ter 19.

Sup pose we wanted to find all the files in our list of pro grams that had the word zip em bed ded in the name. Such a search might give us an idea of some of the pro grams on our sys tem that had some thing to do with file com pres sion. We would do this:

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

There are a cou ple of handy op tions for `grep` .

- `-i` , which causes `grep` to ig nore case when per form ing the search (nor mally searches are case sen si tive)

`-v` , which tells `grep` to print only those lines that do not match the pat tern

## head/tail: Print First/Last Part of Files

Some times you don't want all the out put from a com mand. You might want only the first few lines or the last few lines. The `head` com mand prints the first 10 lines of a file, and the `tail` com mand prints the last 10 lines. By de fault, both com mands print 10 lines of text, but this can be ad justed with the `-n` op tion.

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

These can be used in pipe lines as well:

```
[me@lin uxbox ~]$ ls /usr/bin | tail -n 5
znew
zonetab2pot.py
zonetab2pot.pyc
zonetab2pot.pyo
zsoe lim
```

`tail` has an op tion that al lows you to view files in real time. This is use ful for watch ing the progress of log files as they are be ing writ ten. In the fol low ing ex am ple, we will look at the mes sages file in /var/log (or the /var/log/sys log file if mes sages is miss ing). Su peruser priv i leges are re quired to do this on some Linux dis tri bu tions be cause the /var/log/mes sages file might con tain se cu rity in forma tion.

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

Us ing the `-f` op tion, `tail` con tin ues to mon i tor the file, and when new lines are ap pended, they im me di ately ap pear on the display. This con tin ues un til you type CTRL-C.

## tee: Read from Stdin and Out put to Std out and Files

In keep ing with our plumb ing metaphor, Linux pro vides a com mand called `tee` that cre ates a "tee" fit ting on our pipe. The `tee` program reads stan dard in put and copies it to both stan dard out put (al low ing the data to con tinue down the pipe line) and to one or more files. This is use ful for cap tur ing a pipe line's con tents at an in ter me di ate stage of pro cess ing. Here we re peat one of our earlier ex am ples, this time in clud ing `tee` to cap ture the en tire di rec tory list ing to the file ls.txt be fore `grep` fil ters the pipe line's con tents:

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

As al ways, check out the doc u men ta tion of each of the com mands we have cov ered in this chap ter. We have seen only their most ba sic us age. They all have a num ber of in ter est ing op tions. As we gain Linux ex pe ri ence, we will see that the re di rect ion fea ture of

the com mand line is ex tremely use ful for solv ing spe cial ized prob lems. There are many com mands that make use of stan dard in put and out put, and al most all com mand line pro grams use stan dard er ror to dis play their in for ma tive mes sages.