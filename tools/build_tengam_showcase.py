import json
import base64
from pathlib import Path
from PIL import Image, ImageDraw

OUT_DIR = Path("/tmp/tengam_candidates")
ARTIFACT_DIR = Path("/home/raishxn/.gemini/antigravity/brain/9c95a421-582d-4dd9-a627-e59f2d3d6c06")
ARTIFACT_PATH = ARTIFACT_DIR / "tengam_showcase.html"

shapes = ["ingot", "plate", "gear", "block"]
options = [1, 2, 3]

b64_data = {}
for opt in options:
    b64_data[opt] = {}
    for shape in shapes:
        gif_file = OUT_DIR / f"tengam_opt{opt}_{shape}.gif"
        if gif_file.exists():
            b64 = base64.b64encode(gif_file.read_bytes()).decode("utf-8")
            b64_data[opt][shape] = f"data:image/gif;base64,{b64}"
        else:
            b64_data[opt][shape] = ""

json_b64 = json.dumps(b64_data)

# Gera imagem estática de grade comparativa
canvas_w = 3 * 160 + 80
canvas_h = 4 * 160 + 120
canvas = Image.new('RGBA', (canvas_w, canvas_h), (8, 18, 10, 255))
draw = ImageDraw.Draw(canvas)

draw.text((40 + 20, 20), 'OPCAO 1: Lorentz Flux Lines', fill=(163, 230, 53, 255))
draw.text((40 + 160 + 40 + 20, 20), 'OPCAO 2: Spin Precession', fill=(74, 222, 128, 255))
draw.text((40 + 320 + 80 + 20, 20), 'OPCAO 3: Meissner Vortex', fill=(190, 242, 100, 255))

for row_idx, shape in enumerate(shapes):
    y_pos = 60 + row_idx * 160
    draw.text((10, y_pos + 60), shape.upper(), fill=(148, 163, 184, 255))
    for opt in [1, 2, 3]:
        gif_p = OUT_DIR / f'tengam_opt{opt}_{shape}.gif'
        if gif_p.exists():
            gif = Image.open(gif_p)
            gif.seek(14)
            frame = gif.convert('RGBA')
            scaled = frame.resize((128, 128), Image.Resampling.NEAREST)
            x_pos = 50 + (opt - 1) * (160 + 20)
            draw.rectangle([x_pos - 6, y_pos - 6, x_pos + 134, y_pos + 134], fill=(12, 28, 14, 255), outline=(25, 60, 30, 255))
            canvas.paste(scaled, (x_pos, y_pos), scaled)

canvas.save(ARTIFACT_DIR / 'tengam_grid.png')
print("Grade comparativa do Tengam salva!")

