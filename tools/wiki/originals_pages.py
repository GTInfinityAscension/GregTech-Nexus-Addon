"""Wiki pages of the four original multiblocks, from the code and the in-game field manual.

    python3 tools/wiki/originals_pages.py
        -> docs/gameplay/machines/originals/{kinetic-orbital-lance,dimensional-rift-gate,
           antimatter-collider-ring,stellar-containment-chamber}{.md,.pt.md,.zh.md}

Text: the field manual keys gtna.originals.info.<machine>.* in the three lang files (already translated).
Numbers: constants copied from api/machine/feature/{lance,rift,collider,stellar}/*Core.java and the machine classes;
update them here when the code changes. Formulas are LaTeX (MathJax, see mkdocs.yml).
Screens: docs/assets/originals/<machine>_<panel>_<lang>.webp, taken in a dev client driven by gtna_dev_commands.txt
(client/debug/DevCommandFile) and cropped by tools/wiki/originals_screens.py.
"""
import json
import math
import os
import sys
import zipfile
import glob

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import zh_punct  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
OUT = os.path.join(ROOT, 'docs/gameplay/machines/originals')
LANGS = (('en', 0, '.md'), ('pt', 1, '.pt.md'), ('zh', 2, '.zh.md'))
IMG = '../../../assets/originals/'


def load_lang():
    files = {'en': 'src/generated/resources/assets/gtna/lang/en_us.json',
             'pt': 'src/main/resources/assets/gtna/lang/pt_br.json',
             'zh': 'src/main/resources/assets/gtna/lang/zh_cn.json'}
    out = {k: json.load(open(os.path.join(ROOT, v), encoding='utf-8')) for k, v in files.items()}
    # GTCEu material names (en, zh) from the GTCEu jar in the Gradle cache; Portuguese is in PT_MAT below.
    jars = glob.glob(os.path.expanduser('~/.gradle/caches/modules-2/files-2.1/com.gregtechceu.gtceu/gtceu-1.20.1/*/*/gtceu-*-slim.jar'))
    gt = {'en': {}, 'zh': {}}
    if jars:
        with zipfile.ZipFile(sorted(jars)[-1]) as z:
            gt['en'] = json.loads(z.read('assets/gtceu/lang/en_us.json'))
            gt['zh'] = json.loads(z.read('assets/gtceu/lang/zh_cn.json'))
    return out, gt


LANG, GT = load_lang()

PT_MAT = {
    'iron': 'Ferro', 'titanium': 'Titânio', 'aluminium': 'Alumínio', 'helium_3': 'Hélio-3', 'carbon': 'Carbono',
    'nickel': 'Níquel', 'magnesium': 'Magnésio', 'chromium': 'Cromo', 'platinum': 'Platina', 'sodium': 'Sódio',
    'ammonia': 'Amônia', 'iridium': 'Irídio', 'osmium': 'Ósmio', 'gold': 'Ouro', 'sulfur': 'Enxofre',
    'deuterium': 'Deutério', 'nitrogen': 'Nitrogênio', 'methane': 'Metano', 'naquadah': 'Naquadah',
    'neutronium': 'Neutrônio', 'certus_quartz': 'Quartzo Certus', 'silicon': 'Silício', 'thallium': 'Tálio',
    'cinnabar': 'Cinábrio', 'tungsten': 'Tungstênio', 'wood': 'Madeira', 'phosphorus': 'Fósforo',
    'naquadah_enriched': 'Naquadah Enriquecida', 'naquadria': 'Naquádria', 'trinium': 'Trínio',
    'duranium': 'Durânio', 'naquadah_alloy': 'Liga de Naquadah',
}


def mat(mid, lang, ns='gtceu'):
    if ns == 'gtna':
        return LANG[lang].get('material.gtna.' + mid) or LANG['en'].get('material.gtna.' + mid, mid)
    if lang == 'pt':
        return PT_MAT.get(mid, GT['en'].get('material.gtceu.' + mid, mid))
    return GT[lang].get('material.gtceu.' + mid) or mid.replace('_', ' ').title()


def tr(lang, key):
    return LANG[lang].get(key) or LANG['en'].get(key, key)


def T(lang, en, pt, zh):
    return {'en': en, 'pt': pt, 'zh': zh}[lang]


def num(x, lang, digits=3):
    """Plain number, Portuguese separators in pt."""
    if x == 0: return '0'
    if abs(x) >= 1e6 or abs(x) < 1e-2:
        return sci(x, lang, digits)
    s = f'{x:,.0f}' if abs(x - round(x)) < 1e-9 or abs(x) >= 1000 else f'{x:,.{digits - 1}f}'.rstrip('0').rstrip('.')
    return s.replace(',', 'X').replace('.', ',').replace('X', '.') if lang == 'pt' else s


def sci(x, lang, digits=3):
    """Scientific notation in LaTeX: $4.00 \\times 10^{12}$."""
    if x == 0: return '$0$'
    e = int(math.floor(math.log10(abs(x))))
    m = x / 10 ** e
    ms = f'{m:.{digits - 1}f}'
    if lang == 'pt': ms = ms.replace('.', '{,}')
    return f'${ms} \\times 10^{{{e}}}$' if e else f'${ms}$'


def table(head, rows):
    return '\n'.join(['| ' + ' | '.join(head) + ' |', '|' + '|'.join('---' for _ in head) + '|'] +
                     ['| ' + ' | '.join(str(c) for c in r) + ' |' for r in rows]) + '\n'


def manual(lang, machine, section, skip=()):
    """Paragraphs of one field manual chapter, minus the lines replaced by LaTeX."""
    k = f'gtna.originals.info.{machine}.{section}'
    out = []
    for i in range(1, 9):
        if i in skip or (k + f'.{i}') not in LANG['en']: continue
        out.append(tr(lang, k + f'.{i}'))
    return '\n\n'.join(out) + '\n'


def heading(lang, machine, section, level='##'):
    return f'{level} {tr(lang, f"gtna.originals.info.{machine}.{section}")}\n'


def screens(lang, machine, panels):
    cap = {'main': T(lang, 'Main screen', 'Tela principal', '主界面'),
           'orbit': T(lang, 'Orbital map', 'Mapa orbital', '轨道图'),
           'bench': T(lang, 'Barrel bench', 'Bancada do cano', '炮管工作台'),
           'chord': T(lang, 'Chord and harmonics', 'Acorde e harmônicos', '和弦与谐波'),
           'atlas': T(lang, 'Atlas', 'Atlas', '星图'),
           'model': T(lang, 'Standard Model board', 'Quadro do Modelo Padrão', '标准模型面板'),
           'board': T(lang, 'Committee', 'Comitê', '委员会'),
           'mp': T(lang, 'Mass–period diagram', 'Diagrama massa–período', '质量-周期图'),
           'quakes': T(lang, 'Seismogram', 'Sismograma', '地震图'),
           'manual': T(lang, 'Field manual', 'Manual de campo', '现场手册')}
    tag = {'en': 'en', 'pt': 'pt', 'zh': 'zh'}[lang]
    # Only screens that were captured (tools/wiki/originals_screens.py); none means no section.
    have = lambda p: os.path.exists(os.path.join(ROOT, 'docs/assets/originals', f'{machine}_{p}_{tag}.webp'))
    if not have('main'): return ''
    panels = [p for p in panels if have(p)]
    L = [f'## {T(lang, "Screens", "Telas", "界面")}\n']
    L.append(T(lang, 'In-game screens of the current version, in English.', 'Telas do jogo na versão atual, em português.',
               '当前版本的游戏界面（简体中文）。') + '\n')
    L.append('=== "' + cap['main'] + '"\n\n    ![' + cap['main'] + '](' + IMG + f'{machine}_main_{tag}.webp){{ loading=lazy }}\n')
    for p in panels:
        L.append(f'=== "{cap[p]}"\n\n    ![{cap[p]}]({IMG}{machine}_{p}_{tag}.webp){{ loading=lazy }}\n')
    return '\n'.join(L)


def facts(lang, rows):
    return table(['', ''], [(f'**{k}**', v) for k, v in rows])


def issues(lang, items):
    title = T(lang, 'Known issues', 'Problemas conhecidos', '已知问题')
    L = [f'!!! bug "{title}"\n']
    for x in items: L.append(f'    - {x}')
    L.append('\n    ' + T(lang, 'Report anything else on the [issue tracker](https://github.com/GTInfinityAscension/GregTech-Nexus-Addon/issues).',
                         'Outros problemas: [issue tracker](https://github.com/GTInfinityAscension/GregTech-Nexus-Addon/issues).',
                         '其他问题请提交到 [issue tracker](https://github.com/GTInfinityAscension/GregTech-Nexus-Addon/issues)。') + '\n')
    return '\n'.join(L)


