import json
import base64
from pathlib import Path
from PIL import Image, ImageDraw

OUT_DIR = Path("/tmp/ichorium_candidates")
ARTIFACT_DIR = Path("/home/raishxn/.gemini/antigravity/brain/9c95a421-582d-4dd9-a627-e59f2d3d6c06")
ARTIFACT_PATH = ARTIFACT_DIR / "ichorium_showcase.html"

shapes = ["ingot", "plate", "gear", "block"]
options = [1, 2, 3]

b64_data = {}
for opt in options:
    b64_data[opt] = {}
    for shape in shapes:
        gif_file = OUT_DIR / f"ichorium_opt{opt}_{shape}.gif"
        if gif_file.exists():
            b64 = base64.b64encode(gif_file.read_bytes()).decode("utf-8")
            b64_data[opt][shape] = f"data:image/gif;base64,{b64}"
        else:
            b64_data[opt][shape] = ""

json_b64 = json.dumps(b64_data)

# Gera imagem estática de grade comparativa
canvas_w = 3 * 160 + 80
canvas_h = 4 * 160 + 120
canvas = Image.new('RGBA', (canvas_w, canvas_h), (18, 12, 6, 255))
draw = ImageDraw.Draw(canvas)

draw.text((40 + 20, 20), 'OPCAO 1: Vis Streams', fill=(251, 191, 36, 255))
draw.text((40 + 160 + 40 + 20, 20), 'OPCAO 2: Thaumic Mandala', fill=(245, 158, 11, 255))
draw.text((40 + 320 + 80 + 20, 20), 'OPCAO 3: Divine Crucible', fill=(254, 240, 138, 255))

for row_idx, shape in enumerate(shapes):
    y_pos = 60 + row_idx * 160
    draw.text((10, y_pos + 60), shape.upper(), fill=(148, 163, 184, 255))
    for opt in [1, 2, 3]:
        gif_p = OUT_DIR / f'ichorium_opt{opt}_{shape}.gif'
        if gif_p.exists():
            gif = Image.open(gif_p)
            gif.seek(14)
            frame = gif.convert('RGBA')
            scaled = frame.resize((128, 128), Image.Resampling.NEAREST)
            x_pos = 50 + (opt - 1) * (160 + 20)
            draw.rectangle([x_pos - 6, y_pos - 6, x_pos + 134, y_pos + 134], fill=(28, 18, 8, 255), outline=(65, 40, 15, 255))
            canvas.paste(scaled, (x_pos, y_pos), scaled)

canvas.save(ARTIFACT_DIR / 'ichorium_grid.png')
print("Grade comparativa do Ichorium salva!")

