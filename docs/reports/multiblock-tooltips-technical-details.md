# Tooltips adaptadas das origens — 2026-10-10

Esta revisão substitui a ampliação G-0253, rejeitada pelo autor por repetir requisitos óbvios.
Foram revisadas as 148 entradas e alteradas 108 tooltips em EN/PT. Tipo, frase de efeito,
descrição, cores, separadores e atribuição foram preservados. Nenhuma mecânica foi modificada.

## Critério aplicado

O conteúdo técnico parte das tooltips originais, acomodado às listas existentes de vantagens,
números e restrições. Valores e condições são ajustados à implementação atual do GTNA.
Listas podem ficar vazias: não é necessário inventar uma restrição para preencher o padrão.

Foram retirados os acréscimos da revisão anterior e 74 linhas anteriores de preenchimento ou
redundância, como exigir Steam Hatch nas máquinas steam, repetir que o Gemini executa receitas
de Packer, anunciar ausência de bônus ou repetir o tipo de receita. O limite ajustável de máquinas
steam passou a ser expresso como máximo, evitando repetir o mesmo valor como padrão e teto.

## Referências conferidas

| Origem | Referência |
|---|---|
| GTOCore | `dc4824d`: registros, `GTOMachineTooltips.kt` e `GTOMachineTooltipsA.kt` |
| GTNL | `52345d2`: `createTooltip` dos controllers e traduções `en_US.lang` |
| GTLCore | `18c7814`: registros, traduções e rotas de `IntegratedOreRecipes` |
| GTCEu | `v7.5.3-1.20.1`: Data Bank, traduções e consumo por hatch |
| TST | `ceaa462`: tooltip e cálculo de Eye of Wood |
| GTNH | `a3e1e11241a814c9fa0dd0973d5699548428f689`: controllers e documentação de EOH/Godforge |
| GTLsupb | jar local `GTLsupb-2.6.4.jar`: traduções de Universal Factory e Primitive Stone Furnace |

A atribuição de cada máquina permanece em `GTNASources` e os avisos existentes em
`THIRD_PARTY_NOTICES.md`. Não foram copiadas implementações dos originais nesta revisão.

## Adaptações relevantes

- **Gemini e demais máquinas com bobinas:** bônus de paralelos por temperatura, comparação com
  o Parallel Hatch e suporte a hatches anunciado pela origem. Sem repetir Packer ou requisitos genéricos.
- **Eye of Harmony:** efeito de compressão, aceleração e estabilização sobre duração, chance e
  rendimento; excesso de gases e acumulação da compensação de falhas sob condições constantes.
- **Fuel Cell Generator:** recuperação de eficiência com água destilada, igualdade das quantidades
  de anólito/católito na absorção, desgaste e troca dos estados de carga na transferência.
- **Integrated Ore Processor:** sequência de processamento dos sete circuitos, conforme a origem.
- **Data Center:** consumo por hatch óptico, incluindo o aumento ao conectar recepção.
- **Supercomputing Center:** soma do CWU dos componentes, fator de correção e MFPC invalidado após uso.
- **Eye of Wood:** falta ou excesso de água/lava reduz a chance de sucesso.
- **Hyper Reactors:** reforço consumido antes do processamento aumentado.
- **Nano Forge:** localização da nanita adaptada ao bus de entrada do port.
- **Weather Modules:** seleção original de clima adaptada aos circuitos 1/2/3 do GTNA.

Recursos da origem ausentes no port foram omitidos, como seletores por materiais nos módulos de
clima, funções adicionais do Steam Vault, Astral Arrays do EOH e mecânicas novas de Convergence.
Bônus e paralelos steam usam os valores do GTNA, quando diferem do original.

## Validação

Fonte única e rastreio: 148 tooltips válidas, 290 números rastreados e zero sem confirmação.
EN/PT mantêm a mesma sequência e linhas de até 72 caracteres visíveis. Compilação, testes
unitários e geração de dados aprovados. O gate completo foi tentado; GameTests continuam travando
no segundo lote em `dimensionalFocusEngravingArrayRunsRecipe` / `BlockPattern.checkPatternAt`,
como nos checkpoints G-0251–G-0253. Não são considerados aprovados.

Pendente: revisão visual e de conteúdo pelo autor no cliente. Alterações locais, sem commit/push.
