"""Regression tests for the repository-owned AI guidance validator."""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = REPOSITORY_ROOT / "ai-guidance" / "scripts" / "validate_guidance.py"


class WorkspaceTemplateValidationTest(unittest.TestCase):
    """Verify that the committed workspace template remains a complete safe contract."""

    def copied_repository(self) -> Path:
        temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(temporary_directory.cleanup)
        repository = Path(temporary_directory.name) / "repo"
        repository.mkdir()
        shutil.copy2(REPOSITORY_ROOT / "AGENTS.md", repository / "AGENTS.md")
        shutil.copy2(REPOSITORY_ROOT / ".gitignore", repository / ".gitignore")
        shutil.copytree(
            REPOSITORY_ROOT / "ai-guidance",
            repository / "ai-guidance",
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
        )
        return repository

    def validate(self, repository: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(VALIDATOR), "--repo-root", str(repository)],
            capture_output=True,
            check=False,
            encoding="utf-8",
        )

    def test_rejects_template_missing_registered_repository_code(self) -> None:
        repository = self.copied_repository()
        template = repository / "ai-guidance" / "workspace.example.yaml"
        template.write_text(
            template.read_text(encoding="utf-8").replace("  - code: P4\n", "  # P4 mapping omitted\n"),
            encoding="utf-8",
        )

        result = self.validate(repository)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("workspace.example.yaml is missing repository codes: P4", result.stderr)

    def test_rejects_template_missing_registered_knowledge_repository_code(self) -> None:
        repository = self.copied_repository()
        template = repository / "ai-guidance" / "workspace.example.yaml"
        template.write_text(
            template.read_text(encoding="utf-8").replace("  - code: K2\n", "  # K2 mapping omitted\n"),
            encoding="utf-8",
        )

        result = self.validate(repository)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("workspace.example.yaml is missing repository codes: K2", result.stderr)

    def test_rejects_template_missing_registered_language_learning_repository_code(self) -> None:
        repository = self.copied_repository()
        template = repository / "ai-guidance" / "workspace.example.yaml"
        template.write_text(
            template.read_text(encoding="utf-8").replace("  - code: K5\n", "  # K5 mapping omitted\n"),
            encoding="utf-8",
        )

        result = self.validate(repository)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("workspace.example.yaml is missing repository codes: K5", result.stderr)

    def test_rejects_template_missing_registered_ai_repository_code(self) -> None:
        repository = self.copied_repository()
        template = repository / "ai-guidance" / "workspace.example.yaml"
        template.write_text(
            template.read_text(encoding="utf-8").replace("  - code: A1\n", "  # A1 mapping omitted\n"),
            encoding="utf-8",
        )

        result = self.validate(repository)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("workspace.example.yaml is missing repository codes: A1", result.stderr)

    def test_rejects_template_missing_registered_architecture_learning_repository_code(self) -> None:
        repository = self.copied_repository()
        template = repository / "ai-guidance" / "workspace.example.yaml"
        template.write_text(
            template.read_text(encoding="utf-8").replace("  - code: L1\n", "  # L1 mapping omitted\n"),
            encoding="utf-8",
        )

        result = self.validate(repository)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("workspace.example.yaml is missing repository codes: L1", result.stderr)

    def test_rejects_template_missing_registered_open_source_skill_repository_code(self) -> None:
        repository = self.copied_repository()
        template = repository / "ai-guidance" / "workspace.example.yaml"
        template.write_text(
            template.read_text(encoding="utf-8").replace("  - code: S1\n", "  # S1 mapping omitted\n"),
            encoding="utf-8",
        )

        result = self.validate(repository)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("workspace.example.yaml is missing repository codes: S1", result.stderr)

    def test_rejects_template_with_duplicate_repository_code(self) -> None:
        repository = self.copied_repository()
        template = repository / "ai-guidance" / "workspace.example.yaml"
        template.write_text(
            template.read_text(encoding="utf-8").replace("  - code: P4\n", "  - code: P1\n"),
            encoding="utf-8",
        )

        result = self.validate(repository)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("workspace.example.yaml has duplicate repository codes: P1", result.stderr)

    def test_rejects_template_with_concrete_repository_path(self) -> None:
        repository = self.copied_repository()
        template = repository / "ai-guidance" / "workspace.example.yaml"
        template.write_text(
            template.read_text(encoding="utf-8").replace("<set-local-p1-path>", "D:/local/p1"),
            encoding="utf-8",
        )

        result = self.validate(repository)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("workspace.example.yaml has concrete repository path: D:/local/p1", result.stderr)

    def test_accepts_local_workspace_with_only_available_repositories(self) -> None:
        repository = self.copied_repository()
        local = repository / "ai-guidance" / "workspace.local.yaml"
        local.write_text(
            "\n".join(
                [
                    "repositories:",
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


if __name__ == "__main__":
    unittest.main()
