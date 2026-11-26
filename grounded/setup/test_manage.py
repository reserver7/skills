import argparse
import contextlib
import io
import subprocess
import sys
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import manage


class PolicyBudgetTests(unittest.TestCase):
    def test_accepts_policy_at_14000_bytes(self):
        self.assertIsNone(manage.validate_policy_budget(b"x" * 14000))

    def test_rejects_policy_at_14001_bytes(self):
        with self.assertRaisesRegex(ValueError, "Default policy exceeds the 14KB budget"):
            manage.validate_policy_budget(b"x" * 14001)


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


class DevelopmentPolicyTests(unittest.TestCase):
    def test_explicit_superpowers_workflows_load_the_opt_in_gate(self):
        policy = (manage.ROOT / "rules/development.md").read_text()
        self.assertIn(
            "When explicitly selected, use `using-superpowers` as the gate before task-specific Superpowers procedures",
            policy,
        )
        self.assertIn("Do not load it for default Grounded work.", policy)

    def test_installer_accepts_current_policy_size(self):
        manifest = manage.load(manage.ROOT / "manifest.json")
        manage.validate_repo(manifest)

    def test_announces_skill_plan_before_action(self):
        policy = (manage.ROOT / "rules/development.md").read_text()
        self.assertIn(
            "After inspection, announce only selected skills/roles (or none); never preview candidates.",
            policy,
        )

    def test_context7_precedes_version_sensitive_work_and_counts_ci_action_tags(self):
        policy = (manage.ROOT / "rules/development.md").read_text()
        self.assertIn(
            "For a pinned library/API/CLI/cloud service or CI action used by the work, resolve/query Context7 for that version before dependent work.",
            policy,
        )
        self.assertIn("fetch the exact official remote release, tag, or package artifact", policy)
        self.assertIn("Lack of a local installation is not unavailability", policy)
        self.assertIn("unversioned current docs do not prove a pinned version", policy)
        self.assertIn("A task spec or acceptance test states intended/repository behavior, not external API support.", policy)
        self.assertIn("Verify each library separately", policy)
        self.assertIn("pause only API-dependent edits or claims and continue independent authorized work", policy)
        self.assertIn("if one route fails, try one other official exact-version source", policy)

    def test_skill_selection_maps_changed_surfaces_without_forcing_bundles(self):
        policy = (manage.ROOT / "rules/development.md").read_text()
        self.assertIn("For existing work/reviews, preflight before skills:", policy)
        self.assertIn("Finish preflight before skill selection; never combine `SKILL.md` reads with that pass.", policy)
        self.assertIn("Read each once and handle prerequisites before dependent work.", policy)
        self.assertIn("Map owners to observed behavior and explicitly requested target surfaces", policy)
        self.assertIn("Cover affected/requested surfaces and matching material risks", policy)
        self.assertIn("even when enforcement files are unchanged", policy)
        self.assertIn("Include inherited trust boundaries even when enforcement files are unchanged.", policy)
        self.assertIn("Cover required roles before dependent work", policy)
        self.assertIn("Match evidenced/requested tech/services to owner cues; read every matching skill before source fallback.", policy)
        self.assertIn("blocked sources don't erase matches.", policy)
        self.assertIn("Never enumerate/search `.agents/skills`", policy)
        self.assertIn("open matched `SKILL.md` by exact path, including ignored files", policy)
        self.assertIn("if missing, query host inventory by exact name once.", policy)
        self.assertIn("a broad description or generic \"always\" wording does not broaden its trigger", policy)
        self.assertIn("Any Supabase product or SDK use, including an injected client/API or Realtime channel: use `supabase`, even when the edited file does not import the package.", policy)
        self.assertIn("Injected clients retain their service owner", policy)
        self.assertIn("Workflow skills do not replace domain expertise.", policy)
        self.assertIn("Ponytail is optional; use only when its minimal-diff role adds value beyond the selected specialist.", policy)
        self.assertIn("Skip when Superpowers directs edits.", policy)

    def test_documentation_skill_is_reserved_for_reconciliation_work(self):
        policy = (manage.ROOT / "rules/development.md").read_text()
        self.assertIn(
            "Use ECC `doc-updater` for coordinated cross-document/contract changes (even short ones)",
            policy,
        )
        self.assertIn("Direct-edit short factual changes only within one doc.", policy)

    def test_requested_target_surfaces_are_owned_before_files_or_dependencies_exist(self):
        policy = (manage.ROOT / "rules/development.md").read_text()
        self.assertIn("explicitly requested target surfaces", policy)
        self.assertIn("even if files/dependencies/source are absent", policy)
        self.assertIn("absence does not erase ownership", policy)
        self.assertIn("read every matching skill before source fallback", policy)

    def test_openspec_discovery_checks_ignored_paths_before_reporting_absence(self):
        policy = (manage.ROOT / "rules/development.md").read_text()
        self.assertIn("including ignored via ignore-aware search", policy)

    def test_quality_per_token_reuses_evidence_without_omitting_needed_checks(self):
        policy = (manage.ROOT / "rules/development.md").read_text()
        self.assertIn("Optimize quality per token: choose the smallest set of distinct skills and checks", policy)
        self.assertIn("Carry valid evidence; add or rerun only for changed behavior, prior misses, uncovered risk, or requested broader coverage.", policy)
        self.assertIn("for identical coverage at one revision, run either the focused test or project suite, not both unless acceptance requires both", policy)
        self.assertIn("never omit needed expertise or a check solely to save tokens.", policy)

    def test_react_specialist_is_conditional_on_framework_behavior(self):
        policy = (manage.ROOT / "rules/development.md").read_text()
        self.assertIn(
            "Use `vercel-react-best-practices` when changed React/Next components, hooks, rendering, routing, or broader integration rely on framework semantics.",
            policy,
        )
        self.assertIn("Component API/composition: `vercel-composition-patterns`.", policy)
        self.assertNotIn("always load `vercel-react-best-practices`", policy)

    def test_resume_requires_explicit_interrupted_task_continuity(self):
        policy = (manage.ROOT / "rules/development.md").read_text()
        self.assertIn(
            "At fresh start, read applicable AGENTS.md before skill selection; name no skill until task evidence is reviewed.",
            policy,
        )
        self.assertIn("context-mode availability, repo familiarity, or chat history alone do not qualify.", policy)

    def test_new_features_do_not_trigger_systematic_debugging(self):
        policy = (manage.ROOT / "rules/development.md").read_text()
        self.assertIn("A failing test that only shows requested new behavior is absent is the expected red step; do not load debugging solely for that.", policy)

    def test_high_risk_behavior_uses_exact_test_first_evidence(self):
        policy = (manage.ROOT / "rules/development.md").read_text()
        self.assertIn("Use `test-driven-development` for nontrivial changes when tests are allowed; skip it for low-risk localized bugs with an exact existing focused test.", policy)
        self.assertIn("Treat public API/module-contract behavior, trust boundaries, destructive or persistent data, concurrency/idempotency, external effects, and rollback as nontrivial regardless of size.", policy)
        self.assertIn("existing tests count only if they assert that path", policy)
        self.assertIn(
            "The TDD red step must be an assertion failure about missing behavior, not an error or setup failure; correct the test/harness before implementation.",
            policy,
        )
        self.assertIn("Unless prohibited, run relevant focused tests after changes; edit-only limits writes, not checks.", policy)
        self.assertIn(
            "After test/tool runs, inspect the worktree diff; remove generated artifacts outside scope and report all remaining changed files.",
            policy,
        )
        self.assertIn("Post-fix tests are regression evidence, not red evidence.", policy)

    def test_structured_input_checks_cover_invalid_field_values(self):
        policy = (manage.ROOT / "rules/development.md").read_text()
        self.assertIn(
            "For structured input formats, test malformed structure and plausible structure with invalid field values",
            policy,
        )

    def test_workload_identity_and_tenant_boundaries_use_security_skill(self):
        policy = (manage.ROOT / "rules/development.md").read_text()
        self.assertIn(
            "Authentication, authorization (including workload identity/OIDC, CI token grants, and production credentials), untrusted input, or personal data: Addy `security-and-hardening`.",
            policy,
        )
        self.assertIn(
            "Creating, migrating, or reviewing a tenant boundary or its schema also uses `security-and-hardening`",
            policy,
        )

    def test_skill_reporting_includes_read_guidance_and_distinguishes_no_finding(self):
        policy = (manage.ROOT / "rules/development.md").read_text()
        self.assertIn(
            "When asked to report skills, list every skill whose instructions were read and its distinct role; say if it yielded no actionable guidance.",
            policy,
        )

    def test_completion_verification_is_not_a_default_for_implementation(self):
        policy = (manage.ROOT / "rules/development.md").read_text()
        self.assertIn("only for a requested requirement-by-requirement acceptance audit of a deliverable", policy)
        self.assertIn(
            "A request to run a focused check, test scenarios, or validate skill routing uses the relevant domain/project checks.",
            policy,
        )
        self.assertIn(
            "Do not load it solely because tests/checks ran or a completion report is next; if no listed trigger applies, do not call it.",
            policy,
        )
        self.assertIn("For code review, use `requesting-code-review` under the triggers below", policy)
        self.assertIn(
            "Load `requesting-code-review` whenever asked to review source/code, even when framed as a security, UX, or other domain review",
            policy,
        )
        self.assertIn("do not also load completion verification solely to repeat its requirements/diff pass.", policy)

    def test_ui_review_route_requires_the_review_specialist(self):
        policy = (manage.ROOT / "rules/development.md").read_text()
        self.assertIn(
            "UI/accessibility review, even source-only: `web-design-guidelines`; no running page is required for source findings.",
            policy,
        )

    def test_browser_checks_fall_back_to_the_managed_playwright_path(self):
        policy = (manage.ROOT / "rules/development.md").read_text()
        self.assertIn(
            "if `playwright-cli` is unavailable, use the managed path in `docs/workflow.md`",
            policy,
        )

    def test_decision_interaction_and_review_boundaries_are_explicit(self):
        policy = (manage.ROOT / "rules/development.md").read_text()
        for phrase in (
            "Ask only for the earliest unresolved decision needed to unblock work.",
            "When decisions are sequential/conditional, request only the first required owner decision and wait; don't request later approvals in the same handoff.",
            "The closing request must name only that first owner decision; after the user replies, reassess any downstream approval.",
            "the final sentence must make a direct request addressed to the user",
            "A status or conditional next step is not a request.",
            "Never ask the user to decide in place of that authority; name the owner.",
            "Static or server-rendered output from initial props does not verify an event-driven transition.",
            "A helper/unit test does not verify the caller's component, hook, route, or integration lifecycle unless it exercises that boundary.",
            "A passing test supports only the boundary it executed; report higher untested behavior as code-reviewed but unverified.",
            "Load `requesting-code-review` whenever asked to review source/code",
            "Read it without delegation",
            "disclose that it was not independent",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, policy)

    def test_auth_and_tenant_fixes_always_trigger_the_review_skill(self):
        policy = (manage.ROOT / "rules/development.md").read_text()
        self.assertIn("any auth/authz, tenant-isolation", policy)
        self.assertIn("regardless of patch size", policy)
        self.assertIn("Creating, migrating, or reviewing a tenant boundary or its schema", policy)
        self.assertIn("Read it without delegation", policy)

    def test_requested_source_review_uses_review_and_domain_roles(self):
        policy = (manage.ROOT / "rules/development.md").read_text()
        self.assertIn(
            "it covers requirements, base/diff, callers/tests, and verdict",
            policy,
        )
        self.assertIn("Add the matching domain specialist for distinct analysis.", policy)

    def test_postgres_migration_reviews_use_the_postgres_specialist(self):
        policy = (manage.ROOT / "rules/development.md").read_text()
        self.assertIn("including read-only reviews of existing SQL, schemas, and migrations", policy)

    def test_blockers_pause_only_dependent_work(self):
        policy = (manage.ROOT / "rules/development.md").read_text()
        self.assertIn(
            "defer skills, edits, and tests for that slice unless a separate authorized review is requested.",
            policy,
        )
        self.assertIn("Before stopping, inspect remaining requested slices and execute every authorized one", policy)
        self.assertIn("including requested existing checks and required matched-skill reads.", policy)
        self.assertIn("stop only when no independent work remains.", policy)


