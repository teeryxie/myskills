"""Build a deterministic dstack tar containing one compressed project payload."""
import argparse
import gzip
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import subprocess
import tarfile


TEXT_SUFFIXES = {".sh", ".py", ".md", ".txt", ".json", ".jsonl", ".yaml", ".yml", ".toml"}


def git(repo, *args):
    return subprocess.check_output(["git", "--literal-pathspecs", "-C", str(repo), *args])


def tar_bytes(entries):
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w", format=tarfile.PAX_FORMAT) as archive:
        for name, data, mode in entries:
            info = tarfile.TarInfo(name)
            info.size, info.mode, info.mtime = len(data), mode, 0
            archive.addfile(info, io.BytesIO(data))
    return buffer.getvalue()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def build(repo, includes, limit=2 * 1024 * 1024 - 8192):
    repo = Path(repo).resolve()
    if Path(git(repo, "rev-parse", "--show-toplevel").decode().strip()).resolve() != repo:
        raise ValueError("--repo must be the repository root")
    if git(repo, "status", "--porcelain"):
        raise ValueError("Commit or otherwise resolve the dirty worktree before packaging")
    if not includes:
        raise ValueError("Choose explicit tracked paths")
    selected = set()
    for include in includes:
        path = PurePosixPath(include.replace("\\", "/"))
        if path.is_absolute() or ".." in path.parts or ":" in str(path) or str(path) == ".":
            raise ValueError("Includes must be explicit repository-relative paths")
        matches = git(repo, "ls-files", "-z", "--", str(path)).split(b"\0")
        matches = [name.decode("utf-8") for name in matches if name]
        if not matches:
            raise ValueError("No tracked files matched: " + str(path))
        selected.update(matches)
    revision = git(repo, "rev-parse", "HEAD").decode().strip()
    entries, records = [], []
    for relative in sorted(selected):
        name = PurePosixPath(relative)
        lower = name.name.lower()
        if (lower in {"service.token", ".env", "credentials", "credentials.json"}
                or lower.endswith((".pem", ".key"))
                or (lower.startswith(".env.") and lower not in {".env.example", ".env.sample"})):
            raise ValueError("Credential-like filename requires exclusion: " + relative)
        path = repo / relative
        if any((repo.joinpath(*name.parts[:i])).is_symlink() for i in range(1, len(name.parts) + 1)):
            raise ValueError("Symlink is not a portable source file: " + relative)
        if not path.is_file() or repo not in path.resolve().parents:
            raise ValueError("Not an ordinary in-repository file: " + relative)
        if relative == "SOURCE_MANIFEST.json":
            raise ValueError("SOURCE_MANIFEST.json is reserved")
        data = path.read_bytes()
        if path.suffix.lower() in TEXT_SUFFIXES:
            data.decode("utf-8")
            data = data.replace(b"\r\n", b"\n")
        mode = 0o755 if path.suffix == ".sh" else 0o644
        records.append({"path": relative, "size": len(data), "sha256": digest(data), "mode": oct(mode)})
        entries.append((relative, data, mode))
    source = {"commit": revision, "files": records}
    entries.append(("SOURCE_MANIFEST.json", (json.dumps(source, indent=2) + "\n").encode(), 0o644))
    compressed = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", fileobj=compressed, mtime=0) as stream:
        stream.write(tar_bytes(entries))
    payload = compressed.getvalue()
    outer = tar_bytes([("payload.tar.gz", payload, 0o644)])
    if len(outer) > limit:
        raise ValueError(f"Archive is {len(outer)} bytes; allowed archive budget is {limit}")
    # Recheck tracked worktree state after reading; publication still needs a quiet checkout.
    if git(repo, "status", "--porcelain") or git(repo, "rev-parse", "HEAD").decode().strip() != revision:
        raise ValueError("Repository changed while packaging")
    manifest = dict(source, archive_sha256=digest(outer), archive_bytes=len(outer),
                    payload_sha256=digest(payload), target_kind="file")
    return outer, manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--include", action="append", required=True)
    parser.add_argument("--max-archive-bytes", type=int, default=2 * 1024 * 1024 - 8192)
    args = parser.parse_args()
    repo, out = args.repo.resolve(), args.out.resolve()
    if out == repo or repo in out.parents:
        parser.error("Output must be outside the source repository")
    data, manifest = build(repo, args.include, args.max_archive_bytes)
    out.mkdir(parents=True, exist_ok=False)
    (out / "upload.tar").write_bytes(data)
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"commit": manifest["commit"], "files": len(manifest["files"]),
                      "archive_bytes": len(data), "archive_sha256": manifest["archive_sha256"],
                      "output": str(out)}))


if __name__ == "__main__":
    main()
