"""Design spec of the IV Pressurized Water Reactor. Tables are computed from the formulas in the text.

    python3 tools/design/pwr_spec.py   ->  docs/roadmap/design/reator-pwr.md
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from endgame_specs import fmt, table  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
OUT = os.path.join(ROOT, 'docs/roadmap/design/reator-pwr.md')

# --- constants (game values; real values noted in the text) ------------------------------------------------
P_NOM = 131072           # nominal thermal power, EU/t (16 A IV)
STEAM_PER_EU = 2         # L of steam per EU of thermal power
TIME_SCALE = 60          # 1 real hour of isotope physics = 1 game minute
BETA, LAMBDA_GEN, LAM_D = 650e-5, 2e-5, 0.08
ROD_WORTH = 8000         # pcm, all banks
BORON_WORTH = -10        # pcm/ppm
ALPHA_DOP, ALPHA_MOD = -2.5, -40   # pcm/K
LEAK = 0.97


def k0(e): return 0.92 + 0.075 * e
def kinf(e, b): return k0(e) - 0.006 * b
def bmax(e): return (k0(e) * LEAK - 1) / (0.006 * LEAK)
def rho_pcm(k): return (k - 1) / k * 1e5
def rod_frac(x): return x - math.sin(2 * math.pi * x) / (2 * math.pi)
def V(x): return (2 * x - 1) * math.log(x / (1 - x))


def swu(xp, xf=0.00711, xt=0.0025):
    F = (xp - xt) / (xf - xt); T = F - 1
    return V(xp) + T * V(xt) - F * V(xf), F


def xenon_after_trip(minutes):
    """Real I-135/Xe-135 equations, time compressed by TIME_SCALE. Values relative to full-power equilibrium Xe."""
    li, lx = math.log(2) / 6.57, math.log(2) / 9.14            # per real hour
    gi, gx = 0.0639, 0.00237
    sig_phi = 2.6e-18 * 3e13 * 3600                              # sigma_a(Xe) * phi, per real hour at 100%
    fiss = 1.0
    I0 = gi * fiss / li
    X0 = (gx + gi) * fiss / (lx + sig_phi)
    out = []
    for m in minutes:
        t = m  # one game minute equals one real hour
        X = X0 * math.exp(-lx * t) + I0 * li / (lx - li) * (math.exp(-li * t) - math.exp(-lx * t))
        out.append(X / X0)
    return out


def decay_heat(t, T_op=3.15e7):
    return 0.066 * (t ** -0.2 - (t + T_op) ** -0.2)


def main():
    md = []
    a = md.append
    a('# Reator de Água Pressurizada (IV)\n')
    a('''!!! warning "Em desenvolvimento"
    Esta máquina ainda não está pronta no jogo. A ficha descreve o design aprovado; números e detalhes podem mudar no balanço.

''')
    a('> Ficha de design, versão 2 (opção A escolhida). Tabelas calculadas por `tools/design/pwr_spec.py`. '
      'A física é a de um PWR real, com escala de tempo e de potência de jogo. Os números finais de balanço ficam com o modpack.\n')
    a('## 1. Visão geral\n')
    a('- **Tipo:** gerador térmico. O reator produz **Vapor de Alta Pressão**; turbinas separadas convertem em EU.')
    a('- **Tier:** IV. Todos os blocos e componentes são da era IV (tungstênio-aço, Inconel 625, Hastelloy-N, carbeto de boro, PBI).')
    a(f'- **Potência nominal:** {fmt(P_NOM)} EU/t térmicos (16 A IV). Vapor: {fmt(P_NOM * STEAM_PER_EU)} L/t.')
    a('- **Estrutura:** contenção ≈ 47 × 48 × 47 + torre de resfriamento de 66 blocos.')
    a('- **Filosofia:** complexo de projetar, simples de manter. Tudo que exige atenção contínua tem um modo automático '
      'configurável uma vez (setpoint, programa de boro, campanha de recarga). O jogador projeta a usina; não fica de babá.\n')

    a('## 2. Estrutura e materiais\n')
    a(table(['Parte', 'Bloco (era IV)', 'Função'], [
        ('Contenção externa', 'High Strength Concrete', 'barreira final; precisa estar completa para ligar'),
        ('Liner da contenção', 'PBI Radiation Resistant Mechanical Enclosure', 'estanqueidade; vazamento aqui = zona radioativa'),
        ('Janelas de inspeção', 'Tungsten Borosilicate Glass', 'anel no nível do piso de operação'),
        ('Blindagem primária', 'Radiation Absorbent Casing', 'cavidade do reator'),
        ('Vaso de pressão e tampa', 'Robust Tungstensteel Machine Casing', 'aguenta 155 bar'),
        ('Barras de controle (CRDM)', 'Boron Carbide Ceramic Radiation Resistant Cube', '5 bancos de barras, movidos pela GUI'),
        ('Canais de combustível', 'Fission Reactor Casing', 'cada canal recebe um conjunto combustível'),
        ('Geradores de vapor (4)', 'Inconel 625 Casing', 'troca de calor primário → secundário'),
        ('Tubulação primária', 'Inconel 625 Pipe Casing', 'pernas quente, fria e de cruzamento'),
        ('Bombas do primário (4)', 'Tungstensteel Gearbox + IV Machine Hull', 'vazão do primário; gastam EU'),
        ('Pressurizador', 'Hastelloy-N 75 Casing', 'controla a pressão (aquecedores e spray)'),
        ('Linha de surto/spray', 'High Pressure Pipe Casing', 'liga pressurizador e perna quente'),
        ('Fundo do canal de recarga', 'Zirconia Ceramic Mechanical Block', 'resistente a água borada'),
        ('Piso de operação', 'Grate Machine Casing', '—'),
        ('Ponte rolante polar', 'Tungstensteel Pipe Casing + listras', 'executa a recarga'),
        ('Torre de resfriamento', 'High Strength Concrete', 'rejeita o calor do secundário'),
    ]))
    a('### 2.1 Hatches\n')
    a(table(['Hatch', 'Qtd.', 'Uso'], [
        ('Hatch de Conjuntos Combustíveis', '1', 'entrada de conjuntos novos e saída dos gastos (para a piscina)'),
        ('Entrada de Água de Alimentação', '1–4', 'água desmineralizada do secundário'),
        ('Saída de Vapor de Alta Pressão', '1–4', 'para as turbinas'),
        ('Entrada de Ácido Bórico', '1', 'controle químico de reatividade'),
        ('Entrada/Saída de Água do Primário', '1 + 1', 'reposição e purga (sai contaminada se houver falha de vareta)'),
        ('Energia (IV)', '1–4', 'bombas, aquecedores do pressurizador, ponte rolante'),
        ('Dados / Redstone', 'até 4', 'telemetria e comandos (seção 12)'),
    ]))

    a('## 3. Combustível\n')
    a('O núcleo tem **37 canais**. Cada canal recebe um **Conjunto Combustível** (item) com enriquecimento `e` e queima `B`.\n')
    a('```\nk∞(e, B) = k₀(e) − 0,006 · B          k₀(e) = 0,92 + 0,075 · e     (e em %, B em GWd/t)\nk_núcleo = média dos k∞ · 0,97        (fuga de nêutrons)\nB_max(e) = queima em que o conjunto sozinho deixa de manter o núcleo crítico\n```\n')
    a(table(['Conjunto', 'e (%)', 'k₀', 'B_max (GWd/t)', 'Ciclos de 1/3 do núcleo'], [
        (n, fmt(e), fmt(k0(e)), fmt(bmax(e)), fmt(3 * bmax(e) / bmax(4.5) * 1.0)) for n, e in
        (('LEU-3', 3.0), ('LEU-4', 4.0), ('LEU-4,5', 4.5), ('LEU-5', 5.0))]))
    a('Variantes: **Conjunto com Gadolínia** (Gd₂O₃ como absorvedor queimável: −3000 pcm no início, some até 15 GWd/t; '
      'deixa o boro baixo no começo do ciclo) e, no LuV, **MOX** (Pu reciclado do PUREX).\n')
    a('Queima por tick: `dB/dt = P_canal / massa_U`. Com o núcleo a 100%, um conjunto LEU-4,5 sai em cerca de 3 ciclos. '
      'Um ciclo nominal dura 6 horas de jogo (ajustável no balanço).\n')

    a('## 4. Reatividade\n')
    a('```\nρ = (k − 1)/k                                  em pcm (1 pcm = 1e-5)\nρ_total = ρ_comb + ρ_barras + ρ_boro + ρ_Doppler + ρ_mod + ρ_Xe + ρ_Sm\n'
      f'ρ_barras  = −{ROD_WORTH} pcm · f(x)        f(x) = x − sin(2πx)/(2π)   (curva S real de valor integral)\n'
      f'ρ_boro    = {BORON_WORTH} pcm/ppm · C_B\nρ_Doppler = {ALPHA_DOP} pcm/K · (T_comb − 565 K)\nρ_mod     = {ALPHA_MOD} pcm/K · (T_mod − 565 K)\n```\n')
    a('Os dois coeficientes de temperatura são negativos: o reator se autorregula. Subir a potência esquenta o combustível '
      'e a água, que tiram reatividade. Isso deixa o controle automático estável.\n')
    a('### 4.1 Valor das barras\n')
    a(table(['Inserção x', 'f(x)', 'ρ_barras (pcm)'], [
        (f'{int(x * 100)}%', fmt(rod_frac(x)), fmt(-ROD_WORTH * rod_frac(x))) for x in (0, 0.1, 0.25, 0.5, 0.75, 0.9, 1)]))
    a('As barras valem pouco nas pontas e muito no meio, como num reator real. Ajuste fino se faz com as barras na faixa de 20–40%.\n')

    a('## 5. Cinética\n')
    a(f'Cinética pontual com um grupo de nêutrons atrasados: `β = {fmt(BETA * 1e5)} pcm`, `Λ = {LAMBDA_GEN} s`, `λ = {LAM_D} /s`.\n')
    a('```\ndn/dt = (ρ − β)/Λ · n + λ·C\ndC/dt = β/Λ · n − λ·C\nperíodo estável τ ≈ (β − ρ) / (λ · ρ)\n```\n')
    a(table(['ρ (pcm)', 'Período τ', 'Tempo para dobrar a potência', 'Situação'], [
        (fmt(r), f'{fmt((BETA * 1e5 - r) / (LAM_D * r))} s', f'{fmt((BETA * 1e5 - r) / (LAM_D * r) * math.log(2))} s',
         (lambda tau: 'normal' if tau >= 30 else 'alarme de período' if tau >= 10 else 'SCRAM por período curto')((BETA * 1e5 - r) / (LAM_D * r)))
        for r in (10, 50, 100, 200, 300, 500, 640)]))
    a('Acima de β (650 pcm) o reator fica **pronto-crítico**: a potência dispara em milissegundos. O SCRAM automático por período curto (< 10 s) existe para isso nunca acontecer em operação normal.\n')

    a('## 6. Xenônio e samário\n')
    a('Equações reais do I-135 → Xe-135, com o tempo comprimido (**1 hora real = 1 minuto de jogo**):\n')
    a('```\ndI/dt = γ_I·Σf·φ − λ_I·I\ndX/dt = γ_X·Σf·φ + λ_I·I − λ_X·X − σ_X·φ·X\nmeias-vidas reais: I-135 = 6,57 h, Xe-135 = 9,14 h\nρ_Xe = −2800 pcm · X / X_eq(100%)\n```\n')
    mins = [0, 2, 5, 8, 11, 15, 20, 30, 45, 60]
    xs = xenon_after_trip(mins)
    a(table(['Minutos após desligar', 'Xe / Xe_eq', 'ρ_Xe (pcm)', 'Pode religar com as barras todas fora?'], [
        (m, fmt(x), fmt(-2800 * x), 'sim' if -2800 * x > -2800 - 1500 else 'não') for m, x in zip(mins, xs)]))
    a('Depois de desligar, o xenônio **sobe** por ~10 minutos antes de cair (poço de xenônio). Religar nessa janela exige excesso de reatividade (combustível novo) ou esperar. '
      'O modo automático conhece o poço e mostra na GUI quanto tempo falta para poder religar.\n')

    a('## 7. Boro\n')
    a('A concentração de boro compensa a queima ao longo do ciclo. O programa de boro automático segue a curva abaixo; o jogador só garante ácido bórico e água desmineralizada.\n')
    a('```\nC_B(B) = ρ_excesso(B) / 10        ρ_excesso = ρ_comb(B) − 1000 pcm de margem para as barras\n```\n')
    a(table(['Queima média (GWd/t)', 'k_núcleo', 'ρ_comb (pcm)', 'Boro crítico (ppm)'], [
        (fmt(b), fmt(kinf(4.5, b) * LEAK), fmt(rho_pcm(kinf(4.5, b) * LEAK)), fmt(max(0, (rho_pcm(kinf(4.5, b) * LEAK) - 1000) / 10)))
        for b in (0, 5, 10, 15, 20, 25, 30)]))
    a('Mudar o boro é lento (diluição pela vazão de reposição), por isso as barras cuidam das mudanças rápidas e o boro das lentas.\n')

    a('## 8. Termo-hidráulica\n')
    a('### 8.1 Primário\n')
    a('```\nP_th = n · P_nom\nṁ_prim = P_th / (c_p · ΔT)          ΔT nominal 33 K (292 → 325 °C), 155 bar\nT_comb = T_mod + P_canal · R_th\nDNBR = q_crítico(vazão, pressão) / q_local     precisa ficar > 1,3\n```\n')
    a(table(['Potência', 'Vazão do primário', 'DNBR', 'Estado'], [
        (f'{p}%', f'{f}%', fmt(2.1 * (f / 100) ** 0.8 / (p / 100)), 'ok' if 2.1 * (f / 100) ** 0.8 / (p / 100) > 1.3 else 'SCRAM por DNBR')
        for p, f in ((100, 100), (100, 75), (100, 50), (60, 50), (110, 100), (100, 25))]))
    a('Perder bombas com o reator em potência é a falha clássica do PWR. Com 3 de 4 bombas o reator cai sozinho para 70%; com 2, SCRAM.\n')
    a('### 8.2 Pressurizador\n')
    a('```\npressão sobe  → spray (água fria da perna fria) condensa vapor\npressão desce → aquecedores elétricos (EU) ferve mais água\nalívio a 172 bar: válvula abre e despeja vapor no tanque de alívio (perde água do primário)\n```\n')
    a('### 8.3 Secundário e torre\n')
    a('```\nvapor = 2 L por EU térmico\ncapacidade da torre Q_torre = 4096 EU/t por bloco de altura útil\nP_max = Q_torre / (1 − η_turbina)        η_turbina = 0,33\nreposição de água da torre = 1,8% da água de circulação (evaporação)\n```\n')
    a(table(['Altura útil da torre', 'Q_torre (EU/t)', 'P_th máxima (EU/t)', '% do nominal'], [
        (h, fmt(4096 * h), fmt(4096 * h / 0.67), f'{fmt(4096 * h / 0.67 / P_NOM * 100)}%') for h in (10, 15, 21, 25)]))
    a('Torre menor que o necessário limita a potência. A altura útil é contada pela estrutura (a torre pode ser construída mais alta).\n')

    a('## 9. Bombas e energia própria\n')
    a(table(['Consumidor', 'Consumo', 'Observação'], [
        ('Bombas do primário (4)', f'{fmt(P_NOM * 0.007 / 4)} EU/t cada', '0,7% de P_th, como numa usina real'),
        ('Aquecedores do pressurizador', 'até 2048 EU/t', 'só quando a pressão cai'),
        ('Ponte rolante', '512 EU/t', 'só durante a recarga'),
        ('Remoção de calor residual', '1024 EU/t', 'após desligar, até o calor de decaimento cair'),
    ]))
    a('Sem energia as bombas perdem vazão pela inércia do volante: `vazão(t) = 1 / (1 + t/10 s)`. O SCRAM acontece antes do DNBR cair.\n')

    a('## 10. Calor de decaimento\n')
    a('Fórmula de Way–Wigner (real). Depois do SCRAM o núcleo continua gerando calor e precisa de remoção de calor residual:\n')
    a('```\nP_d / P₀ = 0,066 · [ t^−0,2 − (t + T_op)^−0,2 ]\n```\n')
    a(table(['Tempo após o SCRAM', 'P_d / P₀', 'Calor (EU/t, a partir do nominal)'], [
        (lbl, f'{fmt(decay_heat(t) * 100)}%', fmt(decay_heat(t) * P_NOM)) for lbl, t in
        (('1 s', 1), ('10 s', 10), ('1 min', 60), ('10 min', 600), ('1 h', 3600), ('1 dia', 86400), ('1 mês', 2.6e6))]))
    a('O mesmo calor vale para os conjuntos gastos: eles vão para a **Piscina de Combustível Usado** (multibloco auxiliar) e só podem ir para o reprocessamento depois que o calor cair abaixo de um limite.\n')

    a('## 11. Proteção e falhas\n')
    a('### 11.1 SCRAM automático\n')
    a(table(['Sinal', 'Limite'], [
        ('Fluxo alto', '109% do nominal'), ('Período curto', '< 10 s'), ('Pressão baixa', '< 130 bar'), ('Pressão alta', '> 166 bar'),
        ('Vazão baixa', '< 90% com P > 30%'), ('DNBR baixo', '< 1,3'), ('T_quente alta', '> 340 °C'), ('Perda de energia', 'bombas sem EU'),
        ('Contenção aberta', 'qualquer bloco faltando')]))
    a('### 11.2 Segurança passiva\n')
    a('- **Acumuladores:** tanques de água borada pressurizados com N₂ injetam sozinhos quando a pressão cai abaixo de 45 bar.')
    a('- **Injeção de segurança:** bombas de alta e baixa pressão (consomem EU e água borada).')
    a('- **Contenção:** segura vapor e radioatividade enquanto estiver completa.\n')
    a('### 11.3 Danos em degraus\n')
    a(table(['Degrau', 'Causa', 'Efeito', 'Recuperação'], [
        ('1. Falha de varetas', 'T_comb alto, DNBR < 1 por > 5 s', 'água do primário sai **contaminada**', 'linha de limpeza: resina de troca iônica + evaporador'),
        ('2. Dano ao núcleo', 'perda de refrigeração com P_d alto', 'conjuntos viram **Destroços de Núcleo**', 'recarga completa; destroços vão para reprocessamento especial'),
        ('3. Fusão', 'dano ao núcleo sem injeção de segurança', '**cório** no fundo do vaso; estrutura desmonta', 'remoção do cório (item muito pesado) e reconstrução do vaso'),
        ('4. Liberação', 'fusão com contenção incompleta', 'zona radioativa ao redor', 'só limpeza; sem explosão nuclear'),
    ]))

    a('## 11.4 Distribuição de potência no núcleo\n')
    a('O núcleo não esquenta por igual. A GUI mostra o mapa de potência por canal e duas grandezas reais de operação:\n')
    a('```\nF_q = potência do canal mais quente / potência média      limite 2,5\nAO  = (P_topo − P_base) / (P_topo + P_base)              offset axial, alvo −5% a +5%\n```\n')
    a('- **Padrão de carregamento:** o jogador escolhe onde vai cada conjunto. Conjuntos novos no centro deixam F_q alto; o padrão de baixa fuga '
      '(novos intercalados, gastos na borda) é o que as usinas reais usam e rende mais queima por ciclo. O modo automático sugere um padrão.')
    a('- **Oscilação de xenônio:** em núcleos grandes o xenônio pode oscilar entre topo e base com período real de ~15–30 h (15–30 min de jogo). '
      'O AO mostra a oscilação e o PID amortece com o banco de barras parcial (banco P).')
    a('- **Inclinação de quadrante:** um conjunto errado num quadrante desequilibra a potência. Acima de 2% de inclinação a potência máxima cai.\n')
    a(table(['F_q', 'Margem de potência', 'Efeito'], [
        (fmt(f), f'{fmt(min(100, 100 * 2.5 / f))}%', 'normal' if f <= 2.5 else 'potência limitada automaticamente') for f in (1.8, 2.2, 2.5, 2.8, 3.2)]))
    a('## 11.5 Química do primário\n')
    a(table(['Parâmetro', 'Faixa', 'Como se controla', 'Fora da faixa'], [
        ('Boro', '0–2000 ppm', 'ácido bórico / diluição', 'reatividade errada'),
        ('Lítio (⁷LiOH)', '2–3,5 ppm', 'hatch de química', 'pH baixo: corrosão e **crud** nas varetas'),
        ('pH a 300 °C', '7,0–7,4', 'relação Li/B (coordenada automaticamente)', 'crud: depósito que muda o AO (anomalia CIPS)'),
        ('Oxigênio', '< 5 ppb', 'hidrogênio dissolvido', 'corrosão sob tensão no Inconel'),
        ('Atividade (I-131)', 'baixa', 'resina de troca iônica', 'sinal de vareta furada; pico de iodo após SCRAM'),
    ]))
    a('O lítio-7 é enriquecido de propósito (o ⁶Li vira trítio). Isso liga o reator a uma linha química de separação de isótopos de lítio.\n')
    a('## 11.6 Geradores de vapor e transientes\n')
    a('- **Tubos do gerador:** cada gerador tem 3.388 tubos (número real de um gerador Westinghouse 51). A corrosão trinca tubos com o tempo; '
      'tubo trincado vaza primário para o secundário. Na parada, o jogador **tampona** tubos: cada 1% tamponado tira 0,4% da potência máxima daquele loop.')
    a('- **Rejeição de carga:** se as turbinas param de puxar vapor, o **despejo de vapor** manda o excesso para o condensador da torre por até 40% da potência; '
      'acima disso, SCRAM por pressão alta no secundário.')
    a('- **Pico de iodo:** depois de um SCRAM a atividade do primário sobe por algumas horas; a purga leva água contaminada para a limpeza.\n')
    a('## 12. Automação\n')
    a('Configura-se uma vez:\n')
    a('- **Modo potência:** setpoint de potência (% ou EU/t). Um PID move as barras; o programa de boro segue a seção 7.')
    a('- **Modo seguir carga:** a potência segue a demanda de vapor das turbinas (pelo nível do tanque de vapor).')
    a('- **Campanha de recarga:** com o hatch de conjuntos abastecido, um botão (ou sinal de redstone) desliga, troca 1/3 do núcleo em padrão de embaralhamento, manda os gastos para a piscina e religa depois do poço de xenônio.')
    a('- **Saídas:** cover/hatch de dados expõe potência, ρ, T, pressão, DNBR, Xe, boro, queima por canal e alarmes. OpenComputers e CC leem tudo.\n')
    a('Fica manual de propósito: limpar contaminação e consertar danos. Operar bem nunca exige intervenção.\n')

    a('## 13. Ciclo do combustível (cadeia de produção)\n')
    a('### 13.1 Enriquecimento (fórmula real de SWU)\n')
    a('```\nV(x) = (2x − 1) · ln(x / (1 − x))\nSWU por kg de produto = V(x_p) + T·V(x_t) − F·V(x_f)       x_f = 0,711%, x_t = 0,25%\n```\n')
    a(table(['Produto', 'Alimentação UF₆ natural (kg/kg)', 'SWU por kg'], [
        (f'LEU-{fmt(x * 100)}', fmt(swu(x)[1]), fmt(swu(x)[0])) for x in (0.03, 0.04, 0.045, 0.05)]))
    a('A **Cascata de Centrífugas** (multibloco auxiliar) entrega SWU por segundo conforme o número de centrífugas; mais estágios dão enriquecimento maior.\n')
    a('### 13.2 Etapas\n')
    a(table(['Etapa', 'Processo real', 'Entrada → Saída'], [
        ('Lixiviação', 'ácido sulfúrico', 'minério de urânio → yellowcake (U₃O₈)'),
        ('Conversão', 'HF + F₂', 'U₃O₈ → UF₆'),
        ('Enriquecimento', 'centrífugas', 'UF₆ natural → UF₆ enriquecido + UF₆ empobrecido'),
        ('Reconversão', 'processo ADU', 'UF₆ → pó de UO₂'),
        ('Pastilhas', 'prensagem + sinterização a 1700 °C (EBF)', 'UO₂ → pastilhas'),
        ('Revestimento', 'tubos de Zircaloy-4 (Zr, Sn, Fe, Cr)', 'pastilhas → varetas'),
        ('Montagem', 'grades espaçadoras de Inconel 718, bocais de inox', 'varetas → Conjunto Combustível'),
    ]))
    a('### 13.3 Combustível gasto (45 GWd/t)\n')
    a(table(['Fração', '% em massa', 'Destino'], [
        ('Urânio (0,8% U-235)', '93,4', 'volta para a conversão (urânio reprocessado)'),
        ('Plutônio', '1,2', 'MOX no LuV'),
        ('Actinídeos menores (Np, Am, Cm)', '0,1', 'linha de transmutação (futuro)'),
        ('Gases (Kr, Xe)', '0,6', 'separação criogênica: xenônio é útil'),
        ('Metais do grupo da platina (Ru, Rh, Pd)', '0,5', 'subproduto valioso'),
        ('Césio e estrôncio', '0,6', 'fontes de calor / RTG'),
        ('Demais produtos de fissão', '3,6', 'vitrificação em vidro borossilicato'),
    ]))
    a('O reprocessamento **PUREX** (dissolução em HNO₃, extração com TBP em querosene) é a linha que separa essas frações.\n')

    a('## 14. Multiblocos auxiliares\n')
    a(table(['Multibloco', 'Tier', 'Papel'], [
        ('Cascata de Centrífugas', 'EV–IV', 'enriquecimento (SWU)'),
        ('Fábrica de Combustível', 'IV', 'pastilhas → varetas → conjuntos'),
        ('Piscina de Combustível Usado', 'IV', 'resfria conjuntos gastos (calor de decaimento)'),
        ('Planta PUREX', 'IV–LuV', 'reprocessamento'),
        ('Vitrificador', 'IV', 'rejeito em vidro borossilicato'),
    ]))
    a('## Tela (mockup)\n\n![Sala de controle](mockups/gt/pwr_control.png){ loading=lazy }\n')
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, 'w', encoding='utf-8').write('\n'.join(md))
    print(OUT)


if __name__ == '__main__':
    main()
