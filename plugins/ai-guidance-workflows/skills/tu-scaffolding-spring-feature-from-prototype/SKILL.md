---
name: tu-scaffolding-spring-feature-from-prototype
description: Use when a user provides a product prototype URL, image, screenshot, or annotated wireframe and wants Codex to autonomously turn it into a Spring Boot backend design and implementation, including API contracts, database changes, persistence models, layered code, basic business logic, Swagger/OpenAPI annotations, and an Apifox-ready interface definition.
---

# Scaffolding a Spring Feature from a Prototype

Turn prototype evidence into a repository-conformant Spring Boot feature through one fixed workflow. Keep invocation lightweight: the user supplies the prototype source and may add a one-line goal; carry the engineering constraints, discovery steps, confirmation gate, implementation, and verification inside this skill.

## Accept minimal input and start

Require only a prototype source: an accessible URL, attached image, or local image path. Treat a one-line goal and target project/module as optional hints.

1. Open or inspect the prototype immediately with the available browser, connector, or image-reading capability. Follow an accessible prototype link instead of asking the user to restate its visible contents.
2. Infer the target repository and module from the active workspace, current project scope, prototype terminology, and comparable code. If exactly one target is not identifiable, ask one focused target question; do not request a full task template.
3. Infer operations, non-goals, acceptance behavior, project conventions, and verification commands from the prototype and current repository evidence. Do not ask the user to repeat `c/r/p/v` fields or the rules already encoded here.
4. Default to the full workflow: analyze, inspect the repository, present the decision preview, implement after the required decision, then verify. Stop after the preview only when the user explicitly requests design-only output.
5. If the prototype source cannot be accessed or read, state the exact access problem and request only the smallest replacement, such as a shareable URL or the affected screenshot.
6. Read the target repository and nearest `AGENTS.md`. When P0 is primary, also read `ai-guidance/AGENTS.md`, `core/rules/development.md`, `core/skills/feature-development.md`, and the Java, architecture, and database rules it references.

## Extract prototype evidence

1. Read every supplied prototype image at a usable resolution. Establish page order and group list, detail, create, edit, and state-action views.
2. Extract visible fields, actions, filters, pagination, sorting, labels, required markers, defaults, enum options, help text, and page relationships.
3. Build traceability from prototype location to UI field, API field, persistence field, rule, and evidence status. Use [prototype-extraction-checklist.md](references/prototype-extraction-checklist.md).
4. Separate **verified prototype evidence**, **verified repository convention**, **inference**, and **open decision**. Do not infer authorization, tenant scope, delete semantics, uniqueness, state transitions, concurrency, idempotency, cascades, or audit behavior from UI appearance alone.
5. If an image is missing or illegible, identify the exact missing region and continue with unaffected evidence. Do not invent its contents.

## Verify repository conventions

Inspect the smallest relevant set of current code, configuration, migrations, tests, and generated API output. Find at least one comparable feature when available and verify:

- Controller routing, response envelope, pagination, validation, authorization, and exception conventions.
- Request DTO, response VO, entity/DO, conversion, service, and Mapper/Repository boundaries.
- ORM, entity base class, identifiers, tenant fields, audit filling, logical deletion, optimistic locking, and naming rules.
- Migration location and naming; column types, defaults, constraints, indexes, and compatibility practices.
- Swagger/OpenAPI library and annotation version, schema conventions, enum representation, and documentation endpoint.

Prefer those verified conventions over generic three-layer boilerplate. Do not expose persistence entities as public request or response models unless the repository has an explicit, justified convention requiring it.

## Produce the design preview

Use [design-preview-format.md](references/design-preview-format.md) and keep it proportional to the feature. Include:

1. Scope, non-goals, and evidence sources.
2. Prototype-to-contract traceability.
3. Endpoint inventory with method, path, authorization, request, response, and error semantics.
4. Request/response schema details: type, requiredness, validation, enum values, examples, and compatibility notes.
5. Database changes: tables/columns, keys, constraints, indexes, audit/delete behavior, migration and rollback boundary.
6. Basic business flow and key failure paths.
7. Confirmed decisions, low-risk repository-derived assumptions, and blocking open decisions.
8. Expected files and verification plan.

Treat an explicit, current, user-approved API/database specification as satisfying the decision gate. Otherwise ask only about decisions that materially change behavior, public contracts, data semantics, security, or scope. Batch related blocking decisions into one concise confirmation. Resolve low-risk details from verified repository conventions and do not turn minor naming choices into approval gates.

## Implement the confirmed feature

1. Implement the smallest confirmed behavior using the comparable feature and existing abstractions.
2. Create only the layers actually used by the target repository. Typical outputs may include Controller, request DTOs, response VOs, Service/ServiceImpl, Mapper/Repository, entity/DO, converters, migration SQL, exceptions, and tests.
3. Keep protocol adaptation and validation in the Controller boundary, business rules in the service/application layer, and persistence details in the repository layer.
4. Implement CRUD operations only when supported by the confirmed contract. Preserve authorization, tenancy, logical deletion, auditing, transaction, pagination, and error conventions.
5. Add Swagger/OpenAPI annotations to the API and schema models using the project's installed library. Document summaries, descriptions, requiredness, formats, enum values, examples, and response shapes accurately; keep Bean Validation and documentation consistent.
6. Do not add speculative abstractions, future-proof fields, silent fallbacks, fake business rules, or unrelated refactors.

## Verify the deliverable

Use [delivery-verification-checklist.md](references/delivery-verification-checklist.md).

1. Run affected tests, static checks, and the smallest relevant build.
2. Verify normal behavior and key failures such as validation, not-found, conflict, and unauthorized access when applicable.
3. Generate or inspect the application's actual OpenAPI document when feasible. Confirm every designed endpoint and schema appears with the correct method, path, fields, requiredness, enum representation, and response wrapper.
4. Review the migration for compatibility, constraints, indexes, repeatability expectations, rollback boundary, and accidental destructive behavior. Do not execute a migration against an external environment without explicit authorization.
5. Review the final diff for unrelated changes, generated artifacts, and sensitive information.
6. Report actual verification output and remaining gaps. Do not claim Apifox readiness solely because annotations compile.

## External delivery boundary

Produce an Apifox-ready Swagger/OpenAPI contract, but do not upload, overwrite, or publish to Apifox unless the user explicitly requests that external action and the required integration is available. If upload remains manual, provide the verified OpenAPI endpoint or artifact and state exactly what was verified locally.

## Output contract

For design preview mode, return: **scope and evidence; traceability; API design; data design; business flow; decisions and unknowns; implementation boundary; verification plan.**

For implementation mode, return: **implemented scope; confirmed contract; files and behavior changed; database impact; OpenAPI verification; tests/build results; unverified items and residual risks.**
