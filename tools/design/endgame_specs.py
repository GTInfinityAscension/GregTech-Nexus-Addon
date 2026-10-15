"""Design specs for the four original GTNA endgame multiblocks.

Every table is computed from the formulas written in the same document, so the numbers stay consistent
when a constant changes. Output: docs/roadmap/design/<machine>.md (Portuguese, author-facing).

    python3 tools/design/endgame_specs.py
"""
import math
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
OUT = os.path.join(ROOT, 'docs/roadmap/design')


def fmt(x, d=3):
    if x == 0: return '0'
    a = abs(x)
    if a >= 1e6 or a < 1e-3: return f'{x:.{d - 1}e}'.replace('e+0', 'e').replace('e+', 'e').replace('e-0', 'e-')
    if a >= 100: return f'{x:,.0f}'.replace(',', '.')
    return f'{x:.{d}g}'.replace('.', ',')


def table(head, rows):
    out = ['| ' + ' | '.join(head) + ' |', '|' + '|'.join('---' for _ in head) + '|']
    out += ['| ' + ' | '.join(str(c) for c in r) + ' |' for r in rows]
    return '\n'.join(out) + '\n'


def upgrades(rows):
    return table(['Tag', 'Custo', 'Pré-requisito', 'Nome', 'Efeito'], rows)


def milestones(kinds, tiers=7):
    head = ['Nível'] + [k[0] for k in kinds]
    rows = []
    for t in range(1, tiers + 1):
        rows.append([t] + [fmt(k[1] * k[2] ** (t - 1)) if k[2] != 1 else fmt(k[1] * t) for k in kinds])
    return table(head, rows)


