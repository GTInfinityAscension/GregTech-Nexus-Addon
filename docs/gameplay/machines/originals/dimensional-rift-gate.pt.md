# Portão de Fenda Dimensional

![Portão de Fenda Dimensional](../../../assets/machines/dimensional_rift_gate.webp){ loading=lazy }

Abre uma fenda para uma dimensão sorteada por seed e extrai recursos dela. Ajuste frequência, fase e amplitude em direção ao ótimo escondido da seed para aumentar a ressonância.

|  |  |
|---|---|
| **Tier** | UIV |
| **Tamanho** | 126 × 126 × 54 |
| **Energia** | $2^{36}$ EU/t da rede Nexus do dono com a fenda aberta |
| **Fluido** | SpaceTime (estabilidade) |
| **Controlador** | Linha de Montagem (UIV), pesquisa no Gerador de Campo UIV |
| **Blocos** | [página do catálogo](../catalog/dimensional_rift_gate.md) |

## Estrutura e hatches

| Hatch | Máx. | Uso |
|---|---|---|
| Hatch de Entrada | 4 | SpaceTime |
| Barramento de Entrada | 4 | Sondas de Fenda, Âncoras de Profundidade, X-Nexus contido |
| Barramento de Saída | 4 | pós do bioma, Singularidade de Fenda |
| Hatch de Sintonia da Fenda | 1 | redstone 0–15 define a amplitude em 0–100% |

## Sintonia

Clique em Abrir para uma fenda com seed aleatória. Sintonize com [--] [-] [+] [++] (±10 / ±1). Cada Rift Probe consumida estreita as tolerâncias em 20%.

$$
\begin{aligned}
R &= \exp\!\left(-\left(\frac{f - f^{*}}{\sigma_f}\right)^{2} - \left(\frac{\Delta\varphi}{\sigma_\varphi}\right)^{2} - \left(\frac{A - A^{*}}{\sigma_A}\right)^{2}\right) \\
\sigma_f &= 260\ \text{THz} \cdot 0{,}8^{n} \qquad \sigma_\varphi = 100^\circ \cdot 0{,}8^{n} \qquad \sigma_A = 45\,\% \cdot 0{,}8^{n}
\end{aligned}
$$

$f$ vai de 1 a 1000 THz, $\varphi$ de 0 a 360° e $A$ de 0 a 100%; $(f^*, \varphi^*, A^*)$ é o ótimo escondido da semente e $n$ o número de sondas gastas nela. Cada botão mostra uma barra de quente/frio do próprio eixo.

| Sondas | $\sigma_f$ (THz) | $\sigma_\varphi$ (°) | $\sigma_A$ (%) | Janela para R ≥ 0,9 em f |
|---|---|---|---|---|
| 0 | 260 | 100 | 45 | ±84,39 THz |
| 2 | 166,4 | 64 | 28,8 | ±54,01 THz |
| 4 | 106,5 | 40,96 | 18,43 | ±34,57 THz |
| 6 | 68,16 | 26,21 | 11,8 | ±22,12 THz |
| 8 | 43,62 | 16,78 | 7,55 | ±14,16 THz |
| 10 | 27,92 | 10,74 | 4,83 | ±9,06 THz |

## Energia e estabilidade

Campo = 2^36 EU/t da rede Nexus enquanto aberta; sem isso a fenda colapsa

O fluido SpaceTime mantém a estabilidade: cada litro soma 2. As perdas crescem com ressonância baixa e com a profundidade.

$$
\begin{aligned}
\frac{dS}{dt} &= 2\,\dot V - \lambda\,(1 - R)\left(1 + \frac{D}{10}\right) - 0{,}4\,(8 - P) \\
\lambda &= 1{,}5\,(1{,}3 - C) \\
\dot V_{\text{SpaceTime}} &= 16 \cdot \frac{\lambda\,(1 - R)\,(1 + D/10) + 0{,}4\,(8 - P)}{2}\ \text{L/s}
\end{aligned}
$$

$S$ é a estabilidade (0–100), $D$ a profundidade, $P$ os pilones ativos (4 na estrutura atual) e $C$ a consonância do acorde (próxima seção). A máquina drena por segundo SpaceTime para a manutenção mais uma unidade; cada litro de SpaceTime vale 1/16 de unidade de estabilidade.

