<!-- Source: 01_normalize/input/x200_103/CertGuide.pdf | Cleaned: 2026-05-08 -->

By de fault, the sort com mand sorts in byte or der, which is the or der in which the char ac ters ap pear in the ASCII text ta ble. No tice that this looks like al pha bet i cal or der, but it is not, as all cap i tal let ters are shown be fore low er case let ters. So Zoo would be listed be fore ap ple. In some cases, that is not con ve nient be cause the con tent that needs sort ing may be nu meric or in an other for mat. The sort com mand off ers diff er ent op tions to help sort ing these spe cific types of data. Type, for in ‐ stance, cut -f 3 -d : /etc/passwd | sort -n to sort the third field of the /etc/passwd file in nu meric or der. It can be use ful also to sort in re verse or der; if you use the com mand du -h | sort -rn, you get a list of files sorted with the big gest file in that di rec tory listed first.

You can also use the sort com mand and spec ify which col umn you want to sort. To do this, use sort -k3 -t : /etc/passwd, for in stance, which uses the field sep a ra tor : to sort the third col umn of the /etc/passwd file. Add -n to the com mand to sort in a nu meric or der, and not in an al pha betic or der.

An other ex am ple is shown in Ex am ple 4-2, where the out put of the ps aux com mand is sorted. This com mand gives an over view of pro cesses run ning on a Linux sys tem. The fourth col umn in di cates mem ory us age, and by ap ply ing a nu meric sort to the out put of the com mand, you can see that the pro cesses are sorted by mem ory us age, such that the process that con sumes the most mem ory is listed last.

|`[root@localhost ~]#`<br>**`ps aux | sort -k`**|`[root@localhost ~]#`<br>**`ps aux | sort -k`**|**`4 -n`**|||
|---|---|---|---|---|
|`root           897  0.3  1.1 348584 42200`|||`?`|`Ssl  08:12   0:00`|
|`/usr/bin/python3 -s /usr/sbin/firewalld`|||`--nofork --nopid`||
|`student       2657  1.0  1.1 2936188`|`45200 ?`|||`Ssl  08:14   0:00`|
|`/usr/bin/gjs /usr/share/org.gnome.Characters/org.gnome.Characters.`|||||
|`BackgroundService`|||||
|`student       2465  0.3  1.3 143976 52644`|||`?`|`S    08:14   0:00`|
|`/usr/bin/Xwayland :0 -rootless -noreset`|||`-accessx -core -auth /`||
|`run/user/1000/.mutter-Xwaylandauth.0SRUV1 -listenfd 4 -listenfd 5`|||||
|`-displayfd 6 -initfd 7`|||||
|`student       2660  1.9  1.4 780200 53412`|||`?`|`Ssl  08:14   0:00`|
|`/usr/libexec/gnome-terminal-server`|||||
|`root          2480  2.1  1.6 379000 61568`|||`?`|`Ssl  08:14   0:00`|
|`/usr/bin/python3 /usr/libexec/rhsm-service`|||||
|`student       2368  0.9  1.6 1057048`|`61096 ?`|||`Sl   08:14   0:00`|
|`/usr/libexec/evolution-data-server/evolution-alarm-notify`|||||
|`root          1536  0.6  1.8 555908 69916`|||`?`|`Ssl  08:12   0:00`|
|`/usr/libexec/packagekitd`|||||
|`student       2518  0.6  1.8 789408 70336`|||`?`|`Ssl  08:14   0:00`|
|`/usr/libexec/gsd-xsettings`|||||
|`student       2540  0.5  1.8 641720 68828`|||`?`|`Sl   08:14   0:00`|
|`/usr/libexec/ibus-x11 --kill-daemon`|||||
|`student       2381  4.7  1.9 1393476`|`74756 ?`|||`Sl   08:14   0:00`|
|`/usr/bin/gnome-software --gapplication-service`|||||
|`student       2000 16.0  7.8 3926096`|`295276 ?`|||`Ssl  08:14   0:03`|
|`/usr/bin/gnome-shell`|||||

When work ing with text files, you some times get a large amount of out put. Be fore de cid ing which ap proach to han dling the large amount of out put works best in a spe cific case, you might want to have an idea about the amount of text you are deal ing with. In that case, the wc com mand is use ful. In its out put, this com mand gives three diff er ent re sults: the num ber of lines, the num ber of words, and the num ber of char ac ters.

