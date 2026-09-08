# Phase 4: Integration & Stabilization

The question is “how do integration, testing, Bugs, and regression close the loop?” `04-integration-log.md` is authority. Record scenario, CAP/Contract, participating systems, input/environment, expected result, actual result, evidence, and conclusion or linked task.

Check REST initial reads, real-time updates, reconnect/fallback, authorization, invalid/repeated/out-of-order input, timeout and dependency failure, deployment order, and real-device verification as applicable. G4 means required automated and integration evidence exists, with every remaining item explicitly blocked, deferred, or out of scope.

Route each Bug before changing state:

- **Implementation Bug:** remain in Phase 4; keep G1–G3 unchanged, diagnose, fix, regress, and log evidence.
- **Contract Bug:** set phase to `contract`, reset G2 to `pending`, and update every affected DEV/INT task before reconfirmation.
- **Requirement Gap:** set phase to `impact`, reset G1 to `pending`, and update CAP, impact, Contract, and Backlog.
- **Environment/Integration Issue:** remain in `stabilization` as an INT task.

A BUG or INT Task Loop Verify only records evidence in `04-integration-log.md`; it does not close the Delivery. An explicit Product Truth Sync may independently update already-established Current Truth without mutating this Delivery. When the whole Delivery reaches G4 / acceptance or another Closing condition, report readiness and suggest the user explicitly invoke `tu-close-delivery DF-YYYYMMDD-NN`. That Skill owns final Product Truth reconciliation, configured external archive, Closed Index, and Active Package retirement; this is a lifecycle closing action, not a new Task Loop Stage. `completed` normally requires accepted G4 evidence; `blocked` and `superseded` may also close, reconciling only facts that remain verified and current-worthy.

When reopening a closed Delivery, resolve its configured immutable external Archive Unit first and use retained local archive only as compatibility fallback. Restore/copy only `<Archive Unit>/delivery/` as the Active Package under `work/active/<domain>/<product>/<DF-ID>-<slug>/`; do not copy `summary.md` or `manifest.yaml`, and never move, delete, or modify the Vault Unit. Recover a reliable archived slug when available, otherwise derive a readable slug from title. Remove its Closed Index, restore `status: active`, remove `archived_at`, `archive_reference`, and `closed_index`, and log Reopened At, Reason, Previous Closing Status, Previous Closed At, Archive Reference, related BUG/CAP, and Current Classification before routing. If `04-integration-log.md` is absent, create it for this stabilization/reopen round and register `integration: 04-integration-log.md` under `task.yaml.artifacts` before writing that evidence. Weeks later, resume the same Delivery ID, read the package's recovery set, and create or update `BUG-xx`; do not start a contextless replacement Delivery. If external and legacy history are both unavailable, report the evidence gap.

For non-trivial BUG or INT work, use the Explore → Plan → Execute → Verify task loop. Do not bypass current authorization or the Delivery Gate/Artifact authority.

Preferred provider: use `diagnosing-bugs` for implementation defects when available and model-invokable. The orchestrator still owns Delivery/CAP/phase classification and Artifact updates.
