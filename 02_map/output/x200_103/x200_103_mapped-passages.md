# Mapped Passages: x200_103

**Objective:** 1.3 Use grep and regular expressions to analyze text

**Run date:** 2026-05-08

---

<!-- Source: 01_normalize/output/x200_103/0toSAvol1_clean.md -->

## Just grepping Around

---

<!-- Source: 01_normalize/output/x200_103/0toSAvol1_clean.md -->

The **`grep`** command is used to select lines that match a specified pattern from a stream of data. **`grep`** is one of the most commonly used filter utilities and can be used in some very creative and interesting ways. The **`grep`** command is one of the few that can correctly be called a filter because it does filter out all the lines of the data stream that you do not want; it leaves only the lines that you do want in the remaining data stream.

---

<!-- Source: 01_normalize/output/x200_103/0toSAvol1_clean.md -->

## **EXPERIMENT 9-16: INTRODUCING GREP**

---

<!-- Source: 01_normalize/output/x200_103/0toSAvol1_clean.md -->

Considering that there are so many passwords, it is very likely that some character strings in them are the same. Use the grep command to locate some short, randomly selected strings from the last ten passwords on the screen. I saw the words "see" and "loop" in one of those ten passwords, so my command looked like this:

---

<!-- Source: 01_normalize/output/x200_103/0toSAvol1_clean.md -->

```
grep see random.txt
```

---

<!-- Source: 01_normalize/output/x200_103/0toSAvol1_clean.md -->

Use the grep filter to locate all of the lines in the output from dmesg with CPU in them:

---

<!-- Source: 01_normalize/output/x200_103/0toSAvol1_clean.md -->

```
dmesg | grep cpu
```

---

<!-- Source: 01_normalize/output/x200_103/0toSAvol1_clean.md -->

```
ls -la | grep ^d
```

---

<!-- Source: 01_normalize/output/x200_103/0toSAvol1_clean.md -->

This works because each directory has a "d" as the first character in a long listing. The caret ( ^ ) is used by grep and other tools to anchor the text being searched to the beginning of the line.

---

<!-- Source: 01_normalize/output/x200_103/0toSAvol1_clean.md -->

```
ls -la | grep -v ^d
```

---

<!-- Source: 01_normalize/output/x200_103/0toSAvol1_clean.md -->

## Meta-characters

---

<!-- Source: 01_normalize/output/x200_103/0toSAvol1_clean.md -->

As we progress further through this course, we will explore the meta-characters we already know in more detail, and we will learn about the few we do not already know.

---

<!-- Source: 01_normalize/output/x200_103/0toSAvol1_clean.md -->

## Using grep

---

<!-- Source: 01_normalize/output/x200_103/0toSAvol1_clean.md -->

There is a tool, `grep` , that can be used to extract and print to STDOUT all of the lines from a data stream based on matching patterns. Those patterns can range from simple text patterns to very complex regular expressions (regex). Written by Ken Thompson3 and first released in 1974, the `grep` utility is provided by the GNU Project4 and is installed by default on every version of Unix and Linux distribution I have ever used.

---

<!-- Source: 01_normalize/output/x200_103/0toSAvol1_clean.md -->

In terms of globbing characters, which grep does not understand, the default search pattern for the `grep` command is *PATTERN*. There is an implicit wildcard match before and after the search pattern. Thus, you can assume that any pattern you specify will be found no matter where it exists in the lines being scanned. It could be at the

---

<!-- Source: 01_normalize/output/x200_103/0toSAvol1_clean.md -->

beginning, anywhere in the middle, or at the end. Thus, it is not necessary to explicitly state that there are characters in the string before and/or after the string for which we are searching.

---

<!-- Source: 01_normalize/output/x200_103/0toSAvol1_clean.md -->

## **EXPERIMENT 15-10: USING GREP**

---

<!-- Source: 01_normalize/output/x200_103/0toSAvol1_clean.md -->

One of the most common tasks I do that requires the use of the grep utility is scanning through log files to find information pertaining to specific things. For example, I may need to determine information about how the operating system sees the network interface cards (NICs) starting with their BIOS names,5 ethX. Information about the NICs installed in the host can be found using the `dmesg` command as well as in the messages log files in /var/log.

---

<!-- Source: 01_normalize/output/x200_103/0toSAvol1_clean.md -->

Searching through pages of data, even with a good search facility, is easier than eyeballing it, but not as easy as using `grep` . The -i option tells grep to ignore case and display the "eth" string regardless of the case of its letters. It will find the strings eth, ETH, Eth, eTh, and so on, which are all different in Linux:

---

<!-- Source: 01_normalize/output/x200_103/0toSAvol1_clean.md -->

```
[root@studentvm1 ~]# dmesg | grep -i eth
```

---

<!-- Source: 01_normalize/output/x200_103/0toSAvol1_clean.md -->

In this first example of usage, `grep` takes the incoming data stream using STDIN and then sends the output to STDOUT. The grep utility can also use a file as the source of the data stream. We can see that in this next example in which we grep through the messages log files for information about our NICs:

---

<!-- Source: 01_normalize/output/x200_103/0toSAvol1_clean.md -->

```
[root@studentvm1 ~]$ cd /var/log ; grep -i eth messages*
<snip>
messages-20181111:Nov  6 09:27:36 studentvm1 dbus-daemon[830]: [system] Rejected send mess
messages-20181111:Nov  6 09:27:36 studentvm1 pulseaudio[1738]: E: [pulseaudio] bluez5-util
messages-20181118:Nov 16 07:41:00 studentvm1 kernel: e1000 0000:00:03.0 eth0: (PCI:33MHz:3
messages-20181118:Nov 16 07:41:00 studentvm1 kernel: e1000 0000:00:03.0 eth0: Intel(R) PRO
messages-20181118:Nov 16 07:41:00 studentvm1 kernel: e1000 0000:00:08.0 eth1: (PCI:33MHz:3
messages-20181118:Nov 16 07:41:00 studentvm1 kernel: e1000 0000:00:08.0 eth1: Intel(R) PRO
<SNIP>
```

---

<!-- Source: 01_normalize/output/x200_103/0toSAvol1_clean.md -->

The first part of each line in our output data stream is the name of the file in which the matched lines were found. If you do a little exploration of the current messages file, which is named just that with no appended date, you may or may not find any lines matching our search pattern. I did not with my VM, so using the file glob to create the pattern "messages*" searches all of the files starting with messages. This file glob matching is performed by the shell and not by the `grep` tool.

---

<!-- Source: 01_normalize/output/x200_103/0toSAvol1_clean.md -->

You will notice also that, on this first try, we found more than we wanted. Some lines have the "eth" string in them that was found as part of the word "method." So let's be a little more explicit and use a set as part of our search pattern:

---

<!-- Source: 01_normalize/output/x200_103/0toSAvol1_clean.md -->

```
[root@studentvm1 log]# grep -i eth[0-9] messages*
```

---

<!-- Source: 01_normalize/output/x200_103/0toSAvol1_clean.md -->

**Tip** Each expression is additive. That is, the eth[0-9] expression finds all messages that contain that phrase, and the enp0 expression finds all messages that contain that one. So lines containing either one or the other or both expressions are displayed. Therefore, this next command will produce a long data stream.

---

<!-- Source: 01_normalize/output/x200_103/0toSAvol1_clean.md -->

```
[root@studentvm1 log]# grep -i -e eth[0-9] -e enp0 messages*
```

---

<!-- Source: 01_normalize/output/x200_103/0toSAvol1_clean.md -->

That does work, but there is also an extension that allows us to search using extended regular expressions. 7 The **`grep`** patterns we have been using so far are basic regular expressions (BRE). To get more complex, we can use extended regular expressions (ERE). To do this we can use egrep:

---

<!-- Source: 01_normalize/output/x200_103/0toSAvol1_clean.md -->

```
[root@studentvm1 log]# egrep "eth[0-9] | enp0" messages*
```

---

<!-- Source: 01_normalize/output/x200_103/0toSAvol1_clean.md -->

Now make /etc the PWD. Sometimes I have previously needed to list all of the configuration files in the /etc directory. These files typically end with a .conf or .cnf extension or with rc. To do this we need an anchor to specify that the search string is at the end of the string being searched. We use the dollar sign ($) for that. The syntax of the search string in the following command finds all the configuration files with the listed endings. The -R option for the **`ll`** or **`ls`** command causes the command to recurse into all of the subdirectories:

---

<!-- Source: 01_normalize/output/x200_103/0toSAvol1_clean.md -->

```
[root@studentvm1 etc]# ls -aR | grep -E "conf$|cnf$|rc$"
```

---

<!-- Source: 01_normalize/output/x200_103/0toSAvol1_clean.md -->

Use word count to display the number of files selected and then use the equivalent egrep command and see that it selects the same number of files.

---

<!-- Source: 01_normalize/output/x200_103/0toSAvol1_clean.md -->

We can also use the caret (^) to anchor the beginning of the string. Suppose that we want to locate all files in /etc that begin with kde because they are used in the configuration of the KDE desktop:

---

<!-- Source: 01_normalize/output/x200_103/0toSAvol1_clean.md -->

```
[root@studentvm1 etc]# ls -R | grep -E "^kde"
kde
```

---

<!-- Source: 01_normalize/output/x200_103/0toSAvol1_clean.md -->

One of the advanced features of **`grep`** is the ability to read the search patterns from a file containing one or more patterns. This is very useful if the same complex searches must be performed on a regular basis.

---

