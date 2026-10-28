# Delivery roadmap

## M0 — monorepo initialization

- [x] Partition characters/features into independently released projects.
- [x] Provide a basic Herrscher of Truth ModBehaviour DLL project (load test only).
- [x] Add metadata validation, generator, independent ZIP packaging and CI structure tests.
- [x] Document asset/copyright boundaries and reference investigations.
- [ ] Compile against installed current-game managed assemblies.
- [ ] Confirm game loads `HerrscherOfTruth.dll` and unloads without errors.

## M1 — generic visual smoke test, then Herrscher of Truth

- [ ] Verify an authorized textured rigged 3D model can render in-game without Unity Editor (or select alternative backend).
- [ ] Verify skeleton / directional locomotion / attack animations and performance.
- [ ] Obtain and license a complete Bronya model and full mecha model for the intended distribution.
- [ ] Register a genuinely selectable **new** playable hero (not a replacement of existing hero).
- [ ] Direct swap between Extremum and Continuation 3D form, preserving character state; assembly animation deferred.

## M2 — gameplay

- [ ] Extremum and Continuation attacks, armament unlocks, SP/mecha resources, skill effects and ultimate.
- [ ] Separate server-authoritative damage/summon states from client cosmetics.
- [ ] In-game memory/essence/upgrade hooks only where actually supported.

## M3 — testing and releases

- [ ] Multiplayer with correct Mod versions on participating clients.
- [ ] Room travel, restart, live reload, death/revive, late join, asset failure.
- [ ] Publish only assets authorized for redistribution; ship standalone ZIP and clear release notes per Mod.

**Note:** There is intentionally no target completion date or promise of verified playability at M0. Findings are tracked by evidence, not assumptions.
