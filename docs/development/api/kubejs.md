# API KubeJS

O GTNA tem integração com KubeJS sem configuração: basta ter o KubeJS instalado. Tudo abaixo existe no código atual; os exemplos completos ficam em `examples/kubejs/` no repositório.

| Recurso | Pasta do script | Para quê |
|---|---|---|
| `gtna:multiple_recipes` | `startup_scripts` | multibloco que roda várias receitas ao mesmo tempo (Thread Hatch) |
| `GTNAStartupEvents.eyeOfHarmony` | `startup_scripts` | adicionar ou remover planetas do Olho da Harmonia |
| `GTNAServerEvents.subPatterns` | `server_scripts` | módulos auxiliares (estruturas extras) para qualquer multibloco |
| `GTNAClientEvents.itemEffects` | `client_scripts` | halo, borda e shaders nos ícones de itens |
| `GTNAPartAbility` | qualquer | habilidades dos hatches do GTNA nos padrões |

Os tipos de receita do GTNA são registrados no GTCEu, então `event.recipes.gtceu.<tipo>` funciona normalmente para todos eles. A lista completa de tipos está no catálogo de multiblocos.

## Tipo de máquina `multiple_recipes`

Cria um multibloco que usa `WorkableElectricMultipleRecipesMachine`: com um Thread Hatch, roda várias receitas diferentes ao mesmo tempo.

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

## Planetas do Olho da Harmonia

`add(itemDoPlaneta, dimensão, tierDeFoguete[, poDePedra])`. Os produtos são os veios de minério do GTCEu registrados naquela dimensão, escalados pelas regras do GTNH para o tier (0–9). Veja a página do Olho da Harmonia para as fórmulas.

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

## Módulos auxiliares (sub-patterns)

Registra uma estrutura extra para um multibloco existente. As partes do módulo formado entram no controlador, então o módulo pode liberar hatches novos. Argumentos opcionais: chave de tradução do tooltip e bônus de velocidade (2.0 = o dobro).

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

## Efeitos de item

Roda de novo a cada F3+T. Efeitos: `halo(argb, tamanho)`, `glowEdge(argb[, largura])`, `cosmic()`, `eternal()`, `unstable()`. Modificadores agem no último efeito: `colors(a, b)`, `color(argb)`, `pulse(bool)`, `speed(x)`, `mask(textura)`. `item(id)` substitui os efeitos do modelo; `material(id)` vale para todas as formas de um material do GTCEu; `clear()` remove.

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
