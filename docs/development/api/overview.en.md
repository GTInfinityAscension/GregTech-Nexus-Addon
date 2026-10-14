# API overview

Public packages in `com.raishxn.gtna.api`. Addons may depend on them; scripts use the [KubeJS API](kubejs.md).

| Package | Main types | What for |
|---|---|---|
| `api.machine` | IThreadModifierMachine, ParallelMachine, GTNAMultipleRecipesLogic, feature/godforge (GodforgeMath), feature/eyeofharmony (EyeOfHarmonyMath) | machine interfaces and math; the wiki formulas come from here |
| `api.pattern` | GTNAPredicates, GTNASubPatterns, leitores .mbs | structure patterns, auxiliary modules, GTO structure readers |
| `api.registry` | GTNARegistry (REGISTRATE) | block, item and machine registration |
| `api.capability` | capabilities de rede e de hatch | wireless energy, steam, condensate |
| `api.bec` | rede de condensado | BEC condensate types and transport |
| `api.steam` | rede wireless de vapor | balance, flow and hatches |
| `api.render` | ItemEffect, ItemEffectOverrides | icon effects (halo, edge, shaders) |
| `api.data / api.item` | dados persistentes e itens com comportamento | — |

## Special hatches

Use `GTNAPartAbility.THREAD_HATCH`, `ACCELERATE_HATCH`, `OVERCLOCK_HATCH` and `OUTPUT_BOOST_HATCH` in `Predicates.abilities(...)`. Machines with a Thread Hatch implement `IThreadModifierMachine`.
