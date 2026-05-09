#!/usr/bin/env python3
"""
Line Commander Labs — Pipeline Orchestrator

Runs Stages 1 through 4 for a single exam objective with zero operator
intervention. All verify gates must pass before the next stage runs.
Stage 4 commits and pushes only after its verify gate passes.

Operator responsibilities:
  1. Drop source files into  01_normalize/input/<objective_id>/
  2. Drop exam objective into _config/exam-objectives/<objective_id>.md
  3. Run: python3 run_pipeline.py <objective_id>

Usage:
  python3 run_pipeline.py x200_103
"""

import os
import sys
import subprocess
import time

# ── Config ────────────────────────────────────────────────────────────────────

VENV_PYTHON     = sys.executable
SUPPORTED_INPUT = {".pdf", ".md", ".txt", ".srt", ".html", ".docx"}

# ── Output helpers ────────────────────────────────────────────────────────────

def banner(text):
    print()
    print("=" * 74)
    print("  " + text)
    print("=" * 74)

def section(text):
    print("\n── " + text + " " + "─" * max(0, 70 - len(text)))

def ok(text):
    print("  ✓ " + text)

def warn(text):
    print("  ! " + text)

def fail(text):
    print("  ✗ " + text)

def abort(reason):
    print()
    print("PIPELINE ABORTED")
    print("  Reason: " + reason)
    print()
    sys.exit(1)

# ── Subprocess helpers ────────────────────────────────────────────────────────

def run_streamed(args):
    """Run a subprocess streaming its output. Returns exit code."""
    result = subprocess.run(args, text=True)
    return result.returncode

def run_captured(args):
    """Run a subprocess capturing its output. Returns (rc, combined_output)."""
    result = subprocess.run(args, capture_output=True, text=True)
    return result.returncode, result.stdout + result.stderr

def git_add_commit(paths, message):
    """Stage specific paths and commit. Silent if nothing to commit."""
    existing = [p for p in paths if os.path.exists(p.rstrip("/"))]
    if not existing:
        return
    subprocess.run(["git", "add"] + existing, capture_output=True)
    status = subprocess.run(["git", "status", "--porcelain"],
                            capture_output=True, text=True)
    if not status.stdout.strip():
        return
    result = subprocess.run(["git", "commit", "-m", message],
                            capture_output=True, text=True)
    if result.returncode == 0:
        ok("Committed: " + message)
    else:
        warn("git commit failed: " + result.stderr.strip())

# ── Pre-flight ────────────────────────────────────────────────────────────────

def preflight(objective_id):
    section("Pre-flight checks")
    errors = []

    obj_path  = "_config/exam-objectives/" + objective_id + ".md"
    input_dir = "01_normalize/input/" + objective_id

    if os.path.exists(obj_path):
        ok("Objective file: " + obj_path)
    else:
        fail("Objective file missing: " + obj_path)
        errors.append(obj_path)

    if os.path.isdir(input_dir):
        sources = [
            f for f in os.listdir(input_dir)
            if os.path.splitext(f)[1].lower() in SUPPORTED_INPUT
            and not f.startswith(".")
        ]
        if sources:
            ok("Source files: " + str(len(sources)) + " files in " + input_dir + "/")
        else:
            fail("No source files in " + input_dir + "/")
            errors.append(input_dir)
    else:
        fail("Source directory missing: " + input_dir + "/")
        errors.append(input_dir)

    if errors:
        print()
        print("Fix the above issues and re-run.")
        sys.exit(1)

# ── Stage 1 ───────────────────────────────────────────────────────────────────

def run_stage1(objective_id):
    section("Stage 1 — Normalize")
    rc = run_streamed([VENV_PYTHON, "stage1_run.py", objective_id])
    if rc != 0:
        abort("Stage 1 failed — check output above")

    section("Stage 1 — Verify")
    # stage1_verify.py accepts a directory — one call, one report
    output_dir = "01_normalize/output/" + objective_id
    if not os.path.isdir(output_dir):
        abort("Stage 1 output directory missing: " + output_dir)

    rc, output = run_captured([VENV_PYTHON, "stage1_verify.py", output_dir])
    print(output)
    if rc != 0:
        abort("Stage 1 verify failed — check output above")
    ok("Stage 1 verify passed")


# ── Stage 2 ───────────────────────────────────────────────────────────────────