Con sider, for ex am ple, the ps aux com mand. When ex e cuted as root, this com mand gives a list of all pro cesses run ning on a server. One so lu tion to count how many pro cesses there are ex actly is to pipe the out put of ps aux through wc, as in ps aux | wc. You can see the re sult of the com mand in Ex am ple 4-3, which shows that the to tal num ber of lines is 90 and that there are 1,045 words and 7,583 char ac ters in the com mand out put.

|`[root@localhost ~]#`|<br>**`ps aux | wc`**|
|---|---|
|`90       1045`|`7583`|

Work ing with text files is an im por tant skill for a Linux ad min is tra tor. You must know not only how to cre ate and mod ify ex ist ing text files, but also how to find the text file that con tains spe cific text.

It will be clear some times which spe cific text you are look ing for. Other times, it might not. For ex am ple, are you look ing for color or colour? Both spellings might give a match. This is just one ex am ple of why us ing flex i ble pat terns while look ing for text can prove use ful. In Linux these flex i ble pat terns are known as reg u lar ex pres sions, of ten also re ferred to as regex.

To un der stand reg u lar ex pres sions a bit bet ter, let's take a look at a text file ex am ple, shown in Ex am ple 4-4. This file con tains the last six lines from the /etc/passwd file. (This file is used for stor ing Linux ac counts; see Chap ter 6, "User and Group Man age ment," for more de tails.)

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

```
[root@localhost ~]# grep anna /etc/passwd
anna:x:1000:1000::/home/anna:/bin/bash
rihanna:x:1001:1001::/home/rihanna:/bin/bash
annabel:x:1002:1002::/home/annabel:/bin/bash
joanna:x:1004:1004::/home/joanna:/bin/bash
```

A reg u lar ex pres sion is a search pat tern that al lows you to look for spe cific text in an ad vanced and flex i ble way. Us ing Line An chors In Ex am ple 4-5, sup pose that you wanted to spec ify that you are look ing for lines that start with the text anna. The type of reg u lar ex pres sion that spec i fies where in a line of out put the re sult is ex pected is known as a line an chor. To show only lines that start with the text you are look ing for, you can use the reg u lar ex pres sion ^ (in this case, to in di cate that you are look ing only for lines where anna is at the be gin ning of the line; see Ex am ple 4-6). Ex am ple 4-6 Look ing for Lines Start ing with a Spe cific Pat tern

|Click here to view code im age|
|---|
|`[root@localhost ~]#`<br>**`grep ^anna /etc/passwd`**|
|`anna:x:1000:1000::/home/anna:/bin/bash`|
|`annabel:x:1002:1002::/home/annabel:/bin/bash`|

An other reg u lar ex pres sion that re lates to the po si tion of spe cific text in a spe cific line is $, which states that the line ends with some text. For in stance, the com ‐ mand grep ash$ /etc/passwd shows all lines in the /etc/passwd file that end with the text ash. This com mand shows all ac counts that have a shell and are able to log in (see Chap ter 6 for more de tails).

Us ing Es cap ing in Reg u lar Ex pres sions

Al though not manda tory, when you're us ing reg u lar ex pres sions, it is a good idea to use es cap ing to pre vent reg u lar ex pres sions from be ing in ter preted by the ‐ shell. When a com mand line is en tered, the Bash shell parses the com mand line, look ing for any spe cial char ac ters like *, $, and ?. It will next in ter pret these char ac ters. The point is that reg u lar ex pres sions use some of these char ac ters as well, and to make sure the Bash shell doesn't in ter pret them, you should use es cap ing.

In many cases, it is not re ally nec es sary to use es cap ing; in some cases, the reg u lar ex pres sion fails with out es cap ing. To pre vent this from ever hap pen ing, it is a good idea to put the reg u lar ex pres sion be tween quotes. So, in stead of typ ing grep ^anna /etc/passwd, it is bet ter to use grep '^anna' /etc/passwd, even if in this case both ex am ples work.

Us ing Wild cards and Mul ti pli ers

In some cases, you might know which text you are look ing for, but you might not know how the spe cific text is writ ten. Or you might just want to use one reg u lar ex pres sion to match diff er ent pat terns. In those cases, wild cards and mul ti pli ers come in handy.

To start with, there is the dot (.) reg u lar ex pres sion. This is used as a wild card char ac ter to look for one spe cific char ac ter. So, the reg u lar ex pres sion r.t would match the strings rat, rot, and rut.

