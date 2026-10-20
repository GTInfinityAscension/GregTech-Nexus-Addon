# Item effects

GTNA's endgame materials have animated icons: halos, glowing outlines and three shaders. GTNA draws them itself; RenderBlender is no longer needed (since 0.5.6).

| Effect | Look | Where |
|---|---|---|
| Halo | soft tinted disc behind the icon | inventories |
| Glow edge | tinted, slightly larger copy of the icon behind it | inventories |
| Cosmic | drifting star field inside the icon | item icon |
| Eternal | slow flowing light bands with sparkles | item icon |
| Unstable | flickering, crackling noise | item icon |

## Turning them down

In `config/gtna.yaml`, `client` section:

| Option | Default | Effect |
|---|---|---|
| `itemHalo` | `true` | draws halos |
| `itemGlowEdge` | `true` | draws glow edges |
| `itemShaderEffects` | `true` | draws the cosmic, eternal and unstable shaders |
| `itemEffectSpeed` | `100` | animation speed in percent, 0 to 400 (0 freezes it) |

## For pack and resource pack authors

**Item models:** five model loaders, `gtna:halo`, `gtna:glow_edge`, `gtna:cosmic`, `gtna:eternal` and `gtna:unstable`, add an effect to any item model.

**KubeJS** (`kubejs/client_scripts`, runs again on every F3+T):

```js
GTNAClientEvents.itemEffects(event => {
  // every form of a GTCEu material
  event.material('gtna:advanced_nitinol').halo(0xFF66CCFF, 8).pulse(true)
  // one item; replaces the effects of its model
  event.item('kubejs:my_core').cosmic().colors(0xFF050418, 0xFF7FD4FF).glowEdge(0xFFFFAA00, 1.5)
  event.item('gtceu:gtna_spacetime_ingot').eternal().mask('gtna:mask/cosmic').speed(0.5)
  event.item('gtceu:gtna_chaos_matter_dust').clear()
})
```

| Method | Meaning |
|---|---|
| `halo(argb, size)` | halo with a radius in item pixels |
| `glowEdge(argb)`, `glowEdge(argb, width)` | outline glow |
| `cosmic()`, `eternal()`, `unstable()` | shader effect |
| `color(argb)`, `colors(primary, secondary)` | tint; `0` keeps the default palette |
| `pulse(true)` | makes the halo pulse |
| `speed(x)` | animation speed multiplier |
| `mask(texture)`, `texture(texture)` | shader mask or halo texture; by default the item's own shape |
| `clear()` | removes every effect from the item |
