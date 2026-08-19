---
name: remote-codex-update
description: Update a Codex CLI on a remote Linux host without outbound internet by downloading the official platform package locally, transferring it through an available SSH or mounted-workspace path, and activating it with integrity checks and rollback support.
---

# Remote Codex Update

Update an offline or network-restricted remote Codex installation without assuming a package manager, install root, transfer path, or persistence model.

## Authorization Boundary

Treat remote extraction, persistent configuration changes, symlink switches, process restarts, and deletion as separate mutations. Diagnose first and obtain explicit confirmation for the exact targets before writing. A request to update does not authorize terminating active Codex processes or deleting old releases.

Keep the existing release and a recoverable link or configuration backup by default. Never install globally with remote npm merely because npm happens to exist.

## Discover Before Choosing a Method

Inspect the target over its actual SSH alias:

```bash
echo "HOST=$(hostname) USER=$(id -un) HOME=$HOME"
uname -s
uname -m
command -v codex || true
codex --version 2>/dev/null || true
readlink -f "$(command -v codex)" 2>/dev/null || true
```

Also inspect symlink layers, ownership, writable version/cache directories, free space, active Codex processes, and any bootstrap manifest that could restore an older version after restart. Query the current official version and platform-package metadata from the networked local machine.

Classify the remote installation before changing it:

- **Persistent bootstrap:** update its offline cache and manifest as well as the live symlink. A live-only replacement is not durable.
- **Versioned user install:** extract a new sibling release and atomically switch the user-level link.
- **Unknown or system-managed install:** stop and identify its owner or installer; do not overwrite system files speculatively.

When a known target is involved, read [references/known-host-layouts.md](references/known-host-layouts.md) after live discovery. Treat those layouts as hints that must be revalidated, not current-state guarantees.

## Select Package And Transfer

Map `uname -m` and libc/runtime requirements to the matching official `@openai/codex@<version>-<platform>` package. Prefer the standalone binary package when the remote has no Node runtime.

Use the safest verified transfer path for that target:

- Use `scp` or SFTP when the SSH route is healthy.
- Use a mounted workspace only after proving its local and remote paths refer to the same target host.
- Never assume a drive mapping belongs to the requested remote.

Download once to a task-specific local staging directory. Record package size plus SHA1, SHA256, and SHA512. Compare npm `dist.shasum` and `dist.integrity` locally, then recompute at least SHA256 on every remote copy before extraction.

## Install And Activate

Use versioned paths and fail closed:

1. Refuse to overwrite an existing target release or cache file unless the user separately approves replacement.
2. Copy the verified archive into a target-specific staging path.
3. Recompute the remote hash and compare it with the locally recorded value.
4. Extract into a unique temporary sibling directory.
5. Run the extracted binary directly and require the exact expected `codex-cli <version>` output.
6. Move the validated temporary directory to its final versioned path.
7. Back up and update the persistent manifest or installer source when one exists.
8. Preserve the old link target, create a temporary new link, and atomically rename it over the stable link.
9. Verify the command resolved through the ordinary remote environment, its final target, version, hashes, and persistence metadata.

Do not restart or kill existing app-server, proxy, code-mode-host, or editor-extension processes during a normal update. Report that existing processes continue on their loaded version until naturally restarted. Do not replace editor-bundled Codex binaries unless they are explicitly in scope.

The warning `failed to clean up stale arg0 temp dirs` is non-fatal only when the requested version still returns successfully. Report it rather than hiding it.

## Rollback And Reporting

Rollback must restore both the stable link and any persistence manifest changed by the update. Verify the restored `codex --version`; do not delete the failed/new release as part of rollback without separate authorization.

Report each target independently:

- old and new versions;
- official metadata and local/remote hashes;
- package transfer path;
- active link and persistence source;
- backup and retained old release;
- active old-version processes and validation limits;
- any target that remains blocked by routing, authentication, storage, or permissions.
