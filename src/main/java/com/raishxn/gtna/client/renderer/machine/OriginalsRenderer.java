package com.raishxn.gtna.client.renderer.machine;

import com.gregtechceu.gtceu.client.renderer.machine.DynamicRender;
import com.gregtechceu.gtceu.client.renderer.machine.DynamicRenderManager;
import com.gregtechceu.gtceu.client.renderer.machine.DynamicRenderType;

import net.minecraft.client.renderer.GameRenderer;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.Vec3;

import com.mojang.blaze3d.platform.GlStateManager;
import com.mojang.blaze3d.systems.RenderSystem;
import com.mojang.blaze3d.vertex.BufferBuilder;
import com.mojang.blaze3d.vertex.DefaultVertexFormat;
import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.blaze3d.vertex.Tesselator;
import com.mojang.blaze3d.vertex.VertexFormat;
import com.mojang.serialization.Codec;
import com.raishxn.gtna.GTNACORE;
import com.raishxn.gtna.api.machine.feature.rift.RiftCore;
import com.raishxn.gtna.common.machine.multiblock.originals.ColliderRingMachine;
import com.raishxn.gtna.common.machine.multiblock.originals.LanceMachine;
import com.raishxn.gtna.common.machine.multiblock.originals.OriginalMachine;
import com.raishxn.gtna.common.machine.multiblock.originals.RiftGateMachine;
import org.joml.Matrix4f;
import org.joml.Quaternionf;
import org.joml.Vector3f;

import java.util.LinkedHashMap;
import java.util.Map;

/**
 * Effects of the original multiblocks, drawn after translucent blocks like the Forge of Gods: the collider's two
 * counter-rotating beams and pulsing core, the rift's swirling event horizon, and the lance's muzzle flash and bolt.
 * The structures themselves are real blocks.
 */
public final class OriginalsRenderer {

    private static final Map<BlockPos, OriginalMachine> QUEUE = new LinkedHashMap<>();

    private OriginalsRenderer() {}

    public static void onRenderLevelStage(net.minecraftforge.client.event.RenderLevelStageEvent event) {
        if (event.getStage() != net.minecraftforge.client.event.RenderLevelStageEvent.Stage.AFTER_TRANSLUCENT_BLOCKS ||
                QUEUE.isEmpty())
            return;
        Vec3 cam = event.getCamera().getPosition();
        PoseStack pose = event.getPoseStack();
        float time = (float) ((net.minecraft.Util.getMillis() % 3_600_000L) / 1000.0);
        Matrix4f projection = new Matrix4f(event.getProjectionMatrix());
        for (var m : QUEUE.values()) {
            if (m instanceof ColliderRingMachine c && c.isCaptured() && !c.isInValid()) {
                pose.pushPose();
                spinningParts(c, pose, cam, projection, time);
                pose.popPose();
            } else if (m instanceof LanceMachine l && l.isCaptured() && !l.isInValid()) {
                pose.pushPose();
                turret(l, pose, cam, projection);
                pose.popPose();
            }
        }
        try {
            RenderSystem.enableBlend();
            RenderSystem.blendFunc(GlStateManager.SourceFactor.SRC_ALPHA, GlStateManager.DestFactor.ONE);
            RenderSystem.depthMask(false);
            RenderSystem.disableCull();
            RenderSystem.setShader(GameRenderer::getPositionColorShader);
            for (var m : QUEUE.values()) {
                if (m.isInValid() || !m.isFormed()) continue;
                pose.pushPose();
                if (m instanceof ColliderRingMachine c && c.isBeamOn()) collider(c, pose, cam, time);
                else if (m instanceof RiftGateMachine r && r.isRiftOpen()) rift(r, pose, cam, time);
                else if (m instanceof LanceMachine l) lance(l, pose, cam, time);
                pose.popPose();
            }
        } finally {
            QUEUE.clear();
            RenderSystem.depthMask(true);
            RenderSystem.disableBlend();
            RenderSystem.defaultBlendFunc();
            RenderSystem.enableCull();
        }
    }

