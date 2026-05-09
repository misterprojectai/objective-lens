# Solution: RHCSA Prep — Quoting and Escaping Special Characters

## Task 1 — Create four files with special characters in their names

```bash
cd ~/quote-test

# Space in name — single or double quotes both work
touch 'report 2024.txt'
touch 'report 2025.txt'

# Square brackets are glob metacharacters — single quotes suppress glob expansion
touch 'costs [final].csv'

# Dollar sign — MUST use single quotes; double quotes would expand $list
touch 'price$list.txt'
```

Verify:

```bash
ls -1 ~/quote-test
```

Expected output:

```
costs [final].csv
price$list.txt
report 2024.txt
report 2025.txt
```

---

## Task 2 — Archive all four files into `special-files.tar.gz`

```bash
cd ~/quote-test

tar czf special-files.tar.gz \
  'report 2024.txt' \
  'report 2025.txt' \
  'costs [final].csv' \
  'price$list.txt'
```

Verify the archive contents:

```bash
tar tzf ~/quote-test/special-files.tar.gz
```

Expected output (order may vary):

```
report 2024.txt
report 2025.txt
costs [final].csv
price$list.txt
```

**Why it works:** Each filename is single-quoted so the shell passes it as a single argument to `tar`. Without quotes, `tar` would receive `costs`, `[final].csv` as separate arguments, and `[final]` might glob-expand against the directory.

---

## Task 3 — Generate `summary.txt` using a for loop

```bash
cd ~/quote-test

for f in 'report 2024.txt' 'report 2025.txt' 'costs [final].csv' 'price$list.txt'; do
  echo "$f"
done > summary.txt
```

Verify:

```bash
cat ~/quote-test/summary.txt
wc -l ~/quote-test/summary.txt
```

Expected output:

```
report 2024.txt
report 2025.txt
costs [final].csv
price$list.txt
4 summary.txt
```

**Key points:**
- The list items in `for f in ...` are single-quoted so each special filename is one token.
- `"$f"` inside the loop body is double-quoted so word splitting does not break filenames with spaces into multiple arguments when passed to `echo`.
- The `>` redirect after `done` captures all four `echo` outputs into the file.

---

## Task 4 — Create `notes.txt` using ANSI-C quoting

```bash
cd ~/quote-test

printf '%s\n' $'Status\tOK' > notes.txt
printf '%s\n' $'it\'s ready' >> notes.txt
```

Or as a single `printf` call:

```bash
printf '%s\n%s\n' $'Status\tOK' $'it\'s ready' > notes.txt
```

Verify:

```bash
# cat -A shows tabs as ^I and line ends as $
cat -A ~/quote-test/notes.txt
```

Expected output:

```
Status^IOK$
it's ready$
```

```bash
grep -P 'Status\tOK' ~/quote-test/notes.txt && echo "Tab confirmed"
grep -F "it's ready" ~/quote-test/notes.txt && echo "Apostrophe confirmed"
```

**Why it works:**
- `$'Status\tOK'` — ANSI-C quoting converts `\t` to a real tab (ASCII 0x09) before the string is passed to `printf`.
- `$'it\'s ready'` — inside `$'...'`, `\'` is a literal single quote (apostrophe). You cannot embed `'` inside a normal single-quoted string, but ANSI-C quoting supports this escape.
- Using double quotes like `"it's ready"` would also work for the apostrophe line, but ANSI-C quoting is the correct form for embedding `\t` without `printf` format string tricks.

---

## Summary of quoting forms used

| Form | Suppresses word split | Suppresses glob | Suppresses `$` expansion | Allows escape sequences |
|---|---|---|---|---|
| `'...'` single quotes | ✓ | ✓ | ✓ | ✗ |
| `"..."` double quotes | ✓ | ✓ | ✗ | `\"` `\\` only |
| `\` backslash | next char only | ✓ | ✓ | ✗ |
| `$'...'` ANSI-C | ✓ | ✓ | ✓ | ✓ (`\t` `\n` `\'` etc.) |