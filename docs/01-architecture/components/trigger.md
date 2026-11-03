# Trigger

## Responsibility

Receive allowed wake-word, hotkey, or typed activation and emit a TriggerEvent. It must not capture indefinite audio, authorize actions, or invoke tools.

| ID | Requirement | Verification |
|---|---|---|
| ARCH-036 | Receive allowed wake-word, hotkey, or typed activation and emit a TriggerEvent. must satisfy this documented contract without widening its responsibility. | Contract test and review. |

## Contract

```text
wait(config: TriggerConfig) -> Result<TriggerEvent>
```

## Behaviour

Normal behavior: Receive allowed wake-word, hotkey, or typed activation and emit a TriggerEvent.
Edge cases and concurrency: Trigger events are serialized; rate-limited repeats are ignored.

## Errors and failover

TransientError: retry once; Unsupported: typed input remains available; user hears “Use typed input.”

## Config keys

trigger.enabled: boolean = true; trigger.hotkey: string; trigger.wake_word: string; exactly one enabled input is required in office profile.

## Logging and audit

Record trigger source and request ID; redact spoken content.

## Security requirements

- [SEC-012](../../03-security/threat-model.md#sec-012)
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

- 2026-11-02: Added Part 4 Trigger component contract.