# ---------------------------------------------------------------------------------------------------------
# 1. Kinetic Orbital Lance
# ---------------------------------------------------------------------------------------------------------
def lance():
    EU_J = 1000.0          # 1 EU = 1 kJ inside this machine's physics
    bodies = [  # name, distance Mm, hardness MJ/kg, composition
        ('Lua', 384, 2.0, 'regolito: Fe, Ti, Al, He-3 (traço)'),
        ('Fobos', 78, 1.2, 'condrito carbonáceo: C, Ni, Fe, compostos orgânicos'),
        ('Vesta', 1.7e5, 3.5, 'basalto diferenciado: Fe, Mg, Cr, Pt'),
        ('Psique', 3.7e5, 6.0, 'núcleo metálico: Fe, Ni, Ir, Os, Au'),
        ('Ceres', 4.1e5, 1.5, 'gelo e argilas: H₂O, NH₃, Mg, Na₂CO₃'),
        ('Europa', 6.3e5, 2.8, 'gelo salino: H₂O, MgSO₄, D₂O'),
        ('Arrokoth', 6.6e6, 0.9, 'gelos voláteis: N₂, CO, CH₄, tolinas'),
        ('Remanescente Kuiper "Nexus-1"', 7.5e6, 9.5, 'matéria exótica: Nq, Nt, Ad (alvo endgame)'),
    ]
    slugs = [('Tungstênio', 50, 1), ('Tungstênio-Carbeto', 80, 2), ('Ósmio-Irídio', 120, 3), ('Neutrônio', 400, 4), ('Matéria Degenerada', 1200, 5)]
    eta0 = 0.35
    md = ['# Lança Cinética Orbital (UEV)\n',
          '> Ficha de design, versão 1. Números calculados por `tools/design/endgame_specs.py`.\n',
          '## 1. Visão geral\n',
          '- **Tipo:** mineração por bombardeio cinético. Gerador de minério sem mina.',
          '- **Tier:** UEV (controlador), módulos até UIV.',
          '- **Estrutura:** 142 × 130 × 242 (torre + canhão), base com até 4 anéis de capacitores.',
          '- **Energia:** hatches de energia ou laser carregam o banco; o tiro descarrega o banco inteiro.',
          '- **Saída:** cápsulas de retorno com minério bruto, metal fundido ou plasma, conforme a energia do impacto.',
          '- **Overclock:** não se aplica ao tiro; a cadência sobe com upgrades e com o banco.\n',
          '## 2. Estrutura\n',
          'A estrutura cresce em **anéis de capacitores** na base. O primeiro anel vem com o controlador; os outros três são construções extras liberadas por upgrade, como os anéis da Godforge.\n',
          table(['Componente', 'Anel 1', 'Anel 2', 'Anel 3', 'Anel 4'], [
              ['Clean Stainless Steel Casing (casco)', '101.609', '+9.000', '+11.000', '+13.000'],
              ['Radiant Naquadah Alloy Casing (blindagem do cano)', '52.147', '—', '—', '—'],
              ['Tungstensteel Pipe Casing (barramento)', '7.963', '+1.200', '+1.500', '+1.800'],
              ['PTFE Inert Casing (isolamento)', '7.044', '+800', '+800', '+800'],
              ['Dyson Deployment Core (células de capacitor)', '803', '+803', '+1.606', '+3.212'],
              ['Neutronium Stable Casing (boca do cano)', '620', '—', '—', '—'],
              ['Heat Vent (radiadores do cano)', '759', '+200', '+200', '+200'],
          ]),
          'Hatches: só nos casings marcados ao redor do controlador. Exatamente um **Hatch de Projétil**, um **Hatch de Revestimento do Cano**, um **Hatch de Refrigerante**, um **Hatch de Dados Ópticos** (computação) e um **Barramento ME de Retorno**.\n',
          '## 3. Física do tiro\n',
          'Constantes da máquina: `1 EU = 1 kJ`, eficiência do trilho `η₀ = 0,35`.\n',
          '```\nE_tiro  = energia descarregada do banco (EU)\nv       = sqrt(2 · η · E_tiro · 1000 / m)          [m/s]\nβ       = v / c\ne       = η · E_tiro · 1000 / m                     [J/kg]  energia específica\nM_frag  = k_frag · η · E_tiro · 1000 / H            [kg]    massa fragmentada (k_frag = 0,2)\nM_ret   = M_frag · r · A                            [kg]    massa recuperada\n```\n',
          '`H` é a dureza do corpo (J/kg), `r` a taxa de recuperação das cápsulas (base 0,6) e `A` a precisão (seção 4).\n',
          '### 3.1 Regime do impacto\n',
          'A energia específica decide a forma da saída. Os limites são múltiplos da dureza do corpo:\n',
          table(['Regime', 'Condição', 'Saída', 'Bônus'], [
              ['Fragmentação', '`e < 10·H`', 'minério bruto (crushed)', '—'],
              ['Fusão de impacto', '`10·H ≤ e < 200·H`', 'metais fundidos (fluidos)', '+25% de elementos raros'],
              ['Vaporização', '`200·H ≤ e < 5000·H`', 'gás ionizado / plasma do elemento', '+60% de raros, sem subproduto de pedra'],
              ['Relativístico', '`e ≥ 5000·H` (β > 0,1)', 'plasma + chance de isótopos exóticos', 'tabela exclusiva por corpo'],
          ]),
          '### 3.2 Projéteis\n',
          table(['Projétil', 'Massa (kg)', 'Tier', 'v com 1e12 EU (km/s)', 'β'], [
              [n, m, t, fmt(math.sqrt(2 * eta0 * 1e12 * EU_J / m) / 1000), fmt(math.sqrt(2 * eta0 * 1e12 * EU_J / m) / 3e8)]
              for n, m, t in slugs]),
          'Projétil leve chega mais rápido e vaporiza mais; projétil pesado fragmenta mais massa por tiro. O jogador escolhe pela saída que quer.\n',
          '### 3.3 Corpos-alvo\n',
          table(['Corpo', 'Distância (Mm)', 'Dureza H (MJ/kg)', 'Composição', 'Retorno da cápsula'], [
              [n, fmt(d), fmt(h), comp, f'{fmt(2 * d * 1e6 / 30000 / 600)} s'] for n, d, h, comp in bodies]),
          '`t_retorno = 2 · d / 30 km/s ÷ 600` (o tempo é comprimido 600×). As cápsulas ficam numa fila visível na GUI.\n',
          '## 4. Mira e precisão\n',
          '```\nθ₀  = 1e-9 · u / sqrt(CWU/t ÷ 1000)        [rad]  erro de apontamento\nθ_T = 2e-10 · max(0, T_cano − 300) / 100     [rad]  deriva térmica\nσ   = d · (θ₀ + θ_T)                         [m]    erro no alvo\nA   = max(0, 1 − σ / R_alvo)                        precisão (R_alvo = 5 km)\nu   = fator de mira dos upgrades (1; ASTR 0,7; DEEP 0,35; KUIP 0,175)\n```\n',
          table(['CWU/t', 'u', 'T do cano (K)', 'Lua A', 'Psique A', 'Nexus-1 A'], [
              [c, u, t] + [fmt(max(0, 1 - d * 1e6 * (1e-9 * u / math.sqrt(c / 1000) + 2e-10 * max(0, t - 300) / 100) / 5000)) for d in (384, 3.7e5, 7.5e6)]
              for c, u, t in ((1000, 1, 300), (16000, 1, 300), (16000, 0.35, 300), (16000, 0.35, 900), (128000, 0.175, 300), (1024000, 0.175, 300), (1024000, 0.175, 1200))]),
          'Alvos distantes exigem muita computação **e** cano frio. Psique e Nexus-1 só ficam viáveis com upgrades de mira (seção 7).\n',
          '## 5. Cano: calor e desgaste\n',
          '```\nΔT_tiro  = (1 − η) · E_tiro / C_cano          C_cano = 2e9 EU/K\nQ_frio   = k_ref · vazão_refrigerante          [EU/s]\nW       += E_tiro / E_desgaste(revestimento)    o revestimento falha em W = 1\n```\n',
          table(['Revestimento', 'E_desgaste (EU)', 'Tiros de 1e12 EU'], [
              (n, fmt(e), fmt(e / 1e12)) for n, e in (('Tungstênio-Carbeto', 5e13), ('Neutrônio', 4e14), ('Grafeno-Neutrônio', 3e15), ('Infinity', 1e17))]),
          'Revestimento gasto falha o tiro (energia perdida, cano a +400 K). A troca é pelo hatch de revestimento, sem desmontar nada.\n',
          '## 6. Banco de capacitores\n',
          '```\nE_max(anéis) = 4e12 · 2^(anéis − 1)  EU\ncarga        = limitada pela entrada (hatches/lasers)\n```\n',
          table(['Anéis', 'E_max (EU)', 'Tempo de carga com 2^31 EU/t (s)'], [
              (n, fmt(4e12 * 2 ** (n - 1)), fmt(4e12 * 2 ** (n - 1) / 2 ** 31 / 20)) for n in (1, 2, 3, 4)]),
          '## 7. Upgrades\n',
          'Comprados com **Fragmentos de Telemetria**, ganhos nos marcos. Mesmo esquema da Godforge: pré-requisitos ligados e custo crescente.\n',
          upgrades([
              ['START', 0, '—', 'Comissionamento', 'Anel 1, Lua e Fobos, projétil de tungstênio, η = 0,35'],
              ['RAIL', 1, 'START', 'Trilhos Supercondutores', 'η += 0,10'],
              ['COLD', 1, 'START', 'Cano Criogênico', 'C_cano × 2; deriva térmica × 0,5'],
              ['ASTR', 1, 'START', 'Efemérides', 'libera Vesta, Ceres; u = 0,7'],
              ['CAPS', 2, 'ASTR', 'Cápsulas Ablativas', 'r = 0,75'],
              ['RING2', 3, 'RAIL', 'Segundo Anel', 'constrói o anel 2'],
              ['WC', 2, 'START', 'Revestimento de Carbeto', 'libera revestimento WC e projétil WC'],
              ['MELT', 2, 'RAIL', 'Recuperação Fundida', 'regime de fusão sai direto em fluido'],
              ['DEEP', 3, 'ASTR', 'Rede de Espaço Profundo', 'libera Psique, Europa; u = 0,35'],
              ['OSIR', 3, 'WC', 'Projétil de Ósmio-Irídio', 'libera projétil OsIr'],
              ['VAPR', 4, 'MELT', 'Coletor de Plasma', 'regime de vaporização sai em plasma'],
              ['RING3', 5, 'RING2', 'Terceiro Anel', 'constrói o anel 3'],
              ['SALVO', 4, 'RING2', 'Salva Dupla', 'dois projéteis por descarga, mesma energia dividida'],
              ['NEUT', 5, 'OSIR', 'Revestimento de Neutrônio', 'revestimento e projétil de neutrônio'],
              ['KUIP', 6, 'DEEP', 'Sonda Transnetuniana', 'libera Arrokoth; u = 0,175'],
              ['RELA', 7, 'VAPR', 'Regime Relativístico', 'libera tabela de isótopos exóticos'],
              ['RING4', 8, 'RING3', 'Quarto Anel', 'constrói o anel 4'],
              ['NEXUS', 10, 'KUIP', 'Coordenada Nexus-1', 'libera o remanescente exótico'],
              ['DEGEN', 10, 'NEUT', 'Projétil Degenerado', 'libera projétil de matéria degenerada'],
              ['OMEGA', 12, 'NEXUS, RELA, RING4', 'Lança Absoluta', 'η = 0,85; recuperação 0,95; fila de cápsulas infinita'],
          ]),
          '## 8. Marcos\n',
          'Cada marco tem 7 níveis e dá fragmentos iguais ao nível, como na Godforge.\n',
          milestones([('Energia descarregada (EU)', 1e14, 8), ('Massa recuperada (kg)', 1e6, 5), ('Tiros', 1000, 4), ('Corpos atingidos', 1, 1)]),
          '## 9. Falhas\n',
          '- **Revestimento gasto**: tiro falha, energia perdida, +400 K no cano.',
          '- **Cano acima de 1500 K**: tiro bloqueado até esfriar; acima de 2500 K o revestimento trinca (W = 1).',
          '- **Precisão < 0,1**: o tiro passa do alvo e não volta nada.',
          '- **Fila de cápsulas cheia**: cápsulas excedentes se perdem.\n',
          '## 10. Automação\n',
          'Projéteis e revestimentos por AE2. O cartucho de alvo (item) define corpo e projétil; um AE2 com vários cartuchos faz rotação de alvos. O Barramento ME de Retorno é obrigatório.\n']
    return '\n'.join(md)


