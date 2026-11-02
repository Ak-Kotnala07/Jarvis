# Process model

Purpose: define runtime ownership, concurrency, budgets, fault isolation, and shutdown behavior.

## Runtime ownership

| Unit | Runs where | Responsibility |
|---|---|---|
| Core process | One local process | State, queue, safety, registry, audit coordination. |
| Trigger/audio tasks | Core-managed async tasks | Triggers and bounded capture. |
| Adapter/tool tasks | Cancellable core-managed async tasks | Contract calls and one permission-gated action. |
| HUD server | Core-managed local service | Loopback WebSocket only. |
| HUD frontend | Separate optional process | Renders status; does not authorize core behavior. |

IPC is a `127.0.0.1` WebSocket protected by [SEC-040](../03-security/security-model.md#sec-040).

## Process requirements

| ID | Requirement | Verification |
|---|---|---|
| ARCH-010 | Core must own request state and must run without the HUD process. | Integration test. |
| ARCH-011 | Core must permit at most one active user request; later triggers must queue, reject, or barge-in only by documented transition. | State-machine test. |
| ARCH-012 | Owner interruption must cancel speaking and pending cancellable work before becoming active. | Integration test. |
| ARCH-013 | Adapter and tool work must be cancellable and bounded by configured timeouts. | Timeout test. |
| ARCH-014 | HUD crash or disconnect must not stop core, safety, or active request handling. | Integration test. |
| ARCH-015 | Core crash must stop child work and require documented restart policy before accepting requests. | Crash test. |
| ARCH-016 | Adapter hang must cancel at timeout, record failure, then use configured failover or degraded mode without indefinite waiting. | Timeout/failover test. |
| ARCH-017 | Idle CPU and RAM must remain within approved non-functional targets; no approved values exist yet, so targets are TO VERIFY. | Profiling test. |
| ARCH-018 | Shutdown must reject new requests, cancel bounded work, stop capture, close IPC, and flush best-effort audit records. | Shutdown test. |

## Concurrency rules

1. One request is active at a time.
2. A trigger while active is queued only when queueing is enabled; otherwise it is rejected with feedback.
3. Owner barge-in cancels speech first, then cancellable adapter/tool work.
4. Tool calls are sequential inside a request until safe parallelism is separately designed.
5. An approval pauses only its own request and cannot authorize queued work.
6. Safe mode, mute, shutdown, and kill switch preempt normal queue processing.

## Failure behavior and budgets

| Condition | Behavior |
|---|---|
| HUD crashes | Disconnect, audit, and continue core without HUD. |
| Core crashes | Stop child work; crash-restart policy governs recovery. |
| Adapter hangs | Cancel at timeout; fail over or enter degraded state with concise feedback. |
| Audio/network unavailable at boot | Bounded retry; offer typed/local fallback; do not spin. |
| Idle CPU/RAM | TO VERIFY from non-functional requirements. |
| Tool concurrency | One active tool action per request. |
| Queue depth | TO VERIFY; overflow must fail soft and audit. |

## Shutdown behavior

Shutdown is ordered in [startup and shutdown](startup-shutdown.md). It has priority over normal work; incomplete audit flushing must not block a safe exit.

## Related docs

- [System overview](system-overview.md)
- [State machine](state-machine.md)
- [Startup and shutdown](startup-shutdown.md)
- [Request lifecycle](request-lifecycle.md)
- [F21](../02-features/F21-interruption.md)
- [Safe mode](../03-security/safe-mode.md)

## Open questions

- What idle CPU/RAM targets are approved? TO VERIFY.
- Should queued triggers be retained or rejected by default? TO VERIFY.
- Which actions can ever run safely in parallel? TO VERIFY.

## Change log

- 2026-11-02: Added Part 3 process and concurrency model.
