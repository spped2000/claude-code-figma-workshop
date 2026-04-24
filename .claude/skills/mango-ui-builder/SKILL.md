---
name: mango-ui-builder
description: Build HTML/CSS/JS for Mango ERP (construction/real estate) from Figma reference or spec. Enforces: data from CSV only (no fabrication), Mango design tokens, runtime fetch (CSV changes → browser refresh updates), effort proportional to task size.
---

# Rules

## 1. Task size → effort

| Size | Examples | Do | Skip |
|---|---|---|---|
| **XS** | change color, typo, single CSS value | Edit only, 1-line confirm | Re-read files, cross-check, preview |
| **S** | add column, tweak filter | Edit + check changed field source | Full layout description |
| **M** | new section, swap chart | Full protocol | — |
| **L** | new page from scratch | Full protocol + 5-bullet layout before code | — |

Pick XS if user says "แค่" / "นิดเดียว" / "ลองเปลี่ยน".

## 2. Data

- **Source order:** live API → DB → CSV in `mock-data/` → hardcoded (last resort)
- **Fetch at runtime** in JS (`fetch(CSV_URL).then(parseCSV)`) — never hardcode rows in HTML
- Missing data → `<span class="placeholder" data-todo="...">[label]</span>` — do not invent

## 3. Design tokens

- Read `figma/design_tokens.json` before CSS
- Copy colors/spacing/fonts to CSS custom properties
- No framework (Bootstrap/Tailwind/MUI) unless user insists

## 4. Output

- Single HTML file, inline `<style>` + `<script>` (CDN OK)
- Semantic tags (`<header>`, `<nav>`, `<main>`, `<aside>`, `<section>`)
- Thai content, English class/id
- Under 500 lines; responsive (≥1 `@media`)

## 5. Path resolution (before creating new file)

1. Glob for existing file with same name
2. If found elsewhere → ask user (use / move / create elsewhere)
3. Default paths: demo → `demos/demo-b/src/`, prod → `src/<module>/`
4. Never create at `<cwd>/src/` if subfolder structure exists

## 6. Cross-check table (size-dependent)

- **XS:** skip
- **S:** changed fields only
- **M/L:** full table

Columns: `Field | Source (file:row:field) | Confidence (✅ exact / ✅ derived / ⚠️ fabricated)`
Any ⚠️ fabricated → mark in HTML with `class="placeholder"` + `<!-- TODO -->`

## 7. Live preview

Launch only if M/L, or user asks ("preview", "รัน", "ดูหน้า"), or no server on port 8080-8099.
Skip if server already running → tell user to hard-refresh (Ctrl+Shift+R).

Helper:
```bash
python .claude/skills/mango-ui-builder/scripts/preview.py <html-path> [port]
```
Auto-detects project root (`.claude/`, `.git`, `pyproject.toml`, `mock-data/`).

## 8. Verify (optional, for M/L)

```bash
python .claude/skills/mango-ui-builder/scripts/verify.py <html-path>
```
Checks: parse, broken refs, JS syntax, secrets, a11y.

## 9. Stop

```bash
bash .claude/skills/mango-ui-builder/scripts/stop.sh [port]
```

---

## Reporting

After editing, reply briefly:
- **XS/S:** 1-3 lines (what changed + where + refresh)
- **M/L:** cross-check table + preview URL + any fabricated fields flagged
