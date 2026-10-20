# Esfera de Dyson

![Silo de Lançamento da Esfera de Dyson](../../assets/machines/dyson_sphere_launch_silo.webp){ loading=lazy }

Dois multiblocos montam um enxame de coletores em volta da estrela de um planeta e transformam isso em energia por laser.

| Máquina | Papel |
|---|---|
| [Silo de Lançamento](../machines/catalog/dyson_sphere_launch_silo.md) | lança Módulos do Enxame de Dyson na órbita do planeta onde está. Só na superfície, não em órbita. O tempo de lançamento cresce com a distância do planeta |
| [Estação Receptora](../machines/catalog/dyson_sphere_receiving_station.md) | transforma o enxame em energia e manda como laser. Precisa de computação e hélio líquido |

## Fórmulas

$$\text{EU/t} = V_{\text{MAX}} \cdot \text{módulos} \cdot \frac{50 - \max(0,\ \text{dano} - 60)}{50}$$

- Cada ciclo da estação soma 1 de dano ao enxame. Acima de 99 de dano o enxame perde um módulo.
- Um lançamento com dano acima de 60 **repara** o enxame em vez de somar um módulo.
- Até 100.000 módulos por planeta.

Continue lançando para manter o dano abaixo de 60 e a produção no máximo.
