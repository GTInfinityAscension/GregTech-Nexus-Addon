// GTNA item icon effects. Client script; reloads with F3+T.
// Effects: halo(argb, size), glowEdge(argb[, width]), cosmic(), eternal(), unstable().
// Modifiers act on the last effect added: colors(a, b), color(argb), pulse(bool), speed(x), mask(texture), texture(texture).

GTNAClientEvents.itemEffects(event => {
    // Every form (ingot, plate, dust...) of a GTCEu material
    event.material('gtna:advanced_nitinol').halo(0xFF66CCFF, 8).pulse(true)

    // One item; replaces the effects of its model
    event.item('minecraft:nether_star').cosmic().colors(0xFF050418, 0xFF7FD4FF).glowEdge(0xFFFFAA00, 1.5)

    // Shader effect limited to a mask texture from the block atlas
    event.item('minecraft:amethyst_shard').eternal().mask('gtna:mask/cosmic').speed(0.5)

    // Remove the effects a model declares
    // event.item('gtceu:gtna_chaos_matter_dust').clear()
})
