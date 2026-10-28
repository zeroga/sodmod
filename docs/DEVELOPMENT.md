# Development and build

## Prerequisites

- Python 3.10 or newer for manifest validation, scaffolding and packaging.
- .NET SDK capable of `netstandard2.1` compilation for the C# loader.
- A legally installed copy of *Shape of Dreams* on Windows. `Dew.Core.dll` and Unity managed DLLs must be read from your own game installation and **never pushed to Git**.
- Unity Editor is **not** a requirement for initial C# compilation. Later model/animation import can use a runtime loader or an editor-built asset backend; both are under investigation.

## Create a new independent mod

```powershell
python tools/new_mod.py --kind character --slug next-character --name "Next Character"
python tools/new_mod.py --kind feature --slug independent-feature --name "Independent Feature"
python tools/validate.py
```

The generator creates one project, one metadata ID and one entry point per mod. It will not overwrite an existing directory.

## Build

```powershell
$env:SOD_GAME_DIR = 'D:\SteamLibrary\steamapps\common\Shape of Dreams'
powershell -ExecutionPolicy Bypass -File tools/build.ps1 -Mod characters/herrscher-of-truth
```

Or use `-GameDir "D:\...\Shape of Dreams"` explicitly. Build expects `Shape of Dreams_Data/Managed/Dew.Core.dll`, `UnityEngine.CoreModule.dll`, and their dependencies. The exact reference list may need adjusting to the installed game version.

`tools/build.ps1` first validates metadata, then compiles one `csproj`, and then packages its DLL plus that mod's public runtime resources. It never packages all mods together.

## Packaging only

```powershell
python tools/package.py --mod characters/herrscher-of-truth --configuration Release
```

This deliberately fails if the compiled DLL is missing. The ZIP contains a single top-level mod folder so it can be extracted to your chosen Mods root; the DLL, `about/metadata.json`, `data/`, and licensed `assets/runtime/` files appear inside that folder.

## Verification levels

- L0: `validate.py` and repository tests pass. **Only structure is proven.**
- L1: game DLL compilation succeeds.
- L2: Mod loads into the game, as confirmed by actual log and UI; no gameplay crashes.
- L3: new character can be selected, animated, transformed, and played through rooms.
- L4: verified multiplayer, game restart, mod reload, and recovery from missing assets.

No release may claim L2–L4 based only on automated tests or another author's mod.
