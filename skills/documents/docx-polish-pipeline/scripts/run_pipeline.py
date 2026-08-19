#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from build_docx import build_document
from export_pdf import export_docx_to_pdf
from render_pdf_pages import render_pages
from review_text import build_prompts as build_text_prompts
from review_vision import build_prompts as build_vision_prompts
from provider_router import review_text, review_vision


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the end-to-end DOCX/PDF production and review pipeline.")
    parser.add_argument("--input-md", required=True, help="Markdown source file")
    parser.add_argument("--output-dir", required=True, help="Directory for final artifacts")
    parser.add_argument("--profile", default="formal-business", help="Document profile")
    parser.add_argument("--title", default="", help="Override title")
    parser.add_argument("--subtitle", default="", help="Optional subtitle")
    parser.add_argument("--review-mode", default="formal-delivery", help="Review mode tag")
    parser.add_argument("--vision-pages", default="1,last", help="Page spec for PNG rendering")
    args = parser.parse_args()

    input_md = Path(args.input_md).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve()
    build_dir = output_dir / "build"
    preview_dir = output_dir / "preview_pages"
    output_dir.mkdir(parents=True, exist_ok=True)

    docx_path = output_dir / f"{input_md.stem}.docx"
    pdf_dir = output_dir / "pdf"
    docx_path = build_document(
        input_md=input_md,
        output_docx=docx_path,
        profile=args.profile,
        title=args.title.strip() or None,
        subtitle=args.subtitle.strip() or None,
        build_dir=build_dir,
    )
    pdf_path = export_docx_to_pdf(docx_path, pdf_dir)
    image_paths = render_pages(pdf_path, preview_dir, dpi=180, page_spec=args.vision_pages)

    source_text = input_md.read_text(encoding="utf-8")
    text_system, text_user = build_text_prompts(source_text, args.profile, args.review_mode)
    text_review = review_text(text_system, text_user)
    vision_system, vision_user = build_vision_prompts(args.profile, args.review_mode)
    vision_review = review_vision(vision_system, vision_user, image_paths)

    print(
        json.dumps(
            {
                "input_md": str(input_md),
                "docx_path": str(docx_path),
                "pdf_path": str(pdf_path),
                "rendered_pages": [str(path) for path in image_paths],
                "text_review": {
                    "status": text_review.status,
                    "backend": text_review.backend,
                    "model": text_review.model,
                    "response_text": text_review.text,
                },
                "vision_review": {
                    "status": vision_review.status,
                    "backend": vision_review.backend,
                    "model": vision_review.model,
                    "response_text": vision_review.text,
                },
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
