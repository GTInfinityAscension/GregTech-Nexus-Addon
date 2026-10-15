package com.raishxn.gtna.client.renderer.machine;

import com.gregtechceu.gtceu.client.renderer.machine.DynamicRender;
import com.gregtechceu.gtceu.client.renderer.machine.DynamicRenderManager;
import com.gregtechceu.gtceu.client.renderer.machine.DynamicRenderType;

import net.minecraft.client.renderer.GameRenderer;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.core.BlockPos;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.Vec3;

import com.mojang.blaze3d.systems.RenderSystem;
import com.mojang.blaze3d.vertex.BufferBuilder;
import com.mojang.blaze3d.vertex.DefaultVertexFormat;
import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.blaze3d.vertex.Tesselator;
import com.mojang.blaze3d.vertex.VertexBuffer;
import com.mojang.blaze3d.vertex.VertexFormat;
import com.mojang.serialization.Codec;
import com.raishxn.gtna.GTNACORE;
import com.raishxn.gtna.common.machine.multiblock.originals.StellarChamberMachine;
import org.jetbrains.annotations.Nullable;
import org.joml.Matrix4f;
import org.joml.Vector3f;

import java.util.LinkedHashMap;
import java.util.Map;

/**
 * Neutron star of the Stellar Containment Chamber: a bright blue-white star (Forge of Gods star shader, blue), two
 * pulsar beams sweeping around the tilted magnetic axis, dipole field lines and an orange accretion disk. In black
 * hole mode the star turns into a black sphere with a photon ring. The hull and bands are real blocks and stay still.
 */
public class StellarChamberRenderer extends DynamicRender<StellarChamberMachine, StellarChamberRenderer> {

    public static final Codec<StellarChamberRenderer> CODEC = Codec.unit(StellarChamberRenderer::new);
    public static final DynamicRenderType<StellarChamberMachine, StellarChamberRenderer> TYPE = DynamicRenderManager
            .register(GTNACORE.id("stellar_chamber/render"), new DynamicRenderType<>(CODEC));

    private static final ResourceLocation[] LAYERS = { GTNACORE.id("textures/render/godforge/star_layer_0.png"),
            GTNACORE.id("textures/render/godforge/star_layer_1.png"),
            GTNACORE.id("textures/render/godforge/star_layer_2.png") };
    private static final float STAR_RADIUS = 5f, BEAM_LENGTH = 40f, DISK_INNER = 9f, DISK_OUTER = 24f;
    private static final float AXIS_TILT = 0.5f;

    @Nullable
    private static VertexBuffer sphere;
    private static final Map<BlockPos, StellarChamberMachine> QUEUE = new LinkedHashMap<>();

    @Override
    public DynamicRenderType<StellarChamberMachine, StellarChamberRenderer> getType() {
        return TYPE;
    }

    @Override
    public boolean shouldRender(StellarChamberMachine machine, Vec3 cameraPos) {
        return machine.isStarLit();
    }

    @Override
    public boolean shouldRenderOffScreen(StellarChamberMachine machine) {
        return true;
    }

    @Override
    public int getViewDistance() {
        return 256;
    }

    @Override
    public AABB getRenderBoundingBox(StellarChamberMachine machine) {
        return new AABB(machine.center()).inflate(BEAM_LENGTH + 2);
    }

    @Override
    public void render(StellarChamberMachine machine, float partialTicks, PoseStack poseStack, MultiBufferSource buffer,
                       int combinedLight, int combinedOverlay) {
        if (machine.getLevel() != null && machine.isStarLit()) QUEUE.put(machine.getPos().immutable(), machine);
    }

    public static void onRenderLevelStage(net.minecraftforge.client.event.RenderLevelStageEvent event) {
        if (event.getStage() != net.minecraftforge.client.event.RenderLevelStageEvent.Stage.AFTER_TRANSLUCENT_BLOCKS ||
                QUEUE.isEmpty())
            return;
        Vec3 camera = event.getCamera().getPosition();
        PoseStack pose = event.getPoseStack();
        Matrix4f projection = new Matrix4f(event.getProjectionMatrix());
        try {
            for (var machine : QUEUE.values()) {
                if (machine.isInValid() || !machine.isStarLit()) continue;
                BlockPos c = machine.center();
                pose.pushPose();
                pose.translate(c.getX() + 0.5 - camera.x, c.getY() + 0.5 - camera.y, c.getZ() + 0.5 - camera.z);
                draw(machine, pose, projection);
                pose.popPose();
            }
        } finally {
            QUEUE.clear();
            RenderSystem.depthMask(true);
            RenderSystem.disableBlend();
            RenderSystem.defaultBlendFunc();
            RenderSystem.enableCull();
            RenderSystem.enableDepthTest();
        }
    }

