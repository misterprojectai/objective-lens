---
title: "grep and Regular Expressions Reference"
type: reference
quadrant:
  practical_theoretical: theoretical
  work_study: work
exam_objective: "x200_103"
version: "1.0"
status: draft
---

# grep and Regular Expressions Reference

`grep` is a line-filtering utility that reads input line by line, evaluates each line against one or more patterns, and writes matching lines to standard output.

---

## Overview

`grep` belongs to the GNU core utilities package (`grep`) and is installed by default on all RHEL-family distributions. It accepts patterns as basic regular expressions (BRE) by default; the `-E`, `-F`, and `-P` flags select alternative pattern dialects. Input may be one or more files, standard input, or a pipeline. Output is the set of lines from the input that match — or, with `-v`, the set that do not match.

Regular expressions (regex) are formal patterns that describe sets of strings. GNU `grep` supports three regex dialects: BRE, ERE, and PCRE. BRE and ERE differ only in metacharacter syntax; PCRE provides a distinct, richer feature set.

---

## Syntax

```
grep [OPTIONS] PATTERN [FILE...]
grep [OPTIONS] -e PATTERN ... [FILE...]
grep [OPTIONS] -f PATTERNFILE ... [FILE...]
```

`FILE` may be `-` to denote standard input. When no `FILE` is given and no recursion option is active, `grep` reads standard input. When multiple files are searched, each output line is prefixed with the filename.

---

## Pattern Dialect Options

| Option | Long Form | Description |
|---|---|---|
| *(default)* | `--basic-regexp` | Interprets patterns as BRE. |
| `-E` | `--extended-regexp` | Interprets patterns as ERE. |
| `-F` | `--fixed-strings` | Interprets patterns as literal fixed strings, not regular expressions. |
| `-P` | `--perl-regexp` | Interprets patterns as PCRE. Availability depends on compile-time options. |

---

## Options / Flags

### Pattern and Input Control

| Option | Long Form | Description |
|---|---|---|
| `-e PATTERN` | `--regexp=PATTERN` | Specifies a pattern. Multiple `-e` options are ORed; a line matching any pattern is selected. |
| `-f FILE` | `--file=FILE` | Reads patterns from `FILE`, one per line. Combinable with `-e`. An empty file matches nothing. |
| `-i` | `--ignore-case` | Pattern and input characters that differ only in case are treated as identical. |
| `-v` | `--invert-match` | Selects lines that do *not* match the pattern. |
| `-w` | `--word-regexp` | Selects only matches that form complete words; the match must be bounded by non-word characters or line edges. |
| `-x` | `--line-regexp` | Selects only matches that span the entire line. Equivalent to anchoring the pattern with `^` and `$`. |

### Output Control

| Option | Long Form | Description |
|---|---|---|
| `-c` | `--count` | Suppresses normal output; prints a count of matching lines per file. With `-v`, counts non-matching lines. |
| `-l` | `--files-with-matches` | Prints only the names of files that contain at least one match. Stops scanning each file at first match. |
| `-L` | `--files-without-match` | Prints only the names of files that contain no matching lines. |
| `-o` | `--only-matching` | Prints only the matched portion of each line, one match per output line. |
| `-q` | `--quiet` / `--silent` | Produces no output; exits with status 0 on first match, 1 if no match. |
| `-s` | `--no-messages` | Suppresses error messages about nonexistent or unreadable files. |
| `-m NUM` | `--max-count=NUM` | Stops after `NUM` selected lines. |
| `-n` | `--line-number` | Prefixes each output line with its 1-based line number within the input file. |
| `-b` | `--byte-offset` | Prefixes each output line with its 0-based byte offset within the input file. |
| `-H` | `--with-filename` | Forces filename prefix on output even when searching a single file. |
| `-h` | `--no-filename` | Suppresses filename prefix on output. Default when searching a single file. |
| `--color[=WHEN]` | `--colour[=WHEN]` | Highlights matched text using terminal escape sequences. `WHEN` is `always`, `never`, or `auto`. |

### Context Lines

| Option | Long Form | Description |
|---|---|---|
| `-A NUM` | `--after-context=NUM` | Prints `NUM` lines of trailing context after each matching line. |
| `-B NUM` | `--before-context=NUM` | Prints `NUM` lines of leading context before each matching line. |
| `-C NUM` | `--context=NUM` | Prints `NUM` lines of context both before and after each matching line. Equivalent to `-A NUM -B NUM`. |

