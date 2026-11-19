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


class WebDesignGuidelinesTests(unittest.TestCase):
    def test_setup_packages_vercel_rules_as_a_managed_skill(self):
        manifest = manage.load(manage.ROOT / "manifest.json")
        source = manifest["sources"]["vercel-guidelines"]
        manifest = {"sources": {"vercel-guidelines": source}, "local_skills": []}
        commit = "a" * 40
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            upstream = root / "upstream"
            upstream.mkdir()
            (upstream / "LICENSE").write_text("MIT License\n")
            (upstream / "command.md").write_text("# Vercel UI rules\n")
            stage = root / "skills"
            stage.mkdir()
            resolved = {"sources": {"vercel-guidelines": {"commit": commit}}, "openspec": {}}
            with patch.object(manage, "fetch_source", return_value=upstream), patch.object(manage, "prepare_openspec"):
                manage.prepare(root, manifest, stage, resolved)

            skill = stage / "web-design-guidelines"
            self.assertEqual((skill / "references/command.md").read_text(), "# Vercel UI rules\n")
            self.assertIn(commit, (skill / "SKILL.md").read_text())
            self.assertIn("MIT License", (skill / "LICENSE").read_text())
            self.assertIn("allow_implicit_invocation: false", (skill / "agents/openai.yaml").read_text())


class EccDocumentationTests(unittest.TestCase):
    def test_setup_preserves_ecc_documentation_workflows_and_audit_files(self):
        sources = manage.load(manage.ROOT / "manifest.json")["sources"]
        self.assertIn("doc-updater", sources["ecc"]["skills"])
        self.assertEqual(sources["ecc-docs-governance"]["skills"], ["docs-governance"])
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            upstream = root / "upstream"
            agent = upstream / "agents/doc-updater.md"
            agent.parent.mkdir(parents=True)
            (upstream / "LICENSE").write_text("MIT License\n")
            agent.write_text("---\nname: doc-updater\ndescription: ECC docs\ntools: Read\nmodel: haiku\n---\n\nOriginal updater workflow.\n")
            governance = upstream / ".agents/skills/docs-governance"
            (governance / "scripts").mkdir(parents=True)
            (governance / "scripts/audit-docs.py").write_text("# Upstream script\n")
            (governance / "SKILL.md").write_text(
                "---\nname: docs-governance\ndescription: ECC audit\n---\n\nOriginal audit workflow.\n"
            )
            stage = root / "skills"
            stage.mkdir()
            manifest = {"sources": {
                "ecc": {**sources["ecc"], "skills": ["doc-updater"]},
                "ecc-docs-governance": sources["ecc-docs-governance"],
            }, "local_skills": []}
            resolved = {"sources": {name: {} for name in manifest["sources"]}, "openspec": {}}
            with patch.object(manage, "fetch_source", return_value=upstream), patch.object(manage, "prepare_openspec"):
                manage.prepare(root, manifest, stage, resolved)
            updater = (stage / "doc-updater/SKILL.md").read_text()
            self.assertIn("Original updater workflow.", updater)
            self.assertNotIn("model: haiku", updater)
            self.assertIn("Original audit workflow.", (stage / "docs-governance/SKILL.md").read_text())
            self.assertEqual((stage / "docs-governance/scripts/audit-docs.py").read_bytes(),
                             (governance / "scripts/audit-docs.py").read_bytes())
            for name in ("doc-updater", "docs-governance"):
                self.assertIn("disable-model-invocation: true", (stage / name / "SKILL.md").read_text())
                self.assertIn("allow_implicit_invocation: false", (stage / name / "agents/openai.yaml").read_text())


class SuperpowersWorkflowTests(unittest.TestCase):
    def test_full_inventory_uses_opt_in_workflow_without_bootstrap_hooks(self):
        manifest = manage.load(manage.ROOT / "manifest.json")
        source = manifest["sources"]["superpowers"]
        self.assertEqual(len(source["skills"]), 15)
        self.assertFalse(set(source["skills"]) & set(manifest["incompatible_skills"]))
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            upstream = root / "upstream"
            (upstream / "hooks").mkdir(parents=True)
            (upstream / "hooks/session-start").write_text("upstream hook")
            (upstream / "LICENSE").write_text("MIT License\n")
            for name in ("brainstorming", "systematic-debugging"):
                skill = upstream / "skills" / name
                skill.mkdir(parents=True)
                (skill / "SKILL.md").write_text(f"---\nname: {name}\n---\nUse superpowers:verification-before-completion.\n")
                (skill / "helper.md").write_text("Use superpowers:writing-plans.\n")
            stage = root / "stage"
            stage.mkdir()
            selected = {"local_skills": [], "sources": {"superpowers": {
                **source, "skills": ["brainstorming", "systematic-debugging"],
            }}}
            with patch.object(manage, "fetch_source", return_value=upstream), patch.object(manage, "prepare_openspec"):
                manage.prepare(root, selected, stage, {"sources": {"superpowers": {}}, "openspec": {}})
            workflow = stage / "brainstorming"
            self.assertIn("disable-model-invocation: true", (workflow / "SKILL.md").read_text())
            self.assertIn("allow_implicit_invocation: false", (workflow / "agents/openai.yaml").read_text())
            self.assertIn("allow_implicit_invocation: true",
                          (stage / "systematic-debugging/agents/openai.yaml").read_text())
            self.assertEqual((workflow / "helper.md").read_text(), "Use writing-plans.\n")
            self.assertFalse((stage / "hooks").exists())


class McpBuilderTests(unittest.TestCase):
    def test_setup_preserves_the_complete_upstream_skill(self):
        manifest = manage.load(manage.ROOT / "manifest.json")
        source = manifest["sources"]["anthropic-mcp-builder"]
        self.assertEqual(source["skills"], ["mcp-builder"])
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            upstream = root / "upstream"
            skill = upstream / "skills/mcp-builder"
            (skill / "scripts").mkdir(parents=True)
            (skill / "reference").mkdir()
            (skill / "LICENSE.txt").write_text("Apache License\nVersion 2.0\n")
            (skill / "SKILL.md").write_bytes(b"---\r\nname: mcp-builder\r\n---\r\nOriginal instructions.\r\n")
            (skill / "scripts/evaluation.py").write_text("# Original script\n")
            (skill / "reference/guide.md").write_text("Original reference\n")
            stage = root / "stage"
            stage.mkdir()
            manifest = {"sources": {"anthropic-mcp-builder": source}, "local_skills": []}
            resolved = {"sources": {"anthropic-mcp-builder": {}}, "openspec": {}}
            with patch.object(manage, "fetch_source", return_value=upstream), patch.object(manage, "prepare_openspec"):
                manage.prepare(root, manifest, stage, resolved)
            self.assertEqual(manage.hashes(stage / "mcp-builder"), manage.hashes(skill))


if __name__ == "__main__":
    unittest.main()
