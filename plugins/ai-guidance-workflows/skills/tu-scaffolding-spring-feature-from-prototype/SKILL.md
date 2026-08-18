---
name: tu-scaffolding-spring-feature-from-prototype
description: Use when a user provides a product prototype URL, image set, screenshot, exported PDF, or annotated wireframe and wants Codex to extract backend requirements, produce a Spring Boot API/data design, or implement the feature with repository-conformant contracts, database changes, layered code, business rules, tests, Swagger/OpenAPI annotations, and an Apifox-ready interface definition.
---

# Scaffolding a Spring Feature from a Prototype

Turn prototype evidence into a repository-conformant Spring Boot feature through one fixed workflow. Keep invocation lightweight: the user supplies the prototype source and may add a one-line goal; carry the engineering constraints, discovery steps, confirmation gate, implementation, and verification inside this skill.

## Accept minimal input and start

Require only a prototype source: an accessible URL, attached image or PDF, or local file path. Treat a one-line goal and target project/module as optional hints.

1. Open or inspect the prototype immediately with the available browser, connector, PDF, or image-reading capability. Follow an accessible prototype link instead of asking the user to restate its visible contents.
2. Establish a source inventory before interpreting details: source identifier, page/frame name, order, variant or revision when visible, and readable or missing regions. Do not treat a file name, page title, OCR output, or prototype annotation as sufficient visual evidence by itself.
3. Infer the target repository and module from the active workspace, current project scope, prototype terminology, and comparable code. If exactly one target is not identifiable, ask one focused target question; do not request a full task template.
4. Infer operations, non-goals, acceptance behavior, project conventions, and verification commands from the prototype and current repository evidence. Do not ask the user to repeat `c/r/p/v` fields or rules already encoded here.
5. Default to the full workflow: analyze, inspect the repository, present the decision preview, implement after the decision gate, then verify. Stop after the preview only when the user explicitly requests design-only output.
6. If a dynamic or authenticated prototype cannot expose its frames, request the smallest usable export, such as the affected screenshots or PDF. State the exact access or legibility problem instead of guessing from surrounding metadata.
7. Read the target repository and nearest `AGENTS.md`. When P0 is primary, also read `ai-guidance/AGENTS.md`, `ai-guidance/core/rules/development.md`, `ai-guidance/core/skills/feature-development.md`, and the Java, architecture, and database rules it references.

## Extract prototype evidence

1. Read every supplied page or frame at a usable resolution. For composite boards or dense screens, inspect both the full frame and targeted crops; use OCR only as an aid and verify its result against the pixels.
2. Establish page order and relationships among entry, list, detail, create, edit, dialog, confirmation, and state-action views. Reconcile desktop/mobile variants, repeated components, and before/after states instead of counting each frame as an independent feature.
3. Extract visible fields, actions, filters, pagination, sorting, labels, required markers, displayed values, placeholders, defaults, enum labels, help text, loading/empty/error states, and conditional visibility.
4. Distinguish literal labels, example records, placeholders, design annotations, and confirmed defaults. Do not convert sample text into a default, a display label into a stable code, or a disabled control into an authorization rule without supporting evidence.
5. Compare repeated fields and actions across screens. Record contradictions in naming, requiredness, option sets, editability, state, and success/failure behavior; do not silently choose one frame as authoritative.
6. Build traceability from prototype location to UI field/action, backend disposition, API field or endpoint, persistence field, rule, and evidence status. Account explicitly for frontend-only, computed, joined, or unknown elements. Use [prototype-extraction-checklist.md](references/prototype-extraction-checklist.md).
7. Separate **verified prototype evidence**, **verified repository convention**, **inference**, and **open decision**. Do not infer authorization, tenant scope, delete semantics, uniqueness, state transitions, concurrency, idempotency, cascades, audit behavior, time-zone policy, monetary precision, upload lifecycle, or enum wire values from UI appearance alone.
8. If an image is missing or illegible, identify the exact missing region and continue with unaffected evidence. Block only the contract or behavior that depends on the missing evidence.

## Translate UI evidence into backend semantics

1. Identify backend-affecting user outcomes before proposing endpoints. Do not create one endpoint per button, one request field per visible value, or one database column per table/detail item.
2. Classify each element as input, output, query criterion, command, navigation-only, presentation-only, computed, joined, or unresolved. Keep create, update, query, and response models asymmetric when the evidence requires it.
3. Resolve types and wire semantics from repository conventions and explicit evidence: identifier representation, enum codes versus labels, date/time and time zone, decimal precision and units, nullability, list ordering, upload/reference lifecycle, and pagination or sorting semantics.
4. Treat filters and search boxes as UI evidence that a query capability exists, not proof of exact match, fuzzy match, case sensitivity, combination logic, default sort, or index strategy.
5. Model state-changing actions as business commands or state transitions only after verifying allowed source states, target states, authorization, concurrency, idempotency, and failure behavior.
6. Run a coverage pass before the design preview: every in-scope page is inventoried; every backend-relevant field/action has a disposition; every contradiction and missing region is recorded; every material inference is either repository-verified or listed as a decision.

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

If no material open decision remains and the user requested implementation, continue without asking for ceremonial approval. If a material decision remains, do not implement the affected contract, migration, or security behavior until it is resolved; continue independent analysis and implementation where safe.

## Implement the confirmed feature

1. Implement the smallest confirmed behavior using the comparable feature and existing abstractions.
2. Create only the layers actually used by the target repository. Typical outputs may include Controller, request DTOs, response VOs, Service/ServiceImpl, Mapper/Repository, entity/DO, converters, migration SQL, exceptions, and tests.
3. Keep protocol adaptation and validation in the Controller boundary, business rules in the service/application layer, and persistence details in the repository layer.
4. Implement CRUD operations only when supported by the confirmed contract. Preserve authorization, tenancy, logical deletion, auditing, transaction, pagination, and error conventions.
5. Add Swagger/OpenAPI annotations to the API and schema models using the project's installed library. Document summaries, descriptions, requiredness, formats, enum values, examples, and response shapes accurately; keep Bean Validation and documentation consistent.
6. Preserve traceability in code review terms: each endpoint, public field, persistence change, validation rule, and state transition must map to prototype evidence, an approved decision, or a verified repository convention.
7. Do not add speculative abstractions, future-proof fields, silent fallbacks, fake business rules, or unrelated refactors.

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
