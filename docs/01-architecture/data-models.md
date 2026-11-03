# Data models

Purpose: define transport and persistence schemas independent of implementation.

## Model requirements

| ID | Requirement | Verification |
|---|---|---|
| ARCH-055 | Every cross-component payload must validate against its documented model before use. | Contract test. |
| ARCH-056 | Persistent records must redact secrets and observe configured retention before storage. | Storage test. |

## Schemas

| Model | Field name | Type | Required | Description | Example |
|---|---|---|---|---|---|
| AudioClip | request_id | string | Yes | Request correlation. | `"req_123"` |
| AudioClip | bytes | binary | Yes | Bounded captured audio. | `<binary>` |
| AudioClip | duration_ms | integer | Yes | Capture duration. | `4200` |
| Transcript | text | string | Yes | Transcribed user content. | `"Read my notes"` |
| Transcript | confidence | number/null | No | Adapter confidence when supplied. | `0.91` |
| Message | role | enum | Yes | user, assistant, tool, system. | `"user"` |
| Message | content | string/object | Yes | Redacted message body. | `"Hello"` |
| ToolSpec | name | string | Yes | Registry-unique tool action. | `"files.read"` |
| ToolSpec | schema | object | Yes | JSON-schema parameters. | `{"type":"object"}` |
| ToolCall | call_id | string | Yes | Model call correlation. | `"call_1"` |
| ToolCall | name | string | Yes | Requested registered action. | `"mail.send"` |
| ToolCall | arguments | object | Yes | Schema-validated parameters. | `{"to":"a@example.com"}` |
| ToolResult | call_id | string | Yes | Matching call ID. | `"call_1"` |
| ToolResult | ok | boolean | Yes | Completion status. | `false` |
| ToolResult | data/error | object/null | Yes | Result or redacted error. | `{"kind":"Timeout"}` |
| Reply | text | string | Yes | User-visible answer. | `"I found two notes."` |
| Reply | speech_allowed | boolean | Yes | Whether TTS may speak it. | `true` |
| ApprovalRequest | approval_id | string | Yes | One-action approval ID. | `"apr_1"` |
| ApprovalRequest | action/target/arguments | string/string/object | Yes | Exact proposed effect. | `"mail.send"` |
| ApprovalDecision | approval_id | string | Yes | Matched request ID. | `"apr_1"` |
| ApprovalDecision | decision/channel | enum/enum | Yes | approve/deny; HUD/hotkey/typed. | `"deny"` |
| AuditRecord | timestamp/request_id | string/string | Yes | UTC event and correlation. | `"2026-11-03T00:00:00Z"` |
| AuditRecord | source/tool/arguments | string/string/object | Yes | Redacted activity detail. | `"hotkey"` |
| AuditRecord | risk/decision/result/duration | string/string/string/integer | Yes | Security outcome. | `"L3"` |
| MemoryItem | id/content/tags | string/string/string[] | Yes | Owner note and labels. | `"note_1"` |
| MemoryItem | created_at/expires_at | string/string/null | Yes | Retention timestamps. | `null` |
| Reminder | id/text/due_at | string/string/string | Yes | Scheduled reminder. | `"rem_1"` |
| GreetingContext | user_name/timezone/state | string/string/string | Yes | Safe greeting context. | `"Example User"` |
| Event | event_id/request_id/type | string/string/null/string | Yes | Standard event identity. | `"evt_1"` |
| Event | timestamp_utc/source/payload | string/string/object | Yes | Origin and validated content. | `"trigger"` |

## Memory store tables

| Table | Columns | Indexes | Retention |
|---|---|---|---|
| memory_items | id, content, tags, created_at, updated_at, expires_at | primary `id`; `expires_at`; tags index TO VERIFY | Delete/expire by `expires_at` and configured retention. |
| reminders | id, text, due_at, status, created_at, updated_at | primary `id`; `due_at,status` | Retain completed items per owner policy TO VERIFY. |
| audit_records | record_id, timestamp, request_id, redacted_payload, hash | primary `record_id`; `timestamp`; `request_id` | Retain under logging policy; rotate with chained hashes. |

## Related docs

- [Components and contracts](components-and-contracts.md)
- [HUD protocol](hud-protocol.md)
- [Tool manifest specification](tool-manifest-spec.md)
- [Audit log component](components/audit-log.md)

## Open questions

- Should memory content use full-text indexing, and under what local privacy guarantees? TO VERIFY.
- Which database engine preserves the required portability? TO VERIFY.

## Change log

- 2026-11-03: Added Part 5 data-model specification.