class LicenseVerificationTests(unittest.TestCase):
    def test_prefers_an_upstream_license_file_when_present(self):
        source = {"license": "MIT", "license_file": None, "license_declaration_file": "README.md"}
        with tempfile.TemporaryDirectory() as temp:
            upstream = Path(temp)
            (upstream / "LICENSE").write_text("MIT License\n")
            (upstream / "README.md").write_text("# Skills\n\n## License\n\nApache-2.0\n")
            with contextlib.redirect_stdout(io.StringIO()) as output:
                manage.verify_source_license(upstream, "vercel-agent-skills", source)
            self.assertEqual(output.getvalue(), "")

    def test_accepts_explicit_upstream_mit_readme_without_creating_license_text(self):
        source = {"license": "MIT", "license_file": None, "license_declaration_file": "README.md"}
        with tempfile.TemporaryDirectory() as temp:
            upstream = Path(temp)
            (upstream / "README.md").write_text("# Skills\n\n## License\n\nMIT\n")
            with contextlib.redirect_stdout(io.StringIO()) as output:
                manage.verify_source_license(upstream, "vercel-agent-skills", source)
            self.assertIn("declares MIT in README.md", output.getvalue())
            self.assertFalse((upstream / "LICENSE").exists())

    def test_rejects_missing_or_ambiguous_readme_license_declaration(self):
        source = {"license": "MIT", "license_file": None, "license_declaration_file": "README.md"}
        with tempfile.TemporaryDirectory() as temp:
            upstream = Path(temp)
            (upstream / "README.md").write_text("# Skills\n\nMIT is a common license.\n")
            with self.assertRaisesRegex(ValueError, "explicit MIT license declaration"):
                manage.verify_source_license(upstream, "vercel-agent-skills", source)


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
            skill_text = (skill / "SKILL.md").read_text()
            self.assertIn(commit, skill_text)
            self.assertIn("Use whenever asked to review, audit, or assess an existing web page or UI for usability or accessibility.", skill_text)
            self.assertIn("MIT License", (skill / "LICENSE").read_text())
            self.assertNotIn("disable-model-invocation:", (skill / "SKILL.md").read_text())
            self.assertIn("allow_implicit_invocation: true", (skill / "agents/openai.yaml").read_text())


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
            self.assertEqual(updater, (upstream / "agents/doc-updater.md").read_text())
            self.assertIn("Original audit workflow.", (stage / "docs-governance/SKILL.md").read_text())
            self.assertEqual((stage / "docs-governance/scripts/audit-docs.py").read_bytes(),
                             (governance / "scripts/audit-docs.py").read_bytes())
            self.assertNotIn("disable-model-invocation:", updater)
            self.assertIn("allow_implicit_invocation: true", (stage / "doc-updater/agents/openai.yaml").read_text())
            self.assertEqual((stage / "docs-governance/SKILL.md").read_bytes(),
                             (governance / "SKILL.md").read_bytes())
            self.assertIn("allow_implicit_invocation: false", (stage / "docs-governance/agents/openai.yaml").read_text())


