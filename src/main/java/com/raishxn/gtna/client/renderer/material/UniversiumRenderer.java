package com.raishxn.gtna.client.renderer.material;

import com.gregtechceu.gtceu.api.block.MaterialBlock;
import com.gregtechceu.gtceu.api.data.tag.TagPrefix;

import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.client.renderer.RenderType;
import net.minecraft.client.renderer.ShaderInstance;
import net.minecraft.client.renderer.block.model.BakedQuad;
import net.minecraft.client.renderer.texture.TextureAtlasSprite;
import net.minecraft.client.resources.model.BakedModel;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.util.RandomSource;
import net.minecraft.world.inventory.InventoryMenu;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.material.Fluid;
import net.minecraftforge.client.event.RegisterShadersEvent;
import net.minecraftforge.client.event.RenderLevelStageEvent;
import net.minecraftforge.event.TickEvent;
import net.minecraftforge.fml.ModList;
import net.minecraftforge.registries.ForgeRegistries;

import com.mojang.blaze3d.vertex.DefaultVertexFormat;
import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.blaze3d.vertex.VertexConsumer;
import com.mojang.blaze3d.vertex.VertexFormat;
import com.raishxn.gtna.GTNACORE;
import com.raishxn.gtna.common.data.GTNAMaterials;
import org.joml.Vector3f;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

/** Universium's live RenderBlender star field on world surfaces and non-material items. */
public final class UniversiumRenderer extends RenderType {

    private static ShaderInstance shader;
    private static final long START = System.currentTimeMillis();
    private static final ResourceLocation SOLID = GTNACORE.id("item/universium/solid_mask");
    private static final ResourceLocation FRAME = GTNACORE.id("item/universium/frame_mask");
    private static final ResourceLocation NANITES = GTNACORE.id("item/universium/nanites_mask");
    private static final RenderType COSMIC = create("gtna_universium_cosmic", DefaultVertexFormat.NEW_ENTITY,
            VertexFormat.Mode.QUADS, 256, false, true, CompositeState.builder()
                    .setShaderState(new ShaderStateShard(() -> shader))
                    .setTextureState(new TextureStateShard(InventoryMenu.BLOCK_ATLAS, false, false))
                    .setTransparencyState(TRANSLUCENT_TRANSPARENCY).setCullState(NO_CULL)
                    .setLightmapState(LIGHTMAP).setOverlayState(OVERLAY)
                    .setWriteMaskState(COLOR_WRITE).createCompositeState(false));
    private static final List<BlockPos> SURFACES = new ArrayList<>();
    private static net.minecraft.client.multiplayer.ClientLevel cachedLevel;
    private static long nextScan;

    private UniversiumRenderer() {
        super("unused", DefaultVertexFormat.NEW_ENTITY, VertexFormat.Mode.QUADS, 256, false, true, () -> {}, () -> {});
    }

    public static void register(RegisterShadersEvent event) throws IOException {
        event.registerShader(new ShaderInstance(event.getResourceProvider(), GTNACORE.id("universium_cosmic"),
                DefaultVertexFormat.NEW_ENTITY), instance -> shader = instance);
    }

    public static boolean isFluid(Fluid fluid) {
        return GTNAMaterials.Universium != null && fluid.isSame(GTNAMaterials.Universium.getFluid());
    }

    private static boolean isBlock(BlockState state) {
        return state.getBlock() instanceof MaterialBlock block && block.material == GTNAMaterials.Universium &&
                (block.tagPrefix == TagPrefix.block || block.tagPrefix == TagPrefix.frameGt);
    }

    private static boolean ready(boolean inventory) {
        if (shader == null || !ModList.get().isLoaded("renderblender")) return false;
        var mc = Minecraft.getInstance();
        shader.safeGetUniform("time").set((System.currentTimeMillis() - START) / 2000f);
        shader.safeGetUniform("yaw").set(mc.player == null ? 0 : (float) Math.toRadians(mc.player.getYRot()));
        shader.safeGetUniform("pitch").set(mc.player == null ? 0 : -(float) Math.toRadians(mc.player.getXRot()));
        shader.safeGetUniform("externalScale").set(inventory ? 25f : 1f);
        shader.safeGetUniform("opacity").set(1f);
        float[] uv = new float[40];
        for (int i = 0; i < 10; i++) {
            var s = sprite(ResourceLocation.fromNamespaceAndPath("renderblender", "misc/cosmic_" + i));
            uv[i * 4] = s.getU0();
            uv[i * 4 + 1] = s.getU1();
            uv[i * 4 + 2] = s.getV0();
            uv[i * 4 + 3] = s.getV1();
        }
        shader.safeGetUniform("cosmicuvs").set(uv);
        return true;
    }

    private static TextureAtlasSprite sprite(ResourceLocation id) {
        return Minecraft.getInstance().getTextureAtlas(InventoryMenu.BLOCK_ATLAS).apply(id);
    }