In some cases, you might want to be more spe cific about the char ac ters you are look ing for. If that is the case, you can spec ify a range of char ac ters that you are ' look ing for. For in stance, the reg u lar ex pres sion r[aou]t matches the strings rat, rot, and rut but it wouldn t match rit and ret.

An other use ful reg u lar ex pres sion is the mul ti plier *. This matches zero or more of the pre vi ous char ac ter. That does not seem to be very use ful, but in deed it is, as you will see in the ex am ples at the end of this sec tion.

If you know ex actly how many of the pre vi ous char ac ter you are look ing for, you can spec ify a num ber also, as in re\{2\}d, which would match reed, but not red. The last reg u lar ex pres sion that is use ful to know about is ?, which matches zero or one of the pre vi ous char ac ter. Ta ble 4-3 pro vides an over view of the most im ‐ por tant reg u lar ex pres sions.

Us ing Ex tended Reg u lar Ex pres sions

What makes reg u lar ex pres sions some times a bit hard to un der stand is the fact that there are diff er ent sets of reg u lar ex pres sions. The base reg u lar ex pres sions as dis cussed so far are sup ported by tools like grep. There is also a set of ex tended reg u lar ex pres sions, which is not sup ported by de fault. When used with grep, you'll have to add the -E op tion to in di cate it is an ex tended reg u lar ex pres sion. The + can be used to in di cate that a char ac ter should oc cur one or more times, and the ? is used to in di cate that a char ac ter should oc cur zero or one times. When used in grep, don't for get to use grep -E to en sure that these are in ter preted as ex ‐ tended reg u lar ex pres sions!

Ta ble 4-3 Most Sig nifi cant Reg u lar Ex pres sions

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

Reg u lar Ex pres sion Use

Matches a min i mum of one and a max i mum of three of the pre vi ous char ac ter.

|||
|---|---|
|\{1,3\}|Matches a min i mum of one and a max i mum of three of the pre vi ous char ac ter.|
|colou?r|Matches zero or one of the pre vi ous char ac ter. This makes the pre vi ous char ac ter op tional, which in this ex am ple would match bothcolorandcolour.|
|(…)|Used to group mul ti ple char ac ters so that the reg u lar ex pres sion can be ap plied to the group.|

Let's take a look at an ex am ple of a reg u lar ex pres sion that comes from the man page se m an age-fcon text and re lates to man ag ing SELinux (see Chap ter 22, "Man ag ‐ ing SELinux"). The sam ple line con tains the fol low ing reg u lar ex pres sion:

## `"/web(/.*)?"`

In this reg u lar ex pres sion, the text /web is re ferred to. This text string can be fol lowed by the reg u lar ex pres sion (/.*)?. To un der stand the reg u lar ex pres sion, start with the ?, which refers to the part be tween braces and in di cates that the part be tween braces may oc cur zero times or one time. Within the braces, the pat tern starts with a slash, which is just a slash, fol lowed by zero or more char ac ters. So this means that just the di rec tory name gives a match, but also the di rec tory name fol lowed by just a slash, or a slash that is fol lowed by a file name.

What makes reg u lar ex pres sions diffi cult is that there is not just one set of reg u lar ex pres sions; there are also ex tended reg u lar ex pres sions. And to make the con ‐ cept more com plex, the ex tended reg u lar ex pres sions need spe cific com mands. The well-known com mand grep (cov ered next) by de fault deals with base reg u lar ex pres sions. If you want to use ex tended reg u lar ex pres sions, you need grep -E or egrep.

Two com mon ex tended reg u lar ex pres sions are + and ?. The + will look for a pat tern where the pre ced ing char ac ter oc curs one or more times, and the ? looks for a pat tern where the pre ced ing char ac ter does not oc cur or oc curs one time. Use the fol low ing pro ce dure to find out how these ex tended reg u lar ex pres sions can be con fus ing:

Step 1. Cre ate a text file with the name regex.txt and the fol low ing con tents:

```
bat
boot
boat
bt
```

Step 2. Use grep 'b.*t' regex.txt to see any line that starts with a b and ends with a t.

Step 3. Use grep 'b.+t' regex.txt. You might ex pect to see only lines that have at least three char ac ters, but you don't, be cause you are us ing an ex tended reg u lar ex pres sion, and with out us ing any ad di tional op tions, grep doesn't rec og nize the ex tended reg u lar ex pres sion.

Step 4. Use grep -E 'b.+t' regex.txt. Now you see that the ex tended reg u lar ex pres sion does work as ex pected.

