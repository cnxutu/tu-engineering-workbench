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
3. Apply the reviewed Product Truth Delta first, or record `knowledge_update_assessment: not-needed`.
4. Perform Sensitive Data Review before any Archive copy. On a sensitive finding, stop with `Sensitive Data Review Failed`, naming the file, finding type, and archive-blocking reason; do not redact silently, Archive, create a Closed Index, or retire active.
5. Require complete, valid `workspace.local.yaml` `external_contexts.tu_vault` configuration and resolve exactly `<delivery_archive_root>/<DF-ID>/`, with logical reference `tu-vault:<delivery_archive_root>/<DF-ID>`.
6. Copy the complete Package into that Unit's `delivery/`; leave the Workbench active source `status: active`. Finalize only archived `delivery/task.yaml` with final status, `archived_at`, `archive_reference`, and `closed_index`; then generate `summary.md` and `manifest.yaml`.
7. Verify manifest and archived task metadata agree on delivery ID, final status, closed time, and archive reference, and that every declared artifact exists. On re-run, inspect an existing Unit and continue from the first incomplete step instead of overwriting a complete, consistent archive.
8. Only after archive verification, create the Thin Closed Index; retire the Active Package last; then verify that Closed Index, manifest, and archived task metadata are consistent and no active/closed conflict remains.

Keep the active Package recoverable through every intermediate failure. Re-run from inspected filesystem state rather than chat memory: do not repeat an already verified archive or needless Product Truth update. Reopen restores/copies the immutable external archive into `work/active/`, resets its archive metadata and status to `active`, and never moves or deletes the Vault Unit; legacy local archive is only a compatibility fallback.
