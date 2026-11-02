# Request lifecycle

Purpose: specify the path from activation to spoken reply, including failures and agent-loop limits.

## Lifecycle requirements

| ID | Requirement | Verification |
|---|---|---|
| ARCH-019 | Each request must have a request ID from trigger acceptance through final audit result. | Integration test. |
| ARCH-020 | Each lifecycle step must detect failure and retry, fail over, or degrade without bypassing safety. | Fault-injection test. |
| ARCH-021 | The agent loop must enforce configured maximum steps, repeated-state detection, and bounded tool errors. | Loop test. |
| ARCH-022 | Tool failure must return structured error data and must not cause unbounded retries. | Tool-error test. |

## Ordered lifecycle

| Step | Normal path | Failure branch: detection → user feedback → log |
|---:|---|---|
| 1 | Trigger accepts wake word, hotkey, or typed request. | Invalid/rate-limited → ignore or typed fallback → trigger reason. |
| 2 | Core creates request ID and enters listening/typed state. | Duplicate/unavailable state → queue/reject → state decision. |
| 3 | Audio task captures bounded input. | Device unavailable/timeout → retry once or typed fallback → audio failure/duration. |
| 4 | STT transcribes audio. | Error/timeout → configured failover, then typed request → adapter/failover result. |
| 5 | Core validates transcript/context and classifies untrusted content. | Empty/unsafe/oversize → clarification/degrade → validation reason. |
| 6 | LLM proposes answer or tool action. | Error/rate limit → bounded failover/local fallback/degraded reply → provider result. |
| 7 | Agent loop validates proposal limits. | Repeated/limit → stop and explain → signature/step count. |
| 8 | Permission gate classifies action and escalation. | Denied/ambiguous/profile-disabled → no execution; explain → risk/decision. |
| 9 | Owner approves L2/L3 action. | Expired/ambiguous/no approval → default deny; explain → approval decision. |
| 10 | Tool executes within timeout. | Error/timeout → cancel, return bounded error → tool/result/duration. |
| 11 | Loop synthesizes final response. | LLM unavailable → local factual status/degrade → response failure. |
| 12 | TTS speaks; HUD reflects state. | TTS failure → retain text/use configured fallback → TTS result. |
| 13 | Core audits and returns idle/degraded. | Audit unavailable → best-effort error; do not repeat action → audit failure. |

## Agent-loop rules

1. The loop must use configured maximum steps; default is TO VERIFY.
2. The loop must detect repeated tool/action/state signatures and stop before equivalent repetition.
3. A tool error is data for one next bounded step, never permission for indefinite retry.
4. The loop must not invent tool names, parameters, approvals, or allow-list entries.
5. The loop must stop on safe mode, mute where applicable, shutdown, or kill switch.
6. Every proposal must return through [SEC-001](../03-security/threat-model.md#sec-001).

## Related docs

- [System overview](system-overview.md)
- [Process model](process-model.md)
- [State machine](state-machine.md)
- [Permission levels](../03-security/permission-levels.md)
- [F01](../02-features/F01-voice-loop.md)
- [F05](../02-features/F05-tool-system-and-permissions.md)

## Open questions

- What maximum steps meet latency and cost goals? TO VERIFY.
- What local reply is guaranteed if every LLM is unavailable? TO VERIFY.

## Change log

- 2026-11-02: Added Part 3 request lifecycle and failure branches.