def hatches(lang, rows):
    head = [T(lang, 'Hatch', 'Hatch', '仓室'), T(lang, 'Max', 'Máx.', '上限'), T(lang, 'Use', 'Uso', '用途')]
    return table(head, rows)


# ====================================================================== Kinetic Orbital Lance
BODIES = [  # id, distance Mm, hardness MJ/kg, survey mass kg, parents, materials
    ('moon', 384, 2.0, 1e6, [], [('iron', 'gtceu'), ('titanium', 'gtceu'), ('aluminium', 'gtceu'), ('helium_3', 'gtceu')]),
    ('phobos', 78, 1.2, 2e6, ['moon'], [('carbon', 'gtceu'), ('nickel', 'gtceu'), ('iron', 'gtceu')]),
    ('vesta', 1.7e5, 3.5, 8e6, ['phobos'], [('iron', 'gtceu'), ('magnesium', 'gtceu'), ('chromium', 'gtceu'), ('platinum', 'gtceu')]),
    ('ceres', 4.1e5, 1.5, 8e6, ['phobos'], [('magnesium', 'gtceu'), ('sodium', 'gtceu'), ('ammonia', 'gtceu')]),
    ('psyche', 3.7e5, 6.0, 5e7, ['vesta'], [('iron', 'gtceu'), ('nickel', 'gtceu'), ('iridium', 'gtceu'), ('osmium', 'gtceu'), ('gold', 'gtceu')]),
    ('europa', 6.3e5, 2.8, 5e7, ['ceres'], [('magnesium', 'gtceu'), ('sulfur', 'gtceu'), ('deuterium', 'gtceu')]),
    ('arrokoth', 6.6e6, 0.9, 2e8, ['europa'], [('primordial_tholin', 'gtna'), ('nitrogen', 'gtceu'), ('methane', 'gtceu'), ('carbon', 'gtceu')]),
    ('nexus_1', 7.5e6, 9.5, 1e9, ['psyche', 'arrokoth'], [('nexium', 'gtna'), ('naquadah', 'gtceu'), ('neutronium', 'gtceu'), ('space_time', 'gtna')]),
]
PROJECTILES = [('naquadah_alloy', 'gtceu', 50), ('trinium', 'gtceu', 80), ('neutronium', 'gtceu', 400),
               ('cosmic_neutronium', 'gtna', 800), ('white_dwarf_matter', 'gtna', 1200), ('magnetarium', 'gtna', 2000)]
COMPONENTS = [  # id, slot, value, mass t, heat, unlocked by
    ('rail_cu_nb', 'rail', 0.02, 40, 3, None), ('rail_superconductor', 'rail', 0.04, 60, 1, 'phobos'),
    ('rail_graphene', 'rail', 0.07, 140, 2, 'psyche'), ('cooling_helium', 'cooling', 2, 30, -10, 'ceres'),
    ('cooling_superconductor', 'cooling', 4, 60, -25, 'europa'), ('cooling_plasma_ice', 'cooling', 8, 90, -60, 'arrokoth'),
    ('sensor_telescope', 'sensor', 0.7, 10, 2, 'moon'), ('sensor_interferometer', 'sensor', 0.35, 40, 2, 'europa'),
    ('sensor_lens', 'sensor', 0.175, 80, 2, 'arrokoth'), ('capsule_ablative', 'capsule', 0.75, 0, 0, 'ceres'),
    ('capsule_magnetic', 'capsule', 0.85, 0, 0, 'psyche'), ('capsule_fold', 'capsule', 0.95, 0, 0, 'nexus_1'),
    ('salvo_splitter', 'salvo', 2, 50, 5, 'vesta'),
]
BANK = 4e12            # LanceCore.bankCapacity() with one capacitor ring
CHARGE_EUT = 2 ** 36   # LanceMachine.CHARGE_PER_SECOND / 20
AIM_CWU = 16000        # LanceMachine.AIM_CWUT
COOL_EU_S = 2 ** 34 * 20


def body(lang, b):
    return tr(lang, f'gtna.machine.kinetic_orbital_lance.body.{b}')


