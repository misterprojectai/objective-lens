<!-- Source: 01_normalize/input/x200_102/CertGuide.pdf | Cleaned: 2026-05-08 -->

The word ar gu ment is a bit con fus ing. Gen er ally speak ing, it refers to any thing that the com mand ad dresses, so any thing you put af ter the com mand is an ar gu ‐ ment (in clud ing the op tions). Apart from the op tions that can be used as an ar gu ment, com mands can have other ar gu ments as well, which serve as a tar get to the com mand.

Let's have a look at an ex am ple: the com mand ls -l /etc. This com mand has two diff er ent ar gu ments: -l and /etc. The first ar gu ment is an op tion, mod i fy ing the be ‐ hav ior of the com mand. The sec ond ar gu ment is a tar get, spec i fy ing where the com mand should do its work. You'll find these three el e ments in nearly all com ‐ mands you work with in a Linux en vi ron ment.

The pur pose of the Linux shell is to pro vide an en vi ron ment in which com mands can be ex e cuted. The shell takes care of in ter pret ing the com mand that a user has en tered cor rectly. To do this, the shell makes a dis tinc tion be tween three kinds of com mands:

An alias is a com mand that a user can de fine as needed. Some aliases are pro vided by de fault; type alias on the com mand line to get an over view. To de fine an alias, use alias new com mand='old com mand' (as in the de fault alias ll='ls -l --color=auto' that has al ready been cre ated on your sys tem). Aliases are ex e cuted be ‐ fore any thing else. So, if you have an alias with the name ll but also a com mand with the name ll, the alias will al ways take prece dence for the com mand, un less a com plete path name like /usr/bin/ls is used.

An in ter nal com mand is a com mand that is a part of the shell it self and, as such, doesn't have to be loaded from disk sep a rately. An ex ter nal com mand is a com ‐ mand that ex ists as an ex e cutable file on the disk of the com puter. Be cause it has to be read from disk the first time it is used, it is a bit slower. When a user ex e cutes a com mand, the shell first looks to de ter mine whether it is an in ter nal com mand; if it is not, it looks for an ex e cutable file with a name that matches the com mand on disk. To find out whether a com mand is a Bash in ter nal com mand or an ex e cutable file on disk, you can use the type com mand. Use for in stance type pwd to find out that the pwd com mand that will be ex e cuted is re ally an alias.

To change how ex ter nal com mands are found by the shell, use the $PATH vari able. This vari able de fines a list of di rec to ries that is searched for a match ing file ‐ name when a user en ters a com mand. To find out which ex act com mand the shell will be us ing, you can use the which com mand. For in stance, type which ls to find out where the shell will get the ls com mand from. An even stronger com mand is type, which will also work on in ter nal com mands and aliases.

You should no tice that, for se cu rity rea sons, the cur rent di rec tory is not in the $PATH vari able and Linux does not look in the cur rent di rec tory to see whether a spe cific com mand is avail able from that di rec tory. That is why you need to start a com mand that is in the cur rent di rec tory but nowhere in the $PATH by in clud ing ./ in front of it. The dot stands for the cur rent di rec tory, and by run ning it as ./, you tell Bash to look for the com mand in the cur rent di rec tory. Al though run ning com mands this way is not very com mon, you will have to do it to run scripts that you've cre ated in your cur rent di rec tory.

The $PATH vari able can be set for spe cific users, but in gen eral, most users will be us ing the same $PATH vari able. The only ex cep tion to this is the user root, who needs ac cess to spe cific ad min is tra tion com mands. In Ex er cise 2-1, you learn some of the ba sics about work ing with com mands.

3. Type time ls. This ex e cutes the ls com mand where the Bash in ter nal time shows in for ma tion about the time it took to com plete this com mand.

4. Type which time. This shows the file name /usr/bin/time that was found in the $PATH vari able.

5. Type time, which shows that time is a shell key word.

6. Type echo $PATH to show the con tents of the $PATH vari able. You can see that /usr/bin is in cluded in the list, but be cause there also is an in ter nal com mand time, the time com mand from the path will not be ex e cuted un less you tell the shell specifi cally to do so—the com mand in step 3 has ex e cuted the in ter nal com mand for you be cause of com mand prece dence.

7. Type /usr/bin/time ls to run the /usr/bin/time com mand when ex e cut ing ls. You'll no tice that the out put diff ers com pletely. Ig nore the mean ing of the out put; we get back to that later. What mat ters for now is that you re al ize that these are re ally two diff er ent com mands.

## I/O Re di rect ion

‐ By de fault, when a com mand is ex e cuted, it shows its re sults on the screen of the com puter you are work ing on. The com puter mon i tor is used as the stan dard des ti na tion for out put, which is also re ferred to as STD OUT. The shell also has de fault stan dard des ti na tions to send er ror mes sages to (STDERR) and to ac cept in put (STDIN). Ta ble 2-2 gives an over view of all three.

Ta ble 2-2 Stan dard In put, Out put, and Er ror Over view