Context groups are separated by `--` in output. `-o` disables context options.

### File and Directory Selection

| Option | Long Form | Description |
|---|---|---|
| `-r` | `--recursive` | Reads all files under each specified directory recursively. Follows command-line symlinks; skips recursive symlinks. |
| `-R` | `--dereference-recursive` | Like `-r` but follows all symbolic links. |
| `--include=GLOB` | | Restricts recursive search to files matching `GLOB`. |
| `--exclude=GLOB` | | Skips files matching `GLOB` during recursive search. |
| `-a` | `--binary-files=text` | Processes binary files as if they were text. |
| `-I` | `--binary-files=without-match` | Ignores binary files (treats them as containing no matches). |

---

## Regular Expression Syntax

### Special Characters

The following characters have special meaning in regular expressions: `. ? * + { | ( ) [ \ ^ $`

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

### Quantifiers (Repetition Operators)

Quantifiers apply to the immediately preceding item (character, group, or bracket expression).

| Quantifier | Description |
|---|---|
| `*` | Preceding item matched zero or more times. |
| `+` | Preceding item matched one or more times. (ERE/PCRE; BRE: `\+`) |
| `?` | Preceding item matched zero or one time. (ERE/PCRE; BRE: `\?`) |
| `{n}` | Preceding item matched exactly `n` times. (ERE/PCRE; BRE: `\{n\}`) |
| `{n,}` | Preceding item matched `n` or more times. (ERE/PCRE; BRE: `\{n,\}`) |
| `{,m}` | Preceding item matched at most `m` times. GNU extension. |
| `{n,m}` | Preceding item matched at least `n` and at most `m` times. |

Quantifiers are greedy by default (match as much as possible). In PCRE, appending `?` to a quantifier makes it lazy (match as little as possible): `*?`, `+?`, `??`, `{n,m}?`.

**Precedence:** repetition > concatenation > alternation.

### Bracket Expressions (Character Classes)

| Syntax | Description |
|---|---|
| `[abc]` | Matches any single character listed. |
| `[^abc]` | Matches any single character *not* listed. |
| `[a-z]` | Matches any single character in the range `a` through `z` (ASCII order in C locale). |
| `[0-9]` | Matches any single decimal digit. |

Special characters lose their special meaning inside bracket expressions. To include `]`, place it first. To include `-`, place it first or last.

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

| Syntax | Description |
|---|---|
| `a\|b` | Matches either `a` or `b`. (BRE) |
| `a\|b` → `a|b` | In ERE, the backslash is not used: `a|b`. |
| `\(expr\)` | Groups subexpression in BRE. |
| `(expr)` | Groups subexpression in ERE/PCRE. |

### Backreferences

| Syntax | Description |
|---|---|
| `\n` | Matches the substring matched by the *n*th parenthesized group (where *n* is 1–9). Supported in BRE and PCRE; not standard in ERE. |

Example: `\(a\)\1` matches `aa` in BRE.

### Special Backslash Expressions (GNU Extension)

| Expression | Description |
|---|---|
| `\b` | Matches the empty string at a word boundary (edge of a word). |
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

---

## Files and Paths

| Path | Purpose |
|---|---|
| `/usr/bin/grep` | `grep` binary. |
| `/usr/bin/egrep` | Legacy wrapper; equivalent to `grep -E`. Deprecated since GNU grep 2.5.3; obsolescence warnings issued since GNU grep 3.8. |
| `/usr/bin/fgrep` | Legacy wrapper; equivalent to `grep -F`. Deprecated on the same schedule as `egrep`. |
| `/usr/share/doc/grep/` | Package documentation directory. |

---

## Environment Variables

| Variable | Effect on grep |
|---|---|
| `LC_ALL` | Overrides all locale categories. Affects character range interpretation in bracket expressions. |
| `LC_COLLATE` | Governs collation order for range expressions such as `[a-z]`. |
| `LC_CTYPE` | Governs character classification for POSIX named classes such as `[:alpha:]`. |
| `LANG` | Default locale when `LC_ALL` and category-specific variables are unset. |
| `GREP_COLORS` | Defines terminal color codes for highlighted output. Default: `ms=01;31:mc=01;31:sl=:cx=:fn=35:ln=32:bn=32:se=36`. |
| `GREP_OPTIONS` | (*Deprecated.*) Default command-line options prepended to every `grep` invocation. Removed in GNU grep 3.3. |

