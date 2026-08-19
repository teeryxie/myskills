#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from provider_router import review_vision


def build_prompts(profile: str, review_mode: str) -> tuple[str, str]:
    system_prompt = (
        "You are a professional visual reviewer for formal documents. Judge layout, hierarchy, "
        "table integrity, page balance, and whether the page looks like a finished deliverable."
    )
    user_prompt = f"""
Profile: {profile}
Review mode: {review_mode}

Review the attached page images of a generated document.

Focus on:
1. first-page formal quality
2. table completeness and alignment
3. page-balance and broken layout
4. whether the document looks internal-ready, external-ready, or revise-required

Return:
- overall judgment
- the 3 most important visual findings
- delivery decision
""".strip()
    return system_prompt, user_prompt


def main() -> None:
    parser = argparse.ArgumentParser(description="Run vision review on rendered PDF pages.")
    parser.add_argument("--image-path", action="append", required=True, help="Rendered PNG path; repeat for multiple images")
    parser.add_argument("--profile", default="formal-business", help="Document profile")
    parser.add_argument("--review-mode", default="formal-delivery", help="Review mode tag")
    args = parser.parse_args()

    image_paths = [Path(path).expanduser().resolve() for path in args.image_path]
    system_prompt, user_prompt = build_prompts(args.profile, args.review_mode)
    result = review_vision(system_prompt, user_prompt, image_paths)
    print(
        json.dumps(
            {
                "status": result.status,
                "backend": result.backend,
                "model": result.model,
                "profile": args.profile,
                "review_mode": args.review_mode,
                "image_paths": [str(path) for path in image_paths],
                "response_text": result.text,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
