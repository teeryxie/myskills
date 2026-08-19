#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from provider_router import review_text


def build_prompts(input_text: str, profile: str, review_mode: str) -> tuple[str, str]:
    system_prompt = (
        "You are a professional document reviewer. Evaluate structure, tone, clarity, "
        "and delivery readiness for formal Chinese documents. Return concise, actionable findings."
    )
    user_prompt = f"""
Profile: {profile}
Review mode: {review_mode}

Review the following document text. Focus on:
1. tone and formality
2. section structure and progression
3. redundancy and overlong paragraphs
4. whether the document feels ready for delivery

Return:
- overall judgment
- 3 to 8 actionable findings
- whether it is internal-ready, external-ready, or revise-required

Document text:
{input_text}
""".strip()
    return system_prompt, user_prompt


def main() -> None:
    parser = argparse.ArgumentParser(description="Run text review for a generated or source document.")
    parser.add_argument("--input-file", default="", help="Path to input text or markdown file")
    parser.add_argument("--input-text", default="", help="Raw text input")
    parser.add_argument("--profile", default="formal-business", help="Document profile")
    parser.add_argument("--review-mode", default="formal-delivery", help="Review mode tag")
    args = parser.parse_args()

    if not args.input_file and not args.input_text:
        raise SystemExit("Provide --input-file or --input-text.")

    input_text = args.input_text or Path(args.input_file).read_text(encoding="utf-8")
    system_prompt, user_prompt = build_prompts(input_text, args.profile, args.review_mode)
    result = review_text(system_prompt, user_prompt)
    print(
        json.dumps(
            {
                "status": result.status,
                "backend": result.backend,
                "model": result.model,
                "profile": args.profile,
                "review_mode": args.review_mode,
                "response_text": result.text,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
