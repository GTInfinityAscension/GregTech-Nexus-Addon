#!/usr/bin/env python3
"""
GTNA Texture Fine-Tuning Showcase - Grupo 1
Materiais: Dragonmetal, Mellion, Nitinol 60, Superconductor UIV Base
"""

import os
import io
import math
import json
import base64
from pathlib import Path
import numpy as np
from PIL import Image

REPO_ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = Path("/tmp/fine_tuning_showcase_g1")
OUT_DIR.mkdir(parents=True, exist_ok=True)

ARTIFACT_DIR = Path("/home/raishxn/.gemini/antigravity/brain/bd675c79-98ee-419c-9725-13ae9cf612a0")
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

# Templates base
MOD_INGOT_PATH = Path("/home/raishxn/Downloads/Modernity-GTNH-2026-09-07/assets/gregtech/textures/items/materialicons/CUSTOM/WhiteDwarfMatter/ingot.png")
GTCEU_SHINY_INGOT = Path("/home/raishxn/MineProjects/GTCEu-7.5.3/src/main/resources/assets/gtceu/textures/item/material_sets/shiny/ingot.png")
GTCEU_DULL_INGOT = Path("/home/raishxn/MineProjects/GTCEu-7.5.3/src/main/resources/assets/gtceu/textures/item/material_sets/dull/ingot.png")

def load_template(path):
    im = Image.open(path).convert("RGBA")
    arr = np.array(im, dtype=np.float32)
    h, w = arr.shape[:2]
    if h > w:
        arr = arr[:w, :, :]
    return arr

TEMPLATE_MOD = load_template(MOD_INGOT_PATH)
TEMPLATE_SHINY = load_template(GTCEU_SHINY_INGOT)
TEMPLATE_DULL = load_template(GTCEU_DULL_INGOT)

def save_gif_base64(frames, duration=66):
    """Gera GIF transparente animado em base64 com paleta indexada estrita."""
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

    buf = io.BytesIO()
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

def extract_old_texture_frames(rel_path, num_frames=30):
    full_path = REPO_ROOT / rel_path
    if not full_path.exists():
        return None
    im = Image.open(full_path).convert("RGBA")
    w, h = im.size
    frames_count = h // w
    arr = np.array(im, dtype=np.uint8)
    frames = []
    for f in range(min(num_frames, frames_count)):
        sub = arr[f*w:(f+1)*w, :w, :]
        frames.append(sub)
    if not frames:
        frames = [arr[:w, :w, :]]
    return frames

def analyze_palette(frames):
    f0 = frames[0]
    alpha = f0[:, :, 3] > 0
    rgb = f0[alpha][:, :3]
    unique = np.unique(rgb, axis=0)
    lum = 0.299 * rgb[:, 0] + 0.587 * rgb[:, 1] + 0.114 * rgb[:, 2]
    min_l, max_l = float(lum.min()), float(lum.max())
    
    # Amostras representativas para swatches (5 cores)
    sorted_idx = np.argsort(lum)
    step = len(sorted_idx) // 5
    swatches = []
    for i in range(5):
        idx = sorted_idx[min(i * step, len(sorted_idx) - 1)]
        c = rgb[idx]
        swatches.append(f"#{int(c[0]):02x}{int(c[1]):02x}{int(c[2]):02x}")
        
    return {
        "unique_colors": len(unique),
        "min_lum": round(min_l, 1),
        "max_lum": round(max_l, 1),
        "contrast": round(max_l - min_l, 1),
        "swatches": swatches
    }

# =========================================================================
# 1. DRAGONMETAL (DRAGONBLOOD METAL)
# =========================================================================
def render_dragonmetal_c1(n_frames=30):
    """Candidato 1: Draconic Scale Iridescence & Ember Pulse (Escama Dracônica Iridescente)"""
    base = TEMPLATE_MOD.copy()
    h, w = base.shape[:2]
    gray = base[:, :, 0]
    alpha = base[:, :, 3] > 0
    t_base = gray / 255.0
    y, x = np.ogrid[:h, :w]
    
    frames = []
    for f in range(n_frames):
        phase = f / n_frames
        tau = 2 * math.pi * phase
        
        # Paleta com Hue Shift dracônico:
        # Sombra: granada profunda e sangue seco (#320814)
        # Meio: rubi dracônico vivo (#b51832)
        # Destaque: âmbar fogo (#ff9e22) -> ouro incandescente (#fff2a8)
        r = 50.0 + t_base * 145.0
        g = 8.0 + (t_base ** 1.8) * 60.0
        b = 18.0 + (t_base ** 1.4) * 35.0
        
        # Onda de pulso de brasa dracônica que corre na diagonal top-left para bottom-right
        wave = np.sin((x + y) * 0.45 - tau) * 0.5 + 0.5
        ember = (wave ** 3.0) * (t_base > 0.4)
        
        # Chanfros superiores recebem glint dourado de escama
        bevel_mask = (y <= x + 2) & (t_base > 0.6)
        scale_glint = np.sin(x * 0.8 - tau) * 0.5 + 0.5
        scale_boost = (scale_glint ** 4.0) * bevel_mask
        
        r += ember * 60.0 + scale_boost * 90.0
        g += ember * 35.0 + scale_boost * 80.0
        b += ember * 5.0 + scale_boost * 30.0
        
        frame = np.zeros((h, w, 4), dtype=np.uint8)
        frame[:, :, 0] = np.where(alpha, np.clip(r, 0, 255), 0)
        frame[:, :, 1] = np.where(alpha, np.clip(g, 0, 255), 0)
        frame[:, :, 2] = np.where(alpha, np.clip(b, 0, 255), 0)
        frame[:, :, 3] = np.where(alpha, 255, 0)
        frames.append(frame)
    return frames

