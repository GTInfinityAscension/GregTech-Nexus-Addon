# Matadouro Industrial

![Matadouro Industrial](../../assets/machines/industrial_slaughterhouse.webp){ loading=lazy }

Fazenda de mobs virtual: a máquina sorteia as loot tables vanilla do grupo de mobs escolhido, sem nenhum mob no mundo. [Página no catálogo](catalog/industrial_slaughterhouse.md).

## Modos

Coloque um circuito programado no barramento de entrada:

| Circuito | Modo | Mobs | A partir de | EU/t | Multiplicador de drops |
|:---:|---|---|---|---:|---|
| 1 | Passivo | galinha, vaca, porco, ovelha, coelho, cavalo, cabra | LV | 1.000 | `2^(tier − LV)` |
| 2 | Hostil | zumbi, esqueleto, creeper, aranha, enderman, bruxa, blaze | MV | 2.560 | `2^(tier − MV)` |
| 3 | Chefes | warden, wither, guardião ancião | ZPM | 32.000 | `3^(tier − ZPM)` |
| 4 | Dragão | 1 Ovo do Dragão, 4 Bafo do Dragão, 1 Cabeça de Dragão | UHV | 120.000 | `5^(tier − UHV)` |

Cada operação dura 40 ticks. O tier é o tier de energia da máquina. Abaixo do tier inicial do modo a máquina não produz nada.

## Quanto ela dá

Cada operação se repete `max(1, (tier − 2) × 8)` vezes: uma vez em LV e MV, 8 em HV, 16 em EV, 24 em IV e assim por diante. Cada repetição escolhe um mob aleatório do grupo, sorteia a loot table dele e multiplica cada drop pelo multiplicador do modo.

| Tier | Repetições | Passivo | Hostil | Chefes | Dragão |
|---|---:|---:|---:|---:|---:|
| LV | 1 | 1× | — | — | — |
| MV | 1 | 2× | 1× | — | — |
| HV | 8 | 4× | 2× | — | — |
| EV | 16 | 8× | 4× | — | — |
| IV | 24 | 16× | 8× | — | — |
| LuV | 32 | 32× | 16× | — | — |
| ZPM | 40 | 64× | 32× | 1× | — |
| UV | 48 | 128× | 64× | 3× | — |
| UHV | 56 | 256× | 128× | 9× | 1× |
| UEV | 64 | 512× | 256× | 27× | 5× |

Cada drop para em uma pilha (64 na maioria dos itens), então acima de 64× o multiplicador não acrescenta mais nada; as repetições extras continuam somando. Como os drops vêm das loot tables reais, mods e datapacks que mudam o loot dos mobs também mudam esta máquina.

## Dicas

- Dê vários barramentos de saída: tiers altos produzem muitas pilhas por operação.
- Ela roda sobre a lógica de múltiplas receitas do GTNA e aceita os Hatches de [Threads](../parts/thread-hatch.md), [Aceleração](../parts/accelerate-hatch.md) e [Overclock](../parts/overclock-hatch.md).
- A GUI mostra o modo atual, o multiplicador e os últimos drops.
