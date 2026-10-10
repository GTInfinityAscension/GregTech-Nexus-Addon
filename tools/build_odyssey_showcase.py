import json
import base64
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = Path("/tmp/odyssey_candidates")
ARTIFACT_DIR = Path("/home/raishxn/.gemini/antigravity/brain/9c95a421-582d-4dd9-a627-e59f2d3d6c06")

shapes = ["ingot", "plate", "gear", "block"]
options = [1, 2, 3]

b64_data = {1: {}, 2: {}, 3: {}}
for opt in options:
    for shape in shapes:
        gif_file = OUT_DIR / f"opt{opt}_{shape}.gif"
        if not gif_file.exists():
            # Se for plate e não existir, copia de ingot
            ingot_file = OUT_DIR / f"opt{opt}_ingot.gif"
            if ingot_file.exists():
                gif_file = ingot_file
        if gif_file.exists():
            b64 = base64.b64encode(gif_file.read_bytes()).decode("utf-8")
            b64_data[opt][shape] = f"data:image/gif;base64,{b64}"

json_b64 = json.dumps(b64_data)

html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Odyssey Nano Superalloy — Avaliação de 3 Opções Visuais</title>
  <style>
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}
    body {{
      background-color: #060f0d;
      color: #e2e8f0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      padding: 20px;
      line-height: 1.5;
    }}
    .container {{
      max-width: 1040px;
      margin: 0 auto;
      display: flex;
      flex-direction: column;
      gap: 18px;
    }}
    .header-card {{
      background: linear-gradient(135deg, #0e2922 0%, #0a1b17 60%, #060f0d 100%);
      border: 1px solid rgba(45, 212, 191, 0.4);
      border-radius: 14px;
      padding: 22px 26px;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      box-shadow: 0 10px 25px -5px rgba(20, 184, 166, 0.2);
    }}
    .badge {{
      display: inline-block;
      padding: 3px 10px;
      border-radius: 9999px;
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      background: rgba(45, 212, 191, 0.18);
      color: #5eead4;
      border: 1px solid rgba(45, 212, 191, 0.4);
      margin-bottom: 6px;
    }}
    .formula-tag {{
      font-size: 12px;
      color: #99f6e4;
      font-family: monospace;
      margin-left: 8px;
    }}
    h1 {{
      font-size: 24px;
      font-weight: 800;
      background: linear-gradient(to right, #ffffff, #5eead4, #14b8a6);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}
    .subtitle {{
      font-size: 13px;
      color: #94a3b8;
      margin-top: 4px;
    }}
    .shader-control {{
      display: flex;
      align-items: center;
      gap: 14px;
      background: #0d1e1a;
      padding: 10px 16px;
      border-radius: 10px;
      border: 1px solid #16382f;
    }}
    .btn-toggle {{
      background: #0d9488;
      color: white;
      border: none;
      padding: 8px 16px;
      border-radius: 8px;
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
      box-shadow: 0 4px 12px rgba(13, 148, 136, 0.35);
      transition: all 0.2s;
    }}
    .btn-toggle:hover {{
      background: #14b8a6;
    }}
    
    .shape-bar {{
      background: #0d1e1a;
      border: 1px solid #16382f;
      border-radius: 12px;
      padding: 12px 18px;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
    }}
    .shape-buttons {{
      display: flex;
      gap: 6px;
      background: #060e0d;
      padding: 4px;
      border-radius: 8px;
      border: 1px solid #16382f;
    }}
    .btn-shape {{
      background: transparent;
      color: #94a3b8;
      border: none;
      padding: 6px 14px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s;
    }}
    .btn-shape.active {{
      background: #0d9488;
      color: #ffffff;
      box-shadow: 0 2px 8px rgba(13, 148, 136, 0.4);
    }}
    .btn-shape:hover:not(.active) {{
      color: #ffffff;
      background: #16382f;
    }}
    
    .grid-options {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 18px;
    }}
    @media (max-width: 820px) {{
      .grid-options {{
        grid-template-columns: 1fr;
      }}
    }}
    
    .card {{
      background: #0d1e1a;
      border: 2px solid #16382f;
      border-radius: 14px;
      padding: 20px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 16px;
      transition: all 0.25s ease;
      position: relative;
    }}
    .card:hover {{
      border-color: rgba(45, 212, 191, 0.5);
      transform: translateY(-2px);
    }}
    .card.selected {{
      border-color: #2dd4bf;
      box-shadow: 0 0 20px rgba(45, 212, 191, 0.25);
    }}
    
    .card-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}
    .tag-opt {{
      padding: 3px 8px;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 700;
      background: rgba(45, 212, 191, 0.18);
      color: #5eead4;
      border: 1px solid rgba(45, 212, 191, 0.3);
    }}
    .card-title {{
      font-size: 16px;
      font-weight: 700;
      color: #f1f5f9;
      margin-top: 6px;
    }}
    .card-desc {{
      font-size: 12px;
      color: #94a3b8;
      margin-top: 4px;
      line-height: 1.45;
    }}
    
    .image-box {{
      background: #050c0a;
      border: 1px solid #132e27;
      border-radius: 12px;
      padding: 24px;
      display: flex;
      align-items: center;
      justify-content: center;
      min-height: 180px;
      position: relative;
      overflow: hidden;
    }}
    
    .pixelated-art {{
      image-rendering: -moz-crisp-edges;
      image-rendering: -webkit-crisp-edges;
      image-rendering: pixelated;
      image-rendering: crisp-edges;
      width: 128px !important;
      height: 128px !important;
      min-width: 128px;
      min-height: 128px;
      max-width: 128px;
      max-height: 128px;
      object-fit: contain;
      display: block;
      transition: transform 0.2s ease;
    }}
    
    @keyframes nanotechGlowPulse {{
      0%, 100% {{
        filter: drop-shadow(0 0 8px rgba(45, 212, 191, 0.85)) drop-shadow(0 0 20px rgba(20, 184, 166, 0.5));
        transform: scale(1);
      }}
      50% {{
        filter: drop-shadow(0 0 16px rgba(94, 234, 212, 1.0)) drop-shadow(0 0 32px rgba(45, 212, 191, 0.75));
        transform: scale(1.02);
      }}
    }}
    .glow-effect {{
      animation: nanotechGlowPulse 2.6s ease-in-out infinite;
    }}
    
    .btn-approve {{
      width: 100%;
      padding: 11px;
      border-radius: 8px;
      font-size: 12px;
      font-weight: 700;
      border: none;
      cursor: pointer;
      transition: all 0.2s;
      background: #142e26;
      color: #cbd5e1;
    }}
    .btn-approve:hover {{
      background: #0d9488;
      color: #ffffff;
      box-shadow: 0 4px 14px rgba(13, 148, 136, 0.4);
    }}
    .card.selected .btn-approve {{
      background: linear-gradient(135deg, #0d9488, #2dd4bf);
      color: #042f2e;
    }}

    .features-list {{
      display: flex;
      flex-wrap: wrap;
      gap: 4px;
      margin-top: 8px;
    }}
    .feature-item {{
      font-size: 10px;
      padding: 2px 6px;
      border-radius: 4px;
      background: #0e2b23;
      color: #99f6e4;
      border: 1px solid #164639;
    }}
    
    .footer-box {{
      background: #0d1e1a;
      border: 1px solid #16382f;
      border-radius: 12px;
      padding: 14px 20px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 12px;
      color: #94a3b8;
    }}
  </style>
</head>
<body>
  <div class="container">
    
    <div class="header-card">
      <div>
        <div>
          <span class="badge">GTO Space-Era Material</span>
          <span class="formula-tag">Tr₁₄Nq₈Mo₁₇ • #4C7A6A</span>
        </div>
        <h1>Odyssey Nano Superalloy — 3 Opções de Animação</h1>
        <p class="subtitle">
          Texturas fluidas de 30 frames combinadas com o <strong>Nanotech Glow Edge Shader</strong> (<code style="color:#5eead4">renderblender:glow_edge</code>).
        </p>
      </div>

      <div class="shader-control">
        <div>
          <div style="font-size:10px; text-transform:uppercase; color:#94a3b8;">Shader In-Game</div>
          <div id="shaderStatusText" style="font-size:12px; font-weight:800; color:#2dd4bf;">GLOW ATIVADO</div>
        </div>
        <button class="btn-toggle" id="btnToggleGlow" onclick="toggleShader()">Alternar Shader</button>
      </div>
    </div>

    <div class="shape-bar">
      <div style="display:flex; align-items:center; gap:12px;">
        <span style="font-size:12px; font-weight:700; color:#94a3b8; text-transform:uppercase;">Forma:</span>
        <div class="shape-buttons">
          <button class="btn-shape active" id="btn-ingot" onclick="setShape('ingot')">Barra (Ingot)</button>
          <button class="btn-shape" id="btn-gear" onclick="setShape('gear')">Engrenagem (Gear)</button>
          <button class="btn-shape" id="btn-block" onclick="setShape('block')">Bloco (Block)</button>
        </div>
      </div>
      <div style="font-size:11px; color:#64748b;">
        Tamanho: <strong>128×128px (8× Zoom Pixel Art Nítido)</strong>
      </div>
    </div>

    <div class="grid-options">
      
      <!-- Option 1 -->
      <div class="card" id="card-1">
        <div>
          <div class="card-header">
            <span class="tag-opt">Opção 1</span>
            <span style="font-size:11px; color:#64748b;">Nano-Lattice</span>
          </div>
          <div class="card-title">Sub-Atomic Nano-Lattice Weave</div>
          <p class="card-desc">
            Trama nanométrica oblíqua de alta densidade: <strong>pacotes de elétrons quânticos coerentes</strong> viajam pelas linhas moleculares com nós atômicos fluorescentes em turquesa.
          </p>
          <div class="features-list">
            <span class="feature-item">Trama 30° Molecular</span>
            <span class="feature-item">Pacotes Quânticos</span>
            <span class="feature-item">Nós Fluorescentes</span>
          </div>
        </div>

        <div class="image-box">
          <div id="wrapper-1" class="glow-effect">
            <img id="img-1" class="pixelated-art" src="{b64_data[1]['ingot']}" alt="Opção 1 Ingot">
          </div>
        </div>

        <button class="btn-approve" onclick="selectCard(1)">Opção 1: Nano-Lattice Weave</button>
      </div>

      <!-- Option 2 (Aprovada) -->
      <div class="card selected" id="card-2">
        <div>
          <div class="card-header">
            <span class="tag-opt" style="background:#0d9488; color:#ffffff;">Aprovada (Autor)</span>
            <span style="font-size:11px; color:#5eead4;">Nanite Swarm</span>
          </div>
          <div class="card-title">Nanite Swarm Self-Assembly</div>
          <p class="card-desc">
            Enxame de nanorrobôs em auto-montagem: <strong>4 núcleos em órbitas Lissajous</strong> fluindo pela superfície com pontes de plasma e picos de sinterização a frio em ciano incandescente.
          </p>
          <div class="features-list">
            <span class="feature-item">4 Núcleos Lissajous</span>
            <span class="feature-item">Solda Flash Incandescente</span>
            <span class="feature-item">Auto-Montagem Fluida</span>
          </div>
        </div>

        <div class="image-box">
          <div id="wrapper-2" class="glow-effect">
            <img id="img-2" class="pixelated-art" src="{b64_data[2]['ingot']}" alt="Opção 2 Ingot">
          </div>
        </div>

        <button class="btn-approve" onclick="selectCard(2)">✓ Opção 2 Aplicada no Mod</button>
      </div>

      <!-- Option 3 -->
      <div class="card" id="card-3">
        <div>
          <div class="card-header">
            <span class="tag-opt">Opção 3</span>
            <span style="font-size:11px; color:#64748b;">Quantum Hex</span>
          </div>
          <div class="card-title">Quantum Coherence Hex-Field</div>
          <p class="card-desc">
            Blindagem de Naquadria-Trinium com <strong>simetria hexagonal pura (ordem 6)</strong> e ondas estacionárias de Chladni com refração dielétrica iridescente.
          </p>
          <div class="features-list">
            <span class="feature-item">Simetria Hexagonal (6θ)</span>
            <span class="feature-item">Ondas de Chladni</span>
            <span class="feature-item">Refração Dielétrica</span>
          </div>
        </div>

        <div class="image-box">
          <div id="wrapper-3" class="glow-effect">
            <img id="img-3" class="pixelated-art" src="{b64_data[3]['ingot']}" alt="Opção 3 Ingot">
          </div>
        </div>

        <button class="btn-approve" onclick="selectCard(3)">Opção 3: Quantum Hex-Field</button>
      </div>

    </div>

    <div class="footer-box">
      <div>
        Status: <strong style="color:#2dd4bf;">Opção 2 aplicada com sucesso no mod (G-0223)</strong>
      </div>
      <div>
        28 itens e 2 blocos gerados com <strong>Nanotech Glow Edge Shader</strong>.
      </div>
    </div>

  </div>

  <script>
    const b64Data = {json_b64};
    let currentShape = 'ingot';
    let shaderActive = true;
    let selectedOption = 2;

    function setShape(shape) {{
      currentShape = shape;
      document.querySelectorAll('.btn-shape').forEach(btn => btn.classList.remove('active'));
      document.getElementById('btn-' + shape).classList.add('active');

      for (let opt = 1; opt <= 3; opt++) {{
        const img = document.getElementById('img-' + opt);
        if (b64Data[opt] && b64Data[opt][shape]) {{
          img.src = b64Data[opt][shape];
        }}
      }}
    }}

    function toggleShader() {{
      shaderActive = !shaderActive;
      const statusText = document.getElementById('shaderStatusText');
      const btn = document.getElementById('btnToggleGlow');

      for (let opt = 1; opt <= 3; opt++) {{
        const wrapper = document.getElementById('wrapper-' + opt);
        if (shaderActive) {{
          wrapper.classList.add('glow-effect');
        }} else {{
          wrapper.classList.remove('glow-effect');
        }}
      }}

      if (shaderActive) {{
        statusText.innerText = 'GLOW ATIVADO';
        statusText.style.color = '#2dd4bf';
        btn.innerText = 'Desativar Glow';
        btn.style.background = '#0d9488';
      }} else {{
        statusText.innerText = 'SHADER DESLIGADO';
        statusText.style.color = '#64748b';
        btn.innerText = 'Ativar Glow';
        btn.style.background = '#334155';
      }}
    }}

    function selectCard(opt) {{
      selectedOption = opt;
      for (let i = 1; i <= 3; i++) {{
        const card = document.getElementById('card-' + i);
        if (i === opt) {{
          card.classList.add('selected');
        }} else {{
          card.classList.remove('selected');
        }}
      }}
    }}
  </script>
</body>
</html>
"""

(ARTIFACT_DIR / "odyssey_showcase.html").write_text(html_content, encoding="utf-8")
print("Showcase interativo da Odyssey atualizado com sucesso!")
