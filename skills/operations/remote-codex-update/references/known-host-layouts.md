# Installation Layout Templates

Use these templates only after live discovery. Replace placeholders with the requested target's verified values. Do not encode personal hosts, usernames, internal addresses, or workstation-specific mounts in a public skill.

## Persistent Bootstrap Layout

Typical components:

- SSH alias: `<remote-alias>`
- Persistent root: `<persistent-root>`
- Bootstrap manifest: `<persistent-root>/bootstrap/manifest.env`
- Offline archive: `<persistent-root>/offline-cache/codex/<version>/<platform>/openai-codex-<version>-<platform>.tgz`
- Versioned release: `<persistent-root>/codex/<version>`
- Stable link: `<persistent-root>/bin/codex`
- Optional system/container entry: a stable link that points to `<persistent-root>/bin/codex`
- Staging: `<persistent-root>/staging/codex-v<version>`

For a durable update, identify every manifest field that controls version, archive name, platform triplet, and integrity hash. Back up the manifest, validate the new cache and release, then update only the discovered Codex fields. Preserve the old release and a version-labelled rollback link.

## Versioned User Layout

Typical components:

- SSH alias: `<remote-alias>`
- User home: `<remote-home>`
- Release: `<remote-home>/.local/opt/codex-<version>-<platform>`
- Stable link: `<remote-home>/.local/bin/codex`
- Staging: a verified writable workspace such as `<remote-workspace>/tmp`

Confirm whether extraction should preserve the npm archive's leading `package/` directory. Validate the exact extracted binary path before switching the stable link. Keep a version-labelled rollback link and the old release.

## Transfer Route Rules

- Use `scp` or SFTP when the target's SSH route is healthy.
- Use a local mounted workspace only after proving its local and remote paths map to the same requested host.
- A successful mounted-file copy does not prove SSH health.
- If SSH routing fails, leave the staged package intact and pause activation. Do not repair VPN, proxy, container, or routing state without separate authorization.
