# Audit log

## Responsibility

Append redacted security and lifecycle records to external runtime storage. It must not store secrets or block emergency shutdown.

| ID | Requirement | Verification |
|---|---|---|
| ARCH-048 | Append redacted security and lifecycle records to external runtime storage. must satisfy this documented contract without widening its responsibility. | Contract test and review. |

## Contract

```text
append(event: AuditEvent) -> Result<AuditReceipt>; verify() -> Result<IntegrityStatus>
```

## Behaviour

Normal behavior: Append redacted security and lifecycle records to external runtime storage.
Edge cases and concurrency: Append operations serialize; failure is surfaced but kill switch proceeds.

## Errors and failover

TransientError: one retry; integrity failure enters safe mode; user hears “Safety records need attention.”

## Config keys

audit.retention_days: integer = TO VERIFY; audit.max_size_mb: integer = TO VERIFY; validate external path.

## Logging and audit

Record schema per SEC-043 with argument redaction.

## Security requirements

- [SEC-009](../../03-security/threat-model.md#sec-009)
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

- 2026-11-02: Added Part 4 Audit log component contract.
