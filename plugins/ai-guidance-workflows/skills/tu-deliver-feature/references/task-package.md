# Task Package and Resume Cache

Create packages under `work/<domain>/<product>/tasks/active/<delivery-id>-<slug>/`. Use `DF-YYYYMMDD-NN` and an optional lowercase readable slug. The ID survives all phases and later Bugs; child work uses `CAP-xx`, `EXT-xx`, `DEV-xx`, `INT-xx`, and `BUG-xx`.

```yaml
delivery_id: DF-20260904-01
title: Robot-dog fill-light control
status: active
phase: impact
product: company/device-inspection-platform
repositories:
  - c-drone-inspection
  - c-iot-server
gates:
  G1_scope_confirmed: pending
  G2_contract_confirmed: pending
  G3_tasks_ready: pending
  G4_test_ready: pending
artifacts:
  impact: 01-impact-review.md
  contract: 02-api-contract.md
  openapi: 02-openapi.yaml
  backlog: 03-execution-backlog.md
  integration: 04-integration-log.md
  resume: resume.md
current_focus:
  type: feature
  id: CAP-01
  summary: Confirm device-command success semantics.
last_verified: []
next_actions: []
knowledge_update_assessment: deferred
```

Omit `openapi` and its file when REST is absent or a machine-readable REST contract is not needed. Artifact keys point to files that actually exist. Archive the whole directory after completing, blocking, or superseding it, adding `archived_at` as required by task metadata.

`resume.md` has only: Delivery ID, Current Phase, Goal, Confirmed Decisions, Current Implementation, Open Items, Relevant Commits, Read Next, and Next Action. Link rather than copy Contracts, source, logs, or requirements. It is never the authority when it conflicts with current evidence.
