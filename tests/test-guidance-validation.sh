#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VALIDATOR="${ROOT}/scripts/validate_guidance.py"

python3 "${VALIDATOR}" --repo-root "${ROOT}"
python3 -m unittest "${ROOT}/tests/test_guidance_validation.py" -v

copy_repository() {
  local destination="$1"
  mkdir -p "${destination}"
  cp "${ROOT}/AGENTS.md" "${ROOT}/.gitignore" "${ROOT}/platform.yaml" "${destination}/"
  cp -R "${ROOT}/.agents" "${ROOT}/bootstrap" "${ROOT}/core" "${ROOT}/docs" "${ROOT}/plugins" "${ROOT}/products" "${ROOT}/scripts" "${ROOT}/tests" "${destination}/"
}

TEMP_ROOT="$(mktemp -d)"
trap 'rm -rf "${TEMP_ROOT}"' EXIT
copy_repository "${TEMP_ROOT}/repo"
printf '\n[broken](missing-file.md)\n' >> "${TEMP_ROOT}/repo/core/index.md"

if OUTPUT="$(python3 "${VALIDATOR}" --repo-root "${TEMP_ROOT}/repo" 2>&1)"; then
  printf 'validator accepted a broken local Markdown link\n' >&2
  exit 1
fi
grep -Fq 'broken Markdown link' <<<"${OUTPUT}"

CONFIG_ROOT="$(mktemp -d)"
trap 'rm -rf "${TEMP_ROOT}" "${CONFIG_ROOT}"' EXIT
copy_repository "${CONFIG_ROOT}/repo"
printf '\n  path: <unset>\n' >> "${CONFIG_ROOT}/repo/workspace.local.yaml"

if OUTPUT="$(python3 "${VALIDATOR}" --repo-root "${CONFIG_ROOT}/repo" 2>&1)"; then
  printf 'validator accepted an unresolved local workspace path\n' >&2
  exit 1
fi
grep -Fq 'workspace.local.yaml has unresolved path' <<<"${OUTPUT}"

printf 'guidance validation test passed\n'
