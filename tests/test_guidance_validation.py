"""Regression tests for the repository-owned AI guidance validator."""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
import re
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = REPOSITORY_ROOT / "scripts" / "validate_guidance.py"


class WorkspaceTemplateValidationTest(unittest.TestCase):
    """Verify that the committed workspace template remains a complete safe contract."""

    def copied_repository(self) -> Path:
        temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(temporary_directory.cleanup)
        repository = Path(temporary_directory.name) / "repo"
        shutil.copytree(
            REPOSITORY_ROOT,
            repository,
            ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc", "workspace.local.yaml"),
        )
        return repository

    def validate(self, repository: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(VALIDATOR), "--repo-root", str(repository)],
            capture_output=True,
            check=False,
            encoding="utf-8",
        )

    def assert_template_rejects_missing_code(self, code: str) -> None:
        repository = self.copied_repository()
        template = repository / "workspace.example.yaml"
        template.write_text(
            template.read_text(encoding="utf-8").replace(f"  - code: {code}\n", f"  # {code} mapping omitted\n"),
            encoding="utf-8",
        )

        result = self.validate(repository)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn(f"workspace.example.yaml is missing repository codes: {code}", result.stderr)

    def test_rejects_template_missing_primary_repository_code(self) -> None:
        self.assert_template_rejects_missing_code("P0")

    def test_rejects_template_missing_devkit_repository_code(self) -> None:
        self.assert_template_rejects_missing_code("P0-1")

    def test_rejects_registry_with_swapped_primary_repository_bindings(self) -> None:
        repository = self.copied_repository()
        registry = repository / "core" / "registry" / "repositories.yaml"
        registry.write_text(
            registry.read_text(encoding="utf-8").replace(
                "repository: tu-engineering-workbench",
                "repository: tu-devkit",
                1,
            ),
            encoding="utf-8",
        )

        result = self.validate(repository)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn(
            "repository registry has invalid primary binding: "
            "P0 -> tu-devkit; expected tu-engineering-workbench",
            result.stderr,
        )

    def test_rejects_template_missing_registered_knowledge_repository_code(self) -> None:
        self.assert_template_rejects_missing_code("K2")

    def test_rejects_template_missing_registered_language_learning_repository_code(self) -> None:
        self.assert_template_rejects_missing_code("K5")

    def test_rejects_template_missing_registered_ai_repository_code(self) -> None:
        self.assert_template_rejects_missing_code("A1")

    def test_rejects_template_missing_registered_architecture_learning_repository_code(self) -> None:
        self.assert_template_rejects_missing_code("L1")

    def test_rejects_template_missing_registered_open_source_skill_repository_code(self) -> None:
        self.assert_template_rejects_missing_code("S1")

    def test_rejects_template_with_duplicate_repository_code(self) -> None:
        repository = self.copied_repository()
        template = repository / "workspace.example.yaml"
        template.write_text(
            template.read_text(encoding="utf-8").replace("  - code: P4\n", "  - code: P1\n"),
            encoding="utf-8",
        )

        result = self.validate(repository)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("workspace.example.yaml has duplicate repository codes: P1", result.stderr)

    def test_rejects_local_workspace_with_unknown_code(self) -> None:
        repository = self.copied_repository()
        (repository / "workspace.local.yaml").write_text(
            "repositories:\n  - code: P999\n    path: " + str(repository) + "\n",
            encoding="utf-8",
        )

        result = self.validate(repository)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("workspace.local.yaml has unknown repository codes: P999", result.stderr)

    def test_rejects_workspace_template_with_unknown_code(self) -> None:
        repository = self.copied_repository()
        template = repository / "workspace.example.yaml"
        template.write_text(
            template.read_text(encoding="utf-8")
            + "  - code: P999\n    path: <set-local-p999-path>\n",
            encoding="utf-8",
        )

        result = self.validate(repository)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("workspace.example.yaml has unknown repository codes: P999", result.stderr)

    def test_rejects_registry_product_binding_not_in_platform(self) -> None:
        repository = self.copied_repository()
        registry = repository / "core" / "registry" / "repositories.yaml"
        registry.write_text(
            registry.read_text(encoding="utf-8").replace(
                "product: company/device-inspection-platform",
                "product: unknown/product",
                1,
            ),
            encoding="utf-8",
        )

        result = self.validate(repository)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn(
            "repository registry has unregistered product bindings: unknown/product",
            result.stderr,
        )

    def test_rejects_repository_manifest_with_unknown_repository(self) -> None:
        repository = self.copied_repository()
        manifest = repository / "products" / "company" / "device-inspection-platform" / "repositories" / "c-drone-inspection.yaml"
        manifest.write_text(
            manifest.read_text(encoding="utf-8").replace(
                "repository: c-drone-inspection",
                "repository: unknown-repository",
                1,
            ),
            encoding="utf-8",
        )

        result = self.validate(repository)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("repository manifest has unknown repository", result.stderr)
        self.assertIn("unknown-repository", result.stderr)

    def test_rejects_repository_manifest_with_mismatched_product_binding(self) -> None:
        repository = self.copied_repository()
        manifest = repository / "products" / "company" / "device-inspection-platform" / "repositories" / "c-drone-inspection.yaml"
        manifest.write_text(
            manifest.read_text(encoding="utf-8").replace(
                "product: company/device-inspection-platform",
                "product: personal/knowledge-hub",
                1,
            ),
            encoding="utf-8",
        )

        result = self.validate(repository)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("repository manifest has mismatched product binding", result.stderr)
        self.assertIn("personal/knowledge-hub", result.stderr)

    def test_rejects_template_with_concrete_repository_path(self) -> None:
        repository = self.copied_repository()
        template = repository / "workspace.example.yaml"
        template.write_text(
            template.read_text(encoding="utf-8").replace("<set-local-p1-path>", "D:/local/p1"),
            encoding="utf-8",
        )

        result = self.validate(repository)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("workspace.example.yaml has concrete repository path: D:/local/p1", result.stderr)

    def test_accepts_local_workspace_with_only_available_repositories(self) -> None:
        repository = self.copied_repository()
        local = repository / "workspace.local.yaml"
        local.write_text(
            "\n".join(
                [
                    "repositories:",
                    "  - code: P0-1",
                    f"    path: {repository}",
                    "  - code: P0",
                    f"    path: {repository}",
                    "  - code: K1",
                    f"    path: {repository}",
                    "  - code: K2",
                    f"    path: {repository}",
                    "",
                ]
            ),
            encoding="utf-8",
        )

        result = self.validate(repository)

        self.assertEqual(result.returncode, 0, result.stderr)

    def test_accepts_fresh_checkout_without_local_workspace(self) -> None:
        repository = self.copied_repository()

        result = self.validate(repository)

        self.assertEqual(result.returncode, 0, result.stderr)

    def test_rejects_broken_root_markdown_link(self) -> None:
        repository = self.copied_repository()
        (repository / "core" / "index.md").write_text(
            (repository / "core" / "index.md").read_text(encoding="utf-8")
            + "\n[broken](missing-file.md)\n",
            encoding="utf-8",
        )

        result = self.validate(repository)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("broken Markdown link", result.stderr)

    def test_rejects_unresolved_local_workspace_path(self) -> None:
        repository = self.copied_repository()
        (repository / "workspace.local.yaml").write_text(
            "repositories:\n  - code: P0-1\n    path: <unset>\n",
            encoding="utf-8",
        )

        result = self.validate(repository)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("workspace.local.yaml has unresolved path", result.stderr)