    /** Pose at {@code point}, with +Z along the machine's back direction. */
    private static Matrix4f frame(OriginalMachine m, PoseStack pose, Vec3 cam, BlockPos point) {
        pose.translate(point.getX() + 0.5 - cam.x, point.getY() + 0.5 - cam.y, point.getZ() + 0.5 - cam.z);
        Direction back = m.getFrontFacing().getOpposite();
        var rot = new Quaternionf().rotationTo(new Vector3f(0, 0, 1),
                new Vector3f(back.getStepX(), back.getStepY(), back.getStepZ()));
        return new Matrix4f(pose.last().pose()).rotate(rot);
    }

    private static void collider(ColliderRingMachine c, PoseStack pose, Vec3 cam, float time) {
        Matrix4f m = frame(c, pose, cam, c.offset(ColliderRingMachine.CENTER_UP, ColliderRingMachine.CENTER_BACK));
        BufferBuilder buf = Tesselator.getInstance().getBuilder();
        buf.begin(VertexFormat.Mode.TRIANGLES, DefaultVertexFormat.POSITION_COLOR);
        float speed = 1.2f + 2.5f * (float) c.beamEnergyShare();
        double r = ColliderRingMachine.RING_RADIUS - 2;
        for (int beam = 0; beam < 2; beam++) {
            float dir = beam == 0 ? 1 : -1;
            float cr = beam == 0 ? 1f : 0.5f, cg = beam == 0 ? 0.5f : 0.85f, cb = 1f;
            for (int k = 0; k < 40; k++) {
                double a = dir * (time * speed - k * 0.02);
                float size = 1.4f * (1 - k / 40f), alpha = 0.9f * (1 - k / 40f);
                billboard(buf, m, (float) (Math.cos(a) * r), (float) (Math.sin(a) * r), 0, size, cr, cg, cb, alpha);
            }
        }
        float pulse = 0.5f + 0.5f * (float) Math.sin(time * 2.2);
        sphereGlow(buf, m, 9 + 2 * pulse, 0.65f, 0.4f, 1f, 0.25f + 0.25f * pulse);
        Tesselator.getInstance().end();
    }

    private static void rift(RiftGateMachine r, PoseStack pose, Vec3 cam, float time) {
        Matrix4f m = frame(r, pose, cam, r.offset(RiftGateMachine.CENTER_UP, RiftGateMachine.CENTER_BACK));
        float[] col = biomeColour(r.biome());
        float strength = (float) Math.max(0.15, r.stability() / 100);
        float res = (float) r.resonance();
        BufferBuilder buf = Tesselator.getInstance().getBuilder();
        buf.begin(VertexFormat.Mode.TRIANGLES, DefaultVertexFormat.POSITION_COLOR);
        int seg = 96, rings = 16;
        float R = (float) RiftGateMachine.INNER_RADIUS;
        for (int ri = 0; ri < rings; ri++) {
            float r0 = R * ri / rings, r1 = R * (ri + 1) / rings;
            for (int i = 0; i < seg; i++) {
                double a0 = 2 * Math.PI * i / seg, a1 = 2 * Math.PI * (i + 1) / seg;
                float swirl = 0.5f + 0.5f * (float) Math.sin(a0 * 5 + 30 / (r0 + 4) - time * (1.5 + res));
                float fade = 1 - (float) ri / rings;
                float alpha = strength * (0.25f + 0.5f * swirl) * (0.4f + 0.6f * fade);
                float white = (float) Math.pow(fade, 6);
                quad(buf, m, (float) Math.cos(a0) * r0, (float) Math.sin(a0) * r0, (float) Math.cos(a0) * r1,
                        (float) Math.sin(a0) * r1, (float) Math.cos(a1) * r1, (float) Math.sin(a1) * r1,
                        (float) Math.cos(a1) * r0, (float) Math.sin(a1) * r0, col[0] + white, col[1] + white,
                        col[2] + white, alpha);
            }
        }
        Tesselator.getInstance().end();
    }

