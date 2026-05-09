#!/usr/bin/env python3
"""
Stage 1 - Verification
Validates Stage 1 normalized output before passing to Stage 2.

Accepts either a single file or a directory:
  python3 stage1_verify.py 01_normalize/output/x200_101/bash001_clean.md
  python3 stage1_verify.py 01_normalize/output/x200_101/

Directory mode runs all checks across all *_clean.md files and prints
a single consolidated pass/fail report. Exit code 0 = all passed.

Checks per file:
  1. Source attribution comment present
  2. File non-empty (size-aware threshold)
  3. Paragraph count healthy (size-aware threshold)
  4. No encoding artifacts
  5. No SRT timestamps remaining
  6. No platform navigation noise
  7. Technical content confirmed (syntax patterns or keyword density)
  8. No empty section headers

Pure stdlib — no external dependencies.
"""

import sys
import os
import re

if len(sys.argv) < 2:
    print("Usage: python3 stage1_verify.py <file_or_directory>")
    sys.exit(1)

target = sys.argv[1]

# ── Resolve targets ───────────────────────────────────────────────────────────

if os.path.isdir(target):
    files = sorted([
        os.path.join(target, f)
        for f in os.listdir(target)
        if f.endswith("_clean.md") and not f.startswith(".")
    ])
    if not files:
        print("ERROR: No *_clean.md files found in " + target)
        sys.exit(1)
    directory_mode = True
elif os.path.isfile(target):
    files = [target]
    directory_mode = False
else:
    print("ERROR: Not a file or directory: " + target)
    sys.exit(1)

# ── Checks (applied per file) ─────────────────────────────────────────────────

SYNTAX_PATTERNS = [
    r'`[^`]+`',           # backtick-quoted commands or terms
    r'--[a-z][\w-]+',     # long flags (--option)
    r'\$[A-Z_]+',         # environment variables ($PATH)
    r'\$\{[^}]+\}',       # variable expansion (${VAR})
    r'(?m)^\s{0,4}\*\*-', # bold flag entries in man pages (**-f)
]

TECH_KEYWORDS = [
    "bash", "shell", "command", "linux", "variable", "script",
    "function", "path", "file", "directory", "process",
    "wildcard", "glob", "ssh", "terminal", "history", "alias",
    "prompt", "environment", "startup", "login", "echo", "export",
    "chmod", "sudo", "user", "root", "signal", "pipe", "redirect",
    "option", "output", "input", "format", "standard", "argument",
    "syntax", "flag", "parameter", "string", "integer", "mode",
]

NOISE_PHRASES = ["click next", "pause the video", "pause and try",
                 "visit our website"]

ENCODING_ARTIFACTS = ["\x00", "\ufffd", "â€", "ï¬", "â€™"]

