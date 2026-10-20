"""Wiki pages whose tables are computed from constants in the mod code: Forge of the Gods and Eye of Harmony.

    python3 tools/wiki/system_pages.py   -> docs/gameplay/systems/{forge-of-gods,eye-of-harmony}{.md,.pt.md,.zh.md}

Forge of the Gods: formulas from api/machine/feature/godforge/GodforgeMath.java (port of GT5-Unofficial a3e1e112).
Eye of Harmony: api/machine/feature/eyeofharmony/EyeOfHarmonyMath.java (same source).
Images credited to the GTNH wiki (CC BY-SA 4.0) live in docs/assets/gtnh/.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import zh_punct  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
OUT = os.path.join(ROOT, 'docs/gameplay/systems')
LANGS = (('en', '.md'), ('pt', '.pt.md'), ('zh', '.zh.md'))

# constants copied from GodforgeData.java / GodforgeMath.java
POWER_C, RECIPE_C, FUEL_C = 1e15, 1e7, 1e4


def n(x, lang):
    if x >= 1e7: s = f'{x:.3g}'.replace('e+0', 'e').replace('e+', 'e')
    else: s = f'{x:,.0f}' if abs(x - round(x)) < 1e-9 or x >= 100 else f'{x:,.2f}'
    return s.replace(',', 'X').replace('.', ',').replace('X', '.') if lang == 'pt' else s


def table(head, rows):
    return '\n'.join(['| ' + ' | '.join(head) + ' |', '|' + '|'.join('---' for _ in head) + '|'] +
                     ['| ' + ' | '.join(str(c) for c in r) + ' |' for r in rows]) + '\n'


def heat(f, base=1.5): return 12601 + int(math.log(f) / math.log(base) * 1000)
def fuel_residue(f, stem=False): return f * 300 * 1.15 ** f * (0.8 if stem else 1)
def fuel_plasma(f, stem=False): return f * 2 * 1.08 ** f * (0.8 if stem else 1)
def startup(f): return max(f * 25 * 1.2 ** f, 1)
def eff_factor(f): return f if f <= 43 else 43 + math.floor((f - 43) ** 0.4)


FOG = {
    'en': dict(
        title='Forge of the Gods', intro='The Forge of the Gods (Godforge) is a UIV multiblock that keeps an artificial star and powers up to 16 processing **modules** with wireless energy. '
        'This page collects what the game does not show: every formula, tables computed from the GTNA code, and the differences from GTNH.',
        credit='Image: GTNH Wiki, CC BY-SA 4.0.', facts=[('Tier', 'UIV'), ('Size', '186 × 127 × 29 (ring 1)'), ('Energy', 'wireless, no energy hatch'),
        ('Overclock', 'imperfect (4/2), 4/2.3 with GGEBE'), ('Origin', 'port of GT5-Unofficial a3e1e112')],
        s_struct='Structure', struct='Up to three rings. Modules sit in smaller rings around them. To build a new ring, turn the animation off (screwdriver on the controller or the cosmetics button), build it, and turn it back on with a soft mallet. '
        'The hologram projector uses the stack size to pick how many rings to show.',
        s_modules='Modules', mod_head=['Module', 'Unlock', 'Base parallel', 'Function'],
        mods=[('Helioflare Power Forge', 'START', 1024, 'blast furnace or multi-smelter (furnace mode does not count for milestones)'),
              ('Helioflux Melting Core', 'FDIM', 512, 'blast furnace with molten output'), ('Heliothermal Plasma Fabricator', 'GPCI', 512, 'dust or fluid straight to plasma'),
              ('Heliofusion Exoticizer', 'QGPIU (magmatter: EE)', 64, 'quark-gluon plasma and MagMatter; needs automation')],
        slots='Module limit: 8, 12 with ring 2 (CD), 16 with ring 3 (EE). Going over the limit disconnects every module.',
        s_fuel='Fuel', fuel_txt='The star is lit with Stellar Fuel in the input bus. Startup cost: $f \\cdot 25 \\cdot 1.2^{f}$ items. '
        'The consumption factor $f$ goes up to 5 without upgrades. The controller drains fuel every 5 s (×2 while the battery charges).',
        fuel_head=['f', 'Base heat (K)', 'Startup (items)', 'DTR/s', 'DTR/s with STEM', 'Stellar plasma/s', 'MCSM/s'],
        fuel_formula='$$\n\\begin{aligned}\n\\text{DTR (residue)} &= f \\cdot 300 \\cdot 1.15^{f} && (\\times 0.8 \\text{ with STEM}) \\\\\n\\text{Stellar plasma} &= f \\cdot 2 \\cdot 1.08^{f} && (\\times 0.8 \\text{ with STEM}) \\\\\n\\text{MCSM} &= f / 25 \\\\\n\\text{heat} &= 12601 + 1000 \\cdot \\log_{1.5} f && (\\text{base } 1.12 / 1.18 \\text{ with SEFCP})\n\\end{aligned}\n$$\n',
        caps='Max factors with TSE: residue 70 (72 with STEM), stellar plasma 181 (184 with STEM), MCSM uncapped. Above 43 the effective SA factor grows slowly: $43 + (f - 43)^{0.4}$.',
        s_heat='Heat and bonus cap', heat_txt='Heat bonuses apply up to the cap: 15,000 K, or 30,000 K with CNTI. With NDPE, heat above 30,000 K counts compressed: $30000 + (\\text{heat} - 30000)^{e}$, with e = 0.85 for the Power Forge and 0.8 for the others.',
        s_par='Parallel', par_txt='$$\n\\begin{aligned}\n\\text{parallel} &= \\text{base} \\cdot \\text{CTCDD}(\\times 2) \\cdot \\text{SA} \\cdot \\text{EPEC} \\cdot \\text{PoS} \\\\\n\\text{SA} &= 1 + f_{\\text{eff}} / 15 && (\\text{TCT: } \\times 3 \\text{ on Melting Core and Power Forge with DoP, } \\times 2 \\text{ otherwise}) \\\\\n\\text{EPEC} &= 1 + \\text{heat} / 15000 && (\\text{Melting Core, Power Forge with DoP; otherwise } 1 + \\text{heat}/25000) \\\\\n\\text{PoS} &= 1 + \\text{upgrades} / 5 && (\\text{Melting Core, Power Forge with DoP; otherwise } 1 + \\text{upgrades}/8)\n\\end{aligned}\n$$\n\nExoticizer: square root of the total with PA, otherwise 1.\n\n',
        par_head=['f', 'f eff.', 'SA', 'SA + TCT (Melting Core)'],
        par_note='The GTNH wiki only shows the /15000 and /5 versions. The code uses larger divisors outside the Melting Core.',
        s_speed='Speed and energy', speed_txt='$$\n\\begin{aligned}\n\\text{IGCC:}\\quad & t \\times \\text{heat}^{-0.01} \\\\\n\\text{DoR:}\\quad & t \\div \\text{parallel}^{0.02} \\text{ (plasma) or } \\text{parallel}^{0.012} \\text{ (others)} \\\\\n\\text{REC:}\\quad & \\text{discount} = \\frac{1 - 1.05^{-0.05 \\cdot \\text{max battery}}}{20} \\\\\n\\text{IMKG:}\\quad & \\text{charge discount} = 1 - \\left(-0.6\\,(c - 0.5)^2 + 0.15\\right) \\text{ on plasma, } \\times \\tfrac{2}{3} \\text{ on the others} \\\\\n\\text{GISS:}\\quad & V \\mathrel{+}= \\text{fuel units/s} \\cdot 10^{8}\\ \\text{EU/t} \\\\\n\\text{NGMS:}\\quad & V \\times 4 \\text{ per active ring (applied last)}\n\\end{aligned}\n$$\n',
        s_ms='Milestones', ms_txt='Each milestone has 7 tiers and grants graviton shards equal to the tier. Once all four reach tier 7, **Inversion** removes the cap and every new tier costs the same as tier 7.',
        ms_head=['Tier', 'Charge (EU)', 'Conversion (recipes)', 'Catalyst (fuel)', 'Composition'],
        s_up='Upgrades', up_txt='Bought with graviton shards. Blue line: one prerequisite is enough; red line: all of them are needed. After the Exoticizer the tree splits in three (purple: heat; orange: parallel; green: plasma). One branch first, the second with ring 2, all three with ring 3. Refunds work only when no dependent upgrade is active.',
        up_head=['Tag', 'Cost', 'Requires', 'Effect'],
        s_cost='Extra upgrade materials (GTNA)', mat='Materials',
        cost_note='GTNA substitutions compared with GTNH: UHT Resistant Mesh → Neutronium foil; Fusion Internal Casing 2 → Fusion Casing MK4; Compact Fusion Coil T4 → Compressed Fusion Coil MK2; UMV parts → UXV. Transdimensional Alignment Matrix and MagMatter nanites are left out.',
        s_diff='Differences from GTNH', diffs=['Plasma Fabricator base parallel is 512 in the code (the GTNH wiki says 384).', 'Exoticizer magmatter is unlocked by **EE** in the GTNA code (the GTNH wiki says END).',
                    'Material costs adapted to items that exist in GTNA (previous section).', 'Fuels and max factors are identical to GT5-Unofficial a3e1e112.'],
        s_tree='Upgrade tree (GTNH)', s_credits='Credits',
        credits='Images marked "GTNH Wiki" come from the [GT New Horizons wiki](https://wiki.gtnewhorizons.com/wiki/Forge_of_the_Gods), licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). '
        'This page is distributed under the same license. Original mechanics: GT5-Unofficial (GTNH team).'),
    'pt': dict(
        title='Forja dos Deuses', intro='A Forja dos Deuses (Godforge) é um multibloco UIV que mantém uma estrela artificial e alimenta até 16 **módulos** de processamento com energia sem fio. '
        'Esta página reúne o que o jogo não mostra: todas as fórmulas, as tabelas calculadas a partir do código do GTNA e as diferenças em relação ao GTNH.',
        credit='Imagem: GTNH Wiki, CC BY-SA 4.0.', facts=[('Tier', 'UIV'), ('Tamanho', '186 × 127 × 29 (anel 1)'), ('Energia', 'sem fio, sem hatch de energia'),
        ('Overclock', 'imperfeito (4/2), 4/2,3 com GGEBE'), ('Origem', 'port do GT5-Unofficial a3e1e112')],
        s_struct='Estrutura', struct='Até três anéis. Os módulos ficam em anéis menores ao redor. Para construir um anel novo, desligue a animação (chave de fenda no controlador ou o botão nos cosméticos), construa e religue com o martelo macio. '
        'O projetor holográfico usa o tamanho da pilha para escolher quantos anéis mostrar.',
        s_modules='Módulos', mod_head=['Módulo', 'Libera', 'Paralelo base', 'Função'],
        mods=[('Helioflare Power Forge', 'START', 1024, 'alto-forno ou multi-fornalha (o modo fornalha não conta nos marcos)'),
              ('Helioflux Melting Core', 'FDIM', 512, 'alto-forno com saída fundida'), ('Heliothermal Plasma Fabricator', 'GPCI', 512, 'pó ou fluido direto para plasma'),
              ('Heliofusion Exoticizer', 'QGPIU (matéria mágica: EE)', 64, 'plasma de quarks e glúons e MagMatter; precisa de automação')],
        slots='Limite de módulos: 8, 12 com o anel 2 (CD), 16 com o anel 3 (EE). Passar do limite desconecta todos.',
        s_fuel='Combustível', fuel_txt='A estrela é acesa com Combustível Estelar no barramento de entrada. Custo de partida: $f \\cdot 25 \\cdot 1{,}2^{f}$ itens. '
        'O fator de consumo $f$ vai até 5 sem upgrades. O controlador drena combustível a cada 5 s (×2 com a bateria carregando).',
        fuel_head=['f', 'Calor base (K)', 'Partida (itens)', 'DTR/s', 'DTR/s com STEM', 'Plasma estelar/s', 'MCSM/s'],
        fuel_formula='$$\n\\begin{aligned}\n\\text{DTR (resíduo)} &= f \\cdot 300 \\cdot 1{,}15^{f} && (\\times 0{,}8 \\text{ com STEM}) \\\\\n\\text{Plasma estelar} &= f \\cdot 2 \\cdot 1{,}08^{f} && (\\times 0{,}8 \\text{ com STEM}) \\\\\n\\text{MCSM} &= f / 25 \\\\\n\\text{calor} &= 12601 + 1000 \\cdot \\log_{1{,}5} f && (\\text{base } 1{,}12 / 1{,}18 \\text{ com SEFCP})\n\\end{aligned}\n$$\n',
        caps='Fatores máximos com TSE: resíduo 70 (72 com STEM), plasma estelar 181 (184 com STEM), MCSM sem limite. Acima de 43 o fator efetivo do SA cresce devagar: $43 + (f - 43)^{0{,}4}$.',
        s_heat='Calor e teto de bônus', heat_txt='Os bônus de calor valem até o teto: 15.000 K, ou 30.000 K com CNTI. Com NDPE, acima de 30.000 K o calor conta comprimido: $30000 + (\\text{calor} - 30000)^{e}$, com e = 0,85 no Power Forge e 0,8 nos demais.',
        s_par='Paralelo', par_txt='$$\n\\begin{aligned}\n\\text{paralelo} &= \\text{base} \\cdot \\text{CTCDD}(\\times 2) \\cdot \\text{SA} \\cdot \\text{EPEC} \\cdot \\text{PoS} \\\\\n\\text{SA} &= 1 + f_{\\text{ef}} / 15 && (\\text{TCT: } \\times 3 \\text{ no Melting Core e no Power Forge com DoP, } \\times 2 \\text{ nos outros}) \\\\\n\\text{EPEC} &= 1 + \\text{calor} / 15000 && (\\text{Melting Core e Power Forge com DoP; senão } 1 + \\text{calor}/25000) \\\\\n\\text{PoS} &= 1 + \\text{upgrades} / 5 && (\\text{Melting Core e Power Forge com DoP; senão } 1 + \\text{upgrades}/8)\n\\end{aligned}\n$$\n\nExoticizer: raiz quadrada do total com PA, senão 1.\n\n',
        par_head=['f', 'f ef.', 'SA', 'SA + TCT (Melting Core)'],
        par_note='A wiki do GTNH mostra só as versões /15000 e /5. O código usa divisores maiores fora do Melting Core.',
        s_speed='Velocidade e energia', speed_txt='$$\n\\begin{aligned}\n\\text{IGCC:}\\quad & t \\times \\text{calor}^{-0{,}01} \\\\\n\\text{DoR:}\\quad & t \\div \\text{paralelo}^{0{,}02} \\text{ (plasma) ou } \\text{paralelo}^{0{,}012} \\text{ (outros)} \\\\\n\\text{REC:}\\quad & \\text{desconto} = \\frac{1 - 1{,}05^{-0{,}05 \\cdot \\text{bateria máx}}}{20} \\\\\n\\text{IMKG:}\\quad & \\text{desconto pela carga} = 1 - \\left(-0{,}6\\,(c - 0{,}5)^2 + 0{,}15\\right) \\text{ no plasma, } \\times \\tfrac{2}{3} \\text{ nos outros} \\\\\n\\text{GISS:}\\quad & V \\mathrel{+}= \\text{unidades de combustível/s} \\cdot 10^{8}\\ \\text{EU/t} \\\\\n\\text{NGMS:}\\quad & V \\times 4 \\text{ por anel ativo (aplicado por último)}\n\\end{aligned}\n$$\n',
        s_ms='Marcos', ms_txt='Cada marco tem 7 níveis e dá fragmentos de gráviton iguais ao nível. Depois que os quatro chegam ao nível 7, a **Inversão** remove o teto e cada nível novo custa o mesmo que o 7.',
        ms_head=['Nível', 'Carga (EU)', 'Conversão (receitas)', 'Catalisador (combustível)', 'Composição'],
        s_up='Upgrades', up_txt='Comprados com fragmentos de gráviton. Linha azul: basta um pré-requisito; linha vermelha: todos. Depois do Exoticizer a árvore se divide em três (roxo: calor; laranja: paralelo; verde: plasma). Um ramo no começo, o segundo com o anel 2, os três com o anel 3. O reembolso só funciona sem upgrades dependentes ativos.',
        up_head=['Tag', 'Custo', 'Pré-requisito', 'Efeito'],
        s_cost='Materiais extras dos upgrades (GTNA)', mat='Materiais',
        cost_note='Substituições do GTNA em relação ao GTNH: Malha Resistente a UHT → folha de Neutrônio; Fusion Internal Casing 2 → Fusion Casing MK4; Compact Fusion Coil T4 → Compressed Fusion Coil MK2; peças UMV → UXV. Transdimensional Alignment Matrix e nanites de MagMatter não entram.',
        s_diff='Diferenças em relação ao GTNH', diffs=['Plasma Fabricator com paralelo base 512 no código (a wiki do GTNH cita 384).', 'A matéria mágica do Exoticizer é liberada pelo **EE** no código do GTNA (a wiki do GTNH cita END).',
                    'Custos de material adaptados aos itens que existem no GTNA (seção anterior).', 'Combustíveis e fatores máximos idênticos ao GT5-Unofficial a3e1e112.'],
        s_tree='Árvore de upgrades (GTNH)', s_credits='Créditos',
        credits='Imagens marcadas com "GTNH Wiki" vêm da [wiki do GT New Horizons](https://wiki.gtnewhorizons.com/wiki/Forge_of_the_Gods), licenciadas sob [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). '
        'Esta página é distribuída sob a mesma licença. Mecânica original: GT5-Unofficial (equipe do GTNH).'),
    'zh': dict(
        title='诸神之锻炉', intro='诸神之锻炉(Godforge)是一个 UIV 多方块,维持一颗人造恒星,并以无线能量为最多 16 个加工**模块**供能。'
        '本页汇总了游戏内看不到的内容:全部公式、根据 GTNA 代码计算的表格,以及与 GTNH 的差异。',
        credit='图片：GTNH Wiki，CC BY-SA 4.0。', facts=[('等级', 'UIV'), ('尺寸', '186 × 127 × 29(第一环)'), ('能量', '无线,无需能源仓'),
        ('超频', '非完美(4/2),GGEBE 后为 4/2.3'), ('来源', '移植自 GT5-Unofficial a3e1e112')],
        s_struct='结构', struct='最多三个环。模块位于周围较小的环上。建造新环时,先关闭动画(对控制器使用螺丝刀,或点击外观按钮),建好后用软锤重新开启。'
        '全息投影仪根据物品堆叠数量决定显示几个环。',
        s_modules='模块', mod_head=['模块', '解锁', '基础并行', '功能'],
        mods=[('太阳烈焰能量锻炉', 'START', 1024, '高炉或多重熔炉(熔炉模式不计入里程碑)'),
              ('太阳射流融化核心', 'FDIM', 512, '输出熔融物的高炉'), ('太阳热能等离子制造机', 'GPCI', 512, '粉或流体直接转为等离子体'),
              ('太阳聚变异化器', 'QGPIU(磁物质:EE)', 64, '夸克-胶子等离子体与磁物质;需要自动化')],
        slots='模块上限:8 个;第二环(CD)后 12 个;第三环(EE)后 16 个。超过上限会断开所有模块。',
        s_fuel='燃料', fuel_txt='在输入总线中放入恒星燃料点燃恒星。启动消耗:$f \\cdot 25 \\cdot 1.2^{f}$ 个。'
        '未升级时燃料消耗系数 $f$ 最高为 5。控制器每 5 秒消耗一次燃料(电池充能时 ×2)。',
        fuel_head=['f', '基础热量 (K)', '启动(个)', 'DTR/秒', 'STEM 后 DTR/秒', '恒星等离子体/秒', 'MCSM/秒'],
        fuel_formula='$$\n\\begin{aligned}\n\\text{DTR（残渣）} &= f \\cdot 300 \\cdot 1.15^{f} && (\\text{STEM 后 } \\times 0.8) \\\\\n\\text{恒星等离子体} &= f \\cdot 2 \\cdot 1.08^{f} && (\\text{STEM 后 } \\times 0.8) \\\\\n\\text{MCSM} &= f / 25 \\\\\n\\text{热量} &= 12601 + 1000 \\cdot \\log_{1.5} f && (\\text{SEFCP 后底数为 } 1.12 / 1.18)\n\\end{aligned}\n$$\n',
        caps='TSE 后的最大系数:残渣 70(STEM 后 72),恒星等离子体 181(STEM 后 184),MCSM 无上限。超过 43 后 SA 的有效系数增长变慢:$43 + (f - 43)^{0.4}$。',
        s_heat='热量与加成上限', heat_txt='热量加成在上限内生效:15,000 K,CNTI 后为 30,000 K。有 NDPE 时,超过 30,000 K 的热量按压缩计算:$30000 + (\\text{热量} - 30000)^{e}$,能量锻炉 e = 0.85,其他模块 e = 0.8。',
        s_par='并行', par_txt='$$\n\\begin{aligned}\n\\text{并行} &= \\text{基础} \\cdot \\text{CTCDD}(\\times 2) \\cdot \\text{SA} \\cdot \\text{EPEC} \\cdot \\text{PoS} \\\\\n\\text{SA} &= 1 + f_{\\text{有效}} / 15 && (\\text{TCT：融化核心及有 DoP 的能量锻炉 } \\times 3\\text{，其他 } \\times 2) \\\\\n\\text{EPEC} &= 1 + \\text{热量} / 15000 && (\\text{融化核心、有 DoP 的能量锻炉；否则 } 1 + \\text{热量}/25000) \\\\\n\\text{PoS} &= 1 + \\text{升级数} / 5 && (\\text{融化核心、有 DoP 的能量锻炉；否则 } 1 + \\text{升级数}/8)\n\\end{aligned}\n$$\n\n异化器：有 PA 时取总值的平方根，否则为 1。\n\n',
        par_head=['f', 'f 有效', 'SA', 'SA + TCT(融化核心)'],
        par_note='GTNH Wiki 只列出了 /15000 和 /5 的版本。代码在融化核心以外使用更大的除数。',
        s_speed='速度与能量', speed_txt='$$\n\\begin{aligned}\n\\text{IGCC：}\\quad & t \\times \\text{热量}^{-0.01} \\\\\n\\text{DoR：}\\quad & t \\div \\text{并行}^{0.02}\\text{（等离子）或 } \\text{并行}^{0.012}\\text{（其他）} \\\\\n\\text{REC：}\\quad & \\text{折扣} = \\frac{1 - 1.05^{-0.05 \\cdot \\text{最大电池}}}{20} \\\\\n\\text{IMKG：}\\quad & \\text{按充能折扣} = 1 - \\left(-0.6\\,(c - 0.5)^2 + 0.15\\right)\\text{（等离子），其他 } \\times \\tfrac{2}{3} \\\\\n\\text{GISS：}\\quad & V \\mathrel{+}= \\text{燃料单位/秒} \\cdot 10^{8}\\ \\text{EU/t} \\\\\n\\text{NGMS：}\\quad & \\text{每个激活的环 } V \\times 4\\text{（最后计算）}\n\\end{aligned}\n$$\n',
        s_ms='里程碑', ms_txt='每个里程碑有 7 级,每级给予与等级相同数量的引力子碎片。四个里程碑都到 7 级后,**反转**解除上限,之后每一级的花费与第 7 级相同。',
        ms_head=['等级', '充能 (EU)', '转化(配方)', '催化(燃料)', '组成'],
        s_up='升级', up_txt='用引力子碎片购买。蓝线:满足任一前置即可;红线:需要全部前置。异化器之后升级树分为三支(紫:热量;橙:并行;绿:等离子)。起初只能走一支,第二环后两支,第三环后三支。只有在没有依赖它的升级激活时才能退还。',
        up_head=['标签', '花费', '前置', '效果'],
        s_cost='升级的额外材料(GTNA)', mat='材料',
        cost_note='GTNA 相对 GTNH 的替换:抗超高温网 → 中子素箔;聚变内部外壳 2 → 聚变外壳 MK4;紧凑聚变线圈 T4 → 压缩聚变线圈 MK2;UMV 部件 → UXV。未加入跨维对准矩阵与磁物质纳米蜂群。',
        s_diff='与 GTNH 的差异', diffs=['代码中等离子制造机的基础并行为 512(GTNH Wiki 写的是 384)。', 'GTNA 代码中异化器的磁物质由 **EE** 解锁(GTNH Wiki 写的是 END)。',
                    '材料花费已改为 GTNA 中存在的物品(见上一节)。', '燃料与最大系数与 GT5-Unofficial a3e1e112 相同。'],
        s_tree='升级树(GTNH)', s_credits='致谢',
        credits='标注 "GTNH Wiki" 的图片来自 [GT New Horizons Wiki](https://wiki.gtnewhorizons.com/wiki/Forge_of_the_Gods),采用 [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) 许可。'
        '本页以相同许可发布。原始机制:GT5-Unofficial(GTNH 团队)。'),
}

UPGRADES = [  # tag, cost, requires, effect (en, pt, zh)
    ('START', 0, '—', ('8 modules, ring 1, Power Forge, 2 bn EU/t, 15,000 K cap', '8 módulos, anel 1, Power Forge, 2 bi EU/t, teto 15.000 K', '8 个模块、第一环、能量锻炉、20 亿 EU/t、上限 15,000 K')),
    ('IGCC', 1, 'START', ('$t \\times \\text{heat}^{-0.01}$', '$t \\times \\text{calor}^{-0{,}01}$', '$t \\times \\text{热量}^{-0.01}$')),
    ('STEM', 1, 'IGCC', ('fuel × 0.8', 'combustível × 0,8', '燃料 × 0.8')),
    ('CFCE', 1, 'IGCC', ('max factor × 1.2', 'fator máximo × 1,2', '最大系数 × 1.2')),
    ('GISS', 1, 'STEM', ('$V \\mathrel{+}= \\text{fuel/s} \\cdot 10^{8}$', '$V \\mathrel{+}= \\text{combustível/s} \\cdot 10^{8}$', '$V \\mathrel{+}= \\text{燃料/秒} \\cdot 10^{8}$')),
    ('FDIM', 1, 'STEM, CFCE', ('unlocks Melting Core', 'libera o Melting Core', '解锁融化核心')),
    ('SA', 1, 'CFCE', ('parallel $\\times (1 + f/15)$', 'paralelo $\\times (1 + f/15)$', '并行 $\\times (1 + f/15)$')),
    ('GPCI', 2, 'FDIM', ('unlocks Plasma Fabricator (T3, single step)', 'libera o Plasma Fabricator (T3, um passo)', '解锁等离子制造机(T3,单步)')),
    ('REC', 2, 'GISS + GPCI', ('configurable battery and discount', 'bateria configurável e desconto', '可配置电池与折扣')),
    ('GEM', 2, 'GPCI', ('max factor += active upgrades', 'fator máximo += upgrades ativos', '最大系数 += 已激活升级数')),
    ('CTCDD', 2, 'GPCI + SA', ('parallel × 2', 'paralelo × 2', '并行 × 2')),
    ('QGPIU', 2, 'REC, CTCDD', ('unlocks Exoticizer', 'libera o Exoticizer', '解锁异化器')),
    ('SEFCP', 3, 'QGPIU', ('heat with base 1.12 / 1.18', 'calor com base 1,12 / 1,18', '热量底数改为 1.12 / 1.18')),
    ('TCT', 3, 'QGPIU', ('SA × 2 or × 3', 'SA × 2 ou × 3', 'SA × 2 或 × 3')),
    ('GGEBE', 3, 'QGPIU', ('overclock 4/2.3', 'overclock 4/2,3', '超频 4/2.3')),
    ('TPTP', 4, 'GGEBE', ('multi-step plasmas', 'plasmas de vários passos', '多步等离子体')),
    ('CNTI', 3, 'SEFCP', ('30,000 K cap', 'teto 30.000 K', '上限 30,000 K')),
    ('DOP', 4, 'CNTI', ('Power Forge gets Melting Core bonuses', 'Power Forge ganha os bônus do Melting Core', '能量锻炉获得融化核心的加成')),
    ('EPEC', 3, 'TCT', ('parallel $\\times (1 + \\text{heat}/15000)$ or $/25000$', 'paralelo $\\times (1 + \\text{calor}/15000)$ ou $/25000$', '并行 $\\times (1 + \\text{热量}/15000)$ 或 $/25000$')),
    ('IMKG', 3, 'GGEBE', ('battery-charge discount', 'desconto pela carga da bateria', '按电池充能折扣')),
    ('NDPE', 3, 'CNTI', ('compressed heat above 30,000 K', 'calor comprimido acima de 30.000 K', '30,000 K 以上热量压缩计算')),
    ('POS', 3, 'EPEC', ('parallel $\\times (1 + \\text{upgrades}/5)$ or $/8$', 'paralelo $\\times (1 + \\text{upgrades}/5)$ ou $/8$', '并行 $\\times (1 + \\text{升级数}/5)$ 或 $/8$')),
    ('DOR', 3, 'IMKG', ('$t \\div \\text{parallel}^{0.02}$', '$t \\div \\text{paralelo}^{0{,}02}$', '$t \\div \\text{并行}^{0.02}$')),
    ('NGMS', 4, 'NDPE, POS, DOR', ('voltage × 4 per ring', 'voltagem × 4 por anel', '每环电压 × 4')),
    ('SEDS', 5, 'NGMS', ('plasmas up to T5', 'plasmas até T5', '等离子体最高 T5')),
    ('PA', 6, 'SEDS', ('Exoticizer gets the bonuses (square root)', 'o Exoticizer recebe os bônus (raiz quadrada)', '异化器获得加成(平方根)')),
    ('CD', 7, 'PA', ('ring 2, +4 modules', 'anel 2, +4 módulos', '第二环,+4 模块')),
    ('TSE', 8, 'CD', ('removes the fuel cap', 'tira o teto do combustível', '解除燃料上限')),
    ('TBF', 9, 'TSE', ('free voltage per module', 'voltagem livre por módulo', '每个模块电压自由设定')),
    ('EE', 10, 'TBF', ('ring 3, +4 modules, magmatter', 'anel 3, +4 módulos, matéria mágica', '第三环,+4 模块,磁物质')),
    ('END', 12, 'EE', ('exotic plasmas, shard ejection', 'plasmas exóticos, ejeção de fragmentos', '奇异等离子体,碎片弹出')),
]
COSTS = [
    ('START', '64 frame Superconductor UIV Base, 32 Superconductor Composite, 16 Metastable Oganesson gear, 8 Eternal Singularity, 64 Robot Arm UIV, 64 Field Generator UEV'),
    ('FDIM', '16 Mega Alloy Blast Smelter, 64 Hypogen Coil, 32 Harmonic Phonon Conduit, 16 Eternal Singularity, 48 Field Restriction Coil T3, 64 Robot Arm UIV, 64 Field Generator UEV'),
    ('GPCI', '8 Stellar Energy Siphon, 8 Advanced Fusion, 64 Fusion Casing MK4, 64 Neutronium foil, 48 dense Quantum plate, 32 Rhugnor gear, 16 Eternal Singularity, 64 Robot Arm UIV, 64 Field Generator UEV'),
    ('QGPIU', '16 Stellar Energy Siphon, 2 Advanced Fusion, 64 Compressed Fusion Coil MK2, 16 Harmonic Phonon Conduit, 4 Transcendent Plasma Mixer, 64 Rhugnor gear, 64 Ichorium gear, 32 Eternal Singularity, 64 Robot Arm UIV, 64 Field Generator UEV'),
    ('CD', '64 frame SpaceTime, 64 frame Superconductor UMV Base, 64 frame Hypogen, 64 frame Dragon Metal, 64 Spatial Casing, 8 Boundary Casing, 2 Mega Battery, 32 Field Generator UXV'),
    ('EE', '64 frame White Dwarf Matter, 64 frame Black Dwarf Matter, 16 frame Eternity, 2 frame Universium, 64 Boundary Casing, 48 Stabilisation Field T5, 16 Mega Battery, 32 Exoticizer, 64 Siphon, 64 Field Generator UXV, 64 Robot Arm UXV'),
    ('END', '64 frame MHDCSM, 64 frame Eternity, 64 frame MagMatter, 64 Stabilisation Field T7, 64 Exoticizer, 4 Astral Array Fabricator, 32 Mega Battery, 64 Field Generator UXV, 64 Robot Arm UXV'),
]
LANG_INDEX = {'en': 0, 'pt': 1, 'zh': 2}


def forge_of_gods(lang):
    t = FOG[lang]; L = []
    a = L.append
    a(f'# {t["title"]}\n')
    a(f'![{t["title"]}](../../assets/gtnh/forge_of_the_gods.png){{ loading=lazy }}\n')
    a(f'<small>{t["credit"]}</small>\n')
    a(t['intro'] + '\n')
    a(table(['', ''], [(f'**{k}**', v) for k, v in t['facts']]))
    a(f'## {t["s_struct"]}\n\n{t["struct"]}\n')
    a(f'![{t["s_struct"]}](../../assets/machines/forge_of_gods.webp){{ loading=lazy }}\n')
    a(f'## {t["s_modules"]}\n')
    a(table(t['mod_head'], t['mods'])); a(t['slots'] + '\n')
    a(f'## {t["s_fuel"]}\n\n{t["fuel_txt"]}\n')
    a(t['fuel_formula'])
    a(table(t['fuel_head'], [(f, n(heat(f), lang), n(math.floor(startup(f)), lang), n(fuel_residue(f), lang), n(fuel_residue(f, True), lang),
                              n(fuel_plasma(f), lang), n(f / 25, lang)) for f in (1, 2, 3, 4, 5, 6, 10, 20, 43, 70)]))
    a(t['caps'] + '\n')
    a(f'## {t["s_heat"]}\n\n{t["heat_txt"]}\n')
    a(f'## {t["s_par"]}\n\n{t["par_txt"]}')
    a(table(t['par_head'], [(f, eff_factor(f), n(1 + eff_factor(f) / 15, lang), n((1 + eff_factor(f) / 15) * 3, lang)) for f in (5, 15, 43, 70, 181, 1000)]))
    a(t['par_note'] + '\n')
    a(f'## {t["s_speed"]}\n\n{t["speed_txt"]}')
    a(f'## {t["s_ms"]}\n\n{t["ms_txt"]}\n')
    a(table(t['ms_head'], [(k, n(POWER_C * 9 ** (k - 1), lang), n(RECIPE_C * 4 ** (k - 1), lang), n(FUEL_C * 3 ** (k - 1), lang), k) for k in range(1, 8)]))
    a(f'## {t["s_up"]}\n\n{t["up_txt"]}\n')
    a(table(t['up_head'], [(u[0], u[1], u[2], u[3][LANG_INDEX[lang]]) for u in UPGRADES]))
    a(f'### {t["s_tree"]}\n\n![{t["s_tree"]}](../../assets/gtnh/godforge_upgrade_tree.png){{ loading=lazy width=360 }}\n\n<small>{t["credit"]}</small>\n')
    a(f'## {t["s_cost"]}\n')
    a(table(['Tag', t['mat']], COSTS)); a(t['cost_note'] + '\n')
    a(f'## {t["s_diff"]}\n'); a('\n'.join('- ' + d for d in t['diffs']) + '\n')
    a(f'## {t["s_credits"]}\n\n{t["credits"]}\n')
    return '\n'.join(L)


# Eye of Harmony (api/machine/feature/eyeofharmony/EyeOfHarmonyMath.java, GT5U a3e1e112)
PLANETS = [(('Overworld, Nether, End', 'Overworld, Nether, End', '主世界、下界、末地'), 0), (('Moon', 'Lua', '月球'), 1), (('Mars', 'Marte', '火星'), 2),
           (('Venus, Mercury', 'Vênus, Mercúrio', '金星、水星'), 4), (('Glacio', 'Glacio', 'Glacio'), 5)]

EOH = {
    'en': dict(
        title='Eye of Harmony',
        intro='The Eye of Harmony simulates a miniature universe and extracts the ores of a whole planet. Each run is expensive, slow and may fail; this page shows every calculation the controller makes.',
        energy='Energy', source='Origin', src_v='port of GT5-Unofficial a3e1e112', wireless='wireless (Nexus network)',
        s_prog='Planetary programs',
        prog='The planet item in the controller slot picks the program. Products come from the GTCEu ore veins registered in that dimension. '
             'Packs add planets through KubeJS (`GTNAStartupEvents.eyeOfHarmony`). Planets beyond the Minecraft dimensions need Ad Astra.',
        prog_code='\\begin{aligned}\n\\text{base duration} &= 18000\\ \\text{s} \\cdot 1.4^{\\text{tier}} \\\\\n\\text{each gas (H and He)} &= 10^{9} \\cdot (\\text{tier} + 1)\\ \\text{mB} \\\\\n\\text{base chance} &= 1 - 0.05 \\cdot \\text{tier} \\\\\n\\text{return} &= \\text{cost} \\cdot (0.6 + \\text{tier}/10) \\\\\n\\text{cost} &= \\text{plasmas} + \\text{ticks} \\cdot (2^{19} + 10^{11})\\ \\text{EU}\n\\end{aligned}',
        prog_head=['Planet', 'Tier', 'Base duration', 'H and He (mB)', 'Base chance', 'Cost without plasmas (EU)'],
        s_fields='Fields and circuit',
        fields='Three fields of tier 0 to 8 (compression $c$, acceleration $a$, stabilisation $s$) and a circuit $k$ from 0 to 24:',
        fields_code='\\begin{aligned}\n\\text{duration} &= \\max\\!\\left(T \\cdot 2^{-a} \\cdot 0.97^{\\,c - r} \\cdot 2^{-k},\\ 1\\right) && r = \\text{program minimum compression} \\\\\n\\text{startup cost} &= \\text{cost} \\cdot 4^{k} \\\\\n\\text{return} &= \\text{base return} \\cdot \\left(1 - (8 - s) \\cdot 0.05\\right) && \\text{does not scale with the circuit} \\\\\n\\text{chance} &= \\text{base chance} - 0.0925\\,a + 0.05\\,s - \\text{gas penalties} \\\\\n\\text{yield} &= 1 - 0.05\\,s - \\text{gas penalties} \\\\\n\\text{gas penalty} &= 1 - \\exp\\!\\left(-\\left(30 \\cdot \\left(\\tfrac{\\text{stored}}{\\text{required}} - 1\\right)\\right)^{2}\\right)\n\\end{aligned}',
        fields_head=['a / s', 'Chance (Overworld)', 'Yield', 'Time'],
        excess='Excess gas also reduces chance and yield: storing 10% more already costs {p}% per gas. Deliver the exact amount.',
        s_fail='Failure and pity',
        fail=['A failure still returns the EU and produces SpaceTime: $\\text{chance} \\cdot 14400 \\cdot 2^{\\text{tier} + 1}$ mB.',
              'Consecutive failures **under the same conditions** build pity: $(1 - \\text{chance}) \\cdot \\text{chance}$ per failure. Changing fields or circuit resets it.',
              'The result is rolled at startup and saved: breaking the controller or reloading the world does not change it.'],
        s_tips='Tips',
        tips=['The controller consumes **all** stored hydrogen and helium at startup, excess included.',
              'The return arrives through the Nexus network in parts; network loss is shown separately in the GUI.',
              'A full output never loses anything: the cycle waits.']),
    'pt': dict(
        title='Olho da Harmonia',
        intro='O Olho da Harmonia simula um universo em miniatura e extrai os minérios de um planeta inteiro. Cada operação é cara, demorada e pode falhar; esta página mostra todas as contas que o controlador faz.',
        energy='Energia', source='Origem', src_v='port do GT5-Unofficial a3e1e112', wireless='sem fio (rede Nexus)',
        s_prog='Programas planetários',
        prog='O item de planeta no slot do controlador escolhe o programa. Os produtos vêm dos veios de minério do GTCEu registrados naquela dimensão. '
             'Packs adicionam planetas pelo KubeJS (`GTNAStartupEvents.eyeOfHarmony`). Planetas além das dimensões do Minecraft precisam do Ad Astra.',
        prog_code='\\begin{aligned}\n\\text{duração base} &= 18000\\ \\text{s} \\cdot 1{,}4^{\\text{tier}} \\\\\n\\text{gás de cada (H e He)} &= 10^{9} \\cdot (\\text{tier} + 1)\\ \\text{mB} \\\\\n\\text{chance base} &= 1 - 0{,}05 \\cdot \\text{tier} \\\\\n\\text{retorno} &= \\text{custo} \\cdot (0{,}6 + \\text{tier}/10) \\\\\n\\text{custo} &= \\text{plasmas} + \\text{ticks} \\cdot (2^{19} + 10^{11})\\ \\text{EU}\n\\end{aligned}',
        prog_head=['Planeta', 'Tier', 'Duração base', 'H e He (mB)', 'Chance base', 'Custo sem plasmas (EU)'],
        s_fields='Campos e circuito',
        fields='Três campos de tier 0 a 8 (compressão $c$, aceleração $a$, estabilização $s$) e um circuito $k$ de 0 a 24:',
        fields_code='\\begin{aligned}\n\\text{duração} &= \\max\\!\\left(T \\cdot 2^{-a} \\cdot 0{,}97^{\\,c - r} \\cdot 2^{-k},\\ 1\\right) && r = \\text{compressão mínima do programa} \\\\\n\\text{custo de partida} &= \\text{custo} \\cdot 4^{k} \\\\\n\\text{retorno} &= \\text{retorno base} \\cdot \\left(1 - (8 - s) \\cdot 0{,}05\\right) && \\text{não sobe com o circuito} \\\\\n\\text{chance} &= \\text{chance base} - 0{,}0925\\,a + 0{,}05\\,s - \\text{penalidades de gás} \\\\\n\\text{rendimento} &= 1 - 0{,}05\\,s - \\text{penalidades de gás} \\\\\n\\text{penalidade de gás} &= 1 - \\exp\\!\\left(-\\left(30 \\cdot \\left(\\tfrac{\\text{guardado}}{\\text{necessário}} - 1\\right)\\right)^{2}\\right)\n\\end{aligned}',
        fields_head=['a / s', 'Chance (Overworld)', 'Rendimento', 'Tempo'],
        excess='O gás em excesso também reduz chance e rendimento: guardar 10% a mais já custa {p}% em cada gás. Entregue a quantidade exata.',
        s_fail='Falha e pity',
        fail=['A falha também devolve o EU de retorno e gera SpaceTime: $\\text{chance} \\cdot 14400 \\cdot 2^{\\text{tier} + 1}$ mB.',
              'Falhas seguidas **nas mesmas condições** acumulam pity: soma $(1 - \\text{chance}) \\cdot \\text{chance}$ a cada falha. Mudar campos ou circuito zera.',
              'O resultado é sorteado na partida e salvo: quebrar o controlador ou recarregar o mundo não muda o resultado.'],
        s_tips='Dicas',
        tips=['O controlador consome **todo** o hidrogênio e o hélio guardados na partida, inclusive o excesso.',
              'O retorno chega pela rede Nexus em parcelas; a perda da rede aparece separada na GUI.',
              'Saída cheia não perde nada: o ciclo espera.']),
    'zh': dict(
        title='鸿蒙之眼',
        intro='鸿蒙之眼模拟一个微型宇宙,提取整颗星球的矿物。每次运行都昂贵、漫长并且可能失败;本页列出控制器的全部计算。',
        energy='能量', source='来源', src_v='移植自 GT5-Unofficial a3e1e112', wireless='无线(Nexus 网络)',
        s_prog='星球程序',
        prog='控制器槽位中的星球物品决定程序。产物来自该维度中注册的 GTCEu 矿脉。'
             '整合包可通过 KubeJS(`GTNAStartupEvents.eyeOfHarmony`)添加星球。Minecraft 原版维度以外的星球需要 Ad Astra。',
        prog_code='\\begin{aligned}\n\\text{基础时长} &= 18000\\ \\text{秒} \\cdot 1.4^{\\text{等级}} \\\\\n\\text{每种气体（H 与 He）} &= 10^{9} \\cdot (\\text{等级} + 1)\\ \\text{mB} \\\\\n\\text{基础成功率} &= 1 - 0.05 \\cdot \\text{等级} \\\\\n\\text{返还} &= \\text{花费} \\cdot (0.6 + \\text{等级}/10) \\\\\n\\text{花费} &= \\text{等离子体} + \\text{刻数} \\cdot (2^{19} + 10^{11})\\ \\text{EU}\n\\end{aligned}',
        prog_head=['星球', '等级', '基础时长', 'H 与 He (mB)', '基础成功率', '不含等离子体的花费 (EU)'],
        s_fields='力场与电路',
        fields='三个 0 至 8 级的力场(压缩 $c$、加速 $a$、稳定 $s$)以及 0 至 24 的电路 $k$:',
        fields_code='\\begin{aligned}\n\\text{时长} &= \\max\\!\\left(T \\cdot 2^{-a} \\cdot 0.97^{\\,c - r} \\cdot 2^{-k},\\ 1\\right) && r = \\text{程序的最低压缩} \\\\\n\\text{启动花费} &= \\text{花费} \\cdot 4^{k} \\\\\n\\text{返还} &= \\text{基础返还} \\cdot \\left(1 - (8 - s) \\cdot 0.05\\right) && \\text{不随电路增长} \\\\\n\\text{成功率} &= \\text{基础成功率} - 0.0925\\,a + 0.05\\,s - \\text{气体惩罚} \\\\\n\\text{产量} &= 1 - 0.05\\,s - \\text{气体惩罚} \\\\\n\\text{气体惩罚} &= 1 - \\exp\\!\\left(-\\left(30 \\cdot \\left(\\tfrac{\\text{储存}}{\\text{所需}} - 1\\right)\\right)^{2}\\right)\n\\end{aligned}',
        fields_head=['a / s', '成功率(主世界)', '产量', '时间'],
        excess='多余的气体同样会降低成功率和产量:多存 10% 就会让每种气体损失 {p}%。请提供精确的数量。',
        s_fail='失败与保底',
        fail=['失败时仍会返还 EU 并产出时空:$\\text{成功率} \\cdot 14400 \\cdot 2^{\\text{等级} + 1}$ mB。',
              '在**相同条件**下连续失败会累积保底:每次失败增加 $(1 - \\text{成功率}) \\cdot \\text{成功率}$。改变力场或电路会清零。',
              '结果在启动时抽取并保存:拆掉控制器或重新加载世界都不会改变结果。'],
        s_tips='提示',
        tips=['启动时控制器会消耗**全部**储存的氢和氦,包括多余部分。',
              '返还通过 Nexus 网络分批到达;网络损耗在界面中单独显示。',
              '输出满时不会损失任何东西:循环会等待。']),
}


def eoh_seconds(t):
    r, b, e = 1.0, 1.4, t
    while e > 0:
        if e & 1: r *= b
        b *= b; e >>= 1
    return int(18000 * r)


def eye_of_harmony(lang):
    t = EOH[lang]; i = LANG_INDEX[lang]; L = []; a = L.append
    hour = {'en': 'h', 'pt': 'h', 'zh': '小时'}[lang]
    a(f'# {t["title"]}\n')
    a(f'![{t["title"]}](../../assets/machines/eye_of_harmony.webp){{ loading=lazy }}\n')
    a(t['intro'] + '\n')
    a(table(['', ''], [('**Tier**', 'UXV'), (f'**{t["energy"]}**', t['wireless']), (f'**{t["source"]}**', t['src_v'])]))
    a(f'## {t["s_prog"]}\n\n{t["prog"]}\n')
    a('$$\n' + t['prog_code'] + '\n$$\n')
    a(table(t['prog_head'], [(p[i], tier, f'{n(eoh_seconds(tier) / 3600, lang)} {hour}', n(1e9 * (tier + 1), lang), f'{n(100 - 5 * tier, lang)}%',
                              n(eoh_seconds(tier) * 20 * (2 ** 19 + 1e11), lang)) for p, tier in PLANETS]))
    a(f'## {t["s_fields"]}\n\n{t["fields"]}\n')
    a('$$\n' + t['fields_code'] + '\n$$\n')
    a(table(t['fields_head'], [(f'{x} / {y}', f'{n(max(0, min(1, 1 - 0.0925 * x + 0.05 * y)) * 100, lang)}%', f'{n((1 - 0.05 * y) * 100, lang)}%', f'÷{2 ** x}')
                               for x, y in ((0, 0), (2, 2), (4, 4), (6, 6), (8, 8), (8, 0), (0, 8))]))
    a(t['excess'].format(p=n((1 - math.exp(-(30 * 0.1) ** 2)) * 100, lang)) + '\n')
    a(f'## {t["s_fail"]}\n\n' + ''.join(f'- {x}\n' for x in t['fail']))
    a(f'## {t["s_tips"]}\n\n' + ''.join(f'- {x}\n' for x in t['tips']))
    return '\n'.join(L)


def main():
    os.makedirs(OUT, exist_ok=True)
    for lang, suffix in LANGS:
        for name, build in (('forge-of-gods', forge_of_gods), ('eye-of-harmony', eye_of_harmony)):
            md = build(lang)
            open(os.path.join(OUT, name + suffix), 'w', encoding='utf-8').write(zh_punct.fix(md) if lang == 'zh' else md)
    print('forge-of-gods eye-of-harmony')


if __name__ == '__main__':
    main()