    private static void draw(StellarChamberMachine machine, PoseStack pose, Matrix4f projection) {
        float time = (float) ((net.minecraft.Util.getMillis() % 3_600_000L) / 1000.0);
        // Visible spin: real pulsars spin far too fast to see, so the beams turn once per (period x 2000) seconds.
        float spin = (float) (time * 2 * Math.PI / Math.max(0.5, machine.renderPeriod() * 2000));
        Matrix4f center = new Matrix4f(pose.last().pose());
        boolean hole = machine.isBlackHole();
        float r = hole ? 1f : 0.62f, g = hole ? 1f : 0.82f, b = 1f;
        if (machine.isMagnetar()) {
            r = 0.85f;
            g = 0.55f;
        }
        RenderSystem.enableDepthTest();
        RenderSystem.disableCull();
        if (hole) drawBlackSphere(center, projection);
        else {
            var shader = GodforgeShaders.star();
            if (shader != null) {
                RenderSystem.depthMask(true);
                RenderSystem.disableBlend();
                layer(shader, center, projection, LAYERS[0], STAR_RADIUS, 1f, r, g, b, spin * 57.3f);
                RenderSystem.enableBlend();
                RenderSystem.defaultBlendFunc();
                RenderSystem.depthMask(false);
                layer(shader, center, projection, LAYERS[1], STAR_RADIUS * 1.04f, 0.45f, r, g, b, -spin * 40f);
                layer(shader, center, projection, LAYERS[2], STAR_RADIUS * 1.08f, 0.25f, r, g, b, spin * 23f);
            }
        }
        RenderSystem.enableBlend();
        RenderSystem.blendFunc(com.mojang.blaze3d.platform.GlStateManager.SourceFactor.SRC_ALPHA,
                com.mojang.blaze3d.platform.GlStateManager.DestFactor.ONE);
        RenderSystem.depthMask(false);
        RenderSystem.setShader(GameRenderer::getPositionColorShader);
        Matrix4f axis = new Matrix4f(center).rotateZ(AXIS_TILT).rotateY(spin);
        if (!hole) {
            beams(axis, r, g, b);
            fieldLines(axis, r, g, b);
            corona(center, projection, r, g, b, time);
        }
        disk(new Matrix4f(center).rotateX(0.22f).rotateY(time * 0.4f), hole);
    }

    private static void layer(net.minecraft.client.renderer.ShaderInstance shader, Matrix4f center, Matrix4f projection,
                              ResourceLocation texture, float scale, float alpha, float r, float g, float b,
                              float degrees) {
        Matrix4f model = new Matrix4f(center)
                .rotate((float) Math.toRadians(degrees), new Vector3f(0, 1, 0.3f).normalize())
                .scale(scale);
        RenderSystem.setShaderTexture(0, texture);
        shader.safeGetUniform("StarColor").set(r, g, b, alpha);
        shader.safeGetUniform("Gamma").set(3f);
        var mesh = sphere();
        mesh.bind();
        mesh.drawWithShader(model, projection, shader);
        VertexBuffer.unbind();
    }