<!-- Source: 01_normalize/output/x200_103/0toSAvol1_clean.md -->

The `ls` command and its aliases such as `ll` are designed to list all of the files in a directory. Special pattern characters and the grep command can be used to narrow down the list of files sent to STDOUT. But there is still something missing. There is a bit of a problem with the command `ls -R | grep -E "^kde"` that we used in Experiment 15-10. Some of the files it found were in subdirectories of /etc/, but the ls command does not display the names of the subdirectories in which those files are stored.

---

<!-- Source: 01_normalize/output/x200_103/CertGuide_clean.md -->

|`[root@localhost ~]#`|<br>**`ps aux | wc`**|
|---|---|
|`90       1045`|`7583`|

---

<!-- Source: 01_normalize/output/x200_103/CertGuide_clean.md -->

Work ing with text files is an im por tant skill for a Linux ad min is tra tor. You must know not only how to cre ate and mod ify ex ist ing text files, but also how to find the text file that con tains spe cific text.

---

<!-- Source: 01_normalize/output/x200_103/CertGuide_clean.md -->

It will be clear some times which spe cific text you are look ing for. Other times, it might not. For ex am ple, are you look ing for color or colour? Both spellings might give a match. This is just one ex am ple of why us ing flex i ble pat terns while look ing for text can prove use ful. In Linux these flex i ble pat terns are known as reg u lar ex pres sions, of ten also re ferred to as regex.

---

<!-- Source: 01_normalize/output/x200_103/CertGuide_clean.md -->

To un der stand reg u lar ex pres sions a bit bet ter, let's take a look at a text file ex am ple, shown in Ex am ple 4-4. This file con tains the last six lines from the /etc/passwd file. (This file is used for stor ing Linux ac counts; see Chap ter 6, "User and Group Man age ment," for more de tails.)

---

<!-- Source: 01_normalize/output/x200_103/CertGuide_clean.md -->

||`[root@localhost ~]#`**`tail -n 6 /etc/passwd`**|`[root@localhost ~]#`**`tail -n 6 /etc/passwd`**|
|---|---|---|
||`anna:x:1000:1000::/home/anna:/bin/bash`||
||`rihanna:x:1001:1001::/home/rihanna:/bin/bash`||
||`annabel:x:1002:1002::/home/annabel:/bin/bash`||
||`anand:x:1003:1003::/home/anand:/bin/bash`||
||`joanna:x:1004:1004::/home/joanna:/bin/bash`||
||`joana:x:1005:1005::/home/joana:/bin/bash`||
|Now sup pose that you are look ing for the user anna. In that case, you could use the gen eral reg u lar ex pres sion parsergrepto look for that spe cifc string in thefle|||
|/etc/passwd by us ing the com mandgrep anna /etc/passwd.<br>Ex am ple 4-5 shows the re sults of that com mand, and as you can see, way too many re sults are shown.|||

---

<!-- Source: 01_normalize/output/x200_103/CertGuide_clean.md -->

```
[root@localhost ~]# grep anna /etc/passwd
anna:x:1000:1000::/home/anna:/bin/bash
rihanna:x:1001:1001::/home/rihanna:/bin/bash
annabel:x:1002:1002::/home/annabel:/bin/bash
joanna:x:1004:1004::/home/joanna:/bin/bash
```

---

<!-- Source: 01_normalize/output/x200_103/CertGuide_clean.md -->

A reg u lar ex pres sion is a search pat tern that al lows you to look for spe cific text in an ad vanced and flex i ble way. Us ing Line An chors In Ex am ple 4-5, sup pose that you wanted to spec ify that you are look ing for lines that start with the text anna. The type of reg u lar ex pres sion that spec i fies where in a line of out put the re sult is ex pected is known as a line an chor. To show only lines that start with the text you are look ing for, you can use the reg u lar ex pres sion ^ (in this case, to in di cate that you are look ing only for lines where anna is at the be gin ning of the line; see Ex am ple 4-6). Ex am ple 4-6 Look ing for Lines Start ing with a Spe cific Pat tern

---

<!-- Source: 01_normalize/output/x200_103/CertGuide_clean.md -->

|Click here to view code im age|
|---|
|`[root@localhost ~]#`<br>**`grep ^anna /etc/passwd`**|
|`anna:x:1000:1000::/home/anna:/bin/bash`|
|`annabel:x:1002:1002::/home/annabel:/bin/bash`|

---

<!-- Source: 01_normalize/output/x200_103/CertGuide_clean.md -->

An other reg u lar ex pres sion that re lates to the po si tion of spe cific text in a spe cific line is $, which states that the line ends with some text. For in stance, the com ‐ mand grep ash$ /etc/passwd shows all lines in the /etc/passwd file that end with the text ash. This com mand shows all ac counts that have a shell and are able to log in (see Chap ter 6 for more de tails).

---

<!-- Source: 01_normalize/output/x200_103/CertGuide_clean.md -->

Us ing Es cap ing in Reg u lar Ex pres sions

---

<!-- Source: 01_normalize/output/x200_103/CertGuide_clean.md -->

Al though not manda tory, when you're us ing reg u lar ex pres sions, it is a good idea to use es cap ing to pre vent reg u lar ex pres sions from be ing in ter preted by the ‐ shell. When a com mand line is en tered, the Bash shell parses the com mand line, look ing for any spe cial char ac ters like *, $, and ?. It will next in ter pret these char ac ters. The point is that reg u lar ex pres sions use some of these char ac ters as well, and to make sure the Bash shell doesn't in ter pret them, you should use es cap ing.

---

<!-- Source: 01_normalize/output/x200_103/CertGuide_clean.md -->

In many cases, it is not re ally nec es sary to use es cap ing; in some cases, the reg u lar ex pres sion fails with out es cap ing. To pre vent this from ever hap pen ing, it is a good idea to put the reg u lar ex pres sion be tween quotes. So, in stead of typ ing grep ^anna /etc/passwd, it is bet ter to use grep '^anna' /etc/passwd, even if in this case both ex am ples work.

---

<!-- Source: 01_normalize/output/x200_103/CertGuide_clean.md -->

In some cases, you might know which text you are look ing for, but you might not know how the spe cific text is writ ten. Or you might just want to use one reg u lar ex pres sion to match diff er ent pat terns. In those cases, wild cards and mul ti pli ers come in handy.

---

<!-- Source: 01_normalize/output/x200_103/CertGuide_clean.md -->

To start with, there is the dot (.) reg u lar ex pres sion. This is used as a wild card char ac ter to look for one spe cific char ac ter. So, the reg u lar ex pres sion r.t would match the strings rat, rot, and rut.

---

<!-- Source: 01_normalize/output/x200_103/CertGuide_clean.md -->

In some cases, you might want to be more spe cific about the char ac ters you are look ing for. If that is the case, you can spec ify a range of char ac ters that you are ' look ing for. For in stance, the reg u lar ex pres sion r[aou]t matches the strings rat, rot, and rut but it wouldn t match rit and ret.

---

<!-- Source: 01_normalize/output/x200_103/CertGuide_clean.md -->

An other use ful reg u lar ex pres sion is the mul ti plier *. This matches zero or more of the pre vi ous char ac ter. That does not seem to be very use ful, but in deed it is, as you will see in the ex am ples at the end of this sec tion.

---

<!-- Source: 01_normalize/output/x200_103/CertGuide_clean.md -->

If you know ex actly how many of the pre vi ous char ac ter you are look ing for, you can spec ify a num ber also, as in re\{2\}d, which would match reed, but not red. The last reg u lar ex pres sion that is use ful to know about is ?, which matches zero or one of the pre vi ous char ac ter. Ta ble 4-3 pro vides an over view of the most im ‐ por tant reg u lar ex pres sions.

---

<!-- Source: 01_normalize/output/x200_103/CertGuide_clean.md -->

Us ing Ex tended Reg u lar Ex pres sions

---

<!-- Source: 01_normalize/output/x200_103/CertGuide_clean.md -->

What makes reg u lar ex pres sions some times a bit hard to un der stand is the fact that there are diff er ent sets of reg u lar ex pres sions. The base reg u lar ex pres sions as dis cussed so far are sup ported by tools like grep. There is also a set of ex tended reg u lar ex pres sions, which is not sup ported by de fault. When used with grep, you'll have to add the -E op tion to in di cate it is an ex tended reg u lar ex pres sion. The + can be used to in di cate that a char ac ter should oc cur one or more times, and the ? is used to in di cate that a char ac ter should oc cur zero or one times. When used in grep, don't for get to use grep -E to en sure that these are in ter preted as ex ‐ tended reg u lar ex pres sions!

---

<!-- Source: 01_normalize/output/x200_103/CertGuide_clean.md -->

Ta ble 4-3 Most Sig nifi cant Reg u lar Ex pres sions

---

<!-- Source: 01_normalize/output/x200_103/CertGuide_clean.md -->

|Reg u lar Ex pres sion|Use|
|---|---|
|^text|Matches line that starts with spec ifed text.|
|text$|Matches line that ends with spec ifed text.|
|.|Wild card. (Matches any sin gle char ac ter.)|
|[abc]|Matchesa, b, orc.|
|?|Ex tended reg u lar ex pres sion that matches zero or one of the pre ced ing char ac ter.|
|+|Ex tended reg u lar ex pres sion that matches one or more of the pre ced ing char ac ter.|
|*|Matches zero to an infnite num ber of the pre vi ous char ac ter.|
|\{2\}|Matches ex actly two of the pre vi ous char ac ter.|

---