# ---------------------------------------------------------------------------------------------------------
# 2. Dimensional Rift Gate
# ---------------------------------------------------------------------------------------------------------
def rift():
    md = ['# Portão de Fenda Dimensional (UIV)\n',
          '> Ficha de design, versão 1.\n',
          '## 1. Visão geral\n',
          '- **Tipo:** exploração de dimensões procedurais. Cada semente é um lugar com saída própria.',
          '- **Estrutura:** anel vertical 126 × 126 × 54 com 8 espinhos; cada espinho é um **Pilone de Âncora**.',
          '- **Energia:** wireless EU (como a Godforge) mais **matéria exótica** para estabilidade.',
          '- **Ciclo:** sintonizar → estabilizar → aprofundar → extrair → fechar ou perder a fenda.\n',
          '## 2. Sintonia\n',
          'Cada semente esconde um ótimo `(f*, φ*, A*)`. O jogador ajusta frequência `f` (1–1000 THz), fase `φ` (0–360°) e amplitude `A` (0–100%).\n',
          '```\nR = exp( −((f − f*)/σf)² − (Δφ/σφ)² − ((A − A*)/σA)² )      ressonância, 0..1\nσf = 40 THz · 0,8^sondas    σφ = 30° · 0,8^sondas    σA = 15% · 0,8^sondas\n```\n',
          'Cada **Sonda de Fenda** lançada estreita as tolerâncias (σ) daquela semente em 20%. A GUI mostra um padrão de interferência que fica mais nítido com R.\n',
          table(['Sondas', 'σf (THz)', 'σφ (°)', 'σA (%)', 'Erro para R ≥ 0,9 em f'], [
              (n, fmt(40 * 0.8 ** n), fmt(30 * 0.8 ** n), fmt(15 * 0.8 ** n), f'±{fmt(40 * 0.8 ** n * math.sqrt(-math.log(0.9)))} THz') for n in (0, 2, 4, 6, 8, 10)]),
          '## 3. Estabilidade\n',
          '```\ndS/dt = κ · ṁ_exótica − λ₀ · (1 − R) · (1 + D/10) − λ_P · (8 − pilones_ativos)\nκ = 2 %/L    λ₀ = 1,5 %/s    λ_P = 0,4 %/s\n```\n',
          '`S` vai de 0 a 100. `D` é a profundidade (seção 4). Em `S = 0` a fenda colapsa.\n',
          table(['R', 'D', 'Pilones', 'Matéria exótica para manter S (L/s)'], [
              (r, d, p, fmt((1.5 * (1 - r) * (1 + d / 10) + 0.4 * (8 - p)) / 2)) for r, d, p in
              ((0.5, 1, 8), (0.9, 1, 8), (0.9, 10, 8), (0.98, 10, 8), (0.98, 30, 8), (0.98, 30, 6), (0.995, 60, 8))]),
          '## 4. Profundidade e saída\n',
          '```\nD sobe 1 por âncora de profundidade inserida (item consumível), máximo pelo upgrade\nsaída/s = B_bioma · R² · D^1,5 · (S/100)\n```\n',
          table(['D', 'Multiplicador D^1,5', 'Tabela liberada'], [
              (d, fmt(d ** 1.5), t) for d, t in ((1, 'superfície'), (5, 'subsolo'), (10, 'manto'), (20, 'núcleo'), (40, 'fronteira'), (80, 'vazio entre dimensões'))]),
          '### 4.1 Biomas (sorteados pela semente)\n',
          table(['Bioma', 'Peso', 'Saída base', 'Regra própria'], [
              ('Planície cristalina', 30, 'gemas, sílica, Ti', '—'),
              ('Oceano de mercúrio', 20, 'Hg, Au, Tl', 'R decai 2× mais rápido'),
              ('Mundo-forja', 15, 'metais fundidos, magma', 'aquece os pilones: +calor'),
              ('Floresta de esporos', 15, 'biomassa, enzimas, DNA alienígena', 'saída para a linha de bio'),
              ('Abismo de antimatéria', 8, 'traços de antimatéria', 'ressonância < 0,95 causa aniquilação'),
              ('Relíquia de civilização', 7, 'circuitos e ligas desconhecidas', 'só aparece com D ≥ 20'),
              ('Vazio', 5, 'Matéria de Fenda pura', 'só com D ≥ 40'),
          ]),
          '## 5. Eventos\n',
          '- **Ressonância em cascata**: R ≥ 0,98 por 60 s seguidos → chance de 5%/min de **Singularidade de Fenda** (item raro, usado no upgrade final).',
          '- **Colapso**: S = 0 → perde as âncoras de profundidade e a fenda fecha. A semente continua anotada.',
          '- **Inversão**: R < 0,2 por 10 s → a fenda inverte e consome matéria exótica em dobro até fechar.\n',
          '## 6. Upgrades\n',
          'Comprados com **Coordenadas Estáveis**.\n',
          upgrades([
              ['START', 0, '—', 'Abertura', '4 pilones, D máx. 5, biomas de peso ≥ 15'],
              ['PROBE', 1, 'START', 'Lançador de Sondas', 'libera Sondas de Fenda'],
              ['PYL6', 2, 'START', 'Pilones Adicionais', '6 pilones'],
              ['DEEP1', 2, 'PROBE', 'Âncoras Reforçadas', 'D máx. 20'],
              ['LOCK', 3, 'PROBE', 'Trava de Fase', 'σφ não muda ao reabrir a mesma semente'],
              ['PYL8', 4, 'PYL6', 'Coroa Completa', '8 pilones'],
              ['DAMP', 3, 'PYL6', 'Amortecedor', 'λ₀ × 0,7'],
              ['ATLAS', 3, 'LOCK', 'Atlas de Sementes', 'guarda 16 sementes com seus ótimos'],
              ['DEEP2', 5, 'DEEP1', 'Âncoras de Manto', 'D máx. 40'],
              ['RARE', 5, 'ATLAS', 'Sintonia Fina', 'libera biomas de peso < 15'],
              ['CASC', 6, 'DAMP', 'Cascata Controlada', 'Singularidade de Fenda 2× mais provável'],
              ['TWIN', 8, 'PYL8', 'Fenda Dupla', 'duas sementes abertas ao mesmo tempo'],
              ['VOID', 10, 'DEEP2, RARE', 'Rasgo do Vazio', 'D máx. 80, bioma Vazio'],
              ['ETER', 12, 'VOID, CASC, TWIN', 'Portão Eterno', 'λ₀ = 0 com R ≥ 0,99'],
          ]),
          '## 7. Marcos\n',
          milestones([('Tempo estável (h)', 1, 3), ('Profundidade máxima', 5, 1.6), ('Sementes catalogadas', 3, 2), ('Matéria extraída (kL)', 10, 4)]),
          '## 8. Automação\n',
          'A sintonia aceita valores por cover de dados ou computador (OpenComputers/CC). Uma rotina pode varrer f e φ procurando o máximo de R, como os scripts de automação da Godforge.\n']
    return '\n'.join(md)


