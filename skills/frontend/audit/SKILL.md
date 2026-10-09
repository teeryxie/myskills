---
name: audit
description: "Technical UI audit — a11y, performance, responsive. Produces a prioritized findings table. Invoke when the user asks for audit on their UI, or mentions 'audit' alongside design / UI / frontend work."
---

<!-- HARNESS MIRROR — do not edit here. Canonical source: skills/ or commands/. After editing source, copy into cli/assets/<harness>/ and repo-root harness mirrors. -->

**Context:** Use the relevant ui-craft guidance if needed and not already loaded. Reviews do not run build Discovery or require brand preference approval.

Run a technical audit of the UI at `$ARGUMENTS`. Load the `ui-craft` skill and apply the audit lens.

## Step 0: Evidence appropriate to the review

Use available browser automation or supplied screenshots for visual findings. Select viewports and themes relevant to the request; a full responsive audit may need desktop, tablet and mobile, while a local issue may need only its affected viewport.

If rendering is unavailable, proceed with independent static checks and label visual findings unverified. Request screenshots only when missing visual evidence prevents the core conclusion; do not block unrelated code, accessibility or performance checks. Never claim visual validation from code alone.

**Note:** audit is knob-agnostic — accessibility and performance are not tunable.

**Scope:** Apply the following checks to the requested target and review dimensions. Do not expand a focused review to unrelated surfaces.

1. **Accessibility** — read `../ui-craft/references/accessibility.md`:
   - Visible `:focus-visible` on every interactive element
   - Keyboard reachable, no focus traps
   - Touch targets ≥ 44px (mobile)
   - Color not the only signal for state
   - Form labels, error association, required indication
   - `prefers-reduced-motion` honored for all animations
2. **Performance** — read `../ui-craft/references/motion.md` Rendering Performance section:
   - Only `transform` / `opacity` animated (no `width`/`top`/`height`)
   - No `transition: all`
   - `will-change` scoped to active interaction, removed after
   - Images have `width`/`height` or `aspect-ratio` (CLS)
   - No layout thrash in scroll/resize handlers
3. **Responsive** — read `../ui-craft/references/responsive.md`:
   - Mobile-first breakpoints, no fixed-width components
   - `env(safe-area-inset-*)` respected on fixed elements
   - Touch zones don't overlap
   - No horizontal scroll at 320px

**Output format** — the Review Format table from SKILL.md:

| Before | After | Why |
| --- | --- | --- |

Group findings by priority: **Critical** (blocks usability/a11y) → **High-impact** (immediately noticeable) → **Quick wins** (polish).

Review-only requests produce findings without edits. If the user already asked to review and fix, repair in-scope findings and verify the changes without requiring another approval.

**Close with a Craft Report** (`../ui-craft/references/review.md` → Craft Report), wrapping the findings table above — Checked states scope (a11y/perf/responsive, at which viewports), Passed carries anything inspected and found sound, Changed lists only authorized repairs, or stays empty for review-only requests, Verdict names the top priority. Produce it even on a clean audit — a11y/perf/responsive coming back clean is the finding.

**Next step:** `/harden` — turn the findings into real production coverage (rung 1).
