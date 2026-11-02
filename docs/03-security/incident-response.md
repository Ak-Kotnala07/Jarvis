# Incident response

Purpose: provide repeatable owner runbooks for security and privacy incidents.

## Incident requirements

| ID | Requirement | Verification |
|---|---|---|
| IR-001 | Every suspected incident must preserve redacted evidence before destructive cleanup where doing so does not prolong harm. | Tabletop exercise |
| IR-002 | Every incident must contain active access or execution before recovery begins. | Tabletop exercise |
| IR-003 | Every incident must record root cause, scope, corrective action, and owner decision in the audit trail. | Review |
| IR-004 | Every incident runbook must update preventive controls or document why no change is required. | Review |

## Leaked API key

| Stage | Steps |
|---|---|
| Detect | Identify secret-scan alert, provider alert, unexpected billing, or observed key exposure. |
| Contain | Disable affected adapter and revoke the key at its provider immediately. |
| Recover | Create replacement key, store it under [SEC-032](security-model.md#sec-032), restart adapter, and test a non-sensitive request. |
| Review | Preserve redacted commit/log evidence; identify exposure path and affected requests. |
| Prevent | Apply [SEC-033](security-model.md#sec-033) and [SEC-035](security-model.md#sec-035); add a regression secret-scan check. |

## Token compromise

| Stage | Steps |
|---|---|
| Detect | Treat unknown provider activity, account notices, or missing token state as compromise. |
| Contain | Revoke provider token, disable the integration, and remove local keychain entries. |
| Recover | Reauthorize with minimum scopes under [SEC-038](security-model.md#sec-038); verify selected account and scopes. |
| Review | Review redacted audit records for reads, drafts, sends, and calendar changes. |
| Prevent | Narrow scopes, review device access, and document root cause under [IR-003](#ir-003). |

## Unwanted action

| Stage | Steps |
|---|---|
| Detect | Capture request ID, audit record, visible result, and owner report. |
| Contain | Trigger kill switch; disable the involved tool or profile. |
| Recover | Undo only with an owner-reviewed action: restore file, revoke draft/send follow-up, or correct calendar item as applicable. |
| Review | Compare transcript, tool arguments, risk level, approval channel, and result to [SEC-013](threat-model.md#sec-013). |
| Prevent | Fix missing validation, approval presentation, allow-list, or escalation test before re-enabling. |

## Mic stuck on

| Stage | Steps |
|---|---|
| Detect | Live-mic indicator remains active after cancellation, timeout, or device change. |
| Contain | Use hard mute/kill switch; revoke OS microphone access if capture does not stop. |
| Recover | Restart only the audio path after verifying no capture session is active; verify device selection. |
| Review | Preserve timestamps and device-change events. |
| Prevent | Test [SEC-011](threat-model.md#sec-011) and [SEC-045](security-model.md#sec-045) for the affected device. |

## Suspected prompt injection

| Stage | Steps |
|---|---|
| Detect | Treat instructions inside email, web, file, or tool output that request hidden actions, policy changes, or data disclosure as suspicious. |
| Contain | Do not approve proposals derived from the content; stop the request and preserve the source identifier. |
| Recover | Resume only with a new owner-authored request that names the intended action and target. |
| Review | Inspect whether [SEC-003](threat-model.md#sec-003) and [SEC-021](permission-levels.md#sec-021) applied. |
| Prevent | Add a redacted case to the injection test corpus and adjust extraction/approval boundaries. |

## Unexpected network calls

| Stage | Steps |
|---|---|
| Detect | Treat firewall, proxy, provider, or audit evidence of an unconfigured destination as suspicious. |
| Contain | Kill switch, disconnect affected adapter, and block destination through local policy where available. |
| Recover | Re-enable only after identifying the responsible component and validating configured provider endpoints. |
| Review | Compare event data against [SEC-036](security-model.md#sec-036) and [SEC-037](security-model.md#sec-037). |
| Prevent | Add endpoint allow-list coverage and a regression test; provider behavior is TO VERIFY. |

## Repository accidentally contains secrets

| Stage | Steps |
|---|---|
| Detect | Treat scanner findings, commit review, or public-repository exposure as an incident. |
| Contain | Revoke exposed values immediately; make repository private if necessary; stop further pushes. |
| Recover | Remove secret from current files and rewrite history only after the owner confirms the repository and collaborators in scope. |
| Review | Identify every clone, release, log, and provider access that may have received the secret. |
| Prevent | Enforce [SEC-033](security-model.md#sec-033), [SEC-035](security-model.md#sec-035), and pre-push scanning. |

## Related docs

- [Security model](security-model.md)
- [Threat model](threat-model.md)
- [Permission levels](permission-levels.md)
- [Safe mode](safe-mode.md)
- [Checklist](../06-checklist/CHECKLIST.md)

## Open questions

- What owner-approved evidence-retention period applies to incident material? TO VERIFY.
- Which incident notifications are required on office PCs? TO VERIFY.

## Change log

- 2026-11-02: Added Part 2 incident-response runbooks.
