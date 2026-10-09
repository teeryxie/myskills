---
name: overengineering-review
description: Use after an implementation, or when the user asks whether code or a diff is over-engineered. Report only concrete needless complexity: removable abstractions, duplicate wrappers, dead flexibility, replaceable dependencies, or speculative configuration. Review and report; do not edit unless the user separately asks for a patch.
license: MIT
metadata:
  abvx_status: experimental
  abvx_origin: adapted
---

# Overengineering Review

## Project phase and handoff

This is the **review-only** stage. Use it when the user wants findings before
changing code, or when a focused diff needs an overengineering check. Do not
run a general correctness audit and do not expand the scope. If the user asks
to apply the findings, use the smallest patch possible and then run the closest
relevant verification. For cleanup after a completed implementation, prefer
`code-simplify`; for preventing scope growth before implementation, prefer
`minimal-code-discipline`.

Review only for unnecessary complexity. This skill does not hunt general correctness issues unless they directly affect the simplification recommendation.

## Pair With

- Use `minimal-diff-builder` when the user wants the simplification findings turned into the smallest correct patch.
- Use `complexity-optimizer` instead when the real question is performance or algorithmic cost rather than architectural bloat.
- Use `architecture-deepening-review` instead when the code is not overbuilt but the boundary design is still wrong.

## Review Surface

Look for:

- needless abstractions;
- replaceable dependencies;
- dead flexibility;
- wrappers around stdlib or native platform features;
- local helpers or files that only forward to something simpler;
- speculative extension points with one caller or one implementation.

## Findings Taxonomy

Use these tags:

- `delete:` code or layer can disappear entirely.
- `stdlib:` custom logic should be replaced by a standard-library primitive.
- `native:` use built-in platform behavior instead of app code or dependency code.
- `existing-dep:` repo already ships a dependency that makes the extra code unnecessary.
- `yagni:` speculative abstraction or configurability with no present payoff.
- `shrink:` same behavior, fewer moving parts.

## Workflow

1. Determine scope:
   - diff review;
   - file review;
   - broad repo audit.
2. Ignore style nitpicks that do not reduce real complexity.
3. Rank findings by payoff:
   - dependency removal;
   - file/layer deletion;
   - abstraction collapse;
   - line-count shrink.
4. For each finding, capture:
   - location;
   - tag;
   - what is overbuilt;
   - what replaces it;
   - why the simpler path still covers the requirement;
   - any safety caveat.
5. Keep findings review-grade:
   - specific;
   - actionable;
   - minimal prose;
   - no vague "this feels complex" commentary.

## Output Format

One finding per line in ranked order:

`<file>:L<line> <tag> <what to cut>. <replacement>. <why it still covers the need>.`

End with one compact summary line:

`net: -<N> lines, -<M> files, -<K> deps possible.`

If nothing meaningful should be cut:

`Lean already. Ship.`

## Boundaries

- Do not recommend deleting trust-boundary validation, security checks, accessibility basics, or data-loss prevention.
- Do not turn the review into a broad bug hunt.
- Do not apply changes unless the user explicitly asks for implementation after review.
- Treat one focused regression test or self-check as acceptable minimum discipline, not bloat.

## Final Report

When a normal prose review is needed, convert the ranked list into:

- findings ordered by impact;
- top simplification opportunities;
- residual caveats where the simpler path only works under current scope.
