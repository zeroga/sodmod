using SodMod.Shared;

namespace SodMod.Characters.HerrscherOfTruth
{
    // M0 smoke-test only: verifies native ModBehaviour assembly loading.
    // A real Hero prefab, skills, model loader and networking are NOT registered yet.
    public sealed class ModEntry : ModBehaviour
    {
        private void Start()
        {
            SodModLog.Info("herrscher-of-truth", "M0 scaffold loaded; hero not implemented.");
        }

        private void OnDestroy()
        {
            // This Mod has no Harmony patches at M0. Future patches must be
            // explicitly reverted with harmony.UnpatchAll(harmony.Id).
            SodModLog.Info("herrscher-of-truth", "M0 scaffold unloaded.");
        }
    }
}
