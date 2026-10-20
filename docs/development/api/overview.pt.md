# API Java

Para addons escritos em Java. Modpacks normalmente só precisam da [API KubeJS](kubejs.md).

## Dependendo do GTNA

Os jars das versões estão no Maven da organização:

```groovy
repositories {
    maven { url = 'https://gtinfinityascension.github.io/maven/' }
}

dependencies {
    modImplementation("com.raishxn.gtna:gtna:<versão>")
    modImplementation("com.gtinfinityascension:gtialib:<versão>")
}
```

O GTNA também precisa do GTCEu 7.5.3+ e do Applied Energistics 2 no classpath. Veja [Instalação](../../getting-started/installation.md) para as versões em tempo de execução.

## Pacotes públicos

Tudo em `com.raishxn.gtna.api` é feito para addons. Classes fora de `api` podem mudar sem aviso.

| Pacote | Tipos principais | Para quê |
|---|---|---|
| `api.machine.multiblock` | `GTNAPartAbility`, `GTNASubPatterns`, `ISubPatternMachine`, `IGTNAModuleHost`, `ParallelMachine` | abilities de hatch, módulos auxiliares, paralelo |
| `api.machine` | `IThreadModifierMachine`, `IZeroEnergyMachine` | interfaces de comportamento de máquina |
| `api.machine.feature` | `AccelerateHatchMath`, `OverclockHatchMath`, `godforge.GodforgeMath`, `eyeofharmony.EyeOfHarmonyMath`, interfaces de modo do pattern buffer | as fórmulas por trás dos hatches e dos sistemas de fim de jogo; as tabelas da wiki vêm daqui |
| `api.capability` | `WirelessEnergyManager`, `SteamWirelessNetworkManager` | ler e mudar o saldo de EU Nexus e de vapor de um jogador |
| `api.steam` | `GTNASteamBalance` | escalar paralelo e duração de todos os multiblocos a vapor do GTNA a partir de um provider |
| `api.bec` | `BECNetwork`, `CondensateType`, `NaniteTier` | a rede do Condensado de Bose-Einstein |
| `api.render` | `ItemEffect`, `ItemEffectOverrides` | efeitos nos ícones de item |
| `api.registry` | `GTNARegistry` | a instância de Registrate do GTNA |

## Abilities de peça

`GTNAPartAbility` guarda as vagas próprias do GTNA. As mais usadas:

| Ability | Hatch |
|---|---|
| `THREAD_HATCH` | Hatch de Threads; a máquina também precisa de `IThreadModifierMachine` (por exemplo `WorkableElectricMultipleRecipesMachine`) |
| `ACCELERATE_HATCH` | Hatch de Aceleração |
| `OVERCLOCK_HATCH` | Hatch de Overclock |
| `OUTPUT_BOOST_HATCH` | Hatch com Saída Ampliada |
| `STEAM_EXPORT_FLUIDS` | Hatch de Saída de Vapor Wireless |

As demais (`BEC_HATCH`, `LINE_OF_SIGHT_HATCH`, `TUNING_HATCH`…) pertencem a máquinas específicas do GTNA.

O registro de módulos foi para o GTIA Lib na 0.6.1 (`com.gtinfinityascension.gtialib.module.ModuleRegistry`); o `GTNASubPatterns` continua funcionando e repassa para ele. `Int128` e os utilitários de posição de bloco foram para `com.gtinfinityascension.gtialib.data`.
