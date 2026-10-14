# Item effects

## What they are

Halo, glow edge and the cosmic, eternal and unstable shaders on GTNA material icons. They are GTNA's own since 0.5.6; RenderBlender is no longer needed.

## Configuration

In `config/gtna.json`, client section: `itemHalo`, `itemGlowEdge`, `itemShaderEffects` and `itemEffectSpeed` (0–400%).

## KubeJS

In `kubejs/client_scripts`: `GTNAClientEvents.itemEffects(event => { event.material('gtna:advanced_nitinol').halo(0xFF66CCFF, 8).pulse(true) })`. See the KubeJS API page.
