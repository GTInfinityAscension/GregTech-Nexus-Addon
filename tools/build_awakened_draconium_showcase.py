import json
import base64
from pathlib import Path

OUT_DIR = Path("/tmp/awakened_draconium_candidates")
ARTIFACT_PATH = Path("/home/raishxn/.gemini/antigravity/brain/9c95a421-582d-4dd9-a627-e59f2d3d6c06/awakened_draconium_showcase.html")

shapes = ["ingot", "plate", "gear", "block"]
options = [1, 2, 3]

b64_data = {}
for opt in options:
    b64_data[opt] = {}
    for shape in shapes:
        gif_file = OUT_DIR / f"awakened_draconium_opt{opt}_{shape}.gif"
        if gif_file.exists():
            b64 = base64.b64encode(gif_file.read_bytes()).decode("utf-8")
            b64_data[opt][shape] = f"data:image/gif;base64,{b64}"
        else:
            b64_data[opt][shape] = ""

json_b64 = json.dumps(b64_data)

html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Awakened Draconium — Avaliação de 3 Opções Visuais</title>
  <style>
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}
    body {{
      background-color: #090d16;
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
      background: linear-gradient(135deg, #2b0f02 0%, #151c2e 60%, #0d121f 100%);
      border: 1px solid #f9731655;
      border-radius: 14px;
      padding: 20px 24px;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      box-shadow: 0 10px 25px -5px rgba(249, 115, 22, 0.15);
    }}
    .badge {{
      display: inline-block;
      padding: 2px 8px;
      border-radius: 9999px;
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      background: rgba(249, 115, 22, 0.2);
      color: #fb923c;
      border: 1px solid rgba(249, 115, 22, 0.4);
      margin-bottom: 6px;
    }}
    .formula-tag {{
      font-size: 12px;
      color: #fde047;
      font-family: monospace;
      margin-left: 8px;
    }}
    h1 {{
      font-size: 22px;
      font-weight: 800;
      background: linear-gradient(to right, #fb923c, #fcd34d, #fef08a);
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
      background: #0f172a;
      padding: 8px 14px;
      border-radius: 10px;
      border: 1px solid #1e293b;
    }}
    .btn-toggle {{
      background: #ea580c;
      color: white;
      border: none;
      padding: 8px 14px;
      border-radius: 8px;
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
      box-shadow: 0 4px 12px rgba(234, 88, 12, 0.35);
      transition: all 0.2s;
    }}
    .btn-toggle:hover {{
      background: #f97316;
    }}
    
    /* Navigation Bar */
    .shape-bar {{
      background: #0f172a;
      border: 1px solid #1e293b;
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
      background: #090d16;
      padding: 4px;
      border-radius: 8px;
      border: 1px solid #1e293b;
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
      background: #ea580c;
      color: #ffffff;
      box-shadow: 0 2px 6px rgba(234, 88, 12, 0.4);
    }}
    .btn-shape:hover:not(.active) {{
      color: #ffffff;
      background: #1e293b;
    }}
    
    /* Comparison Grid */
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
      background: #0f172a;
      border: 2px solid #1e293b;
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
      border-color: rgba(249, 115, 22, 0.5);
      transform: translateY(-2px);
    }}
    .card.selected {{
      border-color: #f97316;
      box-shadow: 0 0 20px rgba(249, 115, 22, 0.25);
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
      background: rgba(249, 115, 22, 0.2);
      color: #fb923c;
      border: 1px solid rgba(249, 115, 22, 0.3);
    }}
    .card-title {{
      font-size: 16px;
      font-weight: 700;
      color: #fed7aa;
      margin-top: 6px;
    }}
    .card-desc {{
      font-size: 12px;
      color: #94a3b8;
      margin-top: 4px;
      line-height: 1.45;
    }}
    
    /* Image Showcase Container */
    .image-box {{
      background: #050811;
      border: 1px solid #1e293b;
      border-radius: 12px;
      padding: 24px;
      display: flex;
      align-items: center;
      justify-content: center;
      min-height: 180px;
      position: relative;
      overflow: hidden;
    }}
    
    /* Crisp Pixelated Enlarged Image */
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
    
    /* Shader Halo Animation */
    @keyframes solarHaloGlow {{
      0%, 100% {{
        filter: drop-shadow(0 0 8px rgba(255, 110, 0, 0.8)) drop-shadow(0 0 20px rgba(255, 170, 0, 0.5));
        transform: scale(1);
      }}
      50% {{
        filter: drop-shadow(0 0 16px rgba(255, 80, 0, 1.0)) drop-shadow(0 0 32px rgba(255, 210, 0, 0.75));
        transform: scale(1.03);
      }}
    }}
    .halo-effect {{
      animation: solarHaloGlow 2.2s ease-in-out infinite;
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
      background: #1e293b;
      color: #cbd5e1;
    }}
    .btn-approve:hover {{
      background: #ea580c;
      color: #ffffff;
      box-shadow: 0 4px 14px rgba(234, 88, 12, 0.4);
    }}
    .card.selected .btn-approve {{
      background: linear-gradient(135deg, #ea580c, #f59e0b);
      color: white;
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
      background: #151c2e;
      color: #fcd34d;
      border: 1px solid #1e293b;
    }}
    
    .footer-box {{
      background: #0f172a;
      border: 1px solid #1e293b;
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
    
    <!-- Top Header -->
    <div class="header-card">
      <div>
        <div>
          <span class="badge">Refatoração de Textura</span>
          <span class="formula-tag">✵Dc✵ • UEV / UIV Tier</span>
        </div>
        <h1>Awakened Draconium — 3 Opções de Animação</h1>
        <p class="subtitle">
          Texturas novas fluidas de 30 frames combinadas com o <strong>Original Halo Shader</strong> (<code style="color:#fdba74">renderblender:halo</code>).
        </p>
      </div>

      <div class="shader-control">
        <div>
          <div style="font-size:10px; text-transform:uppercase; color:#94a3b8;">Shader In-Game</div>
          <div id="shaderStatusText" style="font-size:12px; font-weight:800; color:#fb923c;">HALO ATIVADO</div>
        </div>
        <button class="btn-toggle" id="btnToggleHalo" onclick="toggleShader()">Alternar Halo</button>
      </div>
    </div>

    <!-- Shape Selection Bar -->
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

    <!-- 3 Options Comparison Grid -->
    <div class="grid-options">
      
      <!-- Option 1 -->
      <div class="card selected" id="card-1">
        <div>
          <div class="card-header">
            <span class="tag-opt">Opção 1</span>
            <span style="font-size:11px; color:#64748b;">Solar Loops</span>
          </div>
          <div class="card-title">Draconic Core Fusion</div>
          <p class="card-desc">
            Núcleo térmico pulsante com <strong>loops magnéticos coronais</strong> (solar flares) giratórios que curvam plasma superaquecido sobre as facetas do metal.
          </p>
          <div class="features-list">
            <span class="feature-item">Arcs Magnéticos</span>
            <span class="feature-item">Respiração Térmica</span>
            <span class="feature-item">Núcleo Branco-Quente</span>
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
            <span style="font-size:11px; color:#64748b;">Chaos Arcs</span>
          </div>
          <div class="card-title">Chaos Dragon Sparking Arcs</div>
          <p class="card-desc">
            Runas dracônicas entalhadas nas arestas chanfradas que canalizam <strong>relâmpagos hiper-rápidos de plasma elétrico</strong> saltando entre os vértices com faíscas cósmicas.
          </p>
          <div class="features-list">
            <span class="feature-item">Runas nas Arestas</span>
            <span class="feature-item">Arcos Elétricos Rápidos</span>
            <span class="feature-item">Faíscas de Alta Tensão</span>
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
            <span style="font-size:11px; color:#64748b;">Solar Bénard</span>
          </div>
          <div class="card-title">Awakened Dragon Scales</div>
          <p class="card-desc">
            Malha celular orgânica inspirada em escamas com <strong>células solares de convecção (Bénard)</strong> onde o magma borbulha sob fissuras, com varredura de reflexo especular de luz a 45°.
          </p>
          <div class="features-list">
            <span class="feature-item">Convecção Celular</span>
            <span class="feature-item">Varredura Especular 45°</span>
            <span class="feature-item">Fissuras de Magma</span>
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

    <!-- Footer Instruction -->
    <div class="footer-box">
      <div>
        Qual das 3 opções você prefere aprovar para o <strong>Awakened Draconium</strong>?
      </div>
      <div style="font-weight:700; color:#fb923c;">
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
        statusText.style.color = "#fb923c";
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
print(f"Artifact atualizado com CSS puro e imagem 128px garantida em: {ARTIFACT_PATH}")
