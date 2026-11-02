+# Threat model

Purpose: identify security and privacy threats to the local assistant and define verifiable mitigations.

## Scope and principles

This document applies to [F05: Tool system and permissions](../02-features/F05-tool-system-and-permissions.md). Governing principles: least privilege; confirm before harm; model proposes, code disposes; untrusted input is data not instructions; fail soft; same code on every machine; everything audited; free first.

## Assets

| Asset | Protection concern |
|---|---|
| Files | Private and work data requires configured folder allow-lists. |
| Mail content | May be private and adversarial; it is untrusted data. |
| API keys/tokens | Grant external access and require external runtime storage. |
| Mic audio | May capture private conversations and bystanders. |
| Shell/code execution | Runs with the owner’s OS permissions. |
| Audit log | Provides accountability and incident evidence. |
| Config | Determines providers, profiles, tools, and allow-lists. |

## Trust boundaries and data flow

1. A wake word, hotkey, typed request, or audio capture enters the local process.
2. Audio may leave the machine only to the configured STT adapter; text and selected context may leave only to the configured LLM adapter.
3. The LLM returns a proposal; local code validates it and the permission gate decides whether any tool can receive it.
4. A tool may access configured local allow-lists or its configured external account scope.
5. The HUD receives status only through a loopback WebSocket; runtime records are kept in the OS user-data directory, outside this repository.

