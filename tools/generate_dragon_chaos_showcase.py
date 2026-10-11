#!/usr/bin/env python3
"""
Gera propostas visuais refinadas para Dragonmetal e Chaos Matter:
- 3 Candidatos para Dragonmetal (Ingot, Block, Plate, Gear, 30 frames)
- 3 Candidatos para Chaos Matter (Ingot, Block, Plate, Gear, 30 frames)
- Folhas de comparação estática e comparativos animados lado a lado
- Showcase interativo em HTML para o usuário
"""

import os
import io
import math
import json
import base64
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_DIR = Path("/home/raishxn/.gemini/antigravity/brain/55241845-10ae-45dc-8614-1f1a0d15ea2c")
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
DOCS_DIR = REPO_ROOT / "docs/visualization"
DOCS_DIR.mkdir(parents=True, exist_ok=True)

# Templates
MOD_DIR = Path("/home/raishxn/Downloads/Modernity-GTNH-2026-09-07/assets/gregtech/textures/items/materialicons/CUSTOM/WhiteDwarfMatter")
MOD_BLOCK_DIR = Path("/home/raishxn/Downloads/Modernity-GTNH-2026-09-07/assets/gregtech/textures/blocks/materialicons/CUSTOM/WhiteDwarfMatter")
GTCEU_SHINY_DIR = Path("/home/raishxn/MineProjects/GTCEu-7.5.3/src/main/resources/assets/gtceu/textures/item/material_sets/shiny")
GTCEU_SHINY_BLOCK_DIR = Path("/home/raishxn/MineProjects/GTCEu-7.5.3/src/main/resources/assets/gtceu/textures/block/material_sets/shiny")

def load_template(path):
    im = Image.open(path).convert("RGBA")
    arr = np.array(im, dtype=np.float32)
    h, w = arr.shape[:2]
    if h > w:
        arr = arr[:w, :, :]
    return arr

T_MOD_INGOT = load_template(MOD_DIR / "ingot.png")
T_MOD_PLATE = load_template(MOD_DIR / "plate.png")
T_MOD_GEAR = load_template(MOD_DIR / "gearGt.png")
T_MOD_BLOCK = load_template(MOD_BLOCK_DIR / "block1.png")

T_SHINY_INGOT = load_template(GTCEU_SHINY_DIR / "ingot.png")
T_SHINY_PLATE = load_template(GTCEU_SHINY_DIR / "plate.png")
T_SHINY_GEAR = load_template(GTCEU_SHINY_DIR / "gear.png")
T_SHINY_BLOCK = load_template(GTCEU_SHINY_BLOCK_DIR / "block.png")

def save_gif_file(frames, out_path, duration=66):
    p_frames = []
    for f in frames:
        im = Image.fromarray(f.astype(np.uint8), mode="RGBA")
        alpha = im.split()[3]
        mask = Image.eval(alpha, lambda a: 255 if a < 16 else 0)
        rgb = im.convert("RGB")
        p_frame = rgb.convert("P", palette=Image.ADAPTIVE, colors=254)
        p_frame.paste(255, mask)
        p_frame.info["transparency"] = 255
        p_frames.append(p_frame)

    p_frames[0].save(
        out_path,
        format="GIF",
        save_all=True,
        append_images=p_frames[1:],
        duration=duration,
        loop=0,
        disposal=2,
        transparency=255
    )

def save_gif_base64(frames, duration=66):
    buf = io.BytesIO()
    p_frames = []
    for f in frames:
        im = Image.fromarray(f.astype(np.uint8), mode="RGBA")
        alpha = im.split()[3]
        mask = Image.eval(alpha, lambda a: 255 if a < 16 else 0)
        rgb = im.convert("RGB")
        p_frame = rgb.convert("P", palette=Image.ADAPTIVE, colors=254)
        p_frame.paste(255, mask)
        p_frame.info["transparency"] = 255
        p_frames.append(p_frame)

    p_frames[0].save(
        buf,
        format="GIF",
        save_all=True,
        append_images=p_frames[1:],
        duration=duration,
        loop=0,
        disposal=2,
        transparency=255
    )
    return base64.b64encode(buf.getvalue()).decode("utf-8")

