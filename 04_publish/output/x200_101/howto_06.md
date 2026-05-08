---
description: >-
  Construct shell commands that correctly handle filenames and arguments
  containing spaces, glob characters, dollar signs, and newlines using single
  quotes, double quotes, backslash escaping, and ANSI-C
icon: wrench
---

# How-to 6: Use Quoting and Escaping to Handle Special Characters

{% hint style="info" %}
**Prerequisites**

* A Bash shell prompt on an RHEL system with write access to a working directory
* Familiarity with shell expansion behaviour — specifically that the shell processes quoting before passing arguments to commands
{% endhint %}

{% stepper %}
{% step %}
#### Create Test Files with Problematic Names

Create files whose names contain spaces and glob characters to use throughout this guide.

```bash
mkdir ~/quote-test && cd ~/quote-test
touch 'report 2024.txt' 'report 2025.txt' 'costs [final].csv' 'price$list.txt'
```

Confirm all four files exist:

```bash
ls -1
```

Expected output:

```
costs [final].csv
price$list.txt
report 2024.txt
report 2025.txt
```

{% hint style="warning" %}
Running `touch report 2024.txt` without quotes creates **two** files named `report` and `2024.txt` — not one file with a space in its name. The unquoted space is treated as an argument separator.
{% endhint %}
{% endstep %}

{% step %}
#### Reference Files with Spaces Using Quotes or Backslash Escaping

To pass a filename containing spaces as a single argument, use one of three equivalent forms.

{% tabs %}
{% tab title="Single quotes" %}
```bash
ls -l 'report 2024.txt'
```
{% endtab %}

{% tab title="Double quotes" %}
```bash
ls -l "report 2024.txt"
```
{% endtab %}

{% tab title="Backslash escaping" %}
```bash
ls -l report\ 2024.txt
```
{% endtab %}
{% endtabs %}

All three produce the same result. Choose single quotes when the filename contains no characters you need the shell to expand. Choose double quotes when the filename contains a variable reference you want expanded. Use backslash escaping when quoting would interfere with surrounding syntax.
{% endstep %}

{% step %}
#### Prevent Glob Expansion on Bracket Characters

The filename `costs [final].csv` contains `[` and `]`, which the shell treats as glob metacharacters. Without quoting, the shell attempts to match `[final]` as a character class and may fail or produce unexpected results:

```bash
ls -l costs [final].csv
```

Suppress glob expansion with single quotes:

```bash
ls -l 'costs [final].csv'
```

Or with backslash escaping on each metacharacter:

```bash
ls -l costs\ \[final\].csv
```

{% hint style="warning" %}
`[`, `]`, `*`, and `?` are all glob metacharacters. Any of these appearing unquoted in a filename argument will trigger pathname expansion — which may silently match unintended files or produce a "No match" error.
{% endhint %}
{% endstep %}

{% step %}
#### Prevent Dollar Sign Expansion with Single Quotes

The filename `price$list.txt` contains `$`, which the shell treats as the start of a variable reference.

Double quotes suppress word splitting and glob expansion but **do not** suppress variable expansion:

```bash
ls -l "price$list.txt"
```

The shell expands `$list` — which is likely empty — producing `ls -l price.txt` and a "No such file" error.

Single quotes suppress all expansion including `$`:

```bash
ls -l 'price$list.txt'
```

{% hint style="warning" %}
Double quotes never suppress `$` expansion. If a filename or argument must reach the command exactly as written and contains `$`, always use single quotes.
{% endhint %}
{% endstep %}

{% step %}
#### Expand Variables Inside Filenames Using Double Quotes

When the argument contains both a variable reference you want expanded and characters that would otherwise be split or globbed, use double quotes.

```bash
YEAR=2024
ls -l "report ${YEAR}.txt"
```

The shell expands `${YEAR}` to `2024` but treats the space as part of the filename rather than an argument separator.

{% hint style="warning" %}
Use `${VAR}` brace syntax inside double-quoted strings when the variable name is immediately followed by other word characters — otherwise the shell cannot determine where the variable name ends and adjacent text begins.
{% endhint %}
{% endstep %}

{% step %}
#### Embed Literal Newlines and Escape Sequences Using ANSI-C Quoting

To pass arguments containing newlines, tabs, or other control characters, use ANSI-C quoting: `$'...'`.

Create a file whose name contains a literal newline:

```bash
touch $'line1\nline2'
```

Reference it in a command:

```bash
ls -1 $'line1\nline2'
```

