package com.raishxn.gtna.client.renderer.machine;

import com.gregtechceu.gtceu.client.renderer.machine.DynamicRender;
import com.gregtechceu.gtceu.client.renderer.machine.DynamicRenderManager;
import com.gregtechceu.gtceu.client.renderer.machine.DynamicRenderType;

import net.minecraft.client.renderer.LightTexture;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.client.renderer.RenderType;
import net.minecraft.client.renderer.texture.OverlayTexture;
import net.minecraft.core.BlockPos;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.Vec3;

import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.blaze3d.vertex.VertexConsumer;
import com.mojang.math.Axis;
import com.mojang.serialization.Codec;
import com.raishxn.gtna.GTNACORE;
import com.raishxn.gtna.common.machine.multiblock.part.bec.LineOfSightHatchPartMachine;
import org.joml.Matrix3f;
import org.joml.Matrix4f;

import java.awt.Color;

/**
 * GTNH {@code MTEHatchLoS.renderTESR}: a slowly rotating beacon-style prism between two paired Line-of-Sight
 * connectors, cycling hue, more opaque while the node is crafting.
 */
public class LineOfSightBeamRenderer extends DynamicRender<LineOfSightHatchPartMachine, LineOfSightBeamRenderer> {

    public static final Codec<LineOfSightBeamRenderer> CODEC = Codec.unit(LineOfSightBeamRenderer::new);
    public static final DynamicRenderType<LineOfSightHatchPartMachine, LineOfSightBeamRenderer> TYPE = DynamicRenderManager
            .register(GTNACORE.id("bec/line_of_sight"), new DynamicRenderType<>(CODEC));

    private static final ResourceLocation BEAM = new ResourceLocation("textures/entity/beacon_beam.png");

    @Override
    public DynamicRenderType<LineOfSightHatchPartMachine, LineOfSightBeamRenderer> getType() {
        return TYPE;
    }

    @Override
    public boolean shouldRender(LineOfSightHatchPartMachine machine, Vec3 cameraPos) {
        return machine.canRenderBeam();
    }

    @Override
    public void render(LineOfSightHatchPartMachine machine, float partialTicks, PoseStack poseStack,
                       MultiBufferSource buffer, int combinedLight, int combinedOverlay) {
        BlockPos target = machine.getConnection();
        if (target == null || machine.getLevel() == null) return;
        BlockPos pos = machine.getPos();
        double dx = target.getX() - pos.getX(), dy = target.getY() - pos.getY(), dz = target.getZ() - pos.getZ();
        float length = (float) Math.sqrt(dx * dx + dy * dy + dz * dz);
        if (length < 1e-3) return;
        poseStack.pushPose();
        poseStack.translate(0.5, 0.5, 0.5);
        // rotate +Y toward the paired hatch
        double nx = dx / length, ny = dy / length, nz = dz / length;
        double ax = nz, az = -nx;
        double sin = Math.sqrt(ax * ax + az * az);
        if (sin > 1e-6) {
            poseStack.mulPose(Axis.of(new org.joml.Vector3f((float) (ax / sin), 0, (float) (az / sin)))
                    .rotation((float) Math.atan2(sin, ny)));
        } else if (ny < 0) {
            poseStack.mulPose(Axis.XP.rotationDegrees(180));
        }
        float time = machine.getLevel().getGameTime() + partialTicks;
        float scroll = -time * 0.2f - (float) Math.floor(-time * 0.1f);
        float hue = ((System.currentTimeMillis() % 10_000) / 10_000f + (machine.getPos().hashCode() & 255) / 255f) %
                1f;
        int rgb = Color.HSBtoRGB(hue, 0.5f, 0.75f);
        int r = (rgb >> 16) & 0xff, g = (rgb >> 8) & 0xff, b = rgb & 0xff;
        boolean active = machine.isBeamActive();
        VertexConsumer vertices = buffer.getBuffer(RenderType.beaconBeam(BEAM, !active));
        PoseStack.Pose pose = poseStack.last();
        float rot = time * -0.0375f;
        float radius = 0.6f;
        float[] cx = new float[4], cz = new float[4];
        double[] angles = { 0.75, 0.25, 1.25, 1.75 };
        for (int i = 0; i < 4; i++) {
            cx[i] = (float) (Math.cos(rot + Math.PI * angles[i]) * radius);
            cz[i] = (float) (Math.sin(rot + Math.PI * angles[i]) * radius);
        }
        float vMin = -1 + scroll, vMax = length * (0.5f / radius) + vMin;
        int alpha = active ? 96 : 32;
        quad(vertices, pose, cx[0], cz[0], cx[1], cz[1], length, vMin, vMax, r, g, b, alpha);
        quad(vertices, pose, cx[3], cz[3], cx[2], cz[2], length, vMin, vMax, r, g, b, alpha);
        quad(vertices, pose, cx[1], cz[1], cx[3], cz[3], length, vMin, vMax, r, g, b, alpha);
        quad(vertices, pose, cx[2], cz[2], cx[0], cz[0], length, vMin, vMax, r, g, b, alpha);
        poseStack.popPose();
    }

    private static void quad(VertexConsumer v, PoseStack.Pose pose, float x1, float z1, float x2, float z2,
                             float length, float vMin, float vMax, int r, int g, int b, int a) {
        Matrix4f m = pose.pose();
        Matrix3f n = pose.normal();
        vertex(v, m, n, x1, 0, z1, 1, vMax, r, g, b, a);
        vertex(v, m, n, x1, length, z1, 1, vMin, r, g, b, a);
        vertex(v, m, n, x2, length, z2, 0, vMin, r, g, b, a);
        vertex(v, m, n, x2, 0, z2, 0, vMax, r, g, b, a);
    }

    private static void vertex(VertexConsumer v, Matrix4f m, Matrix3f n, float x, float y, float z, float u, float vv,
                               int r, int g, int b, int a) {
        v.vertex(m, x, y, z).color(r, g, b, a).uv(u, vv).overlayCoords(OverlayTexture.NO_OVERLAY)
                .uv2(LightTexture.FULL_BRIGHT).normal(n, 0, 1, 0).endVertex();
    }

    @Override
    public boolean shouldRenderOffScreen(LineOfSightHatchPartMachine machine) {
        return true;
    }

    @Override
    public int getViewDistance() {
        return 256;
    }

    @Override
    public AABB getRenderBoundingBox(LineOfSightHatchPartMachine machine) {
        BlockPos target = machine.getConnection();
        AABB box = new AABB(machine.getPos());
        return target == null ? box : box.minmax(new AABB(target)).inflate(1);
    }
}
