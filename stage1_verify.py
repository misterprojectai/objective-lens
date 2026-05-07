#!/usr/bin/env python3
"""
Stage 1 - Verification
Runs post-batch checks on Stage 1 output before passing to Stage 2.
Usage: python3 stage1_verify.py 01_normalize/output/bash001_clean.md
"""

import sys
import os

OUTPUT_FILE = sys.argv[1] if len(sys.argv) > 1 else None

if not OUTPUT_FILE:
    print("Usage: python3 stage1_verify.py <output_file>")
    sys.exit(1)

if not os.path.exists(OUTPUT_FILE):
    print(f"ERROR: File not found: {OUTPUT_FILE}")
    sys.exit(1)

print(f"Stage 1 - Verification")
print(f"File: {OUTPUT_FILE}")
print()

with open(OUTPUT_FILE, encoding="utf-8") as f:
    content = f.read()

paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
passes = []
failures = []

# ── Check 1: Source attribution comment present ───────────────────────────────
if content.startswith("<!-- Source:"):
    passes.append("Source attribution comment present")
else:
    failures.append("FAIL: Missing source attribution comment at top of file")

# ── Check 2: File is non-empty ────────────────────────────────────────────────
if len(content) > 500:
    passes.append(f"File non-empty ({len(content):,} chars)")
else:
    failures.append(f"FAIL: File suspiciously small ({len(content)} chars) — possible extraction failure")

# ── Check 3: Multiple paragraphs present ─────────────────────────────────────
content_paras = [p for p in paragraphs if not p.startswith("<!--")]
# Size-aware paragraph threshold: small SRT files legitimately have fewer paragraphs
min_paras = 3 if len(content) < 2000 else 10
if len(content_paras) >= min_paras:
    passes.append(f"Paragraph count healthy ({len(content_paras)} paragraphs)")
elif len(content_paras) >= 1:
    failures.append(f"FAIL: Too few paragraphs ({len(content_paras)}, threshold {min_paras}) — possible paragraph splitting failure")
else:
    failures.append("FAIL: No content paragraphs found")

# ── Check 4: No encoding artifacts ───────────────────────────────────────────
artifacts = ["\x00", "\ufffd", "â€", "ï¬", "â€™"]
found = [a for a in artifacts if a in content]
if not found:
    passes.append("No encoding artifacts detected")
else:
    failures.append(f"FAIL: Encoding artifacts found: {found} — Job B encoding fix incomplete")

# ── Check 5: No SRT timestamps remaining ─────────────────────────────────────
import re
srt_pattern = re.search(r'\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}', content)
if not srt_pattern:
    passes.append("No SRT timestamps remaining")
else:
    failures.append("FAIL: SRT timestamps still present — Job B regex incomplete")

# ── Check 6: No obvious platform navigation noise ────────────────────────────
nav_patterns = ["click next", "pause the video", "pause and try", "visit our website"]
found_nav = [p for p in nav_patterns if p.lower() in content.lower()]
if not found_nav:
    passes.append("No platform navigation noise detected")
else:
    failures.append(f"FAIL: Platform navigation noise found: {found_nav} — Job C missed these")

# ── Check 7: Technical content density ───────────────────────────────────────
# Technical content check — look for Linux command syntax patterns
# More reliable than keyword matching for man pages and narrow-topic transcripts
import re as _re
syntax_patterns = [
    r'`[^`]+`',           # backtick-quoted commands or terms
    r'--[a-z][\w-]+',     # long flags (--option)
    r'\$[A-Z_]+',         # environment variables ($PATH)
    r'\$\{[^}]+\}',       # variable expansion (${VAR})
    r'(?m)^\s{0,4}\*{2}\?-', # bold flag entries in man pages (**-f)
]
syntax_hits = sum(1 for p in syntax_patterns if _re.search(p, content))
# Also check broad keyword list as fallback
tech_markers = [
    "bash", "shell", "command", "linux", "variable", "script",
    "function", "path", "file", "directory", "process",
    "wildcard", "glob", "ssh", "terminal", "history", "alias",
    "prompt", "environment", "startup", "login", "echo", "export",
    "chmod", "sudo", "user", "root", "signal", "pipe", "redirect",
    "option", "output", "input", "format", "standard", "argument",
    "syntax", "flag", "parameter", "string", "integer", "mode"
]
keyword_count = sum(1 for m in tech_markers if m.lower() in content.lower())
# Pass if EITHER syntax patterns found OR sufficient keyword density
threshold = 3 if len(content) < 2000 else 5
if syntax_hits >= 2 or keyword_count >= threshold:
    passes.append(f"Technical content confirmed (syntax patterns: {syntax_hits}/5, keywords: {keyword_count}/{len(tech_markers)})")
else:
    failures.append(f"FAIL: No technical content detected (syntax: {syntax_hits}/5, keywords: {keyword_count}/{len(tech_markers)}) — possible over-aggressive noise removal or wrong source file")

# ── Check 8: No empty section headers ────────────────────────────────────────
empty_headers = re.findall(r'(?m)^#{1,3} \*?\*?$', content)
if not empty_headers:
    passes.append("No empty section headers")
else:
    failures.append(f"FAIL: {len(empty_headers)} empty section headers found — noise removal left orphaned headers")

# ── Report ────────────────────────────────────────────────────────────────────
print(f"Results: {len(passes)} passed, {len(failures)} failed")
print()

for p in passes:
    print(f"  ✓ {p}")

if failures:
    print()
    for f in failures:
        print(f"  ✗ {f}")
    print()
    print("VERIFICATION FAILED — fix issues before running Stage 2")
    sys.exit(1)
else:
    print()
    print("VERIFICATION PASSED — ready for Stage 2")
    print(f"Next: python3 stage2_run.py {OUTPUT_FILE}")
