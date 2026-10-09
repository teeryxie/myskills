---
name: critique
description: "Design lens critique covering visual hierarchy, clarity, and anti-slop patterns — produces a findings table, no code edits unless asked. Use when the user wants a design review, says \"what's wrong with this UI\", or needs a second opinion before a handoff or presentation. Invoke when the user asks for critique on their UI, or mentions 'critique' alongside design / UI / frontend work."
---

<!-- HARNESS MIRROR — do not edit here. Canonical source: skills/ or commands/. After editing source, copy into cli/assets/<harness>/ and repo-root harness mirrors. -->

**Context:** Use the relevant ui-craft guidance if needed and not already loaded. Reviews do not run build Discovery or require brand preference approval.

Critique the UI at `$ARGUMENTS` through a design lens. Load the `ui-craft` skill.

## Step 0: Evidence appropriate to the review

Use available browser automation or supplied screenshots for visual findings. Select viewports and themes relevant to the request; a full responsive audit may need desktop, tablet and mobile, while a local issue may need only its affected viewport.

If rendering is unavailable, proceed with independent static checks and label visual findings unverified. Request screenshots only when missing visual evidence prevents the core conclusion; do not block unrelated code, accessibility or performance checks. Never claim visual validation from code alone.

**Knob awareness (CRAFT_LEVEL sets the bar for what counts as "needs work"):**
- `CRAFT_LEVEL 3` → flag only anti-slop **Critical** items. Skip Minor polish.
- `CRAFT_LEVEL 5-7` → flag Critical + Major. Mention Minor polish as optional.
- `CRAFT_LEVEL 9+` → flag everything, including Minor polish and missing signature detail.

**Run these lenses in order:**

1. **Anti-Slop Test** (from SKILL.md): flag every item present. Critical first (ALL CAPS, purple gradients, identical card grids, bounce easing, emoji icons, glassmorphism + neon). Then major (colored pills on trends, thick colored borders, uniform radii, gradient text, walls of text). Then minor (straight quotes, missing `tabular-nums`, generic CTAs).
2. **Craft Test** (from SKILL.md): where does the design fall short of "one accent, 3-5 placements; plain secondary text for comparisons; functional color only; every section earns its space"?
3. **Hierarchy**: can the user tell what's primary, secondary, tertiary at a glance? Or does everything shout equally?
4. **Clarity**: is the value prop legible in 5 seconds? Are CTAs specific (not "Learn more")?
5. **Signature detail**: is there one memorable element that makes this feel designed, not assembled? If not, suggest one (motif, layout break, custom marker, distinctive hover).
6. **Inspiration gap** — read `../ui-craft/references/inspiration.md`: which observed pattern from the archetypes / signature details applies here, and how does the current state diverge from it?

**Output format** — the Review Format table:

| Before | After | Why |
| --- | --- | --- |

Prioritize by impact, not by file order. End with a one-paragraph summary of the **top 3 changes** that would raise this from "AI-generated" to "designed".

A critique-only request does not authorize edits. If the user also explicitly requests fixes, apply and verify the in-scope repairs without a second confirmation.

**Close with a Craft Report** (`../ui-craft/references/review.md` → Craft Report) as the final wrapper around the findings table and top-3 summary — Checked names the lenses actually run (Anti-Slop, Craft Test, Hierarchy, Clarity, Signature, Inspiration gap) and at what CRAFT_LEVEL bar, Passed carries whatever held up under those lenses, Changed lists authorized repairs or stays empty for critique-only requests, Left alone covers anything flagged but out of scope, Verdict is the one-sentence state. Produce it even when the surface passes clean — that's the validation the user is asking for.

**Next step:** `/polish` — apply the fixes this critique named (rung 1).
