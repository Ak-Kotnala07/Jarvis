+# Permission levels

Purpose: define tool risk classification, approvals, and profile restrictions.

## Fixed risk levels

| Level | Definition | Approval rule |
|---|---|---|
| L0 | Read-only action that does not alter local or external state. | No per-action approval after tool and target allow-list checks. |
| L1 | Safe write with bounded, reversible, non-external effect. | No per-action approval after allow-list checks; audit required. |
| L2 | Modification that can change local state or create meaningful side effects. | Ask for explicit approval for each action. |
| L3 | Destructive or external action, including code or command execution. | Always ask; each action needs valid approval. |

## Permission requirements

| ID | Requirement | Verification |
|---|---|---|
| SEC-017 | The permission gate must assign every tool action exactly one of L0, L1, L2, or L3 before execution. | Test |
| SEC-018 | L0 and L1 actions must verify their allow-list and configured profile before execution. | Test |
| SEC-019 | L2 and L3 actions must require an action-specific approval that expires before execution. | Test |
| SEC-020 | L3 approvals must not be grantable by voice alone; a hotkey press or HUD click must approve them, while voice may request them. | Test — Proposed default, pending owner approval. |
| SEC-021 | A tool call proposed after reading untrusted mail, web, or file text must be escalated one level, capped at L3. | Test |
| SEC-022 | The permission gate must deny execution when action, target, arguments, risk level, or profile decision is unavailable or ambiguous. | Test |
| SEC-023 | The gate must record approved, denied, expired, and timed-out decisions without recording secrets. | Test |
| SEC-024 | Profiles may narrow allow-lists, disable tools, reduce timeouts, or require stronger approval, but must not lower risk or weaken approval. | Review |
| SEC-025 | Mouse and keyboard automation must remain unavailable until designed and approved as an L3 tool. | Review — Proposed default, pending owner approval. |

## Escalation rule

