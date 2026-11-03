# F05: Tool system and permissions

- Priority: P0
- Status: Not started
- Summary: Provide tool system and permissions through bounded, audited, vendor-neutral contracts.

## Behaviour

1. Owner initiates tool system and permissions through the configured interface.
2. Core validates configuration, applies safety and profile policy, then invokes the documented component boundary.
3. Core presents a concise result through available text, HUD, or speech channel.
4. Failure branch: invalid input, unavailable dependency, timeout, or denied policy produces no unsafe side effect, uses bounded failover/degraded behavior, and records a redacted event.

## Sequence flow

1. Accept request and create request ID.
2. Validate input/configuration and classify any untrusted content.
3. Execute the required component/tool contract inside its timeout.
4. Apply permission/approval when an action has effects.
5. Return normalized result, audit it, and update HUD state.
6. Failure branch: cancel work, retry only under shared bounded failover rules, then give the owner a concise status.

## Tools / Components involved

Tool registry, permission gate, orchestrator, audit log. [components catalog](../01-architecture/components-and-contracts.md), [orchestrator](../01-architecture/components/orchestrator.md), [permission gate](../01-architecture/components/permission-gate.md). [tool manifest specification](../01-architecture/tool-manifest-spec.md).

## Requirements

| ID | Requirement | Verification |
|---|---|---|
| FEAT-05-001 | Tool system and permissions must follow the request lifecycle, fixed risk levels, and active profile before any effect occurs. | Integration test. |
| FEAT-05-002 | Tool system and permissions must emit a redacted audit result for success, denial, timeout, and failure. | Safety test. |

## Edge cases

- [ ] empty input is rejected without tool use.
- [ ] adapter timeout fails over once then degrades.
- [ ] duplicate trigger receives one request ID.
- [ ] interruption cancels cancellable work.
- [ ] rate limit never creates retry loop.
- [ ] invalid provider output is rejected.
- [ ] audit sink failure does not repeat an action.
- [ ] safe mode preempts the request.

## Tests

- [ ] Unit: validate feature-specific input and configuration rules.
- [ ] Contract: validate dependent interface envelopes and error mappings.
- [ ] Integration: exercise normal and failover/degraded sequence.
- [ ] Safety: verify denial, escalation, and redacted audit behavior.
- [ ] Manual: confirm the user-visible feedback and profile behavior.

## Done when

- [ ] Requirements FEAT-05-001 and FEAT-05-002 pass their stated verification.
- [ ] All listed edge cases and test layers pass.
- [ ] Feature is linked from the checklist and audit evidence is reviewable.

## Dependencies

- Depends on [F05](F05-tool-system-and-permissions.md), [F20](F20-profiles-and-setup.md), and Phase 2.
- See [CHECKLIST Phase 2](../06-checklist/phase-2.md).

## Related docs

- [Feature index](feature-index.md)
- [Request lifecycle](../01-architecture/request-lifecycle.md)
- [Threat model](../03-security/threat-model.md)
- [Checklist](../06-checklist/CHECKLIST.md)

## Open questions

- Which owner-facing defaults best fit tool system and permissions? TO VERIFY.

## Change log

- 2026-11-03: Completed Part 6 feature specification.
