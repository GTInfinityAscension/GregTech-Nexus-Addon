package com.raishxn.gtna.api.render;

import net.minecraft.resources.ResourceLocation;

import org.jetbrains.annotations.Nullable;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Item effects set by scripts. An entry replaces the effects of the item's model; an empty list removes them.
 * Item entries win over material entries.
 */
public final class ItemEffectOverrides {

    private static final Map<ResourceLocation, List<ItemEffect>> ITEMS = new HashMap<>();
    private static final Map<ResourceLocation, List<ItemEffect>> MATERIALS = new HashMap<>();
    private static int version;

    private ItemEffectOverrides() {}

    public static synchronized void clear() {
        ITEMS.clear();
        MATERIALS.clear();
        version++;
    }

    public static synchronized void setItem(ResourceLocation item, List<ItemEffect> effects) {
        ITEMS.put(item, List.copyOf(effects));
        version++;
    }

    public static synchronized void setMaterial(ResourceLocation material, List<ItemEffect> effects) {
        MATERIALS.put(material, List.copyOf(effects));
        version++;
    }

    public static synchronized @Nullable List<ItemEffect> forItem(ResourceLocation item) {
        return ITEMS.get(item);
    }

    public static synchronized @Nullable List<ItemEffect> forMaterial(ResourceLocation material) {
        return MATERIALS.get(material);
    }

    public static synchronized boolean isEmpty() {
        return ITEMS.isEmpty() && MATERIALS.isEmpty();
    }

    /** Changes whenever an entry changes, so renderers can drop cached lookups. */
    public static synchronized int version() {
        return version;
    }
}
