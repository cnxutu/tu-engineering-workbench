---
name: tu-analyzing-feature-impact
description: Use when a prototype, PRD, screenshot, PDF, or requirement needs an evidence-backed backend and cross-service impact review before API contract design or implementation.
---

# Analyze Feature Impact

Convert requirement evidence into `01-impact-review.md`, not an implementation plan or final API. Read [impact-review-format.md](references/impact-review-format.md) for the required review shape and [prototype-extraction-checklist.md](references/prototype-extraction-checklist.md) when input includes visual prototype material.

## Evidence to capability

1. Inspect every accessible source at usable fidelity. Record source/frame/page, variant, readable coverage, contradictions, and missing regions; OCR assists reading but is not visual evidence by itself.
2. Normalize pages, dialogs, state changes, and behaviors into stable `CAP-xx` capabilities. Classify visible elements as input, output, query, command, navigation-only, presentation-only, computed, joined, or unresolved.
3. For each capability, inspect the smallest relevant repository, Contract, configuration, and test evidence. Mark the disposition `reuse`, `change`, `new`, `frontend_only`, `upstream_dependency`, `out_of_scope`, or `unknown`.
4. Trace repository ownership and cross-service seams. For real-time behavior, separately assess initial read, incremental updates, reconnect, fallback, ordering, and state convergence.
5. Separate verified prototype evidence, verified repository facts, inferences, and open decisions. Do not infer authorization, tenant scope, state transitions, identifiers, enum wire values, idempotency, persistence, or device execution from UI appearance.

## Handoff

The review is ready for G1 consideration only when every in-scope capability has a disposition, each material uncertainty is recorded with an owner/blocker, and scope/non-goals are explicit. Do not create `02-api-contract.md`, write code, or claim scope confirmation without the required evidence and approval.
