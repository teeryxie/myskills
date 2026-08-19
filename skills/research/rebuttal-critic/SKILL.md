---
name: rebuttal-critic
description: "Strictly review and improve an existing academic rebuttal draft against the original paper, reviewer comments, supplementary materials, venue rules, and optional evidence. Use when the user asks for critique, audit, scoring, risk analysis, tightening, fact-checking, or revision suggestions for a rebuttal/author response. Focus on catching unsupported claims, missed reviewer concerns, weak AC persuasion, tone risks, overpromises, and concrete edits."
---

# Rebuttal Critic

Use this skill after a rebuttal draft exists. Be strict: the task is to find what could still cost the paper acceptance, not to reassure the author.

Read [critique-rubric.md](references/critique-rubric.md) before auditing a complete rebuttal.

## Inputs

Require or reconstruct:

1. Paper PDF/source or at least abstract, contributions, main results, and limitations.
2. Full reviewer comments with IDs, scores, confidence, and any AC/meta-review text.
3. Existing rebuttal draft.
4. Venue constraints: word limit, response format, public vs confidential channels, new-experiment policy.
5. Evidence artifacts: tables, figures, line references, extra experiment logs, planned revision notes.

If paper or reviews are unavailable, say the audit is limited and mark all fact-sensitive judgments as provisional.

## Audit Workflow

1. Coverage check.
   - Build a reviewer-concern checklist.
   - Mark each concern `answered`, `partially answered`, `unanswered`, or `misanswered`.
   - Identify duplicated space and missing decision-critical concerns.

2. Evidence check.
   - Verify every factual claim, result, citation, line/table reference, and comparison against supplied materials.
   - Flag unsupported claims, invented certainty, and claims that require a new experiment.

3. AC persuasion check.
   - Ask whether a neutral AC can understand the concern and resolution without rereading the paper.
   - Check whether the opening frames positive signals and major concerns accurately.
   - Check whether reviewer disagreements are used fairly and tactically.

4. Tone and politics check.
   - Flag defensiveness, sarcasm, excessive apology, reviewer-blaming, or "teaching the reviewer" phrasing.
   - Distinguish firm factual correction from needless confrontation.
   - For low-quality reviews, require objective evidence and recommend confidential AC wording when available.

5. Revision realism check.
   - Flag vague promises, overbroad rewrites, impossible experiments, and camera-ready changes likely to create new risk.
   - Convert promises into exact section/table/figure edits.

6. Compression check.
   - Remove low-impact prose before cutting evidence.
   - Merge common concerns across reviewers when it saves space without hiding reviewer-specific answers.

## Output Contract

Lead with findings, not praise:

1. `Blocking issues`: problems likely to hurt acceptance if not fixed.
2. `Major issues`: unsupported or weak responses, missed concerns, bad ordering, tone risks.
3. `Line edits`: replacement wording for the highest-risk passages.
4. `Concern coverage table`: reviewer concern -> draft status -> required fix.
5. `Score`: `Reject / Weak / Borderline / Strong` as a rebuttal draft, with one-sentence rationale.
6. `Next revision plan`: ordered edits that fit the word limit.

If no serious issues are found, say so clearly and list residual risks.

## Hard Rules

- Do not rewrite the entire rebuttal unless the user asks; prioritize critique and targeted replacements.
- Do not accept claims that are not grounded in the supplied paper, reviews, or evidence.
- Do not soften a serious gap just because the prose is fluent.
- Do not recommend public attacks on reviewers.
- Do not let "we will add" stand when the draft can directly answer now.
- Do not treat reviewer conversion as the only goal; the AC is the final audience.