Use ANSI-C quoting to pass a tab-separated argument to `printf`:

```bash
printf '%s\t%s\n' $'col1' $'col2'
```

ANSI-C quoting recognises `\n` (newline), `\t` (tab), `\\` (literal backslash), and `\'` (literal single quote) inside `$'...'`.

{% hint style="warning" %}
`$'...'` is a Bash extension — it is not available in POSIX `sh`. If the shell produces literal text instead of the escape sequence, confirm `echo $SHELL` returns `/bin/bash` and switch to a Bash shell.
{% endhint %}
{% endstep %}

{% step %}
#### Verify Expansion Before Execution Using echo and printf %q

Before running a destructive or complex command, verify that the shell is constructing arguments exactly as intended.

Wrap the command with `echo` to preview argument boundaries:

```bash
echo ls -l 'report 2024.txt' "report ${YEAR}.txt" 'costs [final].csv'
```

Expected output — each filename appears as a single token:

```
ls -l report 2024.txt report 2024.txt costs [final].csv
```

Use `printf '%q '` to display the shell-safe representation of each argument, exposing any unexpected expansion:

```bash
printf '%q ' 'report 2024.txt' "price$list.txt" $'line1\nline2'
printf '\n'
```

Expected output:

```
report\ 2024.txt price.txt line1$'\n'line2
```

{% hint style="warning" %}
The output `price.txt` — not `price\$list.txt` — confirms that `"price$list.txt"` silently expanded `$list` to empty. Switch to single quotes: `'price$list.txt'`.
{% endhint %}
{% endstep %}

{% step %}
#### Escape a Single Quote Inside a Single-Quoted String

Single quotes suppress everything, including escape sequences — there is no way to embed a literal single quote inside a single-quoted string by escaping it. Use one of two alternatives.

**Option 1** — End the single-quoted string, insert an escaped single quote, and reopen:

```bash
echo 'it'\''s a test'
```

**Option 2** — Use ANSI-C quoting, which recognises `\'`:

```bash
echo $'it\'s a test'
```

Both produce:

```
it's a test
```

{% hint style="warning" %}
`echo 'it\'s a test'` does **not** work — the backslash is not interpreted inside single quotes. The shell will wait for a closing single quote, producing a continuation prompt or a syntax error.
{% endhint %}

<details>

<summary>Why the close-reopen trick works</summary>

The shell concatenates adjacent quoted strings with no separator. `'it'` is a single-quoted string containing `it`, `\'` is a backslash-escaped single quote producing a literal `'`, and `'s a test'` is a single-quoted string containing `s a test`. The shell joins them into a single argument: `it's a test`.

</details>
{% endstep %}
{% endstepper %}

## Verification

{% hint style="success" %}
Run the following loop to confirm quoting works correctly across all four problematic filename forms:

```bash
cd ~/quote-test
for f in 'report 2024.txt' 'report 2025.txt' 'costs [final].csv' 'price$list.txt'; do
  ls -1 "$f"
done
```

Expected output — all four filenames appear on separate lines with no errors:

```
report 2024.txt
report 2025.txt
costs [final].csv
price$list.txt
```

Any `No such file or directory` error indicates a quoting failure on that specific name — recheck the quoting form used for that entry.
{% endhint %}

## Troubleshooting

{% hint style="warning" %}
**Common quoting failures and their fixes**

**`ls: cannot access 'price.txt': No such file or directory`** → `$list` was expanded inside double quotes, stripping it to empty → Use single quotes: `'price$list.txt'`

***

**`touch report 2024.txt` creates two files instead of one** → The space is unquoted and treated as an argument separator → Quote the argument: `touch 'report 2024.txt'`

***

**`ls -l costs [final].csv` returns unexpected files or an error** → `[final]` is interpreted as a glob character class → Quote the brackets: `'costs [final].csv'` or escape each: `costs\ \[final\].csv`

***

**ANSI-C quoting `$'...'` produces literal text instead of the escape sequence** → The shell is not Bash — ANSI-C quoting is a Bash extension, not POSIX `sh` → Confirm `echo $SHELL` returns `/bin/bash`; switch to a Bash shell

***

**`echo $'it\'s'` fails with a syntax error** → `$'...'` is being used inside another quoting context → Use `$'...'` standalone, not nested inside other quote characters

***

**Variable inside single quotes not expanded** → Single quotes suppress all expansion by design → Switch to double quotes and verify the variable reference with `echo` first
{% endhint %}
