# Phase 1: Impact

The question is “what must change?” The authority is `01-impact-review.md`; G1 requires confirmed scope, high-level frontend behavior, disposition, and main responsibility boundaries.

Record scope and non-goals; source inventory and legibility; `CAP-xx`; a page/behavior-to-disposition table; repository and cross-service impact; REST/WS/MQTT/state effects; open decisions; risks and suggested slices. Classify each capability as `reuse`, `change`, `new`, `frontend_only`, `upstream_dependency`, `out_of_scope`, or `unknown`.

Evidence from a UI proves user intent, not authorization, data ownership, state transitions, wire values, persistence, or execution success. Examine target repositories and contracts before calling a capability reusable. Do not freeze a final API while material evidence is unknown.

Preferred providers: use `tu-analyzing-feature-impact` for Feature Impact. Use research, domain-modeling, or codebase-design only when available and model-invokable; otherwise adapt their method without bypassing invocation policy.
