# Stage 4 — Publish
**ICM Layer: L2 (Stage Contract)**

Transform Stage 3 Diataxis documents into GitBook-formatted markdown and publish to the live documentation site. Stage 4 runs in two passes: Pass A generates the GitBook documents and pushes them live. Pass B injects iximiuz lab links into those documents after Stage 5 completes.

---

## Inputs

### Pass A — `stage4_run.py`

- `03_diataxis/output/<obj>/` — SOURCE (L4): The complete set of Diataxis documents for the objective. Fourteen files per objective: one explanation, one reference, six tutorials, six how-tos. Transform these.
- `_config/gitbook-blocks.md` — REFERENCE (L3): Complete GitBook block syntax reference — `{% stepper %}`, `{% hint %}`, `{% tabs %}`, `{% code %}`, cards, expandables. Load before writing any block. Never guess syntax.
- `_config/gitbook-skill.md` — REFERENCE (L3): GitBook authoring conventions, SUMMARY.md structure rules, frontmatter options, page option patterns. Load before writing.
- `04_publish/output/SUMMARY.md` — SOURCE (L4): The live navigation file. Read current state before modifying. Append new objective section; never overwrite existing sections.

### Pass B — `stage4b_run.py` (runs after Stage 5 completes)

- `05_iximiuz/output/<obj>-manifest.json` — SOURCE (L4): Deployed iximiuz server names for all 24 content items (tutorials, howtos, challenges, broken challenges). This file must exist before Pass B can run. If it does not exist, run `build_manifest.py <obj>` first.
- `04_publish/output/<obj>/` — SOURCE (L4): The GitBook documents written by Pass A. Pass B appends iximiuz embed sections to these files — it does not rewrite them.

---

## Process

### Pass A — GitBook Document Generation

1. **Load reference files.** Read `_config/gitbook-blocks.md` and `_config/gitbook-skill.md` completely before writing any document. These constrain every block choice in the output.

2. **Transform each Stage 3 document to GitBook format.** Apply the following per document type:
   - **Explanation:** Convert to GitBook markdown. Use `{% hint %}` for key callouts, expandables for optional deep-dives, cards block for navigation links to companion documents. Do NOT use steppers — Explanation has no steps.
   - **Tutorials:** Convert step-by-step sections to `{% stepper %}` blocks. Each step becomes a stepper item with a heading and body. Use `{% hint style="info" %}` for exam tips, `{% hint style="warning" %}` for destructive commands.
   - **How-tos:** Convert each task to a clean numbered list. Use `{% hint style="warning" %}` for caution points. Use code blocks with captions for each command sequence.
   - **Reference:** Convert to tables and code blocks. No steppers, no hint blocks except for `{% hint style="danger" %}` on destructive operations.

3. **Apply platform separation.** Scan every output file before writing. If any MDC syntax appears (`::simple-task`, `::remark-box`, `:tasks:`, `::hint-box`), remove it. GitBook does not render iximiuz MDC. This is a hard platform separation violation if it reaches production.

4. **Write output files** to `04_publish/output/<obj>/` using Stage 4 naming convention. Update `SUMMARY.md` by appending the new objective section. Never touch existing objective sections.

5. **Commit and push.** GitBook syncs automatically from the GitHub push. Wait for sync confirmation before marking Pass A complete.

6. **Self-check before marking Pass A done.** Open the live GitBook URL for the objective's explanation page. Verify:
   - Page renders without raw Liquid block text visible
   - Navigation links between companion documents resolve correctly
   - SUMMARY.md shows the objective in the left sidebar
   If any check fails, fix before running Pass B.

### Pass B — iximiuz Link Injection

1. **Verify manifest exists.** Check `05_iximiuz/output/<obj>-manifest.json`. If absent, stop. Run `python3 build_manifest.py <obj>` first. Pass B cannot run without it.

2. **Update explanation.md** with the full three-section hub:
   - Section 1: Guided Tutorials (6 embeds from manifest `tutorials` keys)
   - Section 2: Practice Challenges (6 embeds from manifest `challenges` keys)
   - Section 3: Advanced — Broken Environment (6 embeds from manifest `challenges_broken` keys)
   Replace the existing `## Practice on a Live System` section if present. Do not duplicate it.

3. **Update each tutorial_NN.md** with a single `## Practice This Lab` section at the bottom containing one iximiuz tutorial embed matched by index.

4. **Update each howto_NN.md** with a `## Test Yourself` section at the bottom containing one clean challenge embed and one broken environment link, matched by index. If no broken challenge exists for that index, omit the Advanced link — do not substitute the clean challenge URL.

5. **Create practice-labs.md** as a dedicated hub page listing all 24 items in three sections. Overwrite if it already exists — always reflects current manifest state.

6. **Update SUMMARY.md** to add `practice-labs.md` to the objective's section. Insert after the last howto entry. Skip if already present.