class SuperpowersWorkflowTests(unittest.TestCase):
    def test_full_inventory_uses_opt_in_workflow_without_bootstrap_hooks(self):
        manifest = manage.load(manage.ROOT / "manifest.json")
        source = manifest["sources"]["superpowers"]
        self.assertEqual(len(source["skills"]), 15)
        installed_names = manifest["local_skills"] + [
            name for item in manifest["sources"].values() for name in item["skills"]
        ]
        self.assertEqual(len(installed_names), len(set(installed_names)))
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
            self.assertEqual((workflow / "SKILL.md").read_bytes(),
                             (upstream / "skills/brainstorming/SKILL.md").read_bytes())
            self.assertIn("allow_implicit_invocation: false", (workflow / "agents/openai.yaml").read_text())
            self.assertIn("allow_implicit_invocation: true",
                          (stage / "systematic-debugging/agents/openai.yaml").read_text())
            self.assertEqual((workflow / "helper.md").read_text(), "Use superpowers:writing-plans.\n")
            self.assertFalse((stage / "hooks").exists())


class AnthropicSkillsTests(unittest.TestCase):
    def test_setup_preserves_the_complete_upstream_skill(self):
        manifest = manage.load(manage.ROOT / "manifest.json")
        source = manifest["sources"]["anthropic-skills"]
        self.assertEqual(source["skills"], ["mcp-builder", "frontend-design"])
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
            frontend = upstream / "skills/frontend-design"
            frontend.mkdir(parents=True)
            (frontend / "LICENSE.txt").write_text("Apache License\nVersion 2.0\n")
            (frontend / "SKILL.md").write_text("---\nname: frontend-design\ndescription: Design UI\n---\nOriginal design guidance.\n")
            stage = root / "stage"
            stage.mkdir()
            manifest = {"sources": {"anthropic-skills": source}, "local_skills": []}
            resolved = {"sources": {"anthropic-skills": {}}, "openspec": {}}
            with patch.object(manage, "fetch_source", return_value=upstream), patch.object(manage, "prepare_openspec"):
                manage.prepare(root, manifest, stage, resolved)
            self.assertEqual(manage.hashes(stage / "mcp-builder"), manage.hashes(skill))


