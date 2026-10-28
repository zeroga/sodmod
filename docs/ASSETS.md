# Character assets, permissions and model loading

## Sources

`assets/source/` and `assets/private/` are ignored by Git. They may hold locally obtained model, texture, audio or animation data while checking individual permissions. No game-extracted assets, copyrighted third-party Mod DLLs, paid commercial source packs, or unauthorized official models should be redistributed through this repository or a public Mod release.

For any distributable asset record: source URL, creator, exact license, attribution, asset version, permitted uses, original checksum and transformation provenance. Store permitted originals under `assets/public/` and cite them in `assets/README.md`.

## Runtime resource contract

Generated resources live under `assets/runtime/` (ignored), for example:

```text
assets/runtime/
  model/
  anim/
  fx/
  audio/
  icons/
  lang/
```

The packager copies the **contents** of `assets/runtime` into the mod ZIP root, never the original proprietary source. JSON gameplay data stays in `data/`. Game's official `about/metadata.json` stays under `about/`.

## Loader investigation (not resolved)

The previously inspected Miyabi Workshop archive presents `.mmesh`, `.manim`, textures, cue JSON and some Unity bundles. This suggests a hybrid pipeline, **not a published general-purpose reusable loader or a confirmed open file format**. No Unity editor installation should be imposed until we test a runtime model import path against the current game version.

Define future interfaces at the Mod level:

- `IModelSource`: load and release named meshes/skins and skeletons.
- `IAnimationSource`: load clips and events, validate bone mapping.
- `IVfxSource`: instantiate/despawn effects, with fallback.
- `IVisualTransition`: direct model swap now; optionally add assembly animation later.

Do not implement these as committed public APIs before real model files and a game runtime probe prove the required signatures. Prioritize one textured rigged humanoid and one arbitrary second form as smoke-test assets before importing the full character.
