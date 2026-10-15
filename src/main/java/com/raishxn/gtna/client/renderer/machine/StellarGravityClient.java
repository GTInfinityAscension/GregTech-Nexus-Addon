package com.raishxn.gtna.client.renderer.machine;

import net.minecraft.client.Minecraft;
import net.minecraft.world.phys.Vec3;
import net.minecraftforge.api.distmarker.Dist;
import net.minecraftforge.api.distmarker.OnlyIn;
import net.minecraftforge.event.TickEvent;

import com.raishxn.gtna.common.machine.multiblock.originals.StellarChamberMachine;

import java.util.Map;
import java.util.WeakHashMap;

/**
 * The Stellar Chamber's gravity on the local player. A player's movement runs on its own client, so velocity set by
 * the server is overwritten every tick; the same pull the server applies to other entities is applied here.
 */
@OnlyIn(Dist.CLIENT)
public final class StellarGravityClient {

    /** Chambers whose star the renderer saw running, so the tick needs no world search. */
    private static final Map<StellarChamberMachine, Boolean> STARS = new WeakHashMap<>();

    private StellarGravityClient() {}

    public static void seen(StellarChamberMachine machine) {
        STARS.put(machine, Boolean.TRUE);
    }

    public static void onClientTick(TickEvent.ClientTickEvent event) {
        var player = Minecraft.getInstance().player;
        if (event.phase != TickEvent.Phase.END || player == null || STARS.isEmpty() || player.isPassenger() ||
                player.getAbilities().flying)
            return;
        var it = STARS.keySet().iterator();
        while (it.hasNext()) {
            var m = it.next();
            if (m.isInValid() || m.getLevel() != player.level()) {
                it.remove();
                continue;
            }
            if (!m.isStarRunning()) continue;
            if (StellarChamberMachine.pull(player, Vec3.atCenterOf(m.center()), m.isBlackHole())) return;
        }
    }
}
