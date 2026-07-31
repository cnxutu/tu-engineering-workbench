#!/usr/bin/env bash
set -Eeuo pipefail

MARKETPLACE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
PLUGIN_ROOT="${MARKETPLACE_ROOT}/plugins/ai-guidance-workflows"
MARKETPLACE="${MARKETPLACE_ROOT}/.agents/plugins/marketplace.json"

python3 -m json.tool "${PLUGIN_ROOT}/.codex-plugin/plugin.json" >/dev/null
python3 -m json.tool "${MARKETPLACE}" >/dev/null

grep -Fq '"name": "ai-guidance-workflows"' "${PLUGIN_ROOT}/.codex-plugin/plugin.json"
grep -Fq '"name": "tu-devkit"' "${MARKETPLACE}"
grep -Fq '"path": "./plugins/ai-guidance-workflows"' "${MARKETPLACE}"

for skill in tu-diagnosing-spring-backend-incidents tu-loading-device-inspection-cross-service-context; do
  skill_file="${PLUGIN_ROOT}/skills/${skill}/SKILL.md"
  ui_file="${PLUGIN_ROOT}/skills/${skill}/agents/openai.yaml"
  [[ -f "${skill_file}" && -f "${ui_file}" ]]
  grep -Fxq "name: ${skill}" "${skill_file}"
  grep -Eq '^description: Use when ' "${skill_file}"
  ! grep -Eq '\[TODO|TODO:' "${skill_file}"
done

printf 'ai-guidance-workflows plugin test passed\n'
