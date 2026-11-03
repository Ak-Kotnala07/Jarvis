# Permission gate

## Responsibility

Validate, classify, escalate, approve, and audit every tool proposal. It must not import tools or execute tool code.

| ID | Requirement | Verification |
|---|---|---|
| ARCH-042 | Validate, classify, escalate, approve, and audit every tool proposal. must satisfy this documented contract without widening its responsibility. | Contract test and review. |

## Contract

```text
decide(call: NormalizedToolCall, context: DecisionContext) -> Result<Decision>
```

## Behaviour

Normal behavior: Validate, classify, escalate, approve, and audit every tool proposal.
Edge cases and concurrency: Decisions are request-bound; one approval cannot satisfy another call.

## Errors and failover

InvalidResponse/Unsupported: deny; Timeout: default deny; user hears “I can’t perform that action.”

## Config keys

sensitive_mode: boolean; paths.allowed_folders: string[]; apps.allowed: string[]; shell.allowed_commands: string[]; validate all lists.

## Logging and audit

Record risk, decision, approver channel, redacted target/arguments.

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

- 2026-11-02: Added Part 4 Permission gate component contract.
