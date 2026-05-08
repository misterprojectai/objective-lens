#!/usr/bin/env python3
"""
Stage 3 - Diataxis Transformation
Transforms mapped passages into a full Diataxis document set.
Uses Sonnet 4.6 throughout — this is the 10% AI judgment layer.

Flow:
  1. Write Explanation (anchor document)
  2. Planning loop (max 3 passes):
     a. Planner — reasons through tutorial/how-to scope, produces JSON plan
     b. Reviewer — challenges the plan, approves or returns revised plan
     c. If revised: feed back to Planner for next iteration
  3. Write N tutorials sequentially (each derived from Explanation)
  4. Write M how-tos sequentially (each derived from Explanation + all tutorials)
  5. Write Reference (one per objective)
  All outputs auto-strip source comments and YAML fences on write.

Quantity constraints:
  MIN_TUTORIALS = 3, MAX_TUTORIALS = 7
  MIN_HOWTOS    = 3, MAX_HOWTOS    = 7

Usage:
  python3 stage3_run.py 02_map/output/x200_101/x200_101_mapped-passages.md
"""

import sys
import os
import re
import json
from datetime import date
import anthropic

# ── Config ────────────────────────────────────────────────────────────────────

MAX_PLAN_ITERATIONS = 3
MIN_TUTORIALS = 3
MAX_TUTORIALS = 7
MIN_HOWTOS    = 3
MAX_HOWTOS    = 7

if len(sys.argv) < 2:
    print("Usage: python3 stage3_run.py 02_map/output/x200_101/x200_101_mapped-passages.md")
    sys.exit(1)

MAPPED_FILE = sys.argv[1]
os.makedirs(OUTPUT_DIR, exist_ok=True)

if not os.path.exists(MAPPED_FILE):
    print(f"ERROR: Mapped passages file not found: {MAPPED_FILE}")
    sys.exit(1)

basename     = os.path.basename(MAPPED_FILE)
objective_id = basename.replace("_mapped-passages.md", "")
OUTPUT_DIR  = f"03_diataxis/output/{objective_id}"
os.makedirs(OUTPUT_DIR, exist_ok=True)

print(f"Stage 3 - Diataxis Transformation")
print(f"Input:       {MAPPED_FILE}")
print(f"Output:      {OUTPUT_DIR}/{objective_id}_*.md")
print(f"Model:       claude-sonnet-4-6")
print(f"Plan loop:   max {MAX_PLAN_ITERATIONS} iterations")
print(f"Constraints: tutorials {MIN_TUTORIALS}-{MAX_TUTORIALS}, how-tos {MIN_HOWTOS}-{MAX_HOWTOS}")
print()

# ── Load inputs ───────────────────────────────────────────────────────────────

with open(MAPPED_FILE, encoding="utf-8") as f:
    mapped_content = f.read()

with open("_config/diataxis-rules.md", encoding="utf-8") as f:
    diataxis_rules = f.read()

with open("_templates/explanation.md", encoding="utf-8") as f:
    explanation_template = f.read()

with open("_templates/tutorial.md", encoding="utf-8") as f:
    tutorial_template = f.read()

with open("_templates/how-to.md", encoding="utf-8") as f:
    howto_template = f.read()

with open("_templates/reference.md", encoding="utf-8") as f:
    reference_template = f.read()

objective_title = ""
for line in mapped_content.splitlines():
    if line.startswith("**Objective:**"):
        objective_title = line.replace("**Objective:**", "").strip()
        break

print(f"Objective: {objective_title}")
print(f"Input:     {len(mapped_content):,} chars")
print()

# ── Sonnet 4.6 client ────────────────────────────────────────────────────────

client = anthropic.Anthropic()

def call_sonnet(system_prompt, user_prompt, label, max_tokens=8192):
    print(f"  [{label}] Calling Sonnet 4.6...", end="", flush=True)
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=max_tokens,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}]
    )
    result = response.content[0].text
    print(f" done ({len(result):,} chars)")
    return result

def strip_source_comments(text):
    """Remove <!-- Source: ... --> comment lines."""
    return re.sub(r'<!-- Source:[^\n]*-->\n?', '', text)

