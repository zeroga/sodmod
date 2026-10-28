#!/usr/bin/env python3
"""Validate the independent Mod package contract without third-party libraries."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = re.compile(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$")
IDENTITY = re.compile(r"^com\.zeroga\.sodmod\.[a-z0-9]+$")
ASSEMBLY = re.compile(r"^[A-Za-z][A-Za-z0-9]*\.dll$")


def discover(root=ROOT):
    for kind, plural in (("character", "characters"), ("feature", "features")):
        base = root / "mods" / plural
        for manifest in sorted(base.glob("*/mod.project.json")):
            yield kind, manifest.parent


def check_project(kind, folder):
    problems = []
    manifest_path = folder / "mod.project.json"
    try:
        project = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
        meta = json.loads((folder / "about/metadata.json").read_text(encoding="utf-8-sig"))
    except (ValueError, OSError) as exc:
        return [f"{folder}: cannot parse metadata: {exc}"]
    if project.get("schemaVersion") != 1:
        problems.append("schemaVersion must be 1")
    if project.get("kind") != kind:
        problems.append(f"kind must be {kind}")
    slug = project.get("slug", "")
    if slug != folder.name or not SLUG.fullmatch(slug):
        problems.append("slug must match directory name and be kebab-case")
    asm = project.get("assembly", "")
    if not ASSEMBLY.fullmatch(asm):
        problems.append("assembly must be PascalCase.dll without separators")
    project_path = project.get("project", "")
    if not re.fullmatch(r"src/[A-Za-z][A-Za-z0-9]*\.csproj", project_path):
        problems.append("project must be src/<Name>.csproj")
    elif not (folder / project_path).is_file():
        problems.append("csproj does not exist")
    if asm != Path(project_path).stem + ".dll":
        problems.append("assembly must match csproj basename")
    if not (folder / "src/ModEntry.cs").is_file():
        problems.append("src/ModEntry.cs not found")
    mod_id = project.get("modId", "")
    if not IDENTITY.fullmatch(mod_id):
        problems.append("modId must use com.zeroga.sodmod.<compactslug>")
    if mod_id != f"com.zeroga.sodmod.{slug.replace('-', '')}":
        problems.append("modId does not match slug")
    if meta.get("id") != mod_id:
        problems.append("about/metadata.json id differs from modId")
    if meta.get("assemblies") != [asm]:
        problems.append("about/metadata.json must declare exactly this mod's DLL")
    if not all(meta.get(key) for key in ("name", "author", "modVer")):
        problems.append("about/metadata.json requires name, author, modVer")
    return [f"{folder.relative_to(ROOT) if folder.is_relative_to(ROOT) else folder}: {p}" for p in problems]


def validate(root=ROOT):
    problems, ids, count = [], set(), 0
    for kind, folder in discover(root):
        count += 1
        problems.extend(check_project(kind, folder))
        try:
            mod_id = json.loads((folder / "mod.project.json").read_text(encoding="utf-8-sig")).get("modId")
            if mod_id in ids:
                problems.append(f"duplicate modId: {mod_id}")
            ids.add(mod_id)
        except (ValueError, OSError):
            pass
    if not count:
        problems.append("No mods found: expected a mod.project.json under characters/ or features/")
    return count, problems


def main():
    count, problems = validate()
    for problem in problems:
        print("ERROR:", problem, file=sys.stderr)
    print(f"Validated {count} independent mod(s); {len(problems)} error(s).")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
