# Instalação

## Requisitos

| Mod | Versão | Obrigatório |
|---|---|---|
| Minecraft | 1.20.1 | sim |
| Forge | 47.4.1 ou mais novo | sim |
| GregTech CEu Modern | 7.5.3 ou mais novo | sim |
| LDLib | a que acompanha o GTCEu | sim (vem com o GTCEu) |
| Ad Astra | 1.15.20 ou mais novo | não: planetas, Elevador a Vapor, Olho da Harmonia fora do Overworld |
| Stargate Journey | 0.6.44 ou mais novo | não: integração de portais |
| KubeJS | 2001.6.5 | não: scripts (veja a API KubeJS) |
| Applied Energistics 2 | 15.x | não: Pattern Buffer, hatches ME, automação |
| JEI ou EMI | qualquer recente | não: receitas e estruturas |

!!! info "RenderBlender não é mais necessário"
    Até a 0.5.5 os efeitos dos ícones de material dependiam do RenderBlender. Desde a 0.5.6 o GTNA tem render próprio.

## Passo a passo

1. Instale Forge 47.4.1 ou mais novo para o Minecraft 1.20.1.
2. Coloque o GTCEu Modern e o GTNA na pasta `mods`.
3. Adicione os opcionais que quiser.
4. Abra o jogo uma vez para gerar `config/gtna.json`.

## Configuração

O arquivo `config/gtna.json` tem seções de gameplay, cliente, máquinas, itens restritos, vapor wireless e liga/desliga por máquina e por hatch. Todas as opções têm nome e comentário em português e inglês no menu de configuração do jogo.
