# Critique Rubric

## Severity Levels

- Blocking: likely harms acceptance or credibility if unchanged.
- Major: materially weakens persuasion, coverage, evidence, or tone.
- Minor: local clarity, compression, or wording issue.
- Suggestion: optional improvement after high-risk fixes.

## Required Checks

### 1. Concern Coverage

Build a table:

```text
Reviewer | Concern | Draft location | Status | Fix
```

Statuses:

- `answered`: directly answered with evidence.
- `partially answered`: direction is right but evidence, specificity, or AC framing is weak.
- `unanswered`: no substantive response.
- `misanswered`: answer misses the reviewer intent or contradicts evidence.
- `overanswered`: spends too much space on low-impact material.

### 2. Evidence Integrity

Flag:

- New result stated without artifact.
- Paper line/table/figure reference that is absent or mismatched.
- Claim stronger than the actual evidence.
- Comparison to prior work without precise basis.
- Feasibility claim without cost/data/support.
- Revision commitment that cannot fit camera-ready constraints.

Recommended fix format:

```text
Problem: ...
Why it matters to AC: ...
Replacement: ...
Evidence needed: ...
```

### 3. AC-Facing Persuasion

Ask:

- Does the opening summarize positive reviewer signals and major concerns?
- Can the AC understand the answer without rereading the paper?
- Are reviewer conflicts used fairly to support the author's case?
- Are the strongest points placed early?
- Does the draft show good faith rather than defensiveness?

### 4. Tone Risk

Flag wording that sounds:

- sarcastic
- wounded
- dismissive
- overly apologetic
- reviewer-blaming
- like it is teaching the reviewer basic knowledge
- like it admits a fatal flaw unnecessarily

Firm corrections are allowed when evidence is strong. Prefer `we respectfully disagree with the premise because...` over `the reviewer is wrong`.

### 5. Revision Realism

Bad:

- `We will rewrite the method section.`
- `We will improve the figures.`
- `We will add more experiments.`

Better:

- `We will add a paragraph at the start of Sec. 3 defining X and summarizing the three-stage pipeline.`
- `We will add the new ablation to Table 2 and move hyperparameters to Appendix B.`
- `We will revise Fig. 2 by adding the missing legend and increasing label contrast.`

### 6. Compression

Cut in this order:

1. Generic thanks and filler.
2. Repeated explanations.
3. Low-impact reviewer-specific details.
4. Long future-work discussion.
5. Background that the AC does not need.

Do not cut:

- Direct answers.
- Numbers.
- Concrete evidence.
- Specific revision commitments.

## Common Failure Modes

- The draft answers reviewers but forgets the AC.
- It quotes paper locations but does not restate the answer.
- It promises future changes instead of giving the answer now.
- It treats a real limitation as a misunderstanding.
- It accepts a false reviewer premise to sound polite.
- It responds to a literal question while missing the concern behind it.
- It lets low-quality review comments consume too much public rebuttal space.
- It uses confident prose without enough evidence.
- It fails to merge repeated concerns.

## Scoring

Use one of:

- `Reject`: draft is unsafe; major concerns are missed, unsupported, or tone-damaging.
- `Weak`: usable skeleton but likely insufficient for AC persuasion.
- `Borderline`: mostly sound but one or two decision-critical fixes remain.
- `Strong`: evidence-grounded, complete, concise, and AC-readable.

Always justify the score in one sentence and list the top three fixes.
