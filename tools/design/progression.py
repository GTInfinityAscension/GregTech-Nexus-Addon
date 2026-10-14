"""Progression systems of the four endgame machines. Each one replaces the Godforge-style tree + milestones
with a system that comes out of the machine's own physics. Tables are computed from the formulas shown."""
import math

from endgame_specs import fmt, table


def lance():
    bodies = [  # name, characteristic mass (kg), parent
        ('Lua', 1e6, '—'), ('Fobos', 2e6, 'Lua'), ('Vesta', 8e6, 'Fobos'), ('Ceres', 8e6, 'Fobos'),
        ('Psique', 5e7, 'Vesta'), ('Europa', 5e7, 'Ceres'), ('Arrokoth', 2e8, 'Europa'), ('Nexus-1', 1e9, 'Psique + Arrokoth')]
    md = ['## 7. Progressão: Levantamento Balístico\n',
          'A Lança não tem árvore de upgrades nem marcos. Ela evolui de duas formas físicas: **conhecer os alvos** '
          '(levantamento) e **montar o cano** (bancada). Nenhuma moeda abstrata.\n',
          '### 7.1 Levantamento de cada corpo\n',
          'Cada corpo tem um levantamento `S` de 0 a 100%, que cresce com a massa recuperada dele:\n',
          '```\nS = 100% · (1 − exp(−M_recuperada / M_car))\n```\n',
          table(['Limiar', 'O que revela'], [
              ('25%', 'linhas principais da tabela de composição'), ('50%', 'linhas secundárias e a dureza exata (H)'),
              ('75%', 'elementos raros e o regime ideal de impacto'), ('100%', '**veio-mãe**: saída especial do corpo + a planta de um componente da bancada')]),
          '### 7.2 Mapa orbital\n',
          'Um corpo só pode ser mirado depois que seus **elementos orbitais** são conhecidos, e isso vem de levantar o corpo de onde ele é observado. '
          'A progressão é um mapa celeste que vai se acendendo, não uma árvore de compras.\n',
          table(['Corpo', 'M_car (kg)', 'Massa para 50%', 'Massa para 100%*', 'Liberado por'], [
              (n, fmt(m), fmt(m * math.log(2)), fmt(m * math.log(100)), p) for n, m, p in bodies]),
          '*100% é atingido em 99%, `M = M_car · ln 100`.\n',
          '### 7.3 Bancada do cano\n',
          'Os "upgrades" são **componentes físicos** encaixados numa planta do canhão. Cada componente é um item craftado; '
          'a planta dele vem de um veio-mãe. O jogador monta a combinação respeitando três orçamentos:\n',
          '```\nMassa da torre    Σ massa ≤ capacidade de giro (sobe com o anel de capacitores)\nCalor             Σ calor ≤ capacidade dos radiadores\nIndutância        Σ L_trilho ≤ L_max do banco (trilho demais não descarrega a tempo)\nη = 0,35 + Σ Δη_trilho · (1 − 0,5 · L/L_max)\n```\n',
          table(['Encaixe', 'Componente', 'Efeito', 'Massa (t)', 'Calor', 'Planta (veio-mãe)'], [
              ('Trilho ×8', 'Cobre-Nióbio', 'Δη +0,02', 40, 3, 'início'),
              ('Trilho ×8', 'Supercondutor UHV', 'Δη +0,04', 60, 1, 'Fobos'),
              ('Trilho ×8', 'Grafeno-Neutrônio', 'Δη +0,07', 140, 2, 'Psique'),
              ('Revestimento', 'WC / Neutrônio / Infinity', 'vida útil (seção 5)', '20–200', '—', 'Vesta / Psique / Nexus-1'),
              ('Arrefecimento', 'Hélio / Supercondutor / Gelo de Plasma', 'C_cano × 2 / × 4 / × 8', '30–90', '−10/−25/−60', 'Ceres / Europa / Arrokoth'),
              ('Sensor', 'Telescópio / Interferômetro / Lente gravitacional', 'u = 0,7 / 0,35 / 0,175', '10–80', 2, 'Lua / Europa / Arrokoth'),
              ('Cápsula', 'Ablativa / Magnética / Dobra', 'r = 0,75 / 0,85 / 0,95', '—', '—', 'Ceres / Psique / Nexus-1'),
              ('Salva', 'Divisor de pulso', '2 ou 4 projéteis por descarga', 50, 5, 'Vesta'),
          ]),
          '### 7.4 Hatches novos\n',
          table(['Hatch', 'Função'], [
              ('Hatch de Projétil', 'recebe projéteis; o tipo define a massa do tiro'),
              ('Hatch de Revestimento', 'troca o revestimento sem desmontar; mostra o desgaste W'),
              ('Hatch de Cartucho de Alvo', 'cada cartucho guarda corpo + regime; AE2 faz a rotação'),
              ('Barramento ME de Retorno', 'recebe as cápsulas; obrigatório'),
              ('Hatch de Banco de Capacitores', 'entrada de laser direto no banco, carga sem limite de amperagem')]),
          'Não existe a melhor configuração: trilhos pesados exigem mais anéis de capacitor para a torre girar; arrefecimento forte ocupa o calor que a salva quádrupla precisaria.\n']
    return '\n'.join(md)