class VersionTests(unittest.TestCase):
    def test_terminal_version_command_works_outside_repository(self):
        with tempfile.TemporaryDirectory() as temp:
            home = Path(temp)
            result = subprocess.run(
                [sys.executable, str(manage.ROOT / "setup/version_report.py"), "-v", "--home", temp],
                cwd=home, capture_output=True, text=True, check=True,
            )
            self.assertIn("Applied Codex policy: not configured", result.stdout)
            self.assertIn("No shared installation receipt.", result.stdout)
            self.assertEqual(list(home.iterdir()), [])

    def run_version(self, home):
        output = io.StringIO()
        with patch("sys.argv", ["manage.py", "version", "--home", str(home)]), contextlib.redirect_stdout(output):
            manage.main()
        return output.getvalue()

    def test_version_reports_package_host_markers_and_shared_receipt(self):
        with tempfile.TemporaryDirectory() as temp:
            home = Path(temp)
            for relative, version in ((".codex/AGENTS.md", "0.5.0"), (".claude/CLAUDE.md", "0.4.0")):
                path = home / relative
                path.parent.mkdir()
                path.write_text(f"{manage.BEGIN}\n<!-- grounded-version: {version} -->\n{manage.END}\n")
            receipt = home / ".local/share/skills-environment/installed.json"
            manage.write_json(receipt, {
                "resolved": {"sources": {"superpowers": {"version": "7.0.2", "commit": "a" * 40}}},
                "openspec": {"version": "2.1.0"},
            })
            output = self.run_version(home)
        self.assertIn("Package:", output)
        self.assertIn("Applied Codex policy: 0.5.0", output)
        self.assertIn("Applied Claude policy: 0.4.0", output)
        self.assertIn("Latest shared installation receipt:", output)
        self.assertIn("superpowers: 7.0.2", output)
        self.assertIn("openspec: 2.1.0", output)

    def test_version_works_before_setup_without_creating_files(self):
        with tempfile.TemporaryDirectory() as temp:
            home = Path(temp)
            output = self.run_version(home)
            self.assertEqual(list(home.iterdir()), [])
        self.assertIn("Applied Codex policy: not configured", output)
        self.assertIn("No shared installation receipt.", output)


if __name__ == "__main__":
    unittest.main()
