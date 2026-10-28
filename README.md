# sodmod — Shape of Dreams mod monorepo

A **multi-mod** development workspace for *Shape of Dreams* (`app/2444750`). Each playable character and each gameplay/utility feature is a standalone Mod with its own assembly, mod metadata, version, and installable ZIP. Shared source, asset tooling, and CI are centralized, but **players never need to install unrelated mods**.

## Status

**M0 scaffold only:** source organization, a minimal load-test DLL project for Herrscher of Truth, manifests, validation, packaging and extension tooling. **No character has been registered and no original character assets are included.** Game runtime load and co-op behavior are untested.

## Layout

```text
mods/
  characters/herrscher-of-truth/  # first character, dedicated DLL and release
  features/                      # standalone feature mods go here
shared/src/                     # linked at compile time; not a runtime dependency
schemas/                        # project manifest schema
tools/                          # create, validate, build and package
.github/workflows/              # repository validation without proprietary game files
docs/                           # architecture, milestones and asset policies
dist/                           # ignored, generated ZIPs
```

## Quick start (Windows, game installed)

```powershell
python tools/validate.py
python -m unittest discover -s tests
python tools/new_mod.py --kind feature --slug example-feature --name "Example Feature"
$env:SOD_GAME_DIR = 'D:\SteamLibrary\steamapps\common\Shape of Dreams'
powershell -File tools/build.ps1 -Mod characters/herrscher-of-truth
```

The build requires the game's **local** managed DLLs under `Shape of Dreams_Data/Managed`. They are not distributed with the repository. If `dotnet` or the game isn't installed yet, `validate.py` and the repository tests can still run. The packager refuses to produce an installable ZIP if the target DLL does not exist.

## Key rules

1. **One mod = one release.** Characters and features do not share runtime assembly dependencies by default.
2. Each mod owns `about/metadata.json`, `mod.project.json`, `src/`, `data/`, and `assets/`.
3. Shared logic may be *linked as source* during compilation. Do not deploy or load a universal `sodmod.dll` until cross-mod assembly-loading behavior is verified.
4. Never commit extracted game binaries, third-party mod DLLs, unauthorized character models, voice files, animations, or proprietary textures. Public assets require a license record.
5. Gameplay authority, network state, visuals, and configuration are separate responsibilities. Model switching must not be intertwined with form/skill logic.
6. Every feature proceeds through its own PR and compatibility/test record. `main` is the reviewed baseline.

See [architecture](docs/ARCHITECTURE.md), [development](docs/DEVELOPMENT.md), [asset pipeline](docs/ASSETS.md), and [roadmap](docs/ROADMAP.md).