---

## Exit Codes

| Code | Meaning |
|---|---|
| `0` | At least one matching line was found. |
| `1` | No matching lines were found. |
| `2` | An error occurred (e.g., nonexistent file, invalid pattern, permission denied). |

When `-q` is active and a match is found, exit status is `0` even if an error also occurred.

---

## Examples

```bash
# Search for a literal string in a file
grep 'root' /etc/passwd
```

```bash
# Case-insensitive search through kernel messages
dmesg | grep -i eth
```

```bash
# Lines starting with the pattern (BRE anchor)
grep '^anna' /etc/passwd
```

```bash
# Lines ending with the pattern (BRE anchor)
grep 'bash$' /etc/passwd
```

```bash
# Invert match: lines that do not start with #
grep -v '^#' /etc/services
```

```bash
# Extended regular expression: match either of two patterns
grep -E 'eth[0-9]|enp[0-9]' /var/log/messages
```

```bash
# Multiple explicit patterns (additive OR)
grep -e 'eth[0-9]' -e 'enp0' /var/log/messages
```

```bash
# Whole-word match
grep -w 'root' /etc/passwd
```

```bash
# Count matching lines per file
grep -c 'error' /var/log/messages
```

```bash
# Print only filenames containing a match
grep -rl 'PermitRootLogin' /etc/ssh/
```

```bash
# Show 3 lines of context after each match
grep -A 3 'Failed password' /var/log/secure
```

```bash
# Recursive search with filename prefix
grep -r 'max_connections' /etc/
```

```bash
# Bracket expression: match eth0 through eth9
grep 'eth[0-9]' /var/log/messages
```

```bash
# POSIX character class: lines beginning with a digit
grep '^[[:digit:]]' /etc/services
```

```bash
# ERE interval: match lines with exactly two digits
grep -E '[0-9]{2}' /etc/passwd
```

```bash
# Suppress binary-file noise
grep -I 'pattern' /usr/bin/*
```

---

## Notes and Constraints

- Pattern matching is anchored to full lines by default only when `-x` is specified; otherwise, a pattern matches anywhere within a line.
- Newline characters cannot be matched within a pattern because newline is the line separator and also separates multiple patterns supplied to `-e` or `-f`.
- When multiple files are specified, output lines are prefixed with the filename. When only one file (or standard input) is searched, the filename prefix is suppressed unless `-H` is given.
- `egrep` and `fgrep` are equivalent to `grep -E` and `grep -F` respectively. Both are deprecated and may be removed in future GNU grep releases.
- Range expressions such as `[a-z]` are locale-dependent. In locales other than C/POSIX, their behavior is unspecified. Use POSIX named classes (`[[:lower:]]`) for portable matching.
- An interval expression repetition count greater than 32767 is invalid.
- A pattern consisting solely of the empty string matches every line; `grep` accepts it but its behavior under POSIX is unspecified. Use `^$` to match empty lines.
- When `grep` encounters a file containing null bytes, it treats the file as binary and suppresses match details unless `-a` or `--binary-files=text` is specified.
- `-P` (PCRE) availability depends on whether `grep` was compiled with PCRE2 support. Availability varies by distribution build.
- BRE backreferences (`\1`–`\9`) are supported; ERE backreferences are not POSIX-portable.
- Requires RHEL 8 / RHEL 9 (GNU grep 3.1 or later).

---

## See Also

- `man grep` — full GNU grep manual including all options, regex syntax, and environment variables
- `man 7 regex` — POSIX regular expression specification
- `man pcre2syntax` — PCRE2 pattern syntax (relevant to `grep -P`)
- `man pcre2pattern` — PCRE2 pattern semantics
- [`sed`](https://www.gnu.org/software/sed/manual/) — stream editor; uses ERE for substitution and address matching
- [`awk`](https://www.gnu.org/software/gawk/manual/) — pattern-scanning and processing language; uses ERE
- Explanation: *Understanding grep and Regular Expressions* — conceptual background on pattern matching, regex dialects, and the filter model