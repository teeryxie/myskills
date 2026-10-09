---
name: tokens
description: "Audit or establish the project's 3-layer token spine. Invoke when the user asks for tokens on their UI, or mentions 'tokens' alongside design / UI / frontend work."
---

<!-- HARNESS MIRROR — do not edit here. Canonical source: skills/ or commands/. After editing source, copy into cli/assets/<harness>/ and repo-root harness mirrors. -->

**Context:** this sub-skill is one lens of the broader `ui-craft` skill. If the `ui-craft` skill is also installed, read its SKILL.md first for Discovery + Anti-Slop + Craft Test, then apply the specific lens below.

Read the relevant sections of `../ui-craft/references/tokens.md` when needed. Layers, categories and themes are scoped to current product requirements, not mandatory additions to every task.

---

## Step 1: Detect existing tokens

Scan for token definitions in the project:
- CSS variables in `:root`, `[data-theme]`, `[data-mode]`, or theme wrapper selectors
- Tailwind config (`tailwind.config.js/ts`) under `theme.extend` or `theme`
- CSS-in-JS theme objects (`theme.ts`, `*.styles.ts`, `styled.d.ts`, `ThemeProvider`)
- `design-tokens.json` or `tokens.json` (Style Dictionary / Theo)
- `globals.css`, `variables.css`, `tokens.css`

Build an inventory: which of the 7 categories exist (color / spacing / type / radii / shadows / motion / z-index), which layers are present (primitive / semantic / component), and whether both light and dark are defined.

---

## Step 2: Route based on `$ARGUMENTS` and inventory

- **"audit"** → run audit only (Step 3). No proposals.
- **"establish"** → skip audit, go to Step 4.
- **"color" / "spacing" / "type" / "radii" / "shadows" / "motion" / "z-index"** → focus the audit and any proposal on that one category.
- **empty** → if tokens exist: audit. If nothing found: establish.

---

## Step 3: Audit (tokens exist)

Evaluate the applicable contract in `../ui-craft/references/tokens.md`. Output a severity-ranked gap list — don't propose code yet.

Check:

1. **Layer coverage** — require only layers justified by current reuse and theming needs; component tokens remain optional until a component needs them.
2. **Category coverage** — check categories used by the requested surface; unused categories are N/A, not missing features.
3. **Intentional dark mode** — assess only if supported by the product or requested. Verify contrast and hierarchy; aesthetic defaults alone are not correctness failures.
4. **Naming discipline** — are primitives named for values (`--gray-500`) not roles (`--button-bg`)? Are semantics named for roles (`--text-primary`) not values (`--gray-900-text`)?
5. **No arbitrary values** — inline colors, spacing, or z-index values that bypass the token system.

Output format:

| Severity | Category | Finding |
|---|---|---|
| Critical | Contrast | Required text is unreadable against its rendered background |
| High | Semantics | A supported theme switches only some values, leaving unreadable component states |
| Medium | Consistency | Related controls bypass the existing shared spacing token |
| Low | Z-index | Arbitrary values (`z-index: 999`) in 3 components |

Show what's missing. Do not propose code during audit unless the user asks.

### Step 3b — Converge mode (explicit opt-in)

When explicitly requested, load `../ui-craft/references/loops.md` preset `token-consistency` with its default budget. State the budget once, fix a coherent batch sharing a root cause, then recheck affected criteria within the requested scope. Stop when applicable criteria pass or the budget is exhausted.

---

## Step 4: Establish (no tokens found)

Establish only tokens needed by the current surface. Add dark mode only when requested or already supported. An audit-only request produces findings; an implementation request authorizes compatible local token edits.

**Minimal spine order:**
1. Primitives — reuse existing scales and add only values used by the current surface.
2. Semantics — add only roles needed by current usage; do not prebuild unused surface or status levels.
3. Component tokens — defer unless a specific component is already being built.

Use OKLCH for color unless the project uses sRGB across the board — in that case flag the gap, propose OKLCH, but don't auto-convert.

**File placement:** Reuse the existing token file or established project convention. Ask only when multiple materially different destinations remain. If none exists, use the matching convention:
- Tailwind project → `globals.css` (CSS variables inside `:root`)
- CSS-in-JS → `theme.ts` (exported theme object)
- Vanilla CSS → `tokens.css` (standalone variables file)
- Cross-platform / multi-consumer → `design-tokens.json` (Style Dictionary format)

Proceed with local writes already authorized by the implementation request; preserve unrelated values and report the change.

---

## Step 5: Preserve existing values

If the project has an existing token file, use narrow patches rather than replacing the file. A proposal-only request may show a diff such as:

```diff
  :root {
+   /* ── Semantic surface stack (new) ── */
+   --surface-canvas:  var(--gray-50);
+   --surface-raised:  var(--gray-100);
+   --surface-overlay: #fff;
+   --surface-sunken:  var(--gray-200);
+   --surface-inverse: var(--gray-900);
  }
```

Apply narrow patches when implementation is already authorized. For audit-only requests, report findings without edits.

---

## Constraints

- Don't impose Tailwind on a vanilla CSS project. Match the project's existing syntax.
- Don't impose OKLCH if the project uses sRGB consistently — flag it, suggest migration, don't force it.
- Respect existing naming conventions — if the project uses `--color-primary` over `--accent-500`, extend that pattern rather than introducing a parallel naming scheme.

**Next step:** `/craft` — build on the spine you just established (rung 1).
