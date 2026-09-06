---
name: tu-deliver-feature
description: Use when a user explicitly invokes a durable feature delivery workflow to start, resume, check, implement, or stabilize a Delivery ID from a prototype, PRD, contract, task, or bug.
---

# Deliver a Feature

Act as the Delivery lifecycle front door. Keep state in a Task Package, preserve the current user authorization boundary, and load only the context required for the requested action. Read [task-package.md](references/task-package.md) first for a new Delivery or when package structure is unclear; use [resume-format.md](references/resume-format.md) when creating or refreshing the Resume Cache.

## Route the request

1. For a new requirement, create a sortable Delivery ID and Task Package, then start Impact. Do not create optional artifacts until that phase needs them.
2. For an existing ID, locate the package by `task.yaml` `delivery_id` in `work/active/` before reading its `work/closed/` Thin Context Index; a directory slug is not identity. The index routes to matching Product Truth and configured external cold archive, with local legacy cold archive only as fallback. If a closed Delivery has a new related issue, resolve external history first; if neither it nor the local fallback is accessible, report that evidence gap rather than inventing prior state. Otherwise restore/copy only `<Archive Unit>/delivery/` as `work/active/<domain>/<product>/<DF-ID>-<slug>/`, remove its Closed Index, set `status: active`, remove `archived_at`, `archive_reference`, and `closed_index`, and record the reopen in `04-integration-log.md`; `summary.md` and `manifest.yaml` never enter active, and the Vault Archive Unit is never moved, deleted, or modified. Recover a reliable archived slug when available, otherwise derive a readable slug from title. If that Artifact is absent, create it for the stabilization/reopen round and add `integration: 04-integration-log.md` to `task.yaml.artifacts` before recording reopen evidence. Refresh `resume.md`. If the same ID is active and closed, stop and report the state conflict. Then read `task.yaml`, `resume.md`, and the current phase Artifact before inspecting code or acting. If an Artifact is absent, report its absence rather than inventing prior decisions.
3. For status, summarize the current phase, Gates, focus, verified evidence, blockers, and next action without changing implementation.
4. For a Bug, create or locate `BUG-xx`, identify the related CAP when evidence permits, and route it using [Phase 4](references/phase-4-stabilization.md). Do not reset a Gate merely because a test failed.

Treat code, approved Contract, authoritative phase Artifact, and reproducible evidence as Authority. `resume.md` is only a compact cache; refresh it after a phase change, material DEV completion, integration round, important Bug fix, explicit pause, or archive preparation.

## Run the current phase

- **Impact:** read [Phase 1](references/phase-1-impact.md), then use `tu-analyzing-feature-impact` when it is available and applicable.
- **Contract:** read [Phase 2](references/phase-2-contract.md). Adapt available specification methods; do not assume a user-invoked external Skill can be called automatically.
- **Execution:** read [Phase 3](references/phase-3-execution.md). Announce ready DEV tasks and suggest an explicit implementation Skill when required; only implement work the user has authorized.
- **Integration & Stabilization:** read [Phase 4](references/phase-4-stabilization.md). Preserve the distinction between acceptance, publication, adapter dispatch, device execution, and state convergence.

Before closing a Gate, verify its stated evidence. After every meaningful update, change the current Artifact, `task.yaml`, and `resume.md` together enough that a fresh Session can continue without replaying chat history. A DEV / BUG / INT Task Loop Verify only updates its parent Artifact; it does not close the Delivery. When G4 / acceptance or another Closing condition is met, report **Delivery Closing Readiness: ready** and suggest `tu-close-delivery DF-YYYYMMDD-NN`; do not Integrate, Archive, create a Closed Index, or retire the Active Package without that Skill's explicit user authorization.

## Boundaries

Do not turn this Skill into prototype parsing, generic debugging, TDD, code review, or a workflow engine. Use available mature Skills or their methods where allowed. Do not make Apifox, an Issue Tracker, or a generated Controller the Authority; do not write empty Controllers only to produce OpenAPI. Product Knowledge is navigational and receives only verified, reusable conclusions at Delivery completion.
