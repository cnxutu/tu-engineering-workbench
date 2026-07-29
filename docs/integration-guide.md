# Integration Guide

This guide describes a repository integration model; it does not implement a resolver, knowledge graph, MCP server, or `ai-guidance init` command.

## Bind a repository

1. Copy [AGENTS.md.template](../bootstrap/AGENTS.md.template) into the repository as `AGENTS.md` and adapt local instruction paths.
2. Copy [repository-manifest.template.yaml](../bootstrap/repository-manifest.template.yaml), bind it to one product, and keep its product manifest and index paths consistent.
3. Configure the guidance root with `AI_GUIDANCE_HOME` or an explicit repository configuration (for example `.ai-guidance.yaml`). An explicit configuration may select a non-default manifest path.
4. For bootstrap reads, resolve `AI_GUIDANCE_HOME` or explicit configuration, read the repository manifest binding, load the product index, load task-specific Core material, then load remaining local instructions and current code.

Semantic precedence is independent of this read sequence: local repository instructions and code > product guidance > Core guidance.

Future `ai-guidance init` tooling may automate these copies and configuration checks; it should produce the same explicit binding rather than inventing product facts.

## Resolver contract

A future resolver should locate guidance in this order: explicit configuration, `AI_GUIDANCE_HOME`, then an installation default. It should return the bound repository manifest, product manifest, and product index, and report ambiguous or missing bindings instead of guessing. The [repository manifest contract](../core/contracts/repository-manifest.schema.yaml) documents the expected fields.

## Knowledge graph and MCP Context Server

Future tooling may expose documents, repositories, services, contracts, evidence, ADRs, and tasks as nodes with typed links. A future MCP Context Server could use that graph to answer targeted context requests, return evidence and staleness status, and recommend the next document for progressive loading. Neither facility is implemented by these templates or documents; repository manifests remain the portable source of truth.

## Verification

Before publishing an integration, verify paths, Markdown links, YAML structure, product binding, and that no sensitive data was introduced. For cross-service changes, also record the product knowledge update assessment.
