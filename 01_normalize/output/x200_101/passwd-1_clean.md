<!-- Source: 01_normalize/input/passwd-1.md | Cleaned: 2026-05-07 -->

# passwd(1) - Linux manual page

# passwd(1) — Linux manual page

_PASSWD_(1)                     User Commands                     _PASSWD_(1)

passwd - change user password

**passwd** \[_options_\] \[_LOGIN_\]

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

Password complexity checking may vary from site to site. The user
       is urged to select a password as complex as he or she feels
       comfortable with.

Users may not be able to change their password on a system if NIS
       is enabled and they are not logged into the NIS server.

**passwd** uses PAM to authenticate users and to change their
       passwords.

/etc/passwd
           User account information.

/etc/shadow
           Secure user account information.

/etc/pam.d/passwd
           PAM configuration for **passwd**.

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

[chpasswd(8)](../man8/chpasswd.8.html), **makepasswd**(1), [passwd(5)](../man5/passwd.5.html), [shadow(5)](../man5/shadow.5.html), [usermod(8)](../man8/usermod.8.html).