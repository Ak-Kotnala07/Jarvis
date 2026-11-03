# LLM provider

## Responsibility

Produce a response or normalized tool proposal from validated context. It must not execute tools, approve actions, receive secrets, or define risk.

| ID | Requirement | Verification |
|---|---|---|
| ARCH-039 | Produce a response or normalized tool proposal from validated context. must satisfy this documented contract without widening its responsibility. | Contract test and review. |

## Contract

```text
chat(request: ChatRequest) -> Result<ChatResult>; chat_with_tools(request: ChatRequest, tools: ToolDefinition[]) -> Result<ChatResult>; healthcheck() -> Result<Health>
```

## Behaviour

Normal behavior: Produce a response or normalized tool proposal from validated context.
Edge cases and concurrency: One call per active loop step; cancel on interruption or safe mode.

### Tool-call normalization

Every adapter maps its native call representation before returning it:

```text
NormalizedToolCall = { call_id: string, name: string, arguments: object,
                       source: "llm", request_id: string }
```

The registry must reject an unknown `name`; the tool schema must reject missing, extra, or wrong-type `arguments`; and the permission gate must reject denied calls before execution. The model receives `{call_id, ok, data|null, error|null}` with a redacted error kind of `unknown_tool`, `invalid_arguments`, `denied`, `timeout`, or `failed`. This is required by [ARCH-034](../components-and-contracts.md#architecture-requirements) and [ARCH-035](../components-and-contracts.md#architecture-requirements).

## Errors and failover

TransientError/RateLimited: retry once then next adapter; InvalidResponse: fail over; user hears “I’m having trouble reasoning right now.”

## Config keys

providers.llm_failover: string[]; llm.timeout_seconds: integer > 0; sensitive_mode requires local adapter; reject empty failover list.

## Logging and audit

Record adapter, token-budget class, duration, error kind; redact prompts, tool arguments, and secrets.

## Security requirements

- [SEC-003](../../03-security/threat-model.md#sec-003)
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

- 2026-11-02: Added Part 4 LLM provider component contract.
