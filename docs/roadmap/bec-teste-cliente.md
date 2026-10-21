# Roteiro de teste no cliente: BEC (G-0257)

Mundo criativo novo, com cheats. Para cada passo, anote **OK**, **erro** (o que aconteceu) ou **feio** (funciona,
mas o visual ou o texto está ruim). Use `/gamemode creative`.

## 0. Itens

```
/give @p gtna:bec_generator
/give @p gtna:bec_storage 2
/give @p gtna:bec_diode
/give @p gtna:bec_assembler
/give @p gtna:bec_io_node 2
/give @p gtna:bec_hatch 16
/give @p gtna:bec_conduit 128
/give @p gtna:bec_conduit_casing 16
/give @p gtna:nanite_containment_bus 4
/give @p gtna:line_of_sight_connector_hatch 4
/give @p gtna:nanite_detector_hatch
/give @p gtna:condensate_detector_hatch
/give @p gtna:io_node_controller_hatch
/give @p gtna:carbon_nanites 64
/give @p gtna:transcendent_metal_nanites 64
```

Hatches de energia: use os do GTCEu de tier alto (UIV ou mais). Também servem os Debug Energy Hatches do GTNA, se
existirem no seu mundo de teste.

## 1. Visual e textos (sem montar nada)

1. No EMI, procure "Bose-Einstein": aparecem os 5 controladores, os 6 hatches, o cano, a carcaça do cano e as
   8 carcaças (Coherence-Preserving..., Electromagnetically-Isolated..., Fine-Structure..., Conflict, Peace,
   Transformative Coil, Guidance Coil, Electromagnetic Waveguide).
2. Texturas: carcaças (a Conduit e a Transformative Coil são animadas), os 28 metamateriais, o Transdimensional
   Alignment Matrix e os 19 fluidos "Entangled ... Condensate" (sem textura roxa/preta).
3. Tooltips dos 5 controladores: tipo, frase, prós, números e contras; repetir em **pt_br** e **zh_cn**.
4. Tooltips dos 6 hatches.
5. EMI, categoria "Condensate Entanglement": 19 receitas (fluido → condensado).
6. EMI, categoria "Condensate Assembly": as receitas mostram os condensados como fluidos de entrada e uma linha
   "Nanite tier per item slot: ...". Confira o Singularity Shielding Casing, o Astral Array Fabricator e um
   metamaterial.
7. Preview da estrutura no EMI (multiblock preview) dos 5: o Observation Array é enorme (61 blocos); veja se
   o preview abre sem travar.

## 2. Cano (Conduit)

1. Coloque uma linha de canos: os braços conectam entre si.
2. Clique com corante num cano: ele muda de cor e **desconecta** dos vizinhos de outra cor.
3. Shift + clique com a mão vazia: tira a cor.
4. Coloque um BEC Hatch com a frente virada para o cano: o cano conecta nele; virado para outro lado, não.
5. Carcaça do cano: bloco cheio, sem braços.

## 3. Montagem

Para cada multibloco, use o preview do EMI (ou o botão de checar estrutura do GTNA) e monte. Anote se formou e o
que a mensagem de erro diz quando não formou.

| Máquina | Hatches que devem caber |
|---|---|
| Entanglement Apparatus | energia, fluid input, item input nas Isolated em volta do controlador; 1 BEC Hatch atrás (Fine-Structure) |
| Containment Field | energia e Condensate Detector nas Isolated; até 4 BEC Hatches nos centros laterais |
| Maxwell Gate | energia e fluid input nas Isolated; BEC Hatch de **entrada** à esquerda e de **saída** à direita |
| Observation Array | energia e Nanite Containment Bus nas Isolated; até 2 BEC Hatches; Line-of-Sight nos anéis |
| Teleportation Node | input/output bus, Nanite Detector e Controller nas Isolated; 1 Line-of-Sight atrás |

## 4. Fluxo completo

Ligue com canos: Entanglement Apparatus → Containment Field → Observation Array.

1. **Containment Field**: abra a tela e, nos parâmetros, coloque field strength = 1000000. O painel mostra a força do
   campo e "Stored: 0 mB". Confira o consumo (1 EU/t por ponto de força).
2. **Entanglement Apparatus**: ponha Infinity fundido num fluid input hatch. Ele roda e, no fim do ciclo, o Field
   mostra "Entangled Infinity" armazenado. Teste dois fluidos ao mesmo tempo.
3. **Observation Array**: ponha Carbon Nanites num Nanite Containment Bus (o slot de cima recebe; o de baixo devolve;
   o texto mostra a quantidade). O painel do Array mostra "Providing Nanites: Carbon ... x N" e a lista de condensado
   disponível.
4. **Teleportation Node**: coloque o Line-of-Sight dele de frente para um Line-of-Sight do Array, com só ar ou vidro
   entre eles (até 128 blocos). Aparece o **feixe** colorido; ele fica mais forte enquanto o nó fabrica.
5. Ponha no input bus do Node os itens de uma receita barata do EMI (por exemplo um metamaterial T1) e garanta os
   condensados no Field. No painel do Node, confira:
   - Status: Crafting
   - Required Nanite / Next Nanite / progresso
   - Required Condensate com "consumido / total"
6. Teste os erros:
   - Tire os nanites → "Insufficient Nanite Tier".
   - Desligue a energia do Array → "Unpowered" ou a receita falha.
   - Quebre o feixe com um bloco opaco → "Observation Array Offline".
   - Ponha 4+ condensados diferentes não pedidos no Field → a receita falha ("more than 3").
7. **Parâmetros do Node**: min parallel alto demais → "Insufficient Parallels"; max parallel e speed divisor mudam a
   velocidade.
8. **Maxwell Gate**: ponha-o entre o Field e o Array. Ligado, o Array vê o condensado só pelo lado de entrada para o
   de saída. Filtro com um condensado → só esse passa. Desligado (soft mallet), o Array não vê nada. Fluido num input
   hatch do Gate vira filtro automático.
9. Containment Field: desligue a energia → o conteúdo some (comportamento do GTNH).

## 5. Hatches de redstone

1. **Condensate Detector** (no Field): filtro vazio soma tudo; escolha um condensado, operação e limite; confira a
   leitura "Current" e uma lâmpada de redstone acendendo.
2. **Nanite Detector** (no Node): limite de tier e modo analógico (sinal = tier pedido).
3. **Controller** (no Node): sinal de redstone pausa ("Paused (Immediate)" ou "Paused (Step)", conforme o botão).

## 6. Persistência

Saia e volte ao mundo com o Node no meio de uma receita e o Field cheio: o progresso, o condensado guardado, os
filtros e os parâmetros continuam iguais.

## Como reportar

Mande a lista com o número do passo e OK/erro/feio. Para erro, mande print ou o trecho do `latest.log`.
