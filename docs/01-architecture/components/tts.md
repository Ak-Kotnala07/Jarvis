# TTS

## Responsibility

Convert approved reply text to playback. It must not decide content, capture mic, or invoke tools.

| ID | Requirement | Verification |
|---|---|---|
| ARCH-040 | Convert approved reply text to playback. must satisfy this documented contract without widening its responsibility. | Contract test and review. |

## Contract

```text
speak(request: SpeechRequest) -> Result<SpeechResult>; stop(request_id: string) -> Result<null>; healthcheck() -> Result<Health>
```

## Behaviour

Normal behavior: Convert approved reply text to playback.
Edge cases and concurrency: One active playback; interruption cancels it.

## Errors and failover

TransientError/RateLimited: retry once then fail over; failure leaves text visible; user hears nothing further.

## Config keys

providers.tts_failover: string[]; tts.timeout_seconds: integer > 0; sensitive_mode requires local adapter.

## Logging and audit

Record adapter, duration, error kind; redact spoken text where policy requires.

## Security requirements

- [SEC-004](../../03-security/threat-model.md#sec-004)
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

- 2026-11-02: Added Part 4 TTS component contract.
