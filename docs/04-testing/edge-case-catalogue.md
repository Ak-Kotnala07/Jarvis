# Edge-case catalogue

Purpose: consolidate de-duplicated, testable edge cases across features.

| ID | Category | Case | Features | Test |
|---|---|---|---|---|
| EDGE-001 | Audio | Empty capture produces no tool call. | [F01](../02-features/F01-voice-loop.md), F03 | Integration |
| EDGE-002 | Audio | Device change stops capture safely. | F01, F02 | Manual |
| EDGE-003 | Audio | False wake-word burst is rate limited. | F03 | Safety |
| EDGE-004 | LLM | Invalid tool format is normalized then rejected. | F04, F05 | Contract |
| EDGE-005 | LLM | Rate limit fails over once without loop. | F04 | Integration |
| EDGE-006 | LLM | Repeated proposal reaches loop limit. | F01, F05 | Safety |
| EDGE-007 | Files | `../` traversal is denied. | F06 | Safety |
| EDGE-008 | Files | Symlink outside allow-list is denied. | F06 | Safety |
| EDGE-009 | Mail/web | Untrusted content cannot authorize action. | F12, F15 | Safety |
| EDGE-010 | Mail/web | Send approval expiry creates no send. | F12 | Integration |
| EDGE-011 | System/lifecycle | HUD disconnect does not interrupt core. | F11 | Integration |
| EDGE-012 | System/lifecycle | Shutdown cancels pending bounded work. | F01, F21 | Integration |
| EDGE-013 | Security | Voice-only L3 approval is denied. | F05, F18 | Safety |
| EDGE-014 | Security | Secret-like content is redacted. | F05, F17 | Safety |
| EDGE-015 | Security | Safe mode disables write/execution. | F05, F18 | Safety |

## Related docs

- [Test strategy](test-strategy.md)
- [Red-team cases](red-team-cases.md)
- [Threat model](../03-security/threat-model.md)

## Open questions

- Which platform-specific cases need distinct IDs? TO VERIFY.

## Change log

- 2026-11-03: Completed Part 6 consolidated edge cases.

