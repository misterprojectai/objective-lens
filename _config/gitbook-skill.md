---
name: gitbook-external-editing
description: Use when editing GitBook documentation in external environments (Cursor, Claude Code, VS Code, CLI, or any editor outside the GitBook UI), working with Git-synced repositories, managing SUMMARY.md navigation structure, authoring custom blocks (tabs, hints, steppers, columns), configuring frontmatter, or setting up variables and Git Sync workflows.
---

# GitBook External Editing

## When to Use This Skill

Use when working with GitBook documentation through:
- Git-synced repositories (GitHub, GitLab)
- Local markdown editors or IDEs
- Command-line tools
- Any environment editing GitBook content as files rather than through the GitBook UI

## Quick Reference

### File Structure

```
/
  .gitbook/
    assets/              # GitBook-managed images and files
    includes/            # Reusable content blocks
    vars.yaml            # Space-level variables
  .gitbook.yaml          # Configuration
  README.md              # Homepage
  SUMMARY.md             # Table of contents
  getting-started/
    installation.md
    quickstart.md
  api-reference/
    authentication.md
    endpoints.md
```

### Frontmatter Template

```markdown
---
description: Page description for SEO
icon: book-open
hidden: true
vars:
  page_variable: value
if: visitor.claims.unsigned.condition
layout:
  width: default  # or 'wide'
  title:
    visible: true
  description:
    visible: true
  tableOfContents:
    visible: true
  outline:
    visible: true
  pagination:
    visible: true
  metadata:
    visible: true
---
```

### Block Selection Table

| Need | Use | Why |
|---|---|---|
| Sequential, ordered instructions | `{% stepper %}` | Guides users through multi-step processes |
| Alternative options (languages, platforms) | `{% tabs %}` | Lets users choose relevant option |
| Optional or detailed information | `<details>` | Keeps page scannable |
| Important warnings or tips | `{% hint %}` | Draws attention with colored styling |
| Side-by-side comparisons | `{% columns %}` | Shows related info in parallel (max 2) |
| Timeline or changelog | `{% updates %}` | Displays dated entries reverse-chronological |
| Visual navigation cards | `<table data-view="cards">` | Creates clickable card grid |
| Downloadable files | `{% file %}` | Provides files with captions |
| Call-to-action links | `<a class="button">` | Highlights primary/secondary actions |
| Reusable content across pages | `{% include %}` | Maintains consistency |
| Dynamic content | `<code class="expression">` | Displays variable values automatically |

### Variable Scope

| If variable is... | Define as... | Access with... |
|---|---|---|
| Used across multiple pages | Space-level in `/.gitbook/vars.yaml` | `space.vars.variableName` |
| Specific to one page | Page-level in frontmatter `vars:` | `page.vars.variableName` |

### Key Reminders

- Read `SUMMARY.md` first when working with existing content
- Test in GitBook after editing locally
- Keep `SUMMARY.md` synchronized with file structure
- Space variables: `/.gitbook/vars.yaml`; page variables: frontmatter `vars:`
- OpenAPI specs must be uploaded via API/CLI/UI — cannot be embedded in markdown

---

## Working with Existing Content

