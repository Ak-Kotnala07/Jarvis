# Startup and shutdown

Purpose: define ordered initialization, readiness, failure handling, and recovery policy.

## Requirements

| ID | Requirement | Verification |
|---|---|---|
| ARCH-026 | Startup must initialize components in documented order and must not accept triggers before readiness passes. | Integration test. |
| ARCH-027 | Startup failures must be fatal only when no safe degraded path exists. | Fault-injection test. |
| ARCH-028 | Boot retries for unavailable audio or network must be bounded and must not busy-loop. | Retry test. |
| ARCH-029 | Core must prevent duplicate active instances before binding resources or accepting triggers. | Integration test. |
| ARCH-030 | Graceful shutdown must follow documented order and crash restart must not repeat unfinished external actions automatically. | Crash/shutdown test. |

## Ordered startup

| Order | Component | Failure behavior | Readiness check |
|---:|---|---|---|
| 1 | Config | Fatal if invalid/unreadable. | Profile and required paths validate. |
| 2 | Logging | Fatal if no safe external runtime location. | Redacted audit sink available. |
| 3 | Safety | Fatal if permission gate unavailable. | Gate and allow-lists load. |
| 4 | Platform | Degraded if optional capability unavailable. | Supported OS capability check. |
| 5 | Adapters | Degraded if configured failover/local fallback exists; otherwise relevant feature unavailable. | Contract/configuration check. |
| 6 | Tools | Fatal only for required safety control; otherwise disable failed tool. | Manifest/schema validation. |
| 7 | Services | Degraded if optional service fails. | Service health check. |
| 8 | HUD server | Degraded; core continues. | Loopback bind and token readiness. |
| 9 | Trigger | Degraded to typed input if unavailable. | Trigger/audio availability check. |
| 10 | Greeting | Skip if disabled/unavailable. | Core already idle. |

Network or audio not ready at boot must use bounded backoff, update HUD/typed status, and retry only while core remains healthy. Exact retry count and delay are TO VERIFY.

## Duplicate-instance prevention

Before startup binds audio, trigger, or HUD resources, core must acquire one OS-appropriate instance lock. Failure to acquire it must notify the owner and exit without connecting providers or starting tools.

## Graceful shutdown and crash restart

1. Enter `shutting_down`; reject new requests and stop trigger acceptance.
2. Cancel capture, speaking, adapters, and tools within their cancellation bounds.
3. Close HUD sessions and invalidate session tokens.
4. Flush best-effort audit records, release instance lock, and exit.
5. After a crash, restart policy may restore idle services but must not replay requests, approvals, tool actions, or external sends automatically.
6. Recovered core must report degraded/crash state until readiness checks pass.

## Related docs

- [System overview](system-overview.md)
- [Process model](process-model.md)
- [State machine](state-machine.md)
- [F09](../02-features/F09-startup-greeting.md)
- [F10](../02-features/F10-autostart.md)

## Open questions

- Which startup controls are mandatory versus safely degradable? TO VERIFY.
- What crash-restart supervisor is appropriate per platform? TO VERIFY.

## Change log

- 2026-11-02: Added Part 3 startup and shutdown model.
