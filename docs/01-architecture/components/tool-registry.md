# Tool registry

## Responsibility

Resolve configured tool manifests and schemas by name. It must not execute tools, assign risk, or bypass the permission gate.

| ID | Requirement | Verification |
|---|---|---|
| ARCH-041 | Resolve configured tool manifests and schemas by name. must satisfy this documented contract without widening its responsibility. | Contract test and review. |

## Contract

```text
resolve(name: string) -> Result<ToolDefinition>; list() -> Result<ToolDefinition[]>
```

## Behaviour

Normal behavior: Resolve configured tool manifests and schemas by name.
Edge cases and concurrency: Read-only and safe for concurrent lookup.

## Errors and failover

Unsupported/InvalidResponse: reject unknown/invalid tool; user hears “That action is unavailable.”

## Config keys

tools.enabled: string[]; reject duplicate names, absent manifests, or invalid schemas.

## Logging and audit

Record requested name and validation errors; redact schema defaults containing secrets.

## Security requirements

- [SEC-001](../../03-security/threat-model.md#sec-001)
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

- 2026-11-02: Added Part 4 Tool registry component contract.
