package com.raishxn.gtna.api.steam;

import java.util.List;
import java.util.Locale;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Pack-level balance for GTNA steam multiblocks. Every steam machine applies {@link #parallels(int)} to its parallel
 * limit and {@link #duration(double)} to its duration multiplier, so a modpack can rebalance the whole steam age
 * from one place (and per world, if its provider changes with the loaded world). Without a provider nothing changes.
 */
public final class GTNASteamBalance {

    /** One set of multipliers, with an optional label shown in tooltips (e.g. a difficulty name). */
    public record Variant(String label, double parallelMultiplier, double durationMultiplier) {

        public int parallels(int base) {
            return Math.max(1, (int) Math.round(base * parallelMultiplier));
        }

        public double duration(double base) {
            return base * durationMultiplier;
        }
    }

    public interface Provider {

        /** The multipliers in effect now (for the loaded world). */
        Variant active();

        /** Variants a tooltip should list when no world decides yet (e.g. in the main menu); never empty. */
        default List<Variant> tooltipVariants() {
            return List.of(active());
        }
    }

    private static final Variant NEUTRAL = new Variant(null, 1.0, 1.0);
    private static volatile Provider provider = () -> NEUTRAL;

    private GTNASteamBalance() {}

    public static void setProvider(Provider newProvider) {
        provider = newProvider == null ? () -> NEUTRAL : newProvider;
    }

    public static Provider provider() {
        return provider;
    }

    /** Whether a pack changed anything (otherwise tooltips keep their plain translated lines). */
    public static boolean isActive() {
        var variants = provider.tooltipVariants();
        return variants.size() > 1 || variants.get(0).label() != null ||
                variants.get(0).parallelMultiplier() != 1.0 || variants.get(0).durationMultiplier() != 1.0;
    }

    /** Parallel limit after the pack's multiplier (at least 1). */
    public static int parallels(int base) {
        return provider.active().parallels(base);
    }

    /** Duration multiplier after the pack's multiplier. */
    public static double duration(double base) {
        return provider.active().duration(base);
    }

    private static final Pattern NUMBER = Pattern.compile("§e(~?)([0-9][0-9,.]*)(x?)");

    /**
     * Rewrites the highlighted numbers of a parallel or speed line with the steam balance in effect. With several
     * variants (no world loaded yet) every value is listed with its label.
     */
    public static String scaleTooltipNumbers(String text, boolean parallel) {
        List<Variant> variants = provider.tooltipVariants();
        Matcher m = NUMBER.matcher(text);
        StringBuilder out = new StringBuilder();
        while (m.find()) {
            double base;
            try {
                base = Double.parseDouble(m.group(2).replace(",", ""));
            } catch (NumberFormatException e) {
                m.appendReplacement(out, Matcher.quoteReplacement(m.group()));
                continue;
            }
            StringBuilder values = new StringBuilder();
            for (int v = 0; v < variants.size(); v++) {
                var variant = variants.get(v);
                String value = parallel ? String.format(Locale.ROOT, "%,d", variant.parallels((int) base)) :
                        trim(base / variant.durationMultiplier());
                if (v > 0) values.append("§7 / ");
                values.append("§e").append(m.group(1)).append(value).append(m.group(3));
                if (variant.label() != null) values.append(" §7(").append(variant.label()).append(")");
            }
            m.appendReplacement(out, Matcher.quoteReplacement(values.toString()));
        }
        m.appendTail(out);
        return out.toString();
    }

    private static String trim(double value) {
        return value == Math.rint(value) ? String.valueOf((long) value) :
                String.format(Locale.ROOT, "%.2f", value).replaceAll("0+$", "");
    }
}
