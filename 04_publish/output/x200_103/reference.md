---
description: Complete syntax, options, flags, regular expression metacharacters, and exit codes for the GNU grep utility and BRE/ERE/PCRE pattern dialects.
icon: brackets-curly
---

# grep and Regular Expressions Reference

{% hint style="info" %}
This reference covers GNU `grep` as shipped on RHEL 8/9 (GNU grep 3.1+), exam objective x200\_103. All BRE, ERE, and PCRE syntax, every flag, environment variable, and exit code is documented here for fast lookup while working.
{% endhint %}

## Command Syntax

{% code title="Syntax" %}
```
grep [OPTIONS] PATTERN [FILE...]
grep [OPTIONS] -e PATTERN ... [FILE...]
grep [OPTIONS] -f PATTERNFILE ... [FILE...]
```
{% endcode %}

`FILE` may be `-` to denote standard input. When no `FILE` is given and no recursion option is active, `grep` reads standard input. When multiple files are searched, each output line is prefixed with the filename.

---

## Pattern Dialect Options

| Option | Long Form | Description |
|---|---|---|
| *(default)* | `--basic-regexp` | Interprets patterns as BRE. |
| `-E` | `--extended-regexp` | Interprets patterns as ERE. |
| `-F` | `--fixed-strings` | Interprets patterns as literal fixed strings — not regular expressions. |
| `-P` | `--perl-regexp` | Interprets patterns as PCRE. Availability depends on compile-time options. |

{% hint style="warning" %}
`-P` (PCRE) availability depends on whether `grep` was compiled with PCRE2 support. Availability varies by distribution build.
{% endhint %}

---

## Options and Flags

<details>

<summary>Pattern and Input Control</summary>

| Option | Long Form | Description |
|---|---|---|
| `-e PATTERN` | `--regexp=PATTERN` | Specifies a pattern. Multiple `-e` options are ORed; a line matching any pattern is selected. |
| `-f FILE` | `--file=FILE` | Reads patterns from `FILE`, one per line. Combinable with `-e`. An empty file matches nothing. |
| `-i` | `--ignore-case` | Pattern and input characters that differ only in case are treated as identical. |
| `-v` | `--invert-match` | Selects lines that do *not* match the pattern. |
| `-w` | `--word-regexp` | Selects only matches that form complete words; bounded by non-word characters or line edges. |
| `-x` | `--line-regexp` | Selects only matches spanning the entire line. Equivalent to anchoring with `^` and `$`. |

</details>

<details>

<summary>Output Control</summary>

| Option | Long Form | Description |
|---|---|---|
| `-c` | `--count` | Suppresses normal output; prints a count of matching lines per file. With `-v`, counts non-matching lines. |
| `-l` | `--files-with-matches` | Prints only the names of files containing at least one match. Stops scanning each file at first match. |
| `-L` | `--files-without-match` | Prints only the names of files containing no matching lines. |
| `-o` | `--only-matching` | Prints only the matched portion of each line, one match per output line. |
| `-q` | `--quiet` / `--silent` | Produces no output; exits with status 0 on first match, 1 if no match. |
| `-s` | `--no-messages` | Suppresses error messages about nonexistent or unreadable files. |
| `-m NUM` | `--max-count=NUM` | Stops after `NUM` selected lines. |
| `-n` | `--line-number` | Prefixes each output line with its 1-based line number within the input file. |
| `-b` | `--byte-offset` | Prefixes each output line with its 0-based byte offset within the input file. |
| `-H` | `--with-filename` | Forces filename prefix on output even when searching a single file. |
| `-h` | `--no-filename` | Suppresses filename prefix on output. Default when searching a single file. |
| `--color[=WHEN]` | `--colour[=WHEN]` | Highlights matched text. `WHEN` is `always`, `never`, or `auto`. |

</details>

<details>

<summary>Context Lines</summary>

| Option | Long Form | Description |
|---|---|---|
| `-A NUM` | `--after-context=NUM` | Prints `NUM` lines of trailing context after each matching line. |
| `-B NUM` | `--before-context=NUM` | Prints `NUM` lines of leading context before each matching line. |
| `-C NUM` | `--context=NUM` | Prints `NUM` lines of context both before and after. Equivalent to `-A NUM -B NUM`. |

