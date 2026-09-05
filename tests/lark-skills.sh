#!/usr/bin/env bash
set -euo pipefail

repo_root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
validator=${SKILL_VALIDATOR:-"${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py"}
skills=(lark-ops-control lark-progress-sync lark-weekly-report-submit)

for skill in "${skills[@]}"; do
  skill_dir="$repo_root/skills/integrations/$skill"
  test -f "$skill_dir/SKILL.md"
  test -f "$skill_dir/agents/openai.yaml"
  rg -q '^name:[[:space:]]*[a-z0-9][a-z0-9-]{0,63}$' "$skill_dir/SKILL.md"
  rg -q '^description:[[:space:]]*\S' "$skill_dir/SKILL.md"
  rg -q 'bins:[[:space:]]*\["lark-cli"\]' "$skill_dir/SKILL.md"

  if test -f "$validator"; then
    uv run --python 3.10 --with pyyaml python "$validator" "$skill_dir"
  fi
done

test -f "$repo_root/skills/integrations/lark-ops-control/references/setup-and-validation.md"
test -f "$repo_root/skills/integrations/lark-ops-control/references/permissions.md"
test -f "$repo_root/skills/integrations/lark-ops-control/references/official-suite.md"
test -f "$repo_root/third_party/licenses/larksuite-cli-MIT.txt"

if rg -n 'TODO|\[TODO|Help with Lark' \
  "$repo_root/skills/integrations/lark-ops-control" \
  "$repo_root/skills/integrations/lark-progress-sync" \
  "$repo_root/skills/integrations/lark-weekly-report-submit"; then
  printf 'Unfinished scaffold content found in Lark skills\n' >&2
  exit 1
fi

if rg -n '(cli|ou|oc|om)_[0-9a-z]{8,}|/Users/|feishu\.cn/(wiki|docx)/[0-9A-Za-z]+' \
  "$repo_root/skills/integrations/lark-ops-control" \
  "$repo_root/skills/integrations/lark-progress-sync" \
  "$repo_root/skills/integrations/lark-weekly-report-submit"; then
  printf 'Potential Lark identifier or personal path found\n' >&2
  exit 1
fi

if command -v lark-cli >/dev/null 2>&1; then
  lark-cli --version >/dev/null
  lark-cli skills list >/dev/null
fi

skill_count=$(find "$repo_root/skills" -type f -name SKILL.md | wc -l | tr -d ' ')
test "$skill_count" = 56

printf 'lark-skills: validated %d custom skills; repository has %s skills\n' \
  "${#skills[@]}" "$skill_count"
