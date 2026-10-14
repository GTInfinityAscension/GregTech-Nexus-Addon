# KubeJS API

GTNA integrates with KubeJS out of the box: just install KubeJS. Everything below exists in the current code; full examples live in `examples/kubejs/` in the repository.

| Feature | Script folder | What for |
|---|---|---|
| `gtna:multiple_recipes` | `startup_scripts` | multiblock that runs several recipes at once (Thread Hatch) |
| `GTNAStartupEvents.eyeOfHarmony` | `startup_scripts` | add or remove Eye of Harmony planets |
| `GTNAServerEvents.subPatterns` | `server_scripts` | auxiliary modules (extra structures) for any multiblock |
| `GTNAClientEvents.itemEffects` | `client_scripts` | halo, edge and shaders on item icons |
| `GTNAPartAbility` | any | GTNA hatch abilities in patterns |

GTNA recipe types are registered in GTCEu, so `event.recipes.gtceu.<type>` works for all of them. The full list of types is in the multiblock catalog.

## `multiple_recipes` machine type

Creates a multiblock backed by `WorkableElectricMultipleRecipesMachine`: with a Thread Hatch it runs several different recipes at once.

```javascript
GTCEuStartupEvents.registry('gtceu:machine', event => {
    
    event.create('my_awesome_machine', 'gtna:multiple_recipes')
        // Which recipes the machine will look for. E.g. assembler recipes.
        .recipeType('gtceu:assembler') 
        .rotationState(RotationState.NON_Y_AXIS)
        .appearanceBlock(GTBlocks.CASING_STEEL_SOLID)
        
        // Let's create a 5x5 hollow structure.
        .pattern(definition => FactoryBlockPattern.start()
            .aisle('CCCCC', 'CCCCC', 'CCCCC')
            .aisle('CCCCC', 'C###C', 'CCCCC')
            .aisle('CCCCC', 'C###C', 'CCCCC')
            .aisle('CCCCC', 'C###C', 'CCCCC')
            .aisle('CCCCC', 'CC~CC', 'CCCCC')
            .where('~', Predicates.controller(Predicates.blocks(definition.get())))
            .where('C', Predicates.blocks(GTBlocks.CASING_STEEL_SOLID.get())
                // Standard GT Hatches
                .or(Predicates.autoAbilities(definition.getRecipeTypes()))
                .or(Predicates.abilities(PartAbility.MAINTENANCE).setExactLimit(1))
                // === GTNA ADVANCED HATCH OPPORTUNITIES ===
                .or(Predicates.abilities(PartAbility.PARALLEL_HATCH).setMaxGlobalLimited(1))
                .or(Predicates.abilities(GTNAPartAbility.THREAD_HATCH).setMaxGlobalLimited(1))
                .or(Predicates.abilities(GTNAPartAbility.ACCELERATE_HATCH).setMaxGlobalLimited(1))
                .or(Predicates.abilities(GTNAPartAbility.OVERCLOCK_HATCH).setMaxGlobalLimited(1))
                .or(Predicates.abilities(PartAbility.MUFFLER).setMaxGlobalLimited(1))
            )
            .where('#', Predicates.air())
            .build()
        )
        
        // Define Custom Multipliers (Optional Config)
        .gtnaConfig(config => {
            config.maxThreadMultiplier(2)    // Double thread amount calculation!
            config.overclockBonus(0.1)       // Extra 10% OC scale
        })
        
        .workableCasingModel(
            'gtceu:block/casings/solid/machine_casing_solid_steel',
            'gtceu:block/multiblock/implosion_compressor'
        )
        
        .tooltips(
            Component.literal('§6My Custom Multi-Thread Machine'),
            Component.literal('§7Supports GTNA Thread, Accelerate & Overclock Hatches'),
            Component.literal('§bUses WorkableElectricMultipleRecipesMachine')
        )
})
```

## GTNAPartAbility