    private static float[] biomeColour(RiftCore.Biome biome) {
        return switch (biome) {
            case CRYSTAL_PLAINS -> new float[] { 0.5f, 0.9f, 1f };
            case MERCURY_OCEAN -> new float[] { 0.75f, 0.78f, 0.85f };
            case FORGE_WORLD -> new float[] { 1f, 0.45f, 0.15f };
            case SPORE_FOREST -> new float[] { 0.4f, 1f, 0.45f };
            case ANTIMATTER_ABYSS -> new float[] { 1f, 0.2f, 0.5f };
            case CIVILISATION_RELIC -> new float[] { 1f, 0.85f, 0.4f };
            case VOID -> new float[] { 0.35f, 0.15f, 0.65f };
        };
    }

    private static void lance(LanceMachine l, PoseStack pose, Vec3 cam, float time) {
        int since = l.secondsSinceShot();
        if (since > 2) return;
        BlockPos muzzle = l.offset(LanceMachine.MUZZLE_UP, LanceMachine.MUZZLE_BACK);
        BlockPos pivot = PIVOTS.get(l.getPos());
        float[] yaw = YAW.get(l.getPos());
        Matrix4f m;
        if (l.isCaptured() && pivot != null && yaw != null) {
            // Follow the slewing gun: turn the muzzle and the barrel axis about the turret bearing.
            pose.translate(pivot.getX() + 0.5 - cam.x, pivot.getY() + 0.5 - cam.y, pivot.getZ() + 0.5 - cam.z);
            pose.mulPose(new Quaternionf().rotationY(yaw[0]));
            pose.translate(muzzle.getX() - pivot.getX(), muzzle.getY() - pivot.getY(), muzzle.getZ() - pivot.getZ());
            Direction back = l.getFrontFacing().getOpposite();
            m = new Matrix4f(pose.last().pose()).rotate(new Quaternionf().rotationTo(new Vector3f(0, 0, 1),
                    new Vector3f(back.getStepX(), back.getStepY(), back.getStepZ())));
        } else m = frame(l, pose, cam, muzzle);
        float phase = (since + (time % 1)) / 2f;
        BufferBuilder buf = Tesselator.getInstance().getBuilder();
        buf.begin(VertexFormat.Mode.TRIANGLES, DefaultVertexFormat.POSITION_COLOR);
        float flash = Math.max(0, 1 - phase * 4);
        sphereGlow(buf, m, 6 + 10 * flash, 0.6f, 1f, 0.7f, flash);
        float z0 = 10 + phase * 600, z1 = z0 + 80;
        float a = Math.max(0, 1 - phase);
        for (int i = 0; i < 4; i++) {
            double ang = i * Math.PI / 4;
            float x = (float) Math.cos(ang) * 1.2f, y = (float) Math.sin(ang) * 1.2f;
            quad(buf, m, -x, -y, x, y, x, y, -x, -y, 0.7f, 1f, 0.8f, a, z0, z0, z1, z1);
        }
        Tesselator.getInstance().end();
    }

    // ------------------------------------------------------------------ captured parts

    private static final Map<BlockPos, com.mojang.blaze3d.vertex.VertexBuffer[]> MESHES = new java.util.HashMap<>();

    /** The collider's main ring and gyroscopes, taken into the controller, spinning in opposite directions. */
    private static void spinningParts(ColliderRingMachine c, PoseStack pose, Vec3 cam, Matrix4f projection,
                                      float time) {
        var level = c.getLevel();
        if (level == null) return;
        BlockPos center = c.offset(ColliderRingMachine.CENTER_UP, ColliderRingMachine.CENTER_BACK);
        var meshes = MESHES.computeIfAbsent(c.getPos().immutable(), k -> new com.mojang.blaze3d.vertex.VertexBuffer[] {
                mesh(c, "ring", center), mesh(c, "gyro", center) });
        var shader = GameRenderer.getRendertypeCutoutShader();
        if (shader == null) return;
        pose.translate(center.getX() + 0.5 - cam.x, center.getY() + 0.5 - cam.y, center.getZ() + 0.5 - cam.z);
        Direction back = c.getFrontFacing().getOpposite();
        var axis = new Vector3f(back.getStepX(), back.getStepY(), back.getStepZ());
        RenderSystem.setShaderTexture(0, net.minecraft.client.renderer.texture.TextureAtlas.LOCATION_BLOCKS);
        net.minecraft.client.Minecraft.getInstance().gameRenderer.lightTexture().turnOnLightLayer();
        RenderSystem.enableDepthTest();
        RenderSystem.depthMask(true);
        RenderSystem.disableBlend();
        float[] spin = { time * 0.12f, -time * 0.5f };
        for (int i = 0; i < 2; i++) {
            if (meshes[i] == null) continue;
            Matrix4f model = new Matrix4f(pose.last().pose()).rotate(spin[i], axis).translate(-0.5f, -0.5f, -0.5f);
            meshes[i].bind();
            meshes[i].drawWithShader(model, projection, shader);
        }
        com.mojang.blaze3d.vertex.VertexBuffer.unbind();
    }