[SEC-021](#sec-021) applies when a proposed action is causally based on mail, web, or file text. That content remains data, never authority: the model proposes and local code disposes.

| Base level | Escalated level |
|---|---|
| L0 | L1 |
| L1 | L2 |
| L2 | L3 |
| L3 | L3 |

## Tool action matrix

Timeout expiry means deny/cancel and audit. “Allow-list” means the applicable configured policy must pass.

| Tool action | Risk | Approval behaviour | Allow-list dependency | Timeout | Reason |
|---|---:|---|---|---:|---|
| files.list | L0 | None | allowed folder | 15s | Reads directory metadata. |
| files.read | L0 | None | allowed folder | 30s | Reads allowed file. |
| files.write | L1 | None; audit | allowed folder | 30s | Bounded local write. |
| files.move | L2 | Per action | source/destination folders | 30s | Alters file location. |
| files.delete | L3 | Always; hotkey/HUD | allowed folder | 30s | Destructive local action. |
| apps.list | L0 | None | configured application inventory | 15s | Reads application metadata. |
| apps.launch | L2 | Per action | apps.allowed | 30s | Starts local process. |
| apps.close | L2 | Per action | apps.allowed | 15s | May discard unsaved work. |
| system.info | L0 | None | none | 15s | Reads system status. |
| mail.read | L0 | None | authorized account/folders | 30s | Reads untrusted content. |
| mail.search | L0 | None | authorized account/folders | 30s | Searches authorized mail. |
| mail.draft | L1 | None; audit | authorized account/recipient policy | 30s | Reversible unsent draft. |
| mail.send | L3 | Always; hotkey/HUD | account/recipient allow-list | 60s | External communication. |
| calendar.read | L0 | None | authorized calendar | 30s | Reads calendar. |
| calendar.search | L0 | None | authorized calendar | 30s | Searches calendar. |
| calendar.create | L1 | None; audit | authorized calendar | 30s | Reversible event creation. |
| calendar.update | L2 | Per action | authorized calendar | 30s | Changes commitment. |
| calendar.delete | L3 | Always; hotkey/HUD | authorized calendar | 30s | Removes commitment. |
| web.search | L0 | None | configured web provider | 30s | Retrieves untrusted results. |
| web.fetch | L0 | None | URL scheme/network policy | 30s | Retrieves untrusted remote content. |
| make.plan | L0 | None | workspace allow-list | 30s | Produces plan only. |
| make.create | L3 | Always; hotkey/HUD | output/destination policy | 120s | Can generate local or external artifacts. |
| shell.execute | L3 | Always; hotkey/HUD | shell.allowed_commands/working folder | 30s | Executes code with user permissions. |
| memory.read | L0 | None | memory namespace | 15s | Reads notes; text is untrusted. |
| memory.write | L1 | None; audit | memory namespace | 15s | Bounded local memory write. |
| memory.delete | L2 | Per action | memory namespace | 15s | Removes information. |
| reminders.list | L0 | None | owner reminder store | 15s | Reads reminders. |
| reminders.create | L1 | None; audit | owner reminder store | 15s | Adds reminder. |
| reminders.update | L2 | Per action | owner reminder store | 15s | Changes reminder. |
| reminders.delete | L2 | Per action | owner reminder store | 15s | Removes reminder. |

Default adapter: none; this contract is vendor-agnostic. Swap candidates: any adapter satisfying documented interfaces.

## Hard-forbidden operations

| ID | Requirement | Verification |
|---|---|---|
| SEC-031 | The permission gate must reject every hard-forbidden operation regardless of approval, profile, or model output. | Test |

The following operations must never be allowed regardless of approval:

- Reading, writing, deleting, or enumerating system folders.
- Reading credential stores or browser password files.
- Disabling, weakening, or bypassing security software.
- Reading or writing outside configured allow-lists.

## Approval prompt requirements

| ID | Requirement | Verification |
|---|---|---|
| SEC-026 | An approval prompt must show the exact action, target, arguments, risk level, requesting source, and expiry. | Test |
| SEC-027 | An approval prompt must state whether [SEC-021](#sec-021) escalated the action for untrusted content. | Test |
| SEC-028 | The gate must default-deny an approval that expires, times out, is cancelled, or receives no response. | Test |
| SEC-029 | The gate must treat ambiguous, partial, or conflicting responses as denial and must not infer approval. | Test |
| SEC-030 | Approval for one action must not authorize another action, target, argument set, or later request. | Test |

## Profile overrides

| Profile | Allowed override | Required restriction |
|---|---|---|
| personal-pc | Enable wake word and personal allow-lists. | Must retain [SEC-017](#sec-017) through [SEC-030](#sec-030). |
| office-pc | Use hotkey only and disable mail. | Must apply policy-compatible provider/tool configuration under [SEC-024](#sec-024). |
| laptop | Enable both wake word and hotkey. | Must retain identical risk and approval rules. |

Profiles must not lower risk, remove L2/L3 approval, enable a hard-forbidden operation, widen access outside allow-lists, or make voice alone sufficient for L3.

## Related docs

- [Threat model](threat-model.md)
- [Security model](security-model.md)
- [F05: Tool system and permissions](../02-features/F05-tool-system-and-permissions.md)
- [F06: File tools](../02-features/F06-file-tools.md)
- [F12: Gmail](../02-features/F12-gmail.md)
- [F18: Shell tool](../02-features/F18-shell-tool.md)
- [ADR-0004: Provider-agnostic interfaces](../05-decisions/ADR-0004-provider-agnostic-interfaces.md)
- [Checklist](../06-checklist/CHECKLIST.md)

## Open questions

- Which actions are sufficiently reversible to remain L1? TO VERIFY.
- What final timeout policy suits slow or offline machines? TO VERIFY.
- Which recipient allow-list semantics suit personal mail? TO VERIFY.

## Change log

- 2026-11-02: Added Part 1 permission-level contract and tool action matrix.

