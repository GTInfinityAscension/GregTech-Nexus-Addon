# Reatores de naquadah

Dois geradores queimam combustível de naquadah para gerar EU. O **Grande Reator de Naquadah** (UHV, port do GregTech Odyssey) vem primeiro; o **Hiper-Reator de Naquadah** (UEV, original do GTNA) queima os mesmos combustíveis com quatro vezes o EU por mB e aceita reforço de plasma.

| | Grande Reator de Naquadah | Hiper-Reator de Naquadah |
|---|---|---|
| **Tier** | UHV | UEV |
| **Tamanho** | 25 × 25 × 9 | 96 × 38 × 24 |
| **Saída** | Dynamo ou Laser Source Hatch (um) | Dynamo ou Laser Source Hatch (um) |
| **Hatches** | até 3 Input Hatches, 1 de Manutenção | até 3 Input Hatches, 1 de Manutenção |
| **Controlador** | Linha de Montagem, pesquisa no Gerador de Campo UV | Linha de Montagem (4 Grandes Reatores de Naquadah), pesquisa no Grande Reator de Naquadah |
| **Blocos** | [página do catálogo](catalog/large_naquadah_reactor.md) | [página do catálogo](catalog/naquadah_hyper_reactor.md) |

<div class="grid" markdown>

![Grande Reator de Naquadah](../../assets/machines/large_naquadah_reactor.webp){ loading=lazy }

![Hiper-Reator de Naquadah](../../assets/machines/naquadah_hyper_reactor.webp){ loading=lazy }

</div>

## Combustíveis

Os dois combustíveis saem do Large Chemical Reactor em UV (4000 ticks, 20.000 mB cada):

- **Combustível de Naquadah**: 16 pós de Naquadah, 30.000 mB de hidrogênio, 15.000 mB de nitrogênio, 8.000 mB de flúor, 8.000 mB de ácido nítrico.
- **Combustível de Naquadah Enriquecido**: 16 pós de Naquadah Enriquecida, 4 pós de antimônio, 48.000 mB de hidrogênio, 30.000 mB de nitrogênio, 12.000 mB de flúor, 8.000 mB de xenônio, 6.000 mB de radônio.

O modpack pode trocar essas receitas pelo id.

## Energia por mB

$$
\frac{\text{EU}}{\text{mB}} = \frac{t \cdot V}{\text{combustível (mB)}}
$$

| Máquina | Receita | Combustível por operação | Tempo | EU/t | EU por mB de combustível |
|---|---|---|---|---|---|
| Grande | Combustível de Naquadah + 80 mB de hidrogênio | 16 mB | 875 ticks | $2^{21}$ (UHV) | 114.688.000 |
| Grande | Combustível de Naquadah Enriquecido + 80 mB de hidrogênio | 16 mB | 1.250 ticks | $2^{21}$ (UHV) | 163.840.000 |
| Grande | Combustível de Naquadah + 40 mB de plasma de oxigênio | 160 mB | 28.000 ticks | $2^{19}$ (UV) | 91.750.400 |
| Grande | Combustível de Naquadah Enriquecido + 40 mB de plasma de nitrogênio | 160 mB | 40.000 ticks | $2^{19}$ (UV) | 131.072.000 |
| Hiper | Combustível de Naquadah + 80 mB de hidrogênio | 16 mB | 875 ticks | $2^{23}$ (UEV) | 458.752.000 |
| Hiper | Combustível de Naquadah Enriquecido + 80 mB de hidrogênio | 16 mB | 1.250 ticks | $2^{23}$ (UEV) | 655.360.000 |

No Grande Reator, as receitas com plasma trocam um pouco de EU por mB por uma operação 32 vezes mais longa em UV.

## Reforço do Hiper-Reator

Se houver um plasma de reforço num Input Hatch no início da operação, ela é multiplicada pelo paralelo do reforço: combustível, hidrogênio e EU/t crescem juntos, e o reforço é gasto uma vez por operação. Vale o melhor reforço presente.

$$
\text{EU/t} = 2^{23} \cdot p \qquad \text{combustível por operação} = 16\,p\ \text{mB} \qquad p \le \text{paralelo do reforço}
$$

| Reforço (por operação) | Paralelo $p$ | EU/t com Combustível de Naquadah |
|---|---|---|
| nenhum | 1 | $2^{23}$ = 8.388.608 |
| 40 mB de plasma de oxigênio | 8 | $2^{26}$ = 67.108.864 |
| 40 mB de plasma de nitrogênio | 16 | $2^{27}$ = 134.217.728 |

O paralelo é limitado pelo combustível nos hatches, nunca pela energia. O EU por mB de combustível não muda: o reforço aumenta a potência, não a eficiência.
