# Phase 3: Execution

The question is “how is the approved work sliced and executed?” `03-execution-backlog.md` is authority; G3 requires at least one executable vertical slice with complete inputs and verification.

Use only `EXT` for external confirmation/environment/device work, `DEV` for authorized code work, and `INT` for integration/acceptance. Each task includes Task ID, CAP, Type, Goal, Repository, Preconditions, Blocking dependencies, Relevant contract, Expected changes, Verification, Status, and Evidence.

Keep tasks small enough for a fresh context. A DEV task becomes ready only after required decisions, contract sections, samples, and dependencies are verified. Do not silently implement blocked semantics. Record actual changes, commands/results, residual risk, and the next action in the backlog and resume cache.

For non-trivial DEV work, use the Explore → Plan → Execute → Verify task loop. Do not bypass current authorization or the Delivery Gate/Artifact authority.

Provider strategy: adapt `to-tickets` methods for tracer bullets, vertical slices, and blocker edges. If mature `implement` is user-invoked, surface the ready DEV task and recommend explicit invocation. Prefer model-invokable TDD or code-review capabilities when applicable.
