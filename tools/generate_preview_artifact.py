import io
import base64
from pathlib import Path
from PIL import Image

ARTIFACT_DIR = Path('/home/raishxn/.gemini/antigravity/brain/2e34b5c7-86d1-4048-a95b-c9306bfb8b8a')
ROOT = Path('/home/raishxn/MineProjects/GregTech-Nexus-Addon')

def strip_to_gif_b64(path, upscale=5):
    im = Image.open(path)
    w, h = im.size
    n_frames = min(30, h // w)
    frames = []
    for i in range(n_frames):
        f = im.crop((0, i * w, w, (i + 1) * w)).convert('RGBA')
        f_up = f.resize((w * upscale, w * upscale), Image.NEAREST)
        frames.append(f_up)
    buf = io.BytesIO()
    frames[0].save(buf, format='GIF', save_all=True, append_images=frames[1:], duration=80, loop=0, disposal=2)
    return 'data:image/gif;base64,' + base64.b64encode(buf.getvalue()).decode('ascii')

def img_to_b64(path, upscale=5):
    im = Image.open(path).convert('RGBA')
    w, h = im.size
    im_up = im.resize((w * upscale, h * upscale), Image.NEAREST)
    buf = io.BytesIO()
    im_up.save(buf, format='PNG')
    return 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode('ascii')

def comp_wire_fine_b64(set_name, upscale=5):
    base_p = ROOT / f'src/main/resources/assets/gtceu/textures/item/material_sets/{set_name}/wire_fine.png'
    ov_p = ROOT / f'src/main/resources/assets/gtceu/textures/item/material_sets/{set_name}/wire_fine_overlay.png'
    im_base = Image.open(base_p).convert('RGBA').crop((0, 0, 16, 16))
    im_ov = Image.open(ov_p).convert('RGBA')
    comp = Image.alpha_composite(im_base, im_ov)
    w, h = comp.size
    comp_up = comp.resize((w * upscale, h * upscale), Image.NEAREST)
    buf = io.BytesIO()
    comp_up.save(buf, format='PNG')
    return 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode('ascii')

# 1. Tonalidades
shirabon_gif = strip_to_gif_b64(ROOT / 'src/main/resources/assets/gtceu/textures/item/material_sets/gtna_shirabon/ingot.png')
dragon_gif = strip_to_gif_b64(ROOT / 'src/main/resources/assets/gtceu/textures/item/material_sets/gtna_dragon_metal/ingot.png')
hastelloy_gif = strip_to_gif_b64(ROOT / 'src/main/resources/assets/gtceu/textures/item/material_sets/gtna_hastelloy_n_75/ingot.png')
hastelloy_casing_png = img_to_b64(ROOT / 'src/main/resources/assets/gtna/textures/block/casings/hastelloy_n_75_casing.png')
hastelloy_pipe_png = img_to_b64(ROOT / 'src/main/resources/assets/gtna/textures/block/hastelloy_n_75_pipe.png')

# 2. Silhuetas
stellite_gif = strip_to_gif_b64(ROOT / 'src/main/resources/assets/gtceu/textures/item/material_sets/gtna_stellite/ingot.png')
indalloy_gif = strip_to_gif_b64(ROOT / 'src/main/resources/assets/gtceu/textures/item/material_sets/gtna_indalloy_140/ingot.png')
shijima_gif = strip_to_gif_b64(ROOT / 'src/main/resources/assets/gtceu/textures/item/material_sets/gtna_shijima/ingot.png')
marm200_gif = strip_to_gif_b64(ROOT / 'src/main/resources/assets/gtceu/textures/item/material_sets/gtna_mar_m_200_steel/ingot.png')

# 3. Fine wire overlays
wf_white_dwarf = comp_wire_fine_b64('gtna_white_dwarf_matter')
wf_dragon = comp_wire_fine_b64('gtna_dragon_metal')
wf_hastelloy = comp_wire_fine_b64('gtna_hastelloy_n_75')
wf_shirabon = comp_wire_fine_b64('gtna_shirabon')

# 4. Singularity, multi-plates, multi-ingots, pipes, liquids
sing_shirabon = strip_to_gif_b64(ROOT / 'src/main/resources/assets/gtceu/textures/item/material_sets/gtna_shirabon/singularity.png')
sing_dragon = strip_to_gif_b64(ROOT / 'src/main/resources/assets/gtceu/textures/item/material_sets/gtna_dragon_metal/singularity.png')
sing_hastelloy = strip_to_gif_b64(ROOT / 'src/main/resources/assets/gtceu/textures/item/material_sets/gtna_hastelloy_n_75/singularity.png')

ingot_double_shirabon = strip_to_gif_b64(ROOT / 'src/main/resources/assets/gtceu/textures/item/material_sets/gtna_shirabon/ingot_double.png')
ingot_triple_shirabon = strip_to_gif_b64(ROOT / 'src/main/resources/assets/gtceu/textures/item/material_sets/gtna_shirabon/ingot_triple.png')
ingot_quad_shirabon = strip_to_gif_b64(ROOT / 'src/main/resources/assets/gtceu/textures/item/material_sets/gtna_shirabon/ingot_quadruple.png')

plate_triple_dragon = strip_to_gif_b64(ROOT / 'src/main/resources/assets/gtceu/textures/item/material_sets/gtna_dragon_metal/plate_triple.png')
plate_superdense_dragon = strip_to_gif_b64(ROOT / 'src/main/resources/assets/gtceu/textures/item/material_sets/gtna_dragon_metal/plate_superdense.png')
gear_dragon = strip_to_gif_b64(ROOT / 'src/main/resources/assets/gtceu/textures/item/material_sets/gtna_dragon_metal/gear.png')
rod_long_dragon = strip_to_gif_b64(ROOT / 'src/main/resources/assets/gtceu/textures/item/material_sets/gtna_dragon_metal/rod_long.png')

pipe_hastelloy = strip_to_gif_b64(ROOT / 'src/main/resources/assets/gtceu/textures/block/material_sets/gtna_hastelloy_n_75/pipe_side.png')
liquid_hastelloy = strip_to_gif_b64(ROOT / 'src/main/resources/assets/gtceu/textures/block/material_sets/gtna_hastelloy_n_75/liquid.png')
molten_shirabon = strip_to_gif_b64(ROOT / 'src/main/resources/assets/gtceu/textures/block/material_sets/gtna_shirabon/molten.png')
wire_side_shirabon = strip_to_gif_b64(ROOT / 'src/main/resources/assets/gtceu/textures/block/material_sets/gtna_shirabon/wire_side.png')

html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>GTNA Animated Material Sets Showcase</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    .pixelated {{
      image-rendering: pixelated;
      image-rendering: crisp-edges;
    }}
  </style>
</head>
<body class="bg-[var(--background)] text-[var(--foreground)] antialiased p-6">
  <div class="max-w-5xl mx-auto space-y-8">
    
    <!-- Header -->
    <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-6 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-500 mb-2">
          <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          Validação Visual de Texturas Animadas
        </div>
        <h1 class="text-2xl font-bold tracking-tight">Galeria de Material Sets do GTNA</h1>
        <p class="text-sm text-[var(--muted-foreground)] mt-1">Calibração de cores, silhuetas estruturais (gordinhos vs pequenininhos), carretel de fios finos e novos blocos/itens.</p>
      </div>
      <div class="flex items-center gap-3 text-xs text-[var(--muted-foreground)]">
        <div class="px-3 py-2 rounded-lg bg-[var(--card)] border border-[var(--border)]">
          Zoom: <span class="font-bold text-[var(--foreground)]">500% (Pixel-Perfect)</span>
        </div>
      </div>
    </div>

    <!-- Seção 1: Calibração de Tonalidade -->
    <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-6 shadow-sm space-y-5">
      <div>
        <h2 class="text-lg font-semibold flex items-center gap-2">
          <span>🎨</span> 1. Calibração de Tonalidade (Shirabon, Dragonblood, Hastelloy)
        </h2>
        <p class="text-sm text-[var(--muted-foreground)]">Cores alinhadas aos padrões canônicos de GTNH/GT++ e sincronização exata com carcaças e blocos.</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
        <!-- Shirabon -->
        <div class="p-4 rounded-xl bg-[var(--background)] border border-[var(--border)] flex flex-col items-center text-center space-y-3">
          <div class="relative p-3 bg-black/40 rounded-lg border border-white/5">
            <img src="{shirabon_gif}" class="pixelated w-20 h-20" alt="Shirabon Ingot">
          </div>
          <div>
            <div class="font-semibold text-sm">Shirabon Ingot</div>
            <div class="text-xs text-fuchsia-400 font-mono mt-0.5">#c61361 (Magenta Afinação)</div>
            <p class="text-xs text-[var(--muted-foreground)] mt-1.5 leading-relaxed">
              Substituído o antigo tom pastel rosa-bebê desbotado por um magenta ressonante e profundo com ondas osciloscópicas em roxo/fúcsia elétrico.
            </p>
          </div>
        </div>

        <!-- Dragon Metal -->
        <div class="p-4 rounded-xl bg-[var(--background)] border border-[var(--border)] flex flex-col items-center text-center space-y-3">
          <div class="relative p-3 bg-black/40 rounded-lg border border-white/5">
            <img src="{dragon_gif}" class="pixelated w-20 h-20" alt="Dragon Metal Ingot">
          </div>
          <div>
            <div class="font-semibold text-sm">Dragon Metal Ingot</div>
            <div class="text-xs text-rose-500 font-mono mt-0.5">#dc2814 (Dragonblood Carmesim)</div>
            <p class="text-xs text-[var(--muted-foreground)] mt-1.5 leading-relaxed">
              Substituído o tom alaranjado/salmão pelo autêntico carmesim-rubi do GT++, pulsando como o coração de um dragão sem lavar as cores.
            </p>
          </div>
        </div>

        <!-- Hastelloy N 75 Trio -->
        <div class="p-4 rounded-xl bg-[var(--background)] border border-[var(--border)] flex flex-col items-center text-center space-y-3">
          <div class="flex items-center gap-2 p-2 bg-black/40 rounded-lg border border-white/5">
            <div class="flex flex-col items-center">
              <img src="{hastelloy_gif}" class="pixelated w-16 h-16" alt="Hastelloy Ingot">
              <span class="text-[10px] text-[var(--muted-foreground)] mt-1">Ingot</span>
            </div>
            <span class="text-xs text-[var(--muted-foreground)]">≈</span>
            <div class="flex flex-col items-center">
              <img src="{hastelloy_casing_png}" class="pixelated w-16 h-16" alt="Hastelloy Casing">
              <span class="text-[10px] text-[var(--muted-foreground)] mt-1">Casing</span>
            </div>
            <span class="text-xs text-[var(--muted-foreground)]">≈</span>
            <div class="flex flex-col items-center">
              <img src="{hastelloy_pipe_png}" class="pixelated w-16 h-16" alt="Hastelloy Pipe">
              <span class="text-[10px] text-[var(--muted-foreground)] mt-1">Pipe</span>
            </div>
          </div>
          <div>
            <div class="font-semibold text-sm">Hastelloy N 75 (Alinhamento Total)</div>
            <div class="text-xs text-lime-400 font-mono mt-0.5">#5a5c44 (Verde-Oliva Metálico)</div>
            <p class="text-xs text-[var(--muted-foreground)] mt-1.5 leading-relaxed">
              O ingot abandonou o tom bronze-âmbar e agora replica perfeitamente a tonalidade khaki/verde-oliva militar da sua carcaça e do seu tubo de aeração!
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Seção 2: Variação Estrutural de Silhuetas de Ingots -->
    <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-6 shadow-sm space-y-5">
      <div>
        <h2 class="text-lg font-semibold flex items-center gap-2">
          <span>📐</span> 2. Variação de Silhueta Estrutural (Gordinhos vs Pequenininhos)
        </h2>
        <p class="text-sm text-[var(--muted-foreground)]">Ligas pesadas recebem o perfil robusto ("gordinho", estilo Ultimet), ligas fusíveis recebem o perfil delicado ("pequenininho", estilo Battery Alloy), e materiais cósmicos mantêm o formato padrão.</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
        <!-- Gordinhos -->
        <div class="p-4 rounded-xl bg-amber-500/5 border border-amber-500/20 flex flex-col items-center text-center space-y-3">
          <div class="text-xs font-semibold text-amber-500 uppercase tracking-wider">Mais Gordinho (Ultimet / Shiny)</div>
          <div class="flex items-center gap-3 p-3 bg-black/40 rounded-lg border border-white/5">
            <div class="flex flex-col items-center">
              <img src="{stellite_gif}" class="pixelated w-16 h-16" alt="Stellite">
              <span class="text-[10px] text-[var(--muted-foreground)] mt-1">Stellite</span>
            </div>
            <div class="flex flex-col items-center">
              <img src="{marm200_gif}" class="pixelated w-16 h-16" alt="Mar-M 200">
              <span class="text-[10px] text-[var(--muted-foreground)] mt-1">Mar-M 200</span>
            </div>
            <div class="flex flex-col items-center">
              <img src="{hastelloy_gif}" class="pixelated w-16 h-16" alt="Hastelloy">
              <span class="text-[10px] text-[var(--muted-foreground)] mt-1">Hastelloy N</span>
            </div>
          </div>
          <div class="text-xs text-[var(--muted-foreground)] leading-relaxed">
            Silhueta densa de <span class="text-[var(--foreground)] font-semibold">136 pixels</span> com bordas volumosas e glint de reflexo nos cantos. Ideal para superligas de alta resistência mecânica e cobalto.
          </div>
        </div>

        <!-- Pequenininhos -->
        <div class="p-4 rounded-xl bg-sky-500/5 border border-sky-500/20 flex flex-col items-center text-center space-y-3">
          <div class="text-xs font-semibold text-sky-400 uppercase tracking-wider">Mais Pequenininho (Battery Alloy / Dull)</div>
          <div class="flex items-center gap-3 p-3 bg-black/40 rounded-lg border border-white/5">
            <div class="flex flex-col items-center">
              <img src="{indalloy_gif}" class="pixelated w-16 h-16" alt="Indalloy 140">
              <span class="text-[10px] text-[var(--muted-foreground)] mt-1">Indalloy 140</span>
            </div>
            <div class="flex flex-col items-center">
              <img src="{shijima_gif}" class="pixelated w-16 h-16" alt="Shijima">
              <span class="text-[10px] text-[var(--muted-foreground)] mt-1">Shijima</span>
            </div>
          </div>
          <div class="text-xs text-[var(--muted-foreground)] leading-relaxed">
            Silhueta compacta de <span class="text-[var(--foreground)] font-semibold">114 pixels</span> (perfil suave e esguio). Perfeito para ligas fusíveis como Indalloy 140 (bismuto-índio) e ligas de memória de forma / serenidade.
          </div>
        </div>

        <!-- Padrão Moderno -->
        <div class="p-4 rounded-xl bg-purple-500/5 border border-purple-500/20 flex flex-col items-center text-center space-y-3">
          <div class="text-xs font-semibold text-purple-400 uppercase tracking-wider">Padrão Moderno (WhiteDwarf / High-Tech)</div>
          <div class="flex items-center gap-3 p-3 bg-black/40 rounded-lg border border-white/5">
            <div class="flex flex-col items-center">
              <img src="{shirabon_gif}" class="pixelated w-16 h-16" alt="Shirabon">
              <span class="text-[10px] text-[var(--muted-foreground)] mt-1">Shirabon</span>
            </div>
            <div class="flex flex-col items-center">
              <img src="{dragon_gif}" class="pixelated w-16 h-16" alt="Dragon Metal">
              <span class="text-[10px] text-[var(--muted-foreground)] mt-1">Dragon Metal</span>
            </div>
          </div>
          <div class="text-xs text-[var(--muted-foreground)] leading-relaxed">
            Silhueta chanfrada de <span class="text-[var(--foreground)] font-semibold">135 pixels</span> do padrão Modernity GTNH. Conservada para metais energéticos, transurânicos e materiais cósmicos.
          </div>
        </div>
      </div>
    </div>

    <!-- Seção 3: Carretel em Fine Wires -->
    <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-6 shadow-sm space-y-5">
      <div>
        <h2 class="text-lg font-semibold flex items-center gap-2">
          <span>🧵</span> 3. Correção do Overlay Padrão nos Fios Finos (Fine Wires)
        </h2>
        <p class="text-sm text-[var(--muted-foreground)]">O overlay do carretel de madeira tradicional (115 pixels não-transparentes de wireFine_OVERLAY) foi restaurado sobre as espirais metálicas animadas.</p>
      </div>

      <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div class="p-3 rounded-xl bg-[var(--background)] border border-[var(--border)] flex flex-col items-center text-center space-y-2">
          <div class="p-2 bg-black/40 rounded-lg border border-white/5">
            <img src="{wf_white_dwarf}" class="pixelated w-16 h-16" alt="White Dwarf Fine Wire">
          </div>
          <div class="text-xs font-medium">White Dwarf</div>
        </div>
        <div class="p-3 rounded-xl bg-[var(--background)] border border-[var(--border)] flex flex-col items-center text-center space-y-2">
          <div class="p-2 bg-black/40 rounded-lg border border-white/5">
            <img src="{wf_shirabon}" class="pixelated w-16 h-16" alt="Shirabon Fine Wire">
          </div>
          <div class="text-xs font-medium">Shirabon</div>
        </div>
        <div class="p-3 rounded-xl bg-[var(--background)] border border-[var(--border)] flex flex-col items-center text-center space-y-2">
          <div class="p-2 bg-black/40 rounded-lg border border-white/5">
            <img src="{wf_dragon}" class="pixelated w-16 h-16" alt="Dragon Metal Fine Wire">
          </div>
          <div class="text-xs font-medium">Dragon Metal</div>
        </div>
        <div class="p-3 rounded-xl bg-[var(--background)] border border-[var(--border)] flex flex-col items-center text-center space-y-2">
          <div class="p-2 bg-black/40 rounded-lg border border-white/5">
            <img src="{wf_hastelloy}" class="pixelated w-16 h-16" alt="Hastelloy Fine Wire">
          </div>
          <div class="text-xs font-medium">Hastelloy N 75</div>
        </div>
      </div>
    </div>

    <!-- Seção 4: Novos Componentes e Blocos -->
    <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-6 shadow-sm space-y-5">
      <div>
        <h2 class="text-lg font-semibold flex items-center gap-2">
          <span>⚙️</span> 4. Novos Componentes, Singularidades, Tubulações e Fluidos
        </h2>
        <p class="text-sm text-[var(--muted-foreground)]">Todos os componentes que faltavam foram gerados em lote com animações completas (.png + .mcmeta + models).</p>
      </div>

      <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-3">
        <!-- Singularity -->
        <div class="p-3 rounded-xl bg-[var(--background)] border border-[var(--border)] flex flex-col items-center text-center space-y-1.5">
          <div class="p-1.5 bg-black/40 rounded-lg border border-white/5">
            <img src="{sing_shirabon}" class="pixelated w-12 h-12" alt="Shirabon Singularity">
          </div>
          <div class="text-[11px] font-medium leading-tight">Singularity<br><span class="text-[var(--muted-foreground)] text-[10px]">Shirabon</span></div>
        </div>

        <div class="p-3 rounded-xl bg-[var(--background)] border border-[var(--border)] flex flex-col items-center text-center space-y-1.5">
          <div class="p-1.5 bg-black/40 rounded-lg border border-white/5">
            <img src="{sing_dragon}" class="pixelated w-12 h-12" alt="Dragon Singularity">
          </div>
          <div class="text-[11px] font-medium leading-tight">Singularity<br><span class="text-[var(--muted-foreground)] text-[10px]">Dragon Metal</span></div>
        </div>

        <!-- Ingot Double / Quad -->
        <div class="p-3 rounded-xl bg-[var(--background)] border border-[var(--border)] flex flex-col items-center text-center space-y-1.5">
          <div class="p-1.5 bg-black/40 rounded-lg border border-white/5">
            <img src="{ingot_double_shirabon}" class="pixelated w-12 h-12" alt="Ingot Double">
          </div>
          <div class="text-[11px] font-medium leading-tight">Ingot Double<br><span class="text-[var(--muted-foreground)] text-[10px]">Shirabon</span></div>
        </div>

        <div class="p-3 rounded-xl bg-[var(--background)] border border-[var(--border)] flex flex-col items-center text-center space-y-1.5">
          <div class="p-1.5 bg-black/40 rounded-lg border border-white/5">
            <img src="{ingot_quad_shirabon}" class="pixelated w-12 h-12" alt="Ingot Quadruple">
          </div>
          <div class="text-[11px] font-medium leading-tight">Ingot Quadruple<br><span class="text-[var(--muted-foreground)] text-[10px]">Shirabon</span></div>
        </div>

        <!-- Superdense Plate -->
        <div class="p-3 rounded-xl bg-[var(--background)] border border-[var(--border)] flex flex-col items-center text-center space-y-1.5">
          <div class="p-1.5 bg-black/40 rounded-lg border border-white/5">
            <img src="{plate_superdense_dragon}" class="pixelated w-12 h-12" alt="Plate Superdense">
          </div>
          <div class="text-[11px] font-medium leading-tight">Superdense Plate<br><span class="text-[var(--muted-foreground)] text-[10px]">Dragon Metal</span></div>
        </div>

        <!-- Gear -->
        <div class="p-3 rounded-xl bg-[var(--background)] border border-[var(--border)] flex flex-col items-center text-center space-y-1.5">
          <div class="p-1.5 bg-black/40 rounded-lg border border-white/5">
            <img src="{gear_dragon}" class="pixelated w-12 h-12" alt="Gear">
          </div>
          <div class="text-[11px] font-medium leading-tight">Gear<br><span class="text-[var(--muted-foreground)] text-[10px]">Dragon Metal</span></div>
        </div>

        <!-- Long Rod -->
        <div class="p-3 rounded-xl bg-[var(--background)] border border-[var(--border)] flex flex-col items-center text-center space-y-1.5">
          <div class="p-1.5 bg-black/40 rounded-lg border border-white/5">
            <img src="{rod_long_dragon}" class="pixelated w-12 h-12" alt="Long Rod">
          </div>
          <div class="text-[11px] font-medium leading-tight">Long Rod<br><span class="text-[var(--muted-foreground)] text-[10px]">Dragon Metal</span></div>
        </div>

        <!-- Fluid Pipe -->
        <div class="p-3 rounded-xl bg-[var(--background)] border border-[var(--border)] flex flex-col items-center text-center space-y-1.5">
          <div class="p-1.5 bg-black/40 rounded-lg border border-white/5">
            <img src="{pipe_hastelloy}" class="pixelated w-12 h-12" alt="Fluid Pipe">
          </div>
          <div class="text-[11px] font-medium leading-tight">Fluid Pipe Side<br><span class="text-[var(--muted-foreground)] text-[10px]">Hastelloy N 75</span></div>
        </div>

        <!-- Liquid -->
        <div class="p-3 rounded-xl bg-[var(--background)] border border-[var(--border)] flex flex-col items-center text-center space-y-1.5">
          <div class="p-1.5 bg-black/40 rounded-lg border border-white/5">
            <img src="{liquid_hastelloy}" class="pixelated w-12 h-12" alt="Liquid Fluid">
          </div>
          <div class="text-[11px] font-medium leading-tight">Liquid Still<br><span class="text-[var(--muted-foreground)] text-[10px]">Hastelloy N 75</span></div>
        </div>

        <!-- Molten -->
        <div class="p-3 rounded-xl bg-[var(--background)] border border-[var(--border)] flex flex-col items-center text-center space-y-1.5">
          <div class="p-1.5 bg-black/40 rounded-lg border border-white/5">
            <img src="{molten_shirabon}" class="pixelated w-12 h-12" alt="Molten Fluid">
          </div>
          <div class="text-[11px] font-medium leading-tight">Molten Fluid<br><span class="text-[var(--muted-foreground)] text-[10px]">Shirabon</span></div>
        </div>

        <!-- Wire -->
        <div class="p-3 rounded-xl bg-[var(--background)] border border-[var(--border)] flex flex-col items-center text-center space-y-1.5">
          <div class="p-1.5 bg-black/40 rounded-lg border border-white/5">
            <img src="{wire_side_shirabon}" class="pixelated w-12 h-12" alt="Cable Wire Side">
          </div>
          <div class="text-[11px] font-medium leading-tight">Cable Wire Side<br><span class="text-[var(--muted-foreground)] text-[10px]">Shirabon</span></div>
        </div>

        <!-- Hastelloy Singularity -->
        <div class="p-3 rounded-xl bg-[var(--background)] border border-[var(--border)] flex flex-col items-center text-center space-y-1.5">
          <div class="p-1.5 bg-black/40 rounded-lg border border-white/5">
            <img src="{sing_hastelloy}" class="pixelated w-12 h-12" alt="Hastelloy Singularity">
          </div>
          <div class="text-[11px] font-medium leading-tight">Singularity<br><span class="text-[var(--muted-foreground)] text-[10px]">Hastelloy N 75</span></div>
        </div>
      </div>
    </div>

  </div>
</body>
</html>
"""

out_path = ARTIFACT_DIR / 'material_preview.html'
out_path.write_text(html_content, encoding='utf-8')
print('HTML artifact created successfully at:', out_path)