    private static final Map<BlockPos, BlockPos> PIVOTS = new java.util.HashMap<>();
    private static final Map<BlockPos, float[]> YAW = new java.util.HashMap<>();

    /** The lance's gun, taken into the controller, slewing about the vertical axis to the selected body. */
    private static void turret(LanceMachine l, PoseStack pose, Vec3 cam, Matrix4f projection) {
        if (l.getLevel() == null) return;
        BlockPos key = l.getPos().immutable();
        BlockPos pivot = PIVOTS.computeIfAbsent(key, k -> pivot(l));
        if (pivot == null) return;
        var meshes = MESHES.computeIfAbsent(key,
                k -> new com.mojang.blaze3d.vertex.VertexBuffer[] { mesh(l, "kinetic_orbital_lance", "gun", pivot) });
        var shader = GameRenderer.getRendertypeCutoutShader();
        if (shader == null || meshes[0] == null) return;
        // Slew towards the target at about 6 degrees a second.
        float[] yaw = YAW.computeIfAbsent(key, k -> new float[] { (float) l.yaw(), net.minecraft.Util.getMillis() });
        float dt = Math.min(1, (net.minecraft.Util.getMillis() - yaw[1]) / 1000f);
        yaw[1] = net.minecraft.Util.getMillis();
        float diff = (float) l.yaw() - yaw[0];
        yaw[0] += Math.signum(diff) * Math.min(Math.abs(diff), 0.1f * dt);
        pose.translate(pivot.getX() + 0.5 - cam.x, pivot.getY() + 0.5 - cam.y, pivot.getZ() + 0.5 - cam.z);
        RenderSystem.setShaderTexture(0, net.minecraft.client.renderer.texture.TextureAtlas.LOCATION_BLOCKS);
        net.minecraft.client.Minecraft.getInstance().gameRenderer.lightTexture().turnOnLightLayer();
        RenderSystem.enableDepthTest();
        RenderSystem.depthMask(true);
        RenderSystem.disableBlend();
        Matrix4f model = new Matrix4f(pose.last().pose()).rotate(yaw[0], new Vector3f(0, 1, 0))
                .translate(-0.5f, -0.5f, -0.5f);
        meshes[0].bind();
        meshes[0].drawWithShader(model, projection, shader);
        com.mojang.blaze3d.vertex.VertexBuffer.unbind();
    }

    /** Horizontal centroid of the gun at the height of its lowest block: the turret bearing. */
    private static BlockPos pivot(LanceMachine l) {
        var parts = com.raishxn.gtna.common.machine.multiblock.originals.CapturedParts.positions(l.getLevel(),
                "kinetic_orbital_lance", "gun", l.getPos(), l.getFrontFacing(), l.getUpwardsFacing(), l.isFlipped());
        if (parts.isEmpty()) return null;
        long x = 0, z = 0;
        int y = Integer.MAX_VALUE;
        for (BlockPos p : parts.keySet()) {
            x += p.getX();
            z += p.getZ();
            y = Math.min(y, p.getY());
        }
        return new BlockPos((int) (x / parts.size()), y, (int) (z / parts.size()));
    }

    private static com.mojang.blaze3d.vertex.VertexBuffer mesh(ColliderRingMachine c, String tag, BlockPos center) {
        return mesh(c, "antimatter_collider_ring", tag, center);
    }

