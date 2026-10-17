package com.raishxn.gtna.common.data;

import com.gregtechceu.gtceu.data.recipe.CustomTags;

import net.minecraft.tags.TagKey;
import net.minecraft.world.item.Item;

import com.raishxn.gtna.GTNACORE;
import com.tterrag.registrate.util.entry.ItemEntry;

import static com.raishxn.gtna.api.registry.GTNARegistry.REGISTRATE;

/**
 * GTNH Optical and Exotic circuit families (G-0202), the "basic" circuits above GTCEu's UHV Wetware Mainframe.
 * GTNH tiers converted to GTCEu (UMV → UXV). Textures from Modernity-GTNH ({@code gt.metaitem.03} 154–157,
 * 166–169), Cosmic and Temporally Transcendent 170–176 (GTNH UMV → UXV, UXV → OpV).
 */
public final class GTNACircuits {

    public static final ItemEntry<Item> OPTICAL_PROCESSOR = circuit("optical_processor", "Optical Processor",
            CustomTags.UV_CIRCUITS);
    public static final ItemEntry<Item> OPTICAL_ASSEMBLY = circuit("optical_assembly", "Optical Assembly",
            CustomTags.UHV_CIRCUITS);
    public static final ItemEntry<Item> OPTICAL_COMPUTER = circuit("optical_computer", "Optical Computer",
            CustomTags.UEV_CIRCUITS);
    public static final ItemEntry<Item> OPTICAL_MAINFRAME = circuit("optical_mainframe", "Optical Mainframe",
            CustomTags.UIV_CIRCUITS);
    public static final ItemEntry<Item> EXOTIC_PROCESSOR = circuit("exotic_processor", "Exotic Processor",
            CustomTags.UHV_CIRCUITS);
    public static final ItemEntry<Item> EXOTIC_ASSEMBLY = circuit("exotic_assembly", "Exotic Assembly",
            CustomTags.UEV_CIRCUITS);
    public static final ItemEntry<Item> EXOTIC_COMPUTER = circuit("exotic_computer", "Exotic Computer",
            CustomTags.UIV_CIRCUITS);
    public static final ItemEntry<Item> EXOTIC_MAINFRAME = circuit("exotic_mainframe", "Exotic Mainframe",
            CustomTags.UXV_CIRCUITS);

    public static final ItemEntry<Item> COSMIC_PROCESSOR = circuit("cosmic_processor", "Cosmic Processor",
            CustomTags.UEV_CIRCUITS);
    public static final ItemEntry<Item> COSMIC_ASSEMBLY = circuit("cosmic_assembly", "Cosmic Assembly",
            CustomTags.UIV_CIRCUITS);
    public static final ItemEntry<Item> COSMIC_COMPUTER = circuit("cosmic_computer", "Cosmic Supercomputer",
            CustomTags.UXV_CIRCUITS);
    public static final ItemEntry<Item> COSMIC_MAINFRAME = circuit("cosmic_mainframe", "Cosmic Mainframe",
            CustomTags.OpV_CIRCUITS);
    public static final ItemEntry<Item> TRANSCENDENT_PROCESSOR = circuit("transcendent_processor",
            "Temporally Transcendent Processor", CustomTags.UXV_CIRCUITS);
    public static final ItemEntry<Item> TRANSCENDENT_ASSEMBLY = circuit("transcendent_assembly",
            "Temporally Transcendent Assembly", CustomTags.OpV_CIRCUITS);
    public static final ItemEntry<Item> TRANSCENDENT_COMPUTER = circuit("transcendent_computer",
            "Temporally Transcendent Supercomputer", CustomTags.MAX_CIRCUITS);

    private GTNACircuits() {}

    private static ItemEntry<Item> circuit(String id, String lang, TagKey<Item> tier) {
        return REGISTRATE.item(id, Item::new).lang(lang).tag(tier)
                .model((ctx, prov) -> prov.generated(ctx, GTNACORE.id("item/circuit/" + id)))
                .register();
    }

    public static void init() {}
}
