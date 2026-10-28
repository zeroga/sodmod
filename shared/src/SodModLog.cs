using UnityEngine;

namespace SodMod.Shared
{
    internal static class SodModLog
    {
        internal static void Info(string modId, string message)
        {
            Debug.Log($"[sodmod:{modId}] {message}");
        }
    }
}