def lance(lang):
    m = 'kinetic_orbital_lance'
    L = [f'# {tr(lang, "block.gtna." + m)}\n']
    L.append(f'![{tr(lang, "block.gtna." + m)}](../../../assets/machines/{m}.webp){{ loading=lazy }}\n')
    L.append(manual(lang, m, 'overview'))
    L.append(facts(lang, [
        ('Tier', 'UEV'),
        (T(lang, 'Size', 'Tamanho', '尺寸'), '242 × 130 × 142'),
        (T(lang, 'Energy', 'Energia', '能量'), T(lang, "owner's Nexus network, up to $2^{36}$ EU/t into the bank",
                                                   'rede Nexus do dono, até $2^{36}$ EU/t para o banco', '所有者的 Nexus 网络，最高 $2^{36}$ EU/t 充入电容组')),
        (T(lang, 'Computation', 'Computação', '算力'), T(lang, f'up to {num(AIM_CWU, lang)} CWU/t (aim)', f'até {num(AIM_CWU, lang)} CWU/t (mira)', f'最多 {AIM_CWU} CWU/t（瞄准）')),
        (T(lang, 'Controller', 'Controlador', '控制器'), T(lang, 'Assembly Line (UEV), research on the UEV Electric Piston',
                                                         'Linha de Montagem (UEV), pesquisa no Pistão Elétrico UEV', '装配线（UEV），研究 UEV 电动活塞')),
        (T(lang, 'Blocks', 'Blocos', '方块'), f'[{T(lang, "catalog page", "página do catálogo", "图鉴页面")}](../catalog/{m}.md)'),
    ]))
    L.append(heading(lang, m, 'build'))
    L.append(hatches(lang, [
        (T(lang, 'Input Bus', 'Barramento de Entrada', '输入总线'), 4, T(lang, 'projectile ingots', 'lingotes de projétil', '弹丸锭')),
        (T(lang, 'Output Bus', 'Barramento de Saída', '输出总线'), 4, T(lang, 'dusts from the capsules', 'pós das cápsulas', '返回舱的粉')),
        (T(lang, 'Computation Data Reception Hatch', 'Hatch de Recepção de Dados de Computação', '计算数据接收仓'), 1, T(lang, 'aim (without it the aim is blind)', 'mira (sem ele a mira fica cega)', '瞄准（没有时为盲射）')),
        (tr(lang, 'block.gtna.liner_hatch'), 1, T(lang, 'spare liners, swapped in automatically', 'revestimentos reserva, trocados sozinhos', '备用内衬，自动更换')),
        (tr(lang, 'block.gtna.target_cartridge_hatch'), 1, T(lang, 'up to 8 target cartridges, one per shot in turn', 'até 8 cartuchos de alvo, um por tiro em rodízio', '最多 8 个目标弹匣，每次射击轮换')),
    ]))
    L.append(manual(lang, m, 'build', skip=(1,)))

    # Bank and the shot
    L.append(heading(lang, m, 'power'))
    L.append(T(lang, 'The bank charges from the Nexus network at up to $2^{36}$ EU/t. With auto-fire on, the Lance fires the whole bank as soon as it is full, the target can be aimed at and an input bus holds a projectile that can break that body.',
               'O banco carrega pela rede Nexus a até $2^{36}$ EU/t. Com o disparo automático ligado, a Lança descarrega o banco inteiro assim que ele enche, se o alvo puder ser mirado e houver no barramento um projétil capaz de quebrar aquele corpo.',
               '电容组通过 Nexus 网络以最高 $2^{36}$ EU/t 充能。开启自动射击后，只要电容组充满、目标可瞄准、输入总线中有能击穿该天体的弹丸，长矛就会一次释放整个电容组。') + '\n')
    L.append(r"""$$
\begin{aligned}
E &= 4 \times 10^{12}\ \text{EU} \\
\eta &= \min\!\left(0.85,\ 0.35 + \textstyle\sum \Delta\eta_{\text{rail}} \cdot \left(1 - 0.5\,\tfrac{n_{\text{rail}}}{8}\right)\right) \\
M_{\text{frag}} &= \frac{0.2\,\eta\,E \cdot 1000\ \text{J/EU}}{H} \\
M_{\text{rec}} &= M_{\text{frag}} \cdot r \cdot A
\end{aligned}
$$
""".replace('0.85', T(lang, '0.85', '0{,}85', '0.85')).replace('0.35', T(lang, '0.35', '0{,}35', '0.35')).replace('0.5\\,', T(lang, '0.5\\,', '0{,}5\\,', '0.5\\,')).replace('0.2\\,', T(lang, '0.2\\,', '0{,}2\\,', '0.2\\,')))
    L.append(T(lang, '$H$ is the body hardness (J/kg), $r$ the capsule recovery (0.6 without a capsule component) and $A$ the accuracy (next section). The capsule lands after $t = 30\\ \\text{s} \\cdot \\ln(1 + d / 50\\ \\text{Mm})$ and unloads **one dust per 100 t**, split evenly over the body\'s materials. A capsule that does not fit waits in the queue.',
               '$H$ é a dureza do corpo (J/kg), $r$ a recuperação da cápsula (0,6 sem componente de cápsula) e $A$ a precisão (próxima seção). A cápsula pousa depois de $t = 30\\ \\text{s} \\cdot \\ln(1 + d / 50\\ \\text{Mm})$ e descarrega **um pó a cada 100 t**, dividido por igual entre os materiais do corpo. Cápsula que não cabe espera na fila.',
               '$H$ 为天体硬度（J/kg），$r$ 为返回舱回收率（无返回舱部件时为 0.6），$A$ 为精度（见下一节）。返回舱在 $t = 30\\ \\text{s} \\cdot \\ln(1 + d / 50\\ \\text{Mm})$ 后着陆，**每 100 t 卸下一份粉**，平均分配给该天体的各种材料。放不下的返回舱会排队等待。') + '\n')
    L.append(T(lang, 'Projectiles are ingots. The type only decides which body can be hit: **Nexus-1 only breaks under Magnetarium**, every projectile works on the other bodies.',
               'Os projéteis são lingotes. O tipo só decide qual corpo pode ser atingido: **Nexus-1 só quebra com Magnetário**; qualquer projétil serve para os outros corpos.',
               '弹丸为锭。弹丸种类只决定能命中哪些天体：**Nexus-1 只能被磁星合金击穿**，其他天体任何弹丸都可以。') + '\n')
    L.append(table([T(lang, 'Projectile (ingot)', 'Projétil (lingote)', '弹丸（锭）'), T(lang, 'Mass (kg)', 'Massa (kg)', '质量 (kg)'),
                    T(lang, 'Breaks Nexus-1', 'Quebra Nexus-1', '可击穿 Nexus-1')],
                   [(mat(p, lang, ns), num(kg, lang), '✅' if p == 'magnetarium' else '—') for p, ns, kg in PROJECTILES]))

    # Targets
    L.append(heading(lang, m, 'targets'))
    L.append(manual(lang, m, 'targets'))
    L.append(r"""$$
\begin{aligned}
S &= 1 - e^{-M / M_{\text{car}}} && \text{%s} \\
\theta &= \frac{10^{-9}\,u}{\sqrt{\text{CWU/t} / 1000}} + 2 \times 10^{-10} \cdot \frac{\max(0,\ T - 300)}{100} \\
A &= \max\!\left(0,\ 1 - \frac{d\,\theta}{5000\ \text{m}}\right)
\end{aligned}
$$
""" % T(lang, 'survey, 99\\% counts as complete', 'levantamento; 99\\% conta como completo', '勘测度，99\\% 视为完成'))
    L.append(T(lang, '$M$ is the mass recovered from the body, $u$ the aim factor of the sensor (1 without one), $T$ the barrel temperature (K) and $d$ the distance. The Lance asks the computation hatch for 16,000 CWU/t at most.',
               '$M$ é a massa recuperada do corpo, $u$ o fator de mira do sensor (1 sem sensor), $T$ a temperatura do cano (K) e $d$ a distância. A Lança pede no máximo 16.000 CWU/t ao hatch de computação.',
               '$M$ 为从该天体回收的质量，$u$ 为传感器的瞄准系数（无传感器时为 1），$T$ 为炮管温度（K），$d$ 为距离。长矛最多向算力仓请求 16,000 CWU/t。') + '\n')
    rows = []
    for b, d, h, mc, parents, mats in BODIES:
        frag = 0.2 * 0.35 * BANK * 1000 / (h * 1e6)
        acc = max(0, 1 - d * 1e6 * (1e-9 / math.sqrt(AIM_CWU / 1000)) / 5000)
        rec = frag * 0.6 * acc
        shots = '—' if rec <= 0 else num(math.ceil(mc * math.log(100) / rec), lang)
        rows.append((body(lang, b), num(d, lang), num(h, lang), sci(mc, lang), f'{round(30 * math.log(1 + d / 50))} s',
                     ', '.join(body(lang, p) for p in parents) or '—', ', '.join(mat(x, lang, ns) for x, ns in mats),
                     num(acc, lang), shots))
    L.append(table([T(lang, 'Body', 'Corpo', '天体'), T(lang, 'Distance (Mm)', 'Distância (Mm)', '距离 (Mm)'), 'H (MJ/kg)', '$M_{car}$ (kg)',
                    T(lang, 'Capsule', 'Cápsula', '返回舱'), T(lang, 'Needs 100% of', 'Precisa de 100% em', '前置（100%）'),
                    T(lang, 'Materials', 'Materiais', '材料'), T(lang, 'Accuracy*', 'Precisão*', '精度*'), T(lang, 'Shots to 100%*', 'Tiros até 100%*', '勘测满所需射击数*')], rows))
    L.append(T(lang, '\\* No bench components ($\\eta = 0.35$, $r = 0.6$, $u = 1$), 16,000 CWU/t, cold barrel.',
               '\\* Sem componentes na bancada ($\\eta = 0{,}35$, $r = 0{,}6$, $u = 1$), 16.000 CWU/t, cano frio.',
               '\\* 无工作台部件（$\\eta = 0.35$，$r = 0.6$，$u = 1$），16,000 CWU/t，炮管冷却。') + '\n')

    # Bench
    L.append(heading(lang, m, 'bench'))
    L.append(T(lang, 'Click components on the bench line or in the Bench tab. Up to 8 rails (shift-click removes one); every other slot takes one component. Surveying a body to 100% unlocks the components that come from it. The loadout must fit three budgets, otherwise the Lance does not fire:',
               'Clique nos componentes na linha da bancada ou na aba Bancada. Até 8 trilhos (shift-clique tira um); os outros encaixes levam um componente cada. Levantar um corpo até 100% libera os componentes que vêm dele. A montagem precisa caber em três orçamentos, senão a Lança não dispara:',
               '在工作台行或“工作台”标签中点击部件。轨道最多 8 条（Shift+点击移除一条），其他槽位各放一个部件。将天体勘测至 100% 会解锁来自该天体的部件。配置必须满足三项预算，否则长矛不会射击：') + '\n')
    L.append(r"""$$
\sum m \le 800\ \text{t} \qquad \sum Q \le 60 \qquad \frac{n_{\text{rail}}}{8} \le 1
$$
""")
    names = {'rail': T(lang, 'Rail', 'Trilho', '轨道'), 'cooling': T(lang, 'Cooling', 'Arrefecimento', '冷却'), 'sensor': T(lang, 'Sensor', 'Sensor', '传感器'),
             'capsule': T(lang, 'Capsule', 'Cápsula', '返回舱'), 'salvo': T(lang, 'Salvo', 'Salva', '齐射')}
    eff = {'rail': lambda v: f'$\\Delta\\eta = +{num(v, lang)}$', 'cooling': lambda v: f'$C_{{\\text{{barrel}}}} \\times {num(v, lang)}$',
           'sensor': lambda v: f'$u = {num(v, lang)}$', 'capsule': lambda v: f'$r = {num(v, lang)}$',
           'salvo': lambda v: T(lang, f'{int(v)} projectiles per shot', f'{int(v)} projéteis por tiro', f'每次 {int(v)} 发弹丸')}
    L.append(table([T(lang, 'Component', 'Componente', '部件'), T(lang, 'Slot', 'Encaixe', '槽位'), T(lang, 'Effect', 'Efeito', '效果'),
                    T(lang, 'Mass (t)', 'Massa (t)', '质量 (t)'), T(lang, 'Heat', 'Calor', '热量'), T(lang, 'Unlocked by', 'Liberado por', '解锁来源')],
                   [(f'`{c}`', names[s], eff[s](v), num(ms, lang), num(q, lang), body(lang, u) if u else T(lang, 'start', 'início', '初始'))
                    for c, s, v, ms, q, u in COMPONENTS]))
    L.append(r"""$$
\begin{aligned}
\Delta T &= \frac{(1 - \eta)\,E}{C_{\text{barrel}}}, \qquad C_{\text{barrel}} = 2 \times 10^{9}\ \text{EU/K} \times k_{\text{cooling}} \\
\dot T_{\text{cooling}} &= -\frac{2^{34} \cdot 20\ \text{EU/s}}{C_{\text{barrel}}} \quad (\text{%s}) \\
W &\mathrel{+}= \frac{E}{E_{\text{liner}}}
\end{aligned}
$$
""" % T(lang, 'down to 300 K', 'até 300 K', '降至 300 K'))
    L.append(manual(lang, m, 'bench', skip=(1,)))
    L.append(table([T(lang, 'Liner (plate or dense plate)', 'Revestimento (placa ou placa densa)', '内衬（板或致密板）'), '$E_{liner}$ (EU)', T(lang, 'Full shots', 'Tiros cheios', '满能射击次数')],
                   [(mat('naquadah_alloy', lang), sci(5e13, lang), num(5e13 / BANK, lang)), (mat('neutronium', lang), sci(2e14, lang), num(2e14 / BANK, lang))]))
    L.append(T(lang, 'Without bench components a full shot heats the barrel by 1,300 K and the base cooling removes about 172 K per second.',
               'Sem componentes na bancada, um tiro cheio esquenta o cano em 1.300 K e o resfriamento base tira uns 172 K por segundo.',
               '无工作台部件时，一次满能射击使炮管升温 1,300 K，基础冷却每秒约降低 172 K。') + '\n')

    L.append(heading(lang, m, 'endgame'))
    L.append(manual(lang, m, 'endgame'))
    L.append(issues(lang, [
        T(lang, 'The projectile mass, the impact regime and the salvo splitter do not change what comes back yet: the recovered mass depends only on $\\eta$, $E$, $H$, $r$ and $A$.',
          'A massa do projétil, o regime do impacto e o divisor de salva ainda não mudam o que volta: a massa recuperada depende só de $\\eta$, $E$, $H$, $r$ e $A$.',
          '弹丸质量、撞击模式和齐射分流器目前不会改变回收量：回收质量只取决于 $\\eta$、$E$、$H$、$r$ 和 $A$。'),
        T(lang, 'The bank has one capacitor ring ($4 \\times 10^{12}$ EU); extra rings are not in the game yet, so the mass budget is 800 t and the heat budget 60.',
          'O banco tem um anel de capacitores ($4 \\times 10^{12}$ EU); anéis extras ainda não existem, então o orçamento de massa é 800 t e o de calor, 60.',
          '电容组只有一个电容环（$4 \\times 10^{12}$ EU）；额外的环尚未加入，因此质量预算为 800 t，热量预算为 60。'),
    ]))
    L.append(screens(lang, m, ['orbit', 'bench']))
    return '\n'.join(L)


