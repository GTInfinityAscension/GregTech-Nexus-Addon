package com.raishxn.gtna.api.render;

import net.minecraft.resources.ResourceLocation;

import org.jetbrains.annotations.Nullable;

import java.util.Locale;

/**
 * One visual effect drawn on top of, or behind, an item icon. Declared by the {@code gtna:<type>} item model
 * loaders or by the {@code GTNAClientEvents.itemEffects} KubeJS event; rendered by GTNA's own item effect
 * renderer, with no external library.
 *
 * @param color     ARGB tint; {@code 0} keeps the type's default palette
 * @param secondary second ARGB colour of the shader effects; {@code 0} derives one from {@code color}
 * @param size      halo radius in item pixels, or glow edge width
 * @param texture   halo texture, or the mask of a shader effect; {@code null} uses the item's own silhouette
 * @param speed     animation speed multiplier
 */
public record ItemEffect(Type type, int color, int secondary, float size, boolean pulse,
                         @Nullable ResourceLocation texture, float speed) {

    public static final ResourceLocation DEFAULT_HALO = ResourceLocation.fromNamespaceAndPath("gtna",
            "item/effect/halo");

    public static ItemEffect of(Type type) {
        return new ItemEffect(type, 0, 0, type.defaultSize, false, type == Type.HALO ? DEFAULT_HALO : null, 1);
    }

    public ItemEffect withColor(int value) {
        return new ItemEffect(type, value, secondary, size, pulse, texture, speed);
    }

    public ItemEffect withSecondary(int value) {
        return new ItemEffect(type, color, value, size, pulse, texture, speed);
    }

    public ItemEffect withSize(float value) {
        return new ItemEffect(type, color, secondary, value, pulse, texture, speed);
    }

    public ItemEffect withPulse(boolean value) {
        return new ItemEffect(type, color, secondary, size, value, texture, speed);
    }

    public ItemEffect withTexture(@Nullable ResourceLocation value) {
        return new ItemEffect(type, color, secondary, size, pulse, value, speed);
    }

    public ItemEffect withSpeed(float value) {
        return new ItemEffect(type, color, secondary, size, pulse, texture, value);
    }

    public enum Type {

        /** Soft tinted disc behind the icon (inventory only). */
        HALO(4),
        /** Tinted, slightly enlarged copy of the icon behind it (inventory only). */
        GLOW_EDGE(1),
        /** Drifting star field inside the mask. */
        COSMIC(0),
        /** Slow flowing light bands with sparkles inside the mask. */
        ETERNAL(0),
        /** Flickering, crackling noise inside the mask. */
        UNSTABLE(0);

        public final float defaultSize;

        Type(float defaultSize) {
            this.defaultSize = defaultSize;
        }

        /** Model loader id path, e.g. {@code glow_edge} for {@code gtna:glow_edge}. */
        public String id() {
            return name().toLowerCase(Locale.ROOT);
        }

        public boolean isShader() {
            return this == COSMIC || this == ETERNAL || this == UNSTABLE;
        }
    }
}