def render_dragonmetal_c2(n_frames=30):
    """Candidato 2: Molten Heart Core & Obsidian Sel-Out (Coração Dracônico com Sel-out Obsidiana)"""
    base = TEMPLATE_SHINY.copy()
    h, w = base.shape[:2]
    gray = base[:, :, 0]
    alpha = base[:, :, 3] > 0
    t_base = gray / 255.0
    y, x = np.ogrid[:h, :w]
    
    # Centro para pulso do coração
    cy, cx = 7.5, 7.5
    dist = np.sqrt((x - cx)**2 + (y - cy)**2)
    
    frames = []
    for f in range(n_frames):
        t = (f / n_frames) * 2 * math.pi
        # Duplo batimento cardíaco dracônico (lub-dub)
        pulse = np.maximum(0, np.sin(t))**3 + 0.55 * np.maximum(0, np.sin(t - 0.75))**3
        pulse = np.clip(pulse, 0, 1.2)
        
        # Sel-out obsidiana nas bordas inferiores e sombras
        r = 25.0 + t_base * 175.0
        g = 4.0 + (t_base ** 2.2) * 55.0
        b = 10.0 + (t_base ** 2.0) * 35.0
        
        # Núcleo de fusão
        core_weight = np.clip(1.0 - dist / 7.0, 0, 1) ** 1.5
        heat = pulse * core_weight * (t_base > 0.3)
        
        r += heat * 95.0
        g += heat * 65.0
        b += heat * 25.0
        
        # Picos de incandescência branca no clímax do batimento
        hot_peak = np.clip(heat - 0.65, 0, 1) * 140.0
        r += hot_peak * 0.95
        g += hot_peak * 0.90
        b += hot_peak * 0.70
        
        frame = np.zeros((h, w, 4), dtype=np.uint8)
        frame[:, :, 0] = np.where(alpha, np.clip(r, 0, 255), 0)
        frame[:, :, 1] = np.where(alpha, np.clip(g, 0, 255), 0)
        frame[:, :, 2] = np.where(alpha, np.clip(b, 0, 255), 0)
        frame[:, :, 3] = np.where(alpha, 255, 0)
        frames.append(frame)
    return frames

def render_dragonmetal_c3(n_frames=30):
    """Candidato 3: Pure Modernity High-Contrast Dragon Steel (Aço Dracônico Modernity)"""
    base = TEMPLATE_MOD.copy()
    h, w = base.shape[:2]
    gray = base[:, :, 0]
    alpha = base[:, :, 3] > 0
    t_base = gray / 255.0
    y, x = np.ogrid[:h, :w]
    
    frames = []
    for f in range(n_frames):
        phase = f / n_frames
        
        # Paleta Modernity de altíssimo contraste com sombreamento violeta-vinho e cromo vermelho
        r = 40.0 + t_base * 195.0
        g = 10.0 + (t_base ** 1.7) * 75.0
        b = 25.0 + (t_base ** 1.6) * 65.0
        
        # Glint chanfrado que desliza pela aresta noroeste
        glint_pos = (phase * 22.0) - 3.0
        diag = (x + y) * 0.5
        glint = np.exp(-((diag - glint_pos) / 1.1)**2) * (t_base > 0.65)
        
        # Cintilação estelar pontual no frame 15
        sparkle = 0.0
        if 13 <= f <= 16:
            sp_dist = np.sqrt((x - 4.0)**2 + (y - 4.0)**2)
            sparkle = np.exp(-(sp_dist / 0.9)**2) * math.sin((f - 13) / 3.0 * math.pi)
            
        r += glint * 90.0 + sparkle * 120.0
        g += glint * 75.0 + sparkle * 115.0
        b += glint * 75.0 + sparkle * 115.0
        
        frame = np.zeros((h, w, 4), dtype=np.uint8)
        frame[:, :, 0] = np.where(alpha, np.clip(r, 0, 255), 0)
        frame[:, :, 1] = np.where(alpha, np.clip(g, 0, 255), 0)
        frame[:, :, 2] = np.where(alpha, np.clip(b, 0, 255), 0)
        frame[:, :, 3] = np.where(alpha, 255, 0)
        frames.append(frame)
    return frames

# =========================================================================
# 2. MELLION (GODFORGE UXV CATALYST METAL)
# =========================================================================
def render_mellion_c1(n_frames=30):
    """Candidato 1: Imperial Rose-Gold & Velvet Crimson (Carmesim Imperial com Ouro Rosado)"""
    base = TEMPLATE_MOD.copy()
    h, w = base.shape[:2]
    gray = base[:, :, 0]
    alpha = base[:, :, 3] > 0
    t_base = gray / 255.0
    y, x = np.ogrid[:h, :w]
    
    frames = []
    for f in range(n_frames):
        phase = f / n_frames
        
        # Paleta com Hue Shift:
        # Sombra: Ametista abissal profunda (#200c2c)
        # Meio: Carmesim imperial nobre (#9c1b48)
        # Highlight: Ouro rosado acetinado e platina (#f8a4bc -> #fff0f5)
        r = 32.0 + t_base * 205.0
        g = 12.0 + (t_base ** 1.6) * 145.0
        b = 44.0 + (t_base ** 1.4) * 160.0
        
        # Glint suave e elegante deslizando pela faceta
        sweep = (phase * 24.0) - 4.0
        diag = (x * 0.7 + y * 0.5)
        glint = np.exp(-((diag - sweep) / 1.4)**2) * (t_base > 0.5)
        
        r += glint * 60.0
        g += glint * 50.0
        b += glint * 55.0
        
        frame = np.zeros((h, w, 4), dtype=np.uint8)
        frame[:, :, 0] = np.where(alpha, np.clip(r, 0, 255), 0)
        frame[:, :, 1] = np.where(alpha, np.clip(g, 0, 255), 0)
        frame[:, :, 2] = np.where(alpha, np.clip(b, 0, 255), 0)
        frame[:, :, 3] = np.where(alpha, 255, 0)
        frames.append(frame)
    return frames

