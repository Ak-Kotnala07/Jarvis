# Orchestrator

## Responsibility

Own request lifecycle, state machine, agent-loop limits, and adapter composition. It must not directly import adapters/tools, execute tools, or override safety decisions.

| ID | Requirement | Verification |
|---|---|---|
| ARCH-043 | Own request lifecycle, state machine, agent-loop limits, and adapter composition. must satisfy this documented contract without widening its responsibility. | Contract test and review. |

## Contract

```text
handle(event: Event) -> Result<ResponseEvent>; cancel(request_id: string) -> Result<null>
```

## Behaviour

Normal behavior: Own request lifecycle, state machine, agent-loop limits, and adapter composition.
Edge cases and concurrency: One active request; interruption follows state machine.

## Errors and failover

Timeout/loop limit: degrade; user hears concise status; all errors retain request ID.

## Config keys

limits.max_tool_calls_per_request: integer > 0; limits.request_seconds: integer > 0; providers failover lists required.

## Logging and audit

Record request ID, state transitions, bounded errors; redact transcript and secrets.

## Security requirements

- [SEC-010](../../03-security/threat-model.md#sec-010)
- See [permission controls](../../03-security/permission-levels.md) and [threat model](../../03-security/threat-model.md).

## Default adapter / swap candidates

Default adapter: none unless a core/platform boundary is stated in the catalog. Swap candidates: any implementation passing this contract and the shared conventions.

## Contract test requirements

`tests/contract/` must verify success envelope shape, each error taxonomy mapping, timeout/cancellation, configuration validation, redaction, and that behavior above is preserved for any adapter.

## Related docs

- [Components and contracts](../components-and-contracts.md)
- [System overview](../system-overview.md)
- [Request lifecycle](../request-lifecycle.md)

## Open questions

- What implementation-specific limits are appropriate without changing this contract? TO VERIFY.

## Change log

- 2026-11-02: Added Part 4 Orchestrator component contract.