# ---------------------------------------------------------------------------------------------------------
# 3. Antimatter Collider Ring
# ---------------------------------------------------------------------------------------------------------
def collider():
    rho = 60 * 50  # ring radius: 60 blocks at 50 m per block (machine scale)
    magnets = [('NbTi', 8.3), ('Nb₃Sn', 12), ('REBCO (HTS)', 20), ('Neutrônio dopado', 45), ('Infinity', 120)]
    processes = [  # name, threshold GeV (centre of mass), cross-section (nb), product
        ('Antiprótons', 5.6, 1e6, 'Antiprótons (gás)'), ('Kaons', 1.0, 1e7, 'Kaons → Píons, Múons'),
        ('Hyperons (Λ, Σ)', 2.5, 2e6, 'Hyperons → matéria estranha'), ('Quarks charm', 10, 1e5, 'Charm Quark'),
        ('Quarks bottom', 40, 1e4, 'Bottom Quark'), ('Bóson de Higgs', 125, 50, 'Higgs Boson'),
        ('Quarks top', 350, 8, 'Top Quark'), ('Plasma de quarks e glúons', 5000, 1, 'QGP (fluido)'),
    ]
    md = ['# Anel Colisor de Antimatéria (UIV)\n',
          '> Ficha de design, versão 1. A física do feixe usa as fórmulas reais de aceleradores; só a escala muda.\n',
          '## 1. Visão geral\n',
          '- **Tipo:** produção de antimatéria e partículas exóticas por colisão de feixes.',
          '- **Estrutura:** 137 × 127 × 155. Eixo injetor (linac), dois anéis de reforço (boosters) e o anel principal.',
          f'- **Escala:** 1 bloco = 50 m. Raio do anel principal ρ = {rho} m.',
          '- **Entradas:** gás de hidrogênio (prótons), hélio líquido, EU, computação.',
          '- **Saídas:** antiprótons e partículas exóticas em armadilhas de Penning.\n',
          '## 2. Estágios\n',
          table(['Estágio', 'Parte da estrutura', 'Energia de saída', 'Tempo'], [
              ('Linac', 'eixo injetor', '0,2 GeV', 'contínuo'),
              ('Booster 1', 'anel giroscópico menor', '8 GeV', '2 s'),
              ('Booster 2', 'anel giroscópico maior', '150 GeV', '6 s'),
              ('Anel principal', 'anel grande', 'até E_max (seção 3)', 'rampa de 20 s'),
          ]),
          '## 3. Energia máxima do feixe\n',
          'Fórmula real de rigidez magnética:\n',
          '```\np [GeV/c] = 0,3 · B [T] · ρ [m]\nE_cm      = 2 · E_feixe        (feixes contrarrotativos, mesma energia)\n```\n',
          table(['Ímã', 'B (T)', 'E_feixe máx (TeV)', 'E_cm (TeV)', 'Hélio (L/s por ímã-tier)'], [
              (n, fmt(b), fmt(0.3 * b * rho / 1000), fmt(0.6 * b * rho / 1000), fmt(0.5 * 2 ** i)) for i, (n, b) in enumerate(magnets)]),
          '## 4. Luminosidade e taxa de eventos\n',
          '```\nL      = f_rev · n_b · N² / (4π · σx · σy)\nf_rev  = c / (2π · ρ)\neventos/s = σ_processo · L\n```\n',
          f'Com ρ = {rho} m, `f_rev = {fmt(3e8 / (2 * math.pi * rho))} Hz`. `n_b` (pacotes) e `N` (prótons por pacote) sobem com upgrades; `σx·σy` cai com o foco, que gasta computação.\n',
          table(['n_b', 'N', 'σ (µm)', 'L (cm⁻² s⁻¹)'], [
              (nb, fmt(n), s, fmt(3e8 / (2 * math.pi * rho) * nb * n * n / (4 * math.pi * (s * 1e-4) ** 2)))
              for nb, n, s in ((10, 1e10, 50), (100, 1e11, 20), (1000, 1e11, 16), (2808, 1.15e11, 16))]),
          '### 4.1 Processos\n',
          'Cada processo só acontece acima do limiar de energia no centro de massa. A taxa é `σ · L`, convertida em itens pela GUI.\n',
          table(['Processo', 'Limiar E_cm', 'σ (nb)', 'Eventos/s com L = 1e34', 'Produto'], [
              (n, f'{fmt(t)} GeV', fmt(s), fmt(s * 1e-33 * 1e34), p) for n, t, s, p in processes]),
          '## 5. Radiação síncrotron e quench\n',
          '```\nP_sr ∝ γ⁴ / ρ²        (prótons: pequena; modo elétron: domina)\nQ_ímãs = P_sr + Q_feixe_perdido\nquench se Q_ímãs > capacidade do hélio\n```\n',
          'Quench descarrega o feixe no **Beam Dump**, ferve o hélio do setor e exige `60 s × tier do ímã` de resfriamento antes de religar.\n',
          '## 6. Armadilhas de Penning\n',
          '```\ncapacidade = 1e12 antipartículas · 4^(tier − 1)\nconsumo    = 2^(tier + 20) EU/t, contínuo\nsem energia: aniquilação, E = 2·m·c² do conteúdo, dano à estrutura\n```\n',
          table(['Tier', 'Capacidade', 'Energia liberada se falhar (J)'], [
              (t, fmt(1e12 * 4 ** (t - 1)), fmt(1e12 * 4 ** (t - 1) * 2 * 1.67e-27 * 9e16)) for t in (1, 2, 3, 4, 5)]),
          '## 7. Upgrades\n',
          'Comprados com **Eventos Catalogados** (marcos).\n',
          upgrades([
              ['START', 0, '—', 'Primeiro Feixe', 'NbTi, n_b = 10, armadilha tier 1'],
              ['BUNCH', 1, 'START', 'Compressão de Pacotes', 'n_b × 10'],
              ['NB3SN', 2, 'START', 'Ímãs de Nb₃Sn', 'B = 12 T'],
              ['FOCUS', 2, 'BUNCH', 'Quadrupolos de Foco Final', 'σ × 0,4 (gasta computação)'],
              ['TRAP2', 2, 'START', 'Armadilha Tier 2', 'capacidade × 4'],
              ['COOL', 3, 'NB3SN', 'Criogenia em Cascata', 'hélio × 0,6'],
              ['HTS', 4, 'NB3SN', 'Ímãs REBCO', 'B = 20 T'],
              ['STOCH', 4, 'FOCUS', 'Resfriamento Estocástico', 'antiprótons × 3'],
              ['TRAP3', 4, 'TRAP2', 'Armadilha Tier 3', 'capacidade × 4'],
              ['ELEC', 5, 'COOL', 'Modo Elétron-Pósitron', 'libera processos limpos (Higgs × 4), P_sr alta'],
              ['NEUT', 7, 'HTS', 'Ímãs de Neutrônio', 'B = 45 T'],
              ['QGP', 8, 'NEUT', 'Colisão de Íons Pesados', 'libera plasma de quarks e glúons'],
              ['INF', 12, 'NEUT, STOCH, TRAP3', 'Ímãs Infinity', 'B = 120 T, quench nunca acontece'],
          ]),
          '## 8. Marcos\n',
          milestones([('Integral de luminosidade (fb⁻¹)', 1, 4), ('Antipartículas guardadas', 1e12, 6), ('Processos descobertos', 1, 1), ('Horas sem quench', 2, 2)]),
          ]
    return '\n'.join(md)