def extract_old_frames(rel_path, num_frames=30):
    full_path = REPO_ROOT / rel_path
    if not full_path.exists():
        return None
    im = Image.open(full_path).convert("RGBA")
    w, h = im.size
    frames_count = max(1, h // w)
    arr = np.array(im, dtype=np.uint8)
    frames = []
    for f in range(min(num_frames, frames_count)):
        sub = arr[f*w:(f+1)*w, :w, :]
        frames.append(sub)
    if not frames:
        frames = [arr[:w, :w, :]]
    res = []
    for i in range(num_frames):
        res.append(frames[i % len(frames)])
    return res

# =========================================================================
# 1. DRAGONMETAL (DRAGONBLOOD METAL) CANDIDATES
# =========================================================================

# Opção 1: Escama Dracônica Ancestral & Veias de Fogo (Ancient Wyrm Scales)
def render_dragonmetal_c1(template, n_frames=30):
    h, w = template.shape[:2]
    gray = template[:, :, 0]
    alpha = template[:, :, 3] > 0
    t_base = gray / 255.0
    y, x = np.ogrid[:h, :w]
    
    # Textura sutil de escama dracônica
    scale_pat = np.sin(x * 1.6 + y * 0.9) * 0.5 + 0.5
    
    frames = []
    for f in range(n_frames):
        tau = 2 * math.pi * (f / n_frames)
        
        # Sombra carmesim-obsidiana profunda (#22040e), corpo rubi arterial (#941028),
        # realce fogo dracônico vivo (#dc223e)
        r = 34.0 + t_base * 170.0 + scale_pat * (t_base > 0.45) * 16.0
        g = 4.0 + (t_base ** 2.0) * 44.0 + scale_pat * (t_base > 0.7) * 20.0
        b = 14.0 + (t_base ** 1.7) * 32.0
        
        # Pulso de calor dracônico diagonal sutil
        wave = np.sin((x + y) * 0.5 - tau) * 0.5 + 0.5
        ember = (wave ** 3.5) * (t_base > 0.35)
        
        # Chanfros superiores recebem glint dourado de escama nobre
        bevel = (y <= x + 2) & (t_base > 0.6)
        gold_glint = np.sin(x * 0.85 - tau) * 0.5 + 0.5
        gold_boost = (gold_glint ** 4.5) * bevel
        
        r += ember * 45.0 + gold_boost * 90.0
        g += ember * 18.0 + gold_boost * 78.0
        b += ember * 2.0 + gold_boost * 15.0
        
        frame = np.zeros((h, w, 4), dtype=np.uint8)
        frame[:, :, 0] = np.where(alpha, np.clip(r, 0, 255), 0)
        frame[:, :, 1] = np.where(alpha, np.clip(g, 0, 255), 0)
        frame[:, :, 2] = np.where(alpha, np.clip(b, 0, 255), 0)
        frame[:, :, 3] = np.where(alpha, 255, 0)
        frames.append(frame)
    return frames

# Opção 2: Coração Dracônico em Fusão & Sel-out Obsidiana (Molten Heart Core)
def render_dragonmetal_c2(template, n_frames=30):
    h, w = template.shape[:2]
    gray = template[:, :, 0]
    alpha = template[:, :, 3] > 0
    t_base = gray / 255.0
    y, x = np.ogrid[:h, :w]
    
    if np.sum(alpha) > 0:
        cy = np.sum(np.where(alpha, y, 0)) / np.sum(alpha)
        cx = np.sum(np.where(alpha, x, 0)) / np.sum(alpha)
    else:
        cy, cx = h / 2.0, w / 2.0
    dist = np.sqrt((x - cx)**2 + (y - cy)**2)
    max_d = max(1.0, np.max(dist[alpha])) if np.sum(alpha) > 0 else 8.0
    norm_dist = dist / max_d
    
    frames = []
    for f in range(n_frames):
        t = (f / n_frames) * 2 * math.pi
        # Duplo batimento cardíaco dracônico (lub-dub)
        pulse = np.maximum(0, np.sin(t))**3 + 0.55 * np.maximum(0, np.sin(t - 0.75))**3
        pulse = np.clip(pulse, 0, 1.2)
        
        # Base: obsidiana dracônica afiada nas bordas (#14020a) e rubi carmesim puro (#a2122b)
        r = 20.0 + t_base * 185.0
        g = 2.0 + (t_base ** 2.2) * 58.0
        b = 10.0 + (t_base ** 1.9) * 40.0
        
        # Núcleo radial vivo em fusão
        core_weight = np.clip(1.0 - norm_dist, 0, 1) ** 1.3
        heat = pulse * core_weight * (t_base > 0.2)
        
        r += heat * 110.0
        g += heat * 75.0
        b += heat * 20.0
        
        # Picos incandescentes ouro/branco no clímax da sístole
        hot_peak = np.clip(heat - 0.65, 0, 1) * 165.0
        r += hot_peak * 0.95
        g += hot_peak * 0.90
        b += hot_peak * 0.60
        
        frame = np.zeros((h, w, 4), dtype=np.uint8)
        frame[:, :, 0] = np.where(alpha, np.clip(r, 0, 255), 0)
        frame[:, :, 1] = np.where(alpha, np.clip(g, 0, 255), 0)
        frame[:, :, 2] = np.where(alpha, np.clip(b, 0, 255), 0)
        frame[:, :, 3] = np.where(alpha, 255, 0)
        frames.append(frame)
    return frames

# Opção 3: Aço Dracônico Modernity de Alto Contraste (Cromo Carmesim Puro)
def render_dragonmetal_c3(template, n_frames=30):
    h, w = template.shape[:2]
    gray = template[:, :, 0]
    alpha = template[:, :, 3] > 0
    t_base = gray / 255.0
    y, x = np.ogrid[:h, :w]
    
    frames = []
    for f in range(n_frames):
        phase = f / n_frames
        
        # Paleta Modernity de altíssimo contraste: violeta-vinho escuro (#1a0312) -> cromo rubi cristalino (#cf1538)
        r = 26.0 + t_base * 205.0
        g = 4.0 + (t_base ** 1.8) * 78.0
        b = 18.0 + (t_base ** 1.6) * 70.0
        
        # Glint de navalha deslizante
        glint_pos = (phase * (w + h)) - 2.0
        diag = (x + y) * 0.5
        glint = np.exp(-((diag - glint_pos * 0.5) / 1.0)**2) * (t_base > 0.6)
        
        # Cintilação estelar no vértice noroeste
        sparkle = 0.0
        if 12 <= f <= 16:
            sp_dist = np.sqrt((x - 4.0)**2 + (y - 4.0)**2)
            sparkle = np.exp(-(sp_dist / 0.85)**2) * math.sin((f - 12) / 4.0 * math.pi)
            
        r += glint * 105.0 + sparkle * 140.0
        g += glint * 90.0 + sparkle * 130.0
        b += glint * 95.0 + sparkle * 140.0
        
        frame = np.zeros((h, w, 4), dtype=np.uint8)
        frame[:, :, 0] = np.where(alpha, np.clip(r, 0, 255), 0)
        frame[:, :, 1] = np.where(alpha, np.clip(g, 0, 255), 0)
        frame[:, :, 2] = np.where(alpha, np.clip(b, 0, 255), 0)
        frame[:, :, 3] = np.where(alpha, 255, 0)
        frames.append(frame)
    return frames

# =========================================================================
# 2. CHAOS MATTER (MATÉRIA DO CAOS) CANDIDATES
# =========================================================================

# Opção 1: Fenda Dimensional & Vácuo Cósmico Instável (Chaos Vortex / Dimensional Fissure)
def render_chaos_c1(template, n_frames=30):
    h, w = template.shape[:2]
    gray = template[:, :, 0]
    alpha = template[:, :, 3] > 0
    t_base = gray / 255.0
    y, x = np.ogrid[:h, :w]
    
    # Fenda diagonal irregular
    fissure_line = (y - 0.75 * x - 1.5)
    fissure_shape = np.exp(-(fissure_line / 1.2)**2)
    
    frames = []
    for f in range(n_frames):
        tau = 2 * math.pi * (f / n_frames)
        
        # Vácuo negro abissal profundo (#080410 a `#1e0e30)
        r = 8.0 + t_base * 28.0
        g = 4.0 + t_base * 14.0
        b = 16.0 + t_base * 48.0
        
        # Pulso orgânico da fenda
        pulse = np.sin(tau) * 0.35 + 0.65
        noise = np.sin(x * 2.8 + tau * 2.0) * np.cos(y * 2.8 - tau) * 0.25
        active_fissure = np.clip(fissure_shape * (pulse + noise), 0, 1) * (t_base > 0.12)
        
        # Aura violeta neon / magenta da fenda
        r += active_fissure * 185.0
        g += active_fissure * 20.0
        b += active_fissure * 220.0
        
        # Núcleo branco estático no centro do rasgo dimensional
        core = np.clip(active_fissure - 0.58, 0, 1) * 2.6
        r += core * 160.0
        g += core * 155.0
        b += core * 180.0
        
        # Chanfros metálicos recebem aura púrpura tênue
        bevel = (t_base > 0.7)
        r += bevel * 22.0
        g += bevel * 6.0
        b += bevel * 38.0
        
        frame = np.zeros((h, w, 4), dtype=np.uint8)
        frame[:, :, 0] = np.where(alpha, np.clip(r, 0, 255), 0)
        frame[:, :, 1] = np.where(alpha, np.clip(g, 0, 255), 0)
        frame[:, :, 2] = np.where(alpha, np.clip(b, 0, 255), 0)
        frame[:, :, 3] = np.where(alpha, 255, 0)
        frames.append(frame)
    return frames

# Opção 2: Descargas Elétricas do Caos Dracônico (Chaos Dragon Sparking Arcs)
def render_chaos_c2(template, n_frames=30):
    h, w = template.shape[:2]
    gray = template[:, :, 0]
    alpha = template[:, :, 3] > 0
    t_base = gray / 255.0
    y, x = np.ogrid[:h, :w]
    
    frames = []
    for f in range(n_frames):
        tau = 2 * math.pi * (f / n_frames)
        
        # Ônix negro facetado estilo Chaos Shard (#100b16 a #2a1b38)
        r = 14.0 + t_base * 36.0
        g = 10.0 + t_base * 24.0
        b = 22.0 + t_base * 52.0
        
        # Arcos elétricos caóticos orgânicos
        arc_grid = np.zeros((h, w), dtype=np.float32)
        arc_seed = (f // 3) * 19 + 7
        rng = np.random.RandomState(arc_seed)
        
        # 2 arcos elétricos ramificados
        for arc_i in range(2):
            y_pts = rng.randint(2, h-2, size=3)
            x_pts = rng.randint(2, w-2, size=3)
            for i in range(len(y_pts)-1):
                y0, y1 = y_pts[i], y_pts[i+1]
                x0, x1 = x_pts[i], x_pts[i+1]
                steps = max(abs(y1 - y0), abs(x1 - x0), 1) * 2
                for s in range(steps + 1):
                    t = s / steps
                    yy = int(round(y0 + t * (y1 - y0)))
                    xx = int(round(x0 + t * (x1 - x0)))
                    if 0 <= yy < h and 0 <= xx < w and alpha[yy, xx]:
                        arc_grid[yy, xx] = 1.0
                        for dy, dx in [(-1,0),(1,0),(0,-1),(0,1)]:
                            ny, nx = yy + dy, xx + dx
                            if 0 <= ny < h and 0 <= nx < w and alpha[ny, nx]:
                                arc_grid[ny, nx] = max(arc_grid[ny, nx], 0.4)
                                
        # Centelhas elétricas estocásticas piscantes
        spark_rng = np.random.RandomState(f * 37 + 11)
        sparks = np.zeros((h, w), dtype=np.float32)
        for _ in range(4):
            sy, sx = spark_rng.randint(2, h-2), spark_rng.randint(2, w-2)
            if alpha[sy, sx] and t_base[sy, sx] > 0.3:
                sparks[sy, sx] = 1.0
                
        # Mistura de ciano elétrico (#00f0ff) e violeta dracônico (#a018ff)
        cyan_weight = np.sin(x * 0.7 + tau) * 0.5 + 0.5
        arc_mask = arc_grid * (t_base > 0.15)
        
        r += arc_mask * (cyan_weight * 10.0 + (1 - cyan_weight) * 185.0) + sparks * 230.0
        g += arc_mask * (cyan_weight * 235.0 + (1 - cyan_weight) * 30.0) + sparks * 240.0
        b += arc_mask * (cyan_weight * 255.0 + (1 - cyan_weight) * 245.0) + sparks * 255.0
        
        frame = np.zeros((h, w, 4), dtype=np.uint8)
        frame[:, :, 0] = np.where(alpha, np.clip(r, 0, 255), 0)
        frame[:, :, 1] = np.where(alpha, np.clip(g, 0, 255), 0)
        frame[:, :, 2] = np.where(alpha, np.clip(b, 0, 255), 0)
        frame[:, :, 3] = np.where(alpha, 255, 0)
        frames.append(frame)
    return frames

# Opção 3: Matéria Entrópica Primordial (Aberração Cromática & Singularidade)
def render_chaos_c3(template, n_frames=30):
    h, w = template.shape[:2]
    gray = template[:, :, 0]
    alpha = template[:, :, 3] > 0
    t_base = gray / 255.0
    y, x = np.ogrid[:h, :w]
    
    if np.sum(alpha) > 0:
        cy = np.sum(np.where(alpha, y, 0)) / np.sum(alpha)
        cx = np.sum(np.where(alpha, x, 0)) / np.sum(alpha)
    else:
        cy, cx = h / 2.0, w / 2.0
    dist = np.sqrt((x - cx)**2 + (y - cy)**2)
    
    frames = []
    for f in range(n_frames):
        tau = 2 * math.pi * (f / n_frames)
        
        # Deslocamento óptico RGB Split
        shift = np.sin(tau) * 0.75
        
        # Canal R: puxado para magenta
        r_base = t_base + shift * 0.12
        r = 10.0 + np.clip(r_base, 0, 1) * 78.0
        
        # Canal G: reduzido (corpo roxo profundo)
        g = 5.0 + t_base * 18.0
        
        # Canal B: puxado para ciano
        b_base = t_base - shift * 0.12
        b = 22.0 + np.clip(b_base, 0, 1) * 110.0
        
        # Singularidade: pulso de lente gravitacional no centro
        sing_pulse = np.sin(tau * 2.0) * 0.5 + 0.5
        sing_radius = 4.0 + sing_pulse * 1.5
        horizon = np.exp(-((dist - sing_radius) / 1.0)**2) * (t_base > 0.2)
        
        r += horizon * 175.0
        g += horizon * 15.0
        b += horizon * 215.0
        
        # Aberração nos chanfros
        edge_c = (x <= cx) & (t_base > 0.6)
        edge_m = (x > cx) & (t_base > 0.6)
        
        r += edge_m * 85.0
        b += edge_c * 95.0
        g += (edge_c | edge_m) * 18.0
        
        frame = np.zeros((h, w, 4), dtype=np.uint8)
        frame[:, :, 0] = np.where(alpha, np.clip(r, 0, 255), 0)
        frame[:, :, 1] = np.where(alpha, np.clip(g, 0, 255), 0)
        frame[:, :, 2] = np.where(alpha, np.clip(b, 0, 255), 0)
        frame[:, :, 3] = np.where(alpha, 255, 0)
        frames.append(frame)
    return frames

# =========================================================================
# GERAÇÃO DAS FOLHAS DE COMPARAÇÃO
# =========================================================================

def create_jei_slot(inner_im):
    slot = Image.new("RGBA", (140, 140), (139, 139, 139, 255))
    draw = ImageDraw.Draw(slot)
    draw.rectangle([0, 0, 139, 3], fill=(55, 55, 55, 255))
    draw.rectangle([0, 0, 3, 139], fill=(55, 55, 55, 255))
    draw.rectangle([0, 136, 139, 139], fill=(255, 255, 255, 255))
    draw.rectangle([136, 0, 139, 139], fill=(255, 255, 255, 255))
    slot.paste(inner_im, (6, 6), inner_im)
    return slot

def build_comparison_sheet(title, old_frames, c1_frames, c2_frames, c3_frames, out_name):
    total_w = 4 * 180 + 5 * 20
    total_h = 280
    sheet = Image.new("RGBA", (total_w, total_h), (22, 27, 34, 255))
    draw = ImageDraw.Draw(sheet)
    
    draw.text((20, 14), title, fill=(240, 246, 252, 255))
    
    candidates = [
        ("ATUAL", old_frames[0] if old_frames else None, (248, 81, 73, 255)),
        ("OPCAO 1", c1_frames[0], (63, 185, 80, 255)),
        ("OPCAO 2", c2_frames[0], (88, 166, 255, 255)),
        ("OPCAO 3", c3_frames[0], (210, 168, 255, 255)),
    ]
    
    for i, (label, arr, tag_color) in enumerate(candidates):
        x_offset = 20 + i * (180 + 20)
        y_offset = 45
        draw.rectangle([x_offset, y_offset, x_offset + 180, y_offset + 220], outline=(48, 54, 61, 255), width=1)
        draw.text((x_offset + 12, y_offset + 10), label, fill=tag_color)
        
        if arr is not None:
            im = Image.fromarray(arr.astype(np.uint8), mode="RGBA")
            im_scaled = im.resize((128, 128), resample=Image.NEAREST)
            slot = create_jei_slot(im_scaled)
            sheet.paste(slot, (x_offset + 20, y_offset + 35), slot)
        else:
            draw.text((x_offset + 30, y_offset + 80), "Sem Imagem", fill=(139, 148, 158, 255))
            
    p1 = ARTIFACT_DIR / out_name
    p2 = DOCS_DIR / out_name
    sheet.save(p1)
    sheet.save(p2)
    print(f"Salvo comparativo estatico: {p1}")

def build_row_animated_gif(title, items, out_name):
    n_items = len(items)
    n_frames = len(items[0][1])
    
    total_w = n_items * 180 + (n_items + 1) * 20
    total_h = 280
    
    gif_frames = []
    for f in range(n_frames):
        sheet = Image.new("RGBA", (total_w, total_h), (22, 27, 34, 255))
        draw = ImageDraw.Draw(sheet)
        draw.text((20, 14), title, fill=(240, 246, 252, 255))
        
        for i, (label, frames, tag_color) in enumerate(items):
            x_offset = 20 + i * (180 + 20)
            y_offset = 45
            draw.rectangle([x_offset, y_offset, x_offset + 180, y_offset + 220], outline=(48, 54, 61, 255), width=1)
            draw.text((x_offset + 12, y_offset + 10), label, fill=tag_color)
            
            arr = frames[f % len(frames)]
            im = Image.fromarray(arr.astype(np.uint8), mode="RGBA")
            im_scaled = im.resize((128, 128), resample=Image.NEAREST)
            slot = create_jei_slot(im_scaled)
            sheet.paste(slot, (x_offset + 20, y_offset + 35), slot)
            
        gif_frames.append(np.array(sheet))
        
    p1 = ARTIFACT_DIR / out_name
    p2 = DOCS_DIR / out_name
    save_gif_file(gif_frames, p1, duration=66)
    save_gif_file(gif_frames, p2, duration=66)
    print(f"Salvo GIF animado lado a lado: {p1}")

# Executa geração
old_dm_i = extract_old_frames("src/main/resources/assets/gtceu/textures/item/material_sets/gtna_dragon_metal/ingot.png")
old_dm_b = extract_old_frames("src/main/resources/assets/gtceu/textures/block/material_sets/gtna_dragon_metal/block.png")

old_cm_i = extract_old_frames("src/main/resources/assets/gtceu/textures/item/material_sets/gtna_chaos_matter/ingot.png")
cm_ov_p = REPO_ROOT / "src/main/resources/assets/gtceu/textures/item/material_sets/gtna_chaos_matter/ingot_overlay.png"
if cm_ov_p.exists() and old_cm_i:
    ov_im = Image.open(cm_ov_p).convert("RGBA")
    b_im = Image.fromarray(old_cm_i[0])
    comp = Image.alpha_composite(b_im, ov_im)
    old_cm_i = [np.array(comp)] * 30

old_cm_b = extract_old_frames("src/main/resources/assets/gtceu/textures/block/material_sets/gtna_chaos_matter/block.png")

# Dragonmetal
dm_i_c1 = render_dragonmetal_c1(T_MOD_INGOT)
dm_i_c2 = render_dragonmetal_c2(T_MOD_INGOT)
dm_i_c3 = render_dragonmetal_c3(T_MOD_INGOT)

dm_b_c1 = render_dragonmetal_c1(T_MOD_BLOCK)
dm_b_c2 = render_dragonmetal_c2(T_MOD_BLOCK)
dm_b_c3 = render_dragonmetal_c3(T_MOD_BLOCK)

dm_p_c1 = render_dragonmetal_c1(T_MOD_PLATE)
dm_p_c2 = render_dragonmetal_c2(T_MOD_PLATE)
dm_p_c3 = render_dragonmetal_c3(T_MOD_PLATE)

dm_g_c1 = render_dragonmetal_c1(T_MOD_GEAR)
dm_g_c2 = render_dragonmetal_c2(T_MOD_GEAR)
dm_g_c3 = render_dragonmetal_c3(T_MOD_GEAR)

# Chaos Matter
cm_i_c1 = render_chaos_c1(T_MOD_INGOT)
cm_i_c2 = render_chaos_c2(T_MOD_INGOT)
cm_i_c3 = render_chaos_c3(T_MOD_INGOT)

cm_b_c1 = render_chaos_c1(T_MOD_BLOCK)
cm_b_c2 = render_chaos_c2(T_MOD_BLOCK)
cm_b_c3 = render_chaos_c3(T_MOD_BLOCK)

cm_p_c1 = render_chaos_c1(T_MOD_PLATE)
cm_p_c2 = render_chaos_c2(T_MOD_PLATE)
cm_p_c3 = render_chaos_c3(T_MOD_PLATE)

cm_g_c1 = render_chaos_c1(T_MOD_GEAR)
cm_g_c2 = render_chaos_c2(T_MOD_GEAR)
cm_g_c3 = render_chaos_c3(T_MOD_GEAR)

# Salva GIFs individuais
assets_to_save = [
    ("dragonmetal_c1_ingot.gif", dm_i_c1),
    ("dragonmetal_c2_ingot.gif", dm_i_c2),
    ("dragonmetal_c3_ingot.gif", dm_i_c3),
    ("dragonmetal_c1_block.gif", dm_b_c1),
    ("dragonmetal_c2_block.gif", dm_b_c2),
    ("dragonmetal_c3_block.gif", dm_b_c3),
    ("dragonmetal_c1_plate.gif", dm_p_c1),
    ("dragonmetal_c2_plate.gif", dm_p_c2),
    ("dragonmetal_c3_plate.gif", dm_p_c3),
    ("dragonmetal_c1_gear.gif", dm_g_c1),
    ("dragonmetal_c2_gear.gif", dm_g_c2),
    ("dragonmetal_c3_gear.gif", dm_g_c3),

    ("chaos_c1_ingot.gif", cm_i_c1),
    ("chaos_c2_ingot.gif", cm_i_c2),
    ("chaos_c3_ingot.gif", cm_i_c3),
    ("chaos_c1_block.gif", cm_b_c1),
    ("chaos_c2_block.gif", cm_b_c2),
    ("chaos_c3_block.gif", cm_b_c3),
    ("chaos_c1_plate.gif", cm_p_c1),
    ("chaos_c2_plate.gif", cm_p_c2),
    ("chaos_c3_plate.gif", cm_p_c3),
    ("chaos_c1_gear.gif", cm_g_c1),
    ("chaos_c2_gear.gif", cm_g_c2),
    ("chaos_c3_gear.gif", cm_g_c3),
]

for name, frames in assets_to_save:
    save_gif_file(frames, ARTIFACT_DIR / name)
    save_gif_file(frames, DOCS_DIR / name)

# Sheets estáticas
build_comparison_sheet("Dragonmetal (Ingot) - Comparativo Visual", old_dm_i, dm_i_c1, dm_i_c2, dm_i_c3, "dragonmetal_ingot_sheet.png")
build_comparison_sheet("Dragonmetal (Block) - Comparativo Visual", old_dm_b, dm_b_c1, dm_b_c2, dm_b_c3, "dragonmetal_block_sheet.png")
build_comparison_sheet("Chaos Matter (Ingot) - Comparativo Visual", old_cm_i, cm_i_c1, cm_i_c2, cm_i_c3, "chaos_ingot_sheet.png")
build_comparison_sheet("Chaos Matter (Block) - Comparativo Visual", old_cm_b, cm_b_c1, cm_b_c2, cm_b_c3, "chaos_block_sheet.png")

# Rows animadas
build_row_animated_gif("Dragonmetal (Ingot) - Animacoes Lado a Lado", [
    ("ATUAL (ALARANJADO)", old_dm_i, (248, 81, 73, 255)),
    ("OPCAO 1 (ESCAMAS)", dm_i_c1, (63, 185, 80, 255)),
    ("OPCAO 2 (CORACAO)", dm_i_c2, (88, 166, 255, 255)),
    ("OPCAO 3 (CROMO)", dm_i_c3, (210, 168, 255, 255)),
], "dragonmetal_ingot_anim_row.gif")

build_row_animated_gif("Dragonmetal (Block) - Animacoes Lado a Lado", [
    ("ATUAL", old_dm_b, (248, 81, 73, 255)),
    ("OPCAO 1 (ESCAMAS)", dm_b_c1, (63, 185, 80, 255)),
    ("OPCAO 2 (CORACAO)", dm_b_c2, (88, 166, 255, 255)),
    ("OPCAO 3 (CROMO)", dm_b_c3, (210, 168, 255, 255)),
], "dragonmetal_block_anim_row.gif")

build_row_animated_gif("Chaos Matter (Ingot) - Animacoes Lado a Lado", [
    ("ATUAL (BLOB)", old_cm_i, (248, 81, 73, 255)),
    ("OPCAO 1 (FENDA)", cm_i_c1, (63, 185, 80, 255)),
    ("OPCAO 2 (RELAMPAGOS)", cm_i_c2, (88, 166, 255, 255)),
    ("OPCAO 3 (ABERRACAO)", cm_i_c3, (210, 168, 255, 255)),
], "chaos_ingot_anim_row.gif")

build_row_animated_gif("Chaos Matter (Block) - Animacoes Lado a Lado", [
    ("ATUAL (PRETO PLANO)", old_cm_b, (248, 81, 73, 255)),
    ("OPCAO 1 (FENDA)", cm_b_c1, (63, 185, 80, 255)),
    ("OPCAO 2 (RELAMPAGOS)", cm_b_c2, (88, 166, 255, 255)),
    ("OPCAO 3 (ABERRACAO)", cm_b_c3, (210, 168, 255, 255)),
], "chaos_block_anim_row.gif")

# =========================================================================
# GERAÇÃO DO SHOWCASE HTML COMPLETO
# =========================================================================
def b64_gif(frames):
    return f"data:image/gif;base64,{save_gif_base64(frames)}"

showcase_data = {
    "dragonmetal": {
        "title": "Dragonmetal (Dragonblood Metal)",
        "formula": "۞",
        "desc": "Metal dracônico lendário da cadeia Godforge. Utilizado em fusões avançadas com Rhugnor para forjar Hypogen.",
        "options": [
            {
                "id": 1,
                "name": "Opção 1: Escama Dracônica Ancestral & Veias de Fogo",
                "tag": "WYRM SCALES & EMBER VEINS",
                "color": "#e02844",
                "desc": "Sombreamento profundo carmesim-obsidiana (#22040e) com escamas dracônicas lustrosas, veias arteriais e chanfros com glint de ouro nobre (#ffe070).",
                "ingot": b64_gif(dm_i_c1),
                "block": b64_gif(dm_b_c1),
                "plate": b64_gif(dm_p_c1),
                "gear": b64_gif(dm_g_c1),
                "swatches": ["#22040e", "#5e0a1b", "#941028", "#dc223e", "#ffe070"]
            },
            {
                "id": 2,
                "name": "Opção 2: Coração Dracônico em Fusão & Sel-out Obsidiana",
                "tag": "MOLTEN HEART & LUB-DUB PULSE",
                "color": "#ff3820",
                "desc": "Bordas em corte de obsidiana fria (#14020a) e núcleo com duplo batimento cardíaco dracônico (lub-dub) que incandesce até o branco-dourado nos picos de sístole.",
                "ingot": b64_gif(dm_i_c2),
                "block": b64_gif(dm_b_c2),
                "plate": b64_gif(dm_p_c2),
                "gear": b64_gif(dm_g_c2),
                "swatches": ["#14020a", "#4a0614", "#a2122b", "#ff4d20", "#ffea80"]
            },
            {
                "id": 3,
                "name": "Opção 3: Aço Dracônico Modernity de Alto Contraste",
                "tag": "RED CHROME MODERNITY",
                "color": "#cf1538",
                "desc": "Estilo Modernity afiado com transição violeta-vinho (#1a0312) para cromo rubi puro (#cf1538), feixe de luz afiado varrendo diagonalmente e cintilação estelar.",
                "ingot": b64_gif(dm_i_c3),
                "block": b64_gif(dm_b_c3),
                "plate": b64_gif(dm_p_c3),
                "gear": b64_gif(dm_g_c3),
                "swatches": ["#1a0312", "#60081d", "#cf1538", "#ff6b85", "#fff0f4"]
            }
        ]
    },
    "chaos": {
        "title": "Chaos Matter (Matéria do Caos)",
        "formula": "✦Ch✦",
        "desc": "Material supremo de entropia cósmica e quebra dimensional do endgame da cadeia Godforge.",
        "options": [
            {
                "id": 1,
                "name": "Opção 1: Fenda Dimensional & Vácuo Cósmico Instável",
                "tag": "DIMENSIONAL FISSURE & VORTEX",
                "color": "#c822e0",
                "desc": "Vácuo negro ultra-profundo (#080410) rasgado por uma fenda dimensional de plasma violeta/magenta neon com núcleo estático branco que pulsa organicamente.",
                "ingot": b64_gif(cm_i_c1),
                "block": b64_gif(cm_b_c1),
                "plate": b64_gif(cm_p_c1),
                "gear": b64_gif(cm_g_c1),
                "swatches": ["#080410", "#1e0e30", "#7c129c", "#ea20d2", "#ffffff"]
            },
            {
                "id": 2,
                "name": "Opção 2: Descargas Elétricas do Caos Dracônico (Chaos Shard)",
                "tag": "CHAOS SHARD SPARKING ARCS",
                "color": "#00f0ff",
                "desc": "Inspirado no Chaos Shard e Chaos Guardian do Draconic Evolution. Metal ônix facetado com arcos elétricos caóticos estalando em ciano elétrico (#00f0ff) e violeta (#a018ff).",
                "ingot": b64_gif(cm_i_c2),
                "block": b64_gif(cm_b_c2),
                "plate": b64_gif(cm_p_c2),
                "gear": b64_gif(cm_g_c2),
                "swatches": ["#100b16", "#2a1b38", "#8c14e0", "#00f0ff", "#ffffff"]
            },
            {
                "id": 3,
                "name": "Opção 3: Matéria Entrópica Primordial (Aberração Cromática)",
                "tag": "CHROMATIC ABERRATION & SINGULARITY",
                "color": "#ff2adb",
                "desc": "Singularidade com efeito óptico de RGB Split (aberração cromática ciano/magenta) nos chanfros e horizonte de eventos pulsante no centro que distorce o espaço.",
                "ingot": b64_gif(cm_i_c3),
                "block": b64_gif(cm_b_c3),
                "plate": b64_gif(cm_p_c3),
                "gear": b64_gif(cm_g_c3),
                "swatches": ["#0a0514", "#221236", "#00d0f0", "#ff2adb", "#ffffff"]
            }
        ]
    }
}

html_out = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>GTNA — Redesign de Texturas: Dragonmetal & Chaos Matter</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: #0d1117;
      color: #c9d1d9;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      padding: 24px;
      line-height: 1.5;
    }}
    .container {{ max-width: 1100px; margin: 0 auto; }}
    header {{
      text-align: center;
      margin-bottom: 28px;
      padding: 24px;
      background: #161b22;
      border: 1px solid #30363d;
      border-radius: 12px;
    }}
    h1 {{ color: #f0f6fc; font-size: 26px; margin-bottom: 8px; }}
    .subtitle {{ color: #8b949e; font-size: 14px; }}
    .tab-bar {{
      display: flex;
      gap: 12px;
      justify-content: center;
      margin: 20px 0;
    }}
    .tab-btn {{
      background: #21262d;
      color: #c9d1d9;
      border: 1px solid #30363d;
      padding: 10px 24px;
      border-radius: 8px;
      font-size: 15px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s;
    }}
    .tab-btn.active {{
      background: #1f6feb;
      color: #ffffff;
      border-color: #388bfd;
      box-shadow: 0 0 12px rgba(31, 111, 235, 0.4);
    }}
    .material-pane {{ display: none; }}
    .material-pane.active {{ display: block; }}
    .mat-header {{
      background: #161b22;
      border: 1px solid #30363d;
      border-radius: 10px;
      padding: 18px 22px;
      margin-bottom: 24px;
    }}
    .mat-title {{ font-size: 20px; font-weight: 700; color: #f0f6fc; }}
    .mat-formula {{ font-family: monospace; color: #58a6ff; font-size: 16px; margin-left: 8px; }}
    .mat-desc {{ color: #8b949e; font-size: 14px; margin-top: 6px; }}
    .cards-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
      gap: 20px;
      margin-bottom: 30px;
    }}
    .card {{
      background: #161b22;
      border: 1px solid #30363d;
      border-radius: 10px;
      padding: 18px;
      display: flex;
      flex-direction: column;
      gap: 14px;
      transition: transform 0.2s, border-color 0.2s;
    }}
    .card:hover {{
      border-color: #58a6ff;
      transform: translateY(-2px);
    }}
    .card-badge {{
      display: inline-block;
      align-self: flex-start;
      padding: 3px 8px;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 0.5px;
    }}
    .card-title {{ font-size: 16px; font-weight: 600; color: #f0f6fc; }}
    .card-desc {{ font-size: 13px; color: #8b949e; flex-grow: 1; }}
    .sprites-row {{
      display: flex;
      gap: 12px;
      justify-content: center;
      background: #0d1117;
      padding: 14px;
      border-radius: 8px;
      border: 1px solid #21262d;
    }}
    .sprite-slot {{
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 6px;
    }}
    .sprite-frame {{
      width: 64px;
      height: 64px;
      background: #8b8b8b;
      border-top: 2px solid #373737;
      border-left: 2px solid #373737;
      border-bottom: 2px solid #ffffff;
      border-right: 2px solid #ffffff;
      display: flex;
      align-items: center;
      justify-content: center;
    }}
    .sprite-frame img {{
      width: 56px;
      height: 56px;
      image-rendering: pixelated;
    }}
    .sprite-label {{ font-size: 11px; color: #8b949e; text-transform: uppercase; }}
    .swatches-row {{
      display: flex;
      gap: 6px;
      align-items: center;
    }}
    .swatch {{
      width: 22px;
      height: 22px;
      border-radius: 4px;
      border: 1px solid rgba(255,255,255,0.15);
    }}
    .choose-btn {{
      background: #238636;
      color: #ffffff;
      border: 1px solid #2ea043;
      padding: 8px 16px;
      border-radius: 6px;
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      text-align: center;
      transition: background 0.2s;
    }}
    .choose-btn:hover {{ background: #2ea043; }}
  </style>
  <script>
    function setTab(matKey) {{
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.material-pane').forEach(p => p.classList.remove('active'));
      document.getElementById('tab-' + matKey).classList.add('active');
      document.getElementById('pane-' + matKey).classList.add('active');
    }}
    function copyDecision(text) {{
      navigator.clipboard.writeText(text);
      alert('Opção copiada! Cole no chat:\\n\\n' + text);
    }}
  </script>
</head>
<body>
  <div class="container">
    <header>
      <h1>Redesign de Texturas — GTNA</h1>
      <p class="subtitle">Avaliação Visual e Escolha dos Novos Materiais: Dragonmetal & Chaos Matter</p>
      <div class="tab-bar">
        <button id="tab-dragonmetal" class="tab-btn active" onclick="setTab('dragonmetal')">Dragonmetal (۞)</button>
        <button id="tab-chaos" class="tab-btn" onclick="setTab('chaos')">Chaos Matter (✦Ch✦)</button>
      </div>
    </header>
"""

for mat_key, mat_info in showcase_data.items():
    is_active = "active" if mat_key == "dragonmetal" else ""
    html_out += f"""
    <div id="pane-{mat_key}" class="material-pane {is_active}">
      <div class="mat-header">
        <span class="mat-title">{mat_info['title']}</span>
        <span class="mat-formula">{mat_info['formula']}</span>
        <p class="mat-desc">{mat_info['desc']}</p>
      </div>
      <div class="cards-grid">
    """
    for opt in mat_info["options"]:
        swatches_html = "".join([f'<div class="swatch" style="background:{s};" title="{s}"></div>' for s in opt["swatches"]])
        btn_copy_text = f"Aprovo a {opt['name']} para o {mat_info['title']}"
        html_out += f"""
        <div class="card">
          <div class="card-badge" style="background:{opt['color']}22; color:{opt['color']}; border:1px solid {opt['color']}55;">
            {opt['tag']}
          </div>
          <div class="card-title">{opt['name']}</div>
          <div class="card-desc">{opt['desc']}</div>
          <div class="sprites-row">
            <div class="sprite-slot">
              <div class="sprite-frame"><img src="{opt['ingot']}" alt="Ingot"></div>
              <span class="sprite-label">Ingot</span>
            </div>
            <div class="sprite-slot">
              <div class="sprite-frame"><img src="{opt['block']}" alt="Block"></div>
              <span class="sprite-label">Block</span>
            </div>
            <div class="sprite-slot">
              <div class="sprite-frame"><img src="{opt['plate']}" alt="Plate"></div>
              <span class="sprite-label">Plate</span>
            </div>
            <div class="sprite-slot">
              <div class="sprite-frame"><img src="{opt['gear']}" alt="Gear"></div>
              <span class="sprite-label">Gear</span>
            </div>
          </div>
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <div class="swatches-row">{swatches_html}</div>
            <button class="choose-btn" onclick="copyDecision('{btn_copy_text}')">Escolher</button>
          </div>
        </div>
        """
    html_out += """
      </div>
    </div>
    """

html_out += """
  </div>
</body>
</html>
"""

(ARTIFACT_DIR / "texture_redesign_showcase.html").write_text(html_out)
(DOCS_DIR / "texture_redesign_showcase.html").write_text(html_out)
print(f"Salvo showcase interativo HTML em {ARTIFACT_DIR / 'texture_redesign_showcase.html'}")

