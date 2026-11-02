# Safe mode

Purpose: define a restricted operating state that contains risk while preserving read-only assistance.

## Safe-mode requirements

| ID | Requirement | Verification |
|---|---|---|
| SEC-053 | Safe mode must activate on manual owner request, repeated errors, provider anomaly, or integrity failure. | Test |
| SEC-054 | Safe mode must disable shell execution, make/create actions, mail sending, file modification/deletion, and app launch. | Test |
| SEC-055 | Safe mode must permit read-only tools and answering questions without allowing state-changing tool actions. | Test |
| SEC-056 | The HUD must visibly indicate safe mode and list disabled capability classes without exposing secrets. | Manual |
| SEC-057 | Exiting safe mode must require explicit owner action and a recorded reason; integrity failures must additionally pass a documented review. | Test |
| SEC-058 | Safe mode must fail closed when its activation state cannot be determined. | Test |

## Activation

| Trigger | Activation behavior |
|---|---|
| Manual | Owner uses HUD control, typed command, or global safety control. |
| Repeated errors | Configured repeated tool, permission-gate, or adapter error threshold is reached; exact threshold is TO VERIFY. |
| Provider anomaly | Provider returns unexpected identity, unsafe protocol state, repeated malformed output, or unexplained usage anomaly. |
| Integrity failure | Audit-chain verification, configuration integrity, or dependency-integrity control reports failure. |

## Capability matrix

| Capability | Safe mode behavior | Reason |
|---|---|---|
| Answering questions | Allowed without state-changing tools. | Preserves low-risk assistance. |
| Read-only tools | Allowed at L0, subject to allow-lists and sensitive mode. | Supports inspection without modification. |
| File write/move/delete | Disabled. | Prevents local modification and destruction. |
| App launch/close | Disabled. | Prevents process side effects. |
| Mail draft/send | Disabled. | Prevents external communication and state change. |
| Calendar create/update/delete | Disabled. | Prevents commitment changes. |
| Make/create | Disabled. | Prevents generated artifacts and external effects. |
| Shell execution | Disabled. | Prevents code execution. |
| Mic/trigger | May remain available only for owner request; active capture still follows [SEC-045](security-model.md#sec-045). | Preserves control while limiting effects. |

## HUD indication

The HUD must show a persistent “Safe mode” state, the activation reason when safe to display, the disabled capability classes, and the owner action required to request exit. The core must continue safely if the HUD is absent.

## Exit procedure

1. Owner reviews the activation reason and relevant redacted audit records.
2. Owner resolves the triggering condition, such as revoking a token, correcting configuration, or completing integrity review.
3. Owner explicitly exits safe mode through a typed command or HUD action.
4. The system records the reason, approver channel, and time.
5. The system restores only capabilities enabled by the active profile and permission matrix; it must not restore a tool disabled by policy.

## Related docs

- [Security model](security-model.md)
- [Incident response](incident-response.md)
- [Threat model](threat-model.md)
- [Permission levels](permission-levels.md)
- [F05: Tool system and permissions](../02-features/F05-tool-system-and-permissions.md)

## Open questions

- What repeated-error threshold should activate safe mode? TO VERIFY.
- Which provider anomalies are reliable enough for automatic activation? TO VERIFY.

## Change log

- 2026-11-02: Added Part 2 safe-mode specification.