1. **Read SUMMARY.md first** — contains complete table of contents, hierarchy, relative paths
2. **If SUMMARY.md missing** — GitBook inferred structure from directory layout; browse directory
3. **Check .gitbook.yaml** — root documentation dir, custom README/SUMMARY paths, existing redirects
4. **Explore .gitbook/assets/** — all uploaded images and files referenced in docs
5. **Check .gitbook/vars.yaml** — space-level variables if defined

---

## Configuration Files

### .gitbook.yaml

```yaml
root: ./

structure:
  readme: ./README.md
  summary: ./SUMMARY.md

redirects:
  old-page: new-page.md
  help: support.md
```

**Options:**
- `root`: Root directory for documentation (default: `./`)
- `structure.readme`: Homepage path (default: `./README.md`)
- `structure.summary`: Table of contents path (default: `./SUMMARY.md`)
- `redirects`: Key-value pairs mapping old URLs to new page paths

**Monorepo support:**

```
/
  packages/
    docs/
      .gitbook.yaml
      README.md
      SUMMARY.md
    api/
      .gitbook.yaml
      README.md
      SUMMARY.md
```

Configure "Project directory" in Git Sync to point to subdirectory containing `.gitbook.yaml`.

**Notes:**
- Paths in `.gitbook.yaml` relative to `root` option
- Redirects are space-specific (not site-wide)
- For site-wide redirects, use GitBook UI
- When using Git Sync, manage README only through repository

### .gitbook Directory

```
.gitbook/
  assets/          # Uploaded images and files
  includes/        # Reusable content blocks (individual .md files)
  vars.yaml        # Space-level variables
```

**Notes:**
- Assets: images uploaded through GitBook UI stored in `.gitbook/assets/`
- Reusable content: each block exported as separate .md file in `.gitbook/includes/`
- Variables: space-level stored in `.gitbook/vars.yaml` as key-value pairs
- References: `{% include "/reusable-content/rc12345" %}`
- Images: `![alt](../.gitbook/assets/image-name.svg)`
- `.gitbook/includes` folder may appear in TOC — manually hide if needed
- In monorepos, `.gitbook` created at root of each synced space

### SUMMARY.md

```markdown
# Summary

## Use headings to create page groups like this one

* [First page's title](page1/README.md)
    * [Some child page](page1/page1-1.md)
    * [Some other child page](page1/page1-2.md)
* [Second page's title](page2/README.md)
    * [Some child page](page2/page2-1.md)

## A second page group

* [Another page](another-page.md)
```

**Key rules:**
- `#` for main title
- `##` headings create page groups (sidebar section headers)
- `*` for unordered lists defining pages and subpages
- Indent with spaces (not tabs) for nested/child pages
- Each list item = markdown link: `[Link text](path/to/file.md)`
- Paths relative to location in `.gitbook.yaml`

**Optional sidebar title:**

```markdown
* [Page main title](page.md "Page link title")
```

Text in quotes used in: TOC sidebar, pagination buttons, relative links.

**Notes:**
- SUMMARY.md optional — GitBook infers from folder hierarchy if absent
- Cannot reference same markdown file twice (each page has one URL)
- GitBook auto-updates SUMMARY.md when editing through UI

---

## Markdown Formatting

**Standard:**

```markdown
# Heading 1
## Heading 2
### Heading 3

**bold text**
*italic text*
`inline code`

- Bullet list item
  - Nested item

1. Numbered list
2. Second item

[Link text](https://example.com)
[Internal link](getting-started.md)
```

**Code blocks with titles:**

````markdown
{% code title="index.js" %}
```javascript
const foo = 'bar';
console.log(foo);
```
{% endcode %}
````

**Links:**
- External: `[text](https://example.com)`
- Internal: `[text](page.md)`, `[text](../folder/page.md)`
- Email: `[text](mailto:email@example.com)`

**Math/TeX:**

```markdown
Inline: $$E = mc^2$$

Block:
$$
E = mc^2
$$
```

---

## Page Frontmatter

**All available fields:**

```markdown
---
description: Page description for SEO and page previews
icon: book-open
hidden: true
vars:
  page_variable: value
  another_var: another value
if: visitor.claims.unsigned.isPremium
layout:
  width: default
  title:
    visible: true
  description:
    visible: true
  tableOfContents:
    visible: true
  outline:
    visible: true
  pagination:
    visible: true
  metadata:
    visible: true
---
```

**Field reference:**

- `description` — Page description; supports multiline with `>-` syntax
- `icon` — Font Awesome icon name (e.g., `book-open`, `bolt`, `stars`, `brackets-curly`)
- `hidden: true` — Hides page from published TOC
- `vars` — Page-level variables referenced in expressions
- `if` — Adaptive content visibility based on visitor attributes (prefer GitBook UI for maintainability)
- `layout.width` — `default` or `wide`
- `layout.title.visible` — Show/hide page title
- `layout.description.visible` — Show/hide page description
- `layout.tableOfContents.visible` — Show/hide left sidebar TOC
- `layout.outline.visible` — Show/hide right sidebar headings
- `layout.pagination.visible` — Show/hide next/previous navigation
- `layout.metadata.visible` — Show/hide metadata section

**Landing page example (minimal chrome):**

```yaml
layout:
  width: wide
  title:
    visible: true
  description:
    visible: true
  tableOfContents:
    visible: false
  outline:
    visible: false
  pagination:
    visible: false
```

---

## Variables and Expressions

### Variable Storage

**Space-level** (`/.gitbook/vars.yaml`):

```yaml
food: apple
latest_version: v3.0.4
company_name: Acme Corp
```

**Page-level** (frontmatter):

```markdown
---
vars:
  page_food: orange
  page_version: v2.1.0
---
```

### Expression Syntax

```markdown
<code class="expression">JavaScript expression here</code>
```

**Examples:**

```markdown
<!-- Simple expression -->
<code class="expression">1 + 1</code>

<!-- Space-level variable -->
<code class="expression">space.vars.latest_version</code>

<!-- String concatenation -->
<code class="expression">"My favorite food is " + space.vars.food</code>

<!-- Page-level variable -->
<code class="expression">page.vars.page_food</code>

<!-- Conditional -->
<code class="expression">space.vars.latest_version === "v3.0.4" ? "Latest" : "Outdated"</code>
```

---

## GitBook Custom Blocks

### Tabs

Use tabs to present alternative content like different programming languages or platform-specific instructions.

**When to use:** Comparing alternatives (code in different languages, platform-specific commands, configuration options).

```markdown
{% tabs %}
{% tab title="JavaScript" %}
```javascript
const greeting = 'Hello World';
console.log(greeting);
```
{% endtab %}

{% tab title="Python" %}
```python
greeting = "Hello World"
print(greeting)
```
{% endtab %}
{% endtabs %}
```

### Stepper

Use steppers for sequential, multi-step processes where order matters.

**When to use:** Tutorials, installation guides, how-to guides, onboarding checklists, any sequential process.

```markdown
{% stepper %}
{% step %}
## First step

Complete initial setup by installing required dependencies.
{% endstep %}

{% step %}
## Second step

Configure environment variables in `.env` file.
{% endstep %}

{% step %}
## Third step

Run application with `npm start`.
{% endstep %}
{% endstepper %}
```

### Hints

Use hints to highlight important information without disrupting flow. Supported styles: `info`, `warning`, `danger`, `success`.

**When to use:** Supplementary information, call-outs, best practices, warnings, troubleshooting tips.

```markdown
{% hint style="info" %}
Informational hint with helpful context.
{% endhint %}

{% hint style="warning" %}
Be careful when running this command in production.
{% endhint %}

{% hint style="danger" %}
This action cannot be undone. Make sure you have backups.
{% endhint %}

{% hint style="success" %}
Configuration saved successfully!
{% endhint %}
```

### Expandable

Use expandable sections for optional content that doesn't need to be visible by default.

**When to use:** Optional deep-dives, advanced explanations, lengthy logs, FAQ answers, content that would clutter the page.

```markdown
<details>
<summary>Advanced Configuration Options</summary>

Detailed information about advanced settings most users won't need.

```yaml
advanced:
  option1: value1
  option2: value2
```
</details>
```

### Columns (max 2)

Use columns to present content side-by-side (2 columns maximum).

**When to use:** Side-by-side comparisons (pros vs cons), before/after examples, parallel instructions.

```markdown
{% columns %}
{% column %}
### Before

Old inefficient implementation.
{% endcolumn %}

{% column %}
### After

New optimized approach.
{% endcolumn %}
{% endcolumns %}
```

### Updates

Use updates blocks for product updates, release notes, or changelogs.

**When to use:** Changelog pages, release notes, version updates, product announcements.

```markdown
{% updates format="full" %}
{% update date="2024-01-15" %}
# Version 2.0 Released

Added dark mode and improved search.
{% endupdate %}

{% update date="2024-01-01" %}
# Bug Fixes

Fixed community-reported issues.
{% endupdate %}
{% endupdates %}
```

### Cards

Use cards to create visual, clickable navigation elements. Cards are HTML tables with special attributes.

**When to use:** Dashboards, feature overviews, linking to related pages, showcasing multiple resources.

```markdown
<table data-view="cards">
    <thead>
        <tr>
            <th>Title</th>
            <th data-card-target data-type="content-ref">Target</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Getting Started Guide</td>
            <td><a href="getting-started/quickstart.md">Quick Start</a></td>
        </tr>
        <tr>
            <td>API Reference</td>
            <td><a href="api-reference/overview.md">API Docs</a></td>
        </tr>
        <tr>
            <td>Examples</td>
            <td><a href="/spaces/abc1234/pages/jkl1121">Code Examples</a></td>
        </tr>
    </tbody>
</table>
```

### Embeds

Use embeds to include external content like videos, interactive demos, or social media.

**When to use:** Demonstration videos, interactive code sandboxes, tweets, external rich media.

```markdown
{% embed url="https://www.youtube.com/watch?v=dQw4w9WgXcQ" %}

{% embed url="https://codepen.io/username/pen/example" %}
```

### Files

Use file blocks to provide downloadable files with captions.

```markdown
{% file src="https://example.com/document.pdf" %}
Complete documentation in PDF format.
{% endfile %}
```

### Buttons

Use buttons for clear call-to-action links. Supported styles: `primary`, `secondary`.

**When to use:** Download links, "Try it now" actions, external resource navigation.

```markdown
<a href="https://example.com/download" class="button primary">Download Now</a>

<a href="https://docs.example.com" class="button secondary">View Documentation</a>
```

**With icon (Font Awesome name without `fa-` prefix):**

```markdown
<a href="https://github.com/user/repo" class="button primary" data-icon="github">View on GitHub</a>
```

### Icons

Inline icons from Font Awesome can enhance text readability.

**When to use:** Visual indicators, status icons, improving scannability.

```markdown
<i class="fa-check">check</i> Feature enabled
<i class="fa-warning">warning</i> Requires configuration
<i class="fa-info-circle">info</i> Learn more
```

### Reusable Content

Reusable content blocks let you sync content across multiple pages.

**When to use:** Call-to-actions, disclaimers, repeated instructions, any content that needs to stay consistent across pages.

```markdown
{% include "/reusable-content/rc12345" %}
```

Note: Reusable content blocks created through GitBook UI, given unique IDs. Different from pages.

### OpenAPI Specifications

**Cannot embed directly in markdown.** Upload via:
1. GitBook API — [OpenAPI endpoints](https://docs.gitbook.com/developers/gitbook-api/api-reference/openapi)
2. GitBook CLI — `gitbook openapi` command
3. GitBook UI

**Once uploaded**, reference in markdown:

```markdown
{% openapi src="https://api.example.com/openapi.json" path="/users" method="get" %}
[https://api.example.com/openapi.json](https://api.example.com/openapi.json)
{% endopenapi %}
```

### Nested Markdown in Custom Blocks

Standard markdown works inside custom block tags:

````markdown
{% tabs %}
{% tab title="Example" %}
This tab contains markdown:

- Bullet points work
  - Nested bullets too
- **Bold text** and *italic text*
- `inline code`

```javascript
// Code blocks work too
const example = true;
```
{% endtab %}
{% endtabs %}
````

---

## Common Pitfalls

**File organization:**
- Don't reference same markdown file twice in SUMMARY.md
- Keep file paths consistent between SUMMARY.md and actual file locations
- Use relative paths consistently

**Configuration conflicts:**
- When using Git Sync, manage README.md only through repository
- Keep .gitbook.yaml at correct root level
- Test redirects after moving or renaming files

**Markdown formatting:**
- Tables and columns discouraged — use custom blocks instead
- Avoid excessive nested lists
- Don't mix tab/space indentation in SUMMARY.md

**Custom blocks:**
- Always close blocks properly (`{% endtab %}`, `{% endhint %}`, etc.)
- Match opening and closing tags exactly
- Test custom blocks in GitBook after editing locally

---

## Git Sync Workflow

1. Changes in Git automatically update GitBook
2. Changes in GitBook automatically commit to Git
3. GitBook maintains SUMMARY.md based on UI edits
4. Resolve merge conflicts in Git

**Best practices:**
- Make structural changes (navigation) through SUMMARY.md in Git
- Make content changes consistently in Git OR GitBook UI (not both)
- Review auto-generated commits from GitBook
- Use branch-based workflows for significant updates
- Test in preview before merging to main

---

## Complete Page Example

````markdown
---
description: Learn to authenticate with our API using API keys or OAuth 2.0.
icon: lock
---

# API Authentication Guide

{% hint style="info" %}
All API requests require authentication. Choose the method that best fits your use case.
{% endhint %}

## Authentication Methods

{% tabs %}
{% tab title="API Key" %}
Simplest method. Include API key in request header:

```bash
curl -H "X-API-Key: your-api-key" https://api.example.com/v1/users
```

{% hint style="warning" %}
Never commit API keys to version control. Use environment variables instead.
{% endhint %}
{% endtab %}

{% tab title="OAuth 2.0" %}
More secure for user-facing applications:

{% stepper %}
{% step %}
## Register your application

Get client ID and secret from developer dashboard.
{% endstep %}

{% step %}
## Request authorization

Redirect users to OAuth endpoint.
{% endstep %}

{% step %}
## Exchange code for token

Use authorization code to get access token.
{% endstep %}
{% endstepper %}
{% endtab %}
{% endtabs %}

## Rate Limits

{% columns %}
{% column %}
### Free Tier
1,000 requests/hour
10,000 requests/day
{% endcolumn %}

{% column %}
### Pro Tier
10,000 requests/hour
100,000 requests/day
{% endcolumn %}
{% endcolumns %}

<details>
<summary>Need higher limits?</summary>

Contact sales team to discuss enterprise plans with custom rate limits and SLAs.
</details>

<a href="https://example.com/signup" class="button primary" data-icon="rocket">Get Started</a>
````
