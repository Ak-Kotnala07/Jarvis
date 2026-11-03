# Test strategy

Purpose: define layered verification, fixtures, cadence, coverage, soak, and regression policy.

| ID | Requirement | Verification |
|---|---|---|
| TEST-001 | Every requirement must map to a test or be marked GAP. | Matrix review. |
| TEST-002 | Adapter contract tests must run unchanged against every swappable adapter. | Contract suite. |
| TEST-003 | Tests must use fake data and no production credentials, mail, or live provider calls. | Review. |
| TEST-004 | Any model/adapter change must run contract, failover, safety, and affected integration regressions. | CI review. |

## Test layers

| Layer | Purpose | Examples |
|---|---|---|
| Unit | Isolated validation/state. | Schema, risk escalation, config merge. |
| Contract | Provider-independent behavior. | Envelope, cancellation, normalized tool call. |
| Integration | Components with fakes. | Trigger → STT → core → TTS; HUD reconnect. |
| Safety | Adversarial boundaries. | Injection, traversal, approval denial. |
| Manual | Device/voice/OS UX. | Mic indicator, hotkey, kill switch. |
| Soak | Repeated bounded work. | Trigger/failover/cancel cycles. |

Contract suites make adapters swappable: candidates must preserve envelope, taxonomy, healthcheck, cancellation, tool normalization, and redaction in [components and contracts](../01-architecture/components-and-contracts.md).

## Fixtures and cadence

- Fixtures use clearly fake audio, mail, calendar, paths, tokens, names, and addresses.
- Every commit runs unit, contract, manifest/schema, link, and safety regressions.
- Nightly runs full integration, dependency scan, failover, and soak sample.
- Manual/release runs microphone/device/hotkey, office-policy, accessibility, and kill-switch checks.

Coverage targets and soak duration are TO VERIFY. Until approved, every changed requirement needs a direct test mapping; soak fails on leak, unbounded queue, repeated action, or missing audit record.

## Regression policy

Any model/adapter change must rerun adapter contracts, [F04](../02-features/F04-provider-failover.md), [F05](../02-features/F05-tool-system-and-permissions.md), affected feature integrations, and red-team cases; behavioral change also updates requirements, traceability, and owner review.

## Related docs

- [Edge-case catalogue](edge-case-catalogue.md)
- [Red-team cases](red-team-cases.md)
- [Traceability matrix](../06-checklist/traceability-matrix.md)

## Open questions

- What numeric coverage and soak targets are approved? TO VERIFY.

## Change log

- 2026-11-03: Completed Part 6 test strategy.

