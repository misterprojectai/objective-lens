# Solution: Fix the Broken Script That Processes Special-Character Filenames

## What Was Broken and Why

The init task created `/home/laborant/process_reports.sh` with three distinct quoting bugs — one for each of the three "difficult" filenames. The bugs are:

1. **Space in filename — unquoted arguments split by the shell:**
   ```bash
   wc -l /home/laborant/reports/report $YEAR.txt
   ```
   The shell sees four arguments: `/home/laborant/reports/report`, `$YEAR` (expanded to `2024`), and `.txt`. It treats each as a separate file path, none of which exist.

2. **Bracket characters — glob expansion fires:**
   ```bash
   wc -l /home/laborant/reports/costs [final].csv
   ```
   `[final]` is a glob character class. The shell attempts to expand it against the filesystem. If no match is found the literal string is passed, causing a "No such file" error. If an accidental match exists, the wrong file is processed.

3. **Dollar sign in filename — variable expansion inside double quotes:**
   ```bash
   wc -l /home/laborant/reports/"price$list.txt"
   ```
   Double quotes suppress word splitting and glob expansion but **do not** suppress variable expansion. `$list` is almost certainly unset, so it expands to the empty string, producing the path `price.txt`, which does not exist.

---

## How to Diagnose It

### Step 1 — Run the script and observe the errors

```bash
bash ~/process_reports.sh
```

You will see output similar to:

```
Processing: report 2024.txt
wc: /home/laborant/reports/report: No such file or directory
wc: 2024.txt: No such file or directory
Processing: costs [final].csv
wc: /home/laborant/reports/costs: No such file or directory
wc: [final].csv: No such file or directory
Processing: price$list.txt
wc: /home/laborant/reports/price.txt: No such file or directory
```

### Step 2 — Inspect the script

```bash
cat ~/process_reports.sh
```

Compare each `wc -l` invocation against the actual filename.

### Step 3 — Confirm the files exist

```bash
ls -1 ~/reports/
```

All four files are present. The problem is purely in how the script references them.

### Step 4 — Use printf %q to preview expansion

```bash
printf '%q\n' "price$list.txt"
# → price.txt   (wrong — $list expanded to empty)

printf '%q\n' 'price$list.txt'
# → price\$list.txt   (correct — dollar sign preserved)
```

---

## How to Fix It

Open the script in a text editor:

```bash
vi ~/process_reports.sh
```

Apply all three fixes:

### Fix 1 — Quote the space-containing filename with double quotes so `$YEAR` still expands

Change:
```bash
wc -l /home/laborant/reports/report $YEAR.txt
```
To:
```bash
wc -l "/home/laborant/reports/report ${YEAR}.txt"
```

### Fix 2 — Quote the bracket-containing filename with single quotes

Change:
```bash
wc -l /home/laborant/reports/costs [final].csv
```
To:
```bash
wc -l '/home/laborant/reports/costs [final].csv'
```

### Fix 3 — Quote the dollar-sign filename with single quotes (not double quotes)

Change:
```bash
wc -l /home/laborant/reports/"price$list.txt"
```
To:
```bash
wc -l '/home/laborant/reports/price$list.txt'
```

### Complete corrected script

```bash
#!/bin/bash
YEAR=2024
echo "Processing: report $YEAR.txt"
wc -l "/home/laborant/reports/report ${YEAR}.txt"
echo "Processing: costs [final].csv"
wc -l '/home/laborant/reports/costs [final].csv'
echo "Processing: price$list.txt"
wc -l '/home/laborant/reports/price$list.txt'
```

---

## How to Verify the Fix

Run the script and confirm there are no errors:

```bash
bash ~/process_reports.sh
```

Expected clean output (all three files report 0 lines because they are empty):

```
Processing: report 2024.txt
0 /home/laborant/reports/report 2024.txt
Processing: costs [final].csv
0 /home/laborant/reports/costs [final].csv
Processing: price$list.txt
0 /home/laborant/reports/price$list.txt
```

No "No such file or directory" errors appear.

---

## Key Takeaways

| Filename contains | Correct quoting | Why |
|---|---|---|
| Space only | Double quotes `"name with space"` | Allows `$VAR` expansion while suppressing word splitting |
| `[` or `]` | Single quotes `'name[bracket]'` | Suppresses glob expansion entirely |
| Literal `$` | Single quotes `'price$list.txt'` | Single quotes are the only form that suppresses `$` expansion |
| Both `$` and a variable you want expanded | Not possible in one token — use variable substitution carefully | Combine double-quoted variable with single-quoted literal using string concatenation |