Context groups are separated by `--` in output. `-o` disables context options.

</details>

<details>

<summary>File and Directory Selection</summary>

| Option | Long Form | Description |
|---|---|---|
| `-r` | `--recursive` | Reads all files under each specified directory recursively. Follows command-line symlinks; skips recursive symlinks. |
| `-R` | `--dereference-recursive` | Like `-r` but follows all symbolic links. |
| `--include=GLOB` | | Restricts recursive search to files matching `GLOB`. |
| `--exclude=GLOB` | | Skips files matching `GLOB` during recursive search. |
| `-a` | `--binary-files=text` | Processes binary files as if they were text. |
| `-I` | `--binary-files=without-match` | Ignores binary files (treats them as containing no matches). |

</details>

---

## Regular Expression Syntax

### Special Characters

The following characters have special meaning in regular expressions and must be escaped to be treated as literals:

`. ? * + { | ( ) [ \ ^ $`

All other characters are ordinary and match themselves.

### Anchors

| Pattern | Description |
|---|---|
| `^` | Matches the empty string at the beginning of a line. |
| `$` | Matches the empty string at the end of a line. |
| `^$` | Matches an empty line. |

### Wildcard

| Pattern | Description |
|---|---|
| `.` | Matches any single character except newline. |

### Quantifiers

Quantifiers apply to the immediately preceding item (character, group, or bracket expression). Quantifiers are **greedy** by default. In PCRE, appending `?` to a quantifier makes it lazy: `*?`, `+?`, `??`, `{n,m}?`.

**Precedence:** repetition > concatenation > alternation.

| Quantifier | BRE Form | ERE/PCRE Form | Description |
|---|---|---|---|
| Zero or more | `*` | `*` | Preceding item matched zero or more times. |
| One or more | `\+` | `+` | Preceding item matched one or more times. |
| Zero or one | `\?` | `?` | Preceding item matched zero or one time. |
| Exactly n | `\{n\}` | `{n}` | Preceding item matched exactly `n` times. |
| n or more | `\{n,\}` | `{n,}` | Preceding item matched `n` or more times. |
| At most m | `\{,m\}` | `{,m}` | Preceding item matched at most `m` times. GNU extension. |
| Between n and m | `\{n,m\}` | `{n,m}` | Preceding item matched at least `n` and at most `m` times. |

{% hint style="warning" %}
An interval expression repetition count greater than 32767 is invalid.
{% endhint %}

### Bracket Expressions

| Syntax | Description |
|---|---|
| `[abc]` | Matches any single character listed. |
| `[^abc]` | Matches any single character *not* listed. |
| `[a-z]` | Matches any single character in the range `a` through `z` (ASCII order in C locale). |
| `[0-9]` | Matches any single decimal digit. |

Special characters lose their special meaning inside bracket expressions. To include `]`, place it first. To include `-`, place it first or last.

{% hint style="warning" %}
Range expressions such as `[a-z]` are locale-dependent. In locales other than C/POSIX their behavior is unspecified. Use POSIX named classes (`[[:lower:]]`) for portable matching.
{% endhint %}

### POSIX Named Character Classes

Used inside bracket expressions as `[[:class:]]`.

| Class | Equivalent (C locale) | Description |
|---|---|---|
| `[:alnum:]` | `[0-9A-Za-z]` | Alphanumeric characters. |
| `[:alpha:]` | `[A-Za-z]` | Alphabetic characters. |
| `[:digit:]` | `[0-9]` | Decimal digits. |
| `[:lower:]` | `[a-z]` | Lowercase letters. |
| `[:upper:]` | `[A-Z]` | Uppercase letters. |
| `[:space:]` | `[ \t\n\r\f\v]` | Whitespace characters. |
| `[:blank:]` | `[ \t]` | Space and tab. |
| `[:punct:]` | Printing chars excluding alnum and space | Punctuation characters. |
| `[:graph:]` | `[:alnum:]` + `[:punct:]` | Graphical (visible) characters. |
| `[:print:]` | `[:graph:]` + space | Printable characters including space. |
| `[:xdigit:]` | `[0-9A-Fa-f]` | Hexadecimal digits. |
| `[:cntrl:]` | | Control characters. |

