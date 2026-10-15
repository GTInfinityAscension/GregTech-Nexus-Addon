package com.raishxn.gtna.client.renderer.machine;

import net.minecraft.client.renderer.ShaderInstance;
import net.minecraftforge.api.distmarker.Dist;
import net.minecraftforge.api.distmarker.OnlyIn;
import net.minecraftforge.client.event.RegisterShadersEvent;

import com.mojang.blaze3d.vertex.DefaultVertexFormat;
import com.raishxn.gtna.GTNACORE;
import org.jetbrains.annotations.Nullable;

import java.io.IOException;

/** Core shaders of the Stellar Containment Chamber: the star effects and the screen-space gravitational lens. */
@OnlyIn(Dist.CLIENT)
public final class StellarShaders {

    @Nullable
    private static ShaderInstance fx;
    @Nullable
    private static ShaderInstance fxAdditive;
    @Nullable
    private static ShaderInstance lens;

    private StellarShaders() {}

    public static void register(RegisterShadersEvent event) throws IOException {
        event.registerShader(new ShaderInstance(event.getResourceProvider(), GTNACORE.id("stellar_fx"),
                DefaultVertexFormat.POSITION_TEX), shader -> fx = shader);
        // Same program with additive blending: a ShaderInstance applies its own blend mode (none unless declared).
        event.registerShader(new ShaderInstance(event.getResourceProvider(), GTNACORE.id("stellar_fx_add"),
                DefaultVertexFormat.POSITION_TEX), shader -> fxAdditive = shader);
        event.registerShader(new ShaderInstance(event.getResourceProvider(), GTNACORE.id("stellar_lens"),
                DefaultVertexFormat.POSITION_TEX), shader -> lens = shader);
    }

    @Nullable
    public static ShaderInstance fx() {
        return fx;
    }

    @Nullable
    public static ShaderInstance fxAdditive() {
        return fxAdditive;
    }

    @Nullable
    public static ShaderInstance lens() {
        return lens;
    }
}
