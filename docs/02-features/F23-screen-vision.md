# F23: Screen vision

- Priority: Future
- Status: Not started
- Summary: Scope note: this capability is deferred and must not widen current permissions.

## Behaviour

Extension point: Interfaces, tool registry, permission gate. It may be designed only through the existing registry, permission-gate, and adapter/tool contracts; no implementation commitment exists.

## Tools / Components involved

[components catalog](../01-architecture/components-and-contracts.md), [orchestrator](../01-architecture/components/orchestrator.md), [permission gate](../01-architecture/components/permission-gate.md). No tool executor.

## Requirements

| ID | Requirement | Verification |
|---|---|---|
| FEAT-23-001 | Screen vision must remain unavailable until its extension-point contract and L0–L3 classification are approved. | Review |

## Edge cases

Scope deferred; no runtime edge-case commitments before design approval.

## Tests

- [ ] Manual: verify the feature remains disabled by default.

## Done when

- [ ] Owner-approved scope, threat review, contract, and phase plan exist.

## Dependencies

- Depends on Phase 8 planning and [F05](F05-tool-system-and-permissions.md).

## Related docs

- [Feature index](feature-index.md)
- [Permission levels](../03-security/permission-levels.md)
- [Checklist](../06-checklist/CHECKLIST.md)

## Open questions

- What owner-approved use case justifies this extension? TO VERIFY.

## Change log

- 2026-11-03: Completed Part 6 deferred-feature scope.
