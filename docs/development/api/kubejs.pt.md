# API KubeJS

O GTNA funciona com o KubeJS sem nada extra: instale o KubeJS e os bindings abaixo já estão lá. Exemplos completos, prontos para rodar, estão em [`examples/kubejs/`](https://github.com/GTInfinityAscension/GregTech-Nexus-Addon/tree/main/examples/kubejs) no repositório.

| Recurso | Pasta do script | Para quê |
|---|---|---|
| [`gtna:multiple_recipes`](#multiple-recipes-machines) | `startup_scripts` | um multibloco novo que roda várias receitas de uma vez |
| [`GTNAServerEvents.subPatterns`](#auxiliary-modules) | `server_scripts` | módulos auxiliares para qualquer multibloco |
| [`GTNAStartupEvents.eyeOfHarmony`](#eye-of-harmony-planets) | `startup_scripts` | acrescentar ou remover planetas do Olho da Harmonia |
| [`GTNAClientEvents.itemEffects`](#item-effects) | `client_scripts` | halos, bordas brilhantes e shaders nos ícones de item |
| [`GTNAPartAbility`](#gtnapartability) | qualquer | abilities dos hatches do GTNA para padrões de estrutura |

## Receitas

Os tipos de receita do GTNA são tipos de receita do GTCEu no namespace `gtna`, então a sintaxe de sempre do GTCEu no KubeJS funciona com `event.recipes.gtna`:

```js
ServerEvents.recipes(event => {
  event.recipes.gtna.hydraulic_manufacturing('kubejs:my_piston')
    .itemInputs('4x gtceu:bronze_plate')
    .itemOutputs('gtna:hydraulic_piston')
    .duration(100)
    .EUt(16)
})
```

O tipo de receita de cada máquina está na [página dela no catálogo](../../gameplay/machines/catalog/index.md). O [motor de pesquisa](../../gameplay/systems/research-engine.md) pode bloquear qualquer id de receita atrás de um nó de pesquisa, por datapack.

## Máquinas de múltiplas receitas {#multiple-recipes-machines}

`gtna:multiple_recipes` cria um multibloco sobre `WorkableElectricMultipleRecipesMachine`, a mesma base do Matadouro Industrial e do Processador de Minério Integrado. Ele usa o builder de multiblocos do GTCEu e, com um [Hatch de Threads](../../gameplay/parts/thread-hatch.md), roda várias receitas diferentes ao mesmo tempo.

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

## Módulos auxiliares {#auxiliary-modules}

Acrescenta uma estrutura extra opcional a um multibloco existente, do GTNA ou de outro mod. O padrão é checado a partir da posição e da direção do controlador; as peças encontradas nele passam para a máquina. Veja [Módulos](../../gameplay/systems/modules.md) para o que o jogador vê.

```js
GTNAServerEvents.subPatterns(event => {
  // uma coluna de três blocos ao lado do Processador de Minério Integrado; o bloco do meio pode ser um barramento de entrada
  event.add('gtna:integrated_ore_processor', definition => FactoryBlockPattern.start()
    .aisle('   A', 'C  A', '   A')
    .where('C', Predicates.controller(Predicates.blocks(definition.get())))
    .where('A', Predicates.blocks(GTBlocks.CASING_STAINLESS_CLEAN.get())
      .or(Predicates.abilities(PartAbility.IMPORT_ITEMS).setMaxGlobalLimited(1)))
    .where(' ', Predicates.any())
    .build(), 'gtna.machine.auxiliary_module.kubejs.item_import')
})
```

| Sobrecarga | Significado |
|---|---|
| `add(machineId, factory)` | registra o módulo |
| `add(machineId, factory, descriptionKey)` | acrescenta uma linha de tooltip a partir de uma chave de tradução |
| `add(machineId, factory, descriptionKey, speedBonus, perfectOverclock)` | em máquinas de múltiplas receitas, o bônus vale só enquanto este módulo está formado: `2.0` corta a duração pela metade (teto combinado de 1024×); `true` liga o overclock perfeito quando nenhum Hatch de Overclock substitui a curva |

## Planetas do Olho da Harmonia {#eye-of-harmony-planets}

```js
GTNAStartupEvents.eyeOfHarmony(event => {
  // add(planetItem, dimension, rocketTier[, stoneDust])
  event.add('kubejs:titan_planet_block', 'mymod:titan', 5)
  event.remove('gtna:eye_of_harmony_planet_glacio')
})
```

Os produtos são os veios de minério do GTCEu registrados naquela dimensão, escalados pelas regras do GTNH para o tier de foguete (0–9). As fórmulas estão na página do [Olho da Harmonia](../../gameplay/systems/eye-of-harmony.md).

## Efeitos de item {#item-effects}

```js
GTNAClientEvents.itemEffects(event => {
  event.material('gtna:advanced_nitinol').halo(0xFF66CCFF, 8).pulse(true)
  event.item('minecraft:nether_star').cosmic().colors(0xFF050418, 0xFF7FD4FF).glowEdge(0xFFFFAA00, 1.5)
  event.item('minecraft:amethyst_shard').eternal().mask('gtna:mask/cosmic').speed(0.5)
})
```

Todos os métodos estão na página de [Efeitos de item](../../gameplay/systems/item-effects.md). O script roda de novo a cada F3+T.

## GTNAPartAbility {#gtnapartability}

| Binding | Hatch |
|---|---|
| `GTNAPartAbility.THREAD_HATCH` | Thread Hatch |
| `GTNAPartAbility.ACCELERATE_HATCH` | Accelerate Hatch |
| `GTNAPartAbility.OVERCLOCK_HATCH` | Overclock Hatch |
| `GTNAPartAbility.OUTPUT_BOOST_HATCH` | Output Boost Hatch |
| `GTNAPartAbility.PARALLEL_CONTROL_HATCH` | Parallel Control Hatch do GTCEu, incluindo os hatches UHV+ do GTNA (`PARALLEL_HATCH` é um apelido) |

Use em `Predicates.abilities(...)`, normalmente com `.setMaxGlobalLimited(1)`.
