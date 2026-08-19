# Workflow

## Purpose

Use this reference to run the document-production loop consistently when the user needs a formal file rather than plain text.

## Prerequisites

Prefer this toolchain:

- `pandoc` for markdown to DOCX conversion
- `python-docx` for DOCX post-processing
- `soffice` for DOCX to PDF export
- `pdftoppm` and `pdfinfo` for page rendering

If a review backend is configured, also require network access.

## Standard Sequence

1. Normalize input into markdown.
2. Choose a profile.
3. Render DOCX.
4. Export PDF.
5. Render key pages:
   - first page
   - first heavy table page
   - one middle body page
   - final page when there is a conclusion or signature area
6. Run text review.
7. Run vision review.
8. Revise content or layout.
9. Regenerate final artifacts.

## Revision Rules

Revise text when the findings are about tone, clarity, repetition, or structure.

Revise layout when the findings are about:

- empty-looking tables
- broken page balance
- headings stranded at the bottom of a page
- weak hierarchy
- title pages that read like drafts

## Delivery Modes

- Internal formal material: acceptable when structure is clear, findings are minor, and the file reads as a finished working document.
- External formal material: require stronger title-page polish, tighter table layout, stable page breaks, and no obvious draft artifacts.