class FeatureDeliveryTaskPackageContractTest(unittest.TestCase):
    """Keep the documentation contract, creation template, and demo aligned without a YAML dependency."""

    def test_new_delivery_template_and_demo_have_metadata_v2_required_fields(self) -> None:
        required_fields = (
            "delivery_id",
            "title",
            "status",
            "repositories",
            "product",
            "created_at",
            "evidence",
            "knowledge_update_assessment",
        )
        metadata = (REPOSITORY_ROOT / "core" / "contracts" / "task-metadata.schema.yaml").read_text(
            encoding="utf-8"
        )
        template = (
            REPOSITORY_ROOT
            / "plugins"
            / "ai-guidance-workflows"
            / "skills"
            / "tu-deliver-feature"
            / "references"
            / "task-package.md"
        ).read_text(encoding="utf-8")
        demo = (
            REPOSITORY_ROOT
            / "docs"
            / "workflows"
            / "feature-delivery"
            / "examples"
            / "robotdog-fill-light"
            / "task.yaml"
        ).read_text(encoding="utf-8")

        for field in required_fields:
            self.assertRegex(metadata, re.compile(rf"^  {field}:", re.MULTILINE), field)
            self.assertRegex(template, re.compile(rf"^{field}:", re.MULTILINE), field)
            self.assertRegex(demo, re.compile(rf"^{field}:", re.MULTILINE), field)

    def test_delivery_id_is_canonical_and_new_template_declares_only_created_artifacts(self) -> None:
        template = (
            REPOSITORY_ROOT
            / "plugins"
            / "ai-guidance-workflows"
            / "skills"
            / "tu-deliver-feature"
            / "references"
            / "task-package.md"
        ).read_text(encoding="utf-8")
        demo = (
            REPOSITORY_ROOT
            / "docs"
            / "workflows"
            / "feature-delivery"
            / "examples"
            / "robotdog-fill-light"
            / "task.yaml"
        ).read_text(encoding="utf-8")
        template_yaml = re.search(r"```yaml\n(.*?)\n```", template, re.DOTALL)
        self.assertIsNotNone(template_yaml)
        self.assertIn("  impact: 01-impact-review.md", template_yaml.group(1))
        self.assertIn("  resume: resume.md", template_yaml.group(1))
        self.assertNotIn("  contract:", template_yaml.group(1))
        self.assertNotIn("  openapi:", template_yaml.group(1))
        self.assertNotIn("  backlog:", template_yaml.group(1))
        self.assertNotIn("  integration:", template_yaml.group(1))
        delivery_id = re.search(r"^delivery_id: (.+)$", demo, re.MULTILINE)
        self.assertIsNotNone(delivery_id)
        self.assertRegex(delivery_id.group(1), r"^DF-\d{8}-\d{2}$")