| Boundary | Data leaving machine | Recipient/form | Control |
|---|---|---|---|
| STT | Audio payload | Configured local or remote STT adapter | [SEC-004](#sec-004), [SEC-011](#sec-011) |
| LLM | User text and selected context | Configured local or remote LLM adapter | [SEC-003](#sec-003), [SEC-004](#sec-004) |
| Tools | Action-specific fields | Configured mail/calendar/web/make destination | [SEC-001](#sec-001), [SEC-008](#sec-008) |
| HUD | Display status | `127.0.0.1` WebSocket | [SEC-005](#sec-005) |
| Runtime store | Logs, tokens, database, generated files | OS user-data directory | [SEC-002](#sec-002), [SEC-009](#sec-009) |

## Actors

| Actor | Capability or motive |
|---|---|
| Owner | Configures and approves intended work. |
| Bystander/other voice | Can speak near the microphone. |
| Malicious email/web/file content | Can inject adversarial instructions. |
| Malicious website | Can target a localhost service. |
| Compromised dependency | Can alter local process behavior. |
| Compromised LLM provider | Can expose input or return unsafe proposals. |
| Curious coworker | Can access a shared office machine or overhear activity. |

## Security requirements

| ID | Requirement | Verification |
|---|---|---|
| SEC-001 | Every tool invocation must pass through the permission gate before reaching its executor. | Test |
| SEC-002 | Runtime secrets, tokens, logs, databases, and generated files must not be written into the repository. | Review |
| SEC-003 | Mail, web, file, and tool-output content must be treated as data and must not directly authorize actions. | Test |
| SEC-004 | Sensitive mode must minimize remote-provider disclosure and must warn before sending data where training, retention, or handling terms are TO VERIFY. | Manual |
| SEC-005 | The HUD WebSocket must bind only to `127.0.0.1`, validate Origin, and require a per-session token. | Test |
| SEC-006 | File tools must resolve canonical paths and must reject traversal or symlink resolution outside configured allow-lists. | Test |
| SEC-007 | Generated code or shell commands must not run with user permissions unless an L3 invocation approves the exact target and arguments. | Test |
| SEC-008 | Secrets must not be emitted to logs, prompts, audit records, generated files, or Git-tracked content. | Test |
| SEC-009 | Audit records must be append-oriented, access-restricted, and detectable when altered or unavailable. | Test |
| SEC-010 | The orchestrator must enforce bounded turns, tool calls, timeouts, and configured provider/token limits. | Test |
| SEC-011 | Mic capture must show an active state, end on timeout or cancellation, and fail closed when state is unknown. | Manual |
| SEC-012 | Voice-triggered requests must not execute actions requiring a stronger-than-voice approval mechanism. | Test |
| SEC-013 | Each approval must identify one exact action, target, arguments, risk level, and expiry, and ambiguous or expired responses must deny it. | Test |
| SEC-014 | False trigger events must be rate-limited and must not open an indefinite mic session. | Test |
| SEC-015 | Office profiles must disable or restrict capabilities required by applicable IT policy before the orchestrator can use them. | Review |
| SEC-016 | Dependencies and integrity metadata must be reviewed before introduction, and updates must be auditable. | Review |

## Threat register

| ID | Threat | Entry point | Likelihood | Impact | Mitigation | Verification | Residual risk |
|---|---|---|---|---|---|---|---|
| THR-001 | Prompt injection causes a tool proposal. | Email, web, file content | H | H | [SEC-003](#sec-003), [SEC-001](#sec-001), [SEC-013](#sec-013) | Injection corpus test | Owner can approve a clearly displayed harmful action. |
| THR-002 | TV, video, or colleague spoofs a voice command. | Microphone | M | H | [SEC-012](#sec-012), [SEC-014](#sec-014), [SEC-011](#sec-011) | Playback/bystander test | L0 requests may still trigger. |
| THR-003 | A webpage abuses the localhost HUD. | Browser WebSocket | M | H | [SEC-005](#sec-005) | Origin/token test | Compromised browser extension risk remains. |
| THR-004 | AI-generated code runs with user permissions. | Make/shell proposal | M | H | [SEC-007](#sec-007), [SEC-013](#sec-013) | L3 target test | Owner can intentionally approve unsafe code. |
| THR-005 | Path traversal or symlink escape reaches disallowed files. | File parameters | M | H | [SEC-006](#sec-006), [SEC-001](#sec-001) | Traversal/symlink test | OS race behavior is TO VERIFY. |
| THR-006 | Keys leak into logs, prompts, Git, or generated output. | Logging/provider/repo | M | H | [SEC-002](#sec-002), [SEC-008](#sec-008) | Secret-scan test | Direct external disclosure is outside local control. |
| THR-007 | Free-tier provider handling exposes sensitive data. | Remote STT/LLM request | M | H | [SEC-004](#sec-004) | Sensitive-mode review | Provider behavior is TO VERIFY. |
| THR-008 | A compromised dependency alters behavior or exfiltrates data. | Dependency/build artifact | M | H | [SEC-016](#sec-016), [SEC-002](#sec-002) | Dependency review | Transitive compromise cannot be eliminated. |
| THR-009 | Mic remains open or captures bystanders. | Audio lifecycle | M | M | [SEC-011](#sec-011), [SEC-014](#sec-014) | Manual capture-state test | OS indicators vary by platform. |
| THR-010 | Audit history is altered to hide actions. | Runtime-data access | L | H | [SEC-009](#sec-009) | Tamper/unavailable-log test | Full OS owner control remains an accepted risk. |
| THR-011 | Runaway loops consume tokens, tools, or quota. | Orchestrator/provider failure | M | M | [SEC-010](#sec-010) | Limit/timeout test | Provider accounting delay is TO VERIFY. |
| THR-012 | Owner approves the wrong action. | Approval UI/voice | M | H | [SEC-013](#sec-013), [SEC-012](#sec-012) | Ambiguity/UI test | Owner inattentiveness remains possible. |
| THR-013 | False wake words deny service. | Wake-word/hotkey | M | M | [SEC-014](#sec-014), [SEC-010](#sec-010) | Trigger-rate test | Noise can reduce availability. |
| THR-014 | Office use violates IT policy. | Office profile/provider | M | H | [SEC-004](#sec-004), [SEC-015](#sec-015) | Profile review | Policy interpretation needs owner/IT confirmation. |

## Out of scope / accepted risks

- Physical access by a person with the owner’s unlocked OS session is accepted; [SEC-009](#sec-009) provides detection, not guaranteed prevention.
- Remote-provider processing, retention, and training are TO VERIFY; sensitive mode only reduces disclosure.
- Local voice processing is deferred to Phase 8 under the cloud-first proposed default, pending owner approval.
- Mouse and keyboard automation are excluded until designed as an L3 tool.

## Related docs

- [Permission levels](permission-levels.md)
- [Security model](security-model.md)
- [F05: Tool system and permissions](../02-features/F05-tool-system-and-permissions.md)
- [ADR-0004: Provider-agnostic interfaces](../05-decisions/ADR-0004-provider-agnostic-interfaces.md)
- [Checklist](../06-checklist/CHECKLIST.md)

## Open questions

- Which remote providers satisfy sensitive-mode requirements? TO VERIFY.
- What tamper-evidence mechanism is suitable for local audit storage? TO VERIFY.
- Which office IT policies apply to each office machine? TO VERIFY.

## Change log

- 2026-11-02: Added Part 1 threat model and requirement register.

