---
name: tu-diagnosing-spring-backend-incidents
description: Use when investigating a Spring Boot backend incident, runtime/container failure, unexpected behavior, message-processing failure, data inconsistency, latency regression, or production issue before proposing a code or configuration fix.
---

# Diagnosing Spring Backend Incidents

Establish the first broken boundary with evidence before proposing a root cause or fix. Treat product knowledge as navigation and current code, configuration, telemetry, and repeatable tests as evidence.

For a runtime-aware incident (the task names `ssh <shortcut>`, an environment/server, Docker/container state, runtime
logs, or otherwise requires runtime evidence), follow the procedure in
[Runtime Diagnostic Procedure](references/runtime-diagnostic-procedure.md). Keep ordinary code/service incidents on
the existing path; do not require SSH or runtime files unless the problem needs that evidence.

## Scope and evidence

1. Read the target repository and nearest `AGENTS.md`; when P0 is the primary context, also read its root `AGENTS.md`, `core/rules/development.md`, and `core/playbooks/bug-analysis.md`.
2. Keep the initial scope to the service named by the user. Expand to an upstream or downstream repository only after boundary evidence requires it.
3. Request or obtain one or more anomalous samples: a desensitized business/device/request identifier, time window, expected result, actual result, impact, version, and environment.
4. Separate observations, hypotheses, and unknowns. Do not name a root cause, class, Topic, table, configuration key, or runtime behavior until it has been read or observed.

## Investigation workflow

1. Reproduce the symptom when safe, or define the smallest repeatable observation.
2. Draw the actual request, message, cache, database, or external-call path from code and configuration.
3. At every boundary, compare input, accepted/processed/rejected result, retry or timeout state, and persisted or observable output using the same correlation key.
4. Locate the first boundary with a verified mismatch. Distinguish delivery failure, consumption/processing failure, intentional business filtering, persistence failure, and read-model or visibility delay.
5. Compare a failing sample with a nearby successful sample; inspect version and configuration differences without exposing credentials or production payloads.
6. Propose the smallest evidence-backed fix. State compatibility, rollback, data repair, and regression scope before implementation.

## Runtime-aware branch

Resolve the repository scope, optional Runtime Target Hint, engineering stage, and problem before touching a host. Then
resolve the logical environment through the Workbench registry, local binding, and product Runtime Context; use only the
minimum deployment, observability, framework-provenance, and local snapshot material required by the problem. Resolve a
diagnostic subject (service, container, request/trace, device, message, dependency, or deployment) and inspect the
smallest relevant boundary first.

Use the evidence ladder in order: runtime state, targeted logs, trace/correlation, evidence-directed dependency or
middleware checks, then repository/code/framework mapping. A trace ID is a local correlation aid unless propagation across
the specific boundary is verified; do not treat it as a universal end-to-end key. Do not copy bulk logs or business
payloads into Workbench.

Runtime diagnosis is read-only by default. Runtime access never authorizes restart, deployment, configuration or data
mutation. Stop when the symptom-to-runtime-to-implementation/configuration chain is closed, or report the evidence gap
and next evidence when it is not. Request an explicit scope decision before reading an out-of-scope repository.

## Output contract

For ordinary incidents, report in this order: **symptom and impact; verified path and scope; evidence timeline or boundary
comparison; hypotheses and exclusions; root cause or next evidence collection; minimal fix; verification; residual risks
and follow-ups.** For runtime-aware incidents, use the stable contract: **Facts; Evidence; Hypothesis; Unknown; Next
Evidence; Diagnosis** (with impact and recommended action as useful context). Diagnosis must be limited to the evidence:
`Root Cause Confirmed`, `Most Likely Cause`, or `Insufficient Evidence`.

If evidence is insufficient, stop at an evidence-collection plan; do not invent a diagnosis or implement a speculative repair.

## Do not use

Do not use for a clearly reproducible local defect whose root cause and minimal fix are already established, or as permission to inspect unrelated services without evidence.