## Us ing grep to An a lyze Text

The ul ti mate util ity to work with reg u lar ex pres sions is grep, which stands for "gen eral reg u lar ex pres sion parser." Quite a few ex am ples that you have seen al ‐ ready were based on the grep com mand. The grep com mand has a cou ple of use ful op tions to make it even more effi cient. Ta ble 4-4 de scribes some of the most use ful op tions.

|Op tion|Use|
|---|---|
|-i|Matches up per- and low er case let ters (i.e., not case sen si tive).|
|-v|Shows only lines that donotcon tain the reg u lar ex pres sion.|

|Op tion|Use|
|---|---|
|-r|Searchesfles in the cur rent di rec tory and all sub di rec to ries.|
|-e|Searches for lines match ing more than one reg u lar ex pres sion. Use-ebe fore each reg u lar ex pres sion you want to use.|
|-E|In ter prets the search pat tern as an ex tended reg u lar ex pres sion.|
|-A <num ber>|Shows <num ber> of lines af ter the match ing reg u lar ex pres sion.|
|-B <num ber>|Shows <num ber> of lines be fore the match ing reg u lar ex pres sion.|

1. Type grep '^#'/etc/ser vices. This shows that the file /etc/ser vices con tains a num ber of lines that start with the com ment sign, #.

2. To view the con fig u ra tion lines that re ally mat ter, type grep -v '^#'/etc/ser vices. This shows only lines that do not start with a #.

3. Type grep -v '^#' /etc/ser vices -B 5. This shows lines that do not start with a # sign but also the five lines that are di rectly be fore each of those lines, which is use ful be cause in the pre ced ing lines you'll typ i cally find com ments on how to use the spe cific pa ram e ters. How ever, you'll also see that many blank lines are dis played.

4. Type grep -v -e '^#' -e '^$'/etc/ser vices. This ex cludes all blank lines and lines that start with #.

## Work ing with Other Use ful Text Pro cess ing Util i ties

The grep util ity is a pow er ful util ity that al lows you to work with reg u lar ex pres sions. It is not the only util ity, though. Some even more pow er ful util i ties ex ist, like awk and sed, both of which are ex tremely rich and merit a book by them selves. The util i ties were de vel oped in the time that com put ers did not com monly have screens at tached, and for that rea son they do a good job of treat ing text files in a scripted way.

As a Linux ad min is tra tor in the twenty-first cen tury, you do not have to be a spe cial ist in us ing these util i ties any more. It does make sense, how ever, to know how to per form some com mon tasks us ing these util i ties. The most use ful use cases are sum ma rized in the fol low ing ex am ples.

This com mand shows the fourth field from /etc/passwd:

```
awk -F :   ' { print $4 }'   /etc/passwd
```

This is some thing that can be done by us ing the cut util ity as well, but the awk util ity is more suc cess ful in dis tin guish ing the fields that are used in com mand out ‐ put of files. The bot tom line is that if cut does not work, you should try the awk util ity.

You can also use the awk util ity to do tasks that you might be used to us ing grep for. Con sider the fol low ing ex am ple:

```
awk -F : ' /user/ { print $4 }'  /etc/passwd
```

This com mand searches the /etc/passwd file for the text user and will print the fourth field of any match ing line.

In this ex am ple, the "stream ed i tor" sed is used to print the fifth line from the /etc/passwd file:

```
sed -n 5p /etc/passwd
```

The sed util ity is a very pow er ful util ity for fil ter ing text from text files (like grep), but it has the ben e fit that it also al lows you to ap ply mod i fi ca tions to text files, as shown in the fol low ing ex am ple:

```
sed -i s/old-text/new-text/g ~/myfile
```

In this ex am ple, the sed util ity is used to search for the text old-text in ~/my file and re place all oc cur rences with the text new-text. No tice that the de fault sed be hav ‐ ior is to write the out put to STD OUT, but the op tion -i will write the re sult di rectly to the file. Make sure that you know what you are do ing be fore us ing this com ‐ mand, be cause it might be diffi cult to re vert file mod i fi ca tions that are ap plied in this way.

```
sed -i -e ' 2d'  ~/myfile
```

With this com mand, you can delete a line based on a spe cific line num ber. You can also make more com pli cated ref er ences to line num bers. Use, for in stance, sed -i -e '2d;20,25d' ~/my file to delete lines 2 and 20 through 25 in the file ~/my file.