<!-- Source: 01_normalize/output/x200_103/CertGuide_clean.md -->

Reg u lar Ex pres sion Use

---

<!-- Source: 01_normalize/output/x200_103/CertGuide_clean.md -->

Matches a min i mum of one and a max i mum of three of the pre vi ous char ac ter.

---

<!-- Source: 01_normalize/output/x200_103/CertGuide_clean.md -->

|||
|---|---|
|\{1,3\}|Matches a min i mum of one and a max i mum of three of the pre vi ous char ac ter.|
|colou?r|Matches zero or one of the pre vi ous char ac ter. This makes the pre vi ous char ac ter op tional, which in this ex am ple would match bothcolorandcolour.|
|(…)|Used to group mul ti ple char ac ters so that the reg u lar ex pres sion can be ap plied to the group.|

---

<!-- Source: 01_normalize/output/x200_103/CertGuide_clean.md -->

Let's take a look at an ex am ple of a reg u lar ex pres sion that comes from the man page se m an age-fcon text and re lates to man ag ing SELinux (see Chap ter 22, "Man ag ‐ ing SELinux"). The sam ple line con tains the fol low ing reg u lar ex pres sion:

---

<!-- Source: 01_normalize/output/x200_103/CertGuide_clean.md -->

In this reg u lar ex pres sion, the text /web is re ferred to. This text string can be fol lowed by the reg u lar ex pres sion (/.*)?. To un der stand the reg u lar ex pres sion, start with the ?, which refers to the part be tween braces and in di cates that the part be tween braces may oc cur zero times or one time. Within the braces, the pat tern starts with a slash, which is just a slash, fol lowed by zero or more char ac ters. So this means that just the di rec tory name gives a match, but also the di rec tory name fol lowed by just a slash, or a slash that is fol lowed by a file name.

---

<!-- Source: 01_normalize/output/x200_103/CertGuide_clean.md -->

What makes reg u lar ex pres sions diffi cult is that there is not just one set of reg u lar ex pres sions; there are also ex tended reg u lar ex pres sions. And to make the con ‐ cept more com plex, the ex tended reg u lar ex pres sions need spe cific com mands. The well-known com mand grep (cov ered next) by de fault deals with base reg u lar ex pres sions. If you want to use ex tended reg u lar ex pres sions, you need grep -E or egrep.

---

<!-- Source: 01_normalize/output/x200_103/CertGuide_clean.md -->

Two com mon ex tended reg u lar ex pres sions are + and ?. The + will look for a pat tern where the pre ced ing char ac ter oc curs one or more times, and the ? looks for a pat tern where the pre ced ing char ac ter does not oc cur or oc curs one time. Use the fol low ing pro ce dure to find out how these ex tended reg u lar ex pres sions can be con fus ing:

---

<!-- Source: 01_normalize/output/x200_103/CertGuide_clean.md -->

Step 2. Use grep 'b.*t' regex.txt to see any line that starts with a b and ends with a t.

---

<!-- Source: 01_normalize/output/x200_103/CertGuide_clean.md -->

Step 3. Use grep 'b.+t' regex.txt. You might ex pect to see only lines that have at least three char ac ters, but you don't, be cause you are us ing an ex tended reg u lar ex pres sion, and with out us ing any ad di tional op tions, grep doesn't rec og nize the ex tended reg u lar ex pres sion.

---

<!-- Source: 01_normalize/output/x200_103/CertGuide_clean.md -->

Step 4. Use grep -E 'b.+t' regex.txt. Now you see that the ex tended reg u lar ex pres sion does work as ex pected.

---

<!-- Source: 01_normalize/output/x200_103/CertGuide_clean.md -->

## Us ing grep to An a lyze Text

---

<!-- Source: 01_normalize/output/x200_103/CertGuide_clean.md -->

The ul ti mate util ity to work with reg u lar ex pres sions is grep, which stands for "gen eral reg u lar ex pres sion parser." Quite a few ex am ples that you have seen al ‐ ready were based on the grep com mand. The grep com mand has a cou ple of use ful op tions to make it even more effi cient. Ta ble 4-4 de scribes some of the most use ful op tions.

---

<!-- Source: 01_normalize/output/x200_103/CertGuide_clean.md -->

|Op tion|Use|
|---|---|
|-i|Matches up per- and low er case let ters (i.e., not case sen si tive).|
|-v|Shows only lines that donotcon tain the reg u lar ex pres sion.|

---

<!-- Source: 01_normalize/output/x200_103/CertGuide_clean.md -->

|Op tion|Use|
|---|---|
|-r|Searchesfles in the cur rent di rec tory and all sub di rec to ries.|
|-e|Searches for lines match ing more than one reg u lar ex pres sion. Use-ebe fore each reg u lar ex pres sion you want to use.|
|-E|In ter prets the search pat tern as an ex tended reg u lar ex pres sion.|
|-A <num ber>|Shows <num ber> of lines af ter the match ing reg u lar ex pres sion.|
|-B <num ber>|Shows <num ber> of lines be fore the match ing reg u lar ex pres sion.|

---

<!-- Source: 01_normalize/output/x200_103/CertGuide_clean.md -->

1. Type grep '^#'/etc/ser vices. This shows that the file /etc/ser vices con tains a num ber of lines that start with the com ment sign, #.

---

<!-- Source: 01_normalize/output/x200_103/CertGuide_clean.md -->

2. To view the con fig u ra tion lines that re ally mat ter, type grep -v '^#'/etc/ser vices. This shows only lines that do not start with a #.

---

<!-- Source: 01_normalize/output/x200_103/CertGuide_clean.md -->

3. Type grep -v '^#' /etc/ser vices -B 5. This shows lines that do not start with a # sign but also the five lines that are di rectly be fore each of those lines, which is use ful be cause in the pre ced ing lines you'll typ i cally find com ments on how to use the spe cific pa ram e ters. How ever, you'll also see that many blank lines are dis played.

---

<!-- Source: 01_normalize/output/x200_103/CertGuide_clean.md -->

4. Type grep -v -e '^#' -e '^$'/etc/ser vices. This ex cludes all blank lines and lines that start with #.

---

<!-- Source: 01_normalize/output/x200_103/CertGuide_clean.md -->

The grep util ity is a pow er ful util ity that al lows you to work with reg u lar ex pres sions. It is not the only util ity, though. Some even more pow er ful util i ties ex ist, like awk and sed, both of which are ex tremely rich and merit a book by them selves. The util i ties were de vel oped in the time that com put ers did not com monly have screens at tached, and for that rea son they do a good job of treat ing text files in a scripted way.

---

<!-- Source: 01_normalize/output/x200_103/CertGuide_clean.md -->

This com mand searches the /etc/passwd file for the text user and will print the fourth field of any match ing line.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

Given one or more patterns, `grep` searches input files for matches to the patterns. When it finds a match in a line, it copies the line to standard output (by default), or produces whatever other sort of output you have requested with options.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

Though `grep` expects to do the matching on text, it has no limits on input line length other than available memory, and it can match arbitrary characters within a line. If the final byte of an input file is not a newline, `grep` silently supplies one. Since newline is also a separator for the list of patterns, there is no way to match newline characters in a text.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

## `grep [` _`option`_ `]... [` _`patterns`_ `] [` _`file`_ `]...`

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

There can be zero or more _option_ arguments, and zero or more _file_ arguments. The _patterns_ argument contains one or more patterns separated by newlines, and is omitted when patterns are given via the ' `-e` _`patterns`_ ' or ' `-f` _`file`_ ' options. Typically _patterns_ should be quoted when `grep` is used in a shell command.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

`grep` comes with a rich set of options: some from POSIX and some being GNU extensions. Long option names are always a GNU extension, even for options that are from POSIX specifications. Options that are specified by POSIX, under their short names, are explicitly marked as such to facilitate POSIX-portable programming. A few option names are provided for compatibility with older or more exotic implementations.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

Several additional options control which variant of the `grep` matching engine is used. See Section 2.4 [grep Programs], page 13.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

Use _patterns_ as one or more patterns; newlines within _patterns_ separate each pattern from the next. If this option is used multiple times or is combined with the `-f` ( `--file` ) option, search for all patterns given. Typically _patterns_ should be quoted when `grep` is used in a shell command. ( `-e` is specified by POSIX.)

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

Obtain patterns from _file_ , one per line. If this option is used multiple times or is combined with the `-e` ( `--regexp` ) option, search for all patterns given. ' `-` When _file_ is ', read patterns from standard input. The empty file contains zero patterns, and therefore matches nothing. ( `-f` is specified by POSIX.)

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

Ignore case distinctions in patterns and input data, so that characters that differ only in case match each other. Although this is straightforward when

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

Invert the sense of matching, to select non-matching lines. ( `-v` is specified by POSIX.)

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

Select only those lines containing matches that form whole words. The test is that the matching substring must either be at the beginning of the line, or preceded by a non-word constituent character. Similarly, it must be either at the end of the line or followed by a non-word constituent character. Word constituent characters are letters, digits, and the underscore. This option has no effect if `-x` is also specified.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

Because the `-w` option can match a substring that does not begin and end with word constituents, it differs from surrounding a regular expression with ' `\<` ' and ' `\>` '. For example, although ' `grep -w @` ' matches a line containing only ' `@` ', ' `grep '\<@\>'` ' cannot match any line because ' `@` ' is not a word constituent. See Section 3.3 [Special Backslash Expressions], page 17.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

```
--line-regexp
```

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