    private static com.mojang.blaze3d.vertex.VertexBuffer mesh(OriginalMachine c, String name, String tag,
                                                               BlockPos center) {
        var parts = com.raishxn.gtna.common.machine.multiblock.originals.CapturedParts.positions(c.getLevel(),
                name, tag, c.getPos(), c.getFrontFacing(), c.getUpwardsFacing(), c.isFlipped());
        if (parts.isEmpty()) return null;
        var dispatcher = net.minecraft.client.Minecraft.getInstance().getBlockRenderer();
        var random = net.minecraft.util.RandomSource.create(42);
        var builder = new BufferBuilder(
                Math.min(parts.size() * 4 * 4, 1 << 18) * DefaultVertexFormat.BLOCK.getVertexSize());
        builder.begin(VertexFormat.Mode.QUADS, DefaultVertexFormat.BLOCK);
        PoseStack ps = new PoseStack();
        for (var e : parts.entrySet()) {
            BlockPos p = e.getKey();
            var state = com.raishxn.gtna.common.machine.multiblock.originals.CapturedParts
                    .blockFor(name, e.getValue()).defaultBlockState();
            var model = dispatcher.getBlockModel(state);
            ps.pushPose();
            ps.translate(p.getX() - center.getX(), p.getY() - center.getY(), p.getZ() - center.getZ());
            for (Direction side : Direction.values()) {
                if (parts.containsKey(p.relative(side))) continue;
                random.setSeed(42);
                for (var quad : model.getQuads(state, side, random,
                        net.minecraftforge.client.model.data.ModelData.EMPTY, null))
                    builder.putBulkData(ps.last(), quad, 1f, 1f, 1f,
                            net.minecraft.client.renderer.LightTexture.FULL_BRIGHT,
                            net.minecraft.client.renderer.texture.OverlayTexture.NO_OVERLAY);
            }
            ps.popPose();
        }
        var mesh = new com.mojang.blaze3d.vertex.VertexBuffer(com.mojang.blaze3d.vertex.VertexBuffer.Usage.STATIC);
        mesh.bind();
        mesh.upload(builder.end());
        com.mojang.blaze3d.vertex.VertexBuffer.unbind();
        return mesh;
    }

    // ------------------------------------------------------------------ primitives

    private static void quad(BufferBuilder b, Matrix4f m, float x0, float y0, float x1, float y1, float x2, float y2,
                             float x3, float y3, float r, float g, float bl, float a) {
        quad(b, m, x0, y0, x1, y1, x2, y2, x3, y3, r, g, bl, a, 0, 0, 0, 0);
    }

    private static void quad(BufferBuilder b, Matrix4f m, float x0, float y0, float x1, float y1, float x2, float y2,
                             float x3, float y3, float r, float g, float bl, float a, float z0, float z1, float z2,
                             float z3) {
        float[][] v = { { x0, y0, z0 }, { x1, y1, z1 }, { x2, y2, z2 }, { x3, y3, z3 } };
        for (int k : new int[] { 0, 1, 2, 0, 2, 3 })
            b.vertex(m, v[k][0], v[k][1], v[k][2]).color(Math.min(1, r), Math.min(1, g), Math.min(1, bl), a)
                    .endVertex();
    }

    private static void billboard(BufferBuilder b, Matrix4f m, float x, float y, float z, float s, float r, float g,
                                  float bl, float a) {
        for (int plane = 0; plane < 3; plane++) {
            float[][] v = switch (plane) {
                case 0 -> new float[][] { { -s, -s, 0 }, { s, -s, 0 }, { s, s, 0 }, { -s, s, 0 } };
                case 1 -> new float[][] { { -s, 0, -s }, { s, 0, -s }, { s, 0, s }, { -s, 0, s } };
                default -> new float[][] { { 0, -s, -s }, { 0, s, -s }, { 0, s, s }, { 0, -s, s } };
            };
            for (int k : new int[] { 0, 1, 2, 0, 2, 3 })
                b.vertex(m, x + v[k][0], y + v[k][1], z + v[k][2]).color(r, g, bl, a).endVertex();
        }
    }