    public static void renderItem(ItemStack stack, net.minecraft.world.item.ItemDisplayContext context,
                                  BakedModel model, PoseStack pose, MultiBufferSource buffers) {
        ResourceLocation mask;
        if (stack.getItem() instanceof BlockItem item && isBlock(item.getBlock().defaultBlockState())) {
            var block = (MaterialBlock) item.getBlock();
            mask = block.tagPrefix == TagPrefix.frameGt ? FRAME : SOLID;
        } else if (ForgeRegistries.ITEMS.getKey(stack.getItem()).equals(GTNACORE.id("universium_nanites"))) {
            mask = NANITES;
        } else return;
        if (!ready(context == net.minecraft.world.item.ItemDisplayContext.GUI)) return;
        var out = buffers.getBuffer(COSMIC);
        emitModel(model, null, null, pose, out, sprite(mask));
    }

    private static void emitModel(BakedModel model, BlockState state, BlockPos pos, PoseStack pose,
                                  VertexConsumer out, TextureAtlasSprite mask) {
        var random = RandomSource.create(42);
        for (Direction face : Direction.values()) {
            if (state != null && !Block.shouldRenderFace(state, Minecraft.getInstance().level, pos, face,
                    pos.relative(face)))
                continue;
            random.setSeed(42);
            for (var quad : model.getQuads(state, face, random)) emitQuad(quad, pose, out, mask);
        }
        random.setSeed(42);
        for (var quad : model.getQuads(state, null, random)) emitQuad(quad, pose, out, mask);
    }

    private static void emitQuad(BakedQuad quad, PoseStack pose, VertexConsumer out, TextureAtlasSprite mask) {
        int[] data = quad.getVertices();
        var source = quad.getSprite();
        var normal = quad.getDirection().step();
        for (int i = 0; i < 4; i++) {
            int offset = i * 8;
            float x = Float.intBitsToFloat(data[offset]) + normal.x() * 0.001f;
            float y = Float.intBitsToFloat(data[offset + 1]) + normal.y() * 0.001f;
            float z = Float.intBitsToFloat(data[offset + 2]) + normal.z() * 0.001f;
            float u = (Float.intBitsToFloat(data[offset + 4]) - source.getU0()) / (source.getU1() - source.getU0());
            float v = (Float.intBitsToFloat(data[offset + 5]) - source.getV0()) / (source.getV1() - source.getV0());
            vertex(pose, out, x, y, z, mask.getU(u * 16), mask.getV(v * 16), normal);
        }
    }

    private static void vertex(PoseStack pose, VertexConsumer out, float x, float y, float z,
                               float u, float v, Vector3f normal) {
        out.vertex(pose.last().pose(), x, y, z).color(255, 255, 255, 255).uv(u, v)
                .overlayCoords(0, 10).uv2(240, 240)
                .normal(pose.last().normal(), normal.x(), normal.y(), normal.z()).endVertex();
    }

    public static void renderFluidGui(GuiGraphics graphics, float x, float y, float width, float height) {
        renderFluidGui(graphics, x, y, width, height, 0.01f);
    }

    public static void renderFluidGui(GuiGraphics graphics, float x, float y, float width, float height, float depth) {
        if (width <= 0 || height <= 0 || !ready(true)) return;
        graphics.flush();
        var out = graphics.bufferSource().getBuffer(COSMIC);
        var s = sprite(SOLID);
        var n = new Vector3f(0, 0, 1);
        var pose = graphics.pose();
        vertex(pose, out, x, y, depth, s.getU0(), s.getV0(), n);
        vertex(pose, out, x, y + height, depth, s.getU0(), s.getV1(), n);
        vertex(pose, out, x + width, y + height, depth, s.getU1(), s.getV1(), n);
        vertex(pose, out, x + width, y, depth, s.getU1(), s.getV0(), n);
        graphics.bufferSource().endBatch(COSMIC);
    }

    public static void tick(TickEvent.ClientTickEvent event) {
        if (event.phase != TickEvent.Phase.END) return;
        var mc = Minecraft.getInstance();
        if (mc.level != cachedLevel) {
            SURFACES.clear();
            cachedLevel = mc.level;
            nextScan = 0;
        }
        if (mc.level == null || mc.player == null || mc.level.getGameTime() < nextScan) return;
        nextScan = mc.level.getGameTime() + 20;
        SURFACES.clear();
        var center = mc.player.blockPosition();
        // Inspect palettes of already loaded nearby sections; never request/generate chunks.
        for (int cx = (center.getX() >> 4) - 2; cx <= (center.getX() >> 4) + 2; cx++) {
            for (int cz = (center.getZ() >> 4) - 2; cz <= (center.getZ() >> 4) + 2; cz++) {
                var chunk = mc.level.getChunkSource().getChunk(cx, cz, false);
                if (chunk == null) continue;
                var sections = chunk.getSections();
                for (int sectionIndex = 0; sectionIndex < sections.length; sectionIndex++) {
                    int bottom = mc.level.getSectionYFromSectionIndex(sectionIndex) << 4;
                    if (Math.abs(bottom - center.getY()) > 48) continue;
                    var section = sections[sectionIndex];
                    if (!section.maybeHas(s -> isBlock(s) || isFluid(s.getFluidState().getType()))) continue;
                    for (int y = 0; y < 16; y++) for (int z = 0; z < 16; z++) for (int x = 0; x < 16; x++) {
                        var state = section.getBlockState(x, y, z);
                        if (isBlock(state) || isFluid(state.getFluidState().getType())) {
                            var pos = new BlockPos((cx << 4) + x, bottom + y, (cz << 4) + z);
                            if (pos.distSqr(center) <= 32 * 32) SURFACES.add(pos);
                        }
                    }
                }
            }
        }
    }