def check_file(path):
    """Run all checks on a single file. Returns (passes, failures) lists."""
    passes   = []
    failures = []

    if not os.path.exists(path):
        failures.append("file not found: " + path)
        return passes, failures

    with open(path, encoding="utf-8") as f:
        content = f.read()

    paragraphs     = [p.strip() for p in content.split("\n\n") if p.strip()]
    content_paras  = [p for p in paragraphs if not p.startswith("<!--")]

    # ── Check 1: Source attribution ───────────────────────────────────────────
    if content.startswith("<!-- Source:"):
        passes.append("source attribution comment present")
    else:
        failures.append("missing source attribution comment at top of file")

    # ── Check 2: Non-empty ────────────────────────────────────────────────────
    if len(content) > 500:
        passes.append("file non-empty (" + str(len(content)) + " chars)")
    else:
        failures.append("file suspiciously small ("
                        + str(len(content)) + " chars) — possible extraction failure")

    # ── Check 3: Paragraph count ──────────────────────────────────────────────
    min_paras = 3 if len(content) < 2000 else 10
    if len(content_paras) >= min_paras:
        passes.append("paragraph count healthy (" + str(len(content_paras)) + " paragraphs)")
    else:
        failures.append("too few paragraphs ("
                        + str(len(content_paras)) + ", threshold " + str(min_paras)
                        + ") — possible paragraph splitting failure")

    # ── Check 4: No encoding artifacts ───────────────────────────────────────
    found_artifacts = [a for a in ENCODING_ARTIFACTS if a in content]
    if not found_artifacts:
        passes.append("no encoding artifacts detected")
    else:
        failures.append("encoding artifacts found: " + str(found_artifacts)
                        + " — Job B encoding fix incomplete")

    # ── Check 5: No SRT timestamps ────────────────────────────────────────────
    if not re.search(r'\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}', content):
        passes.append("no SRT timestamps remaining")
    else:
        failures.append("SRT timestamps still present — Job B regex incomplete")

    # ── Check 6: No platform navigation noise ────────────────────────────────
    found_noise = [p for p in NOISE_PHRASES if p.lower() in content.lower()]
    if not found_noise:
        passes.append("no platform navigation noise detected")
    else:
        failures.append("platform navigation noise found: " + str(found_noise)
                        + " — Job C missed these")

    # ── Check 7: Technical content density ───────────────────────────────────
    syntax_hits  = sum(1 for p in SYNTAX_PATTERNS if re.search(p, content))
    keyword_hits = sum(1 for kw in TECH_KEYWORDS if kw.lower() in content.lower())
    threshold    = 3 if len(content) < 2000 else 5
    if syntax_hits >= 2 or keyword_hits >= threshold:
        passes.append("technical content confirmed (syntax: "
                      + str(syntax_hits) + "/5, keywords: "
                      + str(keyword_hits) + "/" + str(len(TECH_KEYWORDS)) + ")")
    else:
        failures.append("no technical content detected (syntax: "
                        + str(syntax_hits) + "/5, keywords: "
                        + str(keyword_hits) + "/" + str(len(TECH_KEYWORDS))
                        + ") — possible over-aggressive noise removal or wrong source file")

    # ── Check 8: No empty section headers ────────────────────────────────────
    empty_headers = re.findall(r'(?m)^#{1,3} \*?\*?$', content)
    if not empty_headers:
        passes.append("no empty section headers")
    else:
        failures.append(str(len(empty_headers))
                        + " empty section headers found — noise removal left orphaned headers")

    return passes, failures

# ── Single file mode ──────────────────────────────────────────────────────────

def run_single(path):
    print("Stage 1 - Verification")
    print("File: " + path)
    print()

    passes, failures = check_file(path)

    print("Results: " + str(len(passes)) + " passed, " + str(len(failures)) + " failed")
    print()
    for p in passes:
        print("  \u2713 " + p)
    if failures:
        print()
        for f in failures:
            print("  \u2717 " + f)
        print()
        print("VERIFICATION FAILED — fix issues before running Stage 2")
        sys.exit(1)
    else:
        print()
        print("VERIFICATION PASSED — ready for Stage 2")
        print("Next: python3 stage2_run.py "
              + "_config/exam-objectives/<objective_id>.md")

# ── Directory mode ────────────────────────────────────────────────────────────

def run_directory(directory, file_list):
    objective_id = os.path.basename(directory.rstrip("/"))
    print("Stage 1 - Verification")
    print("Directory:  " + directory)
    print("Objective:  " + objective_id)
    print("Files:      " + str(len(file_list)))
    print()

    all_passes   = []
    all_failures = []
    file_results = []

    for path in file_list:
        fname          = os.path.basename(path)
        passes, fails  = check_file(path)
        all_passes.extend(passes)
        all_failures.extend(fails)
        file_results.append((fname, passes, fails))

    total = len(all_passes) + len(all_failures)
    print("Results: " + str(len(all_passes)) + "/" + str(total)
          + " passed, " + str(len(all_failures)) + " failed across "
          + str(len(file_list)) + " files")
    print()

    for fname, passes, fails in file_results:
        status = "\u2713" if not fails else "\u2717"
        print("  " + status + " " + fname
              + " — " + str(len(passes)) + " passed"
              + (", " + str(len(fails)) + " failed" if fails else ""))
        for f in fails:
            print("      \u2717 " + f)

    if all_failures:
        print()
        print("VERIFICATION FAILED — " + str(len(all_failures))
              + " issue(s) across " + str(len(file_list)) + " files")
        sys.exit(1)
    else:
        print()
        print("VERIFICATION PASSED — all " + str(len(file_list))
              + " files ready for Stage 2")
        print("Next: python3 stage2_run.py "
              + "_config/exam-objectives/" + objective_id + ".md")

# ── Dispatch ──────────────────────────────────────────────────────────────────

if directory_mode:
    run_directory(target, files)
else:
    run_single(files[0])
