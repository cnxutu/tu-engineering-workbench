# Design Preview Format

Use the smallest sections needed, but preserve decisions affecting public API or data semantics.

## 1. Scope and evidence

- Goal and acceptance outcome.
- Target repository and module.
- Prototype sources, page/frame coverage, variants, and comparable code inspected.
- Non-goals, inaccessible or unreadable regions, and contradictions affecting confidence.

## 2. Prototype-to-contract traceability

Include the field/action traceability table from the extraction checklist. Account explicitly for frontend-only, computed, joined, and unresolved elements; highlight open decisions rather than hiding them in prose.

Add the contradiction and coverage log when frames disagree or evidence is missing. State which endpoints, schemas, or rules are unaffected and which remain blocked.

## 3. Endpoint inventory

| Operation | Method and path | Authorization/data scope | Request | Response | Failure semantics |
| --- | --- | --- | --- | --- | --- |

For each request and response schema, state field type, requiredness, validation, enum wire values and labels, example, null/clear behavior, and whether the field is create-only, update-only, query-only, output-only, or shared. Call out identifier, date/time, precision/unit, upload, pagination, and sorting semantics when applicable.

## 4. Data design

| Table/change | Column or constraint | Type/default/nullability | Source and rationale | Compatibility/rollback |
| --- | --- | --- | --- | --- |

State primary/foreign keys, unique constraints, indexes tied to real query paths, audit and logical-delete behavior, and whether existing rows require backfill.

## 5. Business flow

Describe the normal flow and only the key failure paths. Include validation, not-found, conflict, permission, transaction, and concurrency semantics when applicable.

For state-changing actions, state allowed source state, target state, authorization/data scope, idempotency or retry behavior, and conflict handling when applicable.

## 6. Decision log

Classify each item as:

- **Confirmed**: explicit requirement or approved decision.
- **Repository-derived**: verified convention reused without changing public semantics.
- **Proposed**: recommended decision awaiting confirmation.
- **Unknown**: missing evidence that blocks safe implementation.

## 7. Implementation and verification boundary

- Expected files/layers to change.
- Migration and compatibility approach.
- Tests, build, and OpenAPI checks to run.
- External actions excluded, including Apifox upload unless explicitly authorized.

End with one batched confirmation request only when proposed or unknown items materially alter behavior, contract, data, security, or scope.
