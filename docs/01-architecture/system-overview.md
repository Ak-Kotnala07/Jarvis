+# System overview

Purpose: define the layered assistant architecture and enforceable dependency boundaries.

## Layered design

```text
Trigger / Audio / HUD frontend
          |       |
      interfaces  local WebSocket
          |
core <--> safety <--> settings
 |                     |
 registry          configuration
 |                     |
adapters          tools --> platform
```

| Layer | Responsibility |
|---|---|
| interfaces | Stable trigger, audio, STT, LLM, TTS, and tool contracts. |
| core | Request/state orchestration using only allowed layers. |
| safety | Permission, risk, allow-list, and audit decisions. |
| settings | Configuration and external runtime-data paths. |
| adapters | Configured interface implementations. |
| tools | One capability manifest, schema, and executor per folder. |
| platform | OS-specific integration only. |
| HUD | Optional separate frontend; core never requires it. |

## Architecture requirements

| ID | Requirement | Enforcement |
|---|---|---|
| ARCH-001 | Core must import only interfaces, safety, and settings and must not import adapters or tools directly. | Import-linter, test, review. |
| ARCH-002 | Adapters and tools must be selected by configured registry name rather than direct core imports. | Integration test, review. |
| ARCH-003 | Safety must not import tools, and every tool invocation must pass through the permission gate. | Import-linter, test, review. |
| ARCH-004 | OS-specific libraries and implementation must exist only under platform. | Import-linter, review. |
| ARCH-005 | Every tool must occupy one folder containing `tool.yaml`, `schema.py`, `executor.py`, and `__init__.py`. | Manifest test, review. |
| ARCH-006 | Every adapter must satisfy its shared interface contract and contract-test suite. | Contract test. |
| ARCH-007 | The HUD must use only a local WebSocket and core must run when the HUD is absent or crashed. | Integration test. |
| ARCH-008 | Runtime logs, databases, tokens, and AI-generated files must live outside the repository. | Integration test, review. |
| ARCH-009 | All machines must run the same codebase, with behavior narrowed only by reviewed profiles and configuration. | Profile test, review. |

## What changes when the AI changes

| Capability swapped | Files/config entries that change | Must not change |
|---|---|---|
| Trigger | One file under `src/jarvis/adapters/trigger/`; trigger config/profile selection. | `interfaces/trigger.py`, core, safety, tool manifests. |
| STT | One file under `src/jarvis/adapters/stt/`; `providers.stt_failover`. | `interfaces/stt.py`, core, tool schemas, risk levels. |
| LLM | One file under `src/jarvis/adapters/llm/`; `providers.llm_failover` and local/remote selection. | `interfaces/llm.py`, permission gate, executors, approval behavior. |
| TTS | One file under `src/jarvis/adapters/tts/`; `providers.tts_failover`. | `interfaces/tts.py`, core state machine, safety controls. |
| Local fallback | Adapter registration/configuration and contract tests. | Public interfaces, audit schema, L0–L3 meanings. |

Default adapter: none. Swap candidates: any contract-compliant adapter selected by configuration.

## Related docs

- [Components and contracts](components-and-contracts.md)
- [Process model](process-model.md)
- [Request lifecycle](request-lifecycle.md)
- [State machine](state-machine.md)
- [Startup and shutdown](startup-shutdown.md)
- [ADR-0004](../05-decisions/ADR-0004-provider-agnostic-interfaces.md)
- [F04](../02-features/F04-provider-failover.md)

## Open questions

- What registry discovery mechanism avoids widening core imports? TO VERIFY.
- Which platform libraries are acceptable per OS? TO VERIFY.

## Change log

- 2026-11-02: Added Part 3 layered architecture and dependency requirements.

