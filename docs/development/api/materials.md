# Materials API

GTNA materials are ordinary GTCEu materials registered under the `gtna` namespace, so every GTCEu material tool applies: forms are generated from flags, and recipes use `ChemicalHelper` or tags such as `forge:ingots/<material>`. The [materials page](../../gameplay/materials/index.md) lists them.

## Registering a material in your addon

GTCEu materials are registered in the `MaterialEvent` of your GTCEu addon class:

```java
public static Material MyAlloy;

public static void register() {
    MyAlloy = new Material.Builder(MyMod.id("my_alloy"))
            .ingot().fluid()
            .color(0x7FD4FF)
            .iconSet(MaterialIconSet.METALLIC)
            .components(GTMaterials.Iron, 3, GTMaterials.Copper, 1)
            .blastTemp(1200, BlastProperty.GasTier.LOW)
            .flags(MaterialFlags.GENERATE_PLATE, MaterialFlags.GENERATE_ROD, MaterialFlags.GENERATE_GEAR)
            .buildAndRegister();
}
```

The GTCEu documentation covers every builder option.

## Using GTNA materials

```java
ItemStack plate = ChemicalHelper.get(TagPrefix.plate, GTNAMaterials.Stronze);
```

Turn on advanced tooltips (F3+H) to see the exact id of any material form before using it in a script.

## Icon effects

To give your own material a halo or a shader, use the `gtna:*` item model loaders or the KubeJS event on the [Item effects](../../gameplay/systems/item-effects.md) page.
