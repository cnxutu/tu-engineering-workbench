#!/usr/bin/env bash
set -Eeuo pipefail

MARKETPLACE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
PLUGIN_ROOT="${MARKETPLACE_ROOT}/plugins/ai-guidance-workflows"
MARKETPLACE="${MARKETPLACE_ROOT}/.agents/plugins/marketplace.json"

if command -v python3 >/dev/null 2>&1; then
  PYTHON_CMD="python3"
elif command -v python >/dev/null 2>&1; then
  PYTHON_CMD="python"
else
  printf 'python3 or python is required\n' >&2
  exit 1
fi

"${PYTHON_CMD}" -m json.tool "${PLUGIN_ROOT}/.codex-plugin/plugin.json" >/dev/null
"${PYTHON_CMD}" -m json.tool "${MARKETPLACE}" >/dev/null

grep -Fq '"name": "ai-guidance-workflows"' "${PLUGIN_ROOT}/.codex-plugin/plugin.json"
grep -Fq '"name": "tu-devkit"' "${MARKETPLACE}"
grep -Fq '"path": "./plugins/ai-guidance-workflows"' "${MARKETPLACE}"

"${PYTHON_CMD}" "${PLUGIN_ROOT}/tests/validate-skills.py" "${PLUGIN_ROOT}"

printf 'ai-guidance-workflows plugin test passed\n'
