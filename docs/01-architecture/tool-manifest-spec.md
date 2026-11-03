# Tool manifest specification

Purpose: define the vendor-neutral `tool.yaml` contract and registry validation process.

## Manifest requirements

| ID | Requirement | Verification |
|---|---|---|
| ARCH-060 | Every registered tool must provide a valid manifest before its executor can be resolved. | Manifest test. |
| ARCH-061 | A manifest must classify each action with fixed L0–L3 risk and must not permit configuration to lower it. | Validation test. |
| ARCH-062 | Registry must reject invalid, duplicate, unsupported, or policy-weakening manifests before execution. | Registry test. |

## Format

```yaml
name: files
description: "TODO"
version: "1"
actions:
  read:
    risk_level: L0
    timeout_seconds: 30
    parameters:
      type: object
      properties: {}
      additionalProperties: false
    allow_list_requirements: ["paths.allowed_folders"]
    untrusted_output: true
    platform_support: ["windows", "macos", "linux"]
```

| Field | Type | Rule |
|---|---|---|
| name | string | Lowercase unique tool namespace. |
| description | string | Non-empty owner-readable statement. |
| version | string | Manifest compatibility version. |
| actions | object | One or more unique action names. |
| actions.*.risk_level | enum | L0, L1, L2, or L3; fixed semantics. |
| actions.*.timeout_seconds | integer | Positive and within global limit. |
| actions.*.parameters | JSON Schema object | Must reject undeclared unsafe arguments. |
| actions.*.allow_list_requirements | string array | Refer only to documented configuration keys. |
| actions.*.untrusted_output | boolean | True where returned content can influence an LLM. |
| actions.*.platform_support | string array | Subset of windows, macos, linux. |

## Registry flow

1. Discover configured tool folders by registry name.
2. Parse manifest and validate structure, version, unique names, action schema, risk, timeout, allow-list keys, and platform support.
3. Bind schema and executor only after validation.
4. Reject a duplicate name, unknown risk, absent action, invalid JSON schema, unsupported platform, forbidden allow-list reference, or timeout outside limits.
5. Return a redacted `Unsupported` or `InvalidResponse` result; no rejected manifest may reach an executor.

## Related docs

- [Components and contracts](components-and-contracts.md)
- [Tool registry component](components/tool-registry.md)
- [Permission levels](../03-security/permission-levels.md)
- [F05: Tool system and permissions](../02-features/F05-tool-system-and-permissions.md)

## Open questions

- How are backward-incompatible manifest versions migrated? TO VERIFY.
- Which JSON Schema draft will be fixed for all manifests? TO VERIFY.

## Change log

- 2026-11-03: Added Part 5 tool-manifest specification.
