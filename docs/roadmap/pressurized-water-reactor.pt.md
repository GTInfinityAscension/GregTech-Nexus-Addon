# Reator de Água Pressurizada (planejado)

!!! info "Ainda não está no jogo"
    O design está aprovado; o código ainda não começou. Os números abaixo são as metas do design e podem mudar no balanço.

Um reator de fissão para a era **IV**, com a física de um PWR real em escala de tempo e de potência de jogo. Ele produz **vapor de alta pressão**; turbinas separadas convertem em EU. Difícil de projetar, fácil de operar: tudo o que exige atenção contínua tem um modo automático configurado uma vez (setpoint de potência, programa de boro, campanha de recarga).

| | |
|---|---|
| **Tier** | IV (todos os blocos e peças da era IV: aço de tungstênio, Inconel 625, Hastelloy-N, carbeto de boro, PBI) |
| **Potência nominal** | 131.072 EU/t térmicos (16 A IV), 262.144 L/t de vapor |
| **Estrutura** | contenção de cerca de 47 × 48 × 47 e torre de resfriamento de 66 blocos |
| **Núcleo** | 37 canais de combustível, 5 bancos de barras de controle, 4 geradores de vapor, 4 bombas do primário, pressurizador |

## Combustível

Cada canal recebe um **conjunto combustível** com enriquecimento $e$ (%) e queima $B$ (GWd/t):

$$
\begin{aligned}
k_\infty(e, B) &= k_0(e) - 0{,}006\,B, \qquad k_0(e) = 0{,}92 + 0{,}075\,e \\
k_{\text{núcleo}} &= 0{,}97 \cdot \overline{k_\infty} \quad \text{(fuga de nêutrons)}
\end{aligned}
$$

| Conjunto | $e$ (%) | $k_0$ | Queima máxima (GWd/t) |
|---|---|---|---|
| LEU-3 | 3 | 1,15 | 19 |
| LEU-4 | 4 | 1,22 | 31,5 |
| LEU-4,5 | 4,5 | 1,26 | 37,8 |
| LEU-5 | 5 | 1,29 | 44 |

Conjuntos com gadolínia (absorvedor queimável) e, no LuV, MOX com o plutônio reciclado pelo PUREX.

## Reatividade

$$
\begin{aligned}
\rho &= \frac{k - 1}{k} \quad (1\ \text{pcm} = 10^{-5}) \\
\rho_{\text{total}} &= \rho_{\text{comb}} + \rho_{\text{barras}} + \rho_{\text{boro}} + \rho_{\text{Doppler}} + \rho_{\text{mod}} + \rho_{\text{Xe}} + \rho_{\text{Sm}} \\
\rho_{\text{barras}} &= -8000\ \text{pcm} \cdot \left(x - \frac{\sin 2\pi x}{2\pi}\right) \\
\rho_{\text{boro}} &= -10\ \text{pcm/ppm} \cdot C_B \\
\rho_{\text{Doppler}} &= -2{,}5\ \text{pcm/K} \cdot (T_{\text{comb}} - 565\ \text{K}), \qquad \rho_{\text{mod}} = -40\ \text{pcm/K} \cdot (T_{\text{mod}} - 565\ \text{K})
\end{aligned}
$$

Os dois coeficientes de temperatura são negativos: o reator se autorregula. As barras valem pouco nas pontas e muito no meio (a curva S real).

## Cinética

Cinética pontual com um grupo de nêutrons atrasados: $\beta = 650$ pcm, $\Lambda = 2 \times 10^{-5}$ s, $\lambda = 0{,}08\ \text{s}^{-1}$.

$$
\frac{dn}{dt} = \frac{\rho - \beta}{\Lambda}\,n + \lambda C, \qquad \frac{dC}{dt} = \frac{\beta}{\Lambda}\,n - \lambda C, \qquad \tau \approx \frac{\beta - \rho}{\lambda\,\rho}
$$

Acima de $\beta$ o reator fica pronto-crítico; o SCRAM automático por período curto (< 10 s) mantém a operação normal longe disso.

## Xenônio

Cadeia real I-135 → Xe-135 com o tempo comprimido (1 hora real = 1 minuto de jogo). Depois de desligar, o xenônio sobe por uns 10 minutos antes de cair (poço de xenônio); o modo automático mostra quanto falta para poder religar.

$$
\frac{dI}{dt} = \gamma_I \Sigma_f \varphi - \lambda_I I, \qquad \frac{dX}{dt} = \gamma_X \Sigma_f \varphi + \lambda_I I - \lambda_X X - \sigma_X \varphi X, \qquad \rho_{\text{Xe}} = -2800\ \text{pcm} \cdot \frac{X}{X_{\text{eq}}}
$$

## Ciclo do combustível

O enriquecimento usa a fórmula real de trabalho separativo:

$$
V(x) = (2x - 1)\ln\frac{x}{1 - x}, \qquad \text{SWU/kg} = V(x_p) + T\,V(x_t) - F\,V(x_f), \quad x_f = 0{,}711\,\%,\ x_t = 0{,}25\,\%
$$

| Produto | Alimentação de UF₆ natural (kg/kg) | SWU por kg |
|---|---|---|
| LEU-3 | 5,97 | 3,81 |
| LEU-4 | 8,13 | 5,83 |
| LEU-4,5 | 9,22 | 6,87 |
| LEU-5 | 10,3 | 7,92 |

O combustível gasto (45 GWd/t) vai para a piscina e depois para o reprocessamento PUREX.
