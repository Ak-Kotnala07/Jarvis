+# Configuration specification

Purpose: define validated configuration, profile differences, precedence, and failure behavior.

## Configuration requirements

| ID | Requirement | Verification |
|---|---|---|
| ARCH-051 | Settings must apply precedence in this order: defaults, profile, user file, then environment. | Settings test. |
| ARCH-052 | Settings must reject invalid types, unknown unsafe values, and policy-weakening overrides before startup reaches idle. | Validation test. |
| ARCH-053 | Sensitive mode must select local STT, LLM, and TTS adapters and reject a configuration that cannot do so. | Profile test. |
| ARCH-054 | Secrets must be referenced by name only and resolved outside configuration files. | Review and secret test. |

## Key catalog

| Path | Type | Default | Allowed values / validation | Profile difference | Reader |
|---|---|---|---|---|---|
| `user.name` | string | `"Example User"` | Non-empty, no secret value. | Per owner. | greeting, settings |
| `trigger.wake_word_enabled` | boolean | `true` | Boolean. | Office false; laptop/personal true. | trigger |
| `trigger.hotkey_enabled` | boolean | `true` | Boolean; at least one activation route or typed input available. | Office true; laptop true; personal false in example. | trigger |
| `trigger.wake_word` | string | `"jarvis"` | Non-empty when wake word enabled. | Personal/laptop only. | trigger |
| `trigger.hotkey` | string | `"ctrl+shift+j"` | Valid platform hotkey syntax TO VERIFY. | Office/laptop. | trigger |
| `providers.stt_failover` | ordered string array | `[]` | Unique configured adapter names; non-empty unless typed-only. | Sensitive mode local-only. | settings, registry |
| `providers.llm_failover` | ordered string array | `[]` | Unique configured adapter names; non-empty for reasoning. | Sensitive mode local-only. | settings, registry |
| `providers.tts_failover` | ordered string array | `[]` | Unique configured adapter names; non-empty unless text-only. | Sensitive mode local-only. | settings, registry |
| `sensitive_mode` | boolean | `true` | Boolean; true requires local compatible adapters. | Office default TO VERIFY. | settings, adapters |
| `paths.allowed_folders` | string array | `[]` | Canonical user folders only; no system folders; no duplicates. | Narrow per machine. | permission gate, files |
| `apps.allowed` | string array | `[]` | Approved application identifiers only. | Office policy-narrowed. | permission gate, apps |
| `shell.allowed_commands` | string array | `[]` | Exact approved command identifiers only; empty disables shell. | Office empty by default. | permission gate, shell |
| `permissions.overrides` | object | `{}` | May narrow/disable only; may not lower risk or weaken L2/L3 approval. | Office may disable more. | permission gate |
| `limits.max_tool_calls_per_request` | integer | `5` | Integer greater than zero. | May lower only. | orchestrator |
| `limits.request_seconds` | integer | `TO VERIFY` | Positive integer when set. | May lower only. | orchestrator |
| `limits.daily_token_budget` | integer | `TO VERIFY` | Nonnegative; zero means no cloud token use. | Office policy may set zero. | orchestrator |
| `limits.provider_rate_retry_count` | integer | `1` | Must equal 0 or 1 under bounded failover rule. | Same. | adapters |
| `greeting.enabled` | boolean | `true` | Boolean. | May disable. | greeting |
| `hud.enabled` | boolean | `false` | Boolean. | Per machine. | HUD server |
| `hud.host` | string | `"127.0.0.1"` | Must be exactly `127.0.0.1`. | No override to remote host. | HUD server |
| `hud.port` | integer | `8765` | Unprivileged valid port; collision fails degraded. | Per machine. | HUD server |
| `autostart.enabled` | boolean | `false` | Boolean; platform support required. | Office requires policy approval. | autostart |
| `logging.level` | string | `"INFO"` | DEBUG, INFO, WARNING, ERROR; no secrets regardless. | May increase restriction. | audit/logging |
| `logging.retention_days` | integer | `TO VERIFY` | Positive policy-approved value. | Office policy-controlled. | audit log |
| `secrets.<reference>` | string reference | absent | Keychain/env reference name only; never a literal secret. | Per machine. | secret resolver |

## Worked profiles

### personal-pc

```yaml
trigger: {wake_word_enabled: true, hotkey_enabled: false, wake_word: "jarvis"}
sensitive_mode: false
paths: {allowed_folders: ["~/Documents"]}
apps: {allowed: ["notepad"]}
shell: {allowed_commands: ["echo"]}
hud: {enabled: false, host: "127.0.0.1", port: 8765}
autostart: {enabled: false}
```

### office-pc

```yaml
trigger: {wake_word_enabled: false, hotkey_enabled: true, hotkey: "ctrl+shift+j"}
sensitive_mode: true
paths: {allowed_folders: []}
apps: {allowed: []}
shell: {allowed_commands: []}
permissions: {overrides: {mail: {enabled: false}}}
hud: {enabled: false, host: "127.0.0.1", port: 8765}
autostart: {enabled: false}
```

### laptop

```yaml
trigger: {wake_word_enabled: true, hotkey_enabled: true, wake_word: "jarvis", hotkey: "ctrl+shift+j"}
sensitive_mode: true
paths: {allowed_folders: ["~/Documents"]}
apps: {allowed: []}
shell: {allowed_commands: []}
hud: {enabled: false, host: "127.0.0.1", port: 8765}
autostart: {enabled: false}
```

## Precedence and invalid configuration

1. Built-in safe defaults apply first.
2. A named profile overlays defaults.
3. A user configuration file overlays the profile.
4. Environment values overlay only permitted non-secret settings; secret references resolve through keychain or untracked environment.
5. A later value may narrow capability but must not weaken fixed security requirements.

Invalid config, a missing required key, unresolved required secret reference, or unsafe override must prevent the affected capability from starting. If no safe degraded path exists, startup is fatal; otherwise core enters degraded mode and reports the affected capability.

## Related docs

- [Settings component](components/settings.md)
- [Security model](../03-security/security-model.md)
- [Permission levels](../03-security/permission-levels.md)
- [F20: Profiles and setup](../02-features/F20-profiles-and-setup.md)

## Open questions

- Which environment keys may override non-secret user settings? TO VERIFY.
- What approved token and request budget values apply per profile? TO VERIFY.

## Change log

- 2026-11-03: Added Part 5 configuration specification.

