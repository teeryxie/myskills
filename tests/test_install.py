import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="myskills-install-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "repository with spaces"
        self.script = self.root / "scripts" / "install.sh"
        self.script.parent.mkdir(parents=True)
        shutil.copy2(Path(__file__).resolve().parents[1] / "scripts" / "install.sh", self.script)
        self.destination = Path(self.temporary.name) / "installed skills"
        self.add_skill("example")

    def add_skill(self, name, folder=None):
        directory = self.root / "skills" / "testing" / (folder or name)
        directory.mkdir(parents=True)
        (directory / "SKILL.md").write_text(
            f"---\nname: {name}\ndescription: Test fixture.\n---\n", encoding="utf-8"
        )

    def install(self, *arguments):
        return subprocess.run(
            ["/bin/bash", str(self.script), *arguments],
            env={**os.environ, "CODEX_SKILLS_DIR": str(self.destination)},
            text=True,
            capture_output=True,
        )

    def test_link_and_repeat(self):
        result = self.install()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.destination / "example").is_symlink())
        result = self.install()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("already linked: 1", result.stdout)

    def test_copy_and_preserve_existing(self):
        result = self.install("--copy")
        self.assertEqual(result.returncode, 0, result.stderr)
        target = self.destination / "example" / "SKILL.md"
        target.write_text("local customization", encoding="utf-8")
        result = self.install("--copy")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(target.read_text(encoding="utf-8"), "local customization")

    def test_preserve_broken_link(self):
        self.destination.mkdir()
        target = self.destination / "example"
        target.symlink_to(self.destination / "missing")
        result = self.install()
        self.assertEqual(result.returncode, 2)
        self.assertEqual(os.readlink(target), str(self.destination / "missing"))

    def test_duplicate_name(self):
        self.add_skill("example", "duplicate")
        self.assertEqual(self.install().returncode, 66)

    def test_invalid_name(self):
        self.add_skill("../outside", "invalid")
        self.assertEqual(self.install().returncode, 65)
        self.assertFalse((self.destination.parent / "outside").exists())

    def test_unknown_argument(self):
        self.assertEqual(self.install("--invalid").returncode, 64)


if __name__ == "__main__":
    unittest.main()
