# Architecture: multiple standalone mods in one repository

## Design decision

`sodmod` is a **monorepo**, not the name of one installable Mod. The unit of installation, testing, release, Workshop item, and version is the *individual mod*. A role mod and a feature mod may be enabled independently. Never assume installing one installs another.

```text
                         Shared build-time source + tools
                         /               |             \
         mods/characters/role-A   mods/characters/role-B   mods/features/feature-X
                 DLL A                    DLL B                   DLL X
                ZIP A                    ZIP B                   ZIP X
```

## Directories and boundaries

- `mods/characters/<slug>`: one playable character. Character-specific state machine, skills, assets, memory integration, model settings.
- `mods/features/<slug>`: one independently installable gameplay/utility change. No dependency on a character package.
- `shared/src`: reused **source** linked into each consuming assembly. At M0, it is limited to very small, stable helpers. This avoids a separate shared runtime DLL and the risk of assembly identity conflicts with Unity's Mod loader.
- `tools/`: repo-wide validation, creation, game-assembly compilation and packaging. No machine-specific absolute paths committed.
- `docs/`, `schemas/`, `tests/`: contracts, technical decisions and checks.
- `dist/`: untracked per-mod ZIP output; never include unrelated mods in one ZIP.

## Individual mod contract

Every mod contains:

```text
mod.project.json           # repository build/packaging manifest
about/metadata.json       # actual Shape of Dreams loader metadata
src/<Assembly>.csproj      # independent compilation target
src/ModEntry.cs            # ModBehaviour lifecycle, no unrelated features
data/                      # game-facing editable data owned by that mod
assets/source/             # private, gitignored; raw legally obtained source
assets/runtime/            # generated, gitignored; runtime-relative resources
assets/README.md           # copyright/status/source attribution notes
```

For any new character with a summon or multiple forms: **gameplay form state** (server-authoritative) is separate from **visual representation** (model swap, animations, VFX, SFX). Later adding an assembly animation should only require changes to the visual transition provider.

## Mod-specific logical layers (add only when implemented)

1. Bootstrap: ModBehaviour startup, cleanup, version capability probes, guarded logging.
2. Domain: pure C# rules, skill definitions, form states, cooldowns; no Unity types where possible.
3. Game adapters: instances, status, registration, skill dispatch and patch entry points.
4. Visuals: meshes, skeleton, animation, VFX/audio, camera and LOD.
5. Networking: authoritative state and client-side observation; Mirror interaction verified with real multiplayer.
6. Config/data: mod-local config, localization, user settings and migration.

The M0 package contains only a basic load-test entry point and pure form identifiers; the actual game registration, model loaders, networking and special effects are **future implementation tasks**, not pre-verified capabilities.

## Versioning and reliability

- Per-mod semantic versions in `about/metadata.json`; repository commits are shared and do not imply simultaneous releases.
- A change in common source may require testing all consumers.
- Explicit `game version tested` metadata lives in release notes, not in guesses.
- Harmony patches must be narrow and reverted on unload; no patch should leak across a mod reload.
- Asset loading should fail with a diagnosis and preferably a placeholder, not cause infinite per-frame logging.
- Keep high-risk dependencies (third-party format loaders, IL analysis, game APIs) behind an adapter.

## Build graph

`source assets -> licensed conversion -> assets/runtime -> compile individual DLL -> validate metadata -> package one ZIP -> game acceptance test -> release`.

The CI workflow without installed game binaries can **only** validate repository structure and pure-code tests. Real DLL compilation needs local game managed DLLs; in-game and co-op verification needs the game itself.
