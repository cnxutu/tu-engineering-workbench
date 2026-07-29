# Authoring Guide

Write guidance for the next engineer who must decide what to load and what can be trusted.

## Product documents

Start each product at `index.md`. It should state scope, evidence posture, and links to the smallest useful domain, architecture, flow, repository, and decision documents. Keep Core generic: it provides methods and templates, not product facts. Put product-specific facts in the product tree and bind repositories through manifests.

Use progressive loading: link rather than duplicate detail, and keep each document focused on one concern. State an owner or source when it clarifies authority. The normal precedence is local repository instructions and code, then product guidance, then Core guidance.

## Facts and citations

For every material product claim, state its evidence and confidence. Prefer stable links to source, tests, contracts, or approved design records. Label a target architecture as a target; it does not prove current code behavior. Use `pending_verification` and `unknown` plainly instead of guessing.

Before completing work that introduces a cross-service fact, assess whether service maps, ownership, contracts, topology, or flows need revision. Update the applicable document when evidence supports it and record the outcome in task metadata.

## Records

Use the contracts in [Core](../core/contracts/) as documentation contracts, not executable validators. Keep task records concise and archive final records under the product's `tasks/archive/`. Use ADRs for durable architectural decisions, and redact sensitive information before adding evidence.

For repository setup, follow the [integration guide](integration-guide.md).

