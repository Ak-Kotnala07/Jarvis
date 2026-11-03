# Settings

## Responsibility

Load, validate, and expose non-secret configuration and runtime-data paths. It must not load secrets into prompts or write runtime data into the repository.

| ID | Requirement | Verification |
|---|---|---|
| ARCH-047 | Load, validate, and expose non-secret configuration and runtime-data paths. must satisfy this documented contract without widening its responsibility. | Contract test and review. |

## Contract

```text
load(profile: string) -> Result<Settings>; validate(settings: Settings) -> Result<null>
```

## Behaviour

Normal behavior: Load, validate, and expose non-secret configuration and runtime-data paths.
Edge cases and concurrency: Immutable snapshot per request; reload only between requests.

## Errors and failover

InvalidResponse: fail startup or disable affected feature; user hears configuration status.

## Config keys

user: object; trigger: object; providers: object; sensitive_mode: boolean; paths/apps/shell/limits/greeting/hud/autostart; reject unknown unsafe values.

## Logging and audit

Record profile and validation errors; redact secret-like values.

## Security requirements

- [SEC-002](../../03-security/threat-model.md#sec-002)
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

- 2026-11-02: Added Part 4 Settings component contract.
