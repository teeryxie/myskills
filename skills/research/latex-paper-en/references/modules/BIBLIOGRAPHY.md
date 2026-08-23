# Module: Bibliography

**Trigger**: bib, bibliography, 参考文献, citation

## Commands

```bash
uv run --python 3.10 python scripts/verify_bib.py references.bib
uv run --python 3.10 python scripts/verify_bib.py references.bib --tex main.tex
uv run --python 3.10 python scripts/verify_bib.py references.bib --standard gb7714
uv run --python 3.10 python scripts/verify_bib.py references.bib --tex main.tex --json
```

## Details
Checks: required fields, duplicate keys, missing citations, unused entries.
Key output fields: `missing_in_bib`, `unused_in_tex`.

See also: [CITATION_VERIFICATION.md](../references/CITATION_VERIFICATION.md) for API-based verification.