Select only those matches that exactly match the whole line. For regular expression patterns, this is like parenthesizing each pattern and then surrounding it with ' `^` ' and ' `$` '. ( `-x` is specified by POSIX.)

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

`--count` Suppress normal output; instead print a count of matching lines for each input file. With the `-v` ( `--invert-match` ) option, count non-matching lines. ( `-c` is specified by POSIX.)

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

Surround matched non-empty strings, matching lines, context lines, file names, line numbers, byte offsets, and separators (for fields and groups of context lines) with escape sequences to display them in color on the terminal. The colors are defined by the environment variable `GREP_COLORS` and default to ' `ms=01;31:mc=01;31:sl=:cx=:fn=35:ln=32:bn=32:se=36` ' for bold red matched text, magenta file names, green line numbers, green byte offsets, cyan separators, and default terminal colors otherwise. See Section 2.2 [Environment Variables], page 10.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

## `--files-without-match`

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

## `--files-with-matches`

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

Suppress normal output; instead print the name of each input file from which output would normally have been printed. Scanning each input file stops upon first match. ( `-l` is specified by POSIX.)

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

Stop after the first _num_ selected lines. If _num_ is zero, `grep` stops right away without reading input. A _num_ of _−_ 1 is treated as infinity and `grep` does not stop; this is the default.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

If the input is standard input from a regular file, and _num_ selected lines are output, `grep` ensures that the standard input is positioned just after the last selected line before exiting, regardless of the presence of trailing context lines. This enables a calling process to resume a search. For example, the following shell script makes use of it:

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

When `grep` stops after _num_ selected lines, it outputs any trailing context lines. When the `-c` or `--count` option is also used, `grep` does not output a count greater than _num_ . When the `-v` or `--invert-match` option is also used, `grep` stops after outputting _num_ non-matching lines.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

Print only the matched non-empty parts of matching lines, with each such part on a separate output line. Output lines use the same delimiters as input, and delimiters are null bytes if `-z` ( `--null-data` ) is also used (see Section 2.1.7 [Other Options], page 9).

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

Suppress error messages about nonexistent or unreadable files. ( `-s` is specified by POSIX.)

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

Print the 0-based byte offset within the input file before each line of output. If `-o` ( `--only-matching` ) is specified, print the offset of the matching part itself.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

Suppress the prefixing of file names on output. This is the default when there is only one file (or only standard input) to search.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

_Context lines_ are non-matching lines that are near a matching line. They are output only if one of the following options are used. Regardless of how these options are set, `grep` never outputs any given line more than once. If the `-o` ( `--only-matching` ) option is specified, these options have no effect and a warning is given upon their use.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

Print _num_ lines of trailing context after matching lines.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

When `-A` , `-B` or `-C` are in use, print _string_ instead of ' `--` ' between groups of lines.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

When `-A` , `-B` or `-C` are in use, do not print a separator between groups of lines.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

- When context is not specified, matching lines are simply output one right after another.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

If a file's data or metadata indicate that the file contains binary data, assume that the file is of type _type_ . Non-text bytes indicate binary data; these are either output bytes that are improperly encoded for the current locale (see Section 2.2 [Environment Variables], page 10), or null input bytes when the `-z` ( `--null-data` ) option is not given (see Section 2.1.7 [Other Options], page 9). By default, _type_ is ' `binary` ', and `grep` suppresses output after null input binary data is discovered, and suppresses output lines that contain improperly encoded data. When some output is suppressed, `grep` follows any output with a message to standard error saying that a binary file matches.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

If _type_ is ' `without-match` ', when `grep` discovers null binary data in an input file it assumes that any unprocessed input does not match; this is equivalent to the `-I` option. In this case the region of unprocessed input starts no later than the null binary data, and continues to end of file.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

If _type_ is ' `text` ', `grep` processes binary data as if it were text; this is equivalent to the `-a` option.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

When _type_ is ' `binary` ', `grep` may treat non-text bytes as line terminators even without the `-z` ( `--null-data` ) option. This means choosing ' `binary` ' versus ' `text` ' can affect whether a pattern matches a file. For example, when _type_ is ' `binary` ' the pattern ' `q$` ' might match ' `q` ' immediately followed by a null byte, even though this is not matched when _type_ is ' `text` '. Conversely, when _type_ is ' ' ' ' `binary` the pattern `.` (period) might not match a null byte.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

_Warning:_ The `-a` ( `--binary-files=text` ) option might output binary garbage, which can have nasty side effects if the output is a terminal and if the

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

If an input file is a directory, use _action_ to process it. By default, _action_ is ' `read` ', which means that directories are read just as if they were ordinary files (some operating systems and file systems disallow this, and will cause `grep` to print error messages for every directory or silently skip them). If _action_ is ' `skip` ', directories are silently skipped. If _action_ is ' `recurse` ', `grep` reads all files under each directory, recursively, following command-line symbolic links and skipping other symlinks; this is equivalent to the `-r` option.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

`-I` Process a binary file as if it did not contain matching data; this is equivalent to the ' `--binary-files=without-match` ' option.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

For each directory operand, read and process all files in that directory, recursively. Follow symbolic links on the command line, but skip symlinks that are encountered recursively. Note that if no file operand is given, grep searches the working directory. This is the same as the ' `--directories=recurse` ' option.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

Delimit the option list. Any later argument is not treated as an option even if it begins with ' `-` '. For example, ' `grep -- -PAT -file1 file2` ' searches for the pattern ' `-PAT` ' in the files named `-file1` and `file2` .

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

The behavior of `grep` is affected by several environment variables, the most important of which control the locale, which specifies how `grep` interprets characters in its patterns and data.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

The following environment variables affect the behavior of `grep` .

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

`LC_ALL LC_COLLATE LANG` These variables specify the locale for the `LC_COLLATE` category, which might affect how range expressions like ' `a-z` ' are interpreted.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

Normally the exit status is 0 if a line is selected, 1 if no lines were selected, and 2 if an error occurred. However, if the `-q` or `--quiet` or `--silent` option is used and a line is selected, the exit status is 0 even if an error occurred. Other `grep` implementations may exit with status greater than 2 on error.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

`grep` searches the named input files for lines containing a match to the given patterns. By default, `grep` prints the matching lines. A file named `-` stands for standard input. If no input is specified, `grep` searches the working directory `.` if given a command-line option specifying recursion; otherwise, `grep` searches standard input. There are four major variants of `grep` , controlled by the following options.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

Interpret patterns as basic regular expressions (BREs). This is the default.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

Interpret patterns as extended regular expressions (EREs). ( `-E` is specified by POSIX.)

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

Interpret patterns as fixed strings, not regular expressions. ( `-F` is specified by POSIX.)

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

Interpret patterns as Perl-compatible regular expressions (PCREs).

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

- In Perl and `git grep -P` , ' `\d` ' matches all Unicode digits, even if they are not ASCII. For example, ' `\d` ' matches (U `+` 0663 ARABIC-INDIC DIGIT THREE). In contrast, in ' `grep -P` ', ' `\d` ' matches only the ten ASCII digits, regardless of locale. In `pcre2grep` , ' `\d` ' ordinarily behaves like Perl and `git grep -P` , but when given the `--posix-digit` option it behaves like ' `grep -P` '. (On all platforms, ' `\D` ' matches the complement of ' `\d` '.)

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

- The pattern ' `[[:digit:]]` ' matches all Unicode digits in Perl, ' `grep -P` ', `git grep -P` , and `pcre2grep` , so you can use it to get the effect of Perl's ' `\d` ' on all these platforms. In other words, in Perl and `git grep -P` , ' `\d` ' is equivalent to ' `[[:digit:]]` ', whereas in ' `grep -P` ', ' `\d` ' is equivalent to ' `[0-9]` ', and `pcre2grep` ordinarily follows Perl but when given `--posixdigit` it follows ' `grep -P` '.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

- If `grep` is built with PCRE2 version 10.43 (2024) or later, ' `(?aD)` ' causes ' `\d` ' to behave like ' `[0-9]` ' and ' `(?-aD)` ' causes it to behave like ' `[[:digit:]]` '.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

- By default, `grep` applies each regexp to a line at a time, so the ' `(?s)` ' ' '

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

- directive (making `.` match line breaks) is generally ineffective. However, with `-z` ( `--null-data` ) it can work:

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

- `$ printf 'a\nb\n' |grep -zP '(?s)a.b'`

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

## **3 Regular Expressions**

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

A _regular expression_ is a pattern that describes a set of strings. Regular expressions are constructed analogously to arithmetic expressions, by using various operators to combine smaller expressions. `grep` understands three different versions of regular expression syntax: basic (BRE), extended (ERE), and Perl-compatible (PCRE). In GNU `grep` , basic and extended regular expressions are merely different notations for the same pattern-matching functionality. In other implementations, basic regular expressions are ordinarily less powerful than extended, though occasionally it is the other way around. The following description applies to extended regular expressions; differences for basic regular expressions are summarized afterwards. Perl-compatible regular expressions have different functionality, and are documented in the _pcre2syntax_ (3) and _pcre2pattern_ (3) manual pages, but work only if PCRE is available in the system.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

In regular expressions, the characters ' `.?*+{|()[\^$` ' are _special characters_ and have uses described below. All other characters are _ordinary characters_ , and each ordinary character is a regular expression that matches itself.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

' ' ' ' The period `.` matches any single character. It is unspecified whether `.` matches an encoding error.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

A regular expression may be followed by one of several repetition operators; the operators ' ' beginning with `{` are called _interval expressions_ .

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

- ' `?` ' The preceding item is optional and is matched at most once.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

