"""Upload a prebuilt archive only; never submit or manage runs."""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import tarfile
import urllib.error
import urllib.parse
import urllib.request
import uuid


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, msg, headers, newurl):
        raise ValueError("Refusing to redirect an authenticated upload")


def multipart(data, boundary):
    sha256 = hashlib.sha256(data).hexdigest()
    prefix = (f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; "
              f"filename=\"{sha256}\"\r\nContent-Type: application/x-tar\r\n\r\n").encode()
    return sha256, prefix + data + f"\r\n--{boundary}--\r\n".encode()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--server", required=True)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--token-env", default="DSTACK_TOKEN")
    parser.add_argument("--max-request-bytes", type=int, default=2 * 1024 * 1024)
    args = parser.parse_args()
    server = urllib.parse.urlsplit(args.server)
    if (server.scheme != "https" or not server.hostname or server.username or server.password
            or server.query or server.fragment or server.path not in {"", "/"}):
        parser.error("--server must be an HTTPS origin without credentials or a path")
    if args.receipt.exists():
        parser.error("Receipt already exists; inspect it before uploading again")
    token = os.environ.get(args.token_env)
    if not token:
        parser.error("Credential environment variable is missing")
    if args.archive.stat().st_size > args.max_request_bytes:
        parser.error("Archive alone exceeds the request limit")
    data = args.archive.read_bytes()
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:") as archive:
        members = archive.getmembers()
        if len(members) != 1 or members[0].name != "payload.tar.gz" or not members[0].isfile():
            parser.error("Expected one ordinary payload.tar.gz member in an uncompressed tar")
    boundary = "scopeupload" + uuid.uuid4().hex
    sha256, body = multipart(data, boundary)
    if len(body) > args.max_request_bytes:
        parser.error("Multipart request exceeds the configured limit")
    url = args.server.rstrip("/") + "/api/files/upload_archive"
    request = urllib.request.Request(url, body, headers={"Authorization": "Bearer " + token,
        "Content-Type": "multipart/form-data; boundary=" + boundary})
    try:
        with urllib.request.build_opener(NoRedirect()).open(request, timeout=90) as response:
            result = json.load(response)
    except urllib.error.HTTPError as exc:
        detail = exc.read(2048).decode("utf-8", errors="replace").replace(token, "[REDACTED]")
        raise RuntimeError(f"Upload rejected ({exc.code}): {detail}") from None
    if result.get("hash") != sha256:
        raise ValueError("Registered digest differs from the uploaded archive")
    archive_id = str(uuid.UUID(result["id"]))
    receipt = {"server": args.server.rstrip("/"), "id": archive_id, "hash": sha256,
               "archive_bytes": len(data), "request_bytes": len(body),
               "file_archives": [{"id": archive_id, "path": "/tmp/project-upload.tar.gz"}]}
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    with args.receipt.open("x", encoding="utf-8") as stream:
        json.dump(receipt, stream, indent=2)
        stream.write("\n")
    print(json.dumps(receipt))


if __name__ == "__main__":
    main()
