#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
VALIDATOR="${ROOT}/ai-guidance/scripts/validate_guidance.py"

python3 "${VALIDATOR}" --repo-root "${ROOT}"

TEMP_ROOT="$(mktemp -d)"
trap 'rm -rf "${TEMP_ROOT}"' EXIT
mkdir -p "${TEMP_ROOT}/repo"
cp "${ROOT}/AGENTS.md" "${TEMP_ROOT}/repo/AGENTS.md"
cp "${ROOT}/.gitignore" "${TEMP_ROOT}/repo/.gitignore"
cp -R "${ROOT}/ai-guidance" "${TEMP_ROOT}/repo/ai-guidance"
printf '\n[broken](missing-file.md)\n' >> "${TEMP_ROOT}/repo/ai-guidance/core/index.md"

if OUTPUT="$(python3 "${VALIDATOR}" --repo-root "${TEMP_ROOT}/repo" 2>&1)"; then
  printf 'validator accepted a broken local Markdown link\n' >&2
  exit 1
fi
grep -Fq 'broken Markdown link' <<<"${OUTPUT}"

CONFIG_ROOT="$(mktemp -d)"
trap 'rm -rf "${TEMP_ROOT}" "${CONFIG_ROOT}"' EXIT
mkdir -p "${CONFIG_ROOT}/repo"
cp "${ROOT}/AGENTS.md" "${CONFIG_ROOT}/repo/AGENTS.md"
cp "${ROOT}/.gitignore" "${CONFIG_ROOT}/repo/.gitignore"
cp -R "${ROOT}/ai-guidance" "${CONFIG_ROOT}/repo/ai-guidance"
printf '\n  path: <unset>\n' >> "${CONFIG_ROOT}/repo/ai-guidance/workspace.local.yaml"

if OUTPUT="$(python3 "${VALIDATOR}" --repo-root "${CONFIG_ROOT}/repo" 2>&1)"; then
  printf 'validator accepted an unresolved local workspace path\n' >&2
  exit 1
fi
grep -Fq 'workspace.local.yaml has unresolved path' <<<"${OUTPUT}"

printf 'guidance validation test passed\n'
