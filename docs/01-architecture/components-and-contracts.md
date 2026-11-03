# Components and contracts

Purpose: catalog stable component boundaries and conventions that keep implementations replaceable.

## Component index

| Slot | Responsibility | Contract in/out | Default adapter | Swap candidates |
|---|---|---|---|---|
| Trigger | Turn an allowed activation into an event. | In: config; out: TriggerEvent. | None. | Any contract-compliant local trigger. |
| Audio input | Capture bounded audio. | In: CaptureRequest; out: AudioFrame. | None. | Any contract-compliant local audio source. |
| STT | Convert audio to transcript. | In: AudioFrame; out: Transcript. | None. | Local or cloud contract-compliant adapter. |
| LLM provider | Produce reply or normalized tool proposals. | In: ChatRequest; out: ChatResult. | None. | Local or cloud contract-compliant adapter. |
| TTS | Convert reply text to playback. | In: SpeechRequest; out: SpeechResult. | None. | Local or cloud contract-compliant adapter. |
| Tool registry | Resolve configured tool manifests. | In: tool name; out: ToolDefinition. | Built-in registry boundary. | Any config-backed registry. |
| Permission gate | Decide whether a proposal may execute. | In: ToolCall; out: Decision. | Built-in safety boundary. | No bypass permitted. |
| Orchestrator | Own request state and agent loop. | In: RequestEvent; out: ResponseEvent. | Built-in core boundary. | No adapter substitution. |
| Memory | Store/retrieve allowed notes. | In: MemoryRequest; out: MemoryResult. | None. | Any external-runtime-data store. |
| Scheduler | Manage bounded reminders/jobs. | In: ScheduleRequest; out: ScheduleResult. | Built-in service boundary. | Any contract-compliant local scheduler. |
| HUD server | Publish local status/messages. | In: Event; out: validated WebSocket message. | Built-in local transport. | Any loopback-only implementation. |
| Settings | Validate/load configuration. | In: files/environment; out: Settings. | Built-in settings boundary. | No adapter substitution. |
| Audit log | Record redacted security events. | In: AuditEvent; out: AuditResult. | Built-in safety boundary. | Any append-oriented store. |
| Platform layer | Isolate OS integration. | In: PlatformRequest; out: PlatformResult. | OS-specific implementation. | Per-OS implementation only. |
| Autostart | Register/remove startup behavior. | In: AutostartRequest; out: AutostartResult. | Platform implementation. | Per-OS implementation only. |

Default adapter: none unless stated. Swap candidates must satisfy the contract, security controls, and contract tests; vendor names do not define behavior.

## Shared conventions

### Error taxonomy

| Error | Meaning | Default handling |
|---|---|---|
| `TransientError` | Retriable local or transport failure. | One bounded retry, then failover/degrade. |
| `RateLimited` | Provider or service refuses current rate. | Respect retry hint once; fail over/degrade. |
| `AuthError` | Missing, expired, revoked, or insufficient authorization. | Disable capability and request owner action. |
| `InvalidResponse` | Output violates contract/schema. | Reject, audit, fail over/degrade. |
| `Timeout` | Work exceeded configured deadline. | Cancel, audit, fail over/degrade. |
| `Unsupported` | Capability/configuration is unavailable. | Degrade and state available alternative. |

### Result envelope

Every contract operation returns the conceptual envelope:

```text
Result<T> = { ok: boolean, data: T | null, error: ErrorInfo | null }
ErrorInfo = { kind: ErrorKind, message: redacted string, retry_after_ms?: integer }
```

[ARCH-031](#architecture-requirements) requires every component contract to return this envelope or an equivalent normalized representation. Verification: contract test.

### Standard event shape

```text
Event = {
  event_id: string,
  request_id: string | null,
  type: string,
  timestamp_utc: string,
  source: string,
  payload: object,
  sensitivity: "normal" | "sensitive"
}
```

[ARCH-032](#architecture-requirements) requires events to carry correlation and source fields and to redact secrets from payloads. Verification: contract test.

### Failover rule

[ARCH-033](#architecture-requirements) requires a component to retry only once for a `TransientError` or `RateLimited` when a retry hint permits it; then select the next configured compatible adapter once, otherwise enter degraded mode. `AuthError`, `InvalidResponse`, and `Unsupported` must not be retried blindly. Verification: fault-injection test.

## LLM tool-call normalization

Every LLM adapter must expose `chat(request)`, `chat_with_tools(request, tools)`, and `healthcheck()`.

```text
NormalizedToolCall = {
  call_id: string,
  name: string,
  arguments: object,
  source: "llm",
  request_id: string
}
```

[ARCH-034](#architecture-requirements) requires adapters to map provider-specific function/tool-call syntax into exactly one `NormalizedToolCall` shape before core receives it. Verification: shared LLM contract test.

Validation sequence:

1. Registry resolves `name`; unknown name is rejected.
2. Tool schema validates `arguments`; malformed, missing, extra, or wrong-type arguments are rejected.
3. Permission gate applies profile, allow-list, untrusted-content escalation, risk, and approval.
4. The result returned to the model is normalized as `{call_id, ok, data|null, error|null}`; errors are redacted and state whether the call was unknown, invalid, denied, timed out, or failed.
5. [ARCH-035](#architecture-requirements) requires rejected calls never to reach an executor. Verification: schema/permission test.

## Architecture requirements

| ID | Requirement | Verification |
|---|---|---|
| ARCH-031 | Every component contract must return the standard result envelope or an equivalent normalized representation. | Contract test. |
| ARCH-032 | Every event must carry correlation and source fields and must redact secrets from payloads. | Contract test. |
| ARCH-033 | Failover must follow the shared error taxonomy and bounded retry rule. | Fault-injection test. |
| ARCH-034 | Every LLM adapter must expose chat, chat_with_tools, and healthcheck and normalize all tool calls to one internal format. | Contract test. |
| ARCH-035 | Unknown tools or invalid arguments must be rejected before execution and reported to the model in the normalized result. | Schema/permission test. |

## Related docs

- [System overview](system-overview.md)
- [Request lifecycle](request-lifecycle.md)
- [Permission levels](../03-security/permission-levels.md)
- [Threat model](../03-security/threat-model.md)
- [F04: Provider failover](../02-features/F04-provider-failover.md)
- [F05: Tool system and permissions](../02-features/F05-tool-system-and-permissions.md)

## Open questions

- Which typed schema representation should be shared across tools and adapters? TO VERIFY.
- How should streaming partial results fit the result envelope? TO VERIFY.

## Change log

- 2026-11-02: Added Part 4 component catalog and shared contracts.

