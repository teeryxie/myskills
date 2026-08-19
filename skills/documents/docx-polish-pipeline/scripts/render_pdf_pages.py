#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


def get_page_count(input_pdf: Path) -> int:
    result = subprocess.run(
        ["pdfinfo", str(input_pdf)],
        check=True,
        capture_output=True,
        text=True,
    )
    for line in result.stdout.splitlines():
        if line.startswith("Pages:"):
            return int(line.split(":", 1)[1].strip())
    raise RuntimeError("Unable to read page count from pdfinfo output.")


def parse_page_spec(spec: str, page_count: int) -> list[int]:
    if not spec or spec == "all":
        return list(range(1, page_count + 1))
    pages: set[int] = set()
    for token in spec.split(","):
        token = token.strip().lower()
        if not token:
            continue
        if token == "last":
            pages.add(page_count)
            continue
        if "-" in token:
            start_text, end_text = token.split("-", 1)
            start = 1 if start_text == "first" else page_count if start_text == "last" else int(start_text)
            end = 1 if end_text == "first" else page_count if end_text == "last" else int(end_text)
            low, high = sorted((start, end))
            pages.update(range(low, high + 1))
            continue
        pages.add(int(token))
    return sorted(page for page in pages if 1 <= page <= page_count)


def render_pages(input_pdf: Path, output_dir: Path, dpi: int = 180, page_spec: str = "all") -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    page_count = get_page_count(input_pdf)
    pages = parse_page_spec(page_spec, page_count)
    rendered: list[Path] = []
    for page in pages:
        prefix = output_dir / "page"
        subprocess.run(
            [
                "pdftoppm",
                "-png",
                "-r",
                str(dpi),
                "-f",
                str(page),
                "-l",
                str(page),
                str(input_pdf),
                str(prefix),
            ],
            check=True,
        )
        rendered.append(output_dir / f"page-{page}.png")
    return rendered


def main() -> None:
    parser = argparse.ArgumentParser(description="Render selected PDF pages to PNG.")
    parser.add_argument("--input-pdf", required=True, help="PDF source path")
    parser.add_argument("--output-dir", required=True, help="Directory for rendered PNG files")
    parser.add_argument("--dpi", type=int, default=180, help="Render DPI")
    parser.add_argument("--pages", default="all", help="Page spec, e.g. all, 1,3,last, 1-3")
    args = parser.parse_args()

    files = render_pages(
        input_pdf=Path(args.input_pdf).expanduser().resolve(),
        output_dir=Path(args.output_dir).expanduser().resolve(),
        dpi=args.dpi,
        page_spec=args.pages,
    )
    print("\n".join(str(path) for path in files))


if __name__ == "__main__":
    main()