- ' `*` ' The preceding item is matched zero or more times.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

- ' `+` ' The preceding item is matched one or more times.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

- ' `{` _`n`_ `}` ' The preceding item is matched exactly _n_ times.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

- ' `{` _`n`_ `,}` ' The preceding item is matched _n_ or more times.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

- ' `{,` _`m`_ `}` ' The preceding item is matched at most _m_ times. This is a GNU extension.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

- ' `{` _`n`_ `,` _`m`_ `}` ' The preceding item is matched at least _n_ times, but not more than _m_ times.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

The empty regular expression matches the empty string. Two regular expressions may be concatenated; the resulting regular expression matches any string formed by concatenating two substrings that respectively match the concatenated expressions.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

Two regular expressions may be joined by the infix operator ' `|` '. The resulting regular expression matches any string matching either of the two expressions, which are called _alternatives_ .

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

Repetition takes precedence over concatenation, which in turn takes precedence over alternation. A whole expression may be enclosed in parentheses to override these precedence rules and form a subexpression. An unmatched ' `)` ' matches just itself.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

A _bracket expression_ is a list of characters enclosed by ' `[` ' and ' `]` '. It matches any single character in that list. If the first character of the list is the caret ' `^` ', then it matches any character not in the list, and it is unspecified whether it matches an encoding error. For example, the regular expression ' `[0123456789]` ' matches any single digit, whereas ' `[^()]` ' matches any single character that is not an opening or closing parenthesis, and might or might not match an encoding error.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

Within a bracket expression, a _range expression_ consists of two characters separated by a hyphen. In the default C locale, it matches any single character that appears between the two characters in ASCII order, inclusive. For example, ' `[a-d]` ' is equivalent to ' `[abcd]` '. In other locales the behavior is unspecified: ' `[a-d]` ' might be equivalent to ' `[abcd]` ' or ' `[aBbCcDd]` ' or some other bracket expression, or it might fail to match any character, or the set of characters that it matches might be erratic, or it might be invalid. To obtain the traditional interpretation of bracket expressions, you can use the ' `C` ' locale by setting the `LC_ALL` environment variable to the value ' `C` '.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

Finally, certain named classes of characters are predefined within bracket expressions, as follows. Their interpretation depends on the `LC_CTYPE` locale; for example, ' `[[:alnum:]]` ' means the character class of numbers and letters in the current locale.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

## ' `[:alnum:]` '

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

Alphanumeric characters: ' `[:alpha:]` ' and ' `[:digit:]` '; in the ' `C` ' locale and ASCII character encoding, this is the same as ' `[0-9A-Za-z]` '.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

## ' `[:alpha:]` '

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

Alphabetic characters: ' `[:lower:]` ' and ' `[:upper:]` '; in the ' `C` ' locale and ASCII character encoding, this is the same as ' `[A-Za-z]` '.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

Graphical characters: ' `[:alnum:]` ' and ' `[:punct:]` '.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

## ' `[:lower:]` '

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

Note that the brackets in these class names are part of the symbolic names, and must be included in addition to the brackets delimiting the bracket expression.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

If you mistakenly omit the outer brackets, and search for say, ' `[:upper:]` ', GNU `grep` prints a diagnostic and exits with status 2, on the assumption that you did not intend to search for the regular expression ' `[:epru]` '.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

Special characters lose their special meaning inside bracket expressions.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

- ' `]` ' ends the bracket expression if it's not the first list item. So, if you want to make the ' `]` ' character a list item, you must put it first.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

- ' `-` ' represents the range if it's not first or last in a list or the ending point of a ' `-` '

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

The ' `\` ' character followed by a special character is a regular expression that matches the special character. The ' `\` ' character, when followed by certain ordinary characters, takes a special meaning:

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

- ' `\b` ' Match the empty string at the edge of a word.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

- ' `\B` ' Match the empty string provided it's not at the edge of a word.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

- ' `\<` ' Match the empty string at the beginning of a word.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

- ' `\>` ' Match the empty string at the end of a word.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

- ' `\w` ' Match word constituent, it is a synonym for ' `[_[:alnum:]]` '.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

' `\W` ' Match non-word constituent, it is a synonym for ' `[^_[:alnum:]]` '.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

' `\s` ' Match whitespace, it is a synonym for ' `[[:space:]]` '.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

' `\S` ' Match non-whitespace, it is a synonym for ' `[^[:space:]]` '. ' `\]` ' Match ' `]` '. ' `\}` ' Match ' `}` '.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

For example, ' `\brat\b` ' matches the separate word ' `rat` ', ' `\Brat\B` ' matches ' `crate` ' but not ' `furry rat` '.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

The behavior of `grep` is unspecified if a unescaped backslash is not followed by a special character, a nonzero digit, or a character in the above list. Although `grep` might issue a diagnostic and/or give the backslash an interpretation now, its behavior may change if the syntax of regular expressions is extended in future versions.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

## **3.4 Anchoring**

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

The caret ' `^` ' and the dollar sign ' `$` ' are special characters that respectively match the empty string at the beginning and end of a line. They are termed _anchors_ , since they force the match to be "anchored" to beginning or end of a line, respectively.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

The back-reference ' `\` _`n`_ ', where _n_ is a single nonzero digit, matches the substring previously matched by the _n_ th parenthesized subexpression of the regular expression. For example, ' `(a)\1` ' matches ' `aa` '. If the parenthesized subexpression does not participate in the match, the back-reference makes the whole match fail; for example, ' `(a)*\1` ' fails to match ' `a` '. If the parenthesized subexpression matches more than one substring, the back-reference refers to the last matched substring; for example, ' `^(ab*)*\1$` ' matches ' `ababbabb` ' but not ' `ababbab` '. When multiple regular expressions are given with `-e` or from a file (' `-f` _`file`_ '), back-references are local to each expression.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

## **3.6 Basic vs Extended Regular Expressions**

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

Basic regular expressions differ from extended regular expressions in the following ways:

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

- The characters ' `?` ', ' `+` ', ' `{` ', ' `|` ', ' `(` ', and ' `)` ' lose their special meaning; instead use the backslashed versions ' `\?` ', ' `\+` ', ' `\{` ', ' `\|` ', ' `\(` ', and ' `\)` '. Also, a backslash is needed before an interval expression's closing ' `}` '.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

- If an unescaped ' `^` ' appears neither first, nor directly after ' `\(` ' or ' `\|` ', it is treated like an ordinary character and is not an anchor.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

- If an unescaped ' `$` ' appears neither last, nor directly before ' `\|` ' or ' `\)` ', it is treated like an ordinary character and is not an anchor.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

- If an unescaped ' `*` ' appears first, or appears directly after ' `\(` ' or ' `\|` ' or anchoring ' `^` ', it is treated like an ordinary character and is not a repetition operator.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

Some strings are _invalid regular expressions_ and cause `grep` to issue a diagnostic and fail. For example, ' `xy\1` ' is invalid because there is no parenthesized subexpression for the backreference ' `\1` ' to refer to.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

Also, some regular expressions have _unspecified behavior_ and should be avoided even if `grep` does not currently diagnose them. For example, ' `xy\0` ' has unspecified behavior because ' `0` ' is not a special character and ' `\0` ' is not a special backslash expression (see Section 3.3 [Special Backslash Expressions], page 17). Unspecified behavior can be particularly problematic because the set of matched strings might be only partially specified, or not be specified at all, or the expression might even be invalid.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

The following regular expression constructs are invalid on all platforms conforming to POSIX, so portable scripts can assume that `grep` rejects these constructs:

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

- A basic regular expression containing a back-reference ' `\` _`n`_ ' preceded by fewer than _n_ closing parentheses. For example, ' `\(a\)\2` ' is invalid.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

- A bracket expression containing ' `[:` ' that does not start a character class; and similarly for ' `[=` ' and ' `[.` '. For example, ' `[a[:b]` ' and ' `[a[:ouch:]b]` ' are invalid.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

- Unescaped ' `\` ' at the end of a regular expression.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

- A ' `\{` ' in a basic regular expression that does not start an interval expression.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

- A basic regular expression with unbalanced ' `\(` ' or ' `\)` ', or an extended regular expression with unbalanced ' `(` '.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

- In the POSIX locale, a range expression like ' `z-a` ' that represents zero elements. A non-GNU `grep` might treat it as a valid range that never matches.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

- An interval expression with a repetition count greater than 32767. (The portable POSIX limit is 255, and even interval expressions with smaller counts can be impractically slow on all known implementations.)

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

- A bracket expression that contains at least three elements, the first and last of which are both ' `:` ', or both ' `.` ', or both ' `=` '. For example, a non-GNU `grep` might treat ' `[:alpha:]` ' like ' `[[:alpha:]]` ', or like ' `[:ahlp]` '.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

- Special backslash expressions like ' `\b` ', ' `\<` ', and ' `\]` '. See Section 3.3 [Special Backslash Expressions], page 17.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

- A basic regular expression that uses ' `\?` ', ' `\+` ', or ' `\|` '.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

- An extended regular expression that uses back-references.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

- An empty regular expression, subexpression, or alternative. For example, ' `(a|bc|)` ' is not portable; a portable equivalent is ' `(a|bc)?` '.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

- In a basic regular expression, an anchoring ' `^` ' that appears directly after ' `\(` ', or an anchoring ' `$` ' that appears directly before ' `\)` '.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

- In an extended regular expression, unescaped ' `{` ' that does not begin a valid interval expression. GNU `grep` treats the ' `{` ' as an ordinary character.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

