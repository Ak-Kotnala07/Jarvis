# Memory

## Responsibility

Store and retrieve allowed owner notes outside the repository. It must not grant authority to retrieved text or store secrets.

| ID | Requirement | Verification |
|---|---|---|
| ARCH-044 | Store and retrieve allowed owner notes outside the repository. must satisfy this documented contract without widening its responsibility. | Contract test and review. |

## Contract

```text
read(query: MemoryQuery) -> Result<MemoryResult>; write(entry: MemoryEntry) -> Result<MemoryResult>
```

## Behaviour

Normal behavior: Store and retrieve allowed owner notes outside the repository.
Edge cases and concurrency: Request-scoped operations; writes serialize.

## Errors and failover

TransientError: retry once; Unsupported: continue without memory; user hears “Memory is unavailable.”

## Config keys

memory.namespace: string; memory.retention_days: integer = TO VERIFY; reject repository paths.

## Logging and audit

Record operation and namespace; redact content and secrets.

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

- 2026-11-02: Added Part 4 Memory component contract.
