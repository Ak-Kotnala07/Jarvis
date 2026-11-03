# Scheduler

## Responsibility

Create and manage bounded local reminders and scheduled jobs. It must not execute arbitrary commands or bypass reminder permissions.

| ID | Requirement | Verification |
|---|---|---|
| ARCH-045 | Create and manage bounded local reminders and scheduled jobs. must satisfy this documented contract without widening its responsibility. | Contract test and review. |

## Contract

```text
create(request: ScheduleRequest) -> Result<ScheduleResult>; cancel(id: string) -> Result<null>
```

## Behaviour

Normal behavior: Create and manage bounded local reminders and scheduled jobs.
Edge cases and concurrency: Single scheduler owner; job execution re-enters permission gate if it has effects.

## Errors and failover

Timeout/TransientError: no infinite retry; user hears “That reminder could not be scheduled.”

## Config keys

scheduler.enabled: boolean = true; scheduler.max_jobs: integer = TO VERIFY; validate future schedule.

## Logging and audit

Record schedule ID, timing, and decision; redact reminder content when needed.

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

- 2026-11-02: Added Part 4 Scheduler component contract.
