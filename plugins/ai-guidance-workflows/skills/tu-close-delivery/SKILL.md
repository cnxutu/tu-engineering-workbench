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
4. Require complete, valid `workspace.local.yaml` `external_contexts.tu_vault` configuration. Archive the complete Package into exactly one configured DF Archive Unit, perform Sensitive Data Review, and verify its contents and logical `tu-vault:<relative-path>` reference.
5. Only after archive verification, create the Thin Closed Index; retire the Active Package last; then verify that closed state is complete and no active/closed conflict remains.

Keep the active Package recoverable through every intermediate failure. Re-run from inspected filesystem state rather than chat memory: do not repeat an already verified archive or needless Product Truth update. Use external archive first for reopen context; legacy local archive is only a compatibility fallback.
