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

### 2. Evidence ladder

1. **Runtime state** — existence, running/health, restart count, exit code, start/finish timestamps, OOMKilled, and restart
   policy. This answers what the service is doing now.
2. **Targeted logs** — a small time window and the target service, filtered by a safe correlation key such as traceId,
   deviceSn, requestId, taskId, messageId, or timestamp. Prefer stdout and the service's high-priority error source; never
   default to copying all Docker logs or business payloads.
3. **Trace/correlation** — consult the product observability and framework-provenance pages. Verify the boundary before
   joining records: HTTP, Feign, async, RocketMQ, MQTT, WebSocket, and TCP may preserve, rebuild, or omit context.
4. **Dependency/middleware** — inspect Nacos, Redis, MySQL, RocketMQ, MQTT/EMQX, ZLMediaKit, network, or DNS only when
   preceding evidence points to that dependency.
5. **Code/framework** — map the runtime unit to repository/module/class/config. Load shared framework context only to
   explain an observed behavior; distinguish business code, framework capability, runtime configuration, and middleware.

### 3. Output and stop conditions

Use concise, sanitized evidence pointers (command/source and time window), not bulk payloads. Separate direct facts from
inferences and unknowns. Stop with `Root Cause Confirmed` only when symptom → runtime evidence → implementation/configuration
reason is closed. Use `Most Likely Cause` for a supported mechanism that lacks its trigger. Use `Insufficient Evidence`
when a required host, deployment, or cross-boundary signal is unavailable, and name the next evidence to obtain.

Keep diagnosis separate from fix: report finding, impact, evidence, and recommended action; do not restart, deploy, edit
configuration, write data, or clean a host without a later explicit authorization.

## Case 001 fixture (sanitized)

Subject: `c-iot-gateway` in `company-dev`.

- **Facts:** container status `exited`; exit code `143`; `OOMKilled=false`; restart count `0`; restart policy
  `unless-stopped`; recent sampled logs show no startup-failure or OOM evidence.
- **Evidence:** read-only Docker inspect and bounded log sampling from the Runtime Context case; source maps the logical
  service to `c-iot-gateway`.
- **Hypothesis:** exit code `143` is consistent with a process receiving `SIGTERM`.
- **Unknown:** which actor or operation sent the termination signal.
- **Next Evidence:** Docker daemon/system journal around stop time, host reboot/uptime evidence, and deployment/compose
  operation evidence, subject to access and secret filtering.
- **Diagnosis:** `Most Likely Cause` — graceful termination mechanism (`SIGTERM`); trigger is
  `Insufficient Evidence`. No restart or other mutation is implied.

## Static routing scenarios

- `P2 E` + message-processing problem: remain on the ordinary incident path; do not force Runtime Context.
- `P3 ssh 150 E` + device-offline problem: enter this runtime-aware branch without binding tests to a real host.
- `ssh 999`: stop at context resolution with `Runtime shortcut not configured`.
- A stopped service: emit the six-field runtime contract and do not restart it.

## Future limitation

Runtime-to-exact-Git-commit mapping is not currently guaranteed. Images/containers should eventually expose sanitized OCI
revision/version/source labels or Spring `git.properties` / `build-info.properties`; this is backlog only and is not a
Phase 2 implementation change.
