# Perguntas frequentes

??? question "O jogo para com uma mensagem de dependência faltando"
    O GTNA 0.6.1 precisa do **GTCEu 7.5.3 ou mais novo** e do **GTIA Lib 0.5.0 ou mais novo**. Um GTCEu antigo causava erros como `NoSuchFieldError: CLUSTER_MAX_HARVESTABLES` (issue #1). Atualize os dois mods. Veja [Instalação](installation.md).

??? question "Os ícones dos materiais do GTNA aparecem sem textura"
    O GTNA 0.5.4 e 0.5.5 dependiam do RenderBlender para esses modelos. Atualize para a 0.5.6 ou mais nova, que desenha os efeitos sozinha.

??? question "Dá para desligar os efeitos de item (halos, shaders)?"
    Sim, no `config/gtna.yaml`, seção `client`: `itemHalo`, `itemGlowEdge`, `itemShaderEffects` e `itemEffectSpeed`. Veja [Efeitos de item](../gameplay/systems/item-effects.md).

??? question "Minha estrutura não forma"
    Abra a estrutura no JEI/EMI e compare camada por camada; passe o mouse em cada posição para ver o que cabe ali. Confira se todos os casings têm o mesmo tier onde a máquina pede (máquinas a vapor em alta pressão precisam de **todos** os casings de aço). O [Terminal de Estruturas Nexus](../gameplay/systems/modules.md#nexus-structure-terminal) pode construir por você.

??? question "O hatch de saída de vapor sem fio não faz nada na minha caldeira"
    Ele só cabe no Large Steam Solar Boiler e nunca aceita vapor por cano. Veja [Rede de vapor sem fio](../gameplay/systems/wireless-steam-network.md).

??? question "Um pattern do Pattern Buffer nunca roda"
    Clique com o botão do meio no slot: circuito programado faltando ou modo preferido errado é a causa mais comum. Veja [ME Pattern Buffers](../gameplay/systems/pattern-buffers.md).

??? question "As receitas são diferentes das do GTNH ou do GTO"
    O GTNA traz receitas padrão que funcionam. O balanceamento é do modpack, que pode mudar tudo por KubeJS, datapacks e pelos arquivos de balanceamento em `config/gtna/balance/`.

??? question "Preciso do Ad Astra?"
    Não. Sem ele o Elevador a Vapor não viaja, o Olho da Harmonia só tem as dimensões do Minecraft e os programas planetários da mineração do vazio não aparecem.

??? question "Onde relato um bug?"
    No [rastreador de issues](https://github.com/GTInfinityAscension/GregTech-Nexus-Addon/issues), com o `latest.log` (e a pasta `crash-reports/` se o jogo travou) e as versões do GTNA, do GTCEu e do GTIA Lib.

??? question "Posso traduzir a wiki ou o mod?"
    Pode, veja [Traduzir](../development/translating.md).
