# date(1) - Linux manual page

[man7.org](../../../index.html) > Linux > [man-pages](../index.html)

[Linux/UNIX system programming training](http://man7.org/training/)

---

# date(1) — Linux manual page

[NAME](#NAME) | [SYNOPSIS](#SYNOPSIS) | [DESCRIPTION](#DESCRIPTION) | [EXAMPLES](#EXAMPLES) | [DATE STRING](#DATE_STRING) | [AUTHOR](#AUTHOR) | [REPORTING BUGS](#REPORTING_BUGS) | [COPYRIGHT](#COPYRIGHT) | [SEE ALSO](#SEE_ALSO) | [COLOPHON](#COLOPHON)

  

_DATE_(1)                       User Commands                       _DATE_(1)

## [](#NAME)NAME         [top](#top_of_page)

       date - print or set the system date and time

## [](#SYNOPSIS)SYNOPSIS         [top](#top_of_page)

       **date** \[_OPTION_\]... \[_+FORMAT_\]
       **date** \[_\-u|--utc|--universal_\] \[_MMDDhhmm_\[\[_CC_\]_YY_\]\[_.ss_\]\]

## [](#DESCRIPTION)DESCRIPTION         [top](#top_of_page)

       Display date and time in the given FORMAT.  With **\-s**, or with
       \[MMDDhhmm\[\[CC\]YY\]\[.ss\]\], set the date and time.

       Mandatory arguments to long options are mandatory for short
       options too.

       **\-d**, **\--date**\=_STRING_
              display time described by STRING, not 'now'

       **\--debug**
              annotate the parsed date, and warn about questionable usage
              to standard error

       **\-f**, **\--file**\=_DATEFILE_
              like **\--date**; once for each line of DATEFILE

       **\-I**\[_FMT_\], **\--iso-8601**\[=_FMT_\]
              output date/time in ISO 8601 format.  FMT='date' for date
              only (the default), 'hours', 'minutes', 'seconds', or 'ns'
              for date and time to the indicated precision.  Example:
              2006-08-14T02:34:56-06:00

       **\--resolution**
              output the available resolution of timestamps Example:
              0.000000001

       **\-R**, **\--rfc-email**
              output date and time in RFC 5322 format.  Example: Mon, 14
              Aug 2006 02:34:56 **\-0600**

       **\--rfc-3339**\=_FMT_
              output date/time in RFC 3339 format.  FMT='date',
              'seconds', or 'ns' for date and time to the indicated
              precision.  Example: 2006-08-14 02:34:56-06:00

       **\-r**, **\--reference**\=_FILE_
              display the last modification time of FILE

       **\-s**, **\--set**\=_STRING_
              set time described by STRING

       **\-u**, **\--utc**, **\--universal**
              print or set Coordinated Universal Time (UTC)

       **\--help** display this help and exit

       **\--version**
              output version information and exit

       All options that specify the date to display are mutually
       exclusive.  I.e.: **\--date**, **\--file**, **\--reference**, **\--resolution**.

       FORMAT controls the output.  Interpreted sequences are:

       %%     a literal %

       %a     locale's abbreviated weekday name (e.g., Sun)

       %A     locale's full weekday name (e.g., Sunday)

       %b     locale's abbreviated month name (e.g., Jan)

       %B     locale's full month name (e.g., January)

       %c     locale's date and time (e.g., Thu Mar  3 23:05:25 2005)

       %C     century; like %Y, except omit last two digits (e.g., 20)

       %d     day of month (e.g., 01)

       %D     date (ambiguous); same as %m/%d/%y

       %e     day of month, space padded; same as %\_d

       %F     full date; like %+4Y-%m-%d

       %g     last two digits of year of ISO week number (ambiguous;
              00-99); see %G

       %G     year of ISO week number; normally useful only with %V

       %h     same as %b

       %H     hour (00..23)

       %I     hour (01..12)

       %j     day of year (001..366)

       %k     hour, space padded ( 0..23); same as %\_H

       %l     hour, space padded ( 1..12); same as %\_I

       %m     month (01..12)

       %M     minute (00..59)

       %n     a newline

       %N     nanoseconds (000000000..999999999)

       %p     locale's equivalent of either AM or PM; blank if not known

       %P     like %p, but lower case

       %q     quarter of year (1..4)

       %r     locale's 12-hour clock time (e.g., 11:11:04 PM)

       %R     24-hour hour and minute; same as %H:%M

       %s     seconds since the Epoch (1970-01-01 00:00 UTC)

       %S     second (00..60)

       %t     a tab

       %T     time; same as %H:%M:%S

       %u     day of week (1..7); 1 is Monday

       %U     week number of year, with Sunday as first day of week
              (00..53)

       %V     ISO week number, with Monday as first day of week (01..53)

       %w     day of week (0..6); 0 is Sunday

       %W     week number of year, with Monday as first day of week
              (00..53)

       %x     locale's date (can be ambiguous; e.g., 12/31/99)

       %X     locale's time representation (e.g., 23:13:48)

       %y     last two digits of year (ambiguous; 00..99)

       %Y     year

       %z     +hhmm numeric time zone (e.g., **\-0400**)

       %:z    +hh:mm numeric time zone (e.g., **\-04**:00)

       %::z   +hh:mm:ss numeric time zone (e.g., **\-04**:00:00)

       %:::z  numeric time zone with : to necessary precision (e.g., **\-04**,
              +05:30)

       %Z     alphabetic time zone abbreviation (e.g., EDT)

       By default, date pads numeric fields with zeroes.  The following
       optional flags may follow '%':

       -      (hyphen) do not pad the field

       \_      (underscore) pad with spaces

       0      (zero) pad with zeros

       +      pad with zeros, and put '+' before future years with >4
              digits

       ^      use upper case if possible

       #      use opposite case if possible

       After any flags comes an optional field width, as a decimal
       number; then an optional modifier, which is either E to use the
       locale's alternate representations if available, or O to use the
       locale's alternate numeric symbols if available.

## [](#EXAMPLES)EXAMPLES         [top](#top_of_page)

       Convert seconds since the Epoch (1970-01-01 UTC) to a date

              $ date --date='@2147483647'

       Show the time on the west coast of the US (use **tzselect**(1) to find
       TZ)

              $ TZ='America/Los\_Angeles' date

       Show the local time for 9AM next Friday on the west coast of the
       US

              $ date --date='TZ="America/Los\_Angeles" 09:00 next Fri'

## [](#DATE_STRING)DATE STRING         [top](#top_of_page)

       The --date=STRING is a mostly free format human readable date
       string such as "Sun, 29 Feb 2004 16:21:42 -0800" or "2004-02-29
       16:21:42" or even "next Thursday".  A date string may contain
       items indicating calendar date, time of day, time zone, day of
       week, relative time, relative date, and numbers.  An empty string
       indicates the beginning of the day.  The date string format is
       more complex than is easily documented here but is fully described
       in the info documentation.

## [](#AUTHOR)AUTHOR         [top](#top_of_page)

       Written by David MacKenzie.

## [](#REPORTING_BUGS)REPORTING BUGS         [top](#top_of_page)

       Report bugs to: bug-coreutils@gnu.org
       GNU coreutils home page: <[https://www.gnu.org/software/coreutils/](https://www.gnu.org/software/coreutils/)\>
       General help using GNU software: <[https://www.gnu.org/gethelp/](https://www.gnu.org/gethelp/)\>
       Report any translation bugs to
       <[https://translationproject.org/team/](https://translationproject.org/team/)\>

## [](#COPYRIGHT)COPYRIGHT         [top](#top_of_page)

       Copyright © 2025 Free Software Foundation, Inc.  License GPLv3+:
       GNU GPL version 3 or later <[https://gnu.org/licenses/gpl.html](https://gnu.org/licenses/gpl.html)\>.
       This is free software: you are free to change and redistribute it.
       There is NO WARRANTY, to the extent permitted by law.

## [](#SEE_ALSO)SEE ALSO         [top](#top_of_page)

       Full documentation <[https://www.gnu.org/software/coreutils/date](https://www.gnu.org/software/coreutils/date)\>
       or available locally via: info '(coreutils) date invocation'

## [](#COLOPHON)COLOPHON         [top](#top_of_page)

       This page is part of the _coreutils_ (basic file, shell and text
       manipulation utilities) project.  Information about the project
       can be found at ⟨[http://www.gnu.org/software/coreutils/](http://www.gnu.org/software/coreutils/)⟩.  If you
       have a bug report for this manual page, see
       ⟨[http://www.gnu.org/software/coreutils/](http://www.gnu.org/software/coreutils/)⟩.  This page was obtained
       from the tarball coreutils-9.9.tar.xz fetched from
       ⟨[http://ftp.gnu.org/gnu/coreutils/](http://ftp.gnu.org/gnu/coreutils/)⟩ on 2026-01-16.  If you
       discover any rendering problems in this HTML version of the page,
       or you believe there is a better or more up-to-date source for the
       page, or you have corrections or improvements to the information
       in this COLOPHON (which is _not_ part of the original manual page),
       send a mail to man-pages@man7.org

GNU coreutils 9.9             November 2025                       _DATE_(1)

---

Pages that refer to this page: [cronnext(1)](../man1/cronnext.1.html),  [dir(1)](../man1/dir.1.html),  [gawk(1)](../man1/gawk.1.html),  [locale(1)](../man1/locale.1.html),  [ls(1)](../man1/ls.1.html),  [pmdashping(1)](../man1/pmdashping.1.html),  [pmdate(1)](../man1/pmdate.1.html),  [timedatectl(1)](../man1/timedatectl.1.html),  [vdir(1)](../man1/vdir.1.html),  [clock\_getres(2)](../man2/clock_getres.2.html),  [gettimeofday(2)](../man2/gettimeofday.2.html),  [stime(2)](../man2/stime.2.html),  [time(2)](../man2/time.2.html),  [ctime(3)](../man3/ctime.3.html),  [difftime(3)](../man3/difftime.3.html),  [posix\_spawn(3)](../man3/posix_spawn.3.html),  [strftime(3)](../man3/strftime.3.html),  [tzset(3)](../man3/tzset.3.html),  [rtc(4)](../man4/rtc.4.html),  [crontab(5)](../man5/crontab.5.html),  [locale(5)](../man5/locale.5.html),  [utmp(5)](../man5/utmp.5.html),  [lvmreport(7)](../man7/lvmreport.7.html),  [rpm-macros(7)](../man7/rpm-macros.7.html),  [time(7)](../man7/time.7.html),  [hwclock(8)](../man8/hwclock.8.html),  [rtcwake(8)](../man8/rtcwake.8.html)

---

---

HTML rendering created 2026-01-16 by [Michael Kerrisk](https://man7.org/mtk/index.html), author of [_The Linux Programming Interface_](https://man7.org/tlpi/).

For details of in-depth **Linux/UNIX system programming training courses** that I teach, look [here](https://man7.org/training/).

Hosting by [jambit GmbH](https://www.jambit.com/index_en.html).

[![Cover of TLPI](https://man7.org/tlpi/cover/TLPI-front-cover-vsmall.png)](https://man7.org/tlpi/)

---

[![Web Analytics Made Easy -
StatCounter](https://c.statcounter.com/7422636/0/9b6714ff/1/)](https://statcounter.com/ "Web Analytics
Made Easy - StatCounter")