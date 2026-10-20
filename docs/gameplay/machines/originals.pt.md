# Multiblocos originais

Máquinas criadas para o GTNA, sem equivalente em outro mod. As quatro abaixo estão no jogo e **em teste**: números e receitas ainda podem mudar. Cada controlador tem uma tela própria com um **manual de campo** (capítulos explicando o funcionamento, em inglês, português e chinês).

!!! warning "Em desenvolvimento"
    Relate problemas com estas máquinas no [rastreador de issues](https://github.com/GTInfinityAscension/GregTech-Nexus-Addon/issues).

| Máquina | Tier | O que faz | Só ela produz |
|---|---|---|---|
| [Lança Cinética Orbital](catalog/kinetic_orbital_lance.md) | UEV | dispara projéteis em luas e asteroides a partir de um banco de capacitores e recolhe os fragmentos em cápsulas | Tolina Primordial (Arrokoth), Nexium (Nexus-1) |
| [Portão de Fenda Dimensional](catalog/dimensional_rift_gate.md) | UIV | abre fendas para dimensões com seed; ajuste frequência, fase e amplitude até a fenda se sustentar | um material exclusivo por bioma: Prismatium, Cronomercúrio, Forjacor, Vivisporo, Antimatéria Abissal, Resíduo Precursor, Cinza do Vazio |
| [Anel Colisor de Antimatéria](catalog/antimatter_collider_ring.md) | UIV | faz colidir feixes em sentidos opostos para gerar partículas exóticas e guarda antiprótons em armadilhas de Penning | células de antiprótons, partículas Higgs e top |
| [Câmara de Contenção Estelar](catalog/stellar_containment_chamber.md) | MAX | prende uma estrela de nêutrons em faixas de campo e manda a energia da rotação dela para a rede Nexus | Cristal de Magnetar, Matéria de Núcleo Degenerado |

As quatro alimentam umas às outras e o fim de jogo: os produtos delas entram na Forja dos Deuses, nos geradores de campo do Olho da Harmonia e nas barras de combustível de antimatéria.

## Lança Cinética Orbital

- Faça o levantamento de cada corpo para abri-lo no mapa orbital.
- Instale trilhos, resfriadores e sensores na bancada do cano. A energia do disparo é `½ m v²`, tirada do banco de capacitores inteiro.
- O regime do impacto (fragmentar, fundir, vaporizar) decide o que volta. As cápsulas voltam depois do tempo de viagem.
- Um revestimento gasto falha o disparo; um cano quente desvia do alvo. Nexus-1 só pode ser atingido com o Magnetar Slug.

## Portão de Fenda Dimensional

- A ressonância vem de três eixos de sintonia. Harmônicos gravados formam acordes que moldam a fenda; acordes dissonantes cavam mais fundo, mas custam mais.
- SpaceTime mantém a fenda estável; com estabilidade 0 ela colapsa.
- Âncoras de Profundidade aumentam a produção em `D^1,5`. A partir da profundidade 40, cada âncora também gasta um Contained X-Nexus.

## Anel Colisor de Antimatéria

- A energia do feixe segue `p = 0,3 · B · ρ`. Hélio líquido resfria os ímãs supercondutores; sem ele, eles perdem a supercondução.
- Uma partícula dá o rendimento cheio depois de descoberta com significância de 5σ. Propostas de pesquisa liberam ímãs e armadilhas mais fortes.
- As armadilhas de Penning usam EU sem fio; uma armadilha sem energia aniquila a antimatéria que guarda.

## Câmara de Contenção Estelar

- Até `2^59` EU/t como estrela de nêutrons. Acima de 2,2 massas solares a estrela colapsa num buraco negro, que dá até `2^62` EU/t a partir da ergosfera.
- Alimentar massa acelera a rotação da estrela. Girar mais rápido que o limite de Kepler a despedaça.
- Terremotos estelares decodificam a estrela e liberam tiers de faixa; faixas sem energia durante um terremoto danificam a contenção. Um magnetar gasta uma placa de Forjacor a cada 60 s.

## Próximo

O **Reator de Água Pressurizada** (IV) está projetado e a implementação está começando. O andamento fica no [roadmap](../../roadmap/index.md).
