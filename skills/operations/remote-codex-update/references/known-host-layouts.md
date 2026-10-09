# Known Host Layouts

Read only the section for the requested target, and revalidate every path before mutation.

## Telos dstack H20

- SSH alias: `telos_h20_8`
- Persistent root: `/mnt/cluster/.tools/xietianyu`
- Bootstrap manifest: `/mnt/cluster/.tools/xietianyu/bootstrap/manifest.env`
- Offline archive: `offline-cache/codex/<version>/linux-x64/openai-codex-<version>-linux-x64.tgz`
- Release: `codex/<version>` with the npm package's leading `package/` component stripped
- Stable link: `bin/codex`
- Container entry: `/usr/local/bin/codex` points to the stable link and normally does not need replacement
- Staging: `staging/codex-v<version>`
- Transfer: use `scp` through `telos_h20_8`; the Windows `W:` drive belongs to SICAU, not Telos

For a durable update, back up and replace exactly the manifest's `CODEX_VERSION`, `CODEX_ARCHIVE`, and `CODEX_SHA256` values after the new cache and release validate. Preserve the old release and a version-labelled rollback link.

## SICAU HPC

- SSH alias: `sicau_hpc`
- User home: `/public/home/xty`
- Release: `~/.local/opt/codex-<version>-linux-x64/package`
- Stable link: `~/.local/bin/codex`
- Mounted transfer path: local `W:/tmp` maps to remote `/public/home/xty/workdir/tmp`

Preserve the npm archive's leading `package/` directory for this layout. Validate the extracted binary at `package/vendor/x86_64-unknown-linux-musl/bin/codex`, retain the old release, and keep a rollback link such as `~/.local/bin/codex.prev` before an atomic switch.

SICAU SSH depends on the local Docker UniVPN/SOCKS5 route. A successful `W:` copy does not prove SSH health. If SSH returns an Ncat reachability error, leave the staged package intact and pause remote activation; do not modify Clash, Docker, or network state unless that repair is separately authorized.
