#!/usr/bin/env bash
set -euo pipefail

repo_root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
skills=(latex-paper-en latex-thesis-zh notion-paper-read)
validator=${SKILL_VALIDATOR:-"${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py"}
task_pycache=$(mktemp -d "${TMPDIR:-/tmp}/myskills-pycache-XXXXXX")

for skill in "${skills[@]}"; do
  skill_dir="$repo_root/skills/research/$skill"
  skill_file="$skill_dir/SKILL.md"

  test -f "$skill_file"
  rg -q '^name:[[:space:]]*[a-z0-9][a-z0-9-]{0,63}$' "$skill_file"
  rg -q '^description:[[:space:]]*\S' "$skill_file"

  if test -f "$validator"; then
    uv run --python 3.10 --with pyyaml python "$validator" "$skill_dir"
  fi

  while IFS= read -r -d '' file; do
    lines=$(wc -l < "$file")
    if ((lines > 500)); then
      printf 'File exceeds 500 lines: %s (%d)\n' "$file" "$lines" >&2
      exit 1
    fi
  done < <(find "$skill_dir" -type f \( -name '*.md' -o -name '*.py' -o -name '*.sh' -o -name '*.yaml' -o -name '*.yml' \) -print0)

  if rg -n -i '(api[_-]?key|access[_-]?token|password|private[_-]?key)[[:space:]]*[:=][[:space:]]*["'"'][^"'"']+["'"']' "$skill_dir"; then
    printf 'Potential embedded credential found in %s\n' "$skill_dir" >&2
    exit 1
  fi

  if rg -n '(/public/home/xty|/home/xty|C:\\Users\\[^\\]+)' "$skill_dir"; then
    printf 'Personal absolute path found in %s\n' "$skill_dir" >&2
    exit 1
  fi
done

PYTHONPYCACHEPREFIX="$task_pycache" uv run --python 3.10 python -m compileall -q \
  "$repo_root/skills/research/latex-paper-en/scripts" \
  "$repo_root/skills/research/latex-thesis-zh/scripts"

printf 'dev_1.1.0_20260823: validated %d skills\n' "${#skills[@]}"