def render_mellion_c2(n_frames=30):
    """Candidato 2: Godforge Resonant Energy Lattice (Rede Harmônica Forja de Deuses)"""
    base = TEMPLATE_SHINY.copy()
    h, w = base.shape[:2]
    gray = base[:, :, 0]
    alpha = base[:, :, 3] > 0
    t_base = gray / 255.0
    y, x = np.ogrid[:h, :w]
    
    frames = []
    for f in range(n_frames):
        phase = f / n_frames
        tau = 2 * math.pi * phase
        
        # Base vinho-rubi ressonante profundo
        r = 40.0 + t_base * 190.0
        g = 8.0 + (t_base ** 1.9) * 85.0
        b = 26.0 + (t_base ** 1.5) * 95.0
        
        # Ondas harmônicas de corte limpo (clusters diagonais em ressonância)
        lattice = np.sin((x - y) * 0.9 - tau) * 0.5 + 0.5
        harmonics = (lattice ** 4.0) * (t_base > 0.35)
        
        # Pico elétrico neon
        r += harmonics * 75.0
        g += harmonics * 25.0
        b += harmonics * 55.0
        
        # Highlights de cristal
        crystal_glint = np.sin((x + y) * 0.6 + tau) * 0.5 + 0.5
        cg = (crystal_glint ** 5.0) * (t_base > 0.7)
        r += cg * 65.0
        g += cg * 65.0
        b += cg * 75.0
        
        frame = np.zeros((h, w, 4), dtype=np.uint8)
        frame[:, :, 0] = np.where(alpha, np.clip(r, 0, 255), 0)
        frame[:, :, 1] = np.where(alpha, np.clip(g, 0, 255), 0)
        frame[:, :, 2] = np.where(alpha, np.clip(b, 0, 255), 0)
        frame[:, :, 3] = np.where(alpha, 255, 0)
        frames.append(frame)
    return frames

def render_mellion_c3(n_frames=30):
    """Candidato 3: Heavy Godforge Refractory Slate (Superliga Refratária com Veios de Ouro Divino)"""
    base = TEMPLATE_SHINY.copy()
    h, w = base.shape[:2]
    gray = base[:, :, 0]
    alpha = base[:, :, 3] > 0
    t_base = gray / 255.0
    y, x = np.ogrid[:h, :w]
    
    frames = []
    for f in range(n_frames):
        phase = f / n_frames
        tau = 2 * math.pi * phase
        
        # Superliga de titânio carmesim escuro ultra denso
        r = 45.0 + t_base * 165.0
        g = 15.0 + (t_base ** 1.8) * 65.0
        b = 30.0 + (t_base ** 1.6) * 55.0
        
        # Veios estáticos de ouro divino que cintilam pontualmente
        vein_pattern = (np.sin(x * 1.3 + y * 0.8) > 0.75) & (t_base > 0.45) & (t_base < 0.85)
        vein_shimmer = np.sin(tau + x * 0.5) * 0.5 + 0.5
        vein_glow = (vein_shimmer ** 3.0) * vein_pattern
        
        r += vein_glow * 110.0
        g += vein_glow * 85.0
        b += vein_glow * 10.0
        
        # Chanfro cirúrgico superior
        rim = (y <= x + 1) & (t_base > 0.7)
        r[rim] += 40.0
        g[rim] += 30.0
        b[rim] += 35.0
        
        frame = np.zeros((h, w, 4), dtype=np.uint8)
        frame[:, :, 0] = np.where(alpha, np.clip(r, 0, 255), 0)
        frame[:, :, 1] = np.where(alpha, np.clip(g, 0, 255), 0)
        frame[:, :, 2] = np.where(alpha, np.clip(b, 0, 255), 0)
        frame[:, :, 3] = np.where(alpha, 255, 0)
        frames.append(frame)
    return frames

# =========================================================================
# 3. NITINOL 60 (Ni4Ti6 SHAPE MEMORY SUPERALLOY)
# =========================================================================
def render_nitinol_c1(n_frames=30):
    """Candidato 1: Mirror-Polished Titanium-Nickel Chrome (Cromo-Titânio Espelhado Anisotrópico)"""
    base = TEMPLATE_MOD.copy()
    h, w = base.shape[:2]
    gray = base[:, :, 0]
    alpha = base[:, :, 3] > 0
    t_base = gray / 255.0
    y, x = np.ogrid[:h, :w]
    
    frames = []
    for f in range(n_frames):
        phase = f / n_frames
        
        # Paleta com Hue Shift aeroespacial:
        # Sombra: Grafite cobalto frio (#202634)
        # Meio: Aço níquel polido límpido (#8898aa)
        # Destaque: Cromo espelhado puro (#e6edf5 -> #ffffff)
        r = 32.0 + t_base * 205.0
        g = 38.0 + (t_base ** 1.05) * 202.0
        b = 52.0 + (t_base ** 1.1) * 198.0
        
        # Glint anisotrópico nítido de superliga polida
        sweep = (phase * 22.0) - 3.0
        diag = (x + y) * 0.5
        glint = np.exp(-((diag - sweep) / 1.0)**2) * (t_base > 0.6)
        
        # Glint estrela pontual no canto top-left
        star = 0.0
        if 8 <= f <= 11:
            st_dist = np.sqrt((x - 3.0)**2 + (y - 3.0)**2)
            star = np.exp(-(st_dist / 0.85)**2) * math.sin((f - 8) / 3.0 * math.pi)
            
        r += glint * 65.0 + star * 95.0
        g += glint * 70.0 + star * 95.0
        b += glint * 80.0 + star * 105.0
        
        frame = np.zeros((h, w, 4), dtype=np.uint8)
        frame[:, :, 0] = np.where(alpha, np.clip(r, 0, 255), 0)
        frame[:, :, 1] = np.where(alpha, np.clip(g, 0, 255), 0)
        frame[:, :, 2] = np.where(alpha, np.clip(b, 0, 255), 0)
        frame[:, :, 3] = np.where(alpha, 255, 0)
        frames.append(frame)
    return frames

