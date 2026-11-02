+# Security model

Purpose: define testable controls for secrets, privacy, local channels, execution, audit, and operational limits.

## Security requirements

| ID | Requirement | Verification |
|---|---|---|
| SEC-032 | Secrets must be stored in the OS keychain where available; an untracked `.env` file is permitted only as a fallback. | Manual |
| SEC-033 | Secrets must never be logged, committed, displayed in the HUD, or sent to an LLM. | Test |
| SEC-034 | Secret rotation must replace the stored value, revoke the old value where supported, restart affected adapters, and record a redacted audit event. | Manual |
| SEC-035 | `.env.example` must contain names, comments, and empty example values only; it must not contain real identifiers, tokens, or secrets. | Review |
| SEC-036 | Normal mode must disclose only the minimum data needed by a configured cloud adapter and must show the active provider class before the request. | Manual |
| SEC-037 | `sensitive_mode` must route reasoning, STT, and TTS to local adapters and must make no cloud calls. | Test |
| SEC-038 | Mail and calendar integrations must request only read-only and draft-capable scopes; sending must remain a separately approved L3 action. | Review |
| SEC-039 | OAuth tokens must use OS keychain storage, be revocable by the owner, and stop the affected integration on expiry until reauthorization succeeds. | Test |
| SEC-040 | The HUD channel must bind only to `127.0.0.1`, validate Origin, use a per-session random token, validate message schema, rate-limit messages, and deny remote access. | Test |
| SEC-041 | Generated-code execution must use a dedicated work folder, a timeout, an output cap, and L3 approval for every execution. | Test |
| SEC-042 | Generated-code execution must deny network access by default; feasibility of platform enforcement is TO VERIFY. | Test |
| SEC-043 | Audit records must be append-oriented and include the defined redacted record schema. | Test |
| SEC-044 | Audit rotation and retention must preserve integrity evidence, and the integrity mechanism must use hash chaining as a Proposed control pending owner approval. | Test |
| SEC-045 | Mic capture must expose a live indicator, support a hard-mute hotkey, auto-timeout in hotkey mode, and stop safely on device change. | Manual |
| SEC-046 | Each request must enforce a maximum tool-step count, maximum elapsed seconds, daily token budget, and per-provider rate-limit handling. | Test |
| SEC-047 | Limit, timeout, provider-rate-limit, and unavailable-provider failures must cancel pending tools, fail soft, and produce an audited explanation. | Test |
| SEC-048 | Dependencies must use pinned versions and a lock file before runtime dependencies are introduced. | Review |
| SEC-049 | Adding or updating a dependency must complete vulnerability scanning and human review before merge. | Review |
| SEC-050 | A global kill switch must stop triggers, audio capture, pending tools, provider requests, TTS, and HUD activity immediately. | Test |
| SEC-051 | The kill switch must be available through a global hotkey and a local command. | Manual |
| SEC-052 | Office-PC features must remain disabled until the owner confirms the corresponding IT and policy checklist item. | Review |

## Secrets and token handling

| Item | Control |
|---|---|
| Primary storage | OS keychain; adapter receives a secret only at use time. |
| Fallback | Untracked `.env`; use only when keychain integration is unavailable. |
| Repository rules | Commit `.env.example` only; never commit `.env`, exported tokens, or generated secret-bearing files. |
| Rotation procedure | 1. Stop affected integration. 2. Create replacement credential. 3. Store replacement. 4. Revoke old credential where supported. 5. Reauthorize/restart adapter. 6. Audit redacted completion. |
| OAuth revocation | 1. Revoke at provider. 2. Delete local keychain token. 3. Disable integration. 4. Audit revocation. |
| Expiry | Disable the affected adapter, notify the owner without leaking token data, and require explicit reauthorization. |

## Privacy modes and data flow

Default adapter: none; privacy behavior is adapter-contract based. Swap candidates: any local or cloud adapter that satisfies the interfaces and controls below.

| Provider class | Normal mode may receive | Sensitive mode may receive |
|---|---|---|
| Cloud STT | Captured audio required for one transcription. | Nothing. |
| Cloud LLM | User request, selected conversation context, and validated tool results with secrets redacted. | Nothing. |
| Cloud TTS | Response text required for synthesis. | Nothing. |
| Local adapter | Locally processed input required for the selected function. | Locally processed input required for the selected function. |