# ---------------------------------------------------------------------------------------------------------
# 4. Stellar Containment Chamber
# ---------------------------------------------------------------------------------------------------------
def star():
    G, c, Msun = 6.674e-11, 2.998e8, 1.989e30
    R = 12e3
    EU_PER_J = 1e-20  # converts astrophysical joules into EU (machine scale)

    def erot(m, P):
        I = 0.4 * m * Msun * R * R
        return 0.5 * I * (2 * math.pi / P) ** 2

    def eta_bh(a):
        return 1 - math.sqrt((1 + math.sqrt(1 - a * a)) / 2)

    md = ['# Câmara de Contenção Estelar (MAX)\n',
          '> Ficha de design, versão 1. Astrofísica real com escala de jogo `1 J = 1e-20 EU`.\n',
          '## 1. Visão geral\n',
          '- **Tipo:** gerador e fonte de matéria degenerada a partir de uma estrela de nêutrons presa em campos.',
          '- **Estrutura:** esfera de 93³; casco de Radiant Naquadah, vidro de campo de plasma e **bandas de contenção** de neutrônio.',
          '- **Saída:** EU em quantidade absurda, neutrônio, matéria degenerada; depois do colapso, energia da ergosfera.',
          '- **Estado:** a estrela é persistente. Não há "receita"; há uma estrela com massa, rotação e crosta.\n',
          '## 2. Estado da estrela\n',
          '```\nM  massa (M☉)         P  período de rotação (s)        R = 12 km\nI  = 0,4 · M · R²     ω = 2π / P\nE_rot = ½ · I · ω²     energia de rotação\n```\n',
          table(['M (M☉)', 'P (ms)', 'E_rot (J)', 'E_rot (EU)'], [
              (fmt(m), fmt(p * 1000), fmt(erot(m, p)), fmt(erot(m, p) * EU_PER_J)) for m, p in
              ((1.2, 0.033), (1.4, 0.0016), (1.4, 0.01), (1.8, 0.0016), (2.1, 0.0014))]),
          '## 3. Extração\n',
          'O jogador escolhe a potência de extração `P_ext`. A rotação cai conforme a energia sai:\n',
          '```\ndE_rot/dt = −P_ext − P_dipolo\nP_dipolo  = B²·R⁶·ω⁴ / (6c³)          perda natural (frenagem magnética)\nω_novo    = sqrt(2 · E_rot / I)\n```\n',
          'Quanto mais rápido a estrela gira, mais energia ela guarda, mas mais ela perde sozinha por frenagem.\n',
          '## 4. Alimentação (spin-up)\n',
          'Alimentar matéria aumenta a massa **e** a rotação, como um pulsar reciclado real:\n',
          '```\nΔJ = ṁ · sqrt(G · M · R)       momento angular entregue pelo disco\nΔM = ṁ · (1 − 0,15)            15% sai como energia de ligação (vira EU na hora)\n```\n',
          '## 5. Limite de colapso\n',
          '```\nM_TOV = 2,2 M☉   (2,4 M☉ com o upgrade EOS)\nM > M_TOV  →  colapso em buraco negro (irreversível)\na* = J · c / (G · M²)    limitado a 0,998\n```\n',
          '### 5.1 Modo buraco negro\n',
          'Depois do colapso a máquina passa a extrair energia da ergosfera (processo de Penrose). Eficiência máxima real:\n',
          '```\nη(a*) = 1 − sqrt( (1 + sqrt(1 − a*²)) / 2 )\nE_extraível = η · M · c²\n```\n',
          table(['a*', 'η', 'E_extraível para 2,3 M☉ (EU)'], [
              (fmt(a), fmt(eta_bh(a)), fmt(eta_bh(a) * 2.3 * Msun * c * c * EU_PER_J)) for a in (0.1, 0.5, 0.7, 0.9, 0.99, 0.998)]),
          'Colapsar com rotação alta vale muito mais. O jogador decide quando "dar o salto".\n',
          '## 5.2 Balanço contra os geradores atuais\n',
          'A câmara só faz sentido se render mais que o Artificial Star. Números atuais do GTNA (barra = 200 ticks, antes de overclock) e proposta de nerf:\n',
          table(['Gerador', 'EU/t hoje', 'EU por barra/ciclo hoje', 'Proposta de nerf', 'EU/t depois'], [
              ('Artificial Star, barra de Neutrônio', fmt(2 ** 43), fmt(2 ** 43 * 200), '÷ 64', fmt(2 ** 43 / 64)),
              ('Artificial Star, barra de Draconium', fmt(2 ** 47), fmt(2 ** 47 * 200), '÷ 128', fmt(2 ** 47 / 128)),
              ('Artificial Star, barra Cósmica', fmt(2 ** 51), fmt(2 ** 51 * 200), '÷ 256', fmt(2 ** 51 / 256)),
              ('Artificial Star, barra de Infinity', fmt(2 ** 55), fmt(2 ** 55 * 200), '÷ 512', fmt(2 ** 55 / 512)),
              ('Câmara Estelar, pulsar de milissegundo', '—', f'E_rot = {fmt(erot(1.4, 0.0016) * EU_PER_J)}', '—', f'até {fmt(2 ** 60)} (bandas tier 4)'),
              ('Câmara Estelar, buraco negro a* = 0,998', '—', f'{fmt(eta_bh(0.998) * 2.3 * Msun * c * c * EU_PER_J)} total', '—', f'até {fmt(2 ** 62)}'),
          ]),
          'Com o nerf, a melhor barra do Artificial Star fica em 2^46 EU/t. A câmara começa em 2^56 com bandas tier 1 e chega a 2^60, '
          'e um pulsar de milissegundo guarda energia para cerca de 6 dias de extração máxima antes de precisar de spin-up. '
          'O overclock do Artificial Star (até 16 OCs, 4×/4×) também precisa de teto, senão o nerf some. Proposta: no máximo 4 OCs.\n',
          '## 5.3 Hatches novos\n',
          table(['Hatch', 'Função', 'Inspiração'], [
              ('Injetor de Massa', 'recebe matéria (itens/fluidos) e converte em ṁ no disco de acreção', 'BEC Hatch (GTNH)'),
              ('Extrator Rotacional', 'saída de energia; só aceita laser ou Nexus Network, nunca dínamo comum', '—'),
              ('Sonda Sísmica', 'registra tremores; sem ela o sismograma não funciona', '—'),
              ('Gerador de Banda', 'um por banda; define o tier e a capacidade da banda', 'Graviton Flow Modulator (Godforge)'),
              ('Coletor de Ejeção', 'barramento ME que recebe a Matéria Degenerada dos tremores', '—'),
          ]),
          '## 6. Tremores estelares\n',
          '```\ntensão σ += k · |Δω| / ω             acumula conforme a rotação muda\ntremor quando σ ≥ 1                   libera E_tremor = 1e-6 · E_rot\nbandas absorvem até C_bandas; o excedente danifica o casco\n```\n',
          table(['Bandas (tier)', 'C_bandas (EU)', 'Consumo contínuo (EU/t)'], [
              (t, fmt(1e15 * 10 ** t), fmt(2 ** (40 + 2 * t))) for t in (1, 2, 3, 4)]),
          '## 7. Saídas de matéria\n',
          table(['Fonte', 'Taxa', 'Produto'], [
              ('Mineração da crosta', '`1e-9 · P_ext` kg/s', 'Neutrônio (poeira)'),
              ('Ejeção em tremor', 'por evento, ∝ E_tremor', 'Matéria Degenerada'),
              ('Disco de acreção', '15% do ṁ', 'Plasma estelar'),
              ('Modo buraco negro', 'com `P_ext` > 0', 'Radiação Hawking condensada (traço)'),
          ]),
          '## 8. Upgrades\n',
          'Comprados com **Fragmentos de Crosta**.\n',
          upgrades([
              ['START', 0, '—', 'Captura', 'estrela de 1,2 M☉, P = 33 ms, bandas tier 1'],
              ['FEED', 1, 'START', 'Disco de Acreção', 'libera alimentação (spin-up)'],
              ['BAND2', 2, 'START', 'Bandas Tier 2', 'C_bandas × 10'],
              ['DIPO', 2, 'START', 'Blindagem de Dipolo', 'P_dipolo × 0,5'],
              ['CRUST', 3, 'FEED', 'Mineração de Crosta', 'neutrônio × 4'],
              ['SEIS', 3, 'BAND2', 'Sismógrafo Estelar', 'prevê tremores com 30 s de antecedência'],
              ['RECY', 4, 'FEED', 'Pulsar Reciclado', 'ΔJ × 1,5'],
              ['BAND3', 5, 'BAND2', 'Bandas Tier 3', 'C_bandas × 10'],
              ['EOS', 6, 'CRUST', 'Equação de Estado Exótica', 'M_TOV = 2,4 M☉'],
              ['BAND4', 8, 'BAND3', 'Bandas Tier 4', 'C_bandas × 10'],
              ['ERGO', 10, 'EOS, SEIS', 'Coletor de Ergosfera', 'libera o modo buraco negro sem perder a estrutura'],
              ['KERR', 12, 'ERGO, RECY, BAND4', 'Máquina de Kerr', 'η do buraco negro × 1,2 (acima do limite clássico: ficção)'],
          ]),
          '## 9. Marcos\n',
          milestones([('Energia extraída (EU)', 1e18, 9), ('Massa alimentada (M☉ × 1e-3)', 1, 4), ('Tremores contidos', 5, 3), ('Dias com a mesma estrela', 1, 2)]),
          ]
    return '\n'.join(md)


