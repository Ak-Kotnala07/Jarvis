# State machine

Purpose: define request states, transitions, and HUD indicators.

## State requirements

| ID | Requirement | Verification |
|---|---|---|
| ARCH-023 | Core must expose exactly the documented state vocabulary to internal consumers and the HUD. | State-machine test. |
| ARCH-024 | State transitions must validate guards and record state-changing failures with request ID. | Test. |
| ARCH-025 | Safe mode, muted, and shutting_down must preempt normal request states. | Test. |

## States

| State | Meaning | HUD indicator |
|---|---|---|
| starting | Initializing dependencies and readiness checks. | Starting. |
| idle | Ready for next request. | Idle/ready. |
| listening | Capturing bounded audio. | Mic active. |
| transcribing | Converting captured audio to text. | Transcribing. |
| thinking | Preparing answer or tool proposal. | Thinking. |
| awaiting_approval | Waiting for L2/L3 decision. | Approval needed. |
| executing_tool | Running one approved tool. | Action and risk level. |
| speaking | Producing spoken response. | Speaking. |
| degraded | Serving with reduced capability. | Degraded and reason. |
| safe_mode | Restricted read-only operation. | Safe mode and disabled classes. |
| muted | Mic capture disabled. | Muted. |
| shutting_down | Rejecting work and closing resources. | Shutting down. |

## Transition table

| From | Event | Guard | To | Side effects |
|---|---|---|---|---|
| starting | readiness passed | required local controls ready | idle | Publish readiness. |
| starting | required startup failure | no safe degraded path | shutting_down | Audit fatal failure. |
| starting | optional failure | degraded path exists | degraded | Publish reason. |
| idle | accepted trigger | not muted/safe-mode restriction | listening or thinking | Create request ID. |
| listening | audio captured | capture valid | transcribing | Close capture. |
| listening | timeout/device error | retry unavailable | degraded | Offer typed input; audit. |
| transcribing | text ready | valid transcript | thinking | Classify untrusted content. |
| transcribing | adapter failure | failover unavailable | degraded | Offer typed input; audit. |
| thinking | answer ready | no tool needed | speaking or idle | Render/speak response. |
| thinking | tool proposed | permitted | awaiting_approval or executing_tool | Classify risk. |
| awaiting_approval | valid approval | approval matches request | executing_tool | Audit approver channel. |
| awaiting_approval | deny/expiry | any | thinking or idle | Return denial response. |
| executing_tool | result returned | within limits | thinking | Provide structured result. |
| executing_tool | error/timeout | any | thinking or degraded | Cancel; bounded error. |
| speaking | completed/cancelled | any | idle | Finalize audit. |
| any normal | safe-mode event | activation valid | safe_mode | Cancel prohibited actions. |
| safe_mode | owner exit | exit procedure complete | idle or degraded | Audit exit. |
| any except shutting_down | mute | any | muted | Stop capture. |
| muted | unmute | owner action | idle | Audit state. |
| any | shutdown/kill switch | any | shutting_down | Reject work; cancel resources. |

## Related docs

- [Request lifecycle](request-lifecycle.md)
- [Process model](process-model.md)
- [Safe mode](../03-security/safe-mode.md)
- [F11](../02-features/F11-hud.md)

## Open questions

- Should degraded remain a top-level state or state annotation? TO VERIFY.
- Which startup controls are required before idle? TO VERIFY.

## Change log

- 2026-11-02: Added Part 3 state machine.