| Mode | STT flow | Reasoning flow | TTS flow | Network behavior |
|---|---|---|---|---|
| Normal | Audio goes to configured local or cloud adapter. | Redacted minimal context goes to configured local or cloud adapter. | Response text goes to configured local or cloud adapter. | Cloud use is permitted only for configured adapters and disclosed per [SEC-036](#sec-036). |
| sensitive_mode | Audio goes to local adapter only. | Context goes to local adapter only. | Response text goes to local adapter only. | No cloud calls under [SEC-037](#sec-037). |

Training, retention, and handling terms for every cloud provider are TO VERIFY before normal-mode enablement.

## Mail and calendar access

| Capability | Required scope class | Risk control |
|---|---|---|
| Read/search | Read-only scope limited to selected account/calendar. | L0; content is untrusted. |
| Draft mail | Draft-capable scope only. | L1; audit required. |
| Send mail | Send scope only if owner enables it. | L3; hotkey/HUD approval under [SEC-020](permission-levels.md#sec-020). |
| Create/update calendar | Minimum write scope for selected calendar. | L1/L2 per [permission matrix](permission-levels.md#tool-action-matrix). |
| Delete calendar event | Minimum write scope for selected calendar. | L3; hotkey/HUD approval. |

## Localhost HUD channel

The HUD is optional; core operation must not depend on it. Each session token must be random, memory-only, and invalidated when the core or HUD session ends. Unknown message types, invalid schemas, invalid Origin values, excess rate, absent tokens, and non-loopback connections must be denied and audited without accepting the message.

## Generated-code execution

The dedicated work folder must be outside the repository and outside protected user folders. Execution output must be capped before it reaches logs, the HUD, or a model. Network isolation is a goal under [SEC-042](#sec-042); platform-specific feasibility is TO VERIFY and no claimed sandbox guarantee exists until verified.

## Audit log

| Field | Recording rule |
|---|---|
| timestamp | UTC event time. |
| request_id | Correlation identifier for the user request. |
| source_trigger | Wake word, hotkey, typed, HUD, or internal event. |
| transcript | Redacted request transcript where retention permits. |
| tool | Tool action name, if any. |
| arguments | Redacted arguments only. |
| risk_level | L0–L3 decision level. |
| decision | Proposed, approved, denied, expired, cancelled, or executed. |
| approver_channel | None, hotkey, HUD, or typed. |
| result | Success, failure class, or cancellation. |
| duration | Elapsed time in milliseconds. |

Rotate logs by configured size or age, retain according to owner policy, and preserve chained hashes across rotated segments. Hash chaining is Proposed, pending owner approval; it provides tamper evidence, not protection against a full OS compromise.

## Mic safety and limits

| Area | Proposed default |
|---|---|
| Live mic | HUD/OS-visible active indicator while capture is open. |
| Hard mute | Global hotkey disables capture immediately. |
| Hotkey mode | Capture auto-times out after a configured short interval; exact value is TO VERIFY. |
| Device change | Stop capture, clear partial session, notify owner, and require a fresh trigger. |
| Tool steps | Configured maximum; exact value is TO VERIFY. |
| Request duration | Configured maximum; exact value is TO VERIFY. |
| Daily tokens | Configured per-provider and total budget; exact value is TO VERIFY. |
| Provider rate limit | Back off once, surface failure, then use configured failover or local fallback without retry loops. |

## Dependency hygiene checklist

Before adding a dependency:

- [ ] Confirm the capability cannot be met by the standard library or existing dependency.
- [ ] Pin an exact version and update the lock file.
- [ ] Review license, maintainer/source, and known vulnerability scan output.
- [ ] Record why the dependency needs the permissions it receives.
- [ ] Obtain human review and audit the addition.

## Office-PC compliance checklist

Before enabling a feature on an office PC, confirm with IT/policy:

- [ ] Microphone and recording permission.
- [ ] Local installation and autostart permission.
- [ ] Approved cloud STT/LLM/TTS providers and data regions.
- [ ] Mail and calendar OAuth scopes and account type.
- [ ] File-folder allow-lists and retention requirements.
- [ ] Network/proxy, localhost service, and firewall policy.
- [ ] Audit-log retention, monitoring, and incident reporting obligations.
- [ ] Shell, generated-code, and external-send restrictions.

## Kill switch

The global hotkey and local command must invoke [SEC-050](#sec-050) without waiting for an LLM, provider, HUD, or audit write. The audit subsystem should record the event after shutdown begins; inability to record it must not delay shutdown.

## Related docs

- [Threat model](threat-model.md)
- [Permission levels](permission-levels.md)
- [Incident response](incident-response.md)
- [Safe mode](safe-mode.md)
- [F05: Tool system and permissions](../02-features/F05-tool-system-and-permissions.md)
- [F19: Offline mode](../02-features/F19-offline-mode.md)
- [Checklist](../06-checklist/CHECKLIST.md)

## Open questions

- Which keychain APIs are supported on each target platform? TO VERIFY.
- What exact limits meet the owner’s cost and latency goals? TO VERIFY.
- Can network denial for generated execution be consistently enforced on all platforms? TO VERIFY.

## Change log

- 2026-11-02: Added Part 2 security control model.