### Alternation and Grouping

| Syntax | Dialect | Description |
|---|---|---|
| `a\|b` | BRE | Matches either `a` or `b`. |
| `a\|b` | ERE | In ERE the backslash is not used: write `a\|b` as `a|b`. |
| `\(expr\)` | BRE | Groups subexpression. |
| `(expr)` | ERE/PCRE | Groups subexpression. |

### Backreferences

| Syntax | Description |
|---|---|
| `\1` … `\9` | Matches the substring captured by the *n*th parenthesized group. Supported in BRE and PCRE; not standard in ERE. |

{% code title="Example — BRE backreference" %}
```bash
# Matches lines containing a doubled word (e.g. "the the")
grep '\(\b[a-z]*\b\) \1' file.txt

# Matches "aa" using backreference
echo 'aa' | grep '\(a\)\1'
```
{% endcode %}

### GNU Backslash Extensions

| Expression | Description |
|---|---|
| `\b` | Matches the empty string at a word boundary. |
| `\B` | Matches the empty string not at a word boundary. |
| `\<` | Matches the empty string at the beginning of a word. |
| `\>` | Matches the empty string at the end of a word. |
| `\w` | Matches a word constituent character. Synonym for `[_[:alnum:]]`. |
| `\W` | Matches a non-word constituent character. Synonym for `[^_[:alnum:]]`. |
| `\s` | Matches whitespace. Synonym for `[[:space:]]`. |
| `\S` | Matches non-whitespace. Synonym for `[^[:space:]]`. |

### BRE vs. ERE Differences

In BRE, the characters `? + { | ( )` are treated as literals unless backslash-escaped. In ERE, these characters are metacharacters and must be backslash-escaped to be treated as literals.

| Feature | BRE syntax | ERE syntax |
|---|---|---|
| Zero or one | `\?` | `?` |
| One or more | `\+` | `+` |
| Alternation | `\|` | `\|` |
| Grouping | `\(…\)` | `(…)` |
| Interval | `\{n,m\}` | `{n,m}` |

{% hint style="warning" %}
BRE backreferences (`\1`–`\9`) are supported. ERE backreferences are not POSIX-portable.
{% endhint %}

---

## Files and Paths

| Path | Purpose |
|---|---|
| `/usr/bin/grep` | `grep` binary. |
| `/usr/bin/egrep` | Legacy wrapper; equivalent to `grep -E`. |
| `/usr/bin/fgrep` | Legacy wrapper; equivalent to `grep -F`. |
| `/usr/share/doc/grep/` | Package documentation directory. |

{% hint style="warning" %}
`egrep` and `fgrep` are deprecated since GNU grep 2.5.3; obsolescence warnings have been issued since GNU grep 3.8. Both may be removed in future releases. Use `grep -E` and `grep -F` instead.
{% endhint %}

---

## Environment Variables

| Variable | Effect on grep |
|---|---|
| `LC_ALL` | Overrides all locale categories. Affects character range interpretation in bracket expressions. |
| `LC_COLLATE` | Governs collation order for range expressions such as `[a-z]`. |
| `LC_CTYPE` | Governs character classification for POSIX named classes such as `[:alpha:]`. |
| `LANG` | Default locale when `LC_ALL` and category-specific variables are unset. |
| `GREP_COLORS` | Defines terminal color codes for highlighted output. Default: `ms=01;31:mc=01;31:sl=:cx=:fn=35:ln=32:bn=32:se=36`. |
| `GREP_OPTIONS` | **Deprecated.** Default options prepended to every invocation. Removed in GNU grep 3.3. |

{% hint style="danger" %}
`GREP_OPTIONS` was removed in GNU grep 3.3. Scripts relying on it will silently lose options on RHEL 8/9 systems. Use shell aliases or wrapper scripts instead.
{% endhint %}

