#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


def export_docx_to_pdf(input_docx: Path, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "soffice",
            "--headless",
            "--convert-to",
            "pdf",
            "--outdir",
            str(output_dir),
            str(input_docx),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return output_dir / f"{input_docx.stem}.pdf"


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert DOCX to PDF via LibreOffice.")
    parser.add_argument("--input-docx", required=True, help="DOCX source path")
    parser.add_argument("--output-dir", required=True, help="Directory for the generated PDF")
    args = parser.parse_args()

    pdf_path = export_docx_to_pdf(
        input_docx=Path(args.input_docx).expanduser().resolve(),
        output_dir=Path(args.output_dir).expanduser().resolve(),
    )
    print(pdf_path)


if __name__ == "__main__":
    main()
