# Condensado de Bose-Einstein

![Aparato de Emaranhamento](../../assets/machines/bec_generator.webp){ loading=lazy }

Uma rede de fabricação de fim de jogo trazida do GT: New Horizons. Cinco multiblocos compartilham **condensado**, um recurso exótico feito de metais fundidos, e usam esse recurso junto com nanites para fabricar as receitas de Montagem com Condensado.

## A rede

As máquinas se ligam por **Condutos de Condensado de Bose-Einstein**. Pinte os condutos para dividir uma rede em várias. O condensado é um recurso de rede, como a energia num cabo: nunca fica parado num hatch.

| Máquina | Papel |
|---|---|
| [Aparato de Emaranhamento](../machines/catalog/bec_generator.md) | transforma metais fundidos e fluidos em condensado, todos os fluidos dos hatches ao mesmo tempo. O paralelo ocupa todo o EU/t disponível; o ciclo dura o mesmo que a receita mais lenta. O condensado é perdido se a rede não tiver espaço |
| [Campo de Contenção](../machines/catalog/bec_storage.md) | guarda condensado (veja abaixo) |
| [Portão de Maxwell](../machines/catalog/bec_diode.md) | deixa o condensado passar num sentido só, com filtros por tipo definidos pelos hatches de entrada de fluido. Gasta 1A UIV ativo e bloqueia a rede desligado |
| [Matriz de Observação](../machines/catalog/bec_assembler.md) | alimenta os Nós de Teleporte ligados por conectores de linha de visão com nanites, EU e condensado. Uma matriz atende vários nós. O tier de nanite é o menor entre os barramentos; contam no máximo 30.720 nanites |
| [Nó de Teleporte](../machines/catalog/bec_io_node.md) | fabrica as receitas com os próprios barramentos (veja abaixo) |

## Fabricação

O Nó de Teleporte fabrica receitas de **Montagem com Condensado**:

- Cada slot de item pede um tier de nanite por vez.
- Nanites extras aceleram de forma linear. Nanites de tier maior que o pedido atrasam em $2^{\,\text{fornecido} - \text{exigido}}$.
- O condensado pode chegar a qualquer momento antes do fim. Se ainda faltar no fim, a fabricação falha.
- Mais de 3 tipos de condensado que a receita não pediu também fazem a fabricação falhar.
- Sem overclock. Paralelo mínimo e máximo e um divisor de velocidade ficam nos parâmetros do nó.
- Os nós param enquanto a Matriz de Observação estiver sem EU.

## Armazenamento

No **Campo de Contenção**, 1 de força de campo guarda 1 mB e custa 1 EU/t. O condensado que entra é dividido entre os campos pela capacidade. Acima da capacidade, o campo mantém 9/10 de cada condensado por segundo.

!!! danger "Falta de energia"
    Um Campo de Contenção que fica sem energia ou é desligado **perde tudo** o que guarda.
