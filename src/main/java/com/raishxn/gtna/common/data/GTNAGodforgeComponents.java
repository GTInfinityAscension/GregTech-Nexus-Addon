package com.raishxn.gtna.common.data;

import com.gregtechceu.gtceu.api.GTValues;
import com.gregtechceu.gtceu.api.data.tag.TagUtil;
import com.gregtechceu.gtceu.api.item.ComponentItem;
import com.gregtechceu.gtceu.api.item.component.ElectricStats;
import com.gregtechceu.gtceu.common.data.GTItems;

import com.tterrag.registrate.util.entry.ItemEntry;

import java.util.Locale;

import static com.raishxn.gtna.api.registry.GTNARegistry.REGISTRATE;

/**
 * GTNH crafting components used by the Forge of Gods recipes (G-0197), with their GT5-Unofficial / Modernity-GTNH
 * textures. The ZPM3-ZPM6 batteries are rechargeable; the GTNH coolant cells and capacitors are plain crafting items.
 */
public final class GTNAGodforgeComponents {

    public static final ItemEntry<ComponentItem> STABLE_BOSON_CONTAINMENT_UNIT = item(
            "stable_boson_containment_unit", "Stable Boson Containment Unit");
    public static final ItemEntry<ComponentItem> SUPERCONDUCTOR_COMPOSITE = item("superconductor_composite",
            "Superconductor Composite");
    public static final ItemEntry<ComponentItem> ELECTROMAGNET_TENGAM = item("electromagnet_tengam",
            "Tengam Electromagnet");
    public static final ItemEntry<ComponentItem> TESSERACT = item("tesseract", "Raw Tesseract");
    public static final ItemEntry<ComponentItem> THERMAL_SUPERCONDUCTOR = item("thermal_superconductor",
            "Thermal Superconductor");
    public static final ItemEntry<ComponentItem> RELATIVISTIC_HEAT_CAPACITOR = item("relativistic_heat_capacitor",
            "Relativistic Heat Capacitor");
    public static final ItemEntry<ComponentItem> NEUTRONIUM_HEAT_CAPACITOR = item("neutronium_heat_capacitor",
            "1G Neutronium Heat Capacitor");
    public static final ItemEntry<ComponentItem> SPACE_COOLANT_CELL = item("space_coolant_cell",
            "1080k Sp Coolant Cell");
    public static final ItemEntry<ComponentItem> GRAVITON_ANOMALY = item("graviton_anomaly", "Graviton Anomaly");

    /** GTNH ZPM3-ZPM6 (full-charge icon: ZPM3 from GT5U, ZPM4-6 Modernity tinted); ZPM2 is GTCEu's Ultimate Battery. */
    public static final ItemEntry<ComponentItem> REALLY_ULTIMATE_BATTERY = battery("really_ultimate_battery",
            "Really Ultimate Battery", GTValues.UEV, -1);
    public static final ItemEntry<ComponentItem> EXTREMELY_ULTIMATE_BATTERY = battery("extremely_ultimate_battery",
            "Extremely Ultimate Battery", GTValues.UIV, 0xffb4a0);
    public static final ItemEntry<ComponentItem> INSANELY_ULTIMATE_BATTERY = battery("insanely_ultimate_battery",
            "Insanely Ultimate Battery", GTValues.UXV, 0xa8c8ff);
    public static final ItemEntry<ComponentItem> MEGA_ULTIMATE_BATTERY = battery("mega_ultimate_battery",
            "Mega Ultimate Battery", GTValues.OpV, 0xe0a8ff);

    private GTNAGodforgeComponents() {}

    private static ItemEntry<ComponentItem> item(String id, String lang) {
        return REGISTRATE.item(id, ComponentItem::create).lang(lang).register();
    }

    /**
     * Rechargeable battery like GTCEu's Ultimate Battery (Long.MAX_VALUE EU), one tier per GTNH ZPM step and tagged
     * {@code gtceu:batteries/<tier>}. ZPM4-ZPM6 share one icon; a light tint per tier tells them apart (-1 = none).
     */
    private static ItemEntry<ComponentItem> battery(String id, String lang, int tier, int color) {
        var builder = REGISTRATE.item(id, ComponentItem::create).lang(lang)
                .onRegister(GTItems.attach(ElectricStats.createRechargeableBattery(Long.MAX_VALUE, tier)))
                .tag(TagUtil.createModItemTag("batteries/" + GTValues.VN[tier].toLowerCase(Locale.ROOT)));
        if (color != -1) {
            builder.color(() -> () -> (net.minecraft.client.color.item.ItemColor) (stack, layer) -> color);
        }
        return builder.register();
    }

    public static void init() {}
}