# ====================================================================== Dimensional Rift Gate
HARMONICS = [('octave', 2, 1, None), ('fifth', 3, 2, 'crystal_plains'), ('fourth', 4, 3, 'spore_forest'), ('major_third', 5, 4, 'mercury_ocean'),
             ('minor_sixth', 8, 5, 'forge_world'), ('minor_seventh', 9, 5, 'civilisation_relic'), ('tritone', 45, 32, 'antimatter_abyss'),
             ('minor_second', 16, 15, 'void')]
HARM_NAMES = {'octave': ('Octave', 'Oitava', '八度'), 'fifth': ('Fifth', 'Quinta', '五度'), 'fourth': ('Fourth', 'Quarta', '四度'),
              'major_third': ('Major third', 'Terça maior', '大三度'), 'minor_sixth': ('Minor sixth', 'Sexta menor', '小六度'),
              'minor_seventh': ('Minor seventh', 'Sétima menor', '小七度'), 'tritone': ('Tritone', 'Trítono', '三全音'),
              'minor_second': ('Minor second', 'Segunda menor', '小二度')}
BIOMES = [('crystal_plains', 30, 0, [('prismatium', 'gtna'), ('certus_quartz', 'gtceu'), ('silicon', 'gtceu'), ('titanium', 'gtceu')]),
          ('mercury_ocean', 20, 0, [('chronomercury', 'gtna'), ('gold', 'gtceu'), ('thallium', 'gtceu'), ('cinnabar', 'gtceu')]),
          ('forge_world', 15, 0, [('forgecore', 'gtna'), ('tungsten', 'gtceu'), ('osmium', 'gtceu'), ('iridium', 'gtceu')]),
          ('spore_forest', 15, 0, [('vivispore', 'gtna'), ('wood', 'gtceu'), ('carbon', 'gtceu'), ('phosphorus', 'gtceu')]),
          ('antimatter_abyss', 8, 0, [('abyssal_antimatter', 'gtna'), ('naquadah', 'gtceu'), ('naquadah_enriched', 'gtceu')]),
          ('civilisation_relic', 7, 20, [('precursor_residue', 'gtna'), ('naquadria', 'gtceu'), ('trinium', 'gtceu'), ('duranium', 'gtceu')]),
          ('void', 5, 40, [('void_ash', 'gtna'), ('neutronium', 'gtceu'), ('space_time', 'gtna')])]


def consonance(p, q): return 1 / math.log2(p * q)


