# Elevador Espacial

![Elevador Espacial](../../assets/machines/space_elevator.webp){ loading=lazy }

Um cabo até a órbita que alimenta até **12 módulos** em volta da base. Trazido do GT: New Horizons.

## Fazendo o elevador funcionar

- Só funciona a partir de UHV (acima de ZPM) e precisa de computação: `128 · (tier − ZPM)` CWU/t.
- Coloque **256 Carretéis de Nanotubos** pelo barramento de entrada.
- Os **Módulos de Energia** da estrutura definem o paralelo de todos os módulos: `4^(MK − 1)`. Todos precisam ser do mesmo MK (I a V). O MK também decide quais receitas do Módulo de Montagem podem rodar.

| Módulo de Energia | Paralelo dos módulos |
|---|---:|
| MK I | 1 |
| MK II | 4 |
| MK III | 16 |
| MK IV | 64 |
| MK V | 256 |

## Módulos

| Módulo | O que faz |
|---|---|
| [Módulo de Montagem](../machines/catalog/assembler_module.md) | monta peças em órbita |
| [Módulo de Coleta de Recursos](../machines/catalog/resource_collection_module.md) | manda drones minerar 20 misturas de asteroide e coletar 11 gases, com drones MK I a VI e combustível de foguete |

Os módulos só funcionam enquanto o Elevador Espacial está rodando.