def strip_yaml_fences(text):
    """Remove ```yaml and ``` wrappers around YAML frontmatter if present."""
    # Pattern: optional whitespace, ```yaml, newline, content, ```, newline
    text = re.sub(r'^```ya?ml?\n(---\n)', r'\1', text, flags=re.MULTILINE)
    # Also handle closing fence immediately after frontmatter block
    text = re.sub(r'\n```\n(---\n)', r'\n\1', text)
    # Catch the case where the entire frontmatter block is wrapped
    text = re.sub(r'^```ya?ml?\n(---.*?---)\n```\n', r'\1\n', text, flags=re.DOTALL)
    return text

def clean_doc(text):
    """Apply all post-write cleaning steps."""
    text = strip_yaml_fences(text)
    text = strip_source_comments(text)
    return text

def write_doc(path, content):
    cleaned = clean_doc(content)
    with open(path, "w", encoding="utf-8") as f:
        f.write(cleaned)
    print(f"  Written: {path} ({os.path.getsize(path):,} bytes)")
    return cleaned

def parse_plan_json(raw):
    """Extract and parse JSON from a model response, stripping code fences."""
    lines = raw.splitlines()
    if lines and lines[0].startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].strip().startswith("```"):
        lines = lines[:-1]
    text = "\n".join(lines).strip()
    brace = text.find("{")
    if brace > 0:
        text = text[brace:]
    return json.loads(text)

# ── SHARED SYSTEM PROMPT ──────────────────────────────────────────────────────

DIATAXIS_CONTEXT = f"""You are a technical documentation writer producing RHCSA Linux certification content using the Diataxis framework.

DIATAXIS RULES (authoritative — excerpt):
{diataxis_rules[:3000]}

OBJECTIVE: {objective_title}
OBJECTIVE ID: {objective_id}

Quality standard — every document and every plan you produce must:
- Continuously maintain high effectiveness (content serves its exact Diataxis purpose with zero contamination)
- Constantly increase maximum efficiency (no padding, no redundancy, every item earns its place)
- Significantly improve top performance (exam-prep content — precision, accuracy, and completeness are non-negotiable)

FRONTMATTER RULE: All documents use bare --- delimiters for YAML frontmatter.
NEVER wrap frontmatter in ```yaml``` code fences. Output raw YAML between --- markers only."""

# ─────────────────────────────────────────────────────────────────────────────
# STEP 1 — EXPLANATION
# ─────────────────────────────────────────────────────────────────────────────

print("Step 1: Writing Explanation (anchor document)...")

EXPLANATION_PROMPT = f"""Write a complete Explanation document for the RHCSA exam objective: {objective_title}

TEMPLATE STRUCTURE:
{explanation_template}

SOURCE MATERIAL (mapped passages):
{mapped_content}

EXPLANATION RULES:
- Understanding-oriented. Answer: what is this, why does it exist, how does it work conceptually.
- No step-by-step instructions anywhere.
- No reference tables as primary content.
- Rich conceptual depth — this is the anchor everything else derives from.
- Required sections: Background, How It Works, Design Philosophy or Key Concepts, Trade-offs and Considerations, Common Misconceptions, Relationship to Other Objectives.
- Further Reading section at the end with placeholder links to Tutorial(s), How-to(s), Reference.
- YAML frontmatter: title, type: explanation, exam_objective: {objective_id}, version: "1.0", status: draft
- FRONTMATTER: use bare --- delimiters only — never ```yaml``` fences.
- Strip all <!-- GUIDANCE --> template comments from output.
- Do NOT include <!-- Source: --> attribution comments.

Output the complete Explanation document only. No preamble."""

explanation_doc   = call_sonnet(DIATAXIS_CONTEXT, EXPLANATION_PROMPT, "Explanation")
explanation_path  = f"{OUTPUT_DIR}/{objective_id}_explanation.md"
explanation_clean = write_doc(explanation_path, explanation_doc)
print()

# ─────────────────────────────────────────────────────────────────────────────
# STEP 2 — PLANNING LOOP
# ─────────────────────────────────────────────────────────────────────────────

print(f"Step 2: Planning loop (max {MAX_PLAN_ITERATIONS} iterations)...")
print()