def rift(lang):
    m = 'dimensional_rift_gate'
    i = {'en': 0, 'pt': 1, 'zh': 2}[lang]
    L = [f'# {tr(lang, "block.gtna." + m)}\n']
    L.append(f'![{tr(lang, "block.gtna." + m)}](../../../assets/machines/{m}.webp){{ loading=lazy }}\n')
    L.append(manual(lang, m, 'overview'))
    L.append(facts(lang, [
        ('Tier', 'UIV'), (T(lang, 'Size', 'Tamanho', '尺寸'), '126 × 126 × 54'),
        (T(lang, 'Energy', 'Energia', '能量'), T(lang, "$2^{36}$ EU/t from the owner's Nexus network while the rift is open", '$2^{36}$ EU/t da rede Nexus do dono com a fenda aberta', '裂隙开启时从所有者的 Nexus 网络消耗 $2^{36}$ EU/t')),
        (T(lang, 'Fluid', 'Fluido', '流体'), T(lang, 'SpaceTime (stability)', 'SpaceTime (estabilidade)', '时空（稳定度）')),
        (T(lang, 'Controller', 'Controlador', '控制器'), T(lang, 'Assembly Line (UIV), research on the UIV Field Generator', 'Linha de Montagem (UIV), pesquisa no Gerador de Campo UIV', '装配线（UIV），研究 UIV 力场发生器')),
        (T(lang, 'Blocks', 'Blocos', '方块'), f'[{T(lang, "catalog page", "página do catálogo", "图鉴页面")}](../catalog/{m}.md)'),
    ]))
    L.append(heading(lang, m, 'build'))
    L.append(hatches(lang, [
        (T(lang, 'Input Hatch', 'Hatch de Entrada', '输入仓'), 4, 'SpaceTime'),
        (T(lang, 'Input Bus', 'Barramento de Entrada', '输入总线'), 4, T(lang, 'Rift Probes, Depth Anchors, Contained X-Nexus', 'Sondas de Fenda, Âncoras de Profundidade, X-Nexus contido', '裂隙探针、深度锚、封装 X-Nexus')),
        (T(lang, 'Output Bus', 'Barramento de Saída', '输出总线'), 4, T(lang, 'biome dusts, Rift Singularity', 'pós do bioma, Singularidade de Fenda', '生物群系粉、裂隙奇点')),
        (tr(lang, 'block.gtna.tuning_hatch'), 1, T(lang, 'redstone 0–15 sets the amplitude to 0–100%', 'redstone 0–15 define a amplitude em 0–100%', '红石 0–15 将振幅设为 0–100%')),
    ]))
    L.append(heading(lang, m, 'tuning'))
    L.append(manual(lang, m, 'tuning', skip=(2, 3, 4)))
    L.append(r"""$$
\begin{aligned}
R &= \exp\!\left(-\left(\frac{f - f^{*}}{\sigma_f}\right)^{2} - \left(\frac{\Delta\varphi}{\sigma_\varphi}\right)^{2} - \left(\frac{A - A^{*}}{\sigma_A}\right)^{2}\right) \\
\sigma_f &= 260\ \text{THz} \cdot 0.8^{n} \qquad \sigma_\varphi = 100^\circ \cdot 0.8^{n} \qquad \sigma_A = 45\,\% \cdot 0.8^{n}
\end{aligned}
$$
""".replace('0.8^', T(lang, '0.8^', '0{,}8^', '0.8^')))
    L.append(T(lang, '$f$ goes from 1 to 1000 THz, $\\varphi$ from 0 to 360° and $A$ from 0 to 100%; $(f^*, \\varphi^*, A^*)$ is the seed\'s hidden optimum and $n$ the number of probes consumed on this seed. Each knob shows a hot/cold bar for its own axis.',
               '$f$ vai de 1 a 1000 THz, $\\varphi$ de 0 a 360° e $A$ de 0 a 100%; $(f^*, \\varphi^*, A^*)$ é o ótimo escondido da semente e $n$ o número de sondas gastas nela. Cada botão mostra uma barra de quente/frio do próprio eixo.',
               '$f$ 范围为 1–1000 THz，$\\varphi$ 为 0–360°，$A$ 为 0–100%；$(f^*, \\varphi^*, A^*)$ 是该种子隐藏的最优值，$n$ 是在该种子上消耗的探针数。每个旋钮都会显示其所在轴的冷热条。') + '\n')
    L.append(table([T(lang, 'Probes', 'Sondas', '探针'), '$\\sigma_f$ (THz)', '$\\sigma_\\varphi$ (°)', '$\\sigma_A$ (%)', T(lang, 'Window for R ≥ 0.9 in f', 'Janela para R ≥ 0,9 em f', 'f 轴上 R ≥ 0.9 的窗口')],
                   [(k, num(260 * .8 ** k, lang), num(100 * .8 ** k, lang), num(45 * .8 ** k, lang), '±' + num(260 * .8 ** k * math.sqrt(-math.log(.9)), lang) + ' THz') for k in (0, 2, 4, 6, 8, 10)]))
    L.append(heading(lang, m, 'power'))
    L.append(manual(lang, m, 'power', skip=(3,)))
    L.append(r"""$$
\begin{aligned}
\frac{dS}{dt} &= 2\,\dot V - \lambda\,(1 - R)\left(1 + \frac{D}{10}\right) - 0.4\,(8 - P) \\
\lambda &= 1.5\,(1.3 - C) \\
\dot V_{\text{SpaceTime}} &= 16 \cdot \frac{\lambda\,(1 - R)\,(1 + D/10) + 0.4\,(8 - P)}{2}\ \text{L/s}
\end{aligned}
$$
""".replace('0.4', T(lang, '0.4', '0{,}4', '0.4')).replace('1.5', T(lang, '1.5', '1{,}5', '1.5')).replace('1.3', T(lang, '1.3', '1{,}3', '1.3')))
    L.append(T(lang, '$S$ is the stability (0–100), $D$ the depth, $P$ the active pylons (4 in the current structure) and $C$ the chord consonance (next section). The machine drains enough SpaceTime each second to cover the upkeep plus one unit; each litre of SpaceTime is worth 1/16 of a stability unit.',
               '$S$ é a estabilidade (0–100), $D$ a profundidade, $P$ os pilones ativos (4 na estrutura atual) e $C$ a consonância do acorde (próxima seção). A máquina drena por segundo SpaceTime para a manutenção mais uma unidade; cada litro de SpaceTime vale 1/16 de unidade de estabilidade.',
               '$S$ 为稳定度（0–100），$D$ 为深度，$P$ 为激活的塔架数（当前结构为 4），$C$ 为和弦协和度（见下一节）。机器每秒抽取足以支付维持量再加一个单位的时空；每升时空相当于 1/16 个稳定度单位。') + '\n')
    rows = []
    for r, d in ((0.5, 1), (0.9, 1), (0.9, 5), (0.98, 5), (0.98, 8), (1.0, 8)):
        rows.append((num(r, lang), d, num(16 * (1.5 * (1.3 - 0.3) * (1 - r) * (1 + d / 10) + 0.4 * 4) / 2, lang)))
    L.append(table(['R', 'D', T(lang, 'SpaceTime (L/s), no chord, 4 pylons', 'SpaceTime (L/s), sem acorde, 4 pilones', '时空 (L/s)，无和弦，4 个塔架')], rows))

    L.append(heading(lang, m, 'harmonics'))
    L.append(manual(lang, m, 'harmonics'))
    L.append(r"""$$
\begin{aligned}
\text{c}(p\!:\!q) &= \frac{1}{\log_2 (p\,q)} \qquad C = \overline{\text{c}} \ (\text{%s}) \\
D_{\max} &= \left\lfloor 5 \cdot \max\!\left(0.5,\ 1 + 3\,(0.3 - C)\right) \right\rfloor
\end{aligned}
$$
""".replace('0.5', T(lang, '0.5', '0{,}5', '0.5')).replace('0.3', T(lang, '0.3', '0{,}3', '0.3')) % T(lang, 'mean of the chord; 0.3 with no chord', 'média do acorde; 0,3 sem acorde', '和弦平均值；无和弦时为 0.3'))
    rows = []
    for h, p, q, src in HARMONICS:
        c = consonance(p, q)
        rows.append((HARM_NAMES[h][i], f'{p}:{q}', num(c, lang), num(1.3 - c, lang), int(5 * max(0.5, 1 + 3 * (0.3 - c))),
                     tr(lang, f'gtna.machine.dimensional_rift_gate.biome.{src}') if src else T(lang, 'not dropped by any biome', 'nenhum bioma dá', '没有生物群系产出')))
    L.append(table([T(lang, 'Interval', 'Intervalo', '音程'), T(lang, 'Ratio', 'Razão', '比例'), T(lang, 'Consonance', 'Consonância', '协和度'),
                    T(lang, 'λ factor (alone)', 'Fator de λ (sozinho)', 'λ 系数（单独）'), T(lang, 'Max depth (alone)', 'Profundidade máx. (sozinho)', '最大深度（单独）'),
                    T(lang, 'Recorded in', 'Gravado em', '记录于')], rows))
    L.append(heading(lang, m, 'endgame'))
    L.append(T(lang, 'Each biome drops dusts of its materials into the output buses. Rate of **each** material:',
               'Cada bioma solta pós dos seus materiais nos barramentos de saída. Taxa de **cada** material:',
               '每个生物群系向输出总线产出其材料的粉。**每种**材料的速率：') + '\n')
    L.append(r"""$$
\text{%s} = 16 \cdot R^{2} \cdot D^{1.5} \cdot \frac{S}{100}
$$
""".replace('1.5', T(lang, '1.5', '1{,}5', '1.5')) % T(lang, 'dusts/s', 'pós/s', '粉/秒'))
    L.append(table([T(lang, 'Biome', 'Bioma', '生物群系'), T(lang, 'Chance', 'Chance', '概率'), T(lang, 'Min. depth', 'Prof. mínima', '最低深度'), T(lang, 'Dusts', 'Pós', '粉')],
                   [(tr(lang, f'gtna.machine.dimensional_rift_gate.biome.{b}'), f'{w}%', d or '—', ', '.join(('**' + mat(x, lang, ns) + '**') if k == 0 else mat(x, lang, ns) for k, (x, ns) in enumerate(mt)))
                    for b, w, d, mt in BIOMES]))
    L.append(manual(lang, m, 'endgame'))
    L.append(issues(lang, [
        T(lang, 'The maximum depth starts at 5 and nothing raises it yet; the most dissonant chord reaches 8. Civilisation Relic (depth 20) and Void (depth 40) therefore yield nothing, so **Precursor Residue** and **Void Ash** cannot be obtained in this version.',
          'A profundidade máxima começa em 5 e ainda nada a aumenta; o acorde mais dissonante chega a 8. Por isso Relíquia de Civilização (profundidade 20) e Vazio (40) não rendem nada, e **Resíduo Precursor** e **Cinza do Vazio** não podem ser obtidos nesta versão.',
          '最大深度从 5 开始，目前没有任何方式提高；最不协和的和弦也只能到 8。因此文明遗迹（深度 20）和虚空（深度 40）不会产出，本版本无法获得**先驱者残留物**和**虚空灰烬**。'),
        T(lang, 'Pylon cores are not in the game: the structure always counts 4 active pylons.', 'Os núcleos de pilone ainda não existem: a estrutura sempre conta 4 pilones ativos.', '塔架核心尚未加入：结构始终按 4 个激活塔架计算。'),
    ]))
    L.append(screens(lang, m, ['chord', 'atlas']))
    return '\n'.join(L)