def rift():
    ratios = [('Oitava', 2, 1), ('Quinta', 3, 2), ('Quarta', 4, 3), ('Terça maior', 5, 4), ('Sexta menor', 8, 5),
              ('Sétima menor', 9, 5), ('Trítono', 45, 32), ('Segunda menor', 16, 15)]
    def cons(p, q): return 1 / math.log2(p * q)
    chords = [('Quinta + Oitava', [(3, 2), (2, 1)]), ('Tríade maior', [(5, 4), (3, 2)]), ('Quarta + Quinta', [(4, 3), (3, 2)]),
              ('Trítono + Segunda', [(45, 32), (16, 15)]), ('Sexta + Sétima', [(8, 5), (9, 5)])]
    md = ['## 6. Progressão: Partitura de Ressonância\n',
          'O Portão evolui pelo que o jogador **ouve** nas fendas. Quando uma fenda fica com R ≥ 0,9 por 30 s, ela deixa gravar um **harmônico**: '
          'uma razão de frequências `p:q`. Os harmônicos são guardados numa partitura de 5 linhas; o acorde montado nela muda o comportamento do Portão.\n',
          '### 6.1 Harmônicos\n',
          'A consonância de um intervalo vem da teoria musical real (intervalos de razões simples soam mais estáveis):\n',
          '```\nconsonância(p:q) = 1 / log₂(p · q)\n```\n',
          table(['Intervalo', 'Razão', 'Consonância', 'Onde aparece'], [
              (n, f'{p}:{q}', fmt(cons(p, q)), b) for (n, p, q), b in zip(ratios, (
                  'qualquer fenda', 'planície cristalina', 'floresta de esporos', 'oceano de mercúrio', 'mundo-forja',
                  'relíquia de civilização', 'abismo de antimatéria', 'vazio'))]),
          '### 6.2 Acordes\n',
          'O acorde ativo é a soma dos harmônicos na partitura. Consonância alta estabiliza; dissonância aprofunda.\n',
          '```\nC = média das consonâncias do acorde\nλ₀_efetivo = λ₀ · (1,3 − C)                  acorde consonante gasta menos matéria exótica\nD_max_efetivo = D_max · max(0,5; 1 + 3 · (0,3 − C))   acorde dissonante desce mais fundo\n```\n',
          table(['Acorde', 'C', 'λ₀ (×)', 'D_max (×)', 'Leitura'], [
              (n, fmt(sum(cons(p, q) for p, q in c) / len(c)), fmt(1.3 - sum(cons(p, q) for p, q in c) / len(c)),
               fmt(max(0.5, 1 + 3 * (0.3 - sum(cons(p, q) for p, q in c) / len(c)))),
               'estável e raso' if sum(cons(p, q) for p, q in c) / len(c) >= 0.3 else 'instável e fundo')
              for n, c in chords]),
          'A partitura é o "loadout" do Portão. Acordes dissonantes são a forma de chegar ao Vazio, mas pedem pilones e matéria exótica de sobra.\n',
          '### 6.3 Atlas de constelações\n',
          'No lugar de marcos, cada semente aberta vira uma estrela no **Atlas**. Sementes próximas ficam ligadas:\n',
          '```\ndistância(a, b) = sqrt( (Δf*/100 THz)² + (Δφ*/36°)² + (ΔA*/10%)² )\nligadas se distância < 1\n```\n',
          'Grupos de estrelas ligadas formam **constelações**. Completar uma constelação (abrir todas as sementes dela) dá um efeito permanente: '
          'um harmônico raro, um pilone extra ou a trava de fase daquela região. O Atlas é compartilhado entre jogadores do mesmo time.\n',
          '### 6.4 Hatches novos\n',
          table(['Hatch', 'Função'], [
              ('Núcleo de Pilone', 'um em cada espinho; sem ele o pilone não conta'),
              ('Hatch de Matéria Exótica', 'entrada da estabilidade (L/s)'),
              ('Lançador de Sondas', 'consome Sondas de Fenda e estreita a sintonia'),
              ('Cofre de Harmônicos', 'guarda as gemas de harmônico gravadas'),
              ('Hatch de Sintonia', 'recebe f, φ e A por cover de dados ou computador')])]
    return '\n'.join(md)