- An input file that ends in a non-newline character, where GNU `grep` silently supplies a newline.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

- A backslash escaping an ordinary character, unless it is a back-reference like ' `\1` ' or a special backslash expression like ' `\<` ' or ' `\b` '. See Section 3.3 [Special Backslash Expressions], page 17. For example, ' `\x` ' has unspecified behavior now, and a future version of `grep` might specify ' `\x` ' to have a new behavior.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

- A range expression outside the POSIX locale. For example, in some locales ' `[a-z]` ' might match some characters that are not lowercase letters, or might not match some lowercase letters, or might be invalid. With GNU `grep` it is not documented whether these range expressions use native code points, or use the collation sequence specified by the `LC_COLLATE` category, or use the collation ordering used by `sort` and `strcoll` , or have some other interpretation. Outside the POSIX locale, it is portable to use ' `[[:lower:]]` ' to match a lower-case letter, or ' `[abcdefghijklmnopqrstuvwxyz]` ' to match an ASCII lower-case letter.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

In the ' `C` ' or ' `POSIX` ' locale, every character is encoded as a single byte and every byte is a valid character. In more-complex encodings such as UTF-8, a sequence of multiple bytes may be needed to represent a character, and some bytes may be encoding errors that do not contribute to the representation of any character. POSIX does not specify the behavior of `grep` when patterns or input data contain encoding errors or null characters, so portable scripts should avoid such usage. As an extension to POSIX, GNU `grep` treats null characters like any other character. However, unless the `-a` ( `--binary-files=text` ) option is used, the presence of null characters in input or of encoding errors in output causes GNU `grep` to treat the file as binary and suppress details about matches. See Section 2.1.6 [File and Directory Selection], page 7.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

In a regular expression, non-ASCII and non-printable characters other than newline are not special, and represent themselves. For example, in a locale using UTF-8 the command ' `grep '` _Λ ω_ `'` ' (where the white space between ' _Λ_ ' and the ' _ω_ ' is a tab character) searches for ' _Λ_ ' (Unicode character U `+` 039B GREEK CAPITAL LETTER LAMBDA), followed by a tab (U `+` 0009 TAB), followed by ' _ω_ ' (U `+` 03C9 GREEK SMALL LETTER OMEGA).

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

Suppose you want to limit your pattern to only printable characters (or even only printable ASCII characters) to keep your script readable or portable, but you also want to match specific non-ASCII or non-null non-printable characters. If you are using the `-P` ( `--perlregexp` ) option, PCREs give you several ways to do this. Otherwise, if you are using Bash, the GNU project's shell, you can represent these characters via ANSI-C quoting. For example, the Bash commands ' `grep $'` _Λ_ `\t` _ω_ `'` ' and ' `grep $'\u039B\t\u03C9'` ' both search for the same three-character string ' _Λ ω_ ' mentioned earlier. However, because Bash translates ANSI-C quoting before `grep` sees the pattern, this technique should not be used to match printable ASCII characters; for example, ' `grep $'\u005E'` ' is equivalent to ' `grep '^'` ' and matches any line, not just lines containing the character ' `^` ' (U `+` 005E CIRCUMFLEX ACCENT).

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

Here is an example command that invokes GNU `grep` :

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

```
grep-i'hello.*world'menu.hmain.c
```

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

This lists all lines in the files `menu.h` and `main.c` that contain the string ' `hello` ' followed by the string ' `world` '; this is because ' `.*` ' matches zero or more characters within a line. See Chapter 3 [Regular Expressions], page 15. The `-i` option causes `grep` to ignore case, causing it to match the line ' `Hello, world!` ', which it would not otherwise match.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

Here is a more complex example, showing the location and contents of any line containing ' `f` ' and ending in ' `.c` ', within all files in the current directory whose names start with non' `.` ', contain ' `g` ', and end in ' `.h` '. The `-n` option outputs line numbers, the `--` argument treats any later arguments as file names not options even if `*g*.h` expands to a file name that starts with ' `-` ', and the empty file `/dev/null` causes file names to be output even if only one file name happens to be of the form ' `*g*.h` '.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

Note that the regular expression syntax used in the pattern differs from the globbing syntax that the shell uses to match file names.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

```
grep-l'main'test-*.c
```

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

searches for ' `hello` ' in all files under the `/home/gigi` directory. For more control over which files are searched, use `find` and `grep` . For example, the following command searches only C files:

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

- `-exec grep -H 'hello' '{}' +`

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

```
grep-e"$pattern"./*
```

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

searches for all lines matching the pattern in all the working directory's files whose ' names do not begin with `.` '. Without the `-e` , `grep` might treat the pattern as an

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

This also fixes the problem, except that if there is a file named ' `-` ', `grep` misinterprets ' `-` ' the as standard input.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

4. Suppose I want to search for a whole word, not a part of a word?

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

```
grep-w'hello'test*.log
```

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

searches only for instances of ' `hello` ' that are entire words; it does not match ' `Othello` '. For more control, use ' `\<` ' and ' `\>` ' to match the start and end of words. For example:

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

```
grep'hello\>'test*.log
```

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

searches only for words ending in ' `hello` ', so it matches the word ' `Othello` '.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

5. How do I output context around the matching lines?

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

```
grep'eli'/etc/passwd/dev/null
```

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

gets you:

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

- `ps -ef | grep '[c]ron'`

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

If the pattern had been written without the square brackets, it would have matched not only the `ps` output line for `cron` , but also the `ps` output line for `grep` . Note that on some platforms, `ps` limits the output to the width of the screen; `grep` does not have any limit on the length of a line except the available memory.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

8. Why does `grep` report "binary file matches"?

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

If `grep` listed all matching "lines" from a binary file, it would probably generate output that is not useful, and it might even muck up your display. So GNU `grep` suppresses output from files that appear to be binary files. To force GNU `grep` to output lines even from files that appear to be binary, use the `-a` or ' `--binary-files=text` ' option. To eliminate the "Binary file matches" messages, use the `-I` or ' `--binary-files=without-match` ' option.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

9. Why doesn't ' `grep -lv` ' print non-matching file names?

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

' `grep -lv` ' lists the names of all files containing one or more lines that do not match. To list the names of all files that contain no matching lines, use the `-L` or `--fileswithout-match` option.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

```
grep'paul'/etc/motd|grep'franc,ois'
```

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

The `grep` command searches for lines that contain strings that match a pattern. Every line contains the empty string, so an empty pattern causes `grep` to find a match on each line. It is not the only such pattern: ' `^` ', ' `$` ', and many other patterns cause `grep` to match every line.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

To match empty lines, use the pattern ' `^$` '. To match blank lines, use the pattern ' `^[[:blank:]]*$` '. To match no lines at all, use an extended regular expression like ' `a^` ' or ' `$a` '. To match every line, a portable script should use a pattern like ' `^` ' instead of the empty pattern, as POSIX does not specify the behavior of the empty pattern.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

12. How can I search in both standard input and in files?

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

There is a related problem with Bash's `set -e -o pipefail` . Since `grep` does not always read all its input, a command outputting to a pipe read by `grep` can fail when `grep` exits before reading all its input, and the command's failure can cause Bash to exit.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

```
echo'ba'|grep-E'(a)\1|b\1'
```

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

Standard grep cannot do this, as it is fundamentally line-based. Therefore, merely using the `[:space:]` character class does not match newlines in the way you might expect.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

With the GNU `grep` option `-z` ( `--null-data` ), each input and output "line" is nullterminated; see Section 2.1.7 [Other Options], page 9. Thus, you can match newlines in the input, but typically if there is a match the entire input is output, so this usage is often combined with output-suppressing options like `-q` , e.g.:

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

```
printf'foo\nbar\n'|grep-z-q'foo[[:space:]]\+bar'
```

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

If this does not suffice, you can transform the input before giving it to `grep` , or turn to `awk` , `sed` , `perl` , or many other utilities that are designed to operate across lines.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

16. What do `grep` , `-E` , and `-F` stand for?

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

The name `grep` comes from the way line editing was done on Unix. For example, `ed` uses the following syntax to print a list of matching lines on the screen:

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

```
g/re/p
```

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

The `-E` option stands for Extended `grep` . The `-F` option stands for Fixed `grep` ;

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

7th Edition Unix had commands `egrep` and `fgrep` that were the counterparts of the modern ' `grep -E` ' and ' `grep -F` '. Although breaking up `grep` into three programs was perhaps useful on the small computers of the 1970s, `egrep` and `fgrep` were deemed obsolescent by POSIX in 1992, removed from POSIX in 2001, deprecated by GNU Grep 2.5.3 in 2007, and changed to issue obsolescence warnings by GNU Grep 3.8 in 2022; eventually, they are planned to be removed entirely.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

Interval expressions may be implemented internally via repetition. For example, ' `^(a|bc){2,4}$` ' might be implemented as ' `^(a|bc)(a|bc)((a|bc)(a|bc)?)?$` '. A large repetition count may exhaust memory or greatly slow matching. Even small counts can cause problems if cascaded; for example, ' `grep -E ".*{10,}{10,}{10,}{10,}{10,}"` ' is likely to overflow a stack. Fortunately, regular expressions like these are typically artificial, and cascaded repetitions do not conform to POSIX so cannot be used in portable programs anyway.

---

<!-- Source: 01_normalize/output/x200_103/grep_clean.md -->