WIP = '''!!! warning "Em desenvolvimento"
    Esta máquina ainda não está pronta no jogo. A ficha descreve o design aprovado; números e detalhes podem mudar no balanço.

'''


STATUS = {
    'camara-estelar': (['Estrutura de 93³ convertida da sua construção; o núcleo degenerado (raio 7) some ao acender e volta ao desligar',
                        'Física completa em `StellarCore`: rotação, alimentação, frenagem, tremores, regiões, colapso em buraco negro (teste `StellarCoreTest`)',
                        'Energia entregue na rede Nexus do dono; bandas pagam manutenção pela rede',
                        'Render da estrela, feixes de pulsar, linhas de campo, coroa e disco de acreção',
                        'GUI em texto com extração ajustável e campo magnetar; gametest de formação, alimentação e núcleo',
                        'Aba gráfica com o diagrama Massa–Período (trilha da estrela, limite TOV e curva de ruptura de Kepler)'],
                       ['Sismograma dos tremores desenhado', 'Lente gravitacional no jogo',
                        'Hatches próprios (Injetor de Massa, Sonda Sísmica)', 'Receita do controlador (fica com o modpack)']),
    'anel-colisor': (['Estrutura de 155×127×137; anel e giroscópios já marcados no padrão para girar',
                      'Física em `ColliderCore`: rigidez magnética, luminosidade, 5σ, quench, armadilhas de Penning, propostas (teste `ColliderCoreTest`)',
                      'Hélio líquido pelos hatches, ímãs e armadilhas pela rede; partículas contidas como itens',
                      'Render dos dois feixes contrarrotativos e do núcleo pulsando; gametest de formação, produção e física',
                      'Anel e giroscópios saem do mundo ao ligar e giram em sentidos opostos (como a Forja dos Deuses); voltam ao desligar',
                      'Aba gráfica com o quadro do Modelo Padrão (significância de cada partícula até 5σ)'],
                     ['Aba do comitê de tempo de feixe (propostas feitas, ativa e progresso) — feito', 'Beam Dump e hatch de detector', 'Receita do controlador']),
    'portao-de-fenda': (['Estrutura de 126×126×54 convertida da sua construção',
                         'Sintonia, estabilidade, profundidade, harmônicos, partitura e atlas em `RiftCore` (teste `RiftCoreTest`)',
                         'Botões de sintonia na GUI; SpaceTime estabiliza; sondas e âncoras pelos barramentos; saída por bioma',
                         'Render do horizonte de eventos com a cor do bioma; gametest de formação e estabilidade',
                         'Aba gráfica com o sismógrafo da fenda (traço da estabilidade e barra de ressonância)'],
                        ['Aba do atlas (roda de harmônicos, partitura e fendas mapeadas) — feito', 'Núcleos de pilone nos espinhos', 'Uso da Singularidade de Fenda', 'Receita do controlador']),
    'lanca-cinetica-orbital': (['Estrutura de 242×130×142 convertida da sua construção; base e canhão separados no padrão',
                                'Tiro, mira, regimes, cano, banco, levantamento e bancada em `LanceCore` (teste `LanceCoreTest`)',
                                'Banco carregado pela rede; projéteis de lingotes; cápsulas devolvem os materiais de cada corpo',
                                'Render do clarão e do rastro de plasma; gametest de formação, tiro e retorno',
                                'O canhão sai do mundo ao ligar e gira no render até o alvo selecionado',
                                'Mira usa CWU real do hatch de computação óptica (sem hatch a mira fica cega)',
                                'Aba gráfica com o mapa orbital (corpos, alvo e CWU)'],
                               ['Aba da bancada (massa, calor, indutância e peças) — feito', 'Clarão do tiro acompanha a rotação do canhão — feito', 'Hatches de revestimento e cartucho', 'Receita do controlador']),
}

