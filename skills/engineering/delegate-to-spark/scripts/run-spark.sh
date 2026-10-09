#!/usr/bin/env bash
set -euo pipefail

effort="high"
sandbox="read-only"
workdir="$PWD"

usage() {
  printf '%s\n' \
    'Usage: run-spark.sh [--effort low|medium|high|xhigh] [--sandbox read-only|workspace-write] [--cwd DIR] -- PROMPT'
}

while (($#)); do
  case "$1" in
    --effort)
      [[ $# -ge 2 ]] || { usage >&2; exit 2; }
      effort="$2"
      shift 2
      ;;
    --sandbox)
      [[ $# -ge 2 ]] || { usage >&2; exit 2; }
      sandbox="$2"
      shift 2
      ;;
    --cwd)
      [[ $# -ge 2 ]] || { usage >&2; exit 2; }
      workdir="$2"
      shift 2
      ;;
    --)
      shift
      break
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      printf 'Unknown option: %s\n' "$1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

case "$effort" in
  low|medium|high|xhigh) ;;
  *) printf 'Invalid effort: %s\n' "$effort" >&2; exit 2 ;;
esac

case "$sandbox" in
  read-only|workspace-write) ;;
  *) printf 'Invalid sandbox: %s\n' "$sandbox" >&2; exit 2 ;;
esac

[[ -d "$workdir" ]] || { printf 'Working directory does not exist: %s\n' "$workdir" >&2; exit 2; }
command -v codex >/dev/null 2>&1 || { printf 'codex executable not found in PATH\n' >&2; exit 127; }
[[ $# -gt 0 ]] || { printf 'A non-empty prompt is required.\n' >&2; usage >&2; exit 2; }

task_prompt="$*"
worker_prompt='You are a bounded execution worker controlled by a stronger main agent. Do not invoke $delegate-to-spark, spawn subagents, or broaden the task. Follow the requested sandbox constraints. Return commands, evidence, changed paths, and a concise conclusion; do not claim final authority.'$'\n\n'"$task_prompt"

exec codex -a never exec \
  --ephemeral \
  --skip-git-repo-check \
  -m gpt-5.3-codex-spark \
  -c "model_reasoning_effort=\"$effort\"" \
  -s "$sandbox" \
  -C "$workdir" \
  "$worker_prompt"
