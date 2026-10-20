# KubeJS API

GTNA works with KubeJS out of the box: install KubeJS and the bindings below are there. Complete, runnable examples are in [`examples/kubejs/`](https://github.com/GTInfinityAscension/GregTech-Nexus-Addon/tree/main/examples/kubejs) in the repository.

| Feature | Script folder | What for |
|---|---|---|
| [`gtna:multiple_recipes`](#multiple-recipes-machines) | `startup_scripts` | a new multiblock that runs several recipes at once |
| [`GTNAServerEvents.subPatterns`](#auxiliary-modules) | `server_scripts` | auxiliary modules for any multiblock |
| [`GTNAStartupEvents.eyeOfHarmony`](#eye-of-harmony-planets) | `startup_scripts` | add or remove Eye of Harmony planets |
| [`GTNAClientEvents.itemEffects`](#item-effects) | `client_scripts` | halos, glow edges and shaders on item icons |
| [`GTNAPartAbility`](#gtnapartability) | any | GTNA hatch abilities for structure patterns |

## Recipes

GTNA's recipe types are GTCEu recipe types in the `gtna` namespace, so the usual GTCEu KubeJS syntax works with `event.recipes.gtna`:

```js
ServerEvents.recipes(event => {
  event.recipes.gtna.hydraulic_manufacturing('kubejs:my_piston')
    .itemInputs('4x gtceu:bronze_plate')
    .itemOutputs('gtna:hydraulic_piston')
    .duration(100)
    .EUt(16)
})
```

The recipe type of every machine is listed on its [catalog page](../../gameplay/machines/catalog/index.md). The [research engine](../../gameplay/systems/research-engine.md) can gate any recipe id behind a research node from a datapack.

## Multiple-recipes machines {#multiple-recipes-machines}

`gtna:multiple_recipes` builds a multiblock on `WorkableElectricMultipleRecipesMachine`, the same base as the Industrial Slaughterhouse and the Integrated Ore Processor. It uses the GTCEu multiblock builder, and with a [Thread Hatch](../../gameplay/parts/thread-hatch.md) it runs several different recipes at the same time.

```js
GTCEuStartupEvents.registry('gtceu:machine', event => {
  event.create('my_assembly_hall', 'gtna:multiple_recipes')
    .recipeType('gtceu:assembler')
    .rotationState(RotationState.NON_Y_AXIS)
    .appearanceBlock(GTBlocks.CASING_STEEL_SOLID)
    .pattern(definition => FactoryBlockPattern.start()
      .aisle('CCCCC', 'CCCCC', 'CCCCC')
      .aisle('CCCCC', 'C###C', 'CCCCC')
      .aisle('CCCCC', 'C###C', 'CCCCC')
      .aisle('CCCCC', 'C###C', 'CCCCC')
      .aisle('CCCCC', 'CC~CC', 'CCCCC')
      .where('~', Predicates.controller(Predicates.blocks(definition.get())))
      .where('C', Predicates.blocks(GTBlocks.CASING_STEEL_SOLID.get())
        .or(Predicates.autoAbilities(definition.getRecipeTypes()))
        .or(Predicates.abilities(PartAbility.MAINTENANCE).setExactLimit(1))
        .or(Predicates.abilities(GTNAPartAbility.PARALLEL_CONTROL_HATCH).setMaxGlobalLimited(1))
        .or(Predicates.abilities(GTNAPartAbility.THREAD_HATCH).setMaxGlobalLimited(1))
        .or(Predicates.abilities(GTNAPartAbility.ACCELERATE_HATCH).setMaxGlobalLimited(1))
        .or(Predicates.abilities(GTNAPartAbility.OVERCLOCK_HATCH).setMaxGlobalLimited(1)))
      .where('#', Predicates.air())
      .build())
    .workableCasingModel('gtceu:block/casings/solid/machine_casing_solid_steel',
      'gtceu:block/multiblock/implosion_compressor')
})
```

## Auxiliary modules {#auxiliary-modules}

Adds an optional extra structure to an existing multiblock, GTNA's or another mod's. The pattern is checked from the controller's position and facing; the parts found in it join the machine. See [Modules](../../gameplay/systems/modules.md) for what players see.

```js
GTNAServerEvents.subPatterns(event => {
  // a three-block column beside the Integrated Ore Processor; the middle block may be an input bus
  event.add('gtna:integrated_ore_processor', definition => FactoryBlockPattern.start()
    .aisle('   A', 'C  A', '   A')
    .where('C', Predicates.controller(Predicates.blocks(definition.get())))
    .where('A', Predicates.blocks(GTBlocks.CASING_STAINLESS_CLEAN.get())
      .or(Predicates.abilities(PartAbility.IMPORT_ITEMS).setMaxGlobalLimited(1)))
    .where(' ', Predicates.any())
    .build(), 'gtna.machine.auxiliary_module.kubejs.item_import')
})
```

| Overload | Meaning |
|---|---|
| `add(machineId, factory)` | registers the module |
| `add(machineId, factory, descriptionKey)` | adds a tooltip line from a translation key |
| `add(machineId, factory, descriptionKey, speedBonus, perfectOverclock)` | on multiple-recipes machines, the bonus applies only while this module is formed: `2.0` halves the duration (combined cap 1024×); `true` enables perfect overclock when no Overclock Hatch overrides the curve |

## Eye of Harmony planets {#eye-of-harmony-planets}

```js
GTNAStartupEvents.eyeOfHarmony(event => {
  // add(planetItem, dimension, rocketTier[, stoneDust])
  event.add('kubejs:titan_planet_block', 'mymod:titan', 5)
  event.remove('gtna:eye_of_harmony_planet_glacio')
})
```

The products are the GTCEu ore veins registered in that dimension, scaled with the GTNH rules for the rocket tier (0–9). Formulas are on the [Eye of Harmony](../../gameplay/systems/eye-of-harmony.md) page.

## Item effects {#item-effects}

```js
GTNAClientEvents.itemEffects(event => {
  event.material('gtna:advanced_nitinol').halo(0xFF66CCFF, 8).pulse(true)
  event.item('minecraft:nether_star').cosmic().colors(0xFF050418, 0xFF7FD4FF).glowEdge(0xFFFFAA00, 1.5)
  event.item('minecraft:amethyst_shard').eternal().mask('gtna:mask/cosmic').speed(0.5)
})
```

Every method is listed on the [Item effects](../../gameplay/systems/item-effects.md) page. The script runs again on every F3+T.

## GTNAPartAbility {#gtnapartability}

| Binding | Hatch |
|---|---|
| `GTNAPartAbility.THREAD_HATCH` | Thread Hatch |
| `GTNAPartAbility.ACCELERATE_HATCH` | Accelerate Hatch |
| `GTNAPartAbility.OVERCLOCK_HATCH` | Overclock Hatch |
| `GTNAPartAbility.OUTPUT_BOOST_HATCH` | Output Boost Hatch |
| `GTNAPartAbility.PARALLEL_CONTROL_HATCH` | GTCEu's Parallel Control Hatch, GTNA's UHV+ hatches included (`PARALLEL_HATCH` is an alias) |

Use them in `Predicates.abilities(...)`, usually with `.setMaxGlobalLimited(1)`.