| R | D | SpaceTime (L/s), sem acorde, 4 pilones |
|---|---|---|
| 0,5 | 1 | 19,4 |
| 0,9 | 1 | 14,12 |
| 0,9 | 5 | 14,6 |
| 0,98 | 5 | 13,16 |
| 0,98 | 8 | 13,23 |
| 1 | 8 | 12,8 |

## Harmônicos

Manter R ≥ 0,9 por 30 s grava o harmônico da seed. Clique nos harmônicos gravados para carregar até 5 no acorde: acordes consonantes (oitava, quinta) são estáveis; dissonantes (trítono, segunda menor) cavam mais fundo mas gastam mais SpaceTime.

Manter R ≥ 0,98 por um minuto pode dar uma Rift Singularity. Estabilidade 0 colapsa a fenda; R abaixo de 0,2 por 10 s a inverte (−10 de estabilidade). Abas laterais: Sismógrafo e Atlas.

$$
\begin{aligned}
\text{c}(p\!:\!q) &= \frac{1}{\log_2 (p\,q)} \qquad C = \overline{\text{c}} \ (\text{média do acorde; 0,3 sem acorde}) \\
D_{\max} &= \left\lfloor 5 \cdot \max\!\left(0{,}5,\ 1 + 3\,(0{,}3 - C)\right) \right\rfloor
\end{aligned}
$$

| Intervalo | Razão | Consonância | Fator de λ (sozinho) | Profundidade máx. (sozinho) | Gravado em |
|---|---|---|---|---|---|
| Oitava | 2:1 | 1 | 0,3 | 2 | nenhum bioma dá |
| Quinta | 3:2 | 0,39 | 0,91 | 3 | Planície cristalina |
| Quarta | 4:3 | 0,28 | 1,02 | 5 | Floresta de esporos |
| Terça maior | 5:4 | 0,23 | 1,07 | 6 | Oceano de mercúrio |
| Sexta menor | 8:5 | 0,19 | 1,11 | 6 | Mundo-forja |
| Sétima menor | 9:5 | 0,18 | 1,12 | 6 | Relíquia de civilização |
| Trítono | 45:32 | 0,1 | 1,2 | 8 | Abismo de antimatéria |
| Segunda menor | 16:15 | 0,13 | 1,17 | 7 | Vazio |

## Endgame

Cada bioma solta pós dos seus materiais nos barramentos de saída. Taxa de **cada** material:

$$
\text{pós/s} = 16 \cdot R^{2} \cdot D^{1{,}5} \cdot \frac{S}{100}
$$

| Bioma | Chance | Prof. mínima | Pós |
|---|---|---|---|
| Planície cristalina | 30% | — | **Prismatium**, Quartzo Certus, Silício, Titânio |
| Oceano de mercúrio | 20% | — | **Cronomercúrio**, Ouro, Tálio, Cinábrio |
| Mundo-forja | 15% | — | **Forjacor**, Tungstênio, Ósmio, Irídio |
| Floresta de esporos | 15% | — | **Vivisporo**, Madeira, Carbono, Fósforo |
| Abismo de antimatéria | 8% | — | **Antimatéria Abissal**, Naquadah, Naquadah Enriquecida |
| Relíquia de civilização | 7% | 20 | **Resíduo Precursor**, Naquádria, Trínio, Durânio |
| Vazio | 5% | 40 | **Cinza do Vazio**, Neutrônio, Espaço-Tempo |

Exclusivo: um material por bioma (Prismatium, Cronomercúrio, Forjacor, Vivisporo, Antimatéria Abissal, Resíduo Precursor, Cinza do Vazio). A Singularidade vai para o controlador do Forge of Gods e os campos Advanced+ do Eye of Harmony.

Precisa de: a partir da profundidade 40, cada Âncora de Profundidade também consome um X-Nexus Contido; sem ele a âncora fica no barramento.

O X-Nexus vem do Anel Colisor de Antimatéria; a Câmara Estelar precisa do seu Forjacor para segurar um magnetar.

!!! bug "Problemas conhecidos"

    - A profundidade máxima começa em 5 e ainda nada a aumenta; o acorde mais dissonante chega a 8. Por isso Relíquia de Civilização (profundidade 20) e Vazio (40) não rendem nada, e **Resíduo Precursor** e **Cinza do Vazio** não podem ser obtidos nesta versão.
    - Os núcleos de pilone ainda não existem: a estrutura sempre conta 4 pilones ativos.

    Outros problemas: [issue tracker](https://github.com/GTInfinityAscension/GregTech-Nexus-Addon/issues).

