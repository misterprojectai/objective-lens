# Solution: Get Help — Use Shell Help Tools to Answer Questions About Commands

## Task 1: Save whatis output for passwd

```bash
whatis passwd > ~/whatis-passwd.txt
cat ~/whatis-passwd.txt
```

Expected output (may vary slightly):

```
passwd (1)               - update user's authentication tokens
passwd (5)               - password file
```

The file must contain at least one line with `passwd` and a section number in parentheses.

---

## Task 2: Save type output for cd

```bash
type cd > ~/type-cd.txt
cat ~/type-cd.txt
```

Expected output:

```
cd is a shell builtin
```

The file must contain the word `builtin`.

---

## Task 3: Rebuild the man page database

```bash
sudo mandb
```

After completion, verify the database is working:

```bash
whatis ls
```

Expected output:

```
ls (1)               - list directory contents
```

---

## Why These Tools Matter for RHCSA

| Tool | Purpose |
|---|---|
| `whatis <cmd>` | One-line description from the man page database |
| `type <cmd>` | Shows whether a name is a builtin, alias, or external binary |
| `man <cmd>` | Full documentation |
| `apropos <keyword>` | Search man page descriptions by topic |
| `sudo mandb` | Rebuild the whatis/apropos database |

- `cd` is a **shell builtin** — documented with `help cd`, not `man cd`
- `passwd` appears in **two sections**: section 1 (the command) and section 5 (the config file format)
- Run `man 5 passwd` or `man 1 passwd` to read a specific section