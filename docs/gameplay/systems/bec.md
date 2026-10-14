# Condensado de Bose-Einstein

![](../../assets/machines/bec_generator.webp){ loading=lazy }

## Rede de condensado

Cinco multiblocos ligados por **conduítes de BEC** (pinte para separar redes). O condensado é um recurso de rede, como energia: não fica em hatches.

## Máquinas

| Máquina | Função |
|---|---|
| Aparato de Emaranhamento | gera condensado a partir de metais fundidos; paralelos até o EU/t disponível |
| Campo de Contenção | guarda condensado (seção abaixo) |
| Portão de Maxwell | deixa o condensado passar em um sentido, com filtros; 1A UIV ativo |
| Matriz de Observação | alimenta os nós por linha de visão com nanites, EU e condensado; até 30.720 nanites |
| Nó de Teleporte | fabrica as receitas (seção abaixo) |

## Fabricação passo a passo

O **Nó de Teleporte** fabrica receitas de Montagem com Condensado com os próprios barramentos. Cada slot de item pede um tier de nanite por vez; nanites extras aceleram linearmente; nanites de tier maior atrasam em `2^(fornecido − exigido)`. O condensado pode chegar a qualquer momento antes do fim; faltando no fim, a receita falha.

## Armazenamento

No **Campo de Contenção**, 1 de força guarda 1 mB e custa 1 EU/t. Acima da capacidade, mantém 9/10 de cada condensado por segundo. **Sem energia ou desligado, destrói tudo.**
