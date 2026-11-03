# Audio input

## Responsibility

Capture bounded audio after an accepted trigger. It must not transcribe, retain audio beyond policy, or choose providers.

| ID | Requirement | Verification |
|---|---|---|
| ARCH-037 | Capture bounded audio after an accepted trigger. must satisfy this documented contract without widening its responsibility. | Contract test and review. |

## Contract

```text
capture(request: CaptureRequest) -> Result<AudioFrame>; stop(request_id: string) -> Result<null>
```

## Behaviour

Normal behavior: Capture bounded audio after an accepted trigger.
Edge cases and concurrency: One capture per active request; device change stops capture.

## Errors and failover

TransientError: retry once; Timeout: stop and offer typed input; user hears “I could not hear that.”

## Config keys

audio.max_seconds: integer = TO VERIFY; audio.device_id: string|null; reject nonpositive duration.

## Logging and audit

Record device, duration, request ID; never log raw audio.

## Security requirements

- [SEC-011](../../03-security/threat-model.md#sec-011)
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

- 2026-11-02: Added Part 4 Audio input component contract.
