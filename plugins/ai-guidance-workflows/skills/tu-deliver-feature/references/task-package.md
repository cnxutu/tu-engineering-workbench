# Task Package and Resume Cache

Create packages under `work/active/<domain>/<product>/<delivery-id>-<slug>/`. `delivery_id` is the stable machine identity and Context Address `DF-YYYYMMDD-NN`; the directory slug is a separately changeable, lowercase readable aid. The ID survives all phases and later Bugs; child work uses `CAP-xx`, `EXT-xx`, `DEV-xx`, `INT-xx`, and `BUG-xx`.

For a new Delivery, scan `work/active/`, `work/closed/`, and retained `work/**/tasks/archive/` cold history for that day's `DF-YYYYMMDD-NN`, choose the greatest `NN` plus one, and retry with the next number if the target directory already exists. This is a local allocation convention only: do not add a lock, sequence file, registry, service, or database.

```yaml
delivery_id: DF-20260904-01
title: Robot-dog fill-light control
status: active
phase: impact
product: company/device-inspection-platform
repositories:
  - c-drone-inspection
capabilities:
  - device-control
related_deliveries: []
created_at: 2026-09-04T10:00:00+08:00
gates:
  G1_scope_confirmed: pending
  G2_contract_confirmed: pending
  G3_tasks_ready: pending
  G4_test_ready: pending
artifacts:
  impact: 01-impact-review.md
  resume: resume.md
current_focus:
  type: feature
  id: CAP-01
  summary: Confirm device-command success semantics.
last_verified: []
next_actions: []
evidence:
  - source: <requirement-or-prototype-reference>
    summary: Short, non-sensitive source summary.
knowledge_update_assessment: deferred
```

New Deliveries create only `task.yaml`, `resume.md`, and the current phase Artifact; Artifact keys point only to files that already exist. Add Contract, OpenAPI, Backlog, and Integration keys as their files are created. At Closing, Integrate verified reusable facts into Product Truth; create `work/closed/<domain>/<product>/<delivery-id>.md` with title, result, Product Truth links, capabilities, repositories, key decisions, related deliveries, and archive reference. Move the full package to retained `work/<domain>/<product>/tasks/archive/` local cold history until an external archive is available, adding `archived_at`, `closed_index`, and `archive_reference` as required by task metadata.

```markdown
# DF-YYYYMMDD-NN

- Status: closed
- Product Truth: <links updated during Integrate>
- Capabilities: <current capability names>
- Repositories: <confirmed repositories>
- Key Decisions: <only durable decisions>
- Related Deliveries: <DF IDs>
- Archive: local cold path | external reference | not-yet-archived
```

When a later Bug belongs to a locally archived Delivery, move the whole directory back to `work/active/`, remove its Closed Index, preserve `delivery_id`, set `status: active`, remove `archived_at`, and record Reopened At, Reason, related BUG/CAP, previous completion context, and current classification in `04-integration-log.md`. If the integration log is absent, create it for the stabilization/reopen round and register `integration: 04-integration-log.md` under `task.yaml.artifacts` before recording the evidence. If the Closed Index references unavailable external history, report the evidence gap instead of inventing context. Refresh the resume cache before continuing.

`resume.md` has only: Delivery ID, Current Phase, Goal, Confirmed Decisions, Current Implementation, Open Items, Relevant Commits, Read Next, and Next Action. Link rather than copy Contracts, source, logs, or requirements. It is never the authority when it conflicts with current evidence.