    private static void drawBlackSphere(Matrix4f center, Matrix4f projection) {
        RenderSystem.setShader(GameRenderer::getPositionColorShader);
        RenderSystem.disableBlend();
        RenderSystem.depthMask(true);
        BufferBuilder buf = Tesselator.getInstance().getBuilder();
        buf.begin(VertexFormat.Mode.TRIANGLES, DefaultVertexFormat.POSITION_COLOR);
        int n = 32;
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                float[][] q = new float[4][];
                for (int k = 0; k < 4; k++) {
                    double phi = Math.PI * (i + (k == 1 || k == 2 ? 1 : 0)) / n - Math.PI / 2;
                    double th = 2 * Math.PI * (j + (k >= 2 ? 1 : 0)) / n;
                    q[k] = new float[] { (float) (STAR_RADIUS * Math.cos(phi) * Math.cos(th)),
                            (float) (STAR_RADIUS * Math.sin(phi)),
                            (float) (STAR_RADIUS * Math.cos(phi) * Math.sin(th)) };
                }
                for (int k : new int[] { 0, 1, 2, 0, 2, 3 })
                    buf.vertex(center, q[k][0], q[k][1], q[k][2]).color(0, 0, 0, 255).endVertex();
            }
        }
        Tesselator.getInstance().end();
    }

    /** Two narrow cones along the magnetic axis. */
    private static void beams(Matrix4f axis, float r, float g, float b) {
        BufferBuilder buf = Tesselator.getInstance().getBuilder();
        buf.begin(VertexFormat.Mode.TRIANGLES, DefaultVertexFormat.POSITION_COLOR);
        int seg = 16;
        for (int side : new int[] { 1, -1 }) {
            for (int i = 0; i < seg; i++) {
                double a0 = 2 * Math.PI * i / seg, a1 = 2 * Math.PI * (i + 1) / seg;
                float w = 3.2f;
                buf.vertex(axis, 0, side * STAR_RADIUS, 0).color(r, g, b, 0.9f).endVertex();
                buf.vertex(axis, (float) Math.cos(a0) * w, side * BEAM_LENGTH, (float) Math.sin(a0) * w)
                        .color(r, g, b, 0f)
                        .endVertex();
                buf.vertex(axis, (float) Math.cos(a1) * w, side * BEAM_LENGTH, (float) Math.sin(a1) * w)
                        .color(r, g, b, 0f)
                        .endVertex();
            }
        }
        Tesselator.getInstance().end();
    }

    /** Dipole field lines r = R sin^2(theta), co-rotating with the beams. */
    private static void fieldLines(Matrix4f axis, float r, float g, float b) {
        BufferBuilder buf = Tesselator.getInstance().getBuilder();
        RenderSystem.lineWidth(2f);
        buf.begin(VertexFormat.Mode.DEBUG_LINES, DefaultVertexFormat.POSITION_COLOR);
        for (int k = 0; k < 10; k++) {
            double ph = k * Math.PI / 5;
            float big = 9 + (k % 3) * 5;
            float[] prev = null;
            for (int i = 0; i <= 40; i++) {
                double th = 0.2 + i / 40.0 * (Math.PI - 0.4);
                double rr = big * Math.sin(th) * Math.sin(th);
                float[] p = { (float) (rr * Math.sin(th) * Math.cos(ph)), (float) (rr * Math.cos(th)),
                        (float) (rr * Math.sin(th) * Math.sin(ph)) };
                if (prev != null) {
                    buf.vertex(axis, prev[0], prev[1], prev[2]).color(r, g, b, 0.5f).endVertex();
                    buf.vertex(axis, p[0], p[1], p[2]).color(r, g, b, 0.5f).endVertex();
                }
                prev = p;
            }
        }
        Tesselator.getInstance().end();
    }

    /** Camera-facing glow quads around the star. */
    private static void corona(Matrix4f center, Matrix4f projection, float r, float g, float b, float time) {
        BufferBuilder buf = Tesselator.getInstance().getBuilder();
        buf.begin(VertexFormat.Mode.TRIANGLES, DefaultVertexFormat.POSITION_COLOR);
        float pulse = 1 + 0.06f * (float) Math.sin(time * 6);
        int seg = 48;
        for (float[] shell : new float[][] { { STAR_RADIUS * 1.1f, STAR_RADIUS * 2.6f * pulse, 0.35f } }) {
            for (int plane = 0; plane < 3; plane++) {
                for (int i = 0; i < seg; i++) {
                    double a0 = 2 * Math.PI * i / seg, a1 = 2 * Math.PI * (i + 1) / seg;
                    float[][] v = { ring(plane, a0, shell[0]), ring(plane, a0, shell[1]), ring(plane, a1, shell[1]),
                            ring(plane, a1, shell[0]) };
                    float[] al = { shell[2], 0, 0, shell[2] };
                    for (int k : new int[] { 0, 1, 2, 0, 2, 3 })
                        buf.vertex(center, v[k][0], v[k][1], v[k][2]).color(r, g, b, al[k]).endVertex();
                }
            }
        }
        Tesselator.getInstance().end();
    }

    private static float[] ring(int plane, double a, float radius) {
        float c = (float) Math.cos(a) * radius, s = (float) Math.sin(a) * radius;
        return switch (plane) {
            case 0 -> new float[] { c, s, 0 };
            case 1 -> new float[] { c, 0, s };
            default -> new float[] { 0, c, s };
        };
    }

    /** Accretion disk with spiral brightness; brighter and thinner around a black hole. */
    private static void disk(Matrix4f m, boolean hole) {
        BufferBuilder buf = Tesselator.getInstance().getBuilder();
        buf.begin(VertexFormat.Mode.TRIANGLES, DefaultVertexFormat.POSITION_COLOR);
        int seg = 96, rings = 10;
        float inner = hole ? 6.5f : DISK_INNER;
        for (int ri = 0; ri < rings; ri++) {
            float r0 = inner + (DISK_OUTER - inner) * ri / rings, r1 = inner + (DISK_OUTER - inner) * (ri + 1) / rings;
            for (int i = 0; i < seg; i++) {
                double a0 = 2 * Math.PI * i / seg, a1 = 2 * Math.PI * (i + 1) / seg;
                float s = 0.5f + 0.5f * (float) Math.sin(a0 * 6 + 40 / r0);
                float fade = 1 - (float) ri / rings;
                float alpha = (hole ? 0.75f : 0.45f) * fade * (0.4f + 0.6f * s);
                float rr = 1f, gg = 0.45f + 0.4f * fade, bb = 0.12f + 0.3f * fade;
                float[][] v = { { (float) Math.cos(a0) * r0, 0, (float) Math.sin(a0) * r0 },
                        { (float) Math.cos(a0) * r1, 0, (float) Math.sin(a0) * r1 },
                        { (float) Math.cos(a1) * r1, 0, (float) Math.sin(a1) * r1 },
                        { (float) Math.cos(a1) * r0, 0, (float) Math.sin(a1) * r0 } };
                for (int k : new int[] { 0, 1, 2, 0, 2, 3 })
                    buf.vertex(m, v[k][0], v[k][1], v[k][2]).color(rr, gg, bb, alpha).endVertex();
            }
        }
        Tesselator.getInstance().end();
    }

    private static VertexBuffer sphere() {
        if (sphere != null) return sphere;
        BufferBuilder builder = new BufferBuilder(64 * 64 * 6 * 20);
        builder.begin(VertexFormat.Mode.TRIANGLES, DefaultVertexFormat.POSITION_TEX);
        int n = 64;
        for (int i = 0; i < n; i++) {
            float v0 = (float) i / n, v1 = (float) (i + 1) / n;
            double p0 = Math.PI / 2 - i * Math.PI / n, p1 = Math.PI / 2 - (i + 1) * Math.PI / n;
            for (int j = 0; j < n; j++) {
                float u0 = 1f - (float) j / n, u1 = 1f - (float) (j + 1) / n;
                double t0 = j * 2 * Math.PI / n, t1 = (j + 1) * 2 * Math.PI / n;
                float[][] q = {
                        { (float) (Math.cos(p0) * Math.cos(t0)), (float) Math.sin(p0),
                                (float) (Math.cos(p0) * Math.sin(t0)), u0, v0 },
                        { (float) (Math.cos(p1) * Math.cos(t0)), (float) Math.sin(p1),
                                (float) (Math.cos(p1) * Math.sin(t0)), u0, v1 },
                        { (float) (Math.cos(p1) * Math.cos(t1)), (float) Math.sin(p1),
                                (float) (Math.cos(p1) * Math.sin(t1)), u1, v1 },
                        { (float) (Math.cos(p0) * Math.cos(t1)), (float) Math.sin(p0),
                                (float) (Math.cos(p0) * Math.sin(t1)), u1, v0 } };
                for (int k : new int[] { 0, 1, 2, 0, 2, 3 })
                    builder.vertex(q[k][0], q[k][1], q[k][2]).uv(q[k][3], q[k][4]).endVertex();
            }
        }
        sphere = new VertexBuffer(VertexBuffer.Usage.STATIC);
        sphere.bind();
        sphere.upload(builder.end());
        VertexBuffer.unbind();
        return sphere;
    }
}