7. **Commit and push.** Include the manifest JSON in the commit — it is part of the pipeline state record.

---

## Output

- **Format:** GitBook-flavored markdown — Liquid block syntax only. Never MDC.
- **Write to:** `04_publish/output/<obj>/`
- **Naming convention (Pass A):**
  ```
  explanation.md
  tutorial_01.md  through  tutorial_06.md
  howto_01.md     through  howto_06.md
  reference.md
  ```
- **Naming convention (Pass B additions):**
  ```
  practice-labs.md        ← new page
  explanation.md          ← updated with hub
  tutorial_NN.md          ← updated with Practice This Lab
  howto_NN.md             ← updated with Test Yourself
  ```
- **Must include:**
  - All GitBook Liquid blocks rendered correctly — no raw `{%` text visible on live site
  - SUMMARY.md updated with objective section (Pass A) and practice-labs.md entry (Pass B)
  - Source Diataxis document headings preserved — page titles must match Stage 3 titles
  - iximiuz embeds matched by index — tutorial_01 links to iximiuz tutorial 1, howto_04 links to challenge 4
  - Manifest JSON committed alongside GitBook changes (Pass B)
- **Must NOT include:**
  - iximiuz MDC syntax (`::simple-task`, `::remark-box`, `::hint-box`, `:tasks:`, `::details-box`)
  - Stage 3 template guidance comments (`<!-- PURPOSE:`, `<!-- IRON LAW:`)
  - Confidence reports or AI self-assessment scores
  - Unfilled placeholder text from Stage 3 templates
  - Direct edits to pages from other objectives — only the current objective's files
  - Duplicate `## Practice on a Live System` sections (Pass B is idempotent — replace, do not append)

---

## Done Looks Like

**Pass A:** All 14 GitBook pages for the objective are live and rendering correctly at the published GitBook URL, SUMMARY.md shows the objective in the left sidebar, and no raw Liquid block syntax is visible on any page.

**Pass B:** explanation.md has the three-section hub with all 24 iximiuz embeds, every tutorial_NN.md ends with `## Practice This Lab` + one embed, every howto_NN.md ends with `## Test Yourself` + one challenge embed, practice-labs.md exists and is in SUMMARY.md, and the manifest JSON is committed.

---

## Common Failure Modes

**Failure 1 — iximiuz MDC syntax in GitBook output.**
What goes wrong: Stage 4 agent carries over `::simple-task` or `::remark-box` syntax from Stage 3 source documents.
How to detect: GitBook renders raw `::simple-task` or `::remark-box` text visible on the live page, or Pass A self-check catches raw MDC in output files.
How to fix: Strip all `::` MDC blocks from the output files. Re-run the affected document through `stage4_run.py` with the platform separation constraint enforced.

**Failure 2 — SUMMARY.md existing sections overwritten.**
What goes wrong: Stage 4 agent rewrites SUMMARY.md from scratch instead of appending.
How to detect: Previously published objectives disappear from the GitBook sidebar.
How to fix: `git revert` the SUMMARY.md commit. Re-run Stage 4 with explicit instruction to append only.

**Failure 3 — Pass B runs before Stage 5 manifest exists.**
What goes wrong: `stage4b_run.py` runs against a missing or empty manifest, writing empty embed sections to all pages.
How to detect: GitBook pages show `## Practice on a Live System` with no content below it, or `stage4b_run.py` exits with "Manifest not found" error.
How to fix: Run `python3 build_manifest.py <obj>`, verify manifest has all 24 items, then re-run `stage4b_run.py`.

**Failure 4 — Duplicate `## Practice on a Live System` section.**
What goes wrong: Pass B appends the hub instead of replacing it — two sections appear on the explanation page.
How to detect: Explanation page shows the section header twice on the live site.
How to fix: `stage4b_run.py` uses marker detection to replace, not append. Check that the marker string `## Practice on a Live System` matches exactly what is in the file — whitespace or character differences prevent detection.

**Failure 5 — GitBook sync fails silently after push.**
What goes wrong: Git push succeeds but GitBook does not sync (API webhook failure, git sync paused).
How to detect: Pages on the live site do not reflect the latest commit content.
How to fix: Open GitBook Space → Integrations → Git Sync → trigger manual sync. If sync is paused, resume it before re-running Stage 4.

**Failure 6 — howto_NN embed uses wrong challenge index.**
What goes wrong: howto_04.md receives the challenge-1 embed instead of challenge-4 because manifest key lookup used wrong index.
How to detect: Click through each howto embed on GitBook — the challenge name should contain the same number as the how-to file.
How to fix: Verify `build_manifest.py` output — each howto index must map to the challenge of the same index. If server names are wrong, re-run `build_manifest.py` and `stage4b_run.py`.
