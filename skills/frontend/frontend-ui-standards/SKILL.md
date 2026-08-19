---
name: frontend-ui-standards
description: Use when implementing, refactoring, or reviewing frontend UI across SwiftUI, React, React Native, Flutter, web, or mobile apps. Applies to Figma-to-code work, visual consistency fixes, design tokens, typography, spacing, layout, buttons, cards, navigation chrome, safe areas, responsive behavior, and component reuse. Helps prevent scattered hardcoded values, one-off layout patches, duplicated components, and UI drift from the design system.
---

# Frontend UI Standards

## Purpose

Use this skill to turn UI work into systematic frontend implementation. The goal is not pixel tweaking. The goal is to preserve a design system in code so future changes stay predictable, reusable, and visually consistent.

This skill is framework-agnostic. Translate the rules to the local stack:

- SwiftUI: design tokens as enums/static constants, reusable `View`s, semantic metrics.
- React/Web: CSS variables, design-token modules, component props/variants.
- React Native/Flutter: theme objects, shared components, semantic dimensions.

## When To Use

Use this skill before touching UI when the task involves:

- Building or changing a visible screen, component, layout, or interaction.
- Translating Figma, SVG, screenshots, or visual specs into code.
- Fixing visual bugs: misalignment, truncation, inconsistent spacing, wrong font, wrong button size, unsafe-area issues.
- Creating or changing buttons, cards, chips, tabs, nav bars, sheets, dialogs, lists, progress indicators, input fields, or reading surfaces.
- Reviewing frontend code for production readiness or design consistency.
- Refactoring duplicated UI or scattered hardcoded values.

Do not use it for pure backend, data model, prompt, or infrastructure work unless the change affects user-facing UI.

## Core Principle

UI code has three layers:

1. **Design tokens**: global primitives and semantic values such as color, type, spacing, radius, elevation, safe-area offsets, content width.
2. **Component metrics**: component-specific structure such as chip height, icon size, internal padding, card header spacing, button variants.
3. **Screen layout metrics**: page-specific composition such as hero card position, section gaps, repeated row alignment, decorative asset placement.

View code should describe structure and state. It should not hide raw design math in the body.

## Implementation Workflow

1. **Inspect Existing Patterns**
   - Search for the closest existing component and screen before adding new UI.
   - Identify the local design token files, theme files, component libraries, and layout helpers.
   - Check if the same visual element already appears elsewhere.

2. **Classify Every Visual Value**
   - Global and reusable: put it in design tokens.
   - Component-specific: put it in a component metrics object/enum.
   - Screen-specific but repeated within that screen: put it in screen layout metrics.
   - One-off decorative positioning: keep it isolated in named screen metrics, not inline in the view body.

3. **Build From Reuse**
   - Prefer extending an existing component variant over creating a new component.
   - If two places use the same visual role, they should share the same component or metrics.
   - If a new component repeats soon after, extract it immediately.

4. **Encode Layout Relationships**
   - Prefer derived values over duplicated numbers.
   - Example: `authorChipWidth = rowWidth - sourceChipWidth - rowGap`, not three unrelated widths.
   - Align related elements by sharing a container, grid, layout guide, or named metric.
   - Do not fix alignment by locally nudging one element unless the offset is a named decorative exception.

5. **Verify Similar Surfaces**
   - After fixing one button/card/header, search for the same label, component, asset, or pattern.
   - Update the shared component when possible.
   - If a one-off remains, document why through a clear metric name or short comment.

6. **Build And Visually Sanity Check**
   - Run the relevant build/typecheck.
   - For mobile UI, install or run in simulator/device when the user is actively validating visuals.
   - Check truncation, safe areas, touch targets, dynamic text risk, and navigation/back behavior.

## Token And Metrics Rules

Prefer semantic names over visual coordinates:

- Good: `primaryActionWidth`, `screenHorizontalInset`, `cardVerticalSpacing`, `metadataRowWidth`, `sourceChipWidth`.
- Bad: `width: 271`, `padding(.leading, 12)`, `offset(y: 37)` repeated inside view bodies.

Allowed numeric values:

