# Runtime Diagnostic Procedure

This procedure is the runtime-aware branch of `tu-diagnosing-spring-backend-incidents`. It is an evidence workflow, not
permission to mutate a runtime.

## Procedure

```text
Problem
  ↓
Resolve scope (repository, ssh hint, stage, problem)
  ↓
Resolve Runtime Context (registry → local binding → product runtime pages/snapshot)
  ↓
Resolve diagnostic subject
  ↓
Establish Expected Runtime State for the environment and verification scenario
  ↓
Runtime state
  ↓
Targeted logs
  ↓
Trace/correlation (only where propagation is evidenced)
  ↓
Dependency/middleware (only when evidence points there)
  ↓
Repository → module → code/config → framework context when needed
  ↓
Facts → Evidence → Hypothesis → Unknown → Next Evidence → Diagnosis
```

### 1. Resolve scope and context

Parse the user message without inventing mappings. A Runtime Target Hint must resolve uniquely through
`core/registry/environments.yaml`, `runtime.local.yaml`, and the product runtime index. If it does not resolve, report
`Runtime shortcut not configured`. Do not guess an IP, SSH alias, environment, or repository. Read deployment,
observability, framework-provenance, and `.runtime.local/<environment>/` material only when the subject requires it.

When a stopped, unhealthy, absent, or replacement runtime unit affects a diagnosis or integration verification, establish
its Expected Runtime State before calling it a fault or recommending recovery. Deployment Intent (Compose, Helm,
deployment config, restart policy, or service mapping) describes static capability and normal shape only. It must be
combined with the Environment Role and Current Operational Intent for the requested scenario. If either dynamic fact is
unknown, report `Need Human Context`; do not infer that the unit should start, restart, deploy, or be replaced.

### 2. Evidence ladder

1. **Runtime state** — existence, running/health, restart count, exit code, start/finish timestamps, OOMKilled, and restart
   policy. This answers what the service is doing now.
2. **Targeted logs** — a small time window and the target service, filtered by a safe correlation key such as traceId,
   deviceSn, requestId, taskId, messageId, or timestamp. Prefer stdout and the service's high-priority error source; never
   default to copying all Docker logs or business payloads.
3. **Trace/correlation** — consult the product observability and framework-provenance pages. Verify the boundary before
   joining records: HTTP, Feign, async, RocketMQ, MQTT, WebSocket, and TCP may preserve, rebuild, or omit context.
4. **Dependency/middleware** — inspect Nacos, Redis, MySQL, RocketMQ, MQTT/EMQX, ZLMediaKit, network, or DNS only when
   preceding evidence points to that dependency. Before a provider check, look for the matching entry in
   `.runtime.local/<environment>/access.local.yaml`. If it is absent, emit
   `Runtime access not configured for <dependency>` and stop at **Next Evidence**; never guess or request a credential
   value in output. An entry's `privilege` (`readonly` or `elevated`) describes the credential's possible capability,
   not authorization for the diagnostic: both remain read-only by default.
5. **Code/framework** — map the runtime unit to repository/module/class/config. Load shared framework context only to
   explain an observed behavior; distinguish business code, framework capability, runtime configuration, and middleware.

### 3. Output and stop conditions

Use concise, sanitized evidence pointers (command/source and time window), not bulk payloads. Separate direct facts from
inferences and unknowns. Stop with `Root Cause Confirmed` only when symptom → runtime evidence → implementation/configuration
reason is closed. Use `Most Likely Cause` for a supported mechanism that lacks its trigger. Use `Insufficient Evidence`
when a required host, deployment, or cross-boundary signal is unavailable, and name the next evidence to obtain.

Keep diagnosis separate from fix: report finding, impact, evidence, and recommended action; do not restart, deploy, edit
configuration, write data, or clean a host without a later explicit authorization. Do not echo credentials, put them in
logs/snapshots/Product Truth, or print complete credential-bearing connection strings; report only sanitized status such as
`MySQL access: configured`.

For any state-changing action (`start`, `restart`, `stop`, `deploy`, `redeploy`, `scale`, `clear`, `delete`, `migrate`, or
runtime configuration change), confirm in order: Environment Role, Current Operational Intent, Expected Runtime State,
and an actual state violation; then obtain Human Approval for the precise action. A stopped unit may be `Fault`,
`Normal`, `Not Applicable`, or `Unknown` depending on those facts.

When an executor cannot obtain a required signal because of permission, SSH, network, Runtime policy, or side-effect
approval, stop the inference and request the smallest sanitized `Need Evidence`. Human-provided evidence or operational
intent may continue the same diagnostic chain; do not bypass the executor constraint.

## Sanitized stopped-service example

- **Facts:** a service is stopped; inspect and bounded logs establish its immediate lifecycle evidence.
- **Required context:** Deployment Intent, Environment Role, and Current Operational Intent for the requested scenario.
- **Verdict:** report `Fault` only when the stopped state violates the established Expected State; otherwise report
  `Normal`, `Not Applicable`, or `Unknown` / `Need Human Context`.
- **Action boundary:** no restart or other mutation is implied by lifecycle evidence alone.

## Static routing scenarios

- `P2 E` + message-processing problem: remain on the ordinary incident path; do not force Runtime Context.
- `P3 ssh <configured-shortcut> E` + device-offline problem: enter this runtime-aware branch without binding tests to a real host.
- `ssh <unconfigured-shortcut>`: stop at context resolution with `Runtime shortcut not configured`.
- A stopped service: emit the six-field runtime contract, establish Expected State, and do not restart it.
- Dependency access missing: emit `Runtime access not configured for <dependency>` and stop at `Next Evidence`.
- `readonly` and `elevated` access: diagnostic operations remain read-only in both cases.

Local Runtime Access V1 is limited to Dev/Test. Production credentials are not supported; production diagnosis requires
a separate policy, audit, approval, isolation, and operation-logging review.

## Future limitation

Runtime-to-exact-Git-commit mapping is not currently guaranteed. Images/containers should eventually expose sanitized OCI
revision/version/source labels or Spring `git.properties` / `build-info.properties`; this is backlog only and is not a
Phase 2 implementation change.
