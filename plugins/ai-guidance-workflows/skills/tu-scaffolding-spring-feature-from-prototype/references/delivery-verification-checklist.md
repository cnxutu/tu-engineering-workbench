# Delivery Verification Checklist

## Code and behavior

- Implementation matches the confirmed endpoint and data inventory.
- Every endpoint, public field, persistence change, validation rule, and state transition maps to prototype evidence, an approved decision, or a verified repository convention.
- Frontend-only, computed, joined, example, and placeholder values did not become accidental request fields or columns.
- Controller, service/application, and persistence responsibilities follow the target repository.
- Public models do not accidentally expose persistence-only fields.
- Validation, authorization, tenancy, transactions, exceptions, pagination, and logical deletion reuse verified conventions.
- Normal behavior and applicable validation, not-found, conflict, and authorization failures are tested.
- Create/update/query/response model asymmetry, enum wire values, time semantics, precision/units, null/clear behavior, and upload lifecycle match the confirmed contract when applicable.

## Database

- Migration naming and location follow the repository.
- Types, lengths, nullability, defaults, keys, constraints, and comments match the confirmed semantics.
- Indexes correspond to actual filters, joins, uniqueness, or ordering.
- Existing-row compatibility and backfill needs are addressed.
- Destructive operations, locking risk, repeatability expectations, validation, and rollback boundary are explicit.
- Columns and indexes are justified by confirmed persistence or query semantics rather than UI layout alone.

## Swagger/OpenAPI

- Controller grouping and operation summaries are useful to frontend consumers.
- Every request and response schema has correct field descriptions and types.
- Requiredness and validation constraints agree with runtime validation.
- Enum wire values, descriptions, and examples are unambiguous.
- Response envelopes, pagination, identifiers, dates/times, uploads, and nullable fields serialize as documented.
- The generated OpenAPI document contains every confirmed method/path and referenced schema.
- Generated documentation was inspected when possible; annotation presence alone is insufficient evidence.

## Final review

- All in-scope pages/frames have recorded coverage; missing regions and prototype contradictions are resolved, explicitly blocked, or out of scope.
- Relevant tests, checks, and build commands have actual recorded results.
- The final diff contains no unrelated formatting, refactors, artifacts, or secrets.
- Any unverified runtime or external Apifox step is stated explicitly.
