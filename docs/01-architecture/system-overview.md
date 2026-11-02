# System overview

Purpose: describe the system architecture and enforced boundaries.

## Architecture rules

1. `core` imports only from `interfaces`, `safety`, and `settings`; it never imports `adapters` or `tools` directly. Adapters and tools are loaded by name from configuration via a registry.
2. Every tool call passes through `safety.permission_gate`; `safety` never imports from `tools`.
3. OS-specific code lives only under `platform/`; no other package imports OS-specific libraries.
4. One tool is one folder containing `tool.yaml`, `schema.py`, `executor.py`, and `__init__.py`.
5. Every adapter is testable through a shared contract suite in `tests/contract/`.
6. The HUD is a separate frontend using a local `127.0.0.1` WebSocket; the core runs without it.
7. Runtime data (logs, database, tokens, and AI-generated files) lives outside the repository in the OS user-data directory.
8. Risk levels are L0 read-only, L1 safe write, L2 modify (ask), and L3 destructive/external (always ask).

## TODO

- TODO

