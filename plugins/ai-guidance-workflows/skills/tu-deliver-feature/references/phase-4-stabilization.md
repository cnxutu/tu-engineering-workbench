# Phase 4: Integration & Stabilization

The question is “how do integration, testing, Bugs, and regression close the loop?” `04-integration-log.md` is authority. Record scenario, CAP/Contract, participating systems, input/environment, expected result, actual result, evidence, and conclusion or linked task.

Check REST initial reads, real-time updates, reconnect/fallback, authorization, invalid/repeated/out-of-order input, timeout and dependency failure, deployment order, and real-device verification as applicable. G4 means required automated and integration evidence exists, with every remaining item explicitly blocked, deferred, or out of scope.

Route each Bug before changing state:

- **Implementation Bug:** remain in Phase 4; diagnose, fix, regress, and log evidence.
- **Contract Bug:** reopen Phase 2; reset G2 and update every affected DEV task before reconfirmation.
- **Requirement Gap:** reopen Phase 1; update CAP, impact, and downstream Contract.
- **Environment/Integration Issue:** remain in Phase 4 as an INT task.

Weeks later, resume the same Delivery ID, read the package's recovery set, and create or update `BUG-xx`; do not start a contextless replacement Delivery.
