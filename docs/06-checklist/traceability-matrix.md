# Traceability matrix

Purpose: map planned features to components, tools, requirements, tests, checklist work, and known gaps.

## Feature traceability

| Feature | Components | Tools | Requirements | Tests | Checklist | Gap |
|---|---|---|---|---|---|---|
| [F01](../02-features/F01-voice-loop.md) | core/trigger/audio/STT/LLM/TTS | — | FEAT-01-001/002; SEC/ARCH per feature links | Planned unit/contract/integration/safety/manual | [Phase 1](phase-1.md) | GAP: no owner; tests not implemented |
| [F02](../02-features/F02-hotkey-and-typed-input.md) | trigger/orchestrator/HUD | — | FEAT-02-001/002; SEC/ARCH per feature links | Planned unit/contract/integration/safety/manual | [Phase 1](phase-1.md) | GAP: no owner; tests not implemented |
| [F03](../02-features/F03-wake-word.md) | trigger/audio | — | FEAT-03-001/002; SEC/ARCH per feature links | Planned unit/contract/integration/safety/manual | [Phase 1](phase-1.md) | GAP: no owner; tests not implemented |
| [F04](../02-features/F04-provider-failover.md) | settings/adapters/orchestrator | — | FEAT-04-001/002; SEC/ARCH per feature links | Planned unit/contract/integration/safety/manual | [Phase 1](phase-1.md) | GAP: no owner; tests not implemented |
| [F05](../02-features/F05-tool-system-and-permissions.md) | registry/gate/audit | all tools | FEAT-05-001/002; SEC/ARCH per feature links | Planned unit/contract/integration/safety/manual | [Phase 2](phase-2.md) | GAP: no owner; tests not implemented |
| [F06](../02-features/F06-file-tools.md) | registry/gate/platform | files | FEAT-06-001/002; SEC/ARCH per feature links | Planned unit/contract/integration/safety/manual | [Phase 3](phase-3.md) | GAP: no owner; tests not implemented |
| [F07](../02-features/F07-app-tools.md) | registry/gate/platform | apps | FEAT-07-001/002; SEC/ARCH per feature links | Planned unit/contract/integration/safety/manual | [Phase 3](phase-3.md) | GAP: no owner; tests not implemented |
| [F08](../02-features/F08-system-info.md) | registry/gate/platform | system | FEAT-08-001/002; SEC/ARCH per feature links | Planned unit/contract/integration/safety/manual | [Phase 3](phase-3.md) | GAP: no owner; tests not implemented |
| [F09](../02-features/F09-startup-greeting.md) | greeting/settings/TTS | — | FEAT-09-001/002; SEC/ARCH per feature links | Planned unit/contract/integration/safety/manual | [Phase 4](phase-4.md) | GAP: no owner; tests not implemented |
| [F10](../02-features/F10-autostart.md) | autostart/platform | autostart | FEAT-10-001/002; SEC/ARCH per feature links | Planned unit/contract/integration/safety/manual | [Phase 4](phase-4.md) | GAP: no owner; tests not implemented |
| [F11](../02-features/F11-hud.md) | HUD/core | — | FEAT-11-001/002; SEC/ARCH per feature links | Planned unit/contract/integration/safety/manual | [Phase 5](phase-5.md) | GAP: no owner; tests not implemented |
| [F12](../02-features/F12-gmail.md) | registry/gate/audit | mail | FEAT-12-001/002; SEC/ARCH per feature links | Planned unit/contract/integration/safety/manual | [Phase 6](phase-6.md) | GAP: no owner; tests not implemented |
| [F13](../02-features/F13-calendar.md) | registry/gate/scheduler | calendar | FEAT-13-001/002; SEC/ARCH per feature links | Planned unit/contract/integration/safety/manual | [Phase 6](phase-6.md) | GAP: no owner; tests not implemented |
| [F14](../02-features/F14-make-tool.md) | registry/gate/platform | make | FEAT-14-001/002; SEC/ARCH per feature links | Planned unit/contract/integration/safety/manual | [Phase 7](phase-7.md) | GAP: no owner; tests not implemented |
| [F15](../02-features/F15-web-search.md) | registry/gate/LLM | web | FEAT-15-001/002; SEC/ARCH per feature links | Planned unit/contract/integration/safety/manual | [Phase 6](phase-6.md) | GAP: no owner; tests not implemented |
| [F16](../02-features/F16-reminders.md) | scheduler/registry/gate | reminders | FEAT-16-001/002; SEC/ARCH per feature links | Planned unit/contract/integration/safety/manual | [Phase 8](phase-8.md) | GAP: no owner; tests not implemented |
| [F17](../02-features/F17-notes-memory.md) | memory/registry/gate | memory | FEAT-17-001/002; SEC/ARCH per feature links | Planned unit/contract/integration/safety/manual | [Phase 8](phase-8.md) | GAP: no owner; tests not implemented |
| [F18](../02-features/F18-shell-tool.md) | registry/gate/platform | shell | FEAT-18-001/002; SEC/ARCH per feature links | Planned unit/contract/integration/safety/manual | [Phase 8](phase-8.md) | GAP: no owner; tests not implemented |
| [F19](../02-features/F19-offline-mode.md) | settings/adapters/core | — | FEAT-19-001/002; SEC/ARCH per feature links | Planned unit/contract/integration/safety/manual | [Phase 8](phase-8.md) | GAP: no owner; tests not implemented |
| [F20](../02-features/F20-profiles-and-setup.md) | settings/platform/safety | — | FEAT-20-001/002; SEC/ARCH per feature links | Planned unit/contract/integration/safety/manual | [Phase 0](phase-0.md) | GAP: no owner; tests not implemented |
| [F21](../02-features/F21-interruption.md) | core/state/TTS/audio | — | FEAT-21-001/002; SEC/ARCH per feature links | Planned unit/contract/integration/safety/manual | [Phase 8](phase-8.md) | GAP: no owner; tests not implemented |
| [F22](../02-features/F22-smart-home-slot.md) | registry/gate | — | FEAT-22-001/002; SEC/ARCH per feature links | Planned unit/contract/integration/safety/manual | [Phase 8](phase-8.md) | GAP: no owner; tests not implemented |
| [F23](../02-features/F23-screen-vision.md) | interfaces/registry/gate | — | FEAT-23-001/002; SEC/ARCH per feature links | Planned unit/contract/integration/safety/manual | [Phase 8](phase-8.md) | GAP: no owner; tests not implemented |

