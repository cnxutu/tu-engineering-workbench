# Phase 4: Integration & Stabilization

The question is “how do integration, testing, Bugs, and regression close the loop?” `04-integration-log.md` is authority. Record scenario, CAP/Contract, participating systems, input/environment, expected result, actual result, evidence, and conclusion or linked task.

Check REST initial reads, real-time updates, reconnect/fallback, authorization, invalid/repeated/out-of-order input, timeout and dependency failure, deployment order, and real-device verification as applicable. G4 means required automated and integration evidence exists, with every remaining item explicitly blocked, deferred, or out of scope.

Route each Bug before changing state:

- **Implementation Bug:** remain in Phase 4; keep G1–G3 unchanged, diagnose, fix, regress, and log evidence.
- **Contract Bug:** set phase to `contract`, reset G2 to `pending`, and update every affected DEV/INT task before reconfirmation.
- **Requirement Gap:** set phase to `impact`, reset G1 to `pending`, and update CAP, impact, Contract, and Backlog.
- **Environment/Integration Issue:** remain in `stabilization` as an INT task.

When reopening an archived Delivery, move the package to `active/`, restore `status: active`, and log Reopened At, Reason, related BUG/CAP, previous completion context, and current classification before routing. If `04-integration-log.md` is absent, create it for this stabilization/reopen round and register `integration: 04-integration-log.md` under `task.yaml.artifacts` before writing that evidence. Weeks later, resume the same Delivery ID, read the package's recovery set, and create or update `BUG-xx`; do not start a contextless replacement Delivery.

Preferred provider: use `diagnosing-bugs` for implementation defects when available and model-invokable. The orchestrator still owns Delivery/CAP/phase classification and Artifact updates.
