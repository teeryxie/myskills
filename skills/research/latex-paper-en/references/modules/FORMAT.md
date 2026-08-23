# Module: Format Check

**Trigger**: format, chktex, lint, 格式检查

## Commands

```bash
uv run --python 3.10 python scripts/check_format.py main.tex
uv run --python 3.10 python scripts/check_format.py main.tex --strict
```

## Details
Output: PASS / WARN / FAIL with categorized issues.
Ensure the document compiles before checking formats iteratively.
