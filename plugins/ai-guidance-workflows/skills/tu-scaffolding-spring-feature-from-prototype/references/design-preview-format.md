# Design Preview Format

Use the smallest sections needed, but preserve decisions affecting public API or data semantics.

## 1. Scope and evidence

- Goal and acceptance outcome.
- Target repository and module.
- Prototype pages and comparable code inspected.
- Non-goals and inaccessible evidence.

## 2. Prototype-to-contract traceability

Include the field/action traceability table from the extraction checklist. Highlight open decisions rather than hiding them in prose.

## 3. Endpoint inventory

| Operation | Method and path | Authorization/data scope | Request | Response | Failure semantics |
| --- | --- | --- | --- | --- | --- |

For each request and response schema, state field type, requiredness, validation, enum values, example, and whether the field is create-only, update-only, output-only, or shared.

## 4. Data design

| Table/change | Column or constraint | Type/default/nullability | Source and rationale | Compatibility/rollback |
| --- | --- | --- | --- | --- |

State primary/foreign keys, unique constraints, indexes tied to real query paths, audit and logical-delete behavior, and whether existing rows require backfill.

## 5. Business flow

Describe the normal flow and only the key failure paths. Include validation, not-found, conflict, permission, transaction, and concurrency semantics when applicable.

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
