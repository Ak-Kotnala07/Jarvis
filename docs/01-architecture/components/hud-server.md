# HUD server

## Responsibility

Publish validated status to the optional loopback HUD. It must not expose remote access, authorize tools, or require core availability.

| ID | Requirement | Verification |
|---|---|---|
| ARCH-046 | Publish validated status to the optional loopback HUD. must satisfy this documented contract without widening its responsibility. | Contract test and review. |

## Contract

```text
start(config: HudConfig) -> Result<Endpoint>; publish(event: Event) -> Result<null>; stop() -> Result<null>
```

## Behaviour

Normal behavior: Publish validated status to the optional loopback HUD.
Edge cases and concurrency: Slow/disconnected clients are dropped; core never waits on HUD.

## Errors and failover

InvalidResponse/Timeout: drop message/client; user hears no interruption.

## Config keys

hud.enabled: boolean = false; hud.host: literal 127.0.0.1; hud.port: integer; reject non-loopback host.

## Logging and audit

Record connection/session ID and message type; redact payload secrets.

## Security requirements

- [SEC-005](../../03-security/threat-model.md#sec-005)
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

- 2026-11-02: Added Part 4 HUD server component contract.
