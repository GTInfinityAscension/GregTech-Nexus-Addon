package com.raishxn.gtna.client.renderer.effect;

import net.minecraft.client.Minecraft;
import net.minecraft.client.renderer.RenderType;
import net.minecraft.client.renderer.ShaderInstance;
import net.minecraft.client.renderer.block.model.BakedQuad;
import net.minecraft.client.renderer.texture.TextureAtlasSprite;
import net.minecraft.world.inventory.InventoryMenu;
import net.minecraftforge.client.event.RegisterShadersEvent;

import com.mojang.blaze3d.vertex.DefaultVertexFormat;
import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.blaze3d.vertex.VertexConsumer;
import com.mojang.blaze3d.vertex.VertexFormat;
import com.raishxn.gtna.GTNACORE;
import org.jetbrains.annotations.Nullable;

import java.io.IOException;

/**
 * The Avaritia/RenderBlender cosmic star field ({@code gtna:rb_cosmic}, ported from RenderBlender 1.1.1, LGPL-3.0):
 * ten star sprites scattered on rotating layers, coloured by a slowly pulsing background, masked by a texture.
 * Items draw it with an equal-depth pass exactly over their own faces, as RenderBlender did; world surfaces use a
 * slightly lifted copy with a normal depth test.
 */
public final class CosmicShader extends RenderType {

    /** RenderBlender's three star-field programs and the opacity it gives each. */
    public enum Kind {

        COSMIC("rb_cosmic", 1f, "misc/cosmic_"),
        ETERNAL("rb_eternal", 1.5f, "misc/eternal/eternal_"),
        UNSTABLE("rb_unstable", 1.5f, "misc/cosmic_");

        final String program;
        final float opacity;
        final String sprites;
        @Nullable
        ShaderInstance shader;
        RenderType item;

        Kind(String program, float opacity, String sprites) {
            this.program = program;
            this.opacity = opacity;
            this.sprites = sprites;
        }

        public RenderType item() {
            return item;
        }
    }

    @Nullable
    private static ShaderInstance shader;
    private static final float[] UVS = new float[40];

    static {
        for (Kind kind : Kind.values()) kind.item = create("gtna_" + kind.program + "_item", DefaultVertexFormat.BLOCK,
                VertexFormat.Mode.QUADS, 2097152, true, false, CompositeState.builder()
                        .setShaderState(new ShaderStateShard(() -> kind.shader)).setDepthTestState(EQUAL_DEPTH_TEST)
                        .setLightmapState(LIGHTMAP).setTransparencyState(TRANSLUCENT_TRANSPARENCY)
                        .setTextureState(BLOCK_SHEET_MIPPED).createCompositeState(true));
    }

    /** Over an item's own faces (the faces must already be drawn). */
    public static final RenderType ITEM = create("gtna_rb_cosmic_item", DefaultVertexFormat.BLOCK,
            VertexFormat.Mode.QUADS, 2097152, true, false, CompositeState.builder()
                    .setShaderState(new ShaderStateShard(() -> shader)).setDepthTestState(EQUAL_DEPTH_TEST)
                    .setLightmapState(LIGHTMAP).setTransparencyState(TRANSLUCENT_TRANSPARENCY)
                    .setTextureState(BLOCK_SHEET_MIPPED).createCompositeState(true));
    /** On world surfaces and GUI fluid tanks: lifted quads, no depth write. */
    public static final RenderType WORLD = create("gtna_rb_cosmic_world", DefaultVertexFormat.BLOCK,
            VertexFormat.Mode.QUADS, 2097152, true, false, CompositeState.builder()
                    .setShaderState(new ShaderStateShard(() -> shader)).setDepthTestState(LEQUAL_DEPTH_TEST)
                    .setLightmapState(LIGHTMAP).setTransparencyState(TRANSLUCENT_TRANSPARENCY)
                    .setTextureState(BLOCK_SHEET_MIPPED).setWriteMaskState(COLOR_WRITE).createCompositeState(true));

