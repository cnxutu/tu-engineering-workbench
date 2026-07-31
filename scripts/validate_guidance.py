#!/usr/bin/env python3
"""Validate the repository-owned AI guidance contract without third-party packages."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)#]+)(?:#[^)]*)?\)")
PATH_PATTERN = re.compile(
    r"^\s*(?:-\s+)?(?P<key>manifest|index|entry|product_manifest|product_index):\s*(?P<value>\S.*)\s*$",
    re.MULTILINE,
)
SENSITIVE_KEY_PATTERN = re.compile(
    r"^\s*[^#\n]*?(?:password|secret|token|api[_-]?key|private[_-]?key)\s*:\s*(?P<value>.+)$",
    re.IGNORECASE | re.MULTILINE,
)
PLACEHOLDER_PATTERN = re.compile(r"^(?:<[^>]+>|\$\{[^}]+\}|redacted)$", re.IGNORECASE)
REGISTERED_REPOSITORY_CODES = {"P0", "P1", "P2", "P3", "P4"}


def error_if_missing(path: Path, label: str, errors: list[str]) -> None:
    if not path.is_file():
        errors.append(f"missing {label}: {path}")


def validate_markdown_links(repo_root: Path, errors: list[str]) -> None:
    files = [repo_root / "AGENTS.md"]
    files.extend((repo_root / "ai-guidance").rglob("*.md"))
    for source in files:
        if not source.is_file():
            continue
        for match in LINK_PATTERN.finditer(source.read_text(encoding="utf-8")):
            target = match.group(1).strip()
            if target.startswith(("http:", "https:", "mailto:")):
                continue
            if not (source.parent / target).resolve().exists():
                errors.append(f"broken Markdown link: {source.relative_to(repo_root)} -> {target}")


def values_for_keys(path: Path, allowed: set[str]) -> list[tuple[str, str]]:
    values: list[tuple[str, str]] = []
    for match in PATH_PATTERN.finditer(path.read_text(encoding="utf-8")):
        key = match.group("key")
        if key in allowed:
            values.append((key, match.group("value").strip().strip("\\\"'")))
    return values


def validate_product_bindings(guidance_root: Path, errors: list[str]) -> None:
    platform = guidance_root / "platform.yaml"
    for key, value in values_for_keys(platform, {"manifest", "index"}):
        error_if_missing(guidance_root / value, f"platform {key}", errors)

    for manifest in guidance_root.glob("products/**/product.yaml"):
        for key, value in values_for_keys(manifest, {"entry"}):
            error_if_missing(manifest.parent / value, f"product {key}", errors)
        repository_values = re.findall(
            r"^\s*-\s+(repositories/[^\s#]+\.yaml)\s*$",
            manifest.read_text(encoding="utf-8"),
            re.MULTILINE,
        )
        for value in repository_values:
            error_if_missing(manifest.parent / value, "repository manifest", errors)

    for manifest in guidance_root.glob("products/**/repositories/*.yaml"):
        for key, value in values_for_keys(manifest, {"product_manifest", "product_index"}):
            error_if_missing(manifest.parent / value, f"repository {key}", errors)


def validate_workspace_configuration(repo_root: Path, errors: list[str]) -> None:
    guidance_root = repo_root / "ai-guidance"
    error_if_missing(guidance_root / "workspace.example.yaml", "workspace template", errors)
    ignore_file = repo_root / ".gitignore"
    if "ai-guidance/workspace.local.yaml" not in ignore_file.read_text(encoding="utf-8"):
        errors.append("workspace.local.yaml is not ignored")

    local = guidance_root / "workspace.local.yaml"
    if not local.is_file():
        return
    text = local.read_text(encoding="utf-8")
    codes = set(re.findall(r"^\s*-\s+code:\s*(P[0-4])\s*$", text, re.MULTILINE))
    missing_codes = sorted({"P0", "P1", "P2", "P3", "P4"} - codes)
    if missing_codes:
        errors.append(f"workspace.local.yaml is missing repository codes: {', '.join(missing_codes)}")
    for raw_path in re.findall(r"^\s+path:\s*(\S.*)\s*$", text, re.MULTILINE):
        value = raw_path.strip().strip("\\\"'")
        if PLACEHOLDER_PATTERN.match(value):
            errors.append(f"workspace.local.yaml has unresolved path: {value}")
        elif not Path(value).is_dir():
            errors.append(f"workspace.local.yaml path does not exist: {value}")


def validate_workspace_template(repo_root: Path, errors: list[str]) -> None:
    template = repo_root / "ai-guidance" / "workspace.example.yaml"
    if not template.is_file():
        return
    text = template.read_text(encoding="utf-8")
    codes = re.findall(r"^\s*-\s+code:\s*(P[0-4])\s*$", text, re.MULTILINE)
    missing_codes = sorted(REGISTERED_REPOSITORY_CODES - set(codes))
    if missing_codes:
        errors.append(f"workspace.example.yaml is missing repository codes: {', '.join(missing_codes)}")
    duplicate_codes = sorted({code for code in codes if codes.count(code) > 1})
    if duplicate_codes:
        errors.append(f"workspace.example.yaml has duplicate repository codes: {', '.join(duplicate_codes)}")
    for raw_path in re.findall(r"^\s+path:\s*(\S.*)\s*$", text, re.MULTILINE):
        value = raw_path.strip().strip("\\\"'")
        if not PLACEHOLDER_PATTERN.match(value):
            errors.append(f"workspace.example.yaml has concrete repository path: {value}")


def validate_sensitive_values(guidance_root: Path, errors: list[str]) -> None:
    for path in guidance_root.rglob("*.yaml"):
        if path.name.endswith("schema.yaml"):
            continue
        for match in SENSITIVE_KEY_PATTERN.finditer(path.read_text(encoding="utf-8")):
            value = match.group("value").strip().strip("\\\"'")
            if value and not PLACEHOLDER_PATTERN.match(value):
                errors.append(f"possible sensitive value in {path.relative_to(guidance_root)}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[2])
    repo_root = parser.parse_args().repo_root.resolve()
    guidance_root = repo_root / "ai-guidance"
    errors: list[str] = []

    error_if_missing(repo_root / "AGENTS.md", "repository AGENTS.md", errors)
    error_if_missing(guidance_root / "AGENTS.md", "guidance AGENTS.md", errors)
    error_if_missing(guidance_root / "platform.yaml", "platform manifest", errors)
    validate_markdown_links(repo_root, errors)
    validate_product_bindings(guidance_root, errors)
    validate_workspace_configuration(repo_root, errors)
    validate_workspace_template(repo_root, errors)
    validate_sensitive_values(guidance_root, errors)

    if errors:
        print("AI guidance validation failed:", file=sys.stderr)
        print("\n".join(f"- {error}" for error in errors), file=sys.stderr)
        return 1
    print("AI guidance validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
