package com.raishxn.gtna.mixin.client;

import com.lowdragmc.lowdraglib.gui.widget.SceneWidget;

import net.minecraft.core.BlockPos;
import net.minecraft.world.level.Level;

import com.gtinfinityascension.gtialib.data.BlockPosLongSet;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

import java.util.Set;

/**
 * The scene's rendered-block set is filled with the whole structure and queried by the preview world's render filter
 * for every block lookup; a {@link BlockPosLongSet} keeps filling and lookups fast for very large multiblocks.
 */
@Mixin(value = SceneWidget.class, remap = false)
public abstract class SceneWidgetCoreMixin {

    @Shadow
    protected Set<BlockPos> core;

    @Inject(method = "createScene(Lnet/minecraft/world/level/Level;Z)V", at = @At("TAIL"))
    private void gtna$fastCore(Level world, boolean useFBOSceneRenderer, CallbackInfo ci) {
        if (core != null) core = new BlockPosLongSet();
    }
}