MOCKUPS = {'lanca-cinetica-orbital': ['lance_survey', 'lance_bench'], 'portao-de-fenda': ['rift_score', 'rift_atlas'],
           'anel-colisor': ['collider_sm', 'collider_beam'], 'camara-estelar': ['star_mp']}


def main():
    os.makedirs(OUT, exist_ok=True)
    import re
    import progression
    for name, fn, prog in (('lanca-cinetica-orbital', lance, progression.lance), ('portao-de-fenda', rift, progression.rift),
                           ('anel-colisor', collider, progression.collider), ('camara-estelar', star, progression.star)):
        text = fn()
        # Replace the Godforge-style upgrades + milestones with the machine's own progression system.
        a = re.search(r'^## \d+\. Upgrades', text, re.M).start()
        m = re.search(r'^## \d+\. Marcos.*?(?=^## |\Z)', text, re.M | re.S)
        text = text[:a] + prog() + '\n' + text[m.end():]
        head, rest = text.split('\n', 1)
        text = head + '\n\n' + WIP + rest
        done, todo = STATUS.get(name, ([], []))
        if done:
            text += '\n## Estado da implementação\n\n**No código:**\n\n' + ''.join(f'- {d}\n' for d in done)
            text += '\n**Falta:**\n\n' + ''.join(f'- {d}\n' for d in todo)
        shots = MOCKUPS.get(name, [])
        if shots: text += '\n## Telas (mockup)\n\n' + ''.join(f'![{s}](mockups/gt/{s}.png){{ loading=lazy }}\n\n' for s in shots)
        open(os.path.join(OUT, name + '.md'), 'w', encoding='utf-8').write(text)
        print(name)


if __name__ == '__main__':
    main()
