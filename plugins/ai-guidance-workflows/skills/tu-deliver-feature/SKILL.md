---
name: tu-deliver-feature
description: Use when a user explicitly invokes a durable feature delivery workflow to start, resume, check, implement, integrate, or stabilize a Delivery ID from a prototype, PRD, contract, task, or bug.
---

# Deliver a Feature

Act as the Delivery lifecycle front door. Keep state in a Task Package, preserve the current user authorization boundary, and load only the context required for the requested action. Read [task-package.md](references/task-package.md) first for a new Delivery or when package structure is unclear; use [resume-format.md](references/resume-format.md) when creating or refreshing the Resume Cache.

## Route the request

1. For a new requirement, create a sortable Delivery ID and Task Package, then start Impact. Do not create optional artifacts until that phase needs them.
2. For an existing ID, locate the package by `task.yaml` `delivery_id` in `work/active/` before reading its `work/closed/` Thin Context Index; a directory slug is not identity. The index routes only to the matching Product Truth and optional local/external cold archive. If a matching local archived Delivery has a new issue that belongs to it, move its complete directory back to `work/active/`, remove its Closed Index, set `status: active`, remove `archived_at`, and record the reopen in `04-integration-log.md`. If full history is external and unavailable, report that evidence gap rather than inventing prior state. If that Artifact is absent, create it for the stabilization/reopen round and add `integration: 04-integration-log.md` to `task.yaml.artifacts` before recording reopen evidence. Refresh `resume.md`. If the same ID is active and closed, stop and report the state conflict. Then read `task.yaml`, `resume.md`, and the current phase Artifact before inspecting code or acting. If an Artifact is absent, report its absence rather than inventing prior decisions.
3. For status, summarize the current phase, Gates, focus, verified evidence, blockers, and next action without changing implementation.
4. For a Bug, create or locate `BUG-xx`, identify the related CAP when evidence permits, and route it using [Phase 4](references/phase-4-stabilization.md). Do not reset a Gate merely because a test failed.

Treat code, approved Contract, authoritative phase Artifact, and reproducible evidence as Authority. `resume.md` is only a compact cache; refresh it after a phase change, material DEV completion, integration round, important Bug fix, explicit pause, or archive preparation.

## Run the current phase

- **Impact:** read [Phase 1](references/phase-1-impact.md), then use `tu-analyzing-feature-impact` when it is available and applicable.
- **Contract:** read [Phase 2](references/phase-2-contract.md). Adapt available specification methods; do not assume a user-invoked external Skill can be called automatically.
- **Execution:** read [Phase 3](references/phase-3-execution.md). Announce ready DEV tasks and suggest an explicit implementation Skill when required; only implement work the user has authorized.
- **Integration & Stabilization:** read [Phase 4](references/phase-4-stabilization.md). Preserve the distinction between acceptance, publication, adapter dispatch, device execution, and state convergence.

Before closing a Gate, verify its stated evidence. After every meaningful update, change the current Artifact, `task.yaml`, and `resume.md` together enough that a fresh Session can continue without replaying chat history. A DEV / BUG / INT Task Loop Verify only updates its parent Artifact; it does not close the Delivery. Only after the whole Delivery reaches G4 / acceptance or an explicit Closing condition, Integrate verified reusable facts into Product Truth before creating the Thin Context Index and recording its archive reference; this is not a new E/P/X/V stage.

## Boundaries

Do not turn this Skill into prototype parsing, generic debugging, TDD, code review, or a workflow engine. Use available mature Skills or their methods where allowed. Do not make Apifox, an Issue Tracker, or a generated Controller the Authority; do not write empty Controllers only to produce OpenAPI. Product Knowledge is navigational and receives only verified, reusable conclusions at Delivery completion.
