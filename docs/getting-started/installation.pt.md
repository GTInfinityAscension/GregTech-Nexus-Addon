# Instalação

## Requisitos

| Mod | Versão | |
|---|---|---|
| Minecraft | 1.20.1 | obrigatório |
| Forge | 47.4.1 ou mais nova | obrigatório |
| [GregTech CEu Modern](https://www.curseforge.com/minecraft/mc-mods/gregtechceu-modern) | 7.5.3 ou mais nova | obrigatório; o Forge para com uma mensagem se for mais antiga |
| [GTIA Lib](https://github.com/GTInfinityAscension/GTIA-Lib) | 0.5.0 ou mais nova | obrigatório desde o GTNA 0.6.1 |
| [Applied Energistics 2](https://www.curseforge.com/minecraft/mc-mods/applied-energistics-2) | para 1.20.1 (testado com 15.4.10) | obrigatório: as peças ME são sempre registradas |
| JEI ou EMI | qualquer recente | opcional, muito recomendado: receitas e prévias de estrutura |
| KubeJS | 2001.6.5 | opcional: [API de scripts](../development/api/kubejs.md) |
| Ad Astra | 1.15.20 ou mais nova | opcional: planetas para o Elevador a Vapor, o Olho da Harmonia e os programas planetários de mineração do vazio |
| FTB Teams / FTB Quests | — | opcional: progresso por time na pesquisa e nas descobertas de fluido, tarefa de quest de pesquisa |
| Productive Bees | — | opcional: módulo de Reprodução de Abelhas do Elevador a Vapor |
| Jade | — | opcional: detalhes dos hatches de vapor sem fio |

O GTCEu tem as próprias dependências (como o LDLib); instale as versões que a página de download dele pede. O RenderBlender **não** é necessário desde o GTNA 0.5.6.

## Passos

1. Instale o Forge 47.4.1 ou mais novo para o Minecraft 1.20.1.
2. Ponha GTCEu, GTIA Lib, Applied Energistics 2 e GTNA na pasta `mods`.
3. Acrescente os mods opcionais que quiser.
4. Abra o jogo uma vez. O GTNA cria o `config/gtna.yaml` e os arquivos de balanceamento em `config/gtna/balance/` (veja [Configuração](configuration.md)).

Downloads: [releases no GitHub](https://github.com/GTInfinityAscension/GregTech-Nexus-Addon/releases). Desenvolvedores também encontram os jars das versões no [Maven da organização](https://gtinfinityascension.github.io/maven/).

## Servidores

O GTNA roda em servidores dedicados. Instale os mesmos mods no servidor e em todos os clientes; as opções só de cliente (HUDs, efeitos de item) ficam no `config/gtna.yaml` de cada jogador.
