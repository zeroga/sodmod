# Shared build-time code

Only reusable helper source belongs in `shared/src/`. Each mod compiles linked source directly into its **own** DLL. The repository does **not** ship a shared runtime DLL or create a dependency between independently installed mods.

Move code here only once there is a real second consumer; keep game-version-sensitive bindings inside the consuming mod's game adapter. A common asset-loader service may be built later after runtime tests and cross-mod coexistence checks.
