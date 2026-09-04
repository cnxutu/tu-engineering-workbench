# Phase 2: Contract

The question is “what do frontend, backend, and upstream/downstream systems agree on?” `02-api-contract.md` is the human-review authority; add `02-openapi.yaml` only for REST machine/tool consumption. G2 is confirmed only when critical semantics and ownership are agreed or an affected capability is explicitly blocked/out of scope.

Cover REST method/path, permission/data scope, request/response, pagination/sorting, validation, errors, idempotency, and compatibility. Cover events with channel, envelope, identifier, full/incremental behavior, initial read, reconnect, fallback, isolation, ordering, and deduplication. Cover device/cross-service owner, producer, consumer, topic or identifier, deployment dependency, and failure responsibility.

State separately: HTTP success, platform acceptance, publication, adapter dispatch, device execution, and state convergence. Phase 2 OpenAPI enables early Apifox alignment; implementation later exposes Runtime OpenAPI; Phase 4 compares runtime output with the approved Contract before any Apifox synchronization.
