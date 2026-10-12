package com.raishxn.gtna.api.bec;

import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;

import com.raishxn.gtna.common.data.GTNANanoForge;
import com.tterrag.registrate.util.entry.ItemEntry;
import org.jetbrains.annotations.Nullable;

import java.util.function.Supplier;

/** GTNH {@code NaniteTier}: the nanites the BEC Observation Array provides and the tier of each. */
public enum NaniteTier {

    Carbon(1, () -> GTNANanoForge.CARBON_NANITES),
    Glowstone(1, () -> GTNANanoForge.GLOWSTONE_NANITES),
    Silver(2, () -> GTNANanoForge.SILVER_NANITES),
    Neutronium(2, () -> GTNANanoForge.NEUTRONIUM_NANITES),
    Gold(3, () -> GTNANanoForge.GOLD_NANITES),
    // intentionally above gold because transmetal nanites are harder to make
    Transcendent(4, () -> GTNANanoForge.TRANSCENDENT_METAL_NANITES),
    SixPhasedCopper(5, () -> GTNANanoForge.SIX_PHASED_COPPER_NANITES),
    WhiteDwarf(6, () -> GTNANanoForge.WHITE_DWARF_MATTER_NANITES),
    BlackDwarf(7, () -> GTNANanoForge.BLACK_DWARF_MATTER_NANITES),
    Universium(8, () -> GTNANanoForge.UNIVERSIUM_NANITES),
    Eternity(9, () -> GTNANanoForge.ETERNITY_NANITES),
    MagMatter(10, () -> GTNANanoForge.MAGMATTER_NANITES);

    public static final NaniteTier[] VALUES = values();

    public final int tier;
    private final Supplier<ItemEntry<?>> item;

    NaniteTier(int tier, Supplier<ItemEntry<?>> item) {
        this.tier = tier;
        this.item = item;
    }

    public Item getItem() {
        return item.get().get().asItem();
    }

    public ItemStack getStack() {
        return new ItemStack(getItem());
    }

    public static @Nullable NaniteTier fromItem(Item item) {
        for (NaniteTier tier : VALUES) if (tier.getItem() == item) return tier;
        return null;
    }

    public static @Nullable NaniteTier fromStack(ItemStack stack) {
        return stack.isEmpty() ? null : fromItem(stack.getItem());
    }

    public static @Nullable NaniteTier byOrdinal(int ordinal) {
        return ordinal >= 0 && ordinal < VALUES.length ? VALUES[ordinal] : null;
    }
}
