# Hatch de Aceleração

Encurta todas as receitas do multibloco, além do overclock normal. Trazido do GregTech Odyssey.

| | |
|---|---|
| **Tiers** | de LV a MAX |
| **Onde cabe** | multiblocos elétricos (GTCEu e GTNA) cuja estrutura o aceite, e os [módulos auxiliares](../systems/modules.md) que o acrescentam |
| **Por máquina** | um |

## Duração

O valor é a duração que sobra, em porcentagem da original:

| Hatch | Duração | Hatch | Duração |
|---|---:|---|---:|
| LV | 50% | UV | 36% |
| MV | 48% | UHV | 34% |
| HV | 46% | UEV | 32% |
| EV | 44% | UIV | 30% |
| IV | 42% | UXV | 28% |
| LuV | 40% | OpV | 26% |
| ZPM | 38% | MAX | 24% |

A fórmula é `50 − 2 · (tier − 1)` por cento. Dá para subir o valor na interface do hatch, até 100% (sem efeito).

## Penalidade

Para cada tier que a **receita** estiver acima do hatch, some 20 pontos. Uma receita de tier baixo numa máquina de tier alto nunca é penalizada.

!!! example
    Um hatch HV (46%) rodando uma receita EV: 46% + 20% = 66%. Uma receita de 100 ticks leva 66.

O valor final fica entre 1% e 100%. Os números ficam em `config/gtna/balance/hatches.json` (`accelerateHatch`), e o multiplicador de custo em EU é `machines.accelerateHatchEnergyCost` no `config/gtna.yaml` (padrão 1,5).

## Com outros hatches

Tudo se multiplica: `duração = base × passos de overclock × aceleração`. Veja um exemplo no [Hatch de Overclock](overclock-hatch.md).