For efficiency `grep` does not always read all its input. For example, the shell command ' `sed '/^...$/d' | grep -q X` ' can cause `grep` to exit immediately after reading a line containing ' `X` ', without bothering to read the rest of its input data. This in turn can cause `sed` to exit with a nonzero status because `sed` cannot write to its output pipe after `grep` exits. For more about the algorithms used by `grep` and about related string matching algorithms, see:

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

# Learning Regular Expressions

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- [You need tools to locate, parse, and replace text ]

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- [What regular expressions are and why they are used ]

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- [Regular expression syntax and rules ]

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- [How to read and write regular expressions ]

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- [How regular expressions are processed]

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- [Use Unix tools (][grep][, ][egrep][, ][sed][, ][awk][) that use regular ] expressions

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- [Read, and more importantly, write regular expressions ]

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- [Test and validate regular expressions using online tools ]

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- [It has tools to work with regexes (][grep][, ][sed][, etc) ]

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

# Introduction to Regular Expressions

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- [What are regular expressions? ]

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- [Why are regular expressions important? ]

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- [Intro to ][grep][/][egrep]

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- [grep][ examples ]

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

# What are Regular Expressions

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- [also known as ] _[regexes]_

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- [a sequence of characters describing a ] _[search pattern]_

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- [used to search text ]

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

# Why are Regular Expressions Important

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- [can search for text in files
]

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

grep Hello file.txt

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- [grep][, ][sed][, ][awk][, ][find]

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- [BRE - Base Regular Expressions (][grep][) ]

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- [ERE - Extended Regular Expressions (][egrep][) ]

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- [PCRE - Perl Compatible Regular Expressions (Python, Javascript) 
] (grep -P) - this is what we will use

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

## Intro to / grep egrep

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

# •[in ][ed][, to print all lines that match a regex:
]

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

g/re/p

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- [grep][ uses the BRE dialect ]

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- [egrep][ uses the ERE dialect ]

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- [egrep][ is equivalent to ][grep -E]

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- [grep -P][ (in Ubuntu) uses PCRE - we will use PCRE in this class ]

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

## grep/egrep Examples

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- [the first argument to grep is a regular expression, the ] second argument is the file

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- [with ][grep][, sometimes it is necessary to quote the regex, ] and usually ok to do so even if it not necessary:

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

## •[difference between ][grep][ and ][egrep][:
]

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

# grep/egrep Examples

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

## •[case insensitive match with the ][-i][ option:
]

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

