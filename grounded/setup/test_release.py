import json
from pathlib import Path
import tempfile
import unittest
import zipfile

import release


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "grounded"
        self.root.mkdir()
        (self.root / ".claude-plugin").mkdir()
        self.paths = [self.root / "plugin.json", self.root / ".claude-plugin/plugin.json"]
        for path in self.paths:
            path.write_text(json.dumps({"name": "grounded", "version": "0.1.0", "description": "Keep this"}))
        self.output = self.root.parent / "grounded.zip"

    def test_bump_updates_both_hosts_without_losing_metadata(self):
        release.bump(self.root, "0.2.0")
        for path in self.paths:
            self.assertEqual(json.loads(path.read_text()), {"name": "grounded", "version": "0.2.0", "description": "Keep this"})

    def test_invalid_versions_do_not_change_files(self):
        before = [path.read_bytes() for path in self.paths]
        for version in ["v1.2.3", "01.2.3", "1.2", "1.2.3-rc.1", "1.2.3\n"]:
            with self.assertRaises(ValueError):
                release.bump(self.root, version)
        self.assertEqual([path.read_bytes() for path in self.paths], before)

    def test_mismatched_tag_or_host_version_prevents_packaging(self):
        with self.assertRaises(ValueError):
            release.package(self.root, "skills-v0.2.0", self.output)
        self.assertFalse(self.output.exists())
        data = json.loads(self.paths[1].read_text())
        data["version"] = "0.2.0"
        self.paths[1].write_text(json.dumps(data))
        with self.assertRaises(ValueError):
            release.package(self.root, "skills-v0.1.0", self.output)
        self.assertFalse(self.output.exists())

    def test_zip_contains_the_matching_manifests_and_skills(self):
        (self.root.parent / "LICENSE").write_text("Repository license")
        skill = self.root / "skills/adr/SKILL.md"
        skill.parent.mkdir(parents=True)
        skill.write_text("ADR procedure")
        cache = self.root / "setup/__pycache__/release.pyc"
        cache.parent.mkdir(parents=True)
        cache.write_bytes(b"cache")
        self.assertEqual(release.package(self.root, "skills-v0.1.0", self.output), "0.1.0")
        with zipfile.ZipFile(self.output) as archive:
            self.assertIn("skills/adr/SKILL.md", archive.namelist())
            self.assertEqual(archive.read("LICENSE").decode(), "Repository license")
            self.assertFalse(any("__pycache__" in name for name in archive.namelist()))
            for name in ["plugin.json", ".claude-plugin/plugin.json"]:
                self.assertEqual(json.loads(archive.read(name))["version"], "0.1.0")

    def test_output_inside_plugin_is_rejected(self):
        with self.assertRaises(ValueError):
            release.package(self.root, "skills-v0.1.0", self.root / "release.zip")


if __name__ == "__main__":
    unittest.main()
