# Java API

For addons written in Java. Modpacks usually only need the [KubeJS API](kubejs.md).

## Depending on GTNA

Release jars are on the organisation's Maven:

```groovy
repositories {
    maven { url = 'https://gtinfinityascension.github.io/maven/' }
}

dependencies {
    modImplementation("com.raishxn.gtna:gtna:<version>")
    modImplementation("com.gtinfinityascension:gtialib:<version>")
}
```

GTNA also needs GTCEu 7.5.3+ and Applied Energistics 2 on the classpath. See [Installation](../../getting-started/installation.md) for the runtime versions.

## Public packages

Everything under `com.raishxn.gtna.api` is meant for addons. Classes outside `api` can change without notice.

| Package | Main types | What for |
|---|---|---|
| `api.machine.multiblock` | `GTNAPartAbility`, `GTNASubPatterns`, `ISubPatternMachine`, `IGTNAModuleHost`, `ParallelMachine` | hatch abilities, auxiliary modules, parallel |
| `api.machine` | `IThreadModifierMachine`, `IZeroEnergyMachine` | machine behaviour interfaces |
| `api.machine.feature` | `AccelerateHatchMath`, `OverclockHatchMath`, `godforge.GodforgeMath`, `eyeofharmony.EyeOfHarmonyMath`, pattern buffer mode interfaces | the formulas behind the hatches and endgame systems; the wiki tables come from here |
| `api.capability` | `WirelessEnergyManager`, `SteamWirelessNetworkManager` | read and change a player's Nexus EU and steam balance |
| `api.steam` | `GTNASteamBalance` | scale the parallel and duration of every GTNA steam multiblock from one provider |
| `api.bec` | `BECNetwork`, `CondensateType`, `NaniteTier` | the Bose-Einstein Condensate network |
| `api.render` | `ItemEffect`, `ItemEffectOverrides` | item icon effects |
| `api.registry` | `GTNARegistry` | GTNA's Registrate instance |

## Part abilities

`GTNAPartAbility` holds GTNA's own slots. The common ones:

| Ability | Hatch |
|---|---|
| `THREAD_HATCH` | Thread Hatch; the machine also needs `IThreadModifierMachine` (for example `WorkableElectricMultipleRecipesMachine`) |
| `ACCELERATE_HATCH` | Accelerate Hatch |
| `OVERCLOCK_HATCH` | Overclock Hatch |
| `OUTPUT_BOOST_HATCH` | Output Boost Hatch |
| `STEAM_EXPORT_FLUIDS` | Wireless Steam Output Hatch |

The rest (`BEC_HATCH`, `LINE_OF_SIGHT_HATCH`, `TUNING_HATCH`…) belong to specific GTNA machines.

The module registry moved to GTIA Lib in 0.6.1 (`com.gtinfinityascension.gtialib.module.ModuleRegistry`); `GTNASubPatterns` still works and forwards to it. `Int128` and the block-position helpers moved to `com.gtinfinityascension.gtialib.data`.