---

## Exit Codes

| Code | Meaning |
|---|---|
| `0` | At least one matching line was found. |
| `1` | No matching lines were found. |
| `2` | An error occurred (nonexistent file, invalid pattern, permission denied). |

{% hint style="info" %}
When `-q` is active and a match is found, exit status is `0` even if an error also occurred.
{% endhint %}

---

## Examples

{% tabs %}
{% tab title="Basic Matching" %}
```bash
# Search for a literal string in a file
grep 'root' /etc/passwd

# Case-insensitive search through kernel messages
dmesg | grep -i eth

# Lines starting with a pattern (BRE anchor)
grep '^anna' /etc/passwd

# Lines ending with a pattern (BRE anchor)
grep 'bash$' /etc/passwd

# Invert match: lines that do not start with #
grep -v '^#' /etc/services

# Whole-word match
grep -w 'root' /etc/passwd

# Match empty lines only
grep '^$' /etc/services
```
{% endtab %}

{% tab title="ERE and Multiple Patterns" %}
```bash
# Extended regular expression: match either of two patterns
grep -E 'eth[0-9]|enp[0-9]' /var/log/messages

# Multiple explicit patterns (additive OR)
grep -e 'eth[0-9]' -e 'enp0' /var/log/messages

# ERE interval: match lines with exactly two digits
grep -E '[0-9]{2}' /etc/passwd
```
{% endtab %}

{% tab title="Output Control" %}
```bash
# Count matching lines per file
grep -c 'error' /var/log/messages

# Print only filenames containing a match (recursive)
grep -rl 'PermitRootLogin' /etc/ssh/

# Show 3 lines of trailing context after each match
grep -A 3 'Failed password' /var/log/secure

# Suppress binary-file noise
grep -I 'pattern' /usr/bin/*
```
{% endtab %}

{% tab title="Recursive and Character Classes" %}
```bash
# Recursive search with filename prefix
grep -r 'max_connections' /etc/

# Bracket expression: match eth0 through eth9
grep 'eth[0-9]' /var/log/messages

# POSIX character class: lines beginning with a digit
grep '^[[:digit:]]' /etc/services
```
{% endtab %}
{% endtabs %}

---

## Constraints and Gotchas

| Constraint | Detail |
|---|---|
| Pattern anchoring | A pattern matches anywhere within a line unless `-x` is used or `^`/`$` anchors are explicit. |
| Newline in patterns | Newline characters cannot be matched within a pattern — newline is the line separator and also separates patterns in `-e` and `-f`. |
| Filename prefix | With multiple files: filename prefix shown. With a single file or stdin: suppressed unless `-H` is given. |
| Empty pattern | A pattern consisting solely of the empty string matches every line. Behavior under POSIX is unspecified. Use `^$` to match empty lines explicitly. |
| Null bytes | When `grep` encounters a file containing null bytes it treats the file as binary and suppresses match details unless `-a` or `--binary-files=text` is specified. |
| Locale and ranges | Range expressions like `[a-z]` are locale-dependent. Use `[[:lower:]]` for portability. |
| Interval limit | A repetition count greater than 32767 in an interval expression `{n,m}` is invalid. |
| BRE backrefs | BRE backreferences `\1`–`\9` are supported; ERE backreferences are not POSIX-portable. |
| PCRE availability | `-P` requires `grep` compiled with PCRE2 support — not guaranteed on all builds. |
| Platform | Requires RHEL 8 / RHEL 9 (GNU grep 3.1 or later). |

---

## See Also

| Resource | Description |
|---|---|
| `man grep` | Full GNU grep manual — all options, regex syntax, environment variables. |
| `man 7 regex` | POSIX regular expression specification. |
| `man pcre2syntax` | PCRE2 pattern syntax (relevant to `grep -P`). |
| `man pcre2pattern` | PCRE2 pattern semantics. |
| `sed` | Stream editor; uses ERE for substitution and address matching. |
| `awk` | Pattern-scanning and processing language; uses ERE. |