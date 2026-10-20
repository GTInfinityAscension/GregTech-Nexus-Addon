# Efeitos de item

Os materiais de fim de jogo do GTNA têm ícones animados: halos, contornos brilhantes e três shaders. O próprio GTNA desenha esses efeitos; o RenderBlender não é mais necessário (desde a 0.5.6).

| Efeito | Aparência | Onde |
|---|---|---|
| Halo | disco colorido e suave atrás do ícone | inventários |
| Borda brilhante | cópia colorida e um pouco maior do ícone, atrás dele | inventários |
| Cosmic | campo de estrelas em movimento dentro do ícone | ícone do item |
| Eternal | faixas de luz fluindo devagar, com brilhos | ícone do item |
| Unstable | ruído tremulante e crepitante | ícone do item |

## Diminuindo os efeitos

No `config/gtna.yaml`, seção `client`:

| Opção | Padrão | Efeito |
|---|---|---|
| `itemHalo` | `true` | desenha os halos |
| `itemGlowEdge` | `true` | desenha as bordas brilhantes |
| `itemShaderEffects` | `true` | desenha os shaders cosmic, eternal e unstable |
| `itemEffectSpeed` | `100` | velocidade da animação em porcentagem, de 0 a 400 (0 congela) |

## Para autores de pack e de resource pack

**Modelos de item:** cinco loaders de modelo, `gtna:halo`, `gtna:glow_edge`, `gtna:cosmic`, `gtna:eternal` e `gtna:unstable`, acrescentam um efeito a qualquer modelo de item.

**KubeJS** (`kubejs/client_scripts`, roda de novo a cada F3+T):

```js
GTNAClientEvents.itemEffects(event => {
  // todas as formas de um material do GTCEu
  event.material('gtna:advanced_nitinol').halo(0xFF66CCFF, 8).pulse(true)
  // um item; substitui os efeitos do modelo dele
  event.item('kubejs:my_core').cosmic().colors(0xFF050418, 0xFF7FD4FF).glowEdge(0xFFFFAA00, 1.5)
  event.item('gtceu:gtna_spacetime_ingot').eternal().mask('gtna:mask/cosmic').speed(0.5)
  event.item('gtceu:gtna_chaos_matter_dust').clear()
})
```

| Método | Significado |
|---|---|
| `halo(argb, tamanho)` | halo com raio em pixels do item |
| `glowEdge(argb)`, `glowEdge(argb, largura)` | contorno brilhante |
| `cosmic()`, `eternal()`, `unstable()` | efeito de shader |
| `color(argb)`, `colors(primária, secundária)` | cor; `0` mantém a paleta padrão |
| `pulse(true)` | faz o halo pulsar |
| `speed(x)` | multiplicador da velocidade da animação |
| `mask(textura)`, `texture(textura)` | máscara do shader ou textura do halo; por padrão, a forma do próprio item |
| `clear()` | tira todos os efeitos do item |
