package com.raishxn.gtna.integration.kubejs;

import net.minecraft.resources.ResourceLocation;

import com.raishxn.gtna.api.render.ItemEffect;
import com.raishxn.gtna.api.render.ItemEffectOverrides;
import dev.latvian.mods.kubejs.event.EventJS;

import java.util.ArrayList;
import java.util.List;

/** KubeJS event: item icon effects. See {@link GTNAClientEvents}. */
public class ItemEffectsEventJS extends EventJS {

    /** Effects for one item; replaces the effects of its model. */
    public Builder item(String id) {
        var key = parse(id);
        return new Builder(effects -> ItemEffectOverrides.setItem(key, effects));
    }

    /** Effects for every item of a GTCEu material (ingot, plate, dust...). */
    public Builder material(String id) {
        var key = parse(id.contains(":") ? id : "gtceu:" + id);
        return new Builder(effects -> ItemEffectOverrides.setMaterial(key, effects));
    }

    static ResourceLocation parse(String id) {
        var location = ResourceLocation.tryParse(id);
        if (location == null) throw new IllegalArgumentException("Invalid id: " + id);
        return location;
    }

    /**
     * Chainable effect list. Effect methods add an effect; {@code pulse}, {@code mask}, {@code texture},
     * {@code colors} and {@code speed} change the last one added.
     */
    public static class Builder {

        private final java.util.function.Consumer<List<ItemEffect>> sink;
        private final List<ItemEffect> effects = new ArrayList<>();

        Builder(java.util.function.Consumer<List<ItemEffect>> sink) {
            this.sink = sink;
            sink.accept(effects);
        }

        private Builder add(ItemEffect effect) {
            effects.add(effect);
            sink.accept(effects);
            return this;
        }

        private Builder last(java.util.function.UnaryOperator<ItemEffect> change) {
            if (effects.isEmpty()) throw new IllegalStateException("Add an effect before changing it");
            effects.set(effects.size() - 1, change.apply(effects.get(effects.size() - 1)));
            sink.accept(effects);
            return this;
        }

        /** Removes every effect, including the ones from the item model. */
        public Builder clear() {
            effects.clear();
            sink.accept(effects);
            return this;
        }

        public Builder halo(int argb, float size) {
            return add(ItemEffect.of(ItemEffect.Type.HALO).withColor(argb).withSize(size));
        }

        public Builder glowEdge(int argb) {
            return glowEdge(argb, ItemEffect.Type.GLOW_EDGE.defaultSize);
        }

        public Builder glowEdge(int argb, float width) {
            return add(ItemEffect.of(ItemEffect.Type.GLOW_EDGE).withColor(argb).withSize(width));
        }

        public Builder cosmic() {
            return add(ItemEffect.of(ItemEffect.Type.COSMIC));
        }

        public Builder eternal() {
            return add(ItemEffect.of(ItemEffect.Type.ETERNAL));
        }

        public Builder unstable() {
            return add(ItemEffect.of(ItemEffect.Type.UNSTABLE));
        }

        /** Two ARGB colours of the last shader effect (background, highlight), or the halo/glow tint. */
        public Builder colors(int primary, int secondary) {
            return last(e -> e.withColor(primary).withSecondary(secondary));
        }

        public Builder color(int argb) {
            return last(e -> e.withColor(argb));
        }

        public Builder pulse(boolean pulse) {
            return last(e -> e.withPulse(pulse));
        }

        public Builder speed(float speed) {
            return last(e -> e.withSpeed(speed));
        }

        /** Mask texture (block atlas) limiting where a shader effect draws; white = full effect. */
        public Builder mask(String texture) {
            return last(e -> e.withTexture(parse(texture)));
        }

        /** Halo texture (block atlas). */
        public Builder texture(String texture) {
            return mask(texture);
        }
    }
}
