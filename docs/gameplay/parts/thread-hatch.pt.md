# Hatch de Threads

Deixa um multibloco rodar receitas **diferentes** ao mesmo tempo. Um Parallel Hatch repete uma receita; um Hatch de Threads acrescenta vagas de receita independentes, cada uma com o próprio cronômetro.

| Hatch | Threads extras | Total |
|---|---:|---:|
| ZPM | +1 | 2 |
| UV | +3 | 4 |
| UHV | +7 | 8 |
| UEV | +15 | 16 |
| UIV | +31 | 32 |
| UXV | +63 | 64 |
| OpV | +127 | 128 |
| MAX | +255 | 256 |

Dá para diminuir o número na interface do hatch. Os valores ficam em `config/gtna/balance/hatches.json` (`threadHatch`).

## Onde funciona

As threads funcionam em máquinas construídas sobre a lógica de **múltiplas receitas** do GTNA cuja estrutura tem vaga para o hatch, por exemplo o [Matadouro Industrial](../machines/industrial-slaughterhouse.md), o Processador de Minério Integrado e a versão avançada, a Mega Destilaria, a Dimensionally Transcendent Dirt Forge, a Fornalha de Pedra Primitiva e o módulo de receitas cruzadas do Reator de Fusão Avançado. Os packs podem criar mais máquinas sobre essa base pelo KubeJS.

## Como as threads dividem o paralelo

Com um Parallel Hatch, o paralelo é dividido entre as threads. Exemplo: um Hatch de Controle de Paralelismo UEV (4.096) e um Hatch de Threads UV (4 threads) dão 4 receitas com 1.024 de paralelo cada.
