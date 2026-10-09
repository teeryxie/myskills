---
name: delegate-to-spark
description: Delegate bounded, independently verifiable coding or validation work to GPT-5.3-Codex-Spark while the main agent retains planning and final judgment. Use when the user explicitly asks for Spark, a fast subagent, or rapid parallel iteration, or when focused tests, bug reproduction, scoped inspection, mechanical edits, benchmarks, or hypothesis checks would benefit from a fast separate model pass.
---

# Delegate to Spark

Use GPT-5.3-Codex-Spark as an execution worker. Keep task decomposition, risk decisions, integration, and the final answer with the main agent.

## Workflow

1. Define one bounded subtask with an observable completion condition. Include exact paths, commands, constraints, and requested evidence.
2. Use native subagent delegation with model `gpt-5.3-codex-spark` when the active runtime explicitly offers that model.
3. If native delegation rejects or does not list Spark, run `scripts/run-spark.sh` from this skill.
4. Default to `--effort high`. Use `xhigh` for a bounded task that genuinely needs deeper reasoning; use `low` or `medium` only when latency matters more than depth.
5. Default to `--sandbox read-only`. Use `workspace-write` only when the delegated task explicitly requires a small implementation or test edit.
6. Inspect the worker's commands, evidence, diffs, and conclusions. Re-run critical verification with the main agent when correctness or risk warrants it.
7. Stop delegating and take over with the main model if results are contradictory, unverifiable, out of scope, or fail twice.

## CLI Fallback

Invoke the bundled launcher with an explicit working directory and a self-contained prompt:

```bash
"${CODEX_HOME:-$HOME/.codex}/skills/delegate-to-spark/scripts/run-spark.sh" \
  --effort high \
  --sandbox read-only \
  --cwd /absolute/project/path \
  -- "Run the focused test and return the command, exit code, and failure location. Do not edit files."
```

The launcher uses an ephemeral Codex session, requests the exact model slug `gpt-5.3-codex-spark`, prevents recursive delegation, and refuses `danger-full-access`.

Before installing this Skill on another host, require a working `codex`
binary, a non-interactive authenticated provider session, and an actual bounded
launcher call that confirms the requested model is accepted. Copying this
Skill or passing `codex login status` alone is not sufficient evidence.

## Guardrails

- Delegate architecture, ambiguous product decisions, security, permissions, destructive operations, broad migrations, and final correctness judgments to the main model only.
- Do not treat the worker's claim about its model identity as proof. Use the launcher trace to confirm the requested model and provider; recognize that a custom provider may remap the model server-side.
- Do not ask Spark to delegate again or orchestrate other workers.
- Parallelize only independent tasks that cannot write the same files or mutate shared state.
- Report material fallback-metadata warnings because they can affect tool behavior or context handling.
