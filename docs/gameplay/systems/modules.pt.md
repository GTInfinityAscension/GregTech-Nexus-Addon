# Módulos e o Structure Terminal

## Módulos auxiliares {#auxiliary-modules}

Alguns multiblocos aceitam um **módulo auxiliar**: uma estrutura extra e opcional, construída ao lado da principal e checada pelo mesmo controlador. A máquina forma sem ela. Quando o módulo forma, os hatches dele passam para a máquina, o que libera novos tipos de hatch ou novos tipos de receita. O controlador mostra *Módulos formados: n / total*, o JEI/EMI mostra cada módulo como uma página extra da prévia da estrutura e o tooltip do item lista o que o módulo libera.

| Máquina | O que o módulo adiciona |
|---|---|
| Electric Blast Furnace (GTCEu) | Accelerate Hatch e Energy Hatches com fio extras |
| Fornalha de Liquefação | Parallel Hatch e Accelerate Hatch |
| Planta de Evaporação | Parallel Hatch e Accelerate Hatch |
| Congelador de Gelo Frio | receitas de Condensação por Atomização, um Accelerate Hatch e até seis Energy Hatches extras |
| Montadora de Componentes | duas formas de extensão (normal e larga) com mais hatches |
| Turbina Grande de Foguete | 2× produção, +20% de eficiência, 2× desgaste do rotor, até três Energy Output Hatches extras |
| Turbina de Vapor Supercrítica | os mesmos bônus do módulo da Turbina Grande de Foguete |
| Reator de Fusão Avançado | quatro módulos de tier (MK-II a MK-V) e um módulo de receitas cruzadas |
| Nano Forge | as estruturas dos tiers 2, 3 e 4 |

Modpacks podem acrescentar módulos a qualquer multibloco, do GTNA ou de outro mod, pelo KubeJS: veja [`GTNAServerEvents.subPatterns`](../../development/api/kubejs.md#auxiliary-modules). O registro de módulos fica no GTIA Lib desde o GTNA 0.6.1.

## Terminal de Estruturas Nexus {#nexus-structure-terminal}

Um construtor para multiblocos grandes.

- **Clique direito** no ar: configurações.
- **Shift + clique direito** num controlador: constrói a estrutura em volta dele, com os módulos.

| Opção | Efeito |
|---|---|
| Blocos por tier | escolhe o tier de bobina, casing ou vidro a colocar, por categoria |
| Repetições (0–1000) | camadas de estruturas expansíveis, como uma torre de destilação |
| Construção de módulos (0–100) | quantas camadas de módulo construir |
| Sem hatch | pula barramentos e hatches, para você colocar à mão |
| Substituir | troca os blocos que já estão no lugar (bobinas de outro tier, por exemplo) pela sua escolha; os blocos antigos vão para o inventário |
| Espelhar | constrói a versão espelhada da estrutura |
| Demolição | tira blocos que estão onde a estrutura precisa de ar |

No survival o terminal pega os blocos do seu inventário. Clique direito num Wireless Access Point do AE2 com ele para também puxar blocos dessa rede ME enquanto estiver no alcance.
