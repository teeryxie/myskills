#!/usr/bin/env bash
set -euo pipefail

repo_root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
skills_root="$repo_root/skills"
destination=${CODEX_SKILLS_DIR:-"$HOME/.agents/skills"}
mode=link

if [[ ${1:-} == "--copy" ]]; then
  mode=copy
elif [[ $# -gt 0 ]]; then
  printf 'Usage: %s [--copy]\n' "$0" >&2
  exit 64
fi

mkdir -p -- "$destination"

names=()
directories=()
installed=0
existing=0
skipped=0

while IFS= read -r -d '' skill_file; do
  skill_dir=$(dirname -- "$skill_file")
  name=$(awk '
    /^name:[[:space:]]*/ {
      value = $0
      sub(/^name:[[:space:]]*/, "", value)
      gsub(/^[[:space:]]+|[[:space:]]+$/, "", value)
      gsub(/^["\047]|["\047]$/, "", value)
      print value
      exit
    }
  ' "$skill_file")

  if [[ ! $name =~ ^[a-z0-9][a-z0-9-]{0,63}$ ]]; then
    printf 'Missing or invalid frontmatter name: %s\n' "$skill_file" >&2
    exit 65
  fi
  for ((index = 0; index < ${#names[@]}; index++)); do
    if [[ ${names[$index]} == "$name" ]]; then
      printf 'Duplicate skill name %s: %s and %s\n' "$name" "$skill_dir" "${directories[$index]}" >&2
      exit 66
    fi
  done
  names[${#names[@]}]=$name
  directories[${#directories[@]}]=$skill_dir

  target="$destination/$name"
  if [[ -e $target || -L $target ]]; then
    if [[ -L $target && -d $target && $(cd -- "$target" && pwd -P) == $(cd -- "$skill_dir" && pwd -P) ]]; then
      printf 'EXISTS %s -> %s\n' "$name" "$skill_dir"
      ((existing += 1))
    else
      printf 'SKIP %s: destination already exists and is not this repository link: %s\n' "$name" "$target" >&2
      ((skipped += 1))
    fi
    continue
  fi

  if [[ $mode == copy ]]; then
    cp -a -- "$skill_dir" "$target"
    printf 'COPIED %s -> %s\n' "$name" "$target"
  else
    ln -s -- "$skill_dir" "$target"
    printf 'LINKED %s -> %s\n' "$name" "$skill_dir"
  fi
  ((installed += 1))
done < <(find "$skills_root" -type f -name SKILL.md -print0 | sort -z)

printf 'Skills discovered: %d\n' "${#names[@]}"
printf 'Installed: %d; already linked: %d; skipped conflicts: %d\n' "$installed" "$existing" "$skipped"

if (( skipped > 0 )); then
  exit 2
fi