QUANTITY_RULES = f"""QUANTITY CONSTRAINTS (hard limits — not negotiable):
- Tutorials: minimum {MIN_TUTORIALS}, maximum {MAX_TUTORIALS}
- How-tos:   minimum {MIN_HOWTOS}, maximum {MAX_HOWTOS}

Under-production is a quality failure. The explanation document contains rich conceptual
material across multiple distinct skill areas. Every distinct learnable skill cluster
supported by the source material must have a tutorial. Every distinct real-world operational
task within the objective's scope must have a how-to. Do not collapse or merge documents
to stay under a lower number — the minimum exists because the content warrants it.

Over-production is also a failure. Do not pad with thin, contrived, or redundant documents
to reach the maximum. The maximum exists as a ceiling, not a target."""

PLANNER_SYSTEM = DIATAXIS_CONTEXT + f"""

You are the PLANNER. Your job is to produce the optimal content plan for tutorials and how-tos.
You reason carefully before deciding. You produce valid JSON only — no markdown fences, no preamble.

{QUANTITY_RULES}"""

REVIEWER_SYSTEM = DIATAXIS_CONTEXT + f"""

You are the REVIEWER. Your job is to challenge content plans and ensure they meet the quality standard.
You are adversarial by design — your default posture is skepticism. You look for:
- Under-production: tutorials below {MIN_TUTORIALS} or how-tos below {MIN_HOWTOS} — ALWAYS a failure unless
  the source material is genuinely insufficient (state specifically why if so)
- Over-production: tutorials above {MAX_TUTORIALS} or how-tos above {MAX_HOWTOS} — always a failure
- Tutorials that are redundant, artificially split, or too thin to stand alone
- How-tos that are contrived exercises rather than real operational tasks
- How-tos where the difficulty progression is flat or illogical
- Coverage gaps — skills the objective requires that no document addresses

{QUANTITY_RULES}

You approve only when the plan is genuinely optimal within the quantity constraints.
Otherwise you return a revised plan that meets all constraints.
You produce valid JSON only — no markdown fences, no preamble."""

def build_planner_prompt(feedback=None):
    base = f"""Produce the optimal content plan for tutorials and how-tos for the RHCSA objective: {objective_title}

EXPLANATION DOCUMENT (already written — derive from this, mine it for content breadth):
{explanation_clean}

SOURCE MATERIAL (first 6000 chars of mapped passages):
{mapped_content[:6000]}

QUANTITY CONSTRAINTS:
- Tutorials: minimum {MIN_TUTORIALS}, maximum {MAX_TUTORIALS}
- How-tos:   minimum {MIN_HOWTOS}, maximum {MAX_HOWTOS}
Under-production is a quality failure. Mine the explanation for every distinct learnable
skill cluster. Mine the source material for every distinct real-world operational task.

REASONING PROCESS — work through each before deciding:

1. TUTORIAL ANALYSIS
   Read the explanation carefully. What distinct hands-on skill clusters does it identify?
   List every candidate tutorial before filtering. Each tutorial teaches one focused thing
   through guided doing. Which candidates are genuinely distinct and supported by enough
   source material to stand alone?
   You must produce at least {MIN_TUTORIALS} tutorials. If you find yourself below that,
   you have missed skill clusters — re-read the explanation and source material.

2. HOW-TO ANALYSIS
   What real operational tasks does a practitioner face within this objective's scope?
   List every candidate how-to before filtering. How-tos chain from tutorials — each
   assumes the learner completed relevant tutorial(s). What is the natural difficulty
   progression: foundational → intermediate → advanced?
   You must produce at least {MIN_HOWTOS} how-tos. If you find yourself below that,
   you have missed real-world tasks — re-read the explanation and source material.

3. QUALITY VERIFICATION
   Does every item continuously maintain high effectiveness?
   Does the set constantly increase maximum efficiency (no redundancy)?
   Does the set significantly improve top performance (complete exam coverage, no gaps)?
   Are you within the quantity constraints ({MIN_TUTORIALS}-{MAX_TUTORIALS} tutorials, {MIN_HOWTOS}-{MAX_HOWTOS} how-tos)?
"""
    if feedback:
        base += f"""
REVIEWER FEEDBACK FROM PREVIOUS ITERATION:
{feedback}

Address every reviewer concern in your revised plan.
"""
    base += f"""
Output ONLY valid JSON:
{{
  "reasoning": "3-5 sentences on decisions made, how you reached the quantity for each type, and any changes from previous iteration",
  "tutorials": [
    {{
      "index": 1,
      "title": "Action-oriented tutorial title",
      "scope": "One sentence: exactly what skill this tutorial builds",
      "prerequisite_tutorials": []
    }}
  ],
  "howtos": [
    {{
      "index": 1,
      "title": "How to [specific task]",
      "scope": "One sentence: the specific real-world task",
      "difficulty": "foundational|intermediate|advanced",
      "prerequisite_tutorials": [1]
    }}
  ]
}}"""
    return base

