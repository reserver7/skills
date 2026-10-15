import argparse
import contextlib
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import manage


class ConfigureTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name)
        self.args = argparse.Namespace(home=self.home, host="both", dry_run=False)
        self.state = self.home / ".local/share/skills-environment"
        self.codex = self.home / ".codex/AGENTS.md"
        self.claude = self.home / ".claude/CLAUDE.md"
        self.codex.parent.mkdir()
        self.codex.write_text("Personal Codex rules\n")

    def configure(self):
        with contextlib.redirect_stdout(io.StringIO()):
            manage.configure(self.args, self.state)

    def test_preserves_personal_rules_without_installing_duplicate_skills(self):
        self.configure()
        self.assertTrue(self.codex.read_text().startswith("Personal Codex rules\n"))
        for path in [self.codex, self.claude]:
            self.assertEqual(path.read_text().count(manage.BEGIN), 1)
            version = manage.load(manage.ROOT / "plugin.json")["version"]
            self.assertIn(f"<!-- grounded-version: {version} -->", path.read_text())
            self.assertIn((manage.ROOT / "rules/development.md").read_text().strip(), path.read_text())
        self.assertFalse((self.home / ".agents/skills").exists())
        self.assertFalse((self.home / ".claude/skills").exists())
        self.assertFalse((self.state / "npm").exists())
        backups = list((self.state / "backups").rglob("*.md"))
        self.assertEqual([p.read_text() for p in backups], ["Personal Codex rules\n"])

    def test_rerun_is_idempotent_and_updates_existing_block(self):
        self.configure()
        original = self.codex.read_text()
        backups = list((self.state / "backups").iterdir())
        self.configure()
        self.assertEqual(self.codex.read_text(), original)
        self.assertEqual(list((self.state / "backups").iterdir()), backups)
        self.codex.write_text("Personal Codex rules\n" + manage.BEGIN + "\nstale policy\n" + manage.END + "\nPersonal suffix\n")
        self.configure()
        self.assertNotIn("stale policy", self.codex.read_text())
        self.assertTrue(self.codex.read_text().endswith("Personal suffix\n"))
        self.assertEqual(self.codex.read_text().count(manage.BEGIN), 1)

    def test_rerun_refreshes_the_configured_version(self):
        self.configure()
        version = manage.load(manage.ROOT / "plugin.json")["version"]
        self.codex.write_text(self.codex.read_text().replace(
            f"<!-- grounded-version: {version} -->", "<!-- grounded-version: 0.0.0 -->"))
        self.configure()
        self.assertIn(f"<!-- grounded-version: {version} -->", self.codex.read_text())
        self.assertNotIn("<!-- grounded-version: 0.0.0 -->", self.codex.read_text())
        self.assertEqual(self.codex.read_text().count(manage.BEGIN), 1)

    def test_dry_run_and_host_selection(self):
        self.args.dry_run = True
        self.configure()
        self.assertEqual(self.codex.read_text(), "Personal Codex rules\n")
        self.assertFalse(self.claude.exists())
        self.assertFalse(self.state.exists())
        self.args.dry_run = False
        self.args.host = "codex"
        self.configure()
        self.assertFalse(self.claude.exists())

    def test_malformed_second_host_prevents_all_changes(self):
        self.claude.parent.mkdir()
        self.claude.write_text(manage.BEGIN)
        with self.assertRaises(ValueError):
            self.configure()
        self.assertEqual(self.codex.read_text(), "Personal Codex rules\n")
        self.assertFalse(self.state.exists())

    def test_symlink_is_preserved(self):
        target = self.home / "personal.md"
        target.write_text("Personal target\n")
        self.claude.parent.mkdir()
        self.claude.symlink_to(target)
        with self.assertRaises(ValueError):
            self.configure()
        self.assertEqual(target.read_text(), "Personal target\n")
        self.assertEqual(self.codex.read_text(), "Personal Codex rules\n")

    def test_write_failure_restores_existing_and_new_files(self):
        write_text = Path.write_text

        def fail_second(path, *args, **kwargs):
            if path == self.claude:
                raise OSError("simulated write failure")
            return write_text(path, *args, **kwargs)

        with patch.object(Path, "write_text", fail_second):
            with self.assertRaises(OSError):
                self.configure()
        self.assertEqual(self.codex.read_text(), "Personal Codex rules\n")
        self.assertFalse(self.claude.exists())


if __name__ == "__main__":
    unittest.main()
