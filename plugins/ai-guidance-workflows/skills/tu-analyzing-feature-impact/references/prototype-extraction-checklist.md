# Prototype Extraction Checklist

Record source, page/frame, variant, relationship to adjacent states, and unreadable regions. Inspect full screens and targeted crops for dense content; distinguish labels, examples, placeholders, annotations, and confirmed defaults.

For lists and forms, capture visible fields, actions, filters, sort/pagination controls, required/read-only markers, conditional visibility, loading/empty/error states, and before/after behavior. Compare repeated views and log contradictions instead of silently selecting one.

For each backend-relevant field/action, record its disposition and traceability:

| Source | UI element | Disposition | Candidate boundary | Persistence implication | Evidence status |
| --- | --- | --- | --- | --- | --- |

Explicitly leave these as decisions unless independently evidenced: authorization/data scope, tenant isolation, public ID representation, enum wire values, time/precision units, null/clear behavior, state machine, concurrency, idempotency, deletion/cascade behavior, audit/retention, migration, error semantics, and attachment lifecycle.