# ====================================================================== Antimatter Collider Ring
MAGNETS = [('NbTi', 8.3), ('Nb₃Sn', 12), ('REBCO', 20), ('Neutronium', 45), ('Infinity', 120)]
RING = 3000
F_REV = 2.998e8 / (2 * math.pi * RING)
PARTICLES = [('antiproton', 5.6, 50), ('kaon', 1.0, 30), ('lambda', 2.5, 8), ('charm', 10, 4), ('bottom', 40, 1.5), ('w_boson', 161, 0.6),
             ('z_boson', 182, 0.8), ('higgs', 250, 0.08), ('top', 346, 0.15), ('x_nexus', 4800, 0.02)]
PROPOSALS = [
    ('nb3sn_magnet', ('5 fb⁻¹ delivered', '5 fb⁻¹ entregues', '累计 5 fb⁻¹'), ('magnet Nb₃Sn (12 T)', 'ímã Nb₃Sn (12 T)', 'Nb₃Sn 磁体（12 T）')),
    ('vertex_detector', ('charm at 5σ', 'charm em 5σ', 'charm 达到 5σ'), ('significance × √2, beam 16 µm', 'significância × √2, feixe de 16 µm', '显著性 × √2，束流 16 µm')),
    ('stochastic_cooling', ('20 fb⁻¹', '20 fb⁻¹', '20 fb⁻¹'), ('1,000 bunches', '1.000 pacotes', '1,000 个束团')),
    ('cryo_penning', ('10¹³ antiprotons stored or 40 fb⁻¹', '10¹³ antiprótons guardados ou 40 fb⁻¹', '储存 10¹³ 反质子或 40 fb⁻¹'), ('trap tier 3, helium × 0.6', 'armadilha tier 3, hélio × 0,6', '陷阱等级 3，氦 × 0.6')),
    ('rebco_magnet', ('W and Z at 5σ', 'W e Z em 5σ', 'W 与 Z 达到 5σ'), ('magnet REBCO (20 T)', 'ímã REBCO (20 T)', 'REBCO 磁体（20 T）')),
    ('lepton_collider', ('bottom at 5σ', 'bottom em 5σ', 'bottom 达到 5σ'), ('electron beams', 'feixes de elétrons', '电子束')),
    ('heavy_ions', ('top at 5σ', 'top em 5σ', 'top 达到 5σ'), ('heavy ions: X-Nexus can be produced', 'íons pesados: X-Nexus pode ser produzido', '重离子：可产生 X-Nexus')),
    ('neutronium_magnet', ('Higgs at 5σ + 1024 fine Nexium wire', 'Higgs em 5σ + 1024 fios finos de Nexium', 'Higgs 达到 5σ + 1024 根奈克斯金属细线'), ('magnet Neutronium (45 T)', 'ímã de Neutrônio (45 T)', '中子素磁体（45 T）')),
    ('beyond_standard_model', ('X-Nexus at 3σ', 'X-Nexus em 3σ', 'X-Nexus 达到 3σ'), ('magnet Infinity (120 T)', 'ímã Infinity (120 T)', '无尽磁体（120 T）')),
]


def lumi(bunches=100, sigma_um=20):
    s = sigma_um * 1e-4
    return F_REV * bunches * 1e11 ** 2 / (4 * math.pi * s * s)