def build_reviewer_prompt(plan_json):
    plan_str = json.dumps(plan_json, indent=2)
    t_count  = len(plan_json.get("tutorials", []))
    h_count  = len(plan_json.get("howtos", []))
    return f"""Review this content plan for the RHCSA objective: {objective_title}

EXPLANATION DOCUMENT (scope boundary and content source):
{explanation_clean[:4000]}

PROPOSED PLAN:
{plan_str}

QUANTITY CHECK (hard constraints):
- Tutorials proposed: {t_count} — must be {MIN_TUTORIALS}-{MAX_TUTORIALS}
- How-tos proposed:   {h_count} — must be {MIN_HOWTOS}-{MAX_HOWTOS}
{"QUANTITY FAILURE: " + str(t_count) + " tutorials is below the minimum of " + str(MIN_TUTORIALS) + "." if t_count < MIN_TUTORIALS else ""}
{"QUANTITY FAILURE: " + str(t_count) + " tutorials exceeds the maximum of " + str(MAX_TUTORIALS) + "." if t_count > MAX_TUTORIALS else ""}
{"QUANTITY FAILURE: " + str(h_count) + " how-tos is below the minimum of " + str(MIN_HOWTOS) + "." if h_count < MIN_HOWTOS else ""}
{"QUANTITY FAILURE: " + str(h_count) + " how-tos exceeds the maximum of " + str(MAX_HOWTOS) + "." if h_count > MAX_HOWTOS else ""}

CONTENT REVIEW CRITERIA:
1. Does the tutorial count satisfy the minimum {MIN_TUTORIALS}? If below, what skill clusters in the explanation are not covered?
2. Does the how-to count satisfy the minimum {MIN_HOWTOS}? If below, what real operational tasks are missing?
3. Are all tutorials genuinely distinct, non-overlapping, and supported by source material?
4. Are all how-tos real operational tasks — not contrived exercises or restatements of tutorial steps?
5. Is the difficulty progression logical and actually increasing?
6. Are there coverage gaps in the explanation's content that no document addresses?
7. Is there padding — documents that duplicate others or add no unique value?
8. Does the total set satisfy the quality standard: high effectiveness, maximum efficiency, top performance?

If the plan is optimal and within quantity constraints, output:
{{"approved": true, "reasoning": "one sentence confirming why this plan is optimal"}}

If the plan needs revision (including quantity violations), output:
{{"approved": false, "issues": ["specific issue 1", ...], "revised_plan": {{ ...full revised plan in same schema... }}}}

Output ONLY valid JSON. No preamble."""

# Run the planning loop
reviewer_feedback = None
final_plan        = None

for iteration in range(1, MAX_PLAN_ITERATIONS + 1):
    print(f"  Iteration {iteration}/{MAX_PLAN_ITERATIONS}:")

    plan_raw = call_sonnet(PLANNER_SYSTEM, build_planner_prompt(feedback=reviewer_feedback),
                           f"Planner (iter {iteration})", max_tokens=3000)
    try:
        current_plan = parse_plan_json(plan_raw)
    except (json.JSONDecodeError, ValueError) as e:
        print(f"  ERROR: Planner returned invalid JSON: {e}")
        print(f"  Raw: {plan_raw[:400]}")
        sys.exit(1)

    t_count = len(current_plan.get("tutorials", []))
    h_count = len(current_plan.get("howtos", []))
    print(f"    Plan: {t_count} tutorial(s), {h_count} how-to(s)")
    print(f"    Reasoning: {current_plan.get('reasoning', '')}")

    review_raw = call_sonnet(REVIEWER_SYSTEM, build_reviewer_prompt(current_plan),
                             f"Reviewer (iter {iteration})", max_tokens=3000)
    try:
        review = parse_plan_json(review_raw)
    except (json.JSONDecodeError, ValueError) as e:
        print(f"  ERROR: Reviewer returned invalid JSON: {e}")
        print(f"  Raw: {review_raw[:400]}")
        sys.exit(1)

    if review.get("approved"):
        print(f"    Reviewer: APPROVED — {review.get('reasoning', '')}")
        final_plan = current_plan
        break
    else:
        issues  = review.get("issues", [])
        revised = review.get("revised_plan")
        print(f"    Reviewer: NOT APPROVED — {len(issues)} issue(s):")
        for issue in issues:
            print(f"      - {issue}")

        if iteration == MAX_PLAN_ITERATIONS:
            print(f"  Max iterations reached. Using reviewer's revised plan as final.")
            final_plan = revised if revised else current_plan
        else:
            reviewer_feedback = (
                "Issues identified by reviewer:\n" +
                "\n".join(f"- {i}" for i in issues)
            )
            if revised:
                reviewer_feedback += f"\n\nReviewer's suggested revised plan:\n{json.dumps(revised, indent=2)}"
    print()