|Name|De fault Des ti na tion|Use in Re di rect ion|File De scrip tor Num ber||
|---|---|---|---|---|
|STDIN|Com puter key board|< (same as 0<)|0||
|||||49|

||Name<br>De fault Des ti na tion<br>Use in Re di rect ion<br>File De scrip tor Num ber<br>STD OUT<br>Com puter mon i tor<br>> (same as 1>)<br>1<br>STDERR<br>Com puter mon i tor<br>2><br>2|
|---|---|
|||
|||
|||

So if you run a com mand, that com mand would ex pect in put from the key board, and it would nor mally send its out put to the mon i tor of your com puter with out mak ing a dis tinc tion be tween nor mal out put and er rors. Some com mands, how ever, are started in the back ground and not from a cur rent ter mi nal ses sion, so these com mands do not have a mon i tor or con sole ses sion to send their out put to, and they do not lis ten to key board in put to ac cept their stan dard in put. That is where re di rect ion comes in handy. Re di rect ion is also use ful if you want to work with in put from an al ter na tive lo ca tion, such as a file.

Pro grams started from the com mand line have no idea what they are read ing from or writ ing to. They just read from what the Linux ker nel calls file de scrip tor 0 if they want to read from stan dard in put, and they write to file de scrip tor num ber 1 to dis play non-er ror out put (also known as "stan dard out put") and to file de scrip ‐ tor 2 if they have er ror mes sages to be out put. By de fault, these fle de scrip tors are con nected to the key board and the screen. If you use re di rect ion sym bols such as <, >, and |, the shell con nects the file de scrip tors to files or other com mands. Let's first look at the redi rec tors < and >. Later we dis cuss pipes (the | sym bol). Ta ‐ ble 2-3 shows the most com mon redi rec tors that are used from the Bash shell.

## Ta ble 2-3 Com mon Bash Redi rec tors

|Redi rec tor|Ex pla na tion|
|---|---|
|> (same as 1>)|Redi rects STD OUT. If re di rect ion is to afle, the cur rent con tents of thatfle are over writ ten.|
|>> (same as 1>>)|Redi rects STD OUT in ap pend mode. If out put is writ ten to afle, the out put is ap pended to thatfle.|
|2>|Redi rects STDERR.|
|2>&1|Redi rects STDERR to the same des ti na tion as STD OUT. No tice that this has to be used in com bi na tion with nor mal out put re di rect ion, as inls whuhiu > er rout 2>&1.|
|< (same as 0<)|Redi rects STDIN.|

In I/O re di rect ion, files can be used to re place the de fault STDIN, STD OUT, and STDERR. You can also re di rect to de vice fles. A de vice file on Linux is a file that is used to ac cess spe cific hard ware. Your hard disk, for in stance, can be re ferred to as /dev/sda in most cases, the con sole of your server is known as /dev/con sole or /dev/tty1, and if you want to dis card a com mand's out put, you can re di rect to /dev/null. Note that to ac cess most de vice files, you need to have root priv i leges.

## Us ing Pipes

Whereas an I/O redi rec tor is used as an al ter na tive for a key board and com puter mon i tor, a pipe can be used to catch the out put of one com mand and use that as in put for a sec ond com mand. If a user runs the com mand ls, for in stance, the out put of the com mand is shown on screen, be cause the screen is the de fault STD OUT. If the user uses ls | less, the com mands ls and less are started in par al lel. The stan dard out put of the ls com mand is con nected to the stan dard in put of less. Ev ery ‐ thing that ls writes to the stan dard out put will be come avail able for read ing from stan dard in put in less. The re sult is that the out put of ls is shown in the less pager, where the user can browse up and down through the re sults eas ily.

As a Linux ad min is tra tor, you will use pipes a lot. Us ing pipes makes Linux a flex i ble op er at ing sys tem; by com bin ing mul ti ple com mands us ing pipes, you can cre ‐ ate "su per" com mands that make al most any thing pos si ble. In Ex er cise 2-2, you use I/O redi rec tors and pipes.

Ex er cise 2-2 Us ing I/O Re di rect ion and Pipes

1. Open a shell as user stu dent and type cd with out any ar gu ments. This en sures that the home di rec tory of this user is the cur rent di rec tory while work ing on this ex er cise. Type pwd to ver ify this.

2. Type ls. You'll see the ls com mand out put on screen.

3. Type ls > /dev/null. This redi rects STD OUT to the null de vice, with the re sult that you will not see it.

4. Type ls il we hgi > /dev/null. This com mand shows a "no such file or di rec tory" mes sage on screen. You see the mes sage be cause it is not STD OUT, but rather an er ror mes sage that is writ ten to STDERR.

5. Type ls il we hgi 2> /dev/null. Now you will no longer see the er ror mes sage.

6. Type ls il we hgi /etc 2> /dev/null. This shows the con tents of the /etc folder while hid ing the er ror mes sage.

7. Type ls il we hgi /etc 2> /dev/null > out put. In this com mand, you still write the er ror mes sage to /dev/null while send ing STD OUT to a file with the name out ‐ put that will be cre ated in your home di rec tory.

