# Multiblocos originais

Máquinas criadas para o GTNA, sem equivalente em outro mod. Cada controlador tem uma tela própria com um **manual de campo** (em inglês, português e chinês), e cada página abaixo traz as fórmulas, tabelas calculadas a partir do código e as telas atuais.

| Máquina | Tier | O que faz | Só ela produz |
|---|---|---|---|
| [Lança Cinética Orbital](originals/kinetic-orbital-lance.md) | UEV | dispara projéteis em luas e asteroides a partir de um banco de capacitores e recolhe os fragmentos em cápsulas | Tolina Primordial (Arrokoth), Nexium (Nexus-1) |
| [Portão de Fenda Dimensional](originals/dimensional-rift-gate.md) | UIV | abre fendas para dimensões com seed; ajuste frequência, fase e amplitude até a fenda se sustentar | um material exclusivo por bioma: Prismatium, Cronomercúrio, Forjacor, Vivisporo, Antimatéria Abissal, Resíduo Precursor, Cinza do Vazio |
| [Anel Colisor de Antimatéria](originals/antimatter-collider-ring.md) | UIV | faz colidir feixes em sentidos opostos para gerar partículas exóticas e guarda antiprótons em armadilhas de Penning | células de antiprótons, partículas Higgs e top |
| [Câmara de Contenção Estelar](originals/stellar-containment-chamber.md) | MAX | prende uma estrela de nêutrons em faixas de campo e manda a energia da rotação dela para a rede Nexus | Cristal de Magnetar, Matéria de Núcleo Degenerado |

As quatro alimentam umas às outras e o fim de jogo: os produtos delas entram na Forja dos Deuses, nos geradores de campo do Olho da Harmonia e nas barras de combustível de antimatéria.

## Dependências

- Lança → **Nexium** → Colisor (dipolos tier 4) e **Magnetário** (o projétil que quebra Nexus-1).
- Portão de Fenda → placas de **Forjacor** → Câmara Estelar (segura o campo de magnetar).
- Câmara Estelar → **Cristal de Magnetar** → Magnetário → Lança.
- Colisor → **X-Nexus** → Portão de Fenda (âncoras depois da profundidade 40) e Forja dos Deuses.

!!! bug "Problemas conhecidos"
    Nesta versão o Portão de Fenda não passa da profundidade 8 (sem Resíduo Precursor nem Cinza do Vazio) e o Colisor para depois da proposta e+e− (sem X-Nexus). Detalhes em cada página.

## Em seguida

O **Reator de Água Pressurizada** (IV) está projetado; veja a [página do planejamento](../../roadmap/pressurized-water-reactor.md).
