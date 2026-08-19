---
name: docx-polish-pipeline
description: "Turn markdown drafts, outlines, rough notes, or mixed document materials into polished DOCX/PDF deliverables with a repeatable pipeline that normalizes content, shapes structure, renders DOCX, exports PDF, previews key pages, runs text and vision reviews, and supports revision. Use when the task requires formal document delivery, stable Word formatting, PDF preview, iterative visual QA, or reusable document-production workflows rather than one-off writing only."
---

# Docx Polish Pipeline

## Overview

Use this skill to produce formal `docx/pdf` deliverables from markdown-centered source material and to close the loop with preview and review steps. Keep the pipeline generic: do not bind it to a single document type, industry, or model provider.

## Run The Standard Pipeline

Execute the workflow in this order:

1. Normalize the source into a clean markdown draft.
2. Shape the document structure before touching layout.
3. Render a styled DOCX.
4. Export a PDF preview.
5. Render key PDF pages to images.
6. Run text review and vision review when configured.
7. Revise the source or layout, then regenerate the final artifacts.

Prefer using `scripts/run_pipeline.py` when the user wants the full loop. Use the narrower scripts only when the user needs a specific step.

## Choose The Right Profile

Pick a document profile before rendering:

- `formal-business`: Best default for proposals, quotations, cooperation letters, reports, and client-facing materials.
- `formal-report`: Use for internal reports, structured summaries, or content that should read more like a report than a business letter.
- `technical-clean`: Use for technical notes or materials where dense information matters more than decorative presentation.

Read [references/profiles.md](references/profiles.md) when the document tone or layout direction is unclear.

## Use The Scripts

Use these scripts as the default execution surface:

- `scripts/build_docx.py`: Render markdown into a styled DOCX.
- `scripts/export_pdf.py`: Convert DOCX to PDF with LibreOffice.
- `scripts/render_pdf_pages.py`: Render selected PDF pages to PNG for review.
- `scripts/review_text.py`: Run a text-focused review through the configured backend.
- `scripts/review_vision.py`: Run a page-image review through the configured backend.
- `scripts/run_pipeline.py`: Execute the end-to-end flow and emit artifact paths plus review outputs.

When only the writing needs improvement, do that locally first and delay DOCX generation. When the user explicitly needs a deliverable file, run the full render-preview-review loop.

## Keep Provider Logic Separate

Do not hard-code secrets, provider names, or model-specific prompts into the core workflow. Keep document generation independent from review providers.

Use `scripts/provider_router.py` to select the review backend:

- `none`: Skip external review and still produce `docx/pdf`.
- `openai-compatible`: Use any OpenAI-compatible endpoint, including gateways.
- `internal-http`: Call an internal review API instead of exposing third-party keys to every user.

Read [references/providers.md](references/providers.md) when configuring environments or discussing security boundaries.

## Apply Review Discipline

Always treat review as a first-class step, not as an optional afterthought.

Use text review to check:

- tone and formality
- structure and sectioning
- redundancy and overlong paragraphs
- readiness for delivery

Use vision review to check:

- title page balance
- table density and alignment
- page breaks and dangling headings
- whether the file looks like a finished deliverable rather than a draft

Read [references/visual-rubric.md](references/visual-rubric.md) before deciding whether a file is ready for internal use or external delivery.

## Respect Output Boundaries

Generate three artifact classes whenever feasible:

- source artifact: cleaned markdown
- production artifact: final `docx`
- preview artifact: `pdf` and selected page images

Keep review comments separate from the final document. Do not leak API keys, internal review prompts, or raw provider configuration into the output files.
