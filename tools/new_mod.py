#!/usr/bin/env python3
"""Generate a new independently installed character/feature mod."""
import argparse
import json
from pathlib import Path
if __package__:
    from .validate import ROOT, SLUG
else:
    from validate import ROOT, SLUG


def create(kind, slug, name, root=ROOT):
    if not SLUG.fullmatch(slug):
        raise ValueError("slug must be lower-case kebab-case, e.g. new-hero")
    if kind not in ("character", "feature"):
        raise ValueError("kind must be character or feature")
    if not name.strip():
        raise ValueError("name must be nonempty")
    assembly = "".join(part.capitalize() for part in slug.split("-"))
    namespace = "SodMod." + ("Characters" if kind == "character" else "Features") + "." + assembly
    folder = root / "mods" / ("characters" if kind == "character" else "features") / slug
    if folder.exists():
        raise FileExistsError(f"Mod already exists: {folder}")
    for sub in ("src", "about", "data", "assets"):
        (folder / sub).mkdir(parents=True, exist_ok=True)
    project = {"schemaVersion": 1, "kind": kind, "slug": slug, "assembly": assembly + ".dll", "project": "src/" + assembly + ".csproj", "modId": "com.zeroga.sodmod." + slug.replace("-", ""), "visualBackend": "not-applicable" if kind == "feature" else "unresolved"}
    metadata = {"id": project["modId"], "name": name + " (M0 Scaffold)", "author": "zeroga", "modVer": "0.0.1", "assemblies": [project["assembly"]]}
    (folder / "mod.project.json").write_text(json.dumps(project, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (folder / "about/metadata.json").write_text(json.dumps(metadata, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (folder / "src" / (assembly + ".csproj")).write_text(f"""<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <AssemblyName>{assembly}</AssemblyName>
    <RootNamespace>{namespace}</RootNamespace>
  </PropertyGroup>
  <ItemGroup>
    <Reference Include="Dew.Core"><HintPath>$(GameManagedDir)/Dew.Core.dll</HintPath><Private>false</Private></Reference>
    <Reference Include="UnityEngine.CoreModule"><HintPath>$(GameManagedDir)/UnityEngine.CoreModule.dll</HintPath><Private>false</Private></Reference>
    <Compile Include="../../../../shared/src/SodModLog.cs" Link="Shared/SodModLog.cs" />
  </ItemGroup>
  <Target Name="CheckGameReferences" BeforeTargets="ResolveReferences">
    <Error Condition="'$(GameDir)' == ''" Text="Set -p:GameDir=... or SOD_GAME_DIR." />
    <Error Condition="'$(GameDir)' != '' and !Exists('$(GameManagedDir)/Dew.Core.dll')" Text="Dew.Core.dll not found under $(GameManagedDir)." />
  </Target>
</Project>
""", encoding="utf-8")
    (folder / "src/ModEntry.cs").write_text(f"""using SodMod.Shared;

namespace {namespace}
{{
    public sealed class ModEntry : ModBehaviour
    {{
        private void Start()
        {{
            SodModLog.Info("{slug}", "Scaffold loaded; behavior not implemented.");
        }}
    }}
}}
""", encoding="utf-8")
    (folder / "assets/README.md").write_text("# Asset policy\n\nDo not commit extracted game assets or third-party resources without redistribution permission. `source/`, `private/`, and `runtime/` are gitignored.\n", encoding="utf-8")
    (folder / "data/README.md").write_text("# Mod-local editable data\n", encoding="utf-8")
    return folder


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--kind", choices=("character", "feature"), required=True)
    parser.add_argument("--slug", required=True)
    parser.add_argument("--name", required=True)
    args = parser.parse_args()
    try:
        folder = create(args.kind, args.slug, args.name)
    except (ValueError, FileExistsError) as exc:
        parser.error(str(exc))
    print("Created", folder.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