tutorials = final_plan.get("tutorials", [])
howtos    = final_plan.get("howtos", [])

print(f"Final plan: {len(tutorials)} tutorial(s), {len(howtos)} how-to(s)")
for t in tutorials:
    print(f"  Tutorial {t['index']}: {t['title']}")
for h in howtos:
    print(f"  How-to {h['index']} [{h['difficulty']}]: {h['title']}")
print()

# ─────────────────────────────────────────────────────────────────────────────
# STEP 3 — TUTORIALS
# ─────────────────────────────────────────────────────────────────────────────

print(f"Step 3: Writing {len(tutorials)} tutorial(s)...")

written_tutorials = []

for t in tutorials:
    idx   = t["index"]
    title = t["title"]
    scope = t["scope"]

    TUTORIAL_PROMPT = f"""Write Tutorial {idx} of {len(tutorials)} for the RHCSA objective: {objective_title}

TUTORIAL TITLE: {title}
TUTORIAL SCOPE: {scope}

TEMPLATE STRUCTURE:
{tutorial_template}

ANCHOR EXPLANATION (derive from this — do not duplicate it):
{explanation_clean}

SOURCE MATERIAL:
{mapped_content}

TUTORIAL RULES:
- Learning-oriented. Learner has no prior competence. Teacher takes full responsibility for success.
- Every step: action description → exact command → "You should see:" with expected output → observation.
- ONE path only. No alternatives, no options.
- Use "we" language throughout — teacher-learner partnership.
- Numbered steps (## Step 1:, ## Step 2:, etc.).
- Required sections: Prerequisites, What We'll Build (concrete terminal state), numbered steps, What We Accomplished, Next Steps.
- No explanation dumps — one sentence max for "why", then link to explanation.
- No reference tables — link to reference doc.
- YAML frontmatter: title, type: tutorial, exam_objective: {objective_id}, tutorial_index: {idx}, version: "1.0", status: draft
- FRONTMATTER: bare --- delimiters only — NEVER wrap in ```yaml``` code fences.
- Strip all <!-- GUIDANCE --> template comments.
- Do NOT include <!-- Source: --> attribution comments.

Output the complete Tutorial {idx} document only. No preamble."""

    tut_doc   = call_sonnet(DIATAXIS_CONTEXT, TUTORIAL_PROMPT, f"Tutorial {idx:02d}")
    tut_path  = f"{OUTPUT_DIR}/{objective_id}_tutorial_{idx:02d}.md"
    tut_clean = write_doc(tut_path, tut_doc)
    written_tutorials.append({"index": idx, "title": title, "content": tut_clean})

print()

# ─────────────────────────────────────────────────────────────────────────────
# STEP 4 — HOW-TOS
# ─────────────────────────────────────────────────────────────────────────────

print(f"Step 4: Writing {len(howtos)} how-to(s)...")

all_tutorial_context = "\n\n---\n\n".join(
    f"TUTORIAL {t['index']}: {t['title']}\n{t['content'][:2000]}"
    for t in written_tutorials
)