def collider(lang):
    m = 'antimatter_collider_ring'
    i = {'en': 0, 'pt': 1, 'zh': 2}[lang]
    L = [f'# {tr(lang, "block.gtna." + m)}\n']
    L.append(f'![{tr(lang, "block.gtna." + m)}](../../../assets/machines/{m}.webp){{ loading=lazy }}\n')
    L.append(manual(lang, m, 'overview'))
    L.append(facts(lang, [
        ('Tier', 'UIV'), (T(lang, 'Size', 'Tamanho', '尺寸'), '155 × 127 × 137'),
        (T(lang, 'Energy', 'Energia', '能量'), T(lang, "owner's Nexus network (magnets and traps)", 'rede Nexus do dono (ímãs e armadilhas)', '所有者的 Nexus 网络（磁体与陷阱）')),
        (T(lang, 'Fluid', 'Fluido', '流体'), T(lang, 'liquid helium', 'hélio líquido', '液氦')),
        (T(lang, 'Controller', 'Controlador', '控制器'), T(lang, 'Assembly Line (UIV), research on the UIV Emitter', 'Linha de Montagem (UIV), pesquisa no Emissor UIV', '装配线（UIV），研究 UIV 发射器')),
        (T(lang, 'Blocks', 'Blocos', '方块'), f'[{T(lang, "catalog page", "página do catálogo", "图鉴页面")}](../catalog/{m}.md)'),
    ]))
    L.append(heading(lang, m, 'build'))
    L.append(hatches(lang, [
        (T(lang, 'Input Hatch', 'Hatch de Entrada', '输入仓'), 4, T(lang, 'liquid helium', 'hélio líquido', '液氦')),
        (T(lang, 'Input Bus', 'Barramento de Entrada', '输入总线'), 2, T(lang, 'fine Nexium wire (Neutronium Magnet proposal)', 'fio fino de Nexium (proposta do ímã de Neutrônio)', '奈克斯金属细线（中子素磁体提案）')),
        (T(lang, 'Output Bus', 'Barramento de Saída', '输出总线'), 4, T(lang, 'particles, Antiproton Penning Cells', 'partículas, Células de Penning de Antiprótons', '粒子、反质子彭宁电池')),
        (tr(lang, 'block.gtna.detector_hatch'), 1, T(lang, 'needed to record physics runs', 'obrigatório para gravar corridas de física', '物理运行记录所必需')),
        (tr(lang, 'block.gtna.beam_dump'), 1, T(lang, 'halves the quench recovery', 'corta pela metade a recuperação do quench', '失超恢复时间减半')),
    ]))
    L.append(manual(lang, m, 'build', skip=(1,)))
    L.append(heading(lang, m, 'modes'))
    L.append(manual(lang, m, 'modes', skip=(3,)))
    L.append(r"""$$
\begin{aligned}
E_{\text{beam}} &= 0.3\,B\,\rho \quad (\text{GeV, } B \text{ in T, } \rho = 3000\ \text{m}) \\
E_{\text{cm}} &= 2\left(150 + (E_{\text{beam}} - 150) \cdot \min\!\left(1, \tfrac{t}{20\ \text{s}}\right)\right)\ \text{GeV} \\
\mathcal{L} &= \frac{f_{\text{rev}}\,n_b\,N^{2}}{4\pi\sigma^{2}}, \qquad f_{\text{rev}} = \frac{c}{2\pi\rho} \approx 15{,}905\ \text{Hz},\ N = 10^{11} \\
\Delta\!\int\!\mathcal{L} &= \mathcal{L} \cdot 10^{-39} \cdot 10^{5}\ \text{fb}^{-1}\ \text{%s} \\
Z &= s\,\sqrt{\textstyle\int\!\mathcal{L}} \cdot (\sqrt{2}\ \text{%s})
\end{aligned}
$$
""".replace('0.3\\,', T(lang, '0.3\\,', '0{,}3\\,', '0.3\\,')).replace('15{,}905', T(lang, '15{,}905', '15.905', '15{,}905')) % (
        T(lang, 'per second', 'por segundo', '每秒'), T(lang, 'with the vertex detector', 'com o detector de vértice', '有顶点探测器时')))
    L.append(T(lang, f'A full ring ramps in 20 s from 150 GeV. Base luminosity is {sci(lumi(), lang)} cm⁻²s⁻¹ ({num(lumi() * 1e-34, lang)} fb⁻¹/s); with stochastic cooling and the vertex detector it is {sci(lumi(1000, 16), lang)} ({num(lumi(1000, 16) * 1e-34, lang)} fb⁻¹/s). Production yield: 10% before 3σ, 40% from 3σ, 100% from 5σ.',
               f'O anel sobe em 20 s a partir de 150 GeV. A luminosidade base é {sci(lumi(), lang)} cm⁻²s⁻¹ ({num(lumi() * 1e-34, lang)} fb⁻¹/s); com resfriamento estocástico e detector de vértice, {sci(lumi(1000, 16), lang)} ({num(lumi(1000, 16) * 1e-34, lang)} fb⁻¹/s). Rendimento da produção: 10% antes de 3σ, 40% a partir de 3σ, 100% a partir de 5σ.',
               f'满环从 150 GeV 起在 20 秒内升能。基础亮度为 {sci(lumi(), lang)} cm⁻²s⁻¹（{num(lumi() * 1e-34, lang)} fb⁻¹/秒）；有随机冷却和顶点探测器时为 {sci(lumi(1000, 16), lang)}（{num(lumi(1000, 16) * 1e-34, lang)} fb⁻¹/秒）。生产产率：3σ 前 10%，3σ 起 40%，5σ 起 100%。') + '\n')
    L.append(table([T(lang, 'Magnet', 'Ímã', '磁体'), 'B (T)', T(lang, 'Max beam (TeV)', 'Feixe máx. (TeV)', '最大束流 (TeV)'), T(lang, 'Upkeep (EU/t)', 'Manutenção (EU/t)', '维持 (EU/t)'),
                    T(lang, 'Liquid helium (L/s)', 'Hélio líquido (L/s)', '液氦 (L/s)'), T(lang, 'Quench pause', 'Pausa do quench', '失超暂停')],
                   [(n, num(b, lang), num(0.3 * b * RING / 1000, lang), f'$2^{{{33 + k}}}$', num(0.5 * 2 ** k, lang) + ' (' + num(0.3 * 2 ** k, lang) + ')', f'{60 * (k + 1)} s')
                    for k, (n, b) in enumerate(MAGNETS)]))
    L.append(T(lang, 'Helium in brackets: after the cryogenic Penning proposal. The quench pause doubles without a Beam Dump.',
               'Hélio entre parênteses: depois da proposta de Penning criogênico. A pausa do quench dobra sem Beam Dump.',
               '括号内为低温彭宁提案后的液氦用量。没有束流收集器时失超暂停时间翻倍。') + '\n')
    base = lumi() * 1e-34
    rows = []
    for p, th, s in PARTICLES:
        fb = (5 / s) ** 2
        rows.append((tr(lang, f'gtna.machine.antimatter_collider_ring.particle.{p}'), num(th, lang), num(s, lang), num(fb, lang), num(fb / 2, lang),
                     num(fb / base / 3600, lang)))
    L.append(table([T(lang, 'Particle', 'Partícula', '粒子'), T(lang, 'Threshold E_cm (GeV)', 'Limiar E_cm (GeV)', '阈值 E_cm (GeV)'), '$s$',
                    T(lang, 'fb⁻¹ for 5σ', 'fb⁻¹ para 5σ', '5σ 所需 fb⁻¹'), T(lang, 'with vertex', 'com vértice', '有顶点探测器'), T(lang, 'hours at base luminosity', 'horas na luminosidade base', '基础亮度下小时数')], rows))
    L.append(T(lang, 'X-Nexus also needs the heavy-ion proposal.', 'O X-Nexus também precisa da proposta de íons pesados.', 'X-Nexus 还需要重离子提案。') + '\n')
    L.append(heading(lang, m, 'power'))
    L.append(r"""$$
\begin{aligned}
P_{\text{magnets}} &= 2^{\,33 + k_{\text{magnet}}}\ \text{EU/t} \qquad P_{\text{traps}} = 2^{\,20 + k_{\text{trap}}}\ \text{EU/t} \\
\dot V_{\text{He}} &= 0.5 \cdot 2^{k_{\text{magnet}}}\ \text{L/s} \quad (\times 0.6\ \text{%s}) \\
\text{%s} &= 10^{12} \cdot 4^{\,k_{\text{trap}} - 1}\ \bar p
\end{aligned}
$$
""".replace('0.5 ', T(lang, '0.5 ', '0{,}5 ', '0.5 ')).replace('0.6', T(lang, '0.6', '0{,}6', '0.6')) % (
        T(lang, 'after cryogenic Penning', 'depois do Penning criogênico', '低温彭宁后'), T(lang, 'trap capacity', 'capacidade das armadilhas', '陷阱容量')))
    L.append(manual(lang, m, 'power', skip=(1, 2)))
    L.append(heading(lang, m, 'proposals'))
    L.append(T(lang, 'The committee grants one proposal at a time, in this order. Physics runs advance the active proposal.',
               'O comitê aprova uma proposta por vez, nesta ordem. As corridas de física avançam a proposta ativa.',
               '委员会每次批准一个提案，按以下顺序。物理运行推进当前提案。') + '\n')
    L.append(table(['#', T(lang, 'Proposal', 'Proposta', '提案'), T(lang, 'Needs', 'Pede', '要求'), T(lang, 'Gives', 'Dá', '奖励')],
                   [(k + 1, tr(lang, f'gtna.machine.antimatter_collider_ring.proposal.{p}'), need[i], give[i]) for k, (p, need, give) in enumerate(PROPOSALS)]))
    L.append(manual(lang, m, 'proposals', skip=(1,)))
    L.append(heading(lang, m, 'endgame'))
    L.append(manual(lang, m, 'endgame'))
    L.append(issues(lang, [
        T(lang, 'After the **e+e− collisions** proposal the ring runs electron beams and the synchrotron load quenches the magnets every second, so the ring stops for good. Until this is fixed, switch to production mode once the REBCO magnet is done: heavy ions, the neutronium magnet, X-Nexus and the last proposal cannot be reached in this version.',
          'Depois da proposta **colisões e+e−** o anel passa a feixes de elétrons e a carga de síncrotron faz quench nos ímãs a cada segundo: o anel para de vez. Até a correção, passe para o modo produção quando o ímã REBCO estiver pronto. Íons pesados, ímã de neutrônio, X-Nexus e a última proposta não são alcançáveis nesta versão.',
          '完成 **e+e− 对撞**提案后，环会改为电子束，同步辐射负载每秒都会导致磁体失超，环将永久停机。修复前，请在 REBCO 磁体完成后切换到生产模式。本版本无法达到重离子、中子素磁体、X-Nexus 以及最后一个提案。'),
    ]))
    L.append(screens(lang, m, ['model', 'board']))
    return '\n'.join(L)


# ====================================================================== Stellar Containment Chamber
G, C, MSUN, R = 6.674e-11, 2.998e8, 1.989e30, 12e3


def kepler_ms(msol): return 2 * math.pi * math.sqrt(R ** 3 / (G * msol * MSUN)) * 1000
def penrose(a): return 1 - math.sqrt((1 + math.sqrt(1 - a * a)) / 2)