- Numeric values are allowed inside token or metrics definitions.
- Numeric values are allowed for one-off asset geometry if they are grouped in a named metrics section.
- Numeric values are allowed when using a platform API that requires a literal and the value is not part of visual design.

Avoid:

- Scattered raw hex colors.
- Inline font sizes when a type scale exists.
- Inline spacing that should come from a spacing scale.
- Multiple local versions of the same button, chip, top bar, card, or bottom CTA.
- Fixing a shared component issue at only one call site.

## Component Reuse Rules

Before creating UI, ask:

- Is this a new visual role or a variant of an existing role?
- Does an existing component already define the interaction, size, shadow, radius, or typography?
- Will this appear on another screen?
- Should this be a component prop/variant instead of a new file?

Create component variants for:

- Same structure, different color or state.
- Same button shape with different text/icon.
- Same card shell with different content.
- Same chip with different label/icon.

Create a new component only when:

- The structure, behavior, or layout role is meaningfully different.
- Extending the old component would make it unclear or fragile.

## Figma-To-Code Rules

When using Figma, SVG, screenshots, or visual specs:

- Treat Figma numbers as input evidence, not as final code structure.
- First identify repeated primitives: colors, typography, radii, shadows, spacing, content widths.
- Map repeated primitives to existing tokens or add new semantic tokens.
- Map repeated UI elements to existing components or component variants.
- Use absolute positioning only when the design is truly illustrative/decorative or when the platform layout model requires it.
- Preserve hierarchy and relationships over blindly copying coordinates.

If Figma shows two elements aligned, encode the shared alignment in code through a common container, grid, width, or derived metric.

## Typography Rules

- Use the project type scale or platform text styles first.
- Text hierarchy should be visible through size, weight, color, and spacing.
- Body text on mobile should remain readable; avoid tiny labels for meaningful content.
- Prefer wrapping for content users need to read.
- Use truncation only for metadata, labels, usernames, authors, or bounded chips where space is intentionally constrained.
- When truncating, constrain the text inside the correct component. Do not let text resize or push surrounding layout.

## Layout And Spacing Rules

- Use consistent page insets and content max widths.
- Respect safe areas, notches, home indicators, and keyboard behavior.
- Primary bottom actions should share a consistent width and vertical placement within the product.
- Top chrome such as back, close, notification, or favorite buttons should share one positioning model.
- Cards in the same family should share shell metrics: width, radius, shadow, content padding, and spacing rhythm.
- Avoid nested cards unless the design explicitly uses a contained sub-card.

## Interaction Rules

- Touch targets should be at least 44pt on iOS or the platform equivalent.
- Icon-only buttons need accessible labels.
- Destructive actions need clear confirmation or undo.
- Loading, retrying, disabled, empty, and error states must be explicit.
- Back behavior should match user entry path when possible.
- Tappable area should match user expectation; do not restrict taps to tiny icons when the whole row/card is the affordance.

## Review Checklist

Before finishing UI work, check:

- Did I search for an existing component before adding a new one?
- Are colors, typography, spacing, radius, and shadows tokenized?
- Are component internals in component metrics rather than inline body values?
- Are screen-specific layout values grouped and named?
- Are related widths/positions derived from one source of truth?
- Did I update all same-family components or explain why not?
- Does text fit without unwanted truncation?
- Are touch targets and safe areas respected?
- Did I run the relevant build/typecheck?
- If this is visual polish, did I install/run the app or capture a screenshot when feasible?

## Common Anti-Patterns

- "Move it down 8px here" without checking the shared container.
- Duplicating a button implementation because this screen is "slightly different."
- Copying Figma coordinates directly into a view body.
- Adding a local font size because one label looks wrong.
- Fixing a width in one screen while the same component is broken elsewhere.
- Using mock-only layout assumptions in production UI.
- Letting generated or backend text dictate UI layout without length limits or truncation strategy.

## When A Local Exception Is Acceptable

Exceptions are acceptable when they are deliberate and contained:

- Decorative assets that are unique to one screen.
- A marketing or editorial layout with one-off art direction.
- A transitional refactor where a full component extraction would be too risky in the current change.
- Platform-specific constraints that require local adaptation.

Even then, keep the value in a named metrics object and keep the exception small.