html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Tengam — Avaliação de 3 Opções Visuais</title>
  <style>
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}
    body {{
      background-color: #061108;
      color: #e2e8f0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      padding: 16px;
      line-height: 1.5;
    }}
    .container {{
      max-width: 1000px;
      margin: 0 auto;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }}
    .header-card {{
      background: linear-gradient(135deg, #143310 0%, #0d210b 60%, #061108 100%);
      border: 1px solid rgba(132, 204, 22, 0.35);
      border-radius: 14px;
      padding: 20px 24px;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      box-shadow: 0 10px 25px -5px rgba(132, 204, 22, 0.2);
    }}
    .badge {{
      display: inline-block;
      padding: 2px 8px;
      border-radius: 9999px;
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      background: rgba(132, 204, 22, 0.2);
      color: #bef264;
      border: 1px solid rgba(132, 204, 22, 0.4);
      margin-bottom: 6px;
    }}
    .formula-tag {{
      font-size: 12px;
      color: #d9f99d;
      font-family: monospace;
      margin-left: 8px;
    }}
    h1 {{
      font-size: 22px;
      font-weight: 800;
      background: linear-gradient(to right, #bef264, #a3e635, #4ade80);
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
      gap: 12px;
      background: #0b1c0e;
      padding: 8px 14px;
      border-radius: 10px;
      border: 1px solid #1c3d1e;
    }}
    .btn-toggle {{
      background: #65a30d;
      color: white;
      border: none;
      padding: 8px 14px;
      border-radius: 8px;
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
      box-shadow: 0 4px 12px rgba(101, 163, 13, 0.35);
      transition: all 0.2s;
    }}
    .btn-toggle:hover {{
      background: #84cc16;
    }}
    
    .shape-bar {{
      background: #0b1c0e;
      border: 1px solid #1c3d1e;
      border-radius: 12px;
      padding: 12px 16px;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
    }}
    .shape-buttons {{
      display: flex;
      gap: 6px;
      background: #061108;
      padding: 4px;
      border-radius: 8px;
      border: 1px solid #1c3d1e;
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
      background: #65a30d;
      color: #ffffff;
      box-shadow: 0 2px 6px rgba(101, 163, 13, 0.4);
    }}
    .btn-shape:hover:not(.active) {{
      color: #ffffff;
      background: #1c3d1e;
    }}
    
    .grid-options {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 16px;
    }}
    @media (max-width: 768px) {{
      .grid-options {{
        grid-template-columns: 1fr;
      }}
    }}
    
    .card {{
      background: #0b1c0e;
      border: 2px solid #1c3d1e;
      border-radius: 14px;
      padding: 18px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 14px;
      transition: all 0.25s ease;
      position: relative;
    }}
    .card:hover {{
      border-color: rgba(132, 204, 22, 0.5);
      transform: translateY(-2px);
    }}
    .card.selected {{
      border-color: #84cc16;
      box-shadow: 0 0 20px rgba(132, 204, 22, 0.25);
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
      background: rgba(132, 204, 22, 0.2);
      color: #bef264;
      border: 1px solid rgba(132, 204, 22, 0.3);
    }}
    .card-title {{
      font-size: 16px;
      font-weight: 700;
      color: #ecfccb;
      margin-top: 6px;
    }}
    .card-desc {{
      font-size: 12px;
      color: #94a3b8;
      margin-top: 4px;
      line-height: 1.45;
    }}
    
    .image-box {{
      background: #040a05;
      border: 1px solid #1c3d1e;
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
    
    @keyframes magneticGlowPulse {{
      0%, 100% {{
        filter: drop-shadow(0 0 8px rgba(132, 204, 22, 0.8)) drop-shadow(0 0 20px rgba(163, 230, 53, 0.45));
        transform: scale(1);
      }}
      50% {{
        filter: drop-shadow(0 0 16px rgba(163, 230, 53, 1.0)) drop-shadow(0 0 32px rgba(190, 242, 100, 0.7));
        transform: scale(1.02);
      }}
    }}
    .glow-effect {{
      animation: magneticGlowPulse 2.4s ease-in-out infinite;
    }}
    
    .btn-approve {{
      width: 100%;
      padding: 10px;
      border-radius: 8px;
      font-size: 12px;
      font-weight: 700;
      border: none;
      cursor: pointer;
      transition: all 0.2s;
      background: #142a17;
      color: #cbd5e1;
    }}
    .btn-approve:hover {{
      background: #65a30d;
      color: #ffffff;
      box-shadow: 0 4px 14px rgba(101, 163, 13, 0.4);
    }}
    .card.selected .btn-approve {{
      background: linear-gradient(135deg, #65a30d, #a3e635);
      color: #061108;
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
      background: #102613;
      color: #bef264;
      border: 1px solid #1c3d1e;
    }}
    
    .footer-box {{
      background: #0b1c0e;
      border: 1px solid #1c3d1e;
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
          <span class="badge">Refatoração de Textura</span>
          <span class="formula-tag">M • UIV / UEV Tier</span>
        </div>
        <h1>Tengam — 3 Opções de Animação</h1>
        <p class="subtitle">
          Texturas novas fluidas de 30 frames combinadas com o <strong>Magnetic Glow Edge Shader</strong> (<code style="color:#d9f99d">gtna:glow_edge</code>).
        </p>
      </div>

      <div class="shader-control">
        <div>
          <div style="font-size:10px; text-transform:uppercase; color:#94a3b8;">Shader In-Game</div>
          <div id="shaderStatusText" style="font-size:12px; font-weight:800; color:#bef264;">GLOW ATIVADO</div>
        </div>
        <button class="btn-toggle" id="btnToggleGlow" onclick="toggleShader()">Alternar Glow</button>
      </div>
    </div>

    <div class="shape-bar">
      <div style="display:flex; align-items:center; gap:12px;">
        <span style="font-size:12px; font-weight:700; color:#94a3b8; text-transform:uppercase;">Forma:</span>
        <div class="shape-buttons">
          <button class="btn-shape active" id="btn-ingot" onclick="setShape('ingot')">Barra (Ingot)</button>
          <button class="btn-shape" id="btn-plate" onclick="setShape('plate')">Placa (Plate)</button>
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
      <div class="card selected" id="card-1">
        <div>
          <div class="card-header">
            <span class="tag-opt">Opção 1</span>
            <span style="font-size:11px; color:#64748b;">Lorentz Field</span>
          </div>
          <div class="card-title">Lorentz Flux Lines</div>
          <p class="card-desc">
            Curvas de indução magnética dipolar onde o plasma supercondutor deriva ao longo das <strong>linhas de campo de Lorentz</strong> aceleradas em direção aos polos.
          </p>
          <div class="features-list">
            <span class="feature-item">Campo Dipolar</span>
            <span class="feature-item">Deriva de Lorentz</span>
            <span class="feature-item">Polos Elétricos</span>
          </div>
        </div>

        <div class="image-box">
          <div id="wrapper-1" class="glow-effect">
            <img id="img-1" class="pixelated-art" src="{b64_data[1]['ingot']}" alt="Opção 1 Ingot">
          </div>
        </div>

        <button class="btn-approve" onclick="selectCard(1)">Aprovar Opção 1 (Responder 1)</button>
      </div>

      <!-- Option 2 -->
      <div class="card" id="card-2">
        <div>
          <div class="card-header">
            <span class="tag-opt">Opção 2</span>
            <span style="font-size:11px; color:#64748b;">Spin Waves</span>
          </div>
          <div class="card-title">Quantum Spin Precession</div>
          <p class="card-desc">
            Ressonância ferromagnética de Larmor onde <strong>ondas de spin transversais (magnons)</strong> cruzam a superfície em padrão de nós de alta frequência.
          </p>
          <div class="features-list">
            <span class="feature-item">Precessão de Larmor</span>
            <span class="feature-item">Ondas de Spin (Magnons)</span>
            <span class="feature-item">Ressonância de RF</span>
          </div>
        </div>

        <div class="image-box">
          <div id="wrapper-2" class="glow-effect">
            <img id="img-2" class="pixelated-art" src="{b64_data[2]['ingot']}" alt="Opção 2 Ingot">
          </div>
        </div>

        <button class="btn-approve" onclick="selectCard(2)">Aprovar Opção 2 (Responder 2)</button>
      </div>

      <!-- Option 3 -->
      <div class="card" id="card-3">
        <div>
          <div class="card-header">
            <span class="tag-opt">Opção 3</span>
            <span style="font-size:11px; color:#64748b;">Meissner Effect</span>
          </div>
          <div class="card-title">Superconducting Meissner Vortex</div>
          <p class="card-desc">
            Tubos de fluxo magnético quantizado (<strong>vórtices de Abrikosov</strong>) orbitando em rede triangular com repulsão do fluxo das bordas pelo Efeito Meissner.
          </p>
          <div class="features-list">
            <span class="feature-item">Vórtices de Abrikosov</span>
            <span class="feature-item">Efeito Meissner</span>
            <span class="feature-item">Fluxo Quantizado</span>
          </div>
        </div>

        <div class="image-box">
          <div id="wrapper-3" class="glow-effect">
            <img id="img-3" class="pixelated-art" src="{b64_data[3]['ingot']}" alt="Opção 3 Ingot">
          </div>
        </div>

        <button class="btn-approve" onclick="selectCard(3)">Aprovar Opção 3 (Responder 3)</button>
      </div>

    </div>

    <div class="footer-box">
      <div>
        Qual das 3 opções você prefere aprovar para o <strong>Tengam</strong>?
      </div>
      <div style="font-weight:700; color:#bef264;">
        Basta responder 1, 2 ou 3 no chat!
      </div>
    </div>

  </div>

  <script>
    const data = {json_b64};
    let currentShape = 'ingot';
    let glowEnabled = true;

    function updateArt() {{
      for (let opt = 1; opt <= 3; opt++) {{
        const img = document.getElementById('img-' + opt);
        if (img && data[opt] && data[opt][currentShape]) {{
          img.src = data[opt][currentShape];
        }}
      }}
    }}

    function setShape(shape) {{
      currentShape = shape;
      ['ingot', 'plate', 'gear', 'block'].forEach(s => {{
        const btn = document.getElementById('btn-' + s);
        if (btn) {{
          if (s === shape) {{
            btn.classList.add('active');
          }} else {{
            btn.classList.remove('active');
          }}
        }}
      }});
      updateArt();
    }}

    function toggleShader() {{
      glowEnabled = !glowEnabled;
      const statusText = document.getElementById('shaderStatusText');
      const toggleBtn = document.getElementById('btnToggleGlow');

      for (let opt = 1; opt <= 3; opt++) {{
        const wrap = document.getElementById('wrapper-' + opt);
        if (wrap) {{
          if (glowEnabled) {{
            wrap.classList.add('glow-effect');
          }} else {{
            wrap.classList.remove('glow-effect');
          }}
        }}
      }}

      if (glowEnabled) {{
        statusText.innerText = "GLOW ATIVADO";
        statusText.style.color = "#bef264";
        toggleBtn.innerText = "Desativar Glow";
      }} else {{
        statusText.innerText = "TEXTURA PURA";
        statusText.style.color = "#94a3b8";
        toggleBtn.innerText = "Ativar Glow";
      }}
    }}

    function selectCard(opt) {{
      for (let i = 1; i <= 3; i++) {{
        const card = document.getElementById('card-' + i);
        if (card) {{
          if (i === opt) {{
            card.classList.add('selected');
          }} else {{
            card.classList.remove('selected');
          }}
        }}
      }}
    }}
  </script>
</body>
</html>
"""

ARTIFACT_PATH.write_text(html_content, encoding="utf-8")
print(f"Artifact criado em: {ARTIFACT_PATH}")
