#!/usr/bin/env python3
"""Validate plugin skill structure without third-party Python dependencies."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


REQUIRED_SKILLS = {
    "tu-diagnosing-spring-backend-incidents",
    "tu-loading-device-inspection-cross-service-context",
    "tu-scaffolding-spring-feature-from-prototype",
}
SKILL_NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FRONTMATTER_PATTERN = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)
MARKDOWN_LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def read_quoted_yaml_value(text: str, key: str) -> str | None:
    match = re.search(rf"^\s*{re.escape(key)}:\s*(\"(?:[^\"\\]|\\.)*\")\s*$", text, re.MULTILINE)
    return json.loads(match.group(1)) if match else None


def validate_skill(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_name = skill_dir.name
    skill_file = skill_dir / "SKILL.md"
    ui_file = skill_dir / "agents" / "openai.yaml"

    if not skill_file.is_file():
        return [f"{skill_name}: missing SKILL.md"]
    if not ui_file.is_file():
        return [f"{skill_name}: missing agents/openai.yaml"]

    skill_text = skill_file.read_text(encoding="utf-8")
    ui_text = ui_file.read_text(encoding="utf-8")
    frontmatter_match = FRONTMATTER_PATTERN.match(skill_text)
    if not frontmatter_match:
        return [f"{skill_name}: invalid or missing YAML frontmatter"]

    frontmatter = frontmatter_match.group(1)
    fields = {}
    for line in frontmatter.splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            errors.append(f"{skill_name}: malformed frontmatter line: {line}")
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip()

    if set(fields) != {"name", "description"}:
        errors.append(f"{skill_name}: frontmatter must contain only name and description")
    if fields.get("name") != skill_name:
        errors.append(f"{skill_name}: frontmatter name does not match directory")
    if len(skill_name) > 64 or SKILL_NAME_PATTERN.fullmatch(skill_name) is None:
        errors.append(f"{skill_name}: name must be <=64 characters in hyphen-case")
    description = fields.get("description", "")
    if not description.startswith("Use when "):
        errors.append(f"{skill_name}: description must start with 'Use when '")
    if len(description) > 1024 or "<" in description or ">" in description:
        errors.append(f"{skill_name}: description must be <=1024 characters without angle brackets")
    if "TODO" in skill_text:
        errors.append(f"{skill_name}: SKILL.md contains TODO text")
    if len(skill_text.splitlines()) > 500:
        errors.append(f"{skill_name}: SKILL.md exceeds 500 lines")

    default_prompt = read_quoted_yaml_value(ui_text, "default_prompt")
    short_description = read_quoted_yaml_value(ui_text, "short_description")
    if default_prompt is None or f"${skill_name}" not in default_prompt:
        errors.append(f"{skill_name}: default_prompt must mention ${skill_name}")
    if short_description is None or not 25 <= len(short_description) <= 64:
        errors.append(f"{skill_name}: short_description must be 25-64 characters")

    linked_relative_files: set[Path] = set()
    for raw_target in MARKDOWN_LINK_PATTERN.findall(skill_text):
        target = raw_target.strip().strip("<>").split("#", 1)[0]
        if not target or target.startswith(("#", "/")) or "://" in target:
            continue
        resolved = (skill_dir / target).resolve()
        if not resolved.is_file():
            errors.append(f"{skill_name}: broken relative link: {raw_target}")
        else:
            linked_relative_files.add(resolved)

    references_dir = skill_dir / "references"
    if references_dir.is_dir():
        for reference_file in references_dir.glob("*.md"):
            if reference_file.resolve() not in linked_relative_files:
                errors.append(f"{skill_name}: unlinked reference: references/{reference_file.name}")

    return errors


def main() -> int:
    plugin_root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
    skills_root = plugin_root / "skills"
    actual_skills = {path.name for path in skills_root.iterdir() if path.is_dir()}
    errors = []

    missing = REQUIRED_SKILLS - actual_skills
    if missing:
        errors.append(f"missing required skills: {', '.join(sorted(missing))}")

    for skill_name in sorted(actual_skills):
        errors.extend(validate_skill(skills_root / skill_name))

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"validated {len(actual_skills)} plugin skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
