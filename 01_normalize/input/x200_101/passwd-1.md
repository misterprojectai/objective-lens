# passwd(1) - Linux manual page

[man7.org](../../../index.html) > Linux > [man-pages](../index.html)

[Linux/UNIX system programming training](http://man7.org/training/)

---

# passwd(1) — Linux manual page

[NAME](#NAME) | [SYNOPSIS](#SYNOPSIS) | [DESCRIPTION](#DESCRIPTION) | [OPTIONS](#OPTIONS) | [CAVEATS](#CAVEATS) | [FILES](#FILES) | [EXIT VALUES](#EXIT_VALUES) | [SEE ALSO](#SEE_ALSO) | [COLOPHON](#COLOPHON)

  

_PASSWD_(1)                     User Commands                     _PASSWD_(1)

## [](#NAME)NAME         [top](#top_of_page)

       passwd - change user password

## [](#SYNOPSIS)SYNOPSIS         [top](#top_of_page)

       **passwd** \[_options_\] \[_LOGIN_\]

## [](#DESCRIPTION)DESCRIPTION         [top](#top_of_page)

       The **passwd** command changes passwords for user accounts. A regular
       user can only change the password for their own account, while the
       superuser can change the password for any account. The **passwd** also
       changes the account or associated password validity period.

   **Password Changes**
       If the account has a non-empty password, the user is first
       prompted to enter their current password. The entered password is
       encrypted and compared to the stored value. The user has only one
       attempt to enter the correct password. The superuser can bypass
       this step to allow changing forgotten passwords.

       After the password has been entered, password aging information is
       checked to determine if the user is permitted to change the
       password at this time. If not, **passwd** refuses to change the
       password and exits.

       The user is then prompted twice for a replacement password. The
       second entry is compared against the first and both are required
       to match for the password to be changed.

       Then, the password is tested for complexity.  **passwd** rejects
       passwords that do not meet the complexity requirements. Do not
       include the system default erase or kill characters.

   **Hints for user passwords**
       The security of a password depends on the strength of the
       encryption algorithm and the size of the key space. The legacy
       _UNIX_ System encryption method is based on the NBS DES algorithm.
       More recent methods are now recommended (see **ENCRYPT\_METHOD**). The
       size of the key space depends on the randomness of the selected
       password.

       Compromises in password security normally result from careless
       password selection or handling. For this reason, you should not
       select a password which appears in a dictionary or one that must
       be written down. The password should also not be a proper name,
       your license number, birth date, or street address. Any of these
       may be used as guesses to violate system security.

       As a general guideline, passwords should be long and random. It's
       fine to use simple character sets, such as passwords consisting
       only of lowercase letters, if that helps memorizing longer
       passwords. For a password consisting only of lowercase English
       letters randomly chosen, and a length of 32, there are 26^32
       (approximately 2^150) different possible combinations. Being an
       exponential equation, it's apparent that the exponent (the length)
       is more important than the base (the size of the character set).

       You can find advice on how to choose a strong password on
       [https://en.wikipedia.org/wiki/Password\_strength](https://en.wikipedia.org/wiki/Password_strength)

## [](#OPTIONS)OPTIONS         [top](#top_of_page)

       The options which apply to the **passwd** command are:

       **\-a**, **\--all**
           This option can be used only with **\-S** and causes show status
           for all users.

       **\-d**, **\--delete**
           Deletes a user's password, making it empty. This command sets
           the account to be passwordless.

       **\-e**, **\--expire**
           Immediately expire an account's password. This in effect can
           force a user to change their password at the user's next
           login.

       **\-h**, **\--help**
           Display help message and exit.

       **\-i**, **\--inactive** _INACTIVE_
           This option is used to disable an account after the password
           has been expired for a number of days. After a user account
           has had an expired password for _INACTIVE_ days, the user may no
           longer sign on to the account.

       **\-k**, **\--keep-tokens**
           Indicate password change should be performed only for expired
           authentication tokens (passwords). The user wishes to keep
           their non-expired tokens as before.

       **\-l**, **\--lock**
           Lock the password of the named account. This option disables a
           password by changing it to a value which matches no possible
           encrypted value (it adds a ´!´ at the beginning of the
           password).

           Note that this does not disable the account. The user may
           still be able to login using another authentication token
           (e.g. an SSH key). To disable the account, administrators
           should use **usermod --expiredate 1** (this sets the account's
           expire date to 1970-01-02).

           Users with a locked password are not allowed to change their
           password.

       **\-n**, **\--mindays** _MIN\_DAYS_
           Set the minimum number of days between password changes to
           _MIN\_DAYS_. A value of zero for this field indicates that the
           user may change their password at any time.

       **\-q**, **\--quiet**
           Quiet mode.

       **\-r**, **\--repository** _REPOSITORY_
           change password in _REPOSITORY_ repository

       **\-R**, **\--root** _CHROOT\_DIR_
           Apply changes in the _CHROOT\_DIR_ directory and use the
           configuration files from the _CHROOT\_DIR_ directory. Only
           absolute paths are supported. No SELINUX support.

       **\-P**, **\--prefix** _PREFIX\_DIR_
           Apply changes to configuration files under the root filesystem
           found under the directory _PREFIX\_DIR_. This option does not
           chroot and is intended for preparing a cross-compilation
           target. Some limitations: NIS and LDAP users/groups are not
           verified. No PAM support. No SELINUX support.

       **\-S**, **\--status**
           Display account status information. The status information
           consists of 7 fields. The first field is the user's login
           name. The second field indicates if the user account has a
           locked password (L), has no password (NP), or has a usable
           password (P). The third field gives the date of the last
           password change. The next four fields are the minimum age,
           maximum age, warning period, and inactivity period for the
           password. These ages are expressed in days.

       **\-u**, **\--unlock**
           Unlock the password of the named account. This option
           re-enables a password by changing the password back to its
           previous value (to the value before using the **\-l** option).

       **\-w**, **\--warndays** _WARN\_DAYS_
           Set the number of days of warning before a password change is
           required. The _WARN\_DAYS_ option is the number of days prior to
           password expiration during which the user is warned that their
           password is about to expire.

       **\-x**, **\--maxdays** _MAX\_DAYS_
           Set the maximum number of days a password remains valid. After
           _MAX\_DAYS_, the password is required to be changed.

           Passing the number _\-1_ as _MAX\_DAYS_ will remove checking a
           password's validity.

       **\-s**, **\--stdin**
           This option is used to indicate that passwd should read the
           new password from standard input, which can be a pipe.

## [](#CAVEATS)CAVEATS         [top](#top_of_page)

       Password complexity checking may vary from site to site. The user
       is urged to select a password as complex as he or she feels
       comfortable with.

       Users may not be able to change their password on a system if NIS
       is enabled and they are not logged into the NIS server.

       **passwd** uses PAM to authenticate users and to change their
       passwords.

## [](#FILES)FILES         [top](#top_of_page)

       /etc/passwd
           User account information.

       /etc/shadow
           Secure user account information.

       /etc/pam.d/passwd
           PAM configuration for **passwd**.

## [](#EXIT_VALUES)EXIT VALUES         [top](#top_of_page)

       The **passwd** command exits with the following values:

       _0_
           success

       _1_
           permission denied

       _2_
           invalid combination of options

       _3_
           unexpected failure, nothing done

       _4_
           unexpected failure, passwd file missing

       _5_
           passwd file busy, try again

       _6_
           invalid argument to option

       _10_
           an error was returned by pam(3)

## [](#SEE_ALSO)SEE ALSO         [top](#top_of_page)

       [chpasswd(8)](../man8/chpasswd.8.html), **makepasswd**(1), [passwd(5)](../man5/passwd.5.html), [shadow(5)](../man5/shadow.5.html), [usermod(8)](../man8/usermod.8.html).

       The following web page comically (yet correctly) compares the
       strength of two different methods for choosing a password:
       "https://xkcd.com/936/"

## [](#COLOPHON)COLOPHON         [top](#top_of_page)

       This page is part of the _shadow-utils_ (utilities for managing
       accounts and shadow password files) project.  Information about
       the project can be found at 
       ⟨[https://github.com/shadow-maint/shadow](https://github.com/shadow-maint/shadow)⟩.  If you have a bug report
       for this manual page, send it to
       pkg-shadow-devel@alioth-lists.debian.net.  This page was obtained
       from the tarball shadow-4.19.0.tar fetched from
       ⟨[https://github.com/shadow-maint/shadow/releases](https://github.com/shadow-maint/shadow/releases)⟩ on 2026-01-16.
       If you discover any rendering problems in this HTML version of the
       page, or you believe there is a better or more up-to-date source
       for the page, or you have corrections or improvements to the
       information in this COLOPHON (which is _not_ part of the original
       manual page), send a mail to man-pages@man7.org

shadow-utils 4.19.0             01/16/2026                      _PASSWD_(1)

---

Pages that refer to this page: [ldappasswd(1)](../man1/ldappasswd.1.html),  [login(1)](../man1/login.1.html),  [login(1@@shadow-utils)](../man1/login.1@@shadow-utils.html),  [crypt(3)](../man3/crypt.3.html),  [pts(4)](../man4/pts.4.html),  [login.defs(5)](../man5/login.defs.5.html),  [passwd(5)](../man5/passwd.5.html),  [passwd(5@@shadow-utils)](../man5/passwd.5@@shadow-utils.html),  [shadow(5)](../man5/shadow.5.html),  [chpasswd(8)](../man8/chpasswd.8.html),  [groupadd(8)](../man8/groupadd.8.html),  [groupdel(8)](../man8/groupdel.8.html),  [groupmems(8)](../man8/groupmems.8.html),  [groupmod(8)](../man8/groupmod.8.html),  [newusers(8)](../man8/newusers.8.html),  [useradd(8)](../man8/useradd.8.html),  [userdel(8)](../man8/userdel.8.html),  [usermod(8)](../man8/usermod.8.html)

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