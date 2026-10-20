# Hatch de Overclock

Melhora a própria curva de overclock. Normalmente cada passo de overclock (4× EU/t) corta a duração pela metade; com este hatch, cada passo divide a duração pelo divisor do hatch. Trazido do GregTech Odyssey.

| Hatch | Divisor por passo | Duração por passo |
|---|---:|---:|
| UV | 2 | 50% |
| UHV | 3 | 33,3% |
| UEV | 4 | 25% |
| UIV | 5 | 20% |
| UXV | 6 | 16,7% |
| OpV | 7 | 14,3% |
| MAX | 8 | 12,5% |

O hatch UV é igual ao overclock padrão, então o ganho começa no UHV. Dá para diminuir o divisor na interface do hatch. Os números ficam em `config/gtna/balance/hatches.json` (`overclockHatch`).

## Exemplo

Uma receita de 200 ticks com dois passos de overclock, um Hatch de Aceleração EV (44%) e um Hatch de Overclock UHV:

```
200 ÷ 3 ÷ 3 = 22,2 ticks      (dois passos de overclock com divisor 3)
22,2 × 0,44 = 9,8 ticks       (Hatch de Aceleração)
```

Sem o Hatch de Overclock, a mesma receita leva `200 ÷ 2 ÷ 2 × 0,44 = 22` ticks.