def render_nitinol_c2(n_frames=30):
    """Candidato 2: Phase-Transition Shape Memory Sheen (Cisalhamento Austenite/Martensite)"""
    base = TEMPLATE_SHINY.copy()
    h, w = base.shape[:2]
    gray = base[:, :, 0]
    alpha = base[:, :, 3] > 0
    t_base = gray / 255.0
    y, x = np.ogrid[:h, :w]
    
    frames = []
    for f in range(n_frames):
        phase = f / n_frames
        tau = 2 * math.pi * phase
        
        # Frente de onda de transição de fase cristalina a 45 graus
        wave_pos = (phase * 26.0) - 5.0
        diag = (x * 0.707 + y * 0.707)
        shear_wave = np.exp(-((diag - wave_pos) / 1.8)**2) * (t_base > 0.3)
        
        # Base titânio-níquel
        r = 35.0 + t_base * 195.0
        g = 40.0 + t_base * 192.0
        b = 55.0 + t_base * 195.0
        
        # Transição de fase temporariamente induz calor de deformação dourado/âmbar sutil
        r += shear_wave * 60.0
        g += shear_wave * 50.0
        b += shear_wave * 20.0
        
        frame = np.zeros((h, w, 4), dtype=np.uint8)
        frame[:, :, 0] = np.where(alpha, np.clip(r, 0, 255), 0)
        frame[:, :, 1] = np.where(alpha, np.clip(g, 0, 255), 0)
        frame[:, :, 2] = np.where(alpha, np.clip(b, 0, 255), 0)
        frame[:, :, 3] = np.where(alpha, 255, 0)
        frames.append(frame)
    return frames

def render_nitinol_c3(n_frames=30):
    """Candidato 3: Modernity Heavy Aero-Titanium (Titânio Denso Modernity)"""
    base = TEMPLATE_MOD.copy()
    h, w = base.shape[:2]
    gray = base[:, :, 0]
    alpha = base[:, :, 3] > 0
    t_base = gray / 255.0
    y, x = np.ogrid[:h, :w]
    
    frames = []
    for f in range(n_frames):
        phase = f / n_frames
        
        # Alto contraste cirúrgico estilo Modernity Titanium/Tungsten
        r = 25.0 + t_base * 215.0
        g = 32.0 + t_base * 212.0
        b = 45.0 + t_base * 210.0
        
        # Reflexo estático muito limpo nos chanfros
        top_bevel = (y <= 3) & (t_base > 0.7)
        r[top_bevel] = np.clip(r[top_bevel] + 25.0, 0, 255)
        g[top_bevel] = np.clip(g[top_bevel] + 25.0, 0, 255)
        b[top_bevel] = np.clip(b[top_bevel] + 30.0, 0, 255)
        
        # Glint sutil a cada 15 frames
        sweep = ((phase * 2.0) % 1.0) * 20.0 - 2.0
        diag = (x + y) * 0.5
        glint = np.exp(-((diag - sweep) / 0.8)**2) * (t_base > 0.75)
        
        r += glint * 45.0
        g += glint * 45.0
        b += glint * 50.0
        
        frame = np.zeros((h, w, 4), dtype=np.uint8)
        frame[:, :, 0] = np.where(alpha, np.clip(r, 0, 255), 0)
        frame[:, :, 1] = np.where(alpha, np.clip(g, 0, 255), 0)
        frame[:, :, 2] = np.where(alpha, np.clip(b, 0, 255), 0)
        frame[:, :, 3] = np.where(alpha, 255, 0)
        frames.append(frame)
    return frames

# =========================================================================
# 4. SUPERCONDUCTOR UIV BASE
# =========================================================================
def render_superconductor_c1(n_frames=30):
    """Candidato 1: Zero-Resistance Supercurrent Filaments (Filamentos Quânticos em Clusters)"""
    base = TEMPLATE_MOD.copy()
    h, w = base.shape[:2]
    gray = base[:, :, 0]
    alpha = base[:, :, 3] > 0
    t_base = gray / 255.0
    y, x = np.ogrid[:h, :w]
    
    # Máscara de filamentos geométricos limpos de 1px (evita ruído estático)
    filaments = np.zeros((h, w), dtype=bool)
    filaments[4, 4:12] = True
    filaments[5:9, 7] = True
    filaments[8, 7:13] = True
    filaments[9:13, 10] = True
    filaments = filaments & alpha
    
    frames = []
    for f in range(n_frames):
        phase = f / n_frames
        tau = 2 * math.pi * phase
        
        # Paleta com Hue Shift:
        # Sombra: Índigo-violeta abissal (#1c0a2c)
        # Meio: Magenta cósmico puro (#b82294)
        # Destaque: Neon supercondutor (#ffa8f0 -> #ffffff)
        r = 35.0 + t_base * 195.0
        g = 10.0 + (t_base ** 1.8) * 115.0
        b = 55.0 + (t_base ** 1.3) * 165.0
        
        # Pulso ultra-rápido de supercorrente fluindo pelos filamentos
        pulse_pos = (phase * 18.0) % 12.0
        # Distância ao longo da trilha
        track_dist = (x + y * 0.8)
        current = np.exp(-((track_dist - (pulse_pos + 4.0)) / 1.2)**2) * filaments
        
        r += current * 125.0
        g += current * 115.0
        b += current * 135.0
        
        # Brilho chanfrado
        bevel = (y <= x) & (t_base > 0.65)
        glow = np.sin(tau) * 0.5 + 0.5
        r += bevel * (glow * 35.0 + 20.0)
        g += bevel * (glow * 15.0 + 10.0)
        b += bevel * (glow * 30.0 + 20.0)
        
        frame = np.zeros((h, w, 4), dtype=np.uint8)
        frame[:, :, 0] = np.where(alpha, np.clip(r, 0, 255), 0)
        frame[:, :, 1] = np.where(alpha, np.clip(g, 0, 255), 0)
        frame[:, :, 2] = np.where(alpha, np.clip(b, 0, 255), 0)
        frame[:, :, 3] = np.where(alpha, 255, 0)
        frames.append(frame)
    return frames

