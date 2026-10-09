---
name: code-simplify
description: Use after code has been implemented or changed to remove high-confidence redundancy, unnecessary complexity, and duplicate logic while preserving behavior, public contracts, side effects, and safety checks. Limit edits to the requested scope and run only proportionate verification.
metadata:
  source: https://www.skills.sh/paulrberg/agent-skills/code-simplify
  source_status: local-compatible-recovery
---

# Code Simplify

Use this skill in the **post-implementation cleanup** stage. The goal is a
small, behavior-preserving cleanup pass, not a rewrite and not a new feature.

## Scope

1. Prefer the user-named files or diff.
2. Otherwise use the current branch diff; if there is no usable diff, use files
   edited earlier in the conversation.
3. Stop if there is no substantive human-authored code in scope.

## Simplification rules

- Remove duplicate branches, dead code, needless wrappers, and speculative
  flexibility when the removal is clearly safe.
- Reuse existing helpers and dependencies before introducing anything new.
- Prefer clear, explicit code over clever compression. Fewer lines alone is not
  a reason to change code.
- Preserve public interfaces, observable side effects, error handling,
  validation at trust boundaries, security controls, accessibility behavior,
  and data-loss protection.
- Do not widen the mutation boundary to fix an unrelated issue.

## Verification

Inspect the resulting diff and run the closest relevant test, type check, or
lint command. Do not run a full-repository validation pass by default. Report
what changed, what was checked, and any unverified boundary.

## Handoff

Use `minimal-code-discipline` before the next implementation if the requested
change is still being designed. Use `overengineering-review` when the user
wants findings only and does not authorize edits.
