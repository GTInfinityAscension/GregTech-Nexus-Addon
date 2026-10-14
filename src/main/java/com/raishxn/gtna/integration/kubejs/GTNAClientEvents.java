package com.raishxn.gtna.integration.kubejs;

import com.raishxn.gtna.api.render.ItemEffectOverrides;
import dev.latvian.mods.kubejs.event.EventGroup;
import dev.latvian.mods.kubejs.event.EventHandler;

/**
 * KubeJS client events exposed by GTNA. Put these in {@code kubejs/client_scripts}; they run again on every
 * resource reload (F3+T).
 *
 * <pre>{@code
 * GTNAClientEvents.itemEffects(event => {
 *     // every form of a GTCEu material
 *     event.material('gtna:advanced_nitinol').halo(0xFF66CCFF, 8).pulse(true)
 *     // one item; replaces the effects of its model
 *     event.item('kubejs:my_core').cosmic().colors(0xFF050418, 0xFF7FD4FF).glowEdge(0xFFFFAA00, 1.5)
 *     event.item('gtceu:gtna_spacetime_ingot').eternal().mask('gtna:mask/cosmic').speed(0.5)
 *     event.item('gtceu:gtna_chaos_matter_dust').clear()
 * })
 * }</pre>
 */
public interface GTNAClientEvents {

    EventGroup GROUP = EventGroup.of("GTNAClientEvents");

    /** Add, replace or remove item icon effects (halo, glow edge, cosmic, eternal, unstable). */
    EventHandler ITEM_EFFECTS = GROUP.client("itemEffects", () -> ItemEffectsEventJS.class);

    /** Called by the client after every model bake, only when KubeJS is loaded. */
    static void postItemEffects() {
        ItemEffectOverrides.clear();
        ITEM_EFFECTS.post(new ItemEffectsEventJS());
    }
}
