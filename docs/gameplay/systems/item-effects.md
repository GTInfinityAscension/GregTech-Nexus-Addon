# Efeitos de item

## O que são

Halo, borda brilhante e os shaders cosmic, eternal e unstable nos ícones dos materiais do GTNA. São do próprio GTNA desde a 0.5.6; o RenderBlender não é mais necessário.

## Configuração

Em `config/gtna.json`, seção client: `itemHalo`, `itemGlowEdge`, `itemShaderEffects` e `itemEffectSpeed` (0–400%).

## KubeJS

Em `kubejs/client_scripts`: `GTNAClientEvents.itemEffects(event => { event.material('gtna:advanced_nitinol').halo(0xFF66CCFF, 8).pulse(true) })`. Veja a página da API KubeJS.
