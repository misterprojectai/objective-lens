<!-- Source: 01_normalize/input/x200_102/Learning Modern Linux.pdf | Cleaned: 2026-05-08 -->

Be fore we get into diff er ent op tions and con fig u ra tions, let's fo cus on some ba sic terms such as _ter mi nal_ and _shell_ . In this sec tion I'll de fine the ter mi nol ogy and show you how to ac com plish ev ery day tasks in the shell. We'll also re view mod ern com mands and see them in ac tion.

## **Ter mi nals**

We start with the ter mi nal, or ter mi nal em u la tor, or soft ter mi nal, all of which re fer to the same thing: a _ter mi nal_ is a pro gram that pro vides a tex tual user in ter face. That is, a ter mi nal sup ports read ing char ac ters from the key board and dis play ing them on the screen. Many years ago, these used to be in te grated de vices (key board and screen to ‐ gether), but nowa days ter mi nals are sim ply apps.

In ad di tion to the ba sic char ac ter-ori ented in put and out put, ter mi nals sup port so-called _es cape se quences_ , or _es cape codes_ , for cur sor and screen han dling and po ten tially sup port for col ors. For ex am ple, press ing Ctrl+H causes a backspace, which deletes the char ac ter to the left of the cur sor.

The en vi ron ment vari able TERM has the ter mi nal em u la tor in use, and its con fig u ra tion is avail able via infocmp as fol lows (note that the out put has been short ened):

$ infocmp #       Reconstructed via infocmp from file: /lib/terminfo/s/screen-256color screen-256color|GNU Screen with 256 colors, am, km, mir, msgr, xenl, colors#0x100, cols#80, it#8, lines#24, pairs#0x10000, acsc=++\,\,--..00``aaffgghhiijjkkllmmnnooppqqrrssttuuvvwwxxyyzz{{||}}~~, bel=^G, blink=\E[5m, bold=\E[1m, cbt=\E[Z, civis=\E[?25l, clear=\E[H\E[J, cnorm=\E[34h\E[?25h, cr=\r, ...