8. Type cat out put to show the con tents of this file.

9. Type echo hello > out put. This over writes the con tents of the out put file. Ver ify this by us ing cat out put again.

10. Type ls >> out put. This ap pends the re sult of the ls com mand to the out put file. Type cat out put to ver ify.

11. Type ls -R /. This shows a long list of files and fold ers scrolling over your com puter mon i tor. (You might want to press Ctrl-C to stop [or wait some time]).

12. Type ls -R /. | less. This shows the same re sult, but in the less pager, where you can scroll up and down us ing the ar row keys on your key board.

13. Type q to close less. This will also end the ls pro gram.

14. Type ls > /dev/tty1. This gives an er ror mes sage be cause you are ex e cut ing the com mand as an or di nary user, and or di nary users can not ad dress de vice files di rectly (un less you were logged in to tty1). Only the user root has per mis sion to write to de vice files di rectly.

## His tory

A con ve nient fea ture of the Bash shell is the Bash his tory. Bash is con fig ured by de fault to keep the last 1,000 com mands a user used. When a shell ses sion is closed, the his tory of that ses sion is up dated to the his tory file. The name of this file is .bash_his tory and it is cre ated in the home di rec tory of the user who started a spe ‐ cific shell ses sion. No tice that the his tory file is writ ten to only when the shell ses sion is closed; un til that mo ment, all com mands in the his tory are kept in mem ory.

The his tory fea ture makes it easy to re peat com plex com mands. There are sev eral ways of work ing with his tory:

Type his tory to show a list of all com mands in the Bash his tory.

Press Ctrl-r to open the prompt from which you can do back ward searches in com mands that you have pre vi ously used. Just type a string and Bash will look back ward in the com mand his tory for any com mand con tain ing that string as the com mand name or one of its ar gu ments. Press Ctrl-r again to re peat the last back ward search.

Type !num ber to ex e cute a com mand with a spe cific num ber from his tory.

- Use his tory -d num ber to delete a spe cific com mand from his tory. No tice that this com mand will renum ber all other lines in his tory: if you've re moved line 31, the line pre vi ously num bered as line 32 will now be line 31.

- Type !some text to ex e cute the last com mand that starts with some text. No tice that this is a po ten tially dan ger ous com mand be cause the com mand that was found is ex e cuted im me di ately!

' ‐ In some cases it might be nec es sary to wipe the Bash his tory. This ca pa bil ity is use ful, for in stance, if you ve typed a pass word in clear text by ac ci dent. If that hap pens, you can type his tory -c to clear the cur rent his tory. Com mands from this ses sion won't be writ ten to the his tory file when you exit the cur rent ses sion. If you want to re move both the cur rent his tory and the con tents of the .bash_his tory file, then type his tory -w im me di ately af ter run ning the his tory -c com mand. Al ter ‐ na tively, use his tory -d num ber to re move a spe cific com mand from his tory.

1. Make sure that you have opened a shell as user stu dent. 2. Type his tory to get an over view of com mands that you have pre vi ously used. 3. Type some com mands, such as the fol low ing: `ls pwd cat /etc/hosts ls –l` The goal is to fill the his tory a bit. 4. Open a sec ond ter mi nal on your server. To do so, click Ac tiv i ties in the up per-left cor ner, and in the Search bar, type term. Next, click the ter mi nal win dow to start it. ‐ 5. Type his tory from this sec ond ter mi nal win dow. No tice that you do not see the com mands that you just typed in the other ter mi nal. The rea son is that the his tory file has not been up dated yet. 6. From the first ter mi nal ses sion, press Ctrl-r. From the prompt that opens now, type ls. You'll see the last ls com mand you used. Press Ctrl-r again. You'll now see that you are look ing back ward and that the pre vi ous ls com mand is high lighted. Press En ter to ex e cute it. 7. Type his tory | grep cat. The grep com mand searches the his tory out put for any com mands that con tain the text cat. Note the com mand num ber of one of the cat com mands you have pre vi ously used. 8. Type !nn, where nn is re placed by the num ber you noted in step 7. You'll see that the last cat com mand is re peated. 9. Close this ter mi nal by typ ing exit. 10. From the re main ing ter mi nal win dow, type his tory -c. This wipes all his tory that is cur rently in mem ory. Close this ter mi nal ses sion as well. 11. Open a new ter mi nal ses sion and type his tory. The re sult may be a bit un ex pected, but you'll see a list of com mands any way. The rea son is that his tory -c clears the in-mem ory his tory, but it does not re move the .bash_his tory file in your home di rec tory.

## Bash Com ple tion

An other use ful fea ture of the Bash shell is com mand-line com ple tion. This fea ture helps you to find the com mand that you need, and it also works on vari ables and file names.

' ‐ Bash com ple tion is use ful when you re work ing with com mands. Just type the be gin ning of a com mand and press the Tab key. If there is only one op tion for com ple tion, Bash will com plete the com mand au to mat i cally for you. If there are sev eral op tions, you need to press Tab once more to get an over view of all the avail able

51