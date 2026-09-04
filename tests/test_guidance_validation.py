"""Regression tests for the repository-owned AI guidance validator."""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
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

    def test_rejects_template_missing_registered_repository_code(self) -> None:
        self.assert_template_rejects_missing_code("P4")

    def test_rejects_template_missing_p0_1_repository_code(self) -> None:
        self.assert_template_rejects_missing_code("P0-1")

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


if __name__ == "__main__":
    unittest.main()
