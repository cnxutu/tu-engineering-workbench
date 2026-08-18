# Prototype Extraction Checklist

Use this checklist while reading prototype pages and frames. Record only visible evidence or separately identified repository facts.

## Source inventory and legibility

- Source identifier, page/frame name, order, visible revision or variant, and relationship to adjacent frames.
- Full-frame inspection completed; targeted crops inspected for dense, small, or ambiguous regions.
- Text verified visually when OCR is used; OCR output is not evidence by itself.
- Missing, clipped, obscured, low-resolution, or inaccessible regions are named precisely.
- Desktop/mobile, role, state, and before/after variants are grouped rather than treated as unrelated features.

## Page inventory

- Page or dialog name and source image.
- Page relationship: entry, list, detail, create, edit, confirmation, or state action.
- User-visible action and its trigger.
- Loading, empty, disabled, success, and failure states when shown.
- Dialog, drawer, popover, confirmation, and navigation destination relationships.

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
- Whether visible text is a label, placeholder, example record, annotation, computed value, or confirmed default.

## Cross-screen consistency

- Repeated fields agree on naming, requiredness, type hints, option labels, default, and editability.
- Repeated actions agree on availability, confirmation, result, and failure behavior.
- List, detail, create, and edit views agree on identity and lifecycle semantics.
- Contradictions are recorded with both sources; no frame is silently chosen as authoritative.

## Backend disposition

Classify every in-scope field and action as one of: input, output, query criterion, command, navigation-only, presentation-only, computed, joined, or unresolved. A visible element may intentionally have no API or persistence mapping.

Check ambiguous wire semantics explicitly:

- Identifier type and public representation.
- Enum display label versus stable wire value.
- Date/time format, time zone, and date-only versus instant semantics.
- Numeric precision, scale, unit, rounding, and currency.
- Null, empty, omitted, defaulted, and clear-field behavior.
- Attachment upload, reference, replacement, deletion, and access lifecycle.
- Search matching, filter combination, sort stability, and pagination behavior.

## Decisions the prototype usually cannot prove

- Authorization, data scope, tenant isolation, and ownership.
- Primary key type, uniqueness, optimistic locking, and idempotency.
- Physical versus logical deletion and cascade behavior.
- State-machine transitions and concurrency behavior.
- Audit fields, retention, migration/backfill, and rollback requirements.
- Exact error codes, conflict rules, and partial-failure semantics.
- Enum wire values, time-zone policy, monetary precision, and upload lifecycle.

Verify these from current repository conventions or request a decision when they materially affect the contract.

## Traceability table

Use one row per field or action:

| Prototype source | UI element | Backend disposition | API mapping | Persistence mapping | Validation/business rule | Evidence status |
| --- | --- | --- | --- | --- | --- | --- |
| Image/page/region | Visible label or action | input/output/query/command/frontend/computed/joined/unresolved | Request/response field, endpoint, or none | Column/relation or none | Confirmed rule or open semantic | prototype / repository / inference / open |

For fields shown only in output, do not automatically place them in create or update requests. For calculated or joined values, do not create redundant columns without evidence.

## Contradiction and coverage log

| Topic | Source A | Source B or missing region | Impacted contract or behavior | Resolution status |
| --- | --- | --- | --- | --- |
| Field/action/state | Page/frame/region | Page/frame/region | Exact endpoint, schema, data, or rule impact | resolved / proposed / blocking / out of scope |

Complete extraction only when every in-scope page/frame is inventoried, every backend-relevant element has a disposition, and every material contradiction, inference, or unreadable region is represented in traceability or the decision log.