def render_superconductor_c2(n_frames=30):
    """Candidato 2: Meissner Levitation Crystal (Cristal Meissner Translúcido)"""
    base = TEMPLATE_SHINY.copy()
    h, w = base.shape[:2]
    gray = base[:, :, 0]
    alpha = base[:, :, 3] > 0
    t_base = gray / 255.0
    y, x = np.ogrid[:h, :w]
    
    cy, cx = 7.5, 7.5
    dist = np.sqrt((x - cx)**2 + (y - cy)**2)
    
    frames = []
    for f in range(n_frames):
        phase = f / n_frames
        tau = 2 * math.pi * phase
        
        # Matriz cristalina magenta-elétrica
        r = 40.0 + t_base * 190.0
        g = 12.0 + (t_base ** 2.0) * 110.0
        b = 60.0 + (t_base ** 1.4) * 175.0
        
        # Núcleo magnético pulsante
        core_pulse = np.sin(tau) * 0.5 + 0.5
        core = np.exp(-((dist - (core_pulse * 1.5 + 1.0)) / 1.6)**2) * (t_base > 0.35)
        
        r += core * 80.0
        g += core * 45.0
        b += core * 90.0
        
        # Expulsão de campo magnético nas bordas inferiores (halo ciano sutil)
        lower_rim = (y >= 10) & alpha & (t_base < 0.5)
        meissner_halo = (np.sin(tau + x * 0.5) * 0.5 + 0.5) * lower_rim
        r += meissner_halo * 10.0
        g += meissner_halo * 65.0
        b += meissner_halo * 95.0
        
        frame = np.zeros((h, w, 4), dtype=np.uint8)
        frame[:, :, 0] = np.where(alpha, np.clip(r, 0, 255), 0)
        frame[:, :, 1] = np.where(alpha, np.clip(g, 0, 255), 0)
        frame[:, :, 2] = np.where(alpha, np.clip(b, 0, 255), 0)
        frame[:, :, 3] = np.where(alpha, 255, 0)
        frames.append(frame)
    return frames

def render_superconductor_c3(n_frames=30):
    """Candidato 3: Modernity Cosmic Superconducting Ingot (Estilo Modernity High-Tier)"""
    base = TEMPLATE_MOD.copy()
    h, w = base.shape[:2]
    gray = base[:, :, 0]
    alpha = base[:, :, 3] > 0
    t_base = gray / 255.0
    y, x = np.ogrid[:h, :w]
    
    frames = []
    for f in range(n_frames):
        phase = f / n_frames
        tau = 2 * math.pi * phase
        
        # Lingote Modernity magenta com contraste extremo
        r = 30.0 + t_base * 210.0
        g = 8.0 + (t_base ** 1.9) * 120.0
        b = 50.0 + (t_base ** 1.3) * 195.0
        
        # Glint diagonal chanfrado contínuo
        sweep = (phase * 22.0) - 3.0
        diag = (x + y) * 0.5
        glint = np.exp(-((diag - sweep) / 1.1)**2) * (t_base > 0.6)
        
        # Clusters pontuais estelares (3 estrelas pontuais desfasadas em 120 graus)
        s1 = np.exp(-((x - 4.0)**2 + (y - 5.0)**2) / 0.8) * (np.sin(tau) * 0.5 + 0.5) ** 4.0
        s2 = np.exp(-((x - 11.0)**2 + (y - 10.0)**2) / 0.8) * (np.sin(tau + 2.09) * 0.5 + 0.5) ** 4.0
        s3 = np.exp(-((x - 8.0)**2 + (y - 7.0)**2) / 0.8) * (np.sin(tau + 4.18) * 0.5 + 0.5) ** 4.0
        stars = (s1 + s2 + s3) * (t_base > 0.35)
        
        r += glint * 55.0 + stars * 110.0
        g += glint * 45.0 + stars * 105.0
        b += glint * 70.0 + stars * 120.0
        
        frame = np.zeros((h, w, 4), dtype=np.uint8)
        frame[:, :, 0] = np.where(alpha, np.clip(r, 0, 255), 0)
        frame[:, :, 1] = np.where(alpha, np.clip(g, 0, 255), 0)
        frame[:, :, 2] = np.where(alpha, np.clip(b, 0, 255), 0)
        frame[:, :, 3] = np.where(alpha, 255, 0)
        frames.append(frame)
    return frames

print("Renderizadores definidos com sucesso.")

# =========================================================================
# MONTAGEM DO SHOWCASE & GERAÇÃO DE ASSETS
# =========================================================================

