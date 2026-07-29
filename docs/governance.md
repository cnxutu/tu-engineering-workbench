# Governance

`ai-guidance` is a shared engineering knowledge base. It is useful only when readers can distinguish verified facts from assumptions and can trace a fact back to evidence.

## Evidence and staleness

Product facts need a reproducible source: code location, API or message contract, checked-in document, test, or approved operational record. Cite the source and state whether it proves current behavior, a target design, or an unresolved hypothesis. Mark unsupported statements as `pending_verification` or `unknown`.

Review product knowledge whenever a task changes service boundaries, shared data ownership, public contracts, deployment topology, or an end-to-end flow. If the task changes such a fact, update the relevant product documentation with evidence; otherwise record a `not-needed` assessment in task metadata. Re-check volatile facts after releases or material infrastructure changes and retire or annotate stale evidence rather than silently treating it as current.

## Sensitive data

Do not store credentials, tokens, private keys, customer identifiers, production payloads, internal host details, or unredacted logs in guidance. Reference a controlled source or redact examples. Evidence references must remain useful without reproducing sensitive content.

## ADRs and task records

Create an ADR under the product's `decisions/` directory for durable, consequential architectural choices: boundaries, ownership, contracts, persistence strategy, or major technology direction. An ADR should name the decision, context, alternatives, outcome, and evidence.

Keep in-progress task records in `tasks/active/`; they may omit `archived_at`. Move completed, blocked, or superseded records to `tasks/archive/`, preserve their identifiers and evidence, add the final status and required `archived_at` time, and link any ADR created by the task. Task records are historical evidence, not a place for secrets or transient scratch notes.

See the [authoring guide](authoring-guide.md), [integration guide](integration-guide.md), and [task metadata contract](../core/contracts/task-metadata.schema.yaml).
