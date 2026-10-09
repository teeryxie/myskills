---
name: finalize
description: "Pre-ship gate — runs detector, verifies brief and tokens, applies the 10-pass finish bar, ranks findings by feedback hierarchy. Use when the user wants to ship, merge, or finalize a surface and needs a verdict (READY / NOT READY / BLOCKED) before committing. Invoke when the user asks for finalize on their UI, or mentions 'finalize' alongside design / UI / frontend work."
---

<!-- HARNESS MIRROR — do not edit here. Canonical source: skills/ or commands/. After editing source, copy into cli/assets/<harness>/ and repo-root harness mirrors. -->

**Context:** this sub-skill is one lens of the broader `ui-craft` skill. If the `ui-craft` skill is also installed, read its SKILL.md first for Discovery + Anti-Slop + Craft Test, then apply the specific lens below.

Use relevant `ui-craft` guidance. Review-only requests produce findings. When the user also asks to fix issues, apply and verify in-scope repairs; no special convergence phrase is required for ordinary authorized fixes.

---

## Step 1 — Brief check (gate)

Look for `.ui-craft/brief.md`.

- Absent: infer applicable acceptance criteria from the user request and existing product; state material assumptions. Ask only if missing criteria prevent a core judgment. Do not require creation of a brief merely to review existing work.
- Present: load it. Extract principles (numbered, in conflict-resolution order). These are the override registry for Steps 4–5.

---

## Step 2 — Detector

Run `npx ui-craft-detect` on `$ARGUMENTS` (or current working surface if no argument).

Capture all output. Every Critical detector finding maps directly to a block-ship finding in the report. Preserve detector source labels.

---

## Step 3 — Token check

Check only token layers and categories needed by the target, and themes already supported or requested. Missing unused categories, optional component tokens or unrequested dark mode are N/A. Flag concrete consistency or usability problems; do not gate delivery on building a new design system.

---

## Step 3b — Craft-intent check (full surfaces only)

Applies only when the target is a complete surface (dashboard, landing, auth, settings shell, portfolio) — skip for single components.

1. **Signature bet present?** Scan for exactly one memorable decision from `../ui-craft/references/craft-intent.md` §3 (product / auth / marketing lists). Zero → **Major** ("no signature — surface is competent but anonymous; run `/bolder` or `/polish`"). Two or more competing → **Major** ("signature bets stack — keep the strongest, cut the rest").
2. **Variance matches surface?** Layout risk visibly inconsistent with the surface's DESIGN_VARIANCE default (e.g. experimental asymmetry on an auth form, or a landing that is one centered symmetric column) → **Major**, unless the brief or spec records the deviation.
3. **Craft Read recorded?** If a `.ui-craft/spec.md` section or session declared a Craft Read, verify the built surface matches it (theme, variance, signature). Mismatch → **Major** with the specific delta.

These findings are Major, never Critical — they gate NOT READY, not BLOCKED.

---

## Step 3c — Copy self-audit + mechanical counts (marketing surfaces only)

Applies to landings, portfolios, and campaign pages — skip for product shells.

Load `../ui-craft/references/recipe-landing.md` and run its Acceptance-bar mechanical checks against the built surface — thresholds (eyebrow count, layout-family budget, hero discipline) live there, not here; this step only names which checks apply and where a violation lands.

1. **Copy self-audit.** Read every visible string (headlines, eyebrows, buttons, captions, alt text, footer). Grammatically broken copy, unclear referents, forced-clever labels ("Field notes" over testimonials, "Quietly trusted by"), or fake-precise numbers with no source → **Major** per `../ui-craft/references/copy.md` Copy Self-Audit.
2. **Eyebrow count (mechanical)** — per `../ui-craft/references/recipe-landing.md` Eyebrow budget. Over budget → **Major** ("eyebrow flood — delete labels until the count passes").
3. **Layout-family count (mechanical)** — per `../ui-craft/references/recipe-landing.md` Layout-family budget. Any repeat or consecutive-split overrun → **Major**.
4. **CTA intent (mechanical)** — per `../ui-craft/references/copy.md` CTAs & Buttons (one label per intent; CTA fits one line at desktop). Violation → **Major**.
5. **Hero discipline** — per `../ui-craft/references/recipe-landing.md` Hero discipline. Over budget → **Major**.

---

## Step 4 — Finish bar

Load `../ui-craft/references/finish-bar.md` when needed. Select applicable passes using scope and the rules below; mark irrelevant checks N/A. Recheck affected passes after repairs, not every unchanged dimension.

**Knob behavior (apply before running):**

- `CRAFT_LEVEL ≤ 6` AND user did not explicitly invoke `/finalize`: run Passes 1, 6, 8 only; mark remaining as N/A (knob-gated).
- `CRAFT_LEVEL ≥ 7` OR user explicitly invoked `/finalize`: run all 10 passes.
- `MOTION_INTENSITY ≤ 3`: Pass 7 = motion-gap audit only; do not fail on absent entrance animations.
- `VISUAL_DENSITY ≥ 8` AND brief documents compressed rhythm: Pass 4 accepts compressed spacing values.

**For each pass:**

- Collect findings.
- Assign severity per the severity map in `finish-bar.md` (Critical / Major / Minor).
- If a finding conflicts with a recorded principle in `brief.md`: downgrade to "Deferred per brief" and cite the exact principle. If no brief principle covers it, it remains a finding regardless.
- Record file:line when available.

---

## Step 5 — Feedback hierarchy filter

Load `../ui-craft/references/review.md` Feedback Hierarchy section.

Group all findings (detector + token + finish-bar) into three tiers:

- **Value** — does the surface solve the problem the brief defines?
- **Ease of Use** — can the user accomplish the primary task?
- **Delight** — is it polished?

If any Value findings exist: surface them first in the report and add a standing recommendation to defer all Delight findings until Value findings are resolved. This prevents polish work masking broken functionality.

---

## Step 6 — Output

Print this report. Do not add preamble.

```
## Finalize report — <surface name>

**Ship verdict:** READY / NOT READY / BLOCKED

> BLOCKED = any Critical finding present.
> NOT READY = any Major finding present, no Critical.
> READY = zero Critical, zero Major (Minor explicitly accepted).

### Block-ship findings (must fix before merge)
- [Pass / detector source] — [finding] — [file:line if available]

### Major findings (fix or defer with recorded reason)
- [...]

### Minor findings (polish; ship-okay if explicitly accepted)
- [...]

### Deferred per brief
- [finding] — [principle from brief.md that defers it]

### Recommended next actions
- [ordered, 3–5 items max]
```

If a tier has no findings, omit the section header entirely.

---

## Step 6b — Convergence mode (explicit opt-in only)

Repeated whole-surface convergence requires an explicit request to iterate until the quality bar passes (including a convergence flag). Ordinary requests such as "check and fix" already authorize in-scope repairs and relevant verification, but do not imply open-ended convergence.

When convergence is requested, load `../ui-craft/references/loops.md` and use preset `visual-anti-slop` (default budget 3, hard cap 5). State the budget once. Apply a coherent batch of fixes sharing a root cause and recheck affected criteria. Stop on success or budget exhaustion, reporting unresolved findings honestly.

---

## Step 7 — Hard stops

Do not edit for review-only requests. An existing request to fix authorizes in-scope repairs without a second request. Neither review nor repair authorizes unrelated redesign, deployment, merging, or other external changes. Stop when the requested outcome and relevant verification pass.

**Next step:** Ship. If the gate is red, the findings name the pass to re-run — `/polish`, `/harden` or `/clarify`.
