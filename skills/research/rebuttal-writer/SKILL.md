---
name: rebuttal-writer
description: "Draft rigorous academic conference rebuttals from a paper, reviewer comments, supplementary materials, and optional experiment/code evidence. Use when the user asks to write, outline, polish, organize, or rewrite a rebuttal/author response for CVPR, ICCV, ECCV, NeurIPS, ICLR, ACL/EMNLP, AAAI, or similar peer-reviewed venues. Focus on AC-facing persuasion, reviewer-specific answers, evidence grounding, and concrete revision commitments."
---

# Rebuttal Writer

Use this skill to produce grounded rebuttal drafts. The goal is not to "win an argument"; it is to help a neutral AC decide that the major concerns were understood, answered with evidence, and can be safely resolved in the revision.

Read [writing-playbook.md](references/writing-playbook.md) when drafting anything longer than a short paragraph.

## Inputs

Collect or infer:

1. Paper PDF/source, abstract, or key claims.
2. Reviewer comments with reviewer IDs, scores, confidence, and questions.
3. Venue constraints: word limit, deadline, public rebuttal vs confidential AC message, whether new experiments are allowed.
4. Available evidence: tables, figures, line numbers, appendix, code results, extra experiments, ablations, limitations.
5. User intent: full rebuttal, per-reviewer answers, AC summary, revision plan, or concise rewrite.

If a critical input is missing, proceed with a clearly marked draft and list the missing evidence instead of inventing facts.

## Workflow

1. Build an issue map.
   - Split reviews into atomic concerns.
   - Tag each concern as `misunderstanding`, `missing evidence`, `valid limitation`, `presentation clarity`, `novelty`, `experiment`, `related work`, `ethics/scope`, or `low-impact`.
   - Merge duplicate concerns across reviewers.

2. Decide priority.
   - Put decision-critical concerns first.
   - Prefer concerns with strong answers, new evidence, or direct impact on scores.
   - Spend little space on minor wording issues unless they create a false impression.

3. Map evidence before writing.
   - For every substantive claim, cite a paper section/table/figure/line, a supplied result, or a concrete new analysis.
   - If evidence is absent, write a limitation or revision commitment; do not bluff.

4. Draft for two audiences.
   - For reviewers: answer questions, correct misunderstandings, and incorporate useful feedback.
   - For the AC: summarize the review landscape, show good faith, demonstrate that major concerns are resolved, and surface low-quality review issues only when evidence is clear.

5. Write in the four-part response shape.
   - `acknowledge`: briefly thank or recognize the concern.
   - `direct answer`: yes/no/not quite/we agree/we respectfully disagree.
   - `evidence`: result, citation, ablation, calculation, or paper location.
   - `revision`: exact change to camera-ready text/table/figure/appendix.

6. Compress and polish.
   - Quote the core reviewer concern when useful.
   - Use reviewer labels such as `R1/R3` for merged responses.
   - Keep responses self-contained; assume the AC will not reread the paper.
   - Use calm, direct, non-defensive language.

## Output Contract

For a full rebuttal, output:

1. `AC-facing opening`: 2-5 sentences summarizing positive signals, main concerns, and added evidence.
2. `Issue map`: concise table or bullets linking concerns to response strategy.
3. `Draft responses`: prioritized, reviewer-labeled text.
4. `Revision commitments`: exact paper changes promised.
5. `Evidence gaps`: missing facts or experiments that should be supplied before final submission.

For a short rewrite request, output only the revised text plus any critical caveat.

## Hard Rules

- Do not fabricate experiment results, citations, reviewer scores, or paper line numbers.
- Do not apologize for the core contribution unless the paper is actually wrong.
- Do not use aggressive, sarcastic, or reviewer-blaming wording in public rebuttal text.
- Do not promise vague future work as a substitute for current evidence.
- Do not bury the strongest answer after weaker points.
- Use confidential AC comments only when the venue supports them and only for evidence-backed review-quality issues.
