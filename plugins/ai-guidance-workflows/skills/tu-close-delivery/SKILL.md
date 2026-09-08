---
name: tu-close-delivery
description: Use when a user explicitly asks to close, finalize, or archive a named DF-YYYYMMDD-NN Delivery.
---

# Close a Delivery

Perform the user-authorized Delivery Closing transaction. Read the [Delivery Closing Playbook](../../../../core/playbooks/delivery-closing.md) before any mutation; it is the authoritative method and archive contract.

## Trigger and boundary

Act only when the request has both an explicit closing intent and a canonical Delivery ID. Do not infer authorization from a passed Verify, completed DEV/BUG, G4, a readiness assessment, or a status question. If the request lacks either condition, report the missing authorization or ID and stop.

The explicit request authorizes only the named Delivery's minimal Product Truth update, configured `tu_vault` Archive Unit, Closed Index, and Active Package retirement. It does not authorize commit, push, release, deploy, production actions, Vault taxonomy changes, or changes to other Deliveries.

## Run the transaction

1. Inspect the active Package and form the Closing Assessment before changing files. If only a Closed Index exists, report Already Closed; do not archive again.
2. Select only `completed`, `blocked`, or `superseded`. Resolve a material status ambiguity before mutation; completed requires acceptance evidence, normally G4.
3. Reconcile the reviewed final Product Truth Delta first. Compare the Delivery's final verified facts with relevant Current Product Truth already represented in `products/`; do not depend on tracking prior `S` actions. Avoid duplicate conclusions, correct or remove facts invalidated by later work, and add only remaining current-worthy facts. Then set the Delivery-level `knowledge_update_assessment`: `updated` when this Delivery has current-worthy Product Truth Delta now correctly represented, even if Closing makes no documentation change; `not-needed` only when the final Delivery has no current-worthy Product Truth Delta. Do not finalize Closing with `deferred` when final assessment is incomplete.
4. Perform Sensitive Data Review before any Archive copy. On a sensitive finding, stop with `Sensitive Data Review Failed`, naming the file, finding type, and archive-blocking reason; do not redact silently, Archive, create a Closed Index, or retire active.
5. Require a complete, valid local `workspace.local.yaml` `external_contexts.tu_vault.path` and the shared logical root from `core/registry/external-contexts.yaml`; resolve exactly `<delivery_archive_root>/<DF-ID>/`, with logical reference `tu-vault:<delivery_archive_root>/<DF-ID>`.
6. Copy the complete Package into that Unit's `delivery/`; leave the Workbench active source `status: active`. Finalize only archived `delivery/task.yaml` with final status, `archived_at`, `archive_reference`, and `closed_index`; then generate `summary.md` and `manifest.yaml`.
7. Verify manifest and archived task metadata agree on delivery ID, final status, closed time, and archive reference, and that every declared artifact exists. On re-run, inspect an existing Unit and continue from the first incomplete step instead of overwriting a complete, consistent archive.
8. Only after archive verification, create the Thin Closed Index; retire the Active Package last; then verify that Closed Index, manifest, and archived task metadata are consistent and no active/closed conflict remains.

Keep the active Package recoverable through every intermediate failure. Re-run from inspected filesystem state rather than chat memory: do not repeat an already verified archive or needless Product Truth update. Reopen restores/copies only immutable `<Archive Unit>/delivery/` as the Active Package under `work/active/`; it excludes `summary.md` and `manifest.yaml`, resets only the working copy's archive metadata, status to `active`, and `knowledge_update_assessment` to `deferred` regardless of its archived outcome, and never moves, deletes, or modifies the Vault Unit; legacy local archive is only a compatibility fallback.