The out put of infocmp is not easy to di gest. If you want to learn about the ca pa bil i ties in de tail, con sult the ter ‐ minfo data base. For ex am ple, in my con crete out put, the ter mi nal sup ports 80 col umns ( cols#80 ) and 24 lines ( lines#24 ) for out put as well as 256 col ors ( colors#0x100 , in hexa dec i mal no ta tion).

Ex am ples of ter mi nals in clude not only xterm , rxvt , and the Gnome ter mi na tor but also new gen er a tion ones that uti lize the GPU, such as Alacritty, kitty, and warp.

## **Shells**

Next up is the _shell_ , a pro gram that runs in side the ter mi nal and acts as a com mand in ter preter. The shell off ers in ‐ put and out put han dling via streams, sup ports vari ables, has some built-in com mands you can use, deals with com ‐ mand ex e cu tion and sta tus, and usu ally sup ports both in ter ac tive us age as well as scripted us age ("Script ing").

The shell is for mally de fined in sh , and we of ten come across the term POSIX shell, which will be come more im por ‐ tant in the con text of scripts and porta bil ity.

Orig i nally, we had the Bourne shell sh , named af ter the au thor, but nowa days it's usu ally re placed with the bash shell—a word play on the orig i nal ver sion, short for "Bourne Again Shell"—which is widely used as the de fault.

If you are cu ri ous about what you're us ing, use the file -h /bin/sh com mand to find out, or if that fails, try echo $0 or echo $SHELL .

In this sec tion, we as sume the bash shell ( bash ), un less we call it out ex plic itly.

There are many more im ple men ta tions of sh as well as other vari ants, such as the Korn shell, ksh , and C shell, csh , which are not widely used to day. We will, how ever, re view mod ern bash re place ments in "Hu man-Friendly Shells".

Let's start our shell ba sics with two fun da men tal fea tures: streams and vari ables.

## **Streams**

Let's start with the topic of in put (streams) and out put (streams), or I/O for short. How can you feed a pro gram some in put? How do you con trol where the out put of a pro gram lands, say, on the ter mi nal or in a file?

First off, the shell equips ev ery process with three de fault file de scrip tors (FDs) for in put and out put:

- stdin (FD 0)

- stdout (FD 1)

- stderr (FD 2)

These FDs are, as de picted in Fig ure 3-2, by de fault con nected to your screen and key board, re spec tively. In other words, un less you spec ify some thing else, a com mand you en ter in the shell will take its in put ( stdin ) from your key board, and it will de liver its out put ( stdout ) to your screen.

$ cat This is some input I type on the keyboard and read on the screen^C

In the pre ced ing ex am ple us ing cat , you see the de faults in ac tion. Note that I used Ctrl+C (shown as ^C ) to ter mi nate the com mand.

If you don't want to use the de faults the shell gives you—for ex am ple, you don't want stderr to be out putted on the screen but want to save it in a file—you can re di rect the streams.

You re di rect the out put stream of a process us ing $FD> and <$FD , with $FD be ing the file de scrip tor—for ex am ple, 2> means re di rect the stderr stream. Note that 1> and > are the same since stdout is the de fault. If you want to re di ‐ rect both stdout and stderr , use &> , and when you want to get rid of a stream, you can use /dev/null .

$ curl https://example.com &> /dev/null

$ curl https://example.com > /tmp/content.txt 2> /tmp/curl-status $ head -3 /tmp/content.txt <!doctype html> <html> <head> $ cat /tmp/curl-status % Total % Received % Xferd Average Speed Time Time Time Current Dload Upload Total Spent Left Speed 100 1256 100 1256 0 0 3187 0 --:--:-- --:--:-- --:--:-3195 $ cat > /tmp/interactive-input.txt $ tr < /tmp/curl-status [A-Z] [a-z] % total % received % xferd average speed time time time current dload upload total spent left speed 100 1256 100 1256 0 0 3187 0 --:--:-- --:--:-- --:--:-3195

Dis card all out put by redi rect ing both stdout and stderr to _/dev/null_ . Re di rect the out put and sta tus to diff er ent files.

In ter ac tively en ter in put and save to file; use Ctrl+D to stop cap tur ing and store the con tent. Low er case all words, us ing the tr com mand that reads from stdin .

Shells usu ally un der stand a num ber of spe cial char ac ters, such as:

_Am per sand (_ & _)_

Placed at the end of a com mand, ex e cutes the com mand in the back ground (see also "Job con trol")

## _Back slash (_ \ _)_

Used to con tinue a com mand on the next line, for bet ter read abil ity of long com mands

## _Pipe (_ | _)_

Con nects stdout of one process with the stdin of the next process, al low ing you to pass data with out hav ing to store it in files as a tem po rary place

## **PIPES AND THE UNIX PHI LOS O PHY**

Again, let's see some of the the o ret i cal con tent in ac tion. Let's try to fig ure out how many lines an HTML file con tains by down load ing it us ing curl and then pip ing the con tent to the wc tool:

$ curl https://example.com 2> /dev/null | \ wc -l 46

Use curl to down load the con tent from the URL, and dis card the sta tus that it out puts on stderr . (Note: in prac ‐ tice, you'd use the -s op tion of curl , but we want to learn how to ap ply our hard-gained knowl edge, right?) The stdout of curl is fed to stdin of wc , which counts the num ber of lines with the -l op tion.

Now that you have a ba sic un der stand ing of com mands, streams, and re di rect ion, let's move on to an other core shell fea ture, the han dling of vari ables.

## **Vari ables**

A term you will come across of ten in the con text of shells is _vari ables_ . When ever you don't want to or can not hard ‐ code a value, you can use a vari able to store and change a value. Use cases in clude the fol low ing:

- When you want to han dle con fig u ra tion items that Linux ex poses—for ex am ple, the place where the shell looks for ex e cuta bles cap tured in the $PATH vari able. This is kind of an in ter face where a vari able might be read/write.

- When you want to in ter ac tively query the user for a value, say, in the con text of a script.

- When you want to shorten in put by defin ing a long value once—for ex am ple, the URL of an HTTP API. This use case roughly cor re sponds to a const value in a pro gram lan guage since you don't change the value af ter you have de clared the vari able.

We dis tin guish be tween two kinds of vari ables:

## _En vi ron ment vari ables_

Shell-wide set tings; list them with env .

## _Shell vari ables_

Valid in the con text of the cur rent ex e cu tion; list with set in bash. Shell vari ables are not in her ited by sub pro ‐ cesses.

You can, in bash, use export to cre ate an en vi ron ment vari able. When you want to ac cess the value of a vari able, put a $ in front of it, and when you want to get rid of it, use unset .

$ set MY_VAR=42 $ set | grep MY_VAR _=MY_VAR=42 $ export MY_GLOBAL_VAR="fun with vars" $ set | grep 'MY_*' MY_GLOBAL_VAR='fun with vars' _=MY_VAR=42 $ env | grep 'MY_*' MY_GLOBAL_VAR=fun with vars $ bash $ echo $MY_GLOBAL_VAR fun with vars $ set | grep 'MY_*'

MY_GLOBAL_VAR='fun with vars'

$ exit

$ unset $MY_VAR $ set | grep 'MY_*' MY_GLOBAL_VAR='fun with vars'

Cre ate a shell vari able called MY_VAR , and as sign a value of 42.

List shell vari ables and fil ter out MY_VAR . Note the _= , in di cat ing it's not ex ported.

Cre ate a new en vi ron ment vari able called MY_GLOBAL_VAR .

List shell vari ables and fil ter out all that start with MY_ . We see, as ex pected, both of the vari ables we cre ated in the pre vi ous steps.

List en vi ron ment vari ables. We see MY_GLOBAL_VAR , as we would hope.

Cre ate a new shell ses sion—that is, a child process of the cur rent shell ses sion that doesn't in herit MY_VAR .

Ac cess the en vi ron ment vari able MY_GLOBAL_VAR .

List the shell vari ables, which gives us only MY_GLOBAL_VAR since we're in a child process.

Exit the child process, re move the MY_VAR shell vari able, and list our shell vari ables. As ex pected, MY_VAR is gone.

In Ta ble 3-1 I put to gether com mon shell and en vi ron ment vari ables. You will find those vari ables al most ev ery ‐ where, and they are im por tant to un der stand and to use. For any of the vari ables, you can have a look at the re spec ‐ tive value us ing echo $XXX , with XXX be ing the vari able name.