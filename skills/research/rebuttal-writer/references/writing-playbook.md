# Writing Playbook

## Core Principle

Write to clarify and convince. The rebuttal must be thorough, direct, and easy for reviewers and the Area Chair to follow. Assume the AC may read only the reviews and the rebuttal.

## Audience Split

- Reviewers: clarify doubts, answer questions, correct misunderstandings, push back on mischaracterizations, and show good-faith incorporation of feedback.
- AC: provide a representative summary of reviews, show that major concerns were addressed, identify unreliable review claims when necessary, and make the decision easier.

Test: could a neutral third party tell that the reviewer concerns were addressed from the rebuttal alone?

## Recommended Process

1. Itemize every reviewer comment in a table.
2. Group common concerns across reviewers.
3. Brain-dump possible responses without worrying about length.
4. Identify new experiments or analyses early if allowed.
5. Draft complete answers first; compress later.
6. Review against the original comments to ensure no major concern is missed.

## Response Patterns

Use this shape by default:

```text
[R2/R4: concern label] We thank the reviewers for raising this point.
Direct answer: ...
Evidence: ...
Revision: We will add ... to Sec./Table/Fig. ...
```

Direct answer examples:

- `Yes, ...`
- `No, ...`
- `Not quite; ...`
- `We agree that the presentation was unclear. The intended point is ...`
- `We respectfully disagree with the premise because ...`

## Tactics

- Start positive. Summarize reviewer-recognized strengths so the AC does not see only negatives.
- Order matters. Put major, answerable, decision-critical issues first.
- Let reviewers speak for themselves. Quote the core concern briefly, then answer directly before adding context.
- Respond to intent, not only literal wording. A question about one dataset may really question experimental completeness.
- Be conversational and calm. Avoid sounding combative.
- Use emphasis for decisive facts: `Table 4, row 2 directly tests this setting.`
- Set the stage when reviewers missed the central goal. Recap what the paper is and is not trying to do.
- Keep answers self-contained. Reintroduce acronyms, setup details, and baselines.
- Get credit for details already in the paper. Cite section/table/figure, then restate the answer.
- Consolidate common concerns across reviewers to save space.
- Make reviewer labels easy to scan, especially when merging concerns.
- Use data before opinion. Prefer numbers, ablations, citations, calculations, and concrete evidence.
- Do, do not merely promise. If possible, include the explanation/result in the rebuttal and then promise to add it to the paper.
- Be receptive when the reviewer is right. Acknowledge useful suggestions and incorporate them.
- Be transparent about constraints: venue disallows new experiments, compute is infeasible, data is unavailable, or no conclusion is yet supported.
- Acknowledge constructive reviewer effort.

## Handling Common Concern Types

### Novelty

Explain the closest-work relationship by mechanism, assumption, supervision, setting, or result. Avoid generic `we are different` claims.

### Missing Experiment

Prefer:

1. Run the experiment if feasible and allowed.
2. Use existing experiments that directly answer the concern.
3. Explain infeasibility with concrete cost/data constraints.
4. Reframe as future work only if it is orthogonal to the contribution.

### Weak Clarity

Accept presentation responsibility. State the correct interpretation and promise exact edits: definition, figure, pseudocode, algorithm box, example, appendix, or section rewrite.

### Incorrect Reviewer Premise

Use a firm but respectful correction:

```text
This may be due to our unclear wording. The method does not assume X; it assumes Y. Evidence is shown in ...
```

### Real Limitation

Concede the boundary and explain why it does not invalidate the core claim. Add a limitation-section commitment.

### Low-Quality Review

Public rebuttal: correct factual errors with evidence and avoid personal judgment.

Confidential AC message, if available: use only for clear review-quality issues such as factual contradictions, unsupported accusations, or failure to engage with the paper. Keep it objective and ask the AC to consider review quality; do not instruct the AC to discard a score.

## Phrases

- `We thank the reviewers for the constructive feedback. We are encouraged that they recognize ...`
- `We agree this was unclear and will revise Sec. X to state ...`
- `This concern is already evaluated in Table Y; we restate the key result here for clarity: ...`
- `To address this concern, we ran ... The result ... supports ...`
- `We respectfully disagree with the premise. ...`
- `We agree this is a limitation; however, it is orthogonal to the main contribution because ...`
- `We will add the following concrete revision: ...`
- `We cannot run this experiment during rebuttal because ..., but we can add ...`

## Avoid

- `We apologize` everywhere.
- Vague promises: `we will improve the paper`.
- Emotional disagreement.
- Teaching basic concepts to reviewers.
- Overclaiming beyond evidence.
- Spending scarce words on concerns that cannot affect the decision.