def stellar(lang):
    m = 'stellar_containment_chamber'
    L = [f'# {tr(lang, "block.gtna." + m)}\n']
    L.append(f'![{tr(lang, "block.gtna." + m)}](../../../assets/machines/{m}.webp){{ loading=lazy }}\n')
    L.append(manual(lang, m, 'overview'))
    L.append(facts(lang, [
        ('Tier', 'MAX'), (T(lang, 'Size', 'Tamanho', '尺寸'), '93 × 93 × 93'),
        (T(lang, 'Energy', 'Energia', '能量'), T(lang, "produces EU into the owner's Nexus network", 'gera EU para a rede Nexus do dono', '向所有者的 Nexus 网络输出 EU')),
        (T(lang, 'Output', 'Saída', '输出'), T(lang, 'up to $2^{59}$ EU/t (neutron star), $2^{62}$ EU/t (black hole)', 'até $2^{59}$ EU/t (estrela de nêutrons), $2^{62}$ EU/t (buraco negro)', '最高 $2^{59}$ EU/t（中子星），$2^{62}$ EU/t（黑洞）')),
        (T(lang, 'Controller', 'Controlador', '控制器'), T(lang, 'Assembly Line (UXV), research on the UXV Field Generator', 'Linha de Montagem (UXV), pesquisa no Gerador de Campo UXV', '装配线（UXV），研究 UXV 力场发生器')),
        (T(lang, 'Blocks', 'Blocos', '方块'), f'[{T(lang, "catalog page", "página do catálogo", "图鉴页面")}](../catalog/{m}.md)'),
    ]))
    L.append(heading(lang, m, 'build'))
    L.append(hatches(lang, [
        (T(lang, 'Input Hatch', 'Hatch de Entrada', '输入仓'), 8, T(lang, 'star matter (any fluid form)', 'matéria estelar (qualquer forma de fluido)', '恒星物质（任意流体形态）')),
        (T(lang, 'Output Bus', 'Barramento de Saída', '输出总线'), 4, T(lang, 'neutronium, white dwarf matter, crystals, core matter', 'neutrônio, matéria de anã branca, cristais, matéria do núcleo', '中子素、白矮星物质、晶体、核心物质')),
        (tr(lang, 'block.gtna.mass_injector'), 4, T(lang, 'dusts and ingots of star matter; ', 'pós e lingotes de matéria estelar; placas de ', '恒星物质的粉和锭；') + mat('forgecore', lang, 'gtna') + T(lang, ' plates', '', '板')),
        (tr(lang, 'block.gtna.seismic_probe'), 1, T(lang, 'decodes starquakes', 'decifra os tremores', '解码星震')),
    ]))
    L.append(manual(lang, m, 'build', skip=(1,)))
    L.append(heading(lang, m, 'power'))
    L.append(manual(lang, m, 'power', skip=(2, 4)))
    L.append(r"""$$
\begin{aligned}
I &= 0.4\,M R^{2}, \quad R = 12\ \text{km} \qquad E_{\text{rot}} = \tfrac12 I\,\omega^{2} \cdot 10^{-20}\ \text{EU/J}, \quad \omega = \frac{2\pi}{P} \\
P_{\text{dipole}} &= \frac{B^{2} R^{6} \omega^{4}}{6 c^{3}} \cdot 10^{-20}\ \text{EU/J}, \quad B = 6.7 \times 10^{11}\ \text{T}\ (\times 4\ \text{%s}) \\
\text{%s} &= 2^{\,40 + 2k}\ \text{EU/t} \qquad \text{%s} = 2^{\,55 + k}\ \text{EU/t}\ (\tfrac12\ \text{%s})
\end{aligned}
$$
""".replace('0.4\\,', T(lang, '0.4\\,', '0{,}4\\,', '0.4\\,')).replace('6.7', T(lang, '6.7', '6{,}7', '6.7')) % (
        T(lang, 'magnetar', 'magnetar', '磁星'), T(lang, 'upkeep', 'manutenção', '维持'), T(lang, 'cap', 'teto', '上限'),
        T(lang, 'until the millisecond region', 'até a região de milissegundos', '到达毫秒区之前')))
    rows = []
    how = {1: T(lang, 'start', 'início', '初始'), 2: T(lang, 'micro quake decoded', 'tremor micro decifrado', '解码微震'),
           3: T(lang, 'Vela quake decoded', 'tremor Vela decifrado', '解码 Vela 震'), 4: T(lang, 'Vela + record spin (< 1.4 ms)', 'Vela + rotação recorde (< 1,4 ms)', 'Vela + 纪录自转（< 1.4 ms）')}
    for k in (1, 2, 3, 4):
        rows.append((k, how[k], f'$2^{{{40 + 2 * k}}}$', f'$2^{{{55 + k}}}$', sci(1e15 * 10 ** k, lang)))
    L.append(table([T(lang, 'Band tier', 'Tier da banda', '束带等级'), T(lang, 'Unlocked by', 'Liberado por', '解锁方式'), T(lang, 'Upkeep (EU/t)', 'Manutenção (EU/t)', '维持 (EU/t)'),
                    T(lang, 'Cap (EU/t)', 'Teto (EU/t)', '上限 (EU/t)'), T(lang, 'Quake capacity', 'Capacidade de tremor', '星震容量')], rows))
    L.append(T(lang, 'Extraction also mines the crust: $\\text{EU/t} / 2^{52}$ neutronium dusts per second.',
               'A extração também minera a crosta: $\\text{EU/t} / 2^{52}$ pós de neutrônio por segundo.',
               '提取同时开采星壳：每秒 $\\text{EU/t} / 2^{52}$ 份中子素粉。') + '\n')
    L.append(heading(lang, m, 'feeding'))
    L.append(manual(lang, m, 'feeding', skip=(2,)))
    L.append(r"""$$
\begin{aligned}
\Delta J &= \Delta M\,\sqrt{G M R} \qquad \omega' = \frac{I\omega + \Delta J}{I'} \\
M' &= M + 0.85\,\Delta M \qquad E_{\text{bind}} = 0.15\,\Delta M\,c^{2} \cdot 10^{-26}\ \text{EU/J}
\end{aligned}
$$
""".replace('0.85', T(lang, '0.85', '0{,}85', '0.85')).replace('0.15', T(lang, '0.15', '0{,}15', '0.15')))
    L.append(table([T(lang, 'Feed', 'Alimento', '投料'), T(lang, 'M☉ per mB', 'M☉ por mB', '每 mB 太阳质量'), T(lang, 'M☉ per dust or ingot', 'M☉ por pó ou lingote', '每份粉或锭太阳质量')],
                   [(mat(x, lang, ns), sci(v, lang), sci(v * 144, lang)) for x, ns, v in (
                       ('magnetohydrodynamically_constrained_star_matter', 'gtna', 1e-7), ('white_dwarf_matter', 'gtna', 1e-8), ('raw_star_matter', 'gtna', 1e-9), ('neutronium', 'gtceu', 1e-10))]))
    L.append(heading(lang, m, 'quakes'))
    L.append(manual(lang, m, 'quakes'))
    L.append(r"""$$
\sigma \mathrel{+}= 10^{4} \cdot \frac{|\Delta\omega|}{\omega} \quad (\text{%s})
$$
""" % T(lang, 'a quake at σ ≥ 1', 'tremor em σ ≥ 1', 'σ ≥ 1 时发生星震'))
    qrows = []
    for q, size in (('micro', 5e-9), ('crab', 5e-8), ('vela', 1.1e-6), ('anti', -3e-7), ('collapse', 1e-4)):
        qrows.append((tr(lang, f'gtna.ui.o.quake.{q}'), tr(lang, f'gtna.ui.o.quake.{q}.how'), sci(size, lang)))
    L.append(table([T(lang, 'Quake', 'Tremor', '星震'), T(lang, 'How', 'Como', '触发'), 'ΔΩ/Ω'], qrows))
    L.append(heading(lang, m, 'limits'))
    L.append(manual(lang, m, 'limits', skip=(2, 3)))
    L.append(r"""$$
\begin{aligned}
P_{\text{Kepler}} &= 2\pi\sqrt{\frac{R^{3}}{G M}} \\
a^{*} &= \min\!\left(0.998,\ \frac{J c}{G M^{2}}\right) \qquad E_{\text{hole}} = \left(1 - \sqrt{\frac{1 + \sqrt{1 - a^{*2}}}{2}}\right) M c^{2}
\end{aligned}
$$
""".replace('0.998', T(lang, '0.998', '0{,}998', '0.998')))
    L.append(table([T(lang, 'Mass (M☉)', 'Massa (M☉)', '质量 (M☉)'), T(lang, 'Kepler period (ms)', 'Período de Kepler (ms)', '开普勒周期 (ms)')],
                   [(num(x, lang), num(kepler_ms(x), lang)) for x in (1.2, 1.4, 1.8, 2.1, 2.2)]))
    L.append(table(['$a^*$', T(lang, 'Extractable share of $Mc^2$', 'Fração extraível de $Mc^2$', '可提取的 $Mc^2$ 比例')],
                   [(num(a, lang), num(penrose(a) * 100, lang) + '%') for a in (0.3, 0.6, 0.9, 0.998)]))
    L.append(T(lang, 'The TOV limit is 2.2 M☉, or 2.4 M☉ after an anti-quake has been decoded. Mass–period regions: young (< 30 ms), millisecond (< 10 ms after feeding), record (< 1.4 ms), magnetar (600 s of inverted field), TOV edge (> 2.1 M☉), black hole.',
               'O limite TOV é 2,2 M☉, ou 2,4 M☉ depois de decifrar um antitremor. Regiões do diagrama massa–período: jovem (< 30 ms), milissegundos (< 10 ms depois de alimentar), recorde (< 1,4 ms), magnetar (600 s de campo invertido), borda TOV (> 2,1 M☉), buraco negro.',
               'TOV 极限为 2.2 M☉，解码反星震后为 2.4 M☉。质量-周期图区域：年轻（< 30 ms）、毫秒（投料后 < 10 ms）、纪录（< 1.4 ms）、磁星（反转场 600 秒）、TOV 边缘（> 2.1 M☉）、黑洞。') + '\n')
    L.append(heading(lang, m, 'endgame'))
    L.append(manual(lang, m, 'endgame'))
    L.append(screens(lang, m, ['mp', 'quakes']))
    return '\n'.join(L)


PAGES = (('kinetic-orbital-lance', lance), ('dimensional-rift-gate', rift), ('antimatter-collider-ring', collider),
         ('stellar-containment-chamber', stellar))


def main():
    os.makedirs(OUT, exist_ok=True)
    for slug, build in PAGES:
        for lang, _, suffix in LANGS:
            md = build(lang)
            open(os.path.join(OUT, slug + suffix), 'w', encoding='utf-8').write(zh_punct.fix(md) if lang == 'zh' else md)
    print(' '.join(s for s, _ in PAGES))


if __name__ == '__main__':
    main()
