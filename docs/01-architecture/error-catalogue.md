# Error catalogue

Purpose: define normalized errors, ownership, retry behavior, spoken feedback, and log severity.

| Code | Meaning | Raised by | Retryable? | User-facing spoken message | Log level |
|---|---|---|---|---|---|
| ERR-001 | Trigger rejected or rate limited. | Trigger | No | “I’m not ready for another request yet.” | INFO |
| ERR-002 | Audio device unavailable. | Audio input | Yes, once | “My microphone is unavailable. Please type that.” | WARNING |
| ERR-003 | Audio capture timed out. | Audio input | No | “I didn’t hear anything. Please try again.” | INFO |
| ERR-004 | STT transient failure. | STT | Yes, once/failover | “I couldn’t transcribe that. Please try again or type it.” | WARNING |
| ERR-005 | Provider rate limited. | STT/LLM/TTS | Yes, once/failover | “That service is busy; I’m trying a fallback.” | WARNING |
| ERR-006 | Provider authentication failed. | Adapter | No | “That service needs attention.” | ERROR |
| ERR-007 | Provider response invalid. | Adapter | No; failover | “I received an invalid response, so I’m using a fallback.” | ERROR |
| ERR-008 | Adapter or tool timed out. | Adapter/tool | No; failover if adapter | “That took too long, so I stopped it.” | WARNING |
| ERR-009 | Unknown tool requested. | Registry | No | “That action is unavailable.” | WARNING |
| ERR-010 | Tool arguments invalid. | Schema validator | No | “I can’t perform that action with those details.” | WARNING |
| ERR-011 | Tool denied by policy. | Permission gate | No | “I can’t perform that action.” | INFO |
| ERR-012 | Approval denied, expired, or ambiguous. | Permission gate | No | “I did not receive approval, so I stopped.” | INFO |
| ERR-013 | Allow-list violation. | Permission gate/tool | No | “That target is not allowed.” | WARNING |
| ERR-014 | Path traversal or symlink escape. | Files tool | No | “That file location is not allowed.” | ERROR |
| ERR-015 | Agent loop limit or repetition detected. | Orchestrator | No | “I stopped because the request was repeating.” | WARNING |
| ERR-016 | Request budget exceeded. | Orchestrator | No | “I reached this request’s limit.” | WARNING |
| ERR-017 | HUD handshake/message invalid. | HUD server | No | “The display connection needs attention.” | WARNING |
| ERR-018 | Audit store/integrity failure. | Audit log | No; safe mode | “Safety records need attention.” | ERROR |
| ERR-019 | Safe mode active. | Safety/core | No | “Safe mode is on; only read-only help is available.” | INFO |
| ERR-020 | Configuration invalid/missing. | Settings | No | “Configuration needs attention before I can start that feature.” | ERROR |
| ERR-021 | Unsupported capability/platform. | Platform/registry | No | “That capability is unavailable on this machine.” | INFO |
| ERR-022 | Kill switch activated. | Core | No | “Stopped.” | WARNING |
| ERR-023 | Network unavailable. | Adapter | Yes, bounded | “Network is unavailable; I’m using local options if available.” | WARNING |
| ERR-024 | Secret reference unavailable. | Settings/secret resolver | No | “A required credential needs attention.” | ERROR |

## Catalogue requirements

| ID | Requirement | Verification |
|---|---|---|
| ARCH-063 | Components must map internal failures to one catalogued error before they cross a contract boundary. | Contract test. |
| ARCH-064 | Spoken messages must not expose secrets, raw provider text, filesystem internals, or security-sensitive detail. | Redaction test. |
| ARCH-065 | Retryable errors must obey the bounded shared failover rule. | Fault-injection test. |

## Related docs

- [Components and contracts](components-and-contracts.md)
- [Request lifecycle](request-lifecycle.md)
- [Incident response](../03-security/incident-response.md)
- [Safe mode](../03-security/safe-mode.md)

## Open questions

- Which error codes need UI-only detail distinct from spoken feedback? TO VERIFY.
- Should codes be exposed in owner-facing HUD diagnostics? TO VERIFY.

## Change log

- 2026-11-03: Added Part 5 error catalogue.
