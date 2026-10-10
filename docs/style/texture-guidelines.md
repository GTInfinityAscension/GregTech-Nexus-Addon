# GTNA Texture Design System & Pixel Art Guidelines

Este documento estabelece o padrão visual e técnico para todas as texturas de blocos, itens e materiais no **GregTech Nexus Addon (GTNA)**, alinhado à estética premium do **Modernity-GTNH** e da API do **GTCEu 7.5.3 (1.20.1)**.

---

## 1. Princípios Fundamentais

Uma textura de alto nível no Minecraft técnico deve ser **instantaneamente legível** no inventário/JEI (16×16 px) e **visualmente rica e coerente** quando colocada no mundo ou inspecionada de perto.

### O que NÃO fazer (Armadilhas comuns):
- ❌ **Fórmulas Matemáticas Contínuas Cruas**: Gradientes puramente senoidais ou radiais em scripts NumPy sem quantização parecem filtros de Photoshop dos anos 90 ou plástico borrado.
- ❌ **Monocromia / Rampas Lineares**: Escurecer ou clarear um material apenas multiplicando por cinza deixa o item "morto", com aparência de argila ou ferrugem seca (ex: o erro do Mellion inicial).
- ❌ **Pillow Shading**: Escurecer as 4 bordas e clarear o centro sem direção de luz definida.
- ❌ **Ruído Difuso (Noise / TV fora do ar)**: Adicionar ruído pixel-a-pixel aleatório destrói a forma e causa poluição visual.
- ❌ **Importação Cega de Assets com Shaders**: No GTNH 1.7.10, vários materiais cósmicos (ex: Universium) dependiam de shaders GLSL em tempo real onde a textura base era apenas uma máscara preta com alpha 1–8. No GTNA (1.20.1), esses materiais devem ser **recriados como pixel art nativo de alta fidelidade**.

---

## 2. As 5 Leis de Ouro do Pixel Art GTNA

### Lei 1: Hue-Shifting Obrigatório
Nenhum material do GTNA pode ter rampa de iluminação com matiz constante.
- **Sombras**: Devem puxar para comprimentos de onda mais frios ou profundos (azul-marinho, violeta cósmico, índigo, carvão azulado).
- **Meio-Tom**: A cor de identidade pura e saturada do material.
- **Highlights**: Devem puxar para tons mais quentes, energéticos ou especulares (ciano, ouro incandescente, branco perolado, platina).

### Lei 2: Estrutura em "Clusters" (Anti-Noise)
- Pixels devem ser agrupados em blocos intencionais (*clusters* de 2×1, 2×2, 3×2).
- Transições de relevo, reflexos e facetas de cristal devem ter arestas limpas.
- Animações procedurais (pulsos, chamas, vórtices) devem propagar ondas através de clusters estruturados, e não como ruído estático independente por pixel.

### Lei 3: Iluminação Noroeste (Top-Left Keylight) e Sel-Out
- A luz padrão do Minecraft vem do canto superior esquerdo (Noroeste: $x = -1, y = -1, z = 1$).
- Arestas superiores e esquerdas recebem chanfro iluminado (*specular highlight*).
- Arestas inferiores e direitas recebem sombreamento profundo e **Selective Outlining (Sel-out)** — contornos escuros adaptados que destacam a silhueta da peça contra qualquer fundo de interface (cinza do JEI, preto do terminal ME ou azul do céu).

### Lei 4: Contraste e Dynamic Range Mínimo
- Para garantir legibilidade em escala 1:1, a amplitude de luminância entre a sombra mais escura e o highlight mais claro deve ter $\Delta L \ge 160$ (em escala de 0 a 255), salvo exceções de materiais propositalmente monocromáticos e sombrios (como Void Matter).

### Lei 5: Resolução e Paridade de Família
- **Itens e Materiais Gerais**: 16×16 nativo (com strips verticais de $16 \times 480$ para 30 frames de animação quando aplicável).
- **Componentes Ópticos / Hiperdensos (Lentes, Nanites, Fórmulas Especiais)**: 32×32 ou 64×64 apenas sob aprovação explícita e com silhueta bem demarcada.
- **Consistência de Família**: Ao criar uma nova liga/material, as variações de lingote (Shiny/Ultimet vs Dull/Battery Alloy vs Standard) devem respeitar a densidade atômica da liga.

---

## 3. Protocolo de Criação: Showcase & Feedback

Antes de aplicar qualquer textura definitivamente ao código:
1. **Geração de Candidatos**: Criar de 2 a 4 variações conceituais com paletas e animações distintas.
2. **Showcase Interativo**: Gerar página HTML / Widget de visualização contendo:
   - Zoom escalonado (1×, 4×, 8×, 16× com renderização `image-rendering: pixelated`).
   - Mockup do slot de inventário do Minecraft (JEI GUI box).
   - Animação em tempo real com controle de velocidade / pause.
   - Dados técnicos da paleta (hexadecimal, contraste, curva de luminância).
   - Comparação lado a lado com a versão antiga/baseline.
3. **Revisão e Aprovação**: O autor seleciona a variação preferida ou solicita calibragens específicas.
4. **Deploy e Gate**: Exportação para o material set completo (`ingot`, `plate`, `gear`, `rod`, `block`, etc.), inclusão do `.mcmeta` apropriado e execução do gate de validação Gradle.