MATERIALS = [
    {
        "id": "dragonmetal",
        "name": "Dragonmetal (Dragonblood Metal)",
        "lore": "Metal exótico derivado de sangue dracônico condensado sob pressão hiperbárica. Símbolo de vigor vulcânico e poder ancestral.",
        "old_path": "src/main/resources/assets/gtceu/textures/item/material_sets/gtna_dragon_metal/ingot.png",
        "old_flaw": "Vermelho monocromático lavado (suco de morango/kool-aid), sem iridescência dracônica, sem contraste nas arestas e sem brilho de escama.",
        "candidates": [
            {
                "title": "Opção 1: Escama Dracônica Iridescente & Pulso de Brasa",
                "renderer": render_dragonmetal_c1,
                "desc": "Paleta rica com hue shift de granada profunda para rubi vivo e reflexo de escama em âmbar-dourado incandescente. Onda de calor diagonal fluindo em 30 frames."
            },
            {
                "title": "Opção 2: Coração Dracônico em Fusão & Sel-out Obsidiana",
                "renderer": render_dragonmetal_c2,
                "desc": "Silhueta robusta com contorno escuro em obsidiana vítrea. Núcleo com duplo batimento biológico (lub-dub) que atinge o ápice em ouro-branco incandescente."
            },
            {
                "title": "Opção 3: Aço Dracônico Modernity de Alto Contraste",
                "renderer": render_dragonmetal_c3,
                "desc": "Estilo clássico Modernity metálico cirúrgico. Chanfro de 1px com reflexo especular de diamante carmesim e cintilação estelar pontual no frame 15."
            }
        ]
    },
    {
        "id": "mellion",
        "name": "Mellion (Godforge UXV Catalyst Metal)",
        "lore": "Superliga catalisadora transcendental da cadeia do Forge of Gods (UXV). Usada em blindagens dimensionais e manipulação de plasma estelar.",
        "old_path": "src/main/resources/assets/gtceu/textures/item/material_sets/gtna_mellion/ingot.png",
        "old_flaw": "Rampa de cor puramente vermelha escura (lama de tijolo / ferrugem seca), sem brilho especular, sem hue shift e sem nobreza visual.",
        "candidates": [
            {
                "title": "Opção 1: Carmesim Imperial com Ouro Rosado Acetinado",
                "renderer": render_mellion_c1,
                "desc": "Sombra em ametista cósmica abissal, corpo carmesim aveludado nobre e highlights em ouro rosado/platina. Glint especular suave que desliza pela faceta chanfrada."
            },
            {
                "title": "Opção 2: Rede Harmônica Forja de Deuses (Cristal Ressonante)",
                "renderer": render_mellion_c2,
                "desc": "Estrutura metálico-vítrea com ondas diagonais harmônicas de corte limpo (sem ruído difuso) e picos elétricos neon carmesim em 30 frames contínuos."
            },
            {
                "title": "Opção 3: Superliga Refratária com Veios de Ouro Divino",
                "renderer": render_mellion_c3,
                "desc": "Silhueta pesada de superliga refratária com micro-veios dourados de infusão divina que cintilam pontualmente ao longo do ciclo."
            }
        ]
    },
    {
        "id": "nitinol_60",
        "name": "Nitinol 60 (Ni₄Ti₆ Shape Memory Superalloy)",
        "lore": "Liga avançada de 60% Níquel e 40% Titânio com superelasticidade e memória de forma. Usada em válvulas e anéis de contenção de altíssima tensão.",
        "old_path": "src/main/resources/assets/gtceu/textures/item/material_sets/gtna_nitinol_60/ingot.png",
        "old_flaw": "Cinza ferro genérico (#c8c8c8) sem alma, parecendo ferro do Minecraft beta de 2011. Sombras desbotadas e sem contraste de superliga aeroespacial.",
        "candidates": [
            {
                "title": "Opção 1: Cromo-Titânio Espelhado Anisotrópico",
                "renderer": render_nitinol_c1,
                "desc": "Sombras frias de cobalto-grafite profundo, corpo em níquel puro polido e chanfro superior em cromo puro espelhado (#ffffff) com glint estelar no canto superior esquerdo."
            },
            {
                "title": "Opção 2: Cisalhamento Termomecânico (Transição Austenite/Martensite)",
                "renderer": render_nitinol_c2,
                "desc": "Frente de onda de reorganização atômica que varre o lingote a 45°, alternando entre cromo frio e reflexo térmico suave com leve calor dourado de titânio."
            },
            {
                "title": "Opção 3: Titânio Denso Modernity de Alto Contraste",
                "renderer": render_nitinol_c3,
                "desc": "Estilo clássico aeroespacial Modernity com contraste cirúrgico de 190+, bordas bem marcadas e leitura instantânea em qualquer fundo de GUI."
            }
        ]
    },
    {
        "id": "superconductor_uiv",
        "name": "Superconductor UIV Base",
        "lore": "Supercondutor de tier UIV (Ultra Immense Voltage - 16.7M EU/t). Fórmula complexa (C₁₄Os₁₁O₇Ag₃SpH₂O)₄?₁ com assinatura magenta cósmica.",
        "old_path": "src/main/resources/assets/gtceu/textures/item/material_sets/gtna_superconductor_uiv_base/ingot.png",
        "old_flaw": "Ruído estático procedural desordenado (chiado de TV) que gerava pixels isolados rosa chiclete sem clusters, parecendo textura com artefato ou corrompida.",
        "candidates": [
            {
                "title": "Opção 1: Filamentos Quânticos de Supercorrente em Clusters",
                "renderer": render_superconductor_c1,
                "desc": "Substitui o ruído de TV por trilhas limpas de 1px em pixel art que conduzem pulsos ultra-rápidos de luz branca/magenta neon sem resistência."
            },
            {
                "title": "Opção 2: Cristal Meissner Translúcido com Halo Magnético",
                "renderer": render_superconductor_c2,
                "desc": "Matriz cristalina com núcleo que expande e contrai em pulso magnético harmônico, acompanhado de leve halo ciano-elétrico de levitação quântica na base."
            },
            {
                "title": "Opção 3: Lingote Cósmico Modernity com Cintilação Estelar",
                "renderer": render_superconductor_c3,
                "desc": "Estilo consagrado de lingotes cósmicos do Modernity: corpo magenta profundo de alto contraste com glint chanfrado contínuo e 3 estrelas pontuais desfasadas."
            }
        ]
    }
]

print("Processando geração de candidatos...")

DATA = []

for mat in MATERIALS:
    print(f" -> Processando {mat['name']}...")
    mat_data = {
        "id": mat["id"],
        "name": mat["name"],
        "lore": mat["lore"],
        "old_flaw": mat["old_flaw"],
        "cards": []
    }
    
    # 1. Old baseline
    old_frames = extract_old_texture_frames(mat["old_path"])
    if old_frames:
        old_gif = save_gif_base64(old_frames)
        old_metrics = analyze_palette(old_frames)
        mat_data["cards"].append({
            "is_old": True,
            "title": "Versão Atual (Baseline)",
            "desc": mat["old_flaw"],
            "gif": old_gif,
            "metrics": old_metrics
        })
    else:
        mat_data["cards"].append({
            "is_old": True,
            "title": "Versão Atual (Baseline)",
            "desc": "Arquivo não encontrado.",
            "gif": "",
            "metrics": {"unique_colors": 0, "min_lum": 0, "max_lum": 0, "contrast": 0, "swatches": []}
        })
        
    # 2. Candidates
    for i, cand in enumerate(mat["candidates"]):
        frames = cand["renderer"]()
        gif = save_gif_base64(frames)
        metrics = analyze_palette(frames)
        mat_data["cards"].append({
            "is_old": False,
            "title": cand["title"],
            "desc": cand["desc"],
            "gif": gif,
            "metrics": metrics
        })
        
    DATA.append(mat_data)