def collider():
    parts = [  # name, mass GeV, signal/background ratio s/b per fb^-1 at threshold
        ('Antipróton', 0.938, 50), ('Káon', 0.494, 30), ('Lambda (Λ)', 1.116, 8), ('Charm (J/ψ)', 3.097, 4),
        ('Bottom (Υ)', 9.46, 1.5), ('Bóson W', 80.4, 0.6), ('Bóson Z', 91.2, 0.8), ('Higgs', 125.1, 0.08),
        ('Top', 172.7, 0.15), ('X(Nexus)', 2400, 0.02)]
    md = ['## 7. Progressão: Modelo Padrão\n',
          'O Colisor evolui por **descobertas**. Cada partícula começa como uma silhueta na tabela do Modelo Padrão. '
          'Ela só vira produto da máquina quando é descoberta com significância estatística real.\n',
          '### 7.1 Significância\n',
          '```\nS = s · L_int        B = b · L_int          (sinal e fundo acumulados, eventos)\nZ = S / sqrt(B) = (s / sqrt(b)) · sqrt(L_int)\nevidência: Z ≥ 3σ        descoberta: Z ≥ 5σ (critério real da física de partículas)\nL_int para 5σ = 25 · b / s²\n```\n',
          'A GUI mostra o histograma de massa invariante com o pico crescendo sobre o fundo a cada fb⁻¹ coletado.\n',
          table(['Partícula', 'Massa (GeV)', 's/√b por fb⁻¹', 'L_int para 3σ (fb⁻¹)', 'L_int para 5σ (fb⁻¹)'], [
              (n, fmt(m), fmt(r), fmt(9 / r ** 2), fmt(25 / r ** 2)) for n, m, r in parts]),
          'Antes da descoberta a partícula sai com rendimento de 10%; com evidência (3σ), 40%; descoberta, 100%. Descobrir é o upgrade.\n',
          '### 7.2 Comitê de tempo de feixe\n',
          'Equipamento novo (ímãs, armadilhas, detectores) vem de **propostas de experimento**. O comitê aprova uma por vez; '
          'cada proposta pede luminosidade numa energia e numa configuração, e só termina se o feixe ficar nela pelo tempo pedido. '
          'O jogador divide o dia do anel entre **corridas de produção** (antimatéria para a fábrica) e **corridas de física** (propostas).\n',
          table(['Proposta', 'Pede', 'Entrega'], [
              ('Teste de ímã de Nb₃Sn', '5 fb⁻¹ a ≥ 7 TeV', 'ímãs de Nb₃Sn'), ('Detector de vértice', 'descobrir Charm', '+30% de pureza (b ÷ 2)'),
              ('Resfriamento estocástico', '20 fb⁻¹ em modo antipróton', 'antiprótons × 3'),
              ('Penning criogênica', '1e13 antiprótons guardados por 1 h', 'armadilha tier 3'),
              ('Ímã REBCO', 'descobrir W e Z', 'B = 20 T'), ('Colisão e⁺e⁻', 'descobrir Bottom', 'modo elétron-pósitron'),
              ('Íons pesados', 'descobrir Top', 'plasma de quarks e glúons'), ('Ímã de neutrônio', 'descobrir Higgs', 'B = 45 T'),
              ('Busca além do Modelo Padrão', 'X(Nexus) a 3σ', 'ímãs Infinity, sem quench')]),
          'A tensão do sistema é o tempo: cada fb⁻¹ de física é antimatéria que não foi produzida.\n',
          '### 7.3 Hatches novos\n',
          table(['Hatch', 'Função'], [
              ('Armadilha de Penning', 'guarda antimatéria; gasta EU contínuo, aniquila sem energia'),
              ('Beam Dump', 'absorve o feixe no quench; sem ele o quench danifica o anel'),
              ('Hatch de Hélio Criogênico', 'entrada de hélio líquido por setor de ímãs'),
              ('Hatch de Detector', 'saída de dados das colisões para o Comitê (computação)'),
              ('Fonte de Íons', 'entrada de gás no linac; define o tipo de feixe (p, e⁻, íons pesados)')])]
    return '\n'.join(md)


