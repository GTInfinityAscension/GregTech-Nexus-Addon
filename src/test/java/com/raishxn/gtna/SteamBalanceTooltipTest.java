package com.raishxn.gtna;

import com.raishxn.gtna.api.steam.GTNASteamBalance;

import java.util.List;

/** Steam tooltips show the parallels and speed that the steam balance really applies. */
public final class SteamBalanceTooltipTest {

    private SteamBalanceTooltipTest() {}

    public static void main(String[] args) {
        try {
            check("§b▸ Parallel: up to §e64§b", true, "§b▸ Parallel: up to §e64§b", "no provider changes nothing");

            var journey = new GTNASteamBalance.Variant("Journey", 1.5, 0.75);
            GTNASteamBalance.setProvider(() -> journey);
            check("§b▸ Parallel: up to §e64§b", true, "§b▸ Parallel: up to §e96 §7(Journey)§b", "parallels scale");
            check("§a▸ §e2x§a speed vs. singleblock", false, "§a▸ §e2.67x §7(Journey)§a speed vs. singleblock",
                    "speed is base / duration multiplier");
            check("§b▸ Parallel: §e16§b default, adjustable up to §e16§b", true,
                    "§b▸ Parallel: §e24 §7(Journey)§b default, adjustable up to §e24 §7(Journey)§b",
                    "every number in a parallel line scales");

            var normal = new GTNASteamBalance.Variant("Normal", 1.0, 1.0);
            GTNASteamBalance.setProvider(new GTNASteamBalance.Provider() {

                public GTNASteamBalance.Variant active() {
                    return normal;
                }

                public List<GTNASteamBalance.Variant> tooltipVariants() {
                    return List.of(normal, journey);
                }
            });
            check("§b▸ Parallel: up to §e128§b", true,
                    "§b▸ Parallel: up to §e128 §7(Normal)§7 / §e192 §7(Journey)§b", "menu lists both presets");
            if (GTNASteamBalance.parallels(128) != 128) throw new AssertionError("active variant drives recipes");
        } finally {
            GTNASteamBalance.setProvider(null);
        }
    }

    private static void check(String in, boolean parallel, String expected, String message) {
        String actual = GTNASteamBalance.scaleTooltipNumbers(in, parallel);
        if (!actual.equals(expected)) {
            throw new AssertionError(message + ": expected [" + expected + "] got [" + actual + "]");
        }
    }
}
