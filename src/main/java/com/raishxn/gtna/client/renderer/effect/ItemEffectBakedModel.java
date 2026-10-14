package com.raishxn.gtna.client.renderer.effect;

import net.minecraft.client.resources.model.BakedModel;
import net.minecraft.world.item.ItemDisplayContext;
import net.minecraft.world.item.ItemStack;
import net.minecraftforge.client.model.BakedModelWrapper;

import com.mojang.blaze3d.vertex.PoseStack;
import com.raishxn.gtna.api.render.ItemEffect;

import java.util.ArrayList;
import java.util.List;

/** Plain baked icon that carries the effects declared by its model; {@link ItemEffectRenderer} draws them. */
public final class ItemEffectBakedModel extends BakedModelWrapper<BakedModel> {

    private final List<ItemEffect> effects;

    private ItemEffectBakedModel(BakedModel base, List<ItemEffect> effects) {
        super(base);
        this.effects = effects;
    }

    /** Wraps {@code base}, merging effects when it is already wrapped. */
    public static ItemEffectBakedModel wrap(BakedModel base, List<ItemEffect> effects) {
        if (base instanceof ItemEffectBakedModel wrapped) {
            var merged = new ArrayList<>(wrapped.effects);
            merged.addAll(effects);
            return new ItemEffectBakedModel(wrapped.originalModel, List.copyOf(merged));
        }
        return new ItemEffectBakedModel(base, List.copyOf(effects));
    }

    public List<ItemEffect> effects() {
        return effects;
    }

    @Override
    public BakedModel applyTransform(ItemDisplayContext context, PoseStack pose, boolean leftHand) {
        // Keep the wrapper through the camera transform so the renderer still sees the effects.
        var transformed = originalModel.applyTransform(context, pose, leftHand);
        return transformed == originalModel ? this : transformed;
    }

    @Override
    public List<BakedModel> getRenderPasses(ItemStack stack, boolean fabulous) {
        return List.of(this);
    }
}
