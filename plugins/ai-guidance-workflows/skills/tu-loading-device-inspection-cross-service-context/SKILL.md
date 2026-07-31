---
name: tu-loading-device-inspection-cross-service-context
description: Use when a device-inspection task spans P1–P4, or requires understanding service responsibilities, upstream/downstream flows, MQTT, OSD, DJI protocol, commands, data ownership, or a cross-service contract before design or implementation.
---

# Loading Device Inspection Cross Service Context

Load the smallest verified P1–P4 context needed to explain a cross-service change. Product documents navigate the investigation; code, contracts, configuration, and tests establish current behavior.

## Scope decision

Use this Skill only when repositories interact through an API, message, shared data responsibility, protocol, or end-to-end release dependency. For a local P1 or P4 change with no such relationship, read only that repository's local guidance and code.

When the user names P1 and P2 but does not describe an interaction, do not automatically load P3/P4. Ask whether the repositories share an affected boundary, or investigate each stated scope independently.

## Context loading workflow

1. Read `ai-guidance/AGENTS.md`, identify the explicit project scope, and resolve paths through `workspace.local.yaml`. P0 supplies guidance and product knowledge; it is not automatically a code-change participant.
2. Read the device-inspection product `index.md`, then load only the maintained Flow or repository entry page that matches the requested boundary. If the product knowledge package does not cover that boundary, use target-repository code, contracts, configuration, and tests instead of inferring product facts.
3. Select flow documents by task signal:
   - DJI OSD, State, or DRC data upstream: `flows/dji-osd-upstream-flow.md`
   - DJI control, task, or DRC command downstream: `flows/dji-osd-command-flow.md`
   - P1 business command routing or IoT upstream consumption: `repositories/c-drone-inspection/key-entry-points.md`
   - P1 OSD/DRC snapshots, topology, running-task, or DRC session semantics: `repositories/c-drone-inspection/cache-design.md`
   - P2 upstream subscription, Data Rule, RocketMQ delivery, or an upstream message missing in P1: `repositories/c-iot-server/message-bridge-and-data-rule.md`
   - P2 device lookup, Thing Model, TSL, downstream service invocation, routing, or synchronous result semantics: `repositories/c-iot-server/device-thing-model-tsl.md`
   - P3 protocol instance, multi-protocol access, `protocolCodecId`, or P4 adapter integration: `repositories/c-iot-gateway/protocol-instance-and-codec-selection.md`
   - P3 upstream forwarding, downstream subscription, connection, MQTT publication, or reply-mode handling: `repositories/c-iot-gateway/gateway-upstream-downstream-bridge.md`
   - P4 DJI Topic, payload field, identifier, command, or service-reply mapping: `repositories/ad-iot-codec-adapter-dji/dji-adapter-mapping.md`
   - device online/state, generic MQTT or protocol, inspection task, video/media, or another uncovered boundary: do not infer a product Flow; start from the affected repository's code and contracts.
4. For each affected repository, read its local `AGENTS.md`, repository entry map, then only the code, contract, configuration, and tests that implement the selected boundary.
5. Treat every document-derived service responsibility, Topic, DTO, cache semantic, or release dependency as a hypothesis until current code or configuration confirms it. Do not invent class names, topics, or message schemas.

## Output contract

Return: **scope and non-goals; service responsibilities; verified upstream/downstream sequence; affected contracts and data ownership; evidence and unknowns; repository-level change candidates; release and rollback dependencies; validation plan.** Use a sequence diagram only when it clarifies the chain more than concise prose.

## Do not use

Do not use for an isolated single-repository change with no affected service boundary, or to load all P1–P4 material merely because multiple project identifiers appear in an example or quoted text.