    private static void sphereGlow(BufferBuilder b, Matrix4f m, float radius, float r, float g, float bl, float a) {
        int seg = 32;
        for (int plane = 0; plane < 3; plane++) {
            for (int i = 0; i < seg; i++) {
                double a0 = 2 * Math.PI * i / seg, a1 = 2 * Math.PI * (i + 1) / seg;
                float[] p0 = ring(plane, a0, radius), p1 = ring(plane, a1, radius);
                b.vertex(m, 0, 0, 0).color(r, g, bl, a).endVertex();
                b.vertex(m, p0[0], p0[1], p0[2]).color(r, g, bl, 0f).endVertex();
                b.vertex(m, p1[0], p1[1], p1[2]).color(r, g, bl, 0f).endVertex();
            }
        }
    }

    private static float[] ring(int plane, double a, float radius) {
        float c = (float) Math.cos(a) * radius, s = (float) Math.sin(a) * radius;
        return switch (plane) {
            case 0 -> new float[] { c, s, 0 };
            case 1 -> new float[] { c, 0, s };
            default -> new float[] { 0, c, s };
        };
    }

    // ------------------------------------------------------------------ the three dynamic renders

    abstract static class Base<M extends OriginalMachine, R extends Base<M, R>> extends DynamicRender<M, R> {

        @Override
        public boolean shouldRenderOffScreen(M machine) {
            return true;
        }

        @Override
        public int getViewDistance() {
            return 384;
        }

        @Override
        public void render(M machine, float partialTicks, PoseStack poseStack, MultiBufferSource buffer, int light,
                           int overlay) {
            if (machine.getLevel() != null && machine.isFormed()) QUEUE.put(machine.getPos().immutable(), machine);
        }
    }

    public static final class ColliderRender extends Base<ColliderRingMachine, ColliderRender> {

        public static final Codec<ColliderRender> CODEC = Codec.unit(ColliderRender::new);
        public static final DynamicRenderType<ColliderRingMachine, ColliderRender> TYPE = DynamicRenderManager
                .register(GTNACORE.id("collider/render"), new DynamicRenderType<>(CODEC));

        @Override
        public DynamicRenderType<ColliderRingMachine, ColliderRender> getType() {
            return TYPE;
        }

        @Override
        public boolean shouldRender(ColliderRingMachine machine, Vec3 cameraPos) {
            return machine.isBeamOn() || machine.isCaptured();
        }

        @Override
        public AABB getRenderBoundingBox(ColliderRingMachine machine) {
            return new AABB(machine.offset(ColliderRingMachine.CENTER_UP, ColliderRingMachine.CENTER_BACK)).inflate(70);
        }
    }

    public static final class RiftRender extends Base<RiftGateMachine, RiftRender> {

        public static final Codec<RiftRender> CODEC = Codec.unit(RiftRender::new);
        public static final DynamicRenderType<RiftGateMachine, RiftRender> TYPE = DynamicRenderManager
                .register(GTNACORE.id("rift/render"), new DynamicRenderType<>(CODEC));

        @Override
        public DynamicRenderType<RiftGateMachine, RiftRender> getType() {
            return TYPE;
        }

        @Override
        public boolean shouldRender(RiftGateMachine machine, Vec3 cameraPos) {
            return machine.isRiftOpen();
        }

        @Override
        public AABB getRenderBoundingBox(RiftGateMachine machine) {
            return new AABB(machine.offset(RiftGateMachine.CENTER_UP, RiftGateMachine.CENTER_BACK)).inflate(60);
        }
    }

    public static final class LanceRender extends Base<LanceMachine, LanceRender> {

        public static final Codec<LanceRender> CODEC = Codec.unit(LanceRender::new);
        public static final DynamicRenderType<LanceMachine, LanceRender> TYPE = DynamicRenderManager
                .register(GTNACORE.id("lance/render"), new DynamicRenderType<>(CODEC));

        @Override
        public DynamicRenderType<LanceMachine, LanceRender> getType() {
            return TYPE;
        }

        @Override
        public boolean shouldRender(LanceMachine machine, Vec3 cameraPos) {
            return machine.secondsSinceShot() <= 2 || machine.isCaptured();
        }

        @Override
        public AABB getRenderBoundingBox(LanceMachine machine) {
            return new AABB(machine.offset(LanceMachine.MUZZLE_UP, LanceMachine.MUZZLE_BACK)).inflate(700);
        }
    }
}
