# Impact Review Format

Use only sections required by the evidence, but make `01-impact-review.md` reviewable without chat history.

## Scope and evidence

- Goal, in-scope outcomes, explicit non-goals, and target product/repositories.
- Source inventory: prototype/PRD links or paths, page/frame coverage, variant, legibility, and missing areas.
- Evidence status: prototype evidence, repository fact, inference, or open decision.

## Capability and disposition matrix

| CAP | Source behavior | Backend disposition | Existing evidence / seam | Affected repositories | Decision or blocker |
| --- | --- | --- | --- | --- | --- |

Use one capability across Contract, backlog, and integration artifacts. A button is not automatically a new endpoint, and a displayed value is not automatically a request field or stored column.

## Cross-service and real-time impact

For every affected seam, name the current or proposed owner, producer, consumer, REST/WS/MQTT/topic/identifier boundary, and unresolved responsibility. For live state, record initial read, incremental refresh, reconnect behavior, fallback, isolation, ordering/deduplication, and the evidence for state convergence.

## Open decisions and release shape

List each question with the affected CAP, decision owner, required evidence, and whether it blocks G1, Contract, implementation, or only an optional slice. End with risks, dependencies, and a recommended vertical-slice order. Do not place final endpoint schemas here.
