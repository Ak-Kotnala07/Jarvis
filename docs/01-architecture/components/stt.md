# STT

## Responsibility

Convert a bounded AudioFrame to Transcript. It must not authorize tools or retain audio outside configured adapter policy.

| ID | Requirement | Verification |
|---|---|---|
| ARCH-038 | Convert a bounded AudioFrame to Transcript. must satisfy this documented contract without widening its responsibility. | Contract test and review. |

## Contract

```text
transcribe(audio: AudioFrame, language?: string) -> Result<Transcript>; healthcheck() -> Result<Health>
```

## Behaviour

Normal behavior: Convert a bounded AudioFrame to Transcript.
Edge cases and concurrency: One transcription per request; cancel on interruption.

## Errors and failover

TransientError/RateLimited: retry once then next adapter; Timeout: typed fallback; user hears “Please type that.”

## Config keys

providers.stt_failover: string[]; stt.timeout_seconds: integer > 0; sensitive_mode selects local adapter.

## Logging and audit

Record adapter name, duration, error kind; redact transcript where policy requires.

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

- 2026-11-02: Added Part 4 STT component contract.
