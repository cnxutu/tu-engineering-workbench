# Prototype Extraction Checklist

Use this checklist while reading prototype images. Record only visible evidence or separately identified repository facts.

## Page inventory

- Page or dialog name and source image.
- Page relationship: entry, list, detail, create, edit, confirmation, or state action.
- User-visible action and its trigger.
- Loading, empty, disabled, success, and failure states when shown.

## List and search

- Displayed columns and formatting.
- Search fields, match semantics if stated, reset behavior, and defaults.
- Filters, enum options, date ranges, sorting, and pagination.
- Row actions, bulk actions, export/import, and confirmation prompts.

## Form and detail

- Labels, controls, placeholders, units, and help text.
- Required markers, read-only fields, defaults, length or format hints.
- Select/radio values and whether values are labels or stable codes.
- Conditional visibility, field dependencies, and edit restrictions.
- Related objects, nested rows, attachments, and ordering.

## Decisions the prototype usually cannot prove

- Authorization, data scope, tenant isolation, and ownership.
- Primary key type, uniqueness, optimistic locking, and idempotency.
- Physical versus logical deletion and cascade behavior.
- State-machine transitions and concurrency behavior.
- Audit fields, retention, migration/backfill, and rollback requirements.
- Exact error codes, conflict rules, and partial-failure semantics.

Verify these from current repository conventions or request a decision when they materially affect the contract.

## Traceability table

Use one row per field or action:

| Prototype source | UI element | API mapping | Persistence mapping | Validation/business rule | Evidence status |
| --- | --- | --- | --- | --- | --- |
| Image/page/region | Visible label or action | Request/response field or endpoint | Column/relation or none | Confirmed rule | prototype / repository / inference / open |

For fields shown only in output, do not automatically place them in create or update requests. For calculated or joined values, do not create redundant columns without evidence.
