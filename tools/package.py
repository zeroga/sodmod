#!/usr/bin/env python3
"""Package one compiled Mod; never silently publish a stub without a DLL."""
import argparse
import json
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
if __package__:
    from .validate import ROOT, check_project
else:
    from validate import ROOT, check_project


def package(mod, configuration="Release", root=ROOT):
    mod_path = Path(mod)
    if mod_path.is_absolute() or len(mod_path.parts) != 2 or mod_path.parts[0] not in ("characters", "features"):
        raise ValueError("--mod must be characters/<slug> or features/<slug>")
    folder = root / "mods" / mod_path
    kind = "character" if mod_path.parts[0] == "characters" else "feature"
    if not folder.is_dir():
        raise ValueError(f"Mod does not exist: {mod}")
    issues = check_project(kind, folder)
    if issues:
        raise ValueError("; ".join(issues))
    m = json.loads((folder / "mod.project.json").read_text(encoding="utf-8"))
    dll = folder / "src/bin" / configuration / "netstandard2.1" / m["assembly"]
    if not dll.is_file():
        raise FileNotFoundError(f"Compiled DLL missing: {dll}. Build this mod first.")
    version = json.loads((folder / "about/metadata.json").read_text(encoding="utf-8"))["modVer"]
    dest = root / "dist" / f"{m['slug']}-{version}.zip"
    dest.parent.mkdir(parents=True, exist_ok=True)
    top = m["slug"]
    with ZipFile(dest, "w", ZIP_DEFLATED) as archive:
        archive.write(dll, f"{top}/{m['assembly']}")
        for source_dir, destination_dir in (("about", "about"), ("data", "data"), ("assets/runtime", "")):
            base = folder / source_dir
            if not base.exists():
                continue
            for file in sorted(base.rglob("*")):
                if not file.is_file():
                    continue
                relative = file.relative_to(base)
                # No source README or placeholder .md text in shipped package.
                if file.suffix.lower() == ".md":
                    continue
                archive.write(file, f"{top}/{destination_dir}/{relative}".replace("//", "/"))
    return dest


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mod", required=True, help="characters/<slug> or features/<slug>")
    parser.add_argument("--configuration", default="Release", choices=("Debug", "Release"))
    args = parser.parse_args()
    try:
        output = package(args.mod, args.configuration)
    except (ValueError, FileNotFoundError) as exc:
        parser.error(str(exc))
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