print("Gerando página HTML interativa...")

HTML = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>GTNA Texture Fine-Tuning Showcase - Grupo 1</title>
<style>
:root {
  --bg: #0d1117;
  --panel: #161b22;
  --border: #30363d;
  --text: #c9d1d9;
  --text-bright: #f0f6fc;
  --accent: #58a6ff;
  --accent-glow: rgba(88, 166, 255, 0.2);
  --danger: #f85149;
  --danger-bg: rgba(248, 81, 73, 0.15);
  --success: #3fb950;
  --success-bg: rgba(63, 185, 80, 0.15);
  --slot-bg: #8b8b8b;
  --slot-border-dark: #373737;
  --slot-border-light: #ffffff;
}

* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  background: var(--bg);
  color: var(--text);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  line-height: 1.5;
  padding: 24px;
}

.header {
  max-width: 1300px;
  margin: 0 auto 24px auto;
  border-bottom: 1px solid var(--border);
  padding-bottom: 20px;
}

.header h1 {
  color: var(--text-bright);
  font-size: 26px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.header .badge {
  background: #1f6feb;
  color: #fff;
  font-size: 12px;
  padding: 4px 8px;
  border-radius: 12px;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.header p {
  color: #8b949e;
  margin-top: 6px;
  font-size: 14px;
}

.controls {
  max-width: 1300px;
  margin: 0 auto 20px auto;
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  align-items: center;
  justify-content: space-between;
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 12px 20px;
}

.tabs {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.tab-btn {
  background: #21262d;
  color: var(--text);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 8px 16px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.tab-btn:hover {
  background: #30363d;
  color: var(--text-bright);
}

.tab-btn.active {
  background: #1f6feb;
  color: #fff;
  border-color: #58a6ff;
  box-shadow: 0 0 12px var(--accent-glow);
}

.view-options {
  display: flex;
  gap: 16px;
  align-items: center;
  font-size: 13px;
}

.select-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

select {
  background: #21262d;
  color: var(--text-bright);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 6px 12px;
  font-size: 13px;
  outline: none;
}

.content {
  max-width: 1300px;
  margin: 0 auto;
}

.material-section {
  display: none;
  animation: fadeIn 0.25s ease-in-out;
}

.material-section.active {
  display: block;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(6px); }
  to { opacity: 1; transform: translateY(0); }
}

.mat-intro {
  margin-bottom: 20px;
  background: rgba(33, 38, 45, 0.5);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 16px 20px;
}

.mat-intro h2 {
  font-size: 20px;
  color: var(--text-bright);
  margin-bottom: 4px;
}

.mat-intro p {
  color: #8b949e;
  font-size: 14px;
}

.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(290px, 1fr));
  gap: 20px;
}

.card {
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  position: relative;
  transition: transform 0.2s, border-color 0.2s;
}

.card:hover {
  border-color: #58a6ff;
  transform: translateY(-2px);
}

.card.old {
  border-color: rgba(248, 81, 73, 0.4);
  background: linear-gradient(180deg, rgba(248, 81, 73, 0.05) 0%, var(--panel) 100%);
}

.card-header {
  margin-bottom: 16px;
}

.card-tag {
  display: inline-block;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  padding: 2px 8px;
  border-radius: 4px;
  margin-bottom: 8px;
}

.card-tag.old-tag {
  background: var(--danger-bg);
  color: var(--danger);
  border: 1px solid rgba(248, 81, 73, 0.3);
}

.card-tag.cand-tag {
  background: var(--success-bg);
  color: var(--success);
  border: 1px solid rgba(63, 185, 80, 0.3);
}

.card-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-bright);
  line-height: 1.3;
}

.card-desc {
  font-size: 13px;
  color: #8b949e;
  margin-top: 8px;
  min-height: 52px;
}

.preview-box-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 24px 0;
  border-top: 1px solid var(--border);
  border-bottom: 1px solid var(--border);
  margin: 12px 0 16px 0;
}

/* JEI Minecraft Slot View */
.slot-jei {
  width: 144px;
  height: 144px;
  background: #8b8b8b;
  border-top: 4px solid #373737;
  border-left: 4px solid #373737;
  border-bottom: 4px solid #ffffff;
  border-right: 4px solid #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.4);
}

