# Contribution instructions for coding agents

This repository contains multiple independent *Shape of Dreams* Mods. Do not collapse them into one DLL.

- First identify the target mod (`mods/characters/<slug>` or `mods/features/<slug>`).
- Make shared changes only for behavior proven reusable; do not add dependencies between individual mods.
- Preserve `about/metadata.json` ID and assembly list. Every new mod has its own ID and ZIP.
- Never copy another Mod's source without a compatible license. Analyze third-party source for technical insights, write original implementations.
- Do not commit game assemblies, extracted proprietary character assets, workshop binaries or private audio/model files.
- Do not claim the mod works in-game unless an actual game-launch log confirms it. Treat CI structure checks as insufficient proof of game compatibility.
- Test scripts: `python tools/validate.py` and `python -m unittest discover -s tests -v`.
- Build scripts require `SOD_GAME_DIR` or `-GameDir`; `dotnet` only compiles, and does not require Unity Editor.
- Do not add an AssetBundle-only requirement until runtime 3D model loading is investigated. Keep visual backend replaceable.
- Game code and source may change with version updates; keep patch sites isolated and unload/reload cleanup symmetric.
- Keep the authoritative gameplay state separate from client-side cosmetic animation and audio.

Read `docs/ARCHITECTURE.md` before creating new modules or dependencies.