## Cross-cutting traceability

| Item | Requirement/threat IDs | Planned test evidence | Gap |
|---|---|---|---|
| Tool safety | SEC-001, SEC-013, SEC-020, SEC-021, SEC-031 | Schema, permission, approval, red-team tests | GAP: tests and owner not implemented/assigned. |
| Privacy/secrets | SEC-032–SEC-039 | Secret/redaction/config tests | GAP: tests and owner not implemented/assigned. |
| HUD/local channel | SEC-005, SEC-040, ARCH-057–059, THR-003 | Handshake/origin/token/rate tests | GAP: tests and owner not implemented/assigned. |
| Lifecycle/failover | ARCH-010–030, ARCH-033, THR-011–013 | Integration/fault-injection/soak tests | GAP: tests and owner not implemented/assigned. |
| Threat register | THR-001–014 | Red-team RT-001–010 and edge cases EDGE-001–015 | GAP: several threats lack dedicated executable test; no owner assigned. |
| Contract/data | ARCH-031–065 | Contract/schema/manifest tests | GAP: contract files are placeholders; no owner assigned. |

## GAP register

- GAP-001: F01–F23 have no assigned owner.
- GAP-002: FEAT-F01-001 through FEAT-F23-002 are documented but have no implemented executable tests.
- GAP-003: SEC-001–SEC-058 and ARCH-001–ARCH-065 have planned verification but no assigned owner; implementation/test evidence is incomplete.
- GAP-004: THR-001–THR-014 have no assigned owner; threat-to-executable-test coverage is incomplete.
- GAP-005: Numeric coverage targets, soak duration, resource budgets, and several provider/platform feasibility decisions remain TO VERIFY.

## Related docs

- [Feature index](../02-features/feature-index.md)
- [Test strategy](../04-testing/test-strategy.md)
- [Edge-case catalogue](../04-testing/edge-case-catalogue.md)
- [Master checklist](CHECKLIST.md)

## Open questions

- Who owns each feature, security control, and test suite? TO VERIFY.
- Which GAPs must close before Phase 1 implementation begins? TO VERIFY.

## Change log

- 2026-11-03: Added Part 6 traceability matrix and GAP register.
