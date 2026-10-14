# Esfera de Dyson

![](../../assets/machines/dyson_sphere_launch_silo.webp){ loading=lazy }

## Ciclo

O **Silo de Lançamento** põe módulos do enxame na órbita do planeta onde está (só na superfície). A **Estação Receptora** converte o enxame em laser, com computação e hélio líquido.

## Fórmulas

`EU/t = V[MAX] · módulos · (50 − max(0, dano − 60)) / 50`. Cada ciclo da estação soma 1 de dano; acima de 99 o enxame perde um módulo. Um lançamento com dano acima de 60 **repara** o enxame em vez de somar módulo. Máximo de 100.000 módulos por planeta.