for h in howtos:
    idx        = h["index"]
    title      = h["title"]
    scope      = h["scope"]
    difficulty = h["difficulty"]

    HOWTO_PROMPT = f"""Write How-to {idx} of {len(howtos)} for the RHCSA objective: {objective_title}

HOW-TO TITLE: {title}
HOW-TO SCOPE: {scope}
DIFFICULTY LEVEL: {difficulty}

TEMPLATE STRUCTURE:
{howto_template}

ANCHOR EXPLANATION (scope boundary):
{explanation_clean[:3000]}

TUTORIALS WRITTEN (learner has completed these):
{all_tutorial_context}

SOURCE MATERIAL:
{mapped_content[:6000]}

HOW-TO RULES:
- Task-oriented. Assumes competence. User is working, not studying.
- Imperative mood throughout — no "we" language, no teaching tone.
- One sentence of context max, then straight to task.
- Variations and conditionals allowed — real tasks have real choices.
- Required sections: Before You Begin (assumes competence), Steps (numbered), Verification (brief), Troubleshooting (table min 3 rows), Related.
- Verification: brief expected state — NOT "You should see:" with exact output.
- Difficulty {difficulty}: {"straightforward single-skill application" if difficulty == "foundational" else "combines multiple skills or operational edge cases" if difficulty == "intermediate" else "real-world complexity, failure modes, or combined skills under constraints"}.
- YAML frontmatter: title, type: how-to, exam_objective: {objective_id}, howto_index: {idx}, difficulty: {difficulty}, version: "1.0", status: draft
- FRONTMATTER: bare --- delimiters only — NEVER wrap in ```yaml``` code fences.
- Strip all <!-- GUIDANCE --> template comments.
- Do NOT include <!-- Source: --> attribution comments.

Output the complete How-to {idx} document only. No preamble."""

    howto_doc  = call_sonnet(DIATAXIS_CONTEXT, HOWTO_PROMPT, f"How-to {idx:02d} [{difficulty}]")
    howto_path = f"{OUTPUT_DIR}/{objective_id}_howto_{idx:02d}.md"
    write_doc(howto_path, howto_doc)

print()

# ─────────────────────────────────────────────────────────────────────────────
# STEP 5 — REFERENCE
# ─────────────────────────────────────────────────────────────────────────────

print("Step 5: Writing Reference...")

REFERENCE_PROMPT = f"""Write a complete Reference document for the RHCSA objective: {objective_title}

TEMPLATE STRUCTURE:
{reference_template}

ANCHOR EXPLANATION (scope boundary):
{explanation_clean[:3000]}

SOURCE MATERIAL:
{mapped_content}

REFERENCE RULES:
- Information-oriented. Describes the system. No instructions, no opinions.
- Structure: Syntax → Option Forms → Built-in Commands → Key Variables → Keyboard Shortcuts → Files and Paths → Exit Codes → Examples → Notes and Constraints → See Also.
- Tables dominate. Prose only where tables cannot capture the information.
- Examples: short code blocks illustrating syntax, no narrative.
- Notes and Constraints: factual bullet points only.
- Zero instructional language. Zero opinion.
- YAML frontmatter: title, type: reference, exam_objective: {objective_id}, version: "1.0", status: draft
- FRONTMATTER: bare --- delimiters only — NEVER wrap in ```yaml``` code fences.
- Strip all <!-- GUIDANCE --> template comments.
- Do NOT include <!-- Source: --> attribution comments.

Output the complete Reference document only. No preamble."""

ref_doc  = call_sonnet(DIATAXIS_CONTEXT, REFERENCE_PROMPT, "Reference")
ref_path = f"{OUTPUT_DIR}/{objective_id}_reference.md"
write_doc(ref_path, ref_doc)
print()

# ─────────────────────────────────────────────────────────────────────────────
# SUMMARY
# ─────────────────────────────────────────────────────────────────────────────

all_outputs = []
for f in sorted(os.listdir(OUTPUT_DIR)):
    if f.startswith(objective_id) and f.endswith(".md"):
        full = os.path.join(OUTPUT_DIR, f)
        all_outputs.append((f, os.path.getsize(full)))

print("Stage 3 complete.")
print()
for fname, size in all_outputs:
    print(f"  {fname} ({size:,} bytes)")
print()
print(f"  Total: {len(all_outputs)} documents")
print(f"    1 explanation  |  {len(tutorials)} tutorial(s)  |  {len(howtos)} how-to(s)  |  1 reference")
print()
print(f"Run quality gate:")
print(f"  python3 stage3_verify.py {OUTPUT_DIR}/{objective_id}")