.slot-dark {
  width: 144px;
  height: 144px;
  background: #0d1117;
  border: 2px solid #30363d;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.slot-clean {
  width: 144px;
  height: 144px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.pixel-img {
  image-rendering: pixelated;
  image-rendering: crisp-edges;
  transition: width 0.15s, height 0.15s;
}

.metrics {
  display: flex;
  flex-direction: column;
  gap: 8px;
  font-size: 12px;
  margin-bottom: 16px;
}

.metric-row {
  display: flex;
  justify-content: space-between;
  color: #8b949e;
}

.metric-val {
  color: var(--text-bright);
  font-weight: 600;
  font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
}

.swatches-row {
  display: flex;
  gap: 6px;
  align-items: center;
}

.swatch {
  width: 18px;
  height: 18px;
  border-radius: 4px;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.action-btn {
  margin-top: auto;
  background: #21262d;
  border: 1px solid var(--border);
  color: var(--text-bright);
  padding: 8px 14px;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  transition: all 0.2s;
}

.action-btn:hover {
  background: #1f6feb;
  border-color: #58a6ff;
}

.action-btn.copied {
  background: #238636;
  border-color: #3fb950;
}
</style>
</head>
<body>

<div class="header">
  <h1>
    <span>GTNA Texture Fine-Tuning Showcase</span>
    <span class="badge">GRUPO 1</span>
  </h1>
  <p>Calibração estética com design system estrito de Pixel Art: Hue-shifting dinâmico, clusters limpos sem ruído difuso e iluminação Top-Left.</p>
</div>

<div class="controls">
  <div class="tabs" id="tabs">
"""

for i, mat in enumerate(DATA):
    active_cls = " active" if i == 0 else ""
    HTML += f'    <button class="tab-btn{active_cls}" onclick="switchTab(\'{mat["id"]}\')">{mat["name"].split(" ")[0]}</button>\n'

HTML += """  </div>
  <div class="view-options">
    <div class="select-group">
      <label for="zoomSelect">Escala / Zoom:</label>
      <select id="zoomSelect" onchange="updateZoom(this.value)">
        <option value="16">1× (16px Nativo)</option>
        <option value="64">4× (64px)</option>
        <option value="96" selected>6× (96px Padrão)</option>
        <option value="128">8× (128px JEI Grande)</option>
      </select>
    </div>
    <div class="select-group">
      <label for="slotSelect">Visualizador:</label>
      <select id="slotSelect" onchange="updateSlotMode(this.value)">
        <option value="slot-jei" selected>Slot JEI (Cinza 3D)</option>
        <option value="slot-dark">Fundo Escuro (Dark HUD)</option>
        <option value="slot-clean">Transparente Limpo</option>
      </select>
    </div>
  </div>
</div>

<div class="content">
"""

for i, mat in enumerate(DATA):
    active_cls = " active" if i == 0 else ""
    HTML += f'<div class="material-section{active_cls}" id="sec-{mat["id"]}">\n'
    HTML += f'  <div class="mat-intro">\n'
    HTML += f'    <h2>{mat["name"]}</h2>\n'
    HTML += f'    <p>{mat["lore"]}</p>\n'
    HTML += f'  </div>\n'
    HTML += f'  <div class="cards-grid">\n'
    
    for c_idx, card in enumerate(mat["cards"]):
        old_cls = " old" if card["is_old"] else ""
        tag_cls = "old-tag" if card["is_old"] else "cand-tag"
        tag_txt = "Problema Atual" if card["is_old"] else f"Candidato {c_idx}"
        
        swatches_html = ""
        for sw in card["metrics"]["swatches"]:
            swatches_html += f'<div class="swatch" style="background:{sw};" title="{sw}"></div>'
            
        HTML += f"""    <div class="card{old_cls}">
      <div class="card-header">
        <span class="card-tag {tag_cls}">{tag_txt}</span>
        <div class="card-title">{card["title"]}</div>
        <div class="card-desc">{card["desc"]}</div>
      </div>
      <div class="preview-box-container">
        <div class="slot-box slot-jei">
          <img class="pixel-img" src="data:image/gif;base64,{card["gif"]}" style="width:96px;height:96px;" alt="{card["title"]}">
        </div>
      </div>
      <div class="metrics">
        <div class="metric-row">
          <span>Paleta / Cores Únicas:</span>
          <span class="metric-val">{card["metrics"]["unique_colors"]} cores</span>
        </div>
        <div class="metric-row">
          <span>Luminância [Min, Max]:</span>
          <span class="metric-val">[{card["metrics"]["min_lum"]}, {card["metrics"]["max_lum"]}]</span>
        </div>
        <div class="metric-row">
          <span>Contraste Dinâmico (ΔL):</span>
          <span class="metric-val">{card["metrics"]["contrast"]}</span>
        </div>
        <div class="metric-row" style="margin-top:4px;">
          <span>Rampa de Matiz:</span>
          <div class="swatches-row">
            {swatches_html}
          </div>
        </div>
      </div>
"""
        if not card["is_old"]:
            btn_text = f"Escolher Opção {c_idx}"
            choice_val = f"{mat['name']} -> Opção {c_idx}: {card['title']}"
            HTML += f"""      <button class="action-btn" onclick="copyChoice(this, '{choice_val}')">
        <span>✓</span> {btn_text}
      </button>
"""
        HTML += "    </div>\n"
        
    HTML += "  </div>\n"
    HTML += "</div>\n"

HTML += """</div>

<script>
function switchTab(id) {
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.querySelectorAll('.material-section').forEach(s => s.classList.remove('active'));
  
  event.target.classList.add('active');
  document.getElementById('sec-' + id).classList.add('active');
}

function updateZoom(size) {
  document.querySelectorAll('.pixel-img').forEach(img => {
    img.style.width = size + 'px';
    img.style.height = size + 'px';
  });
}

function updateSlotMode(modeClass) {
  document.querySelectorAll('.slot-box').forEach(box => {
    box.className = 'slot-box ' + modeClass;
  });
}

function copyChoice(btn, text) {
  navigator.clipboard.writeText(text).then(() => {
    const orig = btn.innerHTML;
    btn.classList.add('copied');
    btn.innerHTML = '<span>✓</span> Copiado para o chat!';
    setTimeout(() => {
      btn.classList.remove('copied');
      btn.innerHTML = orig;
    }, 2000);
  });
}
</script>
</body>
</html>
"""

out_html_path = REPO_ROOT / "docs/visualization/fine_tuning_showcase_g1.html"
out_html_path.parent.mkdir(parents=True, exist_ok=True)
out_html_path.write_text(HTML, encoding="utf-8")

artifact_html_path = ARTIFACT_DIR / "fine_tuning_showcase_g1.html"
artifact_html_path.write_text(HTML, encoding="utf-8")

print(f"Showcase gerado com sucesso!")
print(f" -> Docs path: {out_html_path}")
print(f" -> Artifact path: {artifact_html_path}")
