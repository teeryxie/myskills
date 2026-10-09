"""Offline contract checks; no credentials, network, or cluster operations."""
import gzip
import hashlib
import io
import json
from pathlib import Path
import subprocess
import tarfile
import tempfile
import unittest

from bundle import build
from upload_archive import multipart


class BundleTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp.name) / "repo"
        self.repo.mkdir()
        self.command("init", "-q")
        self.command("config", "core.autocrlf", "false")
        (self.repo / "src").mkdir()
        (self.repo / "src/start.sh").write_bytes(b"#!/bin/bash\r\nprintf 'ok\\n'\r\n")
        (self.repo / "src/data.bin").write_bytes(b"\x00\xff\r\n")
        (self.repo / "outside.txt").write_text("not selected")
        self.commit()

    def tearDown(self):
        self.temp.cleanup()

    def command(self, *args):
        return subprocess.check_output(["git", "-C", str(self.repo), *args], stderr=subprocess.STDOUT)

    def commit(self):
        self.command("add", ".")
        self.command("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                     "commit", "-qm", "fixture")

    def test_deterministic_roundtrip_and_manifest(self):
        data, manifest = build(self.repo, ["src"])
        self.assertEqual(data, build(self.repo, ["src"])[0])
        self.assertEqual(manifest["archive_sha256"], hashlib.sha256(data).hexdigest())
        with tarfile.open(fileobj=io.BytesIO(data), mode="r:") as outer:
            self.assertEqual(outer.getnames(), ["payload.tar.gz"])
            payload = outer.extractfile("payload.tar.gz").read()
        with tarfile.open(fileobj=io.BytesIO(gzip.decompress(payload)), mode="r:") as inner:
            self.assertEqual(inner.extractfile("src/start.sh").read(), b"#!/bin/bash\nprintf 'ok\\n'\n")
            self.assertEqual(inner.extractfile("src/data.bin").read(), b"\x00\xff\r\n")
            self.assertEqual(inner.getmember("src/start.sh").mode, 0o755)
            self.assertNotIn("outside.txt", inner.getnames())
            source = json.load(inner.extractfile("SOURCE_MANIFEST.json"))
            for record in source["files"]:
                self.assertEqual(hashlib.sha256(inner.extractfile(record["path"]).read()).hexdigest(), record["sha256"])

    def test_dirty_tree_is_rejected(self):
        (self.repo / "src/start.sh").write_text("changed")
        with self.assertRaisesRegex(ValueError, "dirty"):
            build(self.repo, ["src"])

    def test_missing_and_outside_paths_are_rejected(self):
        for name in ["../outside", "/root", ".", "missing", "C:/absolute"]:
            with self.subTest(name=name), self.assertRaises(ValueError):
                build(self.repo, [name])

    def test_limit_is_enforced(self):
        with self.assertRaisesRegex(ValueError, "budget"):
            build(self.repo, ["src"], limit=1)

    def test_obvious_secret_file_is_rejected(self):
        (self.repo / "src/service.token").write_text("fixture-only")
        self.commit()
        with self.assertRaisesRegex(ValueError, "Credential"):
            build(self.repo, ["src"])

    def test_upload_filename_is_raw_outer_digest(self):
        data, _ = build(self.repo, ["src"])
        digest, body = multipart(data, "test-boundary")
        self.assertIn(('filename="' + hashlib.sha256(data).hexdigest() + '"').encode(), body)
        self.assertIn(b"\r\n\r\n" + data + b"\r\n--test-boundary--", body)
        self.assertEqual(digest, hashlib.sha256(data).hexdigest())
        self.assertLess(len(body), 2 * 1024 * 1024)


if __name__ == "__main__":
    unittest.main(verbosity=2)
