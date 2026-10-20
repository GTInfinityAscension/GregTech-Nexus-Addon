# 材料 API

GTNA 材料是在 `gtna` 命名空间下注册的普通 GTCEu 材料，因此所有 GTCEu 材料工具都适用：形态由标志生成，配方使用 `ChemicalHelper` 或 `forge:ingots/<材料>` 等标签。[材料页面](../../gameplay/materials/index.md)列出了全部材料。

## 在附属模组中注册材料

GTCEu 材料在 GTCEu 附属类的 `MaterialEvent` 中注册：

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

构建器的全部选项见 GTCEu 文档。

## 使用 GTNA 材料

```java
ItemStack plate = ChemicalHelper.get(TagPrefix.plate, GTNAMaterials.Stronze);
```

在脚本中使用前，开启高级提示（F3+H）即可查看任意材料形态的准确 id。

## 图标特效

要为自己的材料添加光环或着色器，请使用 `gtna:*` 物品模型加载器，或[物品特效](../../gameplay/systems/item-effects.md)页面中的 KubeJS 事件。