| Binding | Hatch |
|---|---|
| `GTNAPartAbility.THREAD_HATCH` | Thread Hatch |
| `GTNAPartAbility.ACCELERATE_HATCH` | Accelerate Hatch |
| `GTNAPartAbility.OVERCLOCK_HATCH` | Overclock Hatch |
| `GTNAPartAbility.OUTPUT_BOOST_HATCH` | Output Boost Hatch |
| `GTNAPartAbility.PARALLEL_HATCH` | Parallel Hatch (GTCEu) |

## Eye of Harmony planets

`add(planetItem, dimension, rocketTier[, stoneDust])`. Products are the GTCEu ore veins registered for that dimension, scaled by the GTNH rules for the tier (0–9). See the Eye of Harmony page for the formulas.

```javascript
// GTNA: Eye of Harmony planetary programs (startup script; runs on client and server).
// add(planetItem, dimension, gtnhRocketTier[, stoneDust]): the products are the GTCEu ore veins
// registered for that dimension, scaled with the GTNH rules for the rocket tier (0-9).
GTNAStartupEvents.eyeOfHarmony(event => {
    // Example: a KubeJS block as the selector of a modded dimension.
    // event.add('kubejs:titan_planet_block', 'mymod:titan', 5)
    // Example: hide a built-in program.
    // event.remove('gtna:eye_of_harmony_planet_glacio')
})
```

## Auxiliary modules (sub-patterns)

Registers an extra structure for an existing multiblock. The formed module's parts join the controller, so it can unlock new hatches. Optional arguments: tooltip translation key and speed bonus (2.0 = twice as fast).

```javascript
// Development example: a three-block auxiliary column beside the Integrated Ore Processor.
// Copy this file to kubejs/server_scripts with KubeJS installed. The middle block may be an
// Item Import Bus; the other two are Clean Stainless Steel Casings.
// The third argument is a translation key for the controller's Auxiliary Module tooltip.
GTNAServerEvents.subPatterns(event => {
  event.add('gtna:integrated_ore_processor', definition => FactoryBlockPattern.start()
    .aisle('   A', 'C  A', '   A')
    .where('C', Predicates.controller(Predicates.blocks(definition.get())))
    .where('A', Predicates.blocks(GTBlocks.CASING_STAINLESS_CLEAN.get())
      .or(Predicates.abilities(PartAbility.IMPORT_ITEMS).setMaxGlobalLimited(1)))
    .where(' ', Predicates.any())
    .build(), 'gtna.machine.auxiliary_module.kubejs.item_import')
  console.info('[GTNA] Registered Integrated Ore Processor auxiliary module example')
})
```

## Item effects

Runs again on every F3+T. Effects: `halo(argb, size)`, `glowEdge(argb[, width])`, `cosmic()`, `eternal()`, `unstable()`. Modifiers act on the last effect: `colors(a, b)`, `color(argb)`, `pulse(bool)`, `speed(x)`, `mask(texture)`. `item(id)` replaces the model's effects; `material(id)` covers every form of a GTCEu material; `clear()` removes them.

```javascript
// GTNA item icon effects. Client script; reloads with F3+T.
// Effects: halo(argb, size), glowEdge(argb[, width]), cosmic(), eternal(), unstable().
// Modifiers act on the last effect added: colors(a, b), color(argb), pulse(bool), speed(x), mask(texture), texture(texture).

GTNAClientEvents.itemEffects(event => {
    // Every form (ingot, plate, dust...) of a GTCEu material
    event.material('gtna:advanced_nitinol').halo(0xFF66CCFF, 8).pulse(true)

    // One item; replaces the effects of its model
    event.item('minecraft:nether_star').cosmic().colors(0xFF050418, 0xFF7FD4FF).glowEdge(0xFFFFAA00, 1.5)

    // Shader effect limited to a mask texture from the block atlas
    event.item('minecraft:amethyst_shard').eternal().mask('gtna:mask/cosmic').speed(0.5)

    // Remove the effects a model declares
    // event.item('gtceu:gtna_chaos_matter_dust').clear()
})
```