# •[read regexes from a file with the ][-f][ option:
]

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- [show all lines the don't match with the ][-v][ option:
]

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- [grep][ with PCRE is available:
]

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- [Basic regular expressions - normal characters and ][.]

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- [Beginning and ending of the line - ][^][ and ][$]

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- [Regular Expression Rule #1 ]

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

## Basic Regexes

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

# •[Most characters (alpha-numeric) match themselves: ]

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

match "a" anywhere in the string (line of the file) grep abc file.txt

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- [Most characters (alpha-numeric) match themselves: ]

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

grep ab12 file.txt

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- [Many characters have special meaning 
]

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

. - matches any character except \n:

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

## Begin and End of String

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- [We can match the beginning or end of the string: ]

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- ^ - match the beginning of the string

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- $ - match the end of the string (or right before newline at the end of the string)

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

# Begin and End of String

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

grep ^abc file.txt

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

match "abc" at the beginning of the string

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

match "abc" at the beginning of the string grep abc$ file.txt

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

match "abc" at the end of the string (or "abc\n" at end of string)

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

match "abc" at the end of the string (or "abc\n" at end of string) grep ^abc$ file.txt

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

## To Match Special Characters

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

## •[To match special characters, they must be escaped with ] the backslash:

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

grep a\.b\.c file.txt grep ^\^\$$ file.txt

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

## Basic Regexes Example

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

# Basic Regexes Example

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- [Think of chars in a regex as 
] statements:

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

/^abc$/

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

**----- Start of picture text -----**<br>
BoS a b c EoS MATCH<br>**----- End of picture text -----**<br>

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- [if MATCH, stop - SUCCESS ]

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

## Regex Rule #1

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

MATCH

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

1. t 2. .n. 3. ^t 4. e$ 5. ne$ 6. ^...$

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- [Write regexes to do the following: ]

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- [match lines that start with ][e]

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- [match 4 character lines that begin with ][f][ and end with ] e

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

# Character Classes

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

•[A character class matches one character, any character in the class: ]

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

same - match one character a through e

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

same - match one character a through e /[a-z]/

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

# •[If the carat is the first character in a class, it means match a character ] not in the class

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- [If the carat is the first character in a class, it means match a character ] not in the class

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

# Character Class Example 2

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- [This class can be replaced with one of the POSIX ] character classes (don't forget the outer [ ]):

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- /[[:lower:]]/

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

alnum   - letters and digits [a-zA-Z0-9] alpha   - letters [a-zA-Z] ascii   - ascii codes 0 - 127 blank   - space or tab [ \t] cntrl   - control characters digit   - digits [0-9] graph   - printing characters, excluding space lower   - lower case letters [a-z] print   - printing characters, including space punct   - printing chars, excl letters, digits, space space   - white space [ \t\n\f\r] and VT upper   - upper case letters [A-Z] word    - word characters [a-zA-Z0-9_] xdigit  - hex digits

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

## Negate POSIX Character Classes

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- [To negate, include the carat after the first colon: ]

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

# Character Class Example 3

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- [Some character classes are so common there is a ] shorthand version:

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- \d   - digit [0-9]

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

\D   - non-digit [^0-9]

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- \w   - word [a-zA-Z0-9_]

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- \W   - non-word [^a-zA-Z0-9_]

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- \s   - space character [ \t\n\r\f]

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- \S   - non-space [^ \t\n\r\f]

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

2. [A-Z][a-z]

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

3. \w\s\d

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

5. ^[[:upper:]]

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

6. [[:^alpha:]]$

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- [match lines in ][words.txt][ that have at least 3 upper ] alphas in a row

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- [match lines in ][phonenumbers.txt][ that have 3 digits ] followed by a space, dash or period followed by 3 digits followed by a space, dash or period followed by 4 digits (use generic classes)

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- [Quantifier syntax ]

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- [Exercise: Quantifiers ]

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

# Quantifier Syntax

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

## * - zero or more

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

ab*c - "a", zero or more "b", "c"

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

+ - one or more

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

* - zero or more

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

ab?c - "a", zero or one "b", "c"

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

## + - one or more

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

## ? - zero or one

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

ab*c - "a", zero or more "b", "c" ac abc abbc abbbc ...

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

ab+c - "a", one or more "b", "c" abc abbc abbbc ...

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

? - zero or one ab?c - "a", zero or one "b", "c"

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

ab?c - "a", zero or one "b", "c" ac abc

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

ab{3}c - "a", 3 "b", "c"

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

{n,}  - n or more

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

ab{3,}c - "a", three or more "b", "c"

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

ab{3,5}c - "a", 3, 4 or 5 "b", "c"

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

m {n,m} - n through ab{3,5}c - "a", 3, 4 or 5 "b", "c"

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

ab{3,5}c - "a", 3, 4 or 5 "b", "c" abbbc abbbbc abbbbbc

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

## Quantifiers Are "Loops"

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

## Regex Rule #2

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- [Quantifiers are greedy - they consume as much as they ]

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

/ab.*c/ MATCH

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- [Quantifiers are by default ] _[greedy]_[ (aka ] _[maximal]_[) ]

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

/(?x) \(? \d{3} [ \-.\)]* \d{3} [ \-.]? \d{4}/

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

## Exercise 3

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

1. [A-Z]{2}

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

3. ([a-z][A-Z]){2}

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

4. [A-Z]+

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

5. [a-zA-Z]+\s\d+

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

6. \w+\s\w+

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- [Create regexes to match the following, embedding ] whitespace in each:

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

2. lines that begin with 3 digits, have 2 lower case vowels in a row somewhere in the line, and end with 3 lower case characters

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

3. lines that begin and end with more than one digit and that have non-digits in between (use generic classes)

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- [Alternation syntax ]

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

(?i) - case insensitive match

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

(?m) - multi-line mode (^ $ match begin/end of line)

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

\A - beginning of string

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

\Z - end of the string

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- [/(?xs) ^ hello .* world $ /] - match a string starting with "hello" and ending with "world", even if that string has \n characters (multiple lines as a single string)

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- match a string that has a line that begins with "world" (eg. "hello\nworld\n")

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- ^   - beginning of the string $   - end of the string (or right before \n at the end)

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- \A   - beginning of string \Z   - end of string (or right before \n at the end)

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- \b   - beginning or end of a word

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- \B   - not the beginning or end of a word

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

## •[Match either: ]

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- /a|b/      - either "a" or "b"

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

/a|b/      - either "a" or "b" /one|two/  - either "one" or "two"

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

/a|b/      - either "a" or "b"

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

/one|two/  - either "one" or "two"

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- /in|outside/      - either "in" or "outside"

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- /in|outside/      - either "in" or "outside" /(in|out)side/    - either "inside" or "outside"

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

/in|outside/      - either "in" or "outside"

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

/(in|out)side/    - either "inside" or "outside"

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

/today is (mon|tues)day/ - either "today is monday" or "today is tuesday"

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

/^first|second|third$/  - "first" at beginning of string, or "second" anywhere, or "third" at the end of the string

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

/^(first|second|third)$/ - begin the string, followed by either "first" or "second" or "third", followed by the end of the string

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- [Matching recurring text ]

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

/(.)\1/   - match two of the same character "aa", "bb", "77", "++"

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

/(.)\1/   - match two of the same character

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

/(.)(.)\1\2/   - match two characters twice in a row

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

/(.)(.)\2\1/   - match two chars, reverse them

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- /(.)\1/   - match two of the same character

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- /(.)(.)\2\1/   - match two chars, reverse them

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- /(?x) \b (\w+) \s \1\b/

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

213

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- $ echo 'the the' | sed -E 's/(\w+)\s\1\b/\1/' the

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

s/(one|two) (\w+)/\2/

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

s/(one|two) (\w+)/\2/ s/(?:one|two) (\w+)/\1/

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- /(?x) (?: https? | ftp) :\/\/ ([^/]+) (/.*)? / \1 is 'www.example.com' \2 is '/test/one/two.html'

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

1. Match a string that starts with an upper alpha and has that character later in the string (example: "My name is Mark")

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- 3.The Acme Corporation is changing its name to Acme Coyote. Write a regular expression to change all occurrences of "Acme" to "Acme Coyote" and "acme" to "acme Coyote" in a document.

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- 4. Some editors say there should only be 1 space character after a sentence. Write a regex to substitute 2 or more spaces after a period followed by an upper alpha with a single space.

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

# •[To match minimally, add a ][?][ after the quantifier: ]

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

*? - zero or more minimal

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

ab*?c - "a", zero or more "b" (minimal), "c"

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

ab+?c - "a", one or more "b" (minimal), "c"

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

ab??c - "a", zero or one "b" (minimal), "c"

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

ab{3}?c - "a", 3 "b" (minimal), "c"

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

ab{3,}?c - "a", three or more "b" (minimal), "c"

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

ab{3,5}?c - "a", 3, 4 or 5 "b" (minimal), "c"

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

## {n,}?  - n or more minimal

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- {n,m}? - n through m minimal

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

1. Match a string with two integers separated by a space. Match all digits of the first integer with a greedy match, but only match the first digit of the second integer with a lazy match.

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

3. Use a lazy quantifier to match the first quoted string (the line contains more than one quote within double quotes).

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

4. Use a lazy quantifier to match the last quoted string (the line contains more than one quote within double quotes).

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- [Zero length assertions (like ][^][ and ][$][) ]

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- [Only determine match or no match]

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

## /\d+(?=[aeiou])/

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

(?<=) - positive lookbehind - must be before

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

s/(\d)(\d\d\d)/\1,\2/g

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

1. Using positive lookahead, match the string "expression", but the matched text only includes "express"

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

2. Using positive lookbehind, write a substitution to convert '{a:test,b:quiz}' to '{a:"test",b:"quiz"}'

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

# Practical, Efficient and Readable Regular Expressions

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

## Practical, Efficient and Readable Regular Expression Topics

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- [Practical regular expressions - solving real problems ]

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- [Efficient regular expressions - writing faster regexes ]

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- [Exercise: Practical, efficient and readable regular ] expressions

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

## Practical Regular Expressions

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- ^           # begin the string

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

) {5,14}    # repeat group 5 to 14 times \d          # must end in a digit $           # end of string

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

(1[0-2]|0?[1-9])\/(3[01]|[12][0-9]|0?[1-9]) |

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

# Practical Regular Expressions

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

# Efficient Regular Expressions

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- [use minimal matching (usually, depends on string) ] - /".*?"/

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

## Efficient Regular Expressions

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- /(?:abc|abd|abe|abf)xy/ /ab(?:c|d|e|f)xy/

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

/(?>mon|tues|wednes)day$/

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

# Readable Regular Expressions

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

1. Write a regex to match all the valid URLs in urls.txt, but not any of the invalid URLs.

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

3. Write a regex to match valid Canadian postal codes. They are alternating upper alpha and digits, for example: "V5K 0V1". The space is optional. There are a few alphas that are not allowed - D, F, I, O, Q, U - use a negative lookahead to eliminate these. Additional invalid alphas for the first position  are W and Z.

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

to:

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

2022-12-02

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- [etc...]

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

s = '''

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- [Two useful text processing tools in Linux that use regular ]

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- expressions:

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

$ **sed 's/[a-z]*/(&)/g' one two** (one) (two) **three four five** (three) (four) (five)

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

# remove space and tab at end of line sed -E 's/[ \t]*$//' file_with_trailing_whitespace.txt # remove space and tab at beginning and end of line sed -E 's/^[ \t]*//;s/[ \t]*$//' file_with_excessive_whitespace.txt

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

- $ **ls -l | awk '/dat/'**

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

$ **awk -F: '/^root/ { print $3 }' /etc/passwd** 0

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

2. /.n./ - one, nine

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

3. /^t/ - two, three

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

4. /e$/ - one, three, five, nine

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

5. /ne$/ - one, nine

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

6. /^...$/ - one, two, six

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

1. grep -P e words.txt

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

2. grep -P ^e words.txt

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

3. grep -P ^f..e$ words.txt

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

1. /[0-9]/ - Ten 10, eleven 11

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

2. /[A-Z][a-z]/ - Zero, One, Two, Seven, Ten 10

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

3. /\w\s\d/ - Ten 10, eleven 11

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

4. /[[:upper:]]/ - zERo, One, Two, tHREE, FIVE, Seven, Ten 10

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

5. /^[[:upper:]]/ - One, Two, FIVE, Seven, Ten 10

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

1. grep -P [A-Z][A-Z][A-Z] words.txt

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

2. grep -P '\d\d\d[ \-.]\d\d\d[ \-.]\d\d\d\d' phonenumbers.txt

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

1. /[A-Z]{2}/ - zERo, tHREE, FIVE

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

2. /[a-z][A-Z]{2}/ - zERo, tHREE

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

3. /([a-z][A-Z]){2}/ - fOuR

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

4. /[A-Z]+/ - zERo, One, Two, tHREE, fOuR, FIVE, Seven, Ten 10

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

5. /[a-zA-Z]+\s\d+/ - Ten 10, eleven 11

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

6. /\w+\s\w+/ - Ten 10, eleven 11

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

1.grep -P '(?x) ^ \d{3} .* \d{3} $' ex3.txt

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

2. grep -P '(?x) ^ \d{3} .* [aeiou]{2} .* [az]{3} $' ex3.txt

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

3. grep -P '(?x) ^ \d{2,} \D+ \d{2,} $' ex3.txt

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

1. grep -P '(?xi) hello' ex4.txt

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

2. grep -P '(?x) \b[A-Z]{2}' ex4.txt

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

3. grep -P '(?x) [uz]\b' ex4.txt

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

4. grep -P '(?xi) \b[aeiou]{2} \w* [aeiou]{2}\b' ex4.txt

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

5. grep -P '(?x) \bthe\b .* \bthe\b' ex4.txt grep -P '(?x) (\bthe\b .*){2}' ex4.txt

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

6. grep -P '(?x) \b(the|there)\b .* \b(the|there)\b' ex4.txt grep -P '(?x) (\b(the|there)\b .*){2}' ex4.txt grep -P '(?x) \bthe(re)?\b .* \bthe(re)?\b' ex4.txt grep -P '(?x) (\bthe(re)?\b .*){2}' ex4.txt

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

7. grep -P '(?x) ^ the\b .* \bthe $' ex4.txt

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

8. grep -P '(?xi) ^ the(re)?\b .* \bthe(re)? $' ex4.txt

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

1.  /(?x) ^ ([A-Z]) .* \1/

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

2.  /(?x) \b(\w+)\b .* \b\1 $ / 3. s/(?i)(acme)/\1 Coyote/g 4.  s/\. {2,}([A-Z])/. \1/g

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

1. grep -P '(?x) \d+ \x20 \d+?' ex6.txt

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

2. grep -P '(?x) \d+? \x20 \d+?' ex6.txt

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

3. grep -P '(?x) " [^"]+? "' ex6.txt

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

4. grep -P '(?x) .* " [^"]+? "' ex6.txt

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

5. grep -P '(?x) , [^,]*+ ,' ex6.txt

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

1.  /express(?=ion)/ 2. s/(?<=:)\w+/"$&"/g

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

1. grep -P '(?xi) ^ (https?|ftp|file) :// \S+ $' urls.txt

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

grep -P '(?xi) ^ (https?|ftp|file) :// [-A-Z0-9+&@#/%? =~_|$!:,.;]* [A-Z0-9+&@#/%=~_|$]' urls.txt grep -P '(?xi) ^ ( (https?|ftp|file):// | (www|ftp) \. ) [-A-Z0-9+&@#/%?=~_|$!:,.;]* [A-Z0-9+&@#/%=~_|$]' urls.txt

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

2. sed -E 's/^((https?|ftp|file):\/\/|(www|ftp)\.)[-A-

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

3. grep -P '(?xi) ^ (?! .* [DFIOQU]) [A-VXY] \d [A-Z] \x20?

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

4. sed -E 's/^([0-9][0-9])-([0-9][0-9])-([0-9][0-9][0-9] [0-9])$/\3-\1-\2/g' dates.txt

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

1. sed -E 's/^\s*(.*)\s*$/\1/' < ex9-1.txt

---

<!-- Source: 01_normalize/output/x200_103/lreslides1742829038471_clean.md -->

^

---

## Extraction Summary

- Objective: x200_103
- Source files scanned: 4
- Total paragraphs classified: 1404
- Paragraphs classified RELEVANT: 518
- Paragraphs filtered out: 886
- Parse errors (kept): 0
- Batch ID: msgbatch_01Xm7ruRQvgfwazgzXqEFbU7
- Run date: 2026-05-08