    private CosmicShader() {
        super("unused", DefaultVertexFormat.BLOCK, VertexFormat.Mode.QUADS, 256, false, true, () -> {}, () -> {});
    }

    public static void register(RegisterShadersEvent event) throws IOException {
        for (Kind kind : Kind.values())
            event.registerShader(new ShaderInstance(event.getResourceProvider(), GTNACORE.id(kind.program),
                    DefaultVertexFormat.BLOCK), instance -> {
                        kind.shader = instance;
                        if (kind == Kind.COSMIC) shader = instance;
                    });
    }

    public static boolean ready(Kind kind) {
        return kind.shader != null;
    }

    public static boolean ready() {
        return shader != null;
    }

    /** Sets the uniforms; inventory icons get RenderBlender's fixed angle and 100x scale. */
    public static void prepare(boolean inventory) {
        prepare(Kind.COSMIC, inventory);
    }

    public static void prepare(Kind kind, boolean inventory) {
        var shader = kind.shader;
        if (shader == null) return;
        var mc = Minecraft.getInstance();
        float yaw = 0, pitch = 0, scale = 1;
        if (!inventory && mc.player != null) {
            yaw = (float) (mc.player.getYRot() * 2.0 * Math.PI / 360.0);
            pitch = -(float) (mc.player.getXRot() * 2.0 * Math.PI / 360.0);
        } else scale = 100;
        // RenderBlender counts client ticks plus the partial tick.
        shader.safeGetUniform("time").set((net.minecraft.Util.getMillis() % 3_600_000L) / 50f);
        shader.safeGetUniform("yaw").set(yaw);
        shader.safeGetUniform("pitch").set(pitch);
        shader.safeGetUniform("externalScale").set(scale);
        shader.safeGetUniform("opacity").set(kind.opacity);
        var atlas = mc.getTextureAtlas(InventoryMenu.BLOCK_ATLAS);
        for (int i = 0; i < 10; i++) {
            TextureAtlasSprite s = atlas.apply(GTNACORE.id(kind.sprites + i));
            UVS[i * 4] = s.getU0();
            UVS[i * 4 + 1] = s.getV0();
            UVS[i * 4 + 2] = s.getU1();
            UVS[i * 4 + 3] = s.getV1();
        }
        shader.safeGetUniform("cosmicuvs").set(UVS);
    }

    /** A quad with its UVs moved onto {@code mask}; {@code lift} pushes it off the surface along its normal. */
    public static void quad(BakedQuad quad, PoseStack pose, VertexConsumer out, TextureAtlasSprite mask, float lift,
                            int light) {
        int[] data = quad.getVertices();
        var source = quad.getSprite();
        var normal = quad.getDirection().step();
        int stride = DefaultVertexFormat.BLOCK.getIntegerSize();
        for (int i = 0; i < 4; i++) {
            int o = i * stride;
            float x = Float.intBitsToFloat(data[o]) + normal.x() * lift;
            float y = Float.intBitsToFloat(data[o + 1]) + normal.y() * lift;
            float z = Float.intBitsToFloat(data[o + 2]) + normal.z() * lift;
            float u = (Float.intBitsToFloat(data[o + 4]) - source.getU0()) / (source.getU1() - source.getU0());
            float v = (Float.intBitsToFloat(data[o + 5]) - source.getV0()) / (source.getV1() - source.getV0());
            vertex(pose, out, x, y, z, mask.getU(u * 16), mask.getV(v * 16), normal.x(), normal.y(), normal.z(),
                    light);
        }
    }

    public static void vertex(PoseStack pose, VertexConsumer out, float x, float y, float z, float u, float v,
                              float nx, float ny, float nz, int light) {
        out.vertex(pose.last().pose(), x, y, z).color(255, 255, 255, 255).uv(u, v).uv2(light)
                .normal(pose.last().normal(), nx, ny, nz).endVertex();
    }
}
