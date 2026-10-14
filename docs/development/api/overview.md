# Visão geral da API

Pacotes públicos em `com.raishxn.gtna.api`. Addons podem depender deles; scripts usam a [API KubeJS](kubejs.md).

| Pacote | Principais tipos | Para quê |
|---|---|---|
| `api.machine` | IThreadModifierMachine, ParallelMachine, GTNAMultipleRecipesLogic, feature/godforge (GodforgeMath), feature/eyeofharmony (EyeOfHarmonyMath) | interfaces e cálculos das máquinas; as fórmulas da wiki saem daqui |
| `api.pattern` | GTNAPredicates, GTNASubPatterns, leitores .mbs | padrões de estrutura, módulos auxiliares, leitura de estruturas do GTO |
| `api.registry` | GTNARegistry (REGISTRATE) | registro de blocos, itens e máquinas |
| `api.capability` | capabilities de rede e de hatch | energia wireless, vapor, condensado |
| `api.bec` | rede de condensado | tipos de condensado e transporte do BEC |
| `api.steam` | rede wireless de vapor | saldo, fluxo e hatches |
| `api.render` | ItemEffect, ItemEffectOverrides | efeitos de ícone (halo, borda, shaders) |
| `api.data / api.item` | dados persistentes e itens com comportamento | — |

## Hatches especiais

Use `GTNAPartAbility.THREAD_HATCH`, `ACCELERATE_HATCH`, `OVERCLOCK_HATCH` e `OUTPUT_BOOST_HATCH` em `Predicates.abilities(...)`. Máquinas com Thread Hatch implementam `IThreadModifierMachine`.
