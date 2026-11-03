# Autostart

## Responsibility

Register or remove platform startup behavior through platform layer. It must not create persistence outside owner-approved configuration or bypass platform policy.

| ID | Requirement | Verification |
|---|---|---|
| ARCH-050 | Register or remove platform startup behavior through platform layer. must satisfy this documented contract without widening its responsibility. | Contract test and review. |

## Contract

```text
install(request: AutostartRequest) -> Result<AutostartResult>; remove() -> Result<AutostartResult>
```

## Behaviour

Normal behavior: Register or remove platform startup behavior through platform layer.
Edge cases and concurrency: One mutation at a time; core remains functional without autostart.

## Errors and failover

Unsupported/AuthError: leave disabled; user hears “Autostart is unavailable.”

## Config keys

autostart.enabled: boolean = false; validate profile and platform support.

## Logging and audit

Record change, profile, and result; redact paths if sensitive.

## Security requirements

- [SEC-015](../../03-security/threat-model.md#sec-015)
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

- 2026-11-02: Added Part 4 Autostart component contract.