    public static void renderWorld(RenderLevelStageEvent event) {
        if (event.getStage() != RenderLevelStageEvent.Stage.AFTER_TRANSLUCENT_BLOCKS || SURFACES.isEmpty() ||
                !ready(false))
            return;
        var mc = Minecraft.getInstance();
        if (mc.level == null) return;
        var pose = event.getPoseStack();
        var camera = event.getCamera().getPosition();
        var buffers = mc.renderBuffers().bufferSource();
        var out = buffers.getBuffer(COSMIC);
        for (var pos : SURFACES) {
            if (!event.getFrustum().isVisible(new net.minecraft.world.phys.AABB(pos))) continue;
            var state = mc.level.getBlockState(pos);
            pose.pushPose();
            pose.translate(pos.getX() - camera.x, pos.getY() - camera.y, pos.getZ() - camera.z);
            if (isBlock(state)) {
                var block = (MaterialBlock) state.getBlock();
                emitModel(mc.getBlockRenderer().getBlockModel(state), state, pos, pose, out,
                        sprite(block.tagPrefix == TagPrefix.frameGt ? FRAME : SOLID));
            } else if (isFluid(state.getFluidState().getType())) {
                renderFluidSurface(mc.level, pos, pose, out);
            }
            pose.popPose();
        }
        buffers.endBatch(COSMIC);
    }

    private static float fluidCorner(net.minecraft.client.multiplayer.ClientLevel level, BlockPos pos, int dx, int dz) {
        float total = 0, weight = 0;
        for (int x : new int[] { 0, dx }) for (int z : new int[] { 0, dz }) {
            var sample = pos.offset(x, 0, z);
            var state = level.getFluidState(sample);
            if (isFluid(state.getType())) {
                if (isFluid(level.getFluidState(sample.above()).getType())) return 1;
                float h = state.getOwnHeight();
                float w = h >= 0.8f ? 10 : 1;
                total += h * w;
                weight += w;
            } else if (!level.getBlockState(sample).isSolid()) weight++;
        }
        return weight == 0 ? 0 : total / weight;
    }

    private static void surface(PoseStack pose, VertexConsumer out, TextureAtlasSprite s, Vector3f n, float... points) {
        for (int i = 0; i < 4; i++) {
            vertex(pose, out, points[i * 3] + n.x() * 0.002f, points[i * 3 + 1] + n.y() * 0.002f,
                    points[i * 3 + 2] + n.z() * 0.002f,
                    i >= 2 ? s.getU1() : s.getU0(), (i == 1 || i == 2) ? s.getV1() : s.getV0(), n);
        }
    }

    private static void renderFluidSurface(net.minecraft.client.multiplayer.ClientLevel level, BlockPos pos,
                                           PoseStack pose, VertexConsumer out) {
        float nw = fluidCorner(level, pos, -1, -1), ne = fluidCorner(level, pos, 1, -1);
        float sw = fluidCorner(level, pos, -1, 1), se = fluidCorner(level, pos, 1, 1);
        var s = sprite(SOLID);
        if (!isFluid(level.getFluidState(pos.above()).getType()))
            surface(pose, out, s, new Vector3f(0, 1, 0), 0, nw, 0, 0, sw, 1, 1, se, 1, 1, ne, 0);
        for (var face : Direction.Plane.HORIZONTAL) {
            var neighbor = pos.relative(face);
            if (isFluid(level.getFluidState(neighbor).getType()) ||
                    level.getBlockState(neighbor).isSolidRender(level, neighbor))
                continue;
            var n = face.step();
            switch (face) {
                case NORTH -> surface(pose, out, s, n, 0, 0, 0, 0, nw, 0, 1, ne, 0, 1, 0, 0);
                case SOUTH -> surface(pose, out, s, n, 1, 0, 1, 1, se, 1, 0, sw, 1, 0, 0, 1);
                case WEST -> surface(pose, out, s, n, 0, 0, 1, 0, sw, 1, 0, nw, 0, 0, 0, 0);
                case EAST -> surface(pose, out, s, n, 1, 0, 0, 1, ne, 0, 1, se, 1, 1, 0, 1);
                default -> {}
            }
        }
        var below = pos.below();
        if (!isFluid(level.getFluidState(below).getType()) && !level.getBlockState(below).isSolidRender(level, below))
            surface(pose, out, s, new Vector3f(0, -1, 0), 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1);
    }
}
