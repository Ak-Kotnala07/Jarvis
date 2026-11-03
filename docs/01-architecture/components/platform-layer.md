# Platform layer

## Responsibility

Provide isolated OS-specific capabilities to approved callers. It must not contain provider logic, tool policy, or cross-platform assumptions outside its package.

| ID | Requirement | Verification |
|---|---|---|
| ARCH-049 | Provide isolated OS-specific capabilities to approved callers. must satisfy this documented contract without widening its responsibility. | Contract test and review. |

## Contract

```text
capability(request: PlatformRequest) -> Result<PlatformResult>; healthcheck() -> Result<Health>
```

## Behaviour

Normal behavior: Provide isolated OS-specific capabilities to approved callers.
Edge cases and concurrency: Platform calls serialize when OS resource requires it.

## Errors and failover

Unsupported: disable capability; user hears available alternative.

## Config keys

platform.enabled_capabilities: string[]; reject unsupported OS/capability.

## Logging and audit

Record capability and redacted result; never log credentials.

## Security requirements

- [SEC-025](../../03-security/permission-levels.md#sec-025)
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

- 2026-11-02: Added Part 4 Platform layer component contract.
