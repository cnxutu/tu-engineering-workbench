#!/usr/bin/env python3
"""Validate the repository-owned AI guidance contract without third-party packages."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path, PurePosixPath, PureWindowsPath


LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)#]+)(?:#[^)]*)?\)")
PATH_PATTERN = re.compile(
    r"^\s*(?:-\s+)?(?P<key>manifest|index|entry|product_manifest|product_index|repository_registry|repository|product):\s*(?P<value>\S.*)\s*$",
    re.MULTILINE,
)
SENSITIVE_KEY_PATTERN = re.compile(
    r"^\s*[^#\n]*?(?:password|secret|token|api[_-]?key|private[_-]?key)\s*:\s*(?P<value>.+)$",
    re.IGNORECASE | re.MULTILINE,
)
PLACEHOLDER_PATTERN = re.compile(r"^(?:<[^>]+>|\$\{[^}]+\}|redacted)$", re.IGNORECASE)
REPOSITORY_REGISTRY = Path("core/registry/repositories.yaml")
PRIMARY_REPOSITORY_BINDINGS = {
    "P0": "tu-engineering-workbench",
    "P0-1": "tu-devkit",
}
DELIVERY_ID_PATTERN = re.compile(r"^DF-\d{8}-\d{2}$")
DELIVERY_DIRECTORY_PATTERN = re.compile(r"^(DF-\d{8}-\d{2})(?:-.+)?$")
CLOSED_DELIVERY_INDEX_PATTERN = re.compile(r"^DF-\d{8}-\d{2}\.md$")
CLOSED_DELIVERY_STATUSES = {"completed", "blocked", "superseded"}


def error_if_missing(path: Path, label: str, errors: list[str]) -> None:
    if not path.is_file():
        errors.append(f"missing {label}: {path}")


def validate_markdown_links(repo_root: Path, errors: list[str]) -> None:
    files = [repo_root / "AGENTS.md"]
    files.extend(path for path in repo_root.rglob("*.md") if ".git" not in path.parts)
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


def workspace_codes(text: str) -> list[str]:
    return re.findall(r"^\s*-\s+code:\s*(\S.*?)\s*$", text, re.MULTILINE)


def external_tu_vault_values(text: str) -> dict[str, str] | None:
    """Read the optional simple external_contexts.tu_vault mapping without YAML dependencies."""
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.strip() != "external_contexts:":
            continue
        for vault_index in range(index + 1, len(lines)):
            candidate = lines[vault_index]
            if candidate and not candidate.startswith((" ", "\t")):
                break
            if re.fullmatch(r"\s+tu_vault:\s*", candidate) is None:
                continue
            values: dict[str, str] = {}
            vault_indent = len(candidate) - len(candidate.lstrip())
            for child in lines[vault_index + 1 :]:
                if not child.strip():
                    continue
                child_indent = len(child) - len(child.lstrip())
                if child_indent <= vault_indent:
                    break
                match = re.match(r"\s+(path|delivery_archive_root):\s*(\S.*?)\s*$", child)
                if match is not None:
                    values[match.group(1)] = match.group(2).strip().strip("\\\"'")
            return values
    return None


def is_safe_relative_path(value: str) -> bool:
    normalized = value.replace("\\", "/")
    posix_path = PurePosixPath(normalized)
    windows_path = PureWindowsPath(value)
    return (
        bool(value)
        and not posix_path.is_absolute()
        and not windows_path.is_absolute()
        and not windows_path.drive
        and ".." not in posix_path.parts
    )


def deterministic_archive_reference(delivery_archive_root: str, delivery_id: str) -> str:
    """Return the sole logical Vault reference for one configured Delivery archive."""
    if not is_safe_relative_path(delivery_archive_root):
        raise ValueError("delivery_archive_root must be a safe relative path")
    if DELIVERY_ID_PATTERN.fullmatch(delivery_id) is None:
        raise ValueError("delivery_id must use DF-YYYYMMDD-NN")
    parts = [part for part in PurePosixPath(delivery_archive_root.replace("\\", "/")).parts if part != "."]
    return "tu-vault:" + "/".join([*parts, delivery_id])


def path_is_descendant(path: Path, ancestor: Path) -> bool:
    try:
        path.relative_to(ancestor)
    except ValueError:
        return False
    return True


def platform_product_ids(repo_root: Path) -> set[str]:
    platform = repo_root / "platform.yaml"
    if not platform.is_file():
        return set()
    return set(re.findall(r"^  - id:\s*(\S.*?)\s*$", platform.read_text(encoding="utf-8"), re.MULTILINE))


def registered_repositories(
    repo_root: Path, platform_products: set[str], errors: list[str]
) -> tuple[dict[str, str], dict[str, str | None]]:
    registry = repo_root / REPOSITORY_REGISTRY
    error_if_missing(registry, "repository registry", errors)
    if not registry.is_file():
        return {}, {}
    registry_text = registry.read_text(encoding="utf-8")
    entries = re.findall(
        r"^  - code:\s*(?P<code>\S+)\s*$\n^    repository:\s*(?P<repository>\S.*?)\s*$(?:\n^    product:\s*(?P<product>\S.*?)\s*$)?",
        registry_text,
        re.MULTILINE,
    )
    codes = [code for code, _, _ in entries]
    duplicate_codes = sorted({code for code in codes if codes.count(code) > 1})
    if duplicate_codes:
        errors.append(f"repository registry has duplicate codes: {', '.join(duplicate_codes)}")
    bindings = {code: repository for code, repository, _ in entries}
    repository_products = {repository: product or None for _, repository, product in entries}
    for code, expected_repository in PRIMARY_REPOSITORY_BINDINGS.items():
        actual_repository = bindings.get(code)
        if actual_repository != expected_repository:
            errors.append(
                "repository registry has invalid primary binding: "
                f"{code} -> {actual_repository or '<missing>'}; expected {expected_repository}"
            )
    unknown_products = sorted(
        set(re.findall(r"^    product:\s*(\S.*?)\s*$", registry_text, re.MULTILINE))
        - platform_products
    )
    if unknown_products:
        errors.append(
            "repository registry has unregistered product bindings: "
            f"{', '.join(unknown_products)}"
        )
    return bindings, repository_products


def validate_product_bindings(repo_root: Path, errors: list[str]) -> None:
    platform = repo_root / "platform.yaml"
    for key, value in values_for_keys(platform, {"manifest", "index", "repository_registry"}):
        error_if_missing(repo_root / value, f"platform {key}", errors)

    for manifest in repo_root.glob("products/**/product.yaml"):
        for key, value in values_for_keys(manifest, {"entry"}):
            error_if_missing(manifest.parent / value, f"product {key}", errors)
        repository_values = re.findall(
            r"^\s*-\s+(repositories/[^\s#]+\.yaml)\s*$",
            manifest.read_text(encoding="utf-8"),
            re.MULTILINE,
        )
        for value in repository_values:
            error_if_missing(manifest.parent / value, "repository manifest", errors)

    for manifest in repo_root.glob("products/**/repositories/*.yaml"):
        for key, value in values_for_keys(manifest, {"product_manifest", "product_index"}):
            error_if_missing(manifest.parent / value, f"repository {key}", errors)


def validate_repository_manifest_bindings(
    repo_root: Path, repository_products: dict[str, str | None], errors: list[str]
) -> None:
    for manifest in repo_root.glob("products/**/repositories/*.yaml"):
        declared = dict(values_for_keys(manifest, {"repository", "product"}))
        repository = declared.get("repository")
        if repository is None:
            continue
        registry_product = repository_products.get(repository)
        if repository not in repository_products:
            errors.append(
                "repository manifest has unknown repository: "
                f"{manifest.relative_to(repo_root)} -> {repository}"
            )
            continue
        product = declared.get("product")
        if product is not None and product != registry_product:
            errors.append(
                "repository manifest has mismatched product binding: "
                f"{manifest.relative_to(repo_root)} -> {product}; registry has {registry_product or '<none>'}"
            )


def validate_workspace_configuration(repo_root: Path, registered_codes: set[str], errors: list[str]) -> None:
    error_if_missing(repo_root / "workspace.example.yaml", "workspace template", errors)
    ignore_file = repo_root / ".gitignore"
    if "workspace.local.yaml" not in ignore_file.read_text(encoding="utf-8"):
        errors.append("workspace.local.yaml is not ignored")

    local = repo_root / "workspace.local.yaml"
    if not local.is_file():
        return
    text = local.read_text(encoding="utf-8")
    codes = workspace_codes(text)
    unknown_codes = sorted(set(codes) - registered_codes)
    if unknown_codes:
        errors.append(f"workspace.local.yaml has unknown repository codes: {', '.join(unknown_codes)}")
    duplicate_codes = sorted({code for code in codes if codes.count(code) > 1})
    if duplicate_codes:
        errors.append(f"workspace.local.yaml has duplicate repository codes: {', '.join(duplicate_codes)}")
    for raw_path in re.findall(r"^\s+path:\s*(\S.*)\s*$", text, re.MULTILINE):
        value = raw_path.strip().strip("\\\"'")
        if PLACEHOLDER_PATTERN.match(value):
            errors.append(f"workspace.local.yaml has unresolved path: {value}")
        elif not Path(value).is_dir():
            errors.append(f"workspace.local.yaml path does not exist: {value}")
    tu_vault = external_tu_vault_values(text)
    if tu_vault is None:
        return
    vault_path = tu_vault.get("path")
    archive_root = tu_vault.get("delivery_archive_root")
    if vault_path is None or archive_root is None:
        errors.append("workspace.local.yaml tu_vault requires path and delivery_archive_root")
        return
    if PLACEHOLDER_PATTERN.match(vault_path) or not Path(vault_path).is_absolute():
        errors.append("workspace.local.yaml tu_vault path must be an absolute configured directory")
    elif not Path(vault_path).is_dir():
        errors.append(f"workspace.local.yaml tu_vault path does not exist: {vault_path}")
    else:
        resolved_vault = Path(vault_path).resolve()
        if resolved_vault == repo_root:
            errors.append("workspace.local.yaml tu_vault path must not be the Workbench itself")
        elif path_is_descendant(resolved_vault, repo_root) or path_is_descendant(repo_root, resolved_vault):
            errors.append(
                "workspace.local.yaml tu_vault path must be a separate directory tree from Workbench"
            )
    if PLACEHOLDER_PATTERN.match(archive_root) or not is_safe_relative_path(archive_root):
        errors.append("workspace.local.yaml tu_vault delivery_archive_root must be a safe relative path")


def validate_workspace_template(repo_root: Path, registered_codes: set[str], errors: list[str]) -> None:
    template = repo_root / "workspace.example.yaml"
    if not template.is_file():
        return
    text = template.read_text(encoding="utf-8")
    codes = workspace_codes(text)
    missing_codes = sorted(registered_codes - set(codes))
    if missing_codes:
        errors.append(f"workspace.example.yaml is missing repository codes: {', '.join(missing_codes)}")
    duplicate_codes = sorted({code for code in codes if codes.count(code) > 1})
    if duplicate_codes:
        errors.append(f"workspace.example.yaml has duplicate repository codes: {', '.join(duplicate_codes)}")
    unknown_codes = sorted(set(codes) - registered_codes)
    if unknown_codes:
        errors.append(f"workspace.example.yaml has unknown repository codes: {', '.join(unknown_codes)}")
    for raw_path in re.findall(r"^\s+path:\s*(\S.*)\s*$", text, re.MULTILINE):
        value = raw_path.strip().strip("\\\"'")
        if not PLACEHOLDER_PATTERN.match(value):
            errors.append(f"workspace.example.yaml has concrete repository path: {value}")
    tu_vault = external_tu_vault_values(text)
    if tu_vault is None:
        errors.append("workspace.example.yaml is missing optional tu_vault external context template")
        return
    vault_path = tu_vault.get("path")
    archive_root = tu_vault.get("delivery_archive_root")
    if vault_path is None or not PLACEHOLDER_PATTERN.match(vault_path):
        errors.append("workspace.example.yaml tu_vault path must be a placeholder")
    if archive_root is None or not PLACEHOLDER_PATTERN.match(archive_root):
        errors.append("workspace.example.yaml tu_vault delivery_archive_root must be a placeholder")


def validate_sensitive_values(repo_root: Path, errors: list[str]) -> None:
    for path in repo_root.rglob("*.yaml"):
        if ".git" in path.parts:
            continue
        if path.name.endswith("schema.yaml"):
            continue
        for match in SENSITIVE_KEY_PATTERN.finditer(path.read_text(encoding="utf-8")):
            value = match.group("value").strip().strip("\\\"'")
            if value and not PLACEHOLDER_PATTERN.match(value):
                errors.append(f"possible sensitive value in {path.relative_to(repo_root)}")


def yaml_scalar(text: str, key: str) -> str | None:
    match = re.search(rf"^{re.escape(key)}:\s*(\S.*?)\s*$", text, re.MULTILINE)
    if match is None:
        return None
    return match.group(1).strip().strip("\\\"'")


def yaml_map_values(text: str, key: str) -> list[str]:
    lines = text.splitlines()
    values: list[str] = []
    for index, line in enumerate(lines):
        if re.fullmatch(rf"{re.escape(key)}:\s*", line) is None:
            continue
        for child in lines[index + 1 :]:
            if not child.strip():
                continue
            if not child.startswith((" ", "\t")):
                break
            match = re.match(r"^\s+[^:#][^:]*:\s*(\S.*?)\s*$", child)
            if match is not None:
                values.append(match.group(1).strip().strip("\\\"'"))
        break
    return values


def validate_feature_delivery_packages(repo_root: Path, errors: list[str]) -> None:
    for state in ("active", "archive"):
        task_roots = list(repo_root.glob(f"work/**/tasks/{state}"))
        current_active_root = repo_root / "work" / "active"
        if state == "active" and current_active_root.is_dir():
            task_roots.append(current_active_root)
        for task_root in task_roots:
            candidates = task_root.rglob("DF-*") if task_root == current_active_root else task_root.glob("DF-*")
            for candidate in candidates:
                if not candidate.is_dir():
                    errors.append(
                        "Feature Delivery package must be a directory: "
                        f"{candidate.relative_to(repo_root)}"
                    )
                    continue
                directory_match = DELIVERY_DIRECTORY_PATTERN.fullmatch(candidate.name)
                if directory_match is None:
                    errors.append(
                        "Feature Delivery package directory has invalid canonical ID: "
                        f"{candidate.relative_to(repo_root)}"
                    )
                    continue
                task_file = candidate / "task.yaml"
                if not task_file.is_file():
                    errors.append(
                        "Feature Delivery package is missing task.yaml: "
                        f"{candidate.relative_to(repo_root)}"
                    )
                    continue
                task_text = task_file.read_text(encoding="utf-8")
                delivery_id = yaml_scalar(task_text, "delivery_id")
                if delivery_id is None or DELIVERY_ID_PATTERN.fullmatch(delivery_id) is None:
                    errors.append(
                        "Feature Delivery task.yaml has invalid delivery_id: "
                        f"{task_file.relative_to(repo_root)}"
                    )
                elif delivery_id != directory_match.group(1):
                    errors.append(
                        "Feature Delivery delivery_id does not match package directory: "
                        f"{task_file.relative_to(repo_root)}"
                    )
                status = yaml_scalar(task_text, "status")
                archived_at = yaml_scalar(task_text, "archived_at")
                if state == "active":
                    for key in ("capabilities", "related_deliveries"):
                        if re.search(rf"^{key}:", task_text, re.MULTILINE) is None:
                            errors.append(
                                f"active Feature Delivery package is missing {key}: "
                                f"{task_file.relative_to(repo_root)}"
                            )
                    if status != "active":
                        errors.append(
                            "active Feature Delivery package must have status: active: "
                            f"{task_file.relative_to(repo_root)}"
                        )
                    for key in ("archived_at", "archive_reference", "closed_index"):
                        if yaml_scalar(task_text, key) is not None:
                            errors.append(
                                f"active Feature Delivery package must not declare {key}: "
                                f"{task_file.relative_to(repo_root)}"
                            )
                else:
                    if status == "active":
                        errors.append(
                            "archived Feature Delivery package must not have status: active: "
                            f"{task_file.relative_to(repo_root)}"
                        )
                    if archived_at is None:
                        errors.append(
                            "archived Feature Delivery package must declare archived_at: "
                            f"{task_file.relative_to(repo_root)}"
                        )
                for artifact in yaml_map_values(task_text, "artifacts"):
                    if not (candidate / artifact).exists():
                        errors.append(
                            "Feature Delivery artifact is missing: "
                            f"{task_file.relative_to(repo_root)} -> {artifact}"
                        )

            if state == "active":
                candidates = task_root.rglob("*") if task_root == current_active_root else task_root.iterdir()
                for candidate in candidates:
                    relative_parts = candidate.relative_to(task_root).parts
                    inside_package = any(part.startswith("DF-") for part in relative_parts[:-1])
                    if (
                        task_root != current_active_root
                        and (not candidate.is_dir() or not candidate.name.startswith("DF-"))
                    ):
                        errors.append(
                            "active Feature Delivery tasks must contain only DF package directories: "
                            f"{candidate.relative_to(repo_root)}"
                        )
                    elif not candidate.is_dir() and not inside_package:
                        errors.append(
                            "active Feature Delivery tasks must contain only DF package directories: "
                            f"{candidate.relative_to(repo_root)}"
                        )
                    elif (
                        candidate.is_dir()
                        and not inside_package
                        and candidate.name.startswith("DF-")
                        and DELIVERY_DIRECTORY_PATTERN.fullmatch(candidate.name) is None
                    ):
                        errors.append(
                            "Feature Delivery package directory has invalid canonical ID: "
                            f"{candidate.relative_to(repo_root)}"
                        )


def closed_index_value(text: str, label: str) -> str | None:
    match = re.search(rf"^- {re.escape(label)}:\s*(\S.*?)\s*$", text, re.MULTILINE)
    return match.group(1).strip() if match is not None else None


def active_delivery_ids(repo_root: Path) -> set[str]:
    active_root = repo_root / "work" / "active"
    if not active_root.is_dir():
        return set()
    ids: set[str] = set()
    for task_file in active_root.rglob("task.yaml"):
        delivery_id = yaml_scalar(task_file.read_text(encoding="utf-8"), "delivery_id")
        if delivery_id is not None and DELIVERY_ID_PATTERN.fullmatch(delivery_id):
            ids.add(delivery_id)
    return ids


def validate_closed_delivery_indexes(repo_root: Path, errors: list[str]) -> None:
    closed_root = repo_root / "work" / "closed"
    if not closed_root.is_dir():
        return
    active_ids = active_delivery_ids(repo_root)
    local = repo_root / "workspace.local.yaml"
    tu_vault = external_tu_vault_values(local.read_text(encoding="utf-8")) if local.is_file() else None
    archive_root = tu_vault.get("delivery_archive_root") if tu_vault is not None else None
    for index in closed_root.rglob("*"):
        if index.is_dir():
            continue
        relative = index.relative_to(closed_root)
        if len(relative.parts) != 3 or CLOSED_DELIVERY_INDEX_PATTERN.fullmatch(index.name) is None:
            errors.append(
                "Closed Delivery Index must use work/closed/<domain>/<product>/DF-YYYYMMDD-NN.md: "
                f"{index.relative_to(repo_root)}"
            )
            continue
        delivery_id = index.stem
        text = index.read_text(encoding="utf-8")
        if re.search(rf"^# {re.escape(delivery_id)}\s*$", text, re.MULTILINE) is None:
            errors.append(
                "Closed Delivery Index heading must match delivery ID: "
                f"{index.relative_to(repo_root)}"
            )
        required_labels = (
            "Status",
            "Result",
            "Product",
            "Capabilities",
            "Repositories",
            "Product Truth",
            "Knowledge Update",
            "Key Decisions",
            "Related Deliveries",
            "Archive",
            "Closed At",
        )
        for label in required_labels:
            if closed_index_value(text, label) is None:
                errors.append(
                    f"Closed Delivery Index is missing {label}: {index.relative_to(repo_root)}"
                )
        status = closed_index_value(text, "Status")
        if status is not None and status not in CLOSED_DELIVERY_STATUSES:
            errors.append(
                "Closed Delivery Index has invalid status: "
                f"{index.relative_to(repo_root)} -> {status}"
            )
        archive_reference = closed_index_value(text, "Archive")
        if archive_reference is not None:
            archive_path = archive_reference.removeprefix("tu-vault:")
            if not archive_reference.startswith("tu-vault:") or not is_safe_relative_path(archive_path):
                errors.append(
                    "Closed Delivery Index archive must use safe logical tu-vault reference: "
                    f"{index.relative_to(repo_root)}"
                )
            elif archive_root is not None and is_safe_relative_path(archive_root):
                expected_reference = deterministic_archive_reference(archive_root, delivery_id)
                if archive_reference != expected_reference:
                    errors.append(
                        "Closed Delivery Index archive must match configured deterministic Archive Unit: "
                        f"{index.relative_to(repo_root)} -> {expected_reference}"
                    )
        if status == "superseded":
            related = closed_index_value(text, "Related Deliveries")
            replacement = closed_index_value(text, "Superseded By")
            replacement_ids = {
                *re.findall(r"\bDF-\d{8}-\d{2}\b", related or ""),
                *re.findall(r"\bDF-\d{8}-\d{2}\b", replacement or ""),
            }
            if not (replacement_ids - {delivery_id}):
                errors.append(
                    "superseded Closed Delivery Index requires a replacement Delivery distinct from itself: "
                    f"{index.relative_to(repo_root)}"
                )
        if delivery_id in active_ids:
            errors.append(
                "Delivery cannot be both active and closed: "
                f"{delivery_id}"
            )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    repo_root = parser.parse_args().repo_root.resolve()
    errors: list[str] = []

    error_if_missing(repo_root / "AGENTS.md", "repository AGENTS.md", errors)
    error_if_missing(repo_root / "platform.yaml", "platform manifest", errors)
    registry_codes, repository_products = registered_repositories(
        repo_root, platform_product_ids(repo_root), errors
    )
    registered_codes = set(registry_codes)
    validate_markdown_links(repo_root, errors)
    validate_product_bindings(repo_root, errors)
    validate_repository_manifest_bindings(repo_root, repository_products, errors)
    validate_workspace_configuration(repo_root, registered_codes, errors)
    validate_workspace_template(repo_root, registered_codes, errors)
    validate_sensitive_values(repo_root, errors)
    validate_feature_delivery_packages(repo_root, errors)
    validate_closed_delivery_indexes(repo_root, errors)

    if errors:
        print("AI guidance validation failed:", file=sys.stderr)
        print("\n".join(f"- {error}" for error in errors), file=sys.stderr)
        return 1
    print("AI guidance validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
