# Hatch de Controle de Paralelismo (UHV+)

Os Parallel Control Hatches do GTCEu param em 256 de paralelo (UV). O GTNA continua a linha com o mesmo nome:

| Hatch | Paralelo máximo |
|---|---:|
| UHV | 1.024 |
| UEV | 4.096 |
| UIV | 16.384 |
| UXV | 65.536 |
| OpV | 262.144 |

Eles usam a vaga normal de Parallel Hatch do GTCEu, então cabem em todo multibloco que aceita Parallel Hatch, um por máquina. Com um [Hatch de Threads](thread-hatch.md), o paralelo é dividido entre as threads.
