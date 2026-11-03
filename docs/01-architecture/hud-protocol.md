# HUD protocol

Purpose: define the optional local WebSocket protocol between core and HUD frontend.

## Protocol requirements

| ID | Requirement | Verification |
|---|---|---|
| ARCH-057 | HUD handshake must require loopback origin validation and a per-session random token. | Integration test. |
| ARCH-058 | Every HUD message must declare protocol version, type, request ID where applicable, and validated payload. | Schema test. |
| ARCH-059 | HUD messages must be rate-limited and an absent/disconnected HUD must not block core. | Load/integration test. |

## Handshake

1. Client connects only to `ws://127.0.0.1:<configured-port>`.
2. Server validates the browser Origin against configured local HUD origin.
3. Client sends `hello` with `version` and memory-only `session_token`.
4. Server rejects missing/invalid token, non-loopback peer, unsupported version, or invalid schema.
5. Server responds `ready` with session ID and current state.

## Message envelope

```json
{"version": 1, "type": "state_changed", "message_id": "msg_1",
 "request_id": "req_1", "sequence": 12, "payload": {}}
```

| Field | Type | Rule |
|---|---|---|
| version | integer | Must equal supported major version. |
| type | string | Must be an allowed message type. |
| message_id | string | Unique per sender session. |
| request_id | string/null | Required for request-scoped events. |
| sequence | integer | Strictly increasing per sender session. |
| payload | object | Must validate for the message type. |

## Message types

| Direction | Type | Required payload fields |
|---|---|---|
| Core → HUD | state_changed | state, reason? |
| Core → HUD | transcript_partial | text, final=false |
| Core → HUD | transcript_final | text, final=true |
| Core → HUD | assistant_text | text, speech_allowed |
| Core → HUD | approval_request | approval_id, action, target, arguments, risk_level, expires_at |
| Core → HUD | action_log | action, decision, result, duration_ms |
| Core → HUD | error | code, message, retryable |
| Core → HUD | mic_status | active, device_id?, muted |
| Core → HUD | safe_mode | active, reason, disabled_capabilities |
| HUD → Core | approval_response | approval_id, decision, channel="hud" |
| HUD → Core | mute | muted |
| HUD → Core | kill_switch | confirmed=true |
| HUD → Core | safe_mode | request_activate/request_exit, reason? |

## Ordering, reconnect, and rate limits

Core messages use monotonically increasing sequence numbers. HUD drops duplicate/out-of-order messages and requests a fresh state snapshot after a gap. Reconnect requires a new handshake and token; the HUD receives current state, not replayed secret-bearing history. Default rate limits are TO VERIFY; excess messages are dropped, audited, and never delay core safety handling.

## Related docs

- [HUD server component](components/hud-server.md)
- [State machine](state-machine.md)
- [Security model](../03-security/security-model.md)
- [F11: HUD](../02-features/F11-hud.md)

## Open questions

- Which local HUD origin is used by the future frontend? TO VERIFY.
- What rate limits preserve responsive approvals without abuse? TO VERIFY.

## Change log

- 2026-11-03: Added Part 5 HUD WebSocket protocol.