class FeatureDeliveryPackageGuardrailTest(unittest.TestCase):
    """Verify lightweight on-disk Feature Delivery package guardrails."""

    def copied_repository(self) -> Path:
        temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(temporary_directory.cleanup)
        repository = Path(temporary_directory.name) / "repo"
        shutil.copytree(
            REPOSITORY_ROOT,
            repository,
            ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc", "workspace.local.yaml"),
        )
        return repository

    def validate(self, repository: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(VALIDATOR), "--repo-root", str(repository)],
            capture_output=True,
            check=False,
            encoding="utf-8",
        )

    def create_package(
        self,
        repository: Path,
        state: str,
        directory_name: str,
        delivery_id: str,
        status: str,
        archived_at: str | None = None,
        create_artifact: bool = True,
    ) -> None:
        package = (
            repository
            / "work"
            / "company"
            / "device-inspection-platform"
            / "tasks"
            / state
            / directory_name
        )
        package.mkdir(parents=True)
        archived_line = f"archived_at: {archived_at}\n" if archived_at is not None else ""
        package.joinpath("task.yaml").write_text(
            "\n".join(
                [
                    f"delivery_id: {delivery_id}",
                    "title: Guardrail fixture",
                    f"status: {status}",
                    "artifacts:",
                    "  impact: 01-impact-review.md",
                    archived_line.rstrip(),
                    "",
                ]
            ),
            encoding="utf-8",
        )
        if create_artifact:
            package.joinpath("01-impact-review.md").write_text("fixture\n", encoding="utf-8")

    def test_accepts_valid_active_and_archived_packages(self) -> None:
        repository = self.copied_repository()
        self.create_package(
            repository, "active", "DF-20260906-01-fill-light", "DF-20260906-01", "active"
        )
        self.create_package(
            repository,
            "archive",
            "DF-20260904-01-fill-light",
            "DF-20260904-01",
            "completed",
            "2026-09-05T12:00:00+08:00",
        )

        result = self.validate(repository)

        self.assertEqual(result.returncode, 0, result.stderr)

    def test_rejects_invalid_delivery_id(self) -> None:
        repository = self.copied_repository()
        self.create_package(
            repository, "active", "DF-20260905-01-fill-light", "DF-20260905-1", "active"
        )

        result = self.validate(repository)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Feature Delivery task.yaml has invalid delivery_id", result.stderr)

    def test_rejects_active_package_with_archived_at(self) -> None:
        repository = self.copied_repository()
        self.create_package(
            repository,
            "active",
            "DF-20260905-01-fill-light",
            "DF-20260905-01",
            "active",
            "2026-09-05T12:00:00+08:00",
        )

        result = self.validate(repository)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("active Feature Delivery package must not declare archived_at", result.stderr)

    def test_rejects_archived_package_without_archived_at(self) -> None:
        repository = self.copied_repository()
        self.create_package(
            repository, "archive", "DF-20260905-01-fill-light", "DF-20260905-01", "completed"
        )

        result = self.validate(repository)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("archived Feature Delivery package must declare archived_at", result.stderr)

    def test_rejects_missing_declared_artifact(self) -> None:
        repository = self.copied_repository()
        self.create_package(
            repository,
            "active",
            "DF-20260905-01-fill-light",
            "DF-20260905-01",
            "active",
            create_artifact=False,
        )

        result = self.validate(repository)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Feature Delivery artifact is missing", result.stderr)

    def test_rejects_flat_active_legacy_files(self) -> None:
        repository = self.copied_repository()
        active = (
            repository
            / "work"
            / "company"
            / "device-inspection-platform"
            / "tasks"
            / "active"
        )
        active.mkdir(parents=True)
        active.joinpath("p0-legacy-task.yaml").write_text("legacy: state\n", encoding="utf-8")
        active.joinpath("legacy-note.md").write_text("legacy state\n", encoding="utf-8")

        result = self.validate(repository)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("active Feature Delivery tasks must contain only DF package directories", result.stderr)
        self.assertIn("p0-legacy-task.yaml", result.stderr)
        self.assertIn("legacy-note.md", result.stderr)

    def test_accepts_flat_pre_v1_archive_evidence(self) -> None:
        repository = self.copied_repository()
        archive = (
            repository
            / "work"
            / "company"
            / "device-inspection-platform"
            / "tasks"
            / "archive"
        )
        archive.mkdir(parents=True, exist_ok=True)
        archive.joinpath("p1-pre-v1-task.yaml").write_text("legacy: evidence\n", encoding="utf-8")

        result = self.validate(repository)

        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