def star():
    G, Msun, R = 6.674e-11, 1.989e30, 12e3
    def p_kep(m): return 2 * math.pi * math.sqrt(R ** 3 / (G * m * Msun))
    md = ['## 8. Progressão: Diagrama M–P e Sismograma\n',
          'A Câmara evolui pelo **caminho que a estrela percorre**. O painel principal é um diagrama massa × período '
          '(como um diagrama HR de astrônomo) com a trajetória da estrela desenhada. Regiões do diagrama liberam comportamentos.\n',
          '### 8.1 Regiões do diagrama\n',
          '```\nP_kepler(M) = 2π · sqrt(R³ / (G·M))     abaixo disso a estrela se desfaz (limite de quebra)\nM_TOV = 2,2 M☉                           à direita disso, buraco negro\n```\n',
          table(['M (M☉)', 'P_kepler (ms)'], [(fmt(m), fmt(p_kep(m) * 1000)) for m in (1.2, 1.4, 1.6, 1.8, 2.0, 2.2)]),
          table(['Região', 'Condição', 'O que libera'], [
              ('Pulsar comum', 'P > 30 ms', 'estado inicial'),
              ('Pulsar recente', '10 ms < P < 30 ms', 'mineração de crosta mais rápida'),
              ('Milissegundo reciclado', 'P < 10 ms, alcançado por alimentação', 'extração em potência máxima'),
              ('Recordista', 'P < 1,4 ms (o pulsar real mais rápido gira a 716 Hz)', 'conquista; bandas tier 4'),
              ('Magnetar', 'campo das bandas invertido por 10 min', 'tremores gigantes e Matéria Degenerada em lote'),
              ('Borda TOV', 'M > 2,1 M☉', 'aviso permanente; prepara o modo buraco negro'),
              ('Quebra', 'P < P_kepler(M)', 'falha catastrófica: a estrela se desfaz e a máquina recomeça'),
          ]),
          '### 8.2 Sismograma\n',
          'O equipamento novo vem dos **tremores** (glitches, como os de pulsares reais). Cada tremor fica registrado com sua assinatura `ΔΩ/Ω` e o tempo de recuperação `τ`. '
          'Comparar um tremor com o catálogo decifra uma camada do interior da estrela, e cada camada decifrada libera um equipamento de contenção.\n',
          table(['Tipo de tremor', 'ΔΩ/Ω (real)', 'Como provocar', 'Decifra', 'Libera'], [
              ('Microtremor', '1e-9 a 1e-8', 'extração constante', 'crosta externa', 'bandas tier 2'),
              ('Tipo Crab', '1e-8 a 1e-7', 'variar a extração', 'crosta interna', 'mineração de crosta ×4'),
              ('Tipo Vela (gigante)', '≈ 1e-6', 'spin-up rápido por alimentação', 'superfluido de nêutrons', 'bandas tier 3, previsão de tremores'),
              ('Antitremor', '< 0 (spin-up súbito)', 'só em magnetar', 'núcleo magnético', 'equação de estado exótica (M_TOV 2,4)'),
              ('Tremor de colapso', 'divergente', 'cruzar a borda TOV', 'horizonte', 'coletor de ergosfera'),
          ]),
          'O sismograma é uma fita que corre na GUI. O jogador aprende a ler os padrões e provoca os tremores que faltam, usando a própria estrela.\n']
    return '\n'.join(md)
