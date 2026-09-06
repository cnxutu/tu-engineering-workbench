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

New Deliveries create only `task.yaml`, `resume.md`, and the current phase Artifact; Artifact keys point only to files that already exist. Add Contract, OpenAPI, Backlog, and Integration keys as their files are created. A Task Loop Verify only updates its parent Artifact. When the whole Delivery reaches G4 / acceptance or another Closing condition, `tu-deliver-feature` only reports readiness and suggests explicit user invocation of `tu-close-delivery`; it does not mutate Closing state. The Closing Skill first Integrates verified reusable facts, then archives the full package to configured `tu-vault`, verifies archive, creates `work/closed/<domain>/<product>/<delivery-id>.md`, and retires the active Package. Retained `work/<domain>/<product>/tasks/archive/` remains legacy/local cold compatibility only. `blocked` and `superseded` can also close; Archive means closed lifecycle/cold context, not successful delivery.

```markdown
# DF-YYYYMMDD-NN

- Status: closed
- Product Truth: <links updated during Integrate>
- Capabilities: <current capability names>
- Repositories: <confirmed repositories>
- Key Decisions: <only durable decisions>
- Related Deliveries: <DF IDs>
- Archive: tu-vault:<relative-path>
```

When a later Bug belongs to a closed Delivery, resolve its configured external archive reference first; if unavailable, inspect retained local legacy cold history as a compatibility fallback. Restore the complete Package to `work/active/`, remove its Closed Index, preserve `delivery_id`, set `status: active`, remove `archived_at`, and record Reopened At, Reason, related BUG/CAP, previous completion context, and current classification in `04-integration-log.md`. If neither external archive nor local legacy history is available, report the evidence gap instead of inventing context. Refresh the resume cache before continuing.

`resume.md` has only: Delivery ID, Current Phase, Goal, Confirmed Decisions, Current Implementation, Open Items, Relevant Commits, Read Next, and Next Action. Link rather than copy Contracts, source, logs, or requirements. It is never the authority when it conflicts with current evidence.