html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Ichorium — Avaliação de 3 Opções Visuais</title>
  <style>
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}
    body {{
      background-color: #0b0704;
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
      background: linear-gradient(135deg, #381a02 0%, #1e1005 60%, #0d0702 100%);
      border: 1px solid rgba(245, 158, 11, 0.35);
      border-radius: 14px;
      padding: 20px 24px;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      box-shadow: 0 10px 25px -5px rgba(245, 158, 11, 0.2);
    }}
    .badge {{
      display: inline-block;
      padding: 2px 8px;
      border-radius: 9999px;
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      background: rgba(245, 158, 11, 0.2);
      color: #fbbf24;
      border: 1px solid rgba(245, 158, 11, 0.4);
      margin-bottom: 6px;
    }}
    .formula-tag {{
      font-size: 12px;
      color: #fef08a;
      font-family: monospace;
      margin-left: 8px;
    }}
    h1 {{
      font-size: 22px;
      font-weight: 800;
      background: linear-gradient(to right, #fbbf24, #f59e0b, #d97706);
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
      background: #181008;
      padding: 8px 14px;
      border-radius: 10px;
      border: 1px solid #302010;
    }}
    .btn-toggle {{
      background: #d97706;
      color: white;
      border: none;
      padding: 8px 14px;
      border-radius: 8px;
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
      box-shadow: 0 4px 12px rgba(217, 119, 6, 0.35);
      transition: all 0.2s;
    }}
    .btn-toggle:hover {{
      background: #f59e0b;
    }}
    
    .shape-bar {{
      background: #181008;
      border: 1px solid #302010;
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
      background: #0b0704;
      padding: 4px;
      border-radius: 8px;
      border: 1px solid #302010;
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
      background: #d97706;
      color: #ffffff;
      box-shadow: 0 2px 6px rgba(217, 119, 6, 0.4);
    }}
    .btn-shape:hover:not(.active) {{
      color: #ffffff;
      background: #302010;
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
      background: #181008;
      border: 2px solid #302010;
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
      border-color: rgba(245, 158, 11, 0.5);
      transform: translateY(-2px);
    }}
    .card.selected {{
      border-color: #f59e0b;
      box-shadow: 0 0 20px rgba(245, 158, 11, 0.25);
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
      background: rgba(245, 158, 11, 0.2);
      color: #fbbf24;
      border: 1px solid rgba(245, 158, 11, 0.3);
    }}
    .card-title {{
      font-size: 16px;
      font-weight: 700;
      color: #fef3c7;
      margin-top: 6px;
    }}
    .card-desc {{
      font-size: 12px;
      color: #94a3b8;
      margin-top: 4px;
      line-height: 1.45;
    }}
    
    .image-box {{
      background: #090502;
      border: 1px solid #302010;
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
    
    @keyframes celestialHaloPulse {{
      0%, 100% {{
        filter: drop-shadow(0 0 8px rgba(245, 158, 11, 0.8)) drop-shadow(0 0 20px rgba(251, 191, 36, 0.45));
        transform: scale(1);
      }}
      50% {{
        filter: drop-shadow(0 0 16px rgba(251, 191, 36, 1.0)) drop-shadow(0 0 32px rgba(254, 240, 138, 0.7));
        transform: scale(1.02);
      }}
    }}
    .halo-effect {{
      animation: celestialHaloPulse 2.4s ease-in-out infinite;
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
      background: #261608;
      color: #cbd5e1;
    }}
    .btn-approve:hover {{
      background: #d97706;
      color: #ffffff;
      box-shadow: 0 4px 14px rgba(217, 119, 6, 0.4);
    }}
    .card.selected .btn-approve {{
      background: linear-gradient(135deg, #d97706, #fbbf24);
      color: #1a0800;
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
      background: #241407;
      color: #fde68a;
      border: 1px solid #302010;
    }}
    
    .footer-box {{
      background: #181008;
      border: 1px solid #302010;
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
          <span class="formula-tag">IcMa • UEV / UIV Tier</span>
        </div>
        <h1>Ichorium — 3 Opções de Animação</h1>
        <p class="subtitle">
          Texturas novas fluidas de 30 frames combinadas com o <strong>Celestial Halo Shader</strong> (<code style="color:#fde68a">renderblender:halo</code>).
        </p>
      </div>

      <div class="shader-control">
        <div>
          <div style="font-size:10px; text-transform:uppercase; color:#94a3b8;">Shader In-Game</div>
          <div id="shaderStatusText" style="font-size:12px; font-weight:800; color:#fbbf24;">HALO ATIVADO</div>
        </div>
        <button class="btn-toggle" id="btnToggleHalo" onclick="toggleShader()">Alternar Halo</button>
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
            <span style="font-size:11px; color:#64748b;">Vis Streams</span>
          </div>
          <div class="card-title">Celestial Vis Streams</div>
          <p class="card-desc">
            Correntes laminares entrelaçadas de <strong>Vis celestial puro</strong> fluindo suavemente através do âmbar, com nódulos orbes orbitais dourados de energia contínua.
          </p>
          <div class="features-list">
            <span class="feature-item">Fluxo Laminar de Vis</span>
            <span class="feature-item">Orbes Dourados Orbitais</span>
            <span class="feature-item">Âmbar Sagrado Fluido</span>
          </div>
        </div>

        <div class="image-box">
          <div id="wrapper-1" class="halo-effect">
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
            <span style="font-size:11px; color:#64748b;">Mandala Arcana</span>
          </div>
          <div class="card-title">Thaumic Mandala Resonance</div>
          <p class="card-desc">
            Geometria sagrada táumica em <strong>simetria de 8 pontas</strong> com anéis harmônicos concêntricos que giram e acendem nós rúnicos em sequência cíclica.
          </p>
          <div class="features-list">
            <span class="feature-item">Simetria Óctupla</span>
            <span class="feature-item">Anéis Concêntricos</span>
            <span class="feature-item">Nós Rúnicos Sagrados</span>
          </div>
        </div>

        <div class="image-box">
          <div id="wrapper-2" class="halo-effect">
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
            <span style="font-size:11px; color:#64748b;">Sangue Divino</span>
          </div>
          <div class="card-title">Ichor Divine Crucible</div>
          <p class="card-desc">
            Alquimia do "Sangue dos Deuses": <strong>micro-gotas de essência celestial ascendem contra a gravidade</strong> pelo metal em levitação com efervescência solar.
          </p>
          <div class="features-list">
            <span class="feature-item">Levitação de Gotas</span>
            <span class="feature-item">Dissolução Fotônica</span>
            <span class="feature-item">Sangue dos Deuses</span>
          </div>
        </div>

        <div class="image-box">
          <div id="wrapper-3" class="halo-effect">
            <img id="img-3" class="pixelated-art" src="{b64_data[3]['ingot']}" alt="Opção 3 Ingot">
          </div>
        </div>

        <button class="btn-approve" onclick="selectCard(3)">Aprovar Opção 3 (Responder 3)</button>
      </div>

    </div>

    <div class="footer-box">
      <div>
        Qual das 3 opções você prefere aprovar para o <strong>Ichorium</strong>?
      </div>
      <div style="font-weight:700; color:#fbbf24;">
        Basta responder 1, 2 ou 3 no chat!
      </div>
    </div>

  </div>

  <script>
    const data = {json_b64};
    let currentShape = 'ingot';
    let haloEnabled = true;

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
      haloEnabled = !haloEnabled;
      const statusText = document.getElementById('shaderStatusText');
      const toggleBtn = document.getElementById('btnToggleHalo');

      for (let opt = 1; opt <= 3; opt++) {{
        const wrap = document.getElementById('wrapper-' + opt);
        if (wrap) {{
          if (haloEnabled) {{
            wrap.classList.add('halo-effect');
          }} else {{
            wrap.classList.remove('halo-effect');
          }}
        }}
      }}

      if (haloEnabled) {{
        statusText.innerText = "HALO ATIVADO";
        statusText.style.color = "#fbbf24";
        toggleBtn.innerText = "Desativar Halo";
      }} else {{
        statusText.innerText = "TEXTURA PURA";
        statusText.style.color = "#94a3b8";
        toggleBtn.innerText = "Ativar Halo";
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