def run_stage2(objective_id):
    section("Stage 2 — Map")
    obj_path = "_config/exam-objectives/" + objective_id + ".md"
    rc = run_streamed([VENV_PYTHON, "stage2_run.py", obj_path])
    if rc != 0:
        abort("Stage 2 failed — check output above")

    section("Stage 2 — Verify")
    mapped_path = ("02_map/output/" + objective_id
                   + "/" + objective_id + "_mapped-passages.md")
    rc, output = run_captured([VENV_PYTHON, "stage2_verify.py", mapped_path])
    print(output)
    if rc != 0:
        abort("Stage 2 verify failed")
    ok("Stage 2 verify passed")


# ── Stage 3 ───────────────────────────────────────────────────────────────────

def run_stage3(objective_id):
    section("Stage 3 — Diataxis")
    mapped_path = ("02_map/output/" + objective_id
                   + "/" + objective_id + "_mapped-passages.md")
    rc = run_streamed([VENV_PYTHON, "stage3_run.py", mapped_path])
    if rc != 0:
        abort("Stage 3 failed — check output above")

    section("Stage 3 — Verify")
    prefix = ("03_diataxis/output/" + objective_id
              + "/" + objective_id)
    rc, output = run_captured([VENV_PYTHON, "stage3_verify.py", prefix])
    print(output)
    if rc != 0:
        abort("Stage 3 verify failed")
    ok("Stage 3 verify passed")


# ── Stage 4 ───────────────────────────────────────────────────────────────────

def run_stage4(objective_id):
    section("Stage 4 — GitBook Publish")
    # stage4_run.py now accepts bare objective_id directly
    rc = run_streamed([VENV_PYTHON, "stage4_run.py", objective_id])
    if rc != 0:
        abort("Stage 4 failed — check output above")

    section("Stage 4 — Verify")
    output_dir = "04_publish/output/" + objective_id
    rc, output = run_captured([VENV_PYTHON, "stage4_verify.py", output_dir])
    print(output)
    if rc != 0:
        # Stage 4 committed and pushed before we ran verify.
        # The operator must fix the failing files and push manually.
        abort(
            "Stage 4 verify failed after push.\n"
            "  Fix the failing documents, then run:\n"
            "    python3 stage4_verify.py " + output_dir + "\n"
            "  Then commit and push manually:\n"
            "    git add " + output_dir + "/\n"
            "    git commit -m \"fix: Stage 4 verify failures " + objective_id + "\"\n"
            "    git push origin main"
        )
    ok("Stage 4 verify passed")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 run_pipeline.py <objective_id>")
        print("Example: python3 run_pipeline.py x200_103")
        sys.exit(1)

    objective_id = sys.argv[1].strip().rstrip("/")
    # Accept full path — extract basename
    if os.sep in objective_id or "/" in objective_id:
        objective_id = os.path.basename(objective_id)

    start = time.time()

    banner("Line Commander Labs Pipeline — " + objective_id)
    print("  Objective: " + objective_id)
    print("  Python:    " + VENV_PYTHON)
    print("  Started:   " + time.strftime("%Y-%m-%d %H:%M:%S"))

    preflight(objective_id)

    # ── Stage 1 ───────────────────────────────────────────────────────────────
    run_stage1(objective_id)
    git_add_commit(
        ["01_normalize/input/" + objective_id,
         "01_normalize/output/" + objective_id],
        "feat: Stage 1 complete — normalize " + objective_id
    )

    # ── Stage 2 ───────────────────────────────────────────────────────────────
    run_stage2(objective_id)
    git_add_commit(
        ["02_map/output/" + objective_id],
        "feat: Stage 2 complete — map " + objective_id
    )

    # ── Stage 3 ───────────────────────────────────────────────────────────────
    run_stage3(objective_id)
    git_add_commit(
        ["03_diataxis/output/" + objective_id],
        "feat: Stage 3 complete — diataxis " + objective_id
    )

    # ── Stage 4 (commits and pushes internally) ───────────────────────────────
    run_stage4(objective_id)

    # ── Done ──────────────────────────────────────────────────────────────────
    elapsed      = int(time.time() - start)
    mins, secs   = divmod(elapsed, 60)

    banner("Pipeline complete — " + objective_id)
    print("  Time:      " + str(mins) + "m " + str(secs) + "s")
    print("  Published: 04_publish/output/" + objective_id + "/")
    print("  GitBook:   check your space for the new " + objective_id + " section")
    print()

if __name__ == "__main__":
    main()
