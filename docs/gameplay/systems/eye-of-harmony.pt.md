# Olho da Harmonia

![Olho da Harmonia](../../assets/machines/eye_of_harmony.webp){ loading=lazy }

O Olho da Harmonia simula um universo em miniatura e extrai os minérios de um planeta inteiro. Cada operação é cara, demorada e pode falhar; esta página mostra todas as contas que o controlador faz.

|  |  |
|---|---|
| **Tier** | UXV |
| **Energia** | sem fio (rede Nexus) |
| **Origem** | port do GT5-Unofficial a3e1e112 |

## Programas planetários

O item de planeta no slot do controlador escolhe o programa. Os produtos vêm dos veios de minério do GTCEu registrados naquela dimensão. Packs adicionam planetas pelo KubeJS (`GTNAStartupEvents.eyeOfHarmony`). Planetas além das dimensões do Minecraft precisam do Ad Astra.

$$
\begin{aligned}
\text{duração base} &= 18000\ \text{s} \cdot 1{,}4^{\text{tier}} \\
\text{gás de cada (H e He)} &= 10^{9} \cdot (\text{tier} + 1)\ \text{mB} \\
\text{chance base} &= 1 - 0{,}05 \cdot \text{tier} \\
\text{retorno} &= \text{custo} \cdot (0{,}6 + \text{tier}/10) \\
\text{custo} &= \text{plasmas} + \text{ticks} \cdot (2^{19} + 10^{11})\ \text{EU}
\end{aligned}
$$

| Planeta | Tier | Duração base | H e He (mB) | Chance base | Custo sem plasmas (EU) |
|---|---|---|---|---|---|
| Overworld, Nether, End | 0 | 5 h | 1e9 | 100% | 3,6e16 |
| Lua | 1 | 7 h | 2e9 | 95% | 5,04e16 |
| Marte | 2 | 9,80 h | 3e9 | 90% | 7,06e16 |
| Vênus, Mercúrio | 4 | 19,21 h | 5e9 | 80% | 1,38e17 |
| Glacio | 5 | 26,89 h | 6e9 | 75% | 1,94e17 |

## Campos e circuito

Três campos de tier 0 a 8 (compressão $c$, aceleração $a$, estabilização $s$) e um circuito $k$ de 0 a 24:

$$
\begin{aligned}
\text{duração} &= \max\!\left(T \cdot 2^{-a} \cdot 0{,}97^{\,c - r} \cdot 2^{-k},\ 1\right) && r = \text{compressão mínima do programa} \\
\text{custo de partida} &= \text{custo} \cdot 4^{k} \\
\text{retorno} &= \text{retorno base} \cdot \left(1 - (8 - s) \cdot 0{,}05\right) && \text{não sobe com o circuito} \\
\text{chance} &= \text{chance base} - 0{,}0925\,a + 0{,}05\,s - \text{penalidades de gás} \\
\text{rendimento} &= 1 - 0{,}05\,s - \text{penalidades de gás} \\
\text{penalidade de gás} &= 1 - \exp\!\left(-\left(30 \cdot \left(\tfrac{\text{guardado}}{\text{necessário}} - 1\right)\right)^{2}\right)
\end{aligned}
$$

| a / s | Chance (Overworld) | Rendimento | Tempo |
|---|---|---|---|
| 0 / 0 | 100% | 100% | ÷1 |
| 2 / 2 | 91,50% | 90% | ÷4 |
| 4 / 4 | 83% | 80% | ÷16 |
| 6 / 6 | 74,50% | 70% | ÷64 |
| 8 / 8 | 66% | 60% | ÷256 |
| 8 / 0 | 26% | 100% | ÷256 |
| 0 / 8 | 100% | 60% | ÷1 |

O gás em excesso também reduz chance e rendimento: guardar 10% a mais já custa 99,99% em cada gás. Entregue a quantidade exata.

## Falha e pity

- A falha também devolve o EU de retorno e gera SpaceTime: $\text{chance} \cdot 14400 \cdot 2^{\text{tier} + 1}$ mB.
- Falhas seguidas **nas mesmas condições** acumulam pity: soma $(1 - \text{chance}) \cdot \text{chance}$ a cada falha. Mudar campos ou circuito zera.
- O resultado é sorteado na partida e salvo: quebrar o controlador ou recarregar o mundo não muda o resultado.

## Dicas

- O controlador consome **todo** o hidrogênio e o hélio guardados na partida, inclusive o excesso.
- O retorno chega pela rede Nexus em parcelas; a perda da rede aparece separada na GUI.
- Saída cheia não perde nada: o ciclo espera.
