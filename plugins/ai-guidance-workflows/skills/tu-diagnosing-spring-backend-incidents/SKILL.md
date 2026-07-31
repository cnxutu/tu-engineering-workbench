---
name: tu-diagnosing-spring-backend-incidents
description: Use when investigating a Spring Boot backend incident, unexpected behavior, message-processing failure, data inconsistency, latency regression, or production issue before proposing a code or configuration fix.
---

# Diagnosing Spring Backend Incidents

Establish the first broken boundary with evidence before proposing a root cause or fix. Treat product knowledge as navigation and current code, configuration, telemetry, and repeatable tests as evidence.

## Scope and evidence

1. Read the target repository and nearest `AGENTS.md`; when P0 is the primary context, also read `ai-guidance/AGENTS.md`, `core/rules/development.md`, and `core/skills/bug-analysis.md`.
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

## Output contract

Report in this order: **symptom and impact; verified path and scope; evidence timeline or boundary comparison; hypotheses and exclusions; root cause or next evidence collection; minimal fix; verification; residual risks and follow-ups.**

If evidence is insufficient, stop at an evidence-collection plan; do not invent a diagnosis or implement a speculative repair.

## Do not use

Do not use for a clearly reproducible local defect whose root cause and minimal fix are already established, or as permission to inspect unrelated services without evidence.
