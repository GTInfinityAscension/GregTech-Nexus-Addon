# API de materiais

Os materiais do GTNA são materiais comuns do GTCEu registrados no namespace `gtna`, então todas as ferramentas de material do GTCEu valem: as formas saem das flags, e as receitas usam `ChemicalHelper` ou tags como `forge:ingots/<material>`. A [página de materiais](../../gameplay/materials/index.md) lista todos.

## Registrando um material no seu addon

Materiais do GTCEu são registrados no `MaterialEvent` da classe de addon do GTCEu:

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

A documentação do GTCEu cobre todas as opções do builder.

## Usando materiais do GTNA

```java
ItemStack plate = ChemicalHelper.get(TagPrefix.plate, GTNAMaterials.Stronze);
```

Ligue os tooltips avançados (F3+H) para ver o id exato de qualquer forma de material antes de usá-lo num script.

## Efeitos de ícone

Para dar um halo ou um shader ao seu material, use os loaders de modelo `gtna:*` ou o evento do KubeJS da página de [Efeitos de item](../../gameplay/systems/item-effects.md).
