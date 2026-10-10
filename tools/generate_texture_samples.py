import os
import json
import base64
import numpy as np
from PIL import Image
from pathlib import Path

WD_ITEMS = Path("/home/raishxn/Downloads/Modernity-GTNH-2026-09-07/assets/gregtech/textures/items/materialicons/CUSTOM/WhiteDwarfMatter")
OUT_DIR = Path("/tmp/gtna_texture_preview")
OUT_DIR.mkdir(parents=True, exist_ok=True)

def palette_echoite(gray_val):
    t = gray_val / 255.0
    r = np.zeros_like(t)
    g = np.zeros_like(t)
    b = np.zeros_like(t)
    
    # Shadow: deep abyssal Warden sculk teal (#092420 to #13463b)
    mask1 = t < 0.4
    s1 = np.clip(t / 0.4, 0, 1)
    r[mask1] = 9 + s1[mask1] * (22 - 9)
    g[mask1] = 34 + s1[mask1] * (72 - 34)
    b[mask1] = 30 + s1[mask1] * (65 - 30)
    
    # Midtone: rich signature #26734d teal
    mask2 = (t >= 0.4) & (t < 0.75)
    s2 = np.clip((t - 0.4) / 0.35, 0, 1)
    r[mask2] = 22 + s2[mask2] * (38 - 22)
    g[mask2] = 72 + s2[mask2] * (145 - 72)
    b[mask2] = 65 + s2[mask2] * (115 - 65)
    
    # Highlight: vibrant soul / sculk cyan (#00ffd5)
    mask3 = t >= 0.75
    s3 = np.clip((t - 0.75) / 0.25, 0, 1)
    r[mask3] = 38 + s3[mask3] * (110 - 38)
    g[mask3] = 145 + s3[mask3] * (235 - 145)
    b[mask3] = 115 + s3[mask3] * (210 - 115)
    
    return np.dstack([r, g, b])

def palette_universium(gray_val):
    t = gray_val / 255.0
    r = np.zeros_like(t)
    g = np.zeros_like(t)
    b = np.zeros_like(t)
    
    # Deep cosmic dark blue-violet (#130e2e)
    mask1 = t < 0.4
    s1 = np.clip(t / 0.4, 0, 1)
    r[mask1] = 24 + s1[mask1] * (62 - 24)
    g[mask1] = 16 + s1[mask1] * (42 - 16)
    b[mask1] = 52 + s1[mask1] * (115 - 52)
    
    # Astral nebula magenta/violet (#8b3cb5)
    mask2 = (t >= 0.4) & (t < 0.75)
    s2 = np.clip((t - 0.4) / 0.35, 0, 1)
    r[mask2] = 62 + s2[mask2] * (145 - 62)
    g[mask2] = 42 + s2[mask2] * (82 - 42)
    b[mask2] = 115 + s2[mask2] * (200 - 115)
    
    # Cosmic starlight / diamond nebula
    mask3 = t >= 0.75
    s3 = np.clip((t - 0.75) / 0.25, 0, 1)
    r[mask3] = 145 + s3[mask3] * (245 - 145)
    g[mask3] = 82 + s3[mask3] * (215 - 82)
    b[mask3] = 200 + s3[mask3] * (255 - 200)
    
    return np.dstack([r, g, b])

def palette_ichorium(gray_val):
    t = gray_val / 255.0
    r = np.zeros_like(t)
    g = np.zeros_like(t)
    b = np.zeros_like(t)
    
    mask1 = t < 0.4
    s1 = np.clip(t / 0.4, 0, 1)
    r[mask1] = 90 + s1[mask1] * (165 - 90)
    g[mask1] = 36 + s1[mask1] * (82 - 36)
    b[mask1] = 6 + s1[mask1] * (16 - 6)
    
    mask2 = (t >= 0.4) & (t < 0.75)
    s2 = np.clip((t - 0.4) / 0.35, 0, 1)
    r[mask2] = 165 + s2[mask2] * (228 - 165)
    g[mask2] = 82 + s2[mask2] * (145 - 82)
    b[mask2] = 16 + s2[mask2] * (32 - 16)
    
    mask3 = t >= 0.75
    s3 = np.clip((t - 0.75) / 0.25, 0, 1)
    r[mask3] = 228 + s3[mask3] * (255 - 228)
    g[mask3] = 145 + s3[mask3] * (235 - 145)
    b[mask3] = 32 + s3[mask3] * (140 - 32)
    
    return np.dstack([r, g, b])

def palette_tengam_purified(gray_val):
    t = gray_val / 255.0
    r = np.zeros_like(t)
    g = np.zeros_like(t)
    b = np.zeros_like(t)
    
    mask1 = t < 0.4
    s1 = np.clip(t / 0.4, 0, 1)
    r[mask1] = 52 + s1[mask1] * (115 - 52)
    g[mask1] = 82 + s1[mask1] * (165 - 82)
    b[mask1] = 26 + s1[mask1] * (65 - 26)
    
    mask2 = (t >= 0.4) & (t < 0.75)
    s2 = np.clip((t - 0.4) / 0.35, 0, 1)
    r[mask2] = 115 + s2[mask2] * (195 - 115)
    g[mask2] = 165 + s2[mask2] * (232 - 165)
    b[mask2] = 65 + s2[mask2] * (115 - 65)
    
    mask3 = t >= 0.75
    s3 = np.clip((t - 0.75) / 0.25, 0, 1)
    r[mask3] = 195 + s3[mask3] * (242 - 195)
    g[mask3] = 232 + s3[mask3] * (255 - 232)
    b[mask3] = 115 + s3[mask3] * (195 - 115)
    
    return np.dstack([r, g, b])

def palette_tengam_attuned(gray_val):
    t = gray_val / 255.0
    r = np.zeros_like(t)
    g = np.zeros_like(t)
    b = np.zeros_like(t)
    
    mask1 = t < 0.4
    s1 = np.clip(t / 0.4, 0, 1)
    r[mask1] = 65 + s1[mask1] * (145 - 65)
    g[mask1] = 105 + s1[mask1] * (205 - 105)
    b[mask1] = 30 + s1[mask1] * (78 - 30)
    
    mask2 = (t >= 0.4) & (t < 0.75)
    s2 = np.clip((t - 0.4) / 0.35, 0, 1)
    r[mask2] = 145 + s2[mask2] * (220 - 145)
    g[mask2] = 205 + s2[mask2] * (255 - 205)
    b[mask2] = 78 + s2[mask2] * (135 - 78)
    
    mask3 = t >= 0.75
    s3 = np.clip((t - 0.75) / 0.25, 0, 1)
    r[mask3] = 220 + s3[mask3] * (255 - 220)
    g[mask3] = 255
    b[mask3] = 135 + s3[mask3] * (235 - 135)
    
    return np.dstack([r, g, b])

def palette_fallking(gray_val):
    t = gray_val / 255.0
    r = np.zeros_like(t)
    g = np.zeros_like(t)
    b = np.zeros_like(t)
    
    mask1 = t < 0.4
    s1 = np.clip(t / 0.4, 0, 1)
    r[mask1] = 95 + s1[mask1] * (185 - 95)
    g[mask1] = 72 + s1[mask1] * (145 - 72)
    b[mask1] = 32 + s1[mask1] * (68 - 32)
    
    mask2 = (t >= 0.4) & (t < 0.75)
    s2 = np.clip((t - 0.4) / 0.35, 0, 1)
    r[mask2] = 185 + s2[mask2] * (255 - 185)
    g[mask2] = 145 + s2[mask2] * (212 - 145)
    b[mask2] = 68 + s2[mask2] * (115 - 68)
    
    mask3 = t >= 0.75
    s3 = np.clip((t - 0.75) / 0.25, 0, 1)
    r[mask3] = 255
    g[mask3] = 212 + s3[mask3] * (250 - 212)
    b[mask3] = 115 + s3[mask3] * (210 - 115)
    
    return np.dstack([r, g, b])

def palette_odyssey(gray_val):
    t = gray_val / 255.0
    r = np.zeros_like(t)
    g = np.zeros_like(t)
    b = np.zeros_like(t)
    
    mask1 = t < 0.4
    s1 = np.clip(t / 0.4, 0, 1)
    r[mask1] = 26 + s1[mask1] * (48 - 26)
    g[mask1] = 48 + s1[mask1] * (88 - 48)
    b[mask1] = 42 + s1[mask1] * (78 - 42)
    
    mask2 = (t >= 0.4) & (t < 0.75)
    s2 = np.clip((t - 0.4) / 0.35, 0, 1)
    r[mask2] = 48 + s2[mask2] * (88 - 48)
    g[mask2] = 88 + s2[mask2] * (148 - 88)
    b[mask2] = 78 + s2[mask2] * (132 - 78)
    
    mask3 = t >= 0.75
    s3 = np.clip((t - 0.75) / 0.25, 0, 1)
    r[mask3] = 88 + s3[mask3] * (165 - 88)
    g[mask3] = 148 + s3[mask3] * (225 - 148)
    b[mask3] = 132 + s3[mask3] * (210 - 132)
    
    return np.dstack([r, g, b])

def palette_draconium(gray_val):
    t = gray_val / 255.0
    r = np.zeros_like(t)
    g = np.zeros_like(t)
    b = np.zeros_like(t)
    
    mask1 = t < 0.4
    s1 = np.clip(t / 0.4, 0, 1)
    r[mask1] = 35 + s1[mask1] * (85 - 35)
    g[mask1] = 10 + s1[mask1] * (28 - 10)
    b[mask1] = 55 + s1[mask1] * (125 - 55)
    
    mask2 = (t >= 0.4) & (t < 0.75)
    s2 = np.clip((t - 0.4) / 0.35, 0, 1)
    r[mask2] = 85 + s2[mask2] * (165 - 85)
    g[mask2] = 28 + s2[mask2] * (58 - 28)
    b[mask2] = 125 + s2[mask2] * (225 - 125)
    
    mask3 = t >= 0.75
    s3 = np.clip((t - 0.75) / 0.25, 0, 1)
    r[mask3] = 165 + s3[mask3] * (245 - 165)
    g[mask3] = 58 + s3[mask3] * (195 - 58)
    b[mask3] = 225 + s3[mask3] * (255 - 225)
    
    return np.dstack([r, g, b])

def palette_awakened_draconium(gray_val):
    t = gray_val / 255.0
    r = np.zeros_like(t)
    g = np.zeros_like(t)
    b = np.zeros_like(t)
    
    mask1 = t < 0.4
    s1 = np.clip(t / 0.4, 0, 1)
    r[mask1] = 95 + s1[mask1] * (185 - 95)
    g[mask1] = 16 + s1[mask1] * (52 - 16)
    b[mask1] = 0 + s1[mask1] * (8 - 0)
    
    mask2 = (t >= 0.4) & (t < 0.75)
    s2 = np.clip((t - 0.4) / 0.35, 0, 1)
    r[mask2] = 185 + s2[mask2] * (255 - 185)
    g[mask2] = 52 + s2[mask2] * (135 - 52)
    b[mask2] = 8 + s2[mask2] * (18 - 8)
    
    mask3 = t >= 0.75
    s3 = np.clip((t - 0.75) / 0.25, 0, 1)
    r[mask3] = 255
    g[mask3] = 135 + s3[mask3] * (250 - 135)
    b[mask3] = 18 + s3[mask3] * (180 - 18)
    
    return np.dstack([r, g, b])

def palette_cosmic_neutronium(gray_val):
    t = gray_val / 255.0
    r = np.zeros_like(t)
    g = np.zeros_like(t)
    b = np.zeros_like(t)
    
    mask1 = t < 0.5
    s1 = np.clip(t / 0.5, 0, 1)
    r[mask1] = 4 + s1[mask1] * (18 - 4)
    g[mask1] = 8 + s1[mask1] * (24 - 8)
    b[mask1] = 18 + s1[mask1] * (48 - 18)
    
    mask2 = t >= 0.5
    s2 = np.clip((t - 0.5) / 0.5, 0, 1)
    r[mask2] = 18 + s2[mask2] * (42 - 18)
    g[mask2] = 24 + s2[mask2] * (54 - 24)
    b[mask2] = 48 + s2[mask2] * (92 - 48)
    
    return np.dstack([r, g, b])

def generate_animation_frames(base_im, mat_name, n_frames=30):
    base_arr = np.array(base_im.convert("RGBA"), dtype=np.float32)
    h_orig, w_orig = base_arr.shape[:2]
    if h_orig > w_orig:
        base_arr = base_arr[:w_orig, :, :]
    h, w = base_arr.shape[:2]
    gray = base_arr[:, :, 0]
    alpha = base_arr[:, :, 3] > 0
    t_base = gray / 255.0
    y_coords, x_coords = np.ogrid[:h, :w]
    
    cy = np.sum(np.where(alpha, y_coords, 0)) / max(1, np.sum(alpha))
    cx = np.sum(np.where(alpha, x_coords, 0)) / max(1, np.sum(alpha))
    dist = np.sqrt((x_coords - cx)**2 + (y_coords - cy)**2)
    
    frames = []
    
    if mat_name == "echoite":
        colored_rgb = palette_echoite(gray)
        colored = np.zeros_like(base_arr)
        colored[:, :, :3] = colored_rgb
        colored[:, :, 3] = base_arr[:, :, 3]
        
        # Sculk soul tendril pattern
        vein1 = np.abs((x_coords * 1.1 + y_coords * 0.7) % 5.0 - 2.5)
        vein2 = np.abs((x_coords * 0.8 - y_coords * 1.2) % 6.0 - 3.0)
        tendrils = np.exp(-vein1 * 2.2) + np.exp(-vein2 * 2.2)
        
        for f in range(n_frames):
            frame = colored.copy()
            t = f / n_frames
            
            # Concentric sonic resonance wave propagating outward
            sonic_phase = (dist / 3.8 - t * 2.0) % 1.0
            sonic_wave = np.exp(-((sonic_phase - 0.5) / 0.16)**2) * (t_base > 0.35)
            
            # Sculk soul flicker
            sculk_pulse = np.sin(2 * np.pi * (t * 2.5 + dist / 7.0)) * 0.5 + 0.5
            soul_veins = tendrils * sculk_pulse * (0.4 + 0.6 * t_base)
            
            # Sonic boom echo peak
            boom_echo = (np.sin(2 * np.pi * t) ** 16) * np.exp(-dist / 5.0) * 85.0
            
            total_sculk = (sonic_wave * 75.0 + soul_veins * 60.0 + boom_echo)
            
            # Add vivid Warden soul-cyan (#00ffd5)
            frame[:, :, 0] += total_sculk * 0.12
            frame[:, :, 1] += total_sculk * 1.05
            frame[:, :, 2] += total_sculk * 0.95
            
            for c in range(3):
                frame[:, :, c] = np.where(alpha, np.clip(frame[:, :, c], 0, 255), 0)
            frames.append(frame.astype(np.uint8))
            
    elif mat_name == "universium":
        colored_rgb = palette_universium(gray)
        colored = np.zeros_like(base_arr)
        colored[:, :, :3] = colored_rgb
        colored[:, :, 3] = base_arr[:, :, 3]
        
        # Twinkling star field
        valid_coords = np.argwhere((alpha) & (t_base > 0.4))
        np.random.seed(777)
        star_pts = [valid_coords[i % len(valid_coords)] for i in [5, 18, 33, 52, 70]] if len(valid_coords) > 75 else []
        star_phases = [0.0, 0.22, 0.45, 0.68, 0.88]
        
        for f in range(n_frames):
            frame = colored.copy()
            t = f / n_frames
            
            # Diagonal sweeping cosmic continuum band
            band_phase = (x_coords * 0.7 - y_coords * 0.7 - t * 16.0) % 14.0
            band_glow = np.exp(-((band_phase - 7.0) / 1.6)**2) * (t_base > 0.3)
            
            # Nebular oscillation
            nebula = np.sin(2 * np.pi * (t + (x_coords + y_coords) / 16.0)) * 15.0
            
            frame[:, :, 0] += band_glow * 95.0 + nebula * 0.9
            frame[:, :, 1] += band_glow * 65.0 + nebula * 0.5
            frame[:, :, 2] += band_glow * 135.0 + nebula * 1.3
            
            for (sy, sx), sp in zip(star_pts, star_phases):
                glint = max(0.0, np.cos(((t - sp) % 1.0) * 2 * np.pi)) ** 10
                if glint > 0.05:
                    for dy, dx, weight in [(0, 0, 1.0), (0, 1, 0.35), (0, -1, 0.35), (1, 0, 0.35), (-1, 0, 0.35)]:
                        ny, nx = sy + dy, sx + dx
                        if 0 <= ny < h and 0 <= nx < w and alpha[ny, nx]:
                            v = glint * weight * 165.0
                            frame[ny, nx, 0] += v * 0.95
                            frame[ny, nx, 1] += v * 0.90
                            frame[ny, nx, 2] += v * 1.00
                            
            for c in range(3):
                frame[:, :, c] = np.where(alpha, np.clip(frame[:, :, c], 0, 255), 0)
            frames.append(frame.astype(np.uint8))
            
    elif mat_name == "ichorium":
        colored_rgb = palette_ichorium(gray)
        colored = np.zeros_like(base_arr)
        colored[:, :, :3] = colored_rgb
        colored[:, :, 3] = base_arr[:, :, 3]
        
        for f in range(n_frames):
            frame = colored.copy()
            t = f / n_frames
            
            # Divine golden sunlight glint sweeping diagonally
            glint_coord = (x_coords * 0.9 + y_coords * 1.1 - t * 18.0) % 15.0
            glint_beam = np.exp(-((glint_coord - 7.5) / 1.3)**2) * (t_base > 0.35)
            
            # Arcane thaumic aura breathing
            arcane_aura = np.sin(2 * np.pi * (t * 2.0 - dist / 6.0)) * 0.5 + 0.5
            aura_glow = arcane_aura * 28.0 * (0.3 + 0.7 * t_base)
            
            frame[:, :, 0] += glint_beam * 115.0 + aura_glow * 1.15
            frame[:, :, 1] += glint_beam * 95.0 + aura_glow * 0.90
            frame[:, :, 2] += glint_beam * 30.0 + aura_glow * 0.25
            
            for c in range(3):
                frame[:, :, c] = np.where(alpha, np.clip(frame[:, :, c], 0, 255), 0)
            frames.append(frame.astype(np.uint8))
            
    elif mat_name == "tengam_purified":
        colored_rgb = palette_tengam_purified(gray)
        colored = np.zeros_like(base_arr)
        colored[:, :, :3] = colored_rgb
        colored[:, :, 3] = base_arr[:, :, 3]
        
        for f in range(n_frames):
            frame = colored.copy()
            t = f / n_frames
            
            # Magnetic flux loop traveling along field gradient
            flux = np.sin(2 * np.pi * (t * 2.0 - (x_coords * 0.9 + y_coords * 0.6) / 5.5))
            flux_intensity = np.maximum(0, flux) ** 2 * 65.0 * (0.35 + 0.65 * t_base)
            
            frame[:, :, 0] += flux_intensity * 0.85
            frame[:, :, 1] += flux_intensity * 1.10
            frame[:, :, 2] += flux_intensity * 0.45
            
            for c in range(3):
                frame[:, :, c] = np.where(alpha, np.clip(frame[:, :, c], 0, 255), 0)
            frames.append(frame.astype(np.uint8))
            
    elif mat_name == "tengam_attuned":
        colored_rgb = palette_tengam_attuned(gray)
        colored = np.zeros_like(base_arr)
        colored[:, :, :3] = colored_rgb
        colored[:, :, 3] = base_arr[:, :, 3]
        
        for f in range(n_frames):
            frame = colored.copy()
            t = f / n_frames
            
            # High-intensity alternating dipole oscillations
            dipole = np.sin(2 * np.pi * (t * 3.0 + x_coords / 4.0)) * np.cos(2 * np.pi * (t * 2.0 - y_coords / 5.0))
            dipole_glow = (dipole * 0.5 + 0.5) ** 2 * 70.0
            
            # Sharp electrostatic spark discharge
            spark = (np.sin(2 * np.pi * (t * 4.0 + y_coords * 0.9)) ** 12) * 80.0 * (t_base > 0.45)
            
            frame[:, :, 0] += (dipole_glow + spark) * 0.90
            frame[:, :, 1] += (dipole_glow + spark) * 1.10
            frame[:, :, 2] += (dipole_glow + spark) * 0.80
            
            for c in range(3):
                frame[:, :, c] = np.where(alpha, np.clip(frame[:, :, c], 0, 255), 0)
            frames.append(frame.astype(np.uint8))
            
    elif mat_name == "fallking":
        colored_rgb = palette_fallking(gray)
        colored = np.zeros_like(base_arr)
        colored[:, :, :3] = colored_rgb
        colored[:, :, 3] = base_arr[:, :, 3]
        
        for f in range(n_frames):
            frame = colored.copy()
            t = f / n_frames
            
            # Hypersonic aerodynamic rotor torque gleam
            sweep_phase = (x_coords * 1.4 - y_coords * 0.7 - t * 22.0) % 16.0
            blade_gleam = np.exp(-((sweep_phase - 8.0) / 1.25)**2) * (t_base > 0.35)
            
            # Radiant solar gold luster
            solar_sheen = np.sin(2 * np.pi * (t * 2.0 + (x_coords + y_coords) / 14.0)) * 18.0
            
            frame[:, :, 0] += blade_gleam * 125.0 + solar_sheen * 1.15
            frame[:, :, 1] += blade_gleam * 110.0 + solar_sheen * 0.95
            frame[:, :, 2] += blade_gleam * 55.0 + solar_sheen * 0.40
            
            for c in range(3):
                frame[:, :, c] = np.where(alpha, np.clip(frame[:, :, c], 0, 255), 0)
            frames.append(frame.astype(np.uint8))
            
    elif mat_name == "odyssey":
        colored_rgb = palette_odyssey(gray)
        colored = np.zeros_like(base_arr)
        colored[:, :, :3] = colored_rgb
        colored[:, :, 3] = base_arr[:, :, 3]
        
        # Hexagonal nanite lattice
        grid_hex = ((x_coords + (y_coords % 2)) % 3 == 0) | (y_coords % 3 == 0)
        
        for f in range(n_frames):
            frame = colored.copy()
            t = f / n_frames
            
            # Nanite pulse propagating through honeycomb lattice
            wave = (x_coords + y_coords - t * 16.0) % 9.0
            wave_glow = np.exp(-((wave - 4.5) / 1.4)**2)
            lattice_flare = np.where(grid_hex, wave_glow * 75.0 + 12.0, 0.0)
            
            frame[:, :, 0] += lattice_flare * 0.50
            frame[:, :, 1] += lattice_flare * 1.10
            frame[:, :, 2] += lattice_flare * 0.95
            
            for c in range(3):
                frame[:, :, c] = np.where(alpha, np.clip(frame[:, :, c], 0, 255), 0)
            frames.append(frame.astype(np.uint8))
            
    elif mat_name == "draconium":
        colored_rgb = palette_draconium(gray)
        colored = np.zeros_like(base_arr)
        colored[:, :, :3] = colored_rgb
        colored[:, :, 3] = base_arr[:, :, 3]
        
        for f in range(n_frames):
            frame = colored.copy()
            t = f / n_frames
            
            # Void dragon heart core breathing
            pulse = np.sin(2 * np.pi * t * 2.0) ** 4
            core_flare = np.exp(-dist / 4.2) * pulse * 90.0
            
            # Dark draconic energy ripple
            ripple = np.sin(2 * np.pi * (t * 2.0 - dist / 5.0)) * 25.0 * (t_base > 0.4)
            
            frame[:, :, 0] += (core_flare + ripple) * 0.95
            frame[:, :, 1] += (core_flare + ripple) * 0.25
            frame[:, :, 2] += (core_flare + ripple) * 1.25
            
            for c in range(3):
                frame[:, :, c] = np.where(alpha, np.clip(frame[:, :, c], 0, 255), 0)
            frames.append(frame.astype(np.uint8))
            
    elif mat_name == "awakened_draconium":
        colored_rgb = palette_awakened_draconium(gray)
        colored = np.zeros_like(base_arr)
        colored[:, :, :3] = colored_rgb
        colored[:, :, 3] = base_arr[:, :, 3]
        
        for f in range(n_frames):
            frame = colored.copy()
            t = f / n_frames
            
            # Violent churning solar dragon plasma fire
            flame1 = np.sin(2 * np.pi * (t * 3.0 + x_coords * 0.8 - y_coords * 0.5))
            flame2 = np.cos(2 * np.pi * (t * 4.0 - x_coords * 0.6 + y_coords * 0.9))
            turbulent_fire = (flame1 * flame2 * 0.5 + 0.5) ** 2 * 80.0
            
            # Core supernova eruption
            eruption = (np.sin(2 * np.pi * (t * 2.0 + dist / 4.0)) ** 8) * 95.0 * (t_base > 0.4)
            
            frame[:, :, 0] += (turbulent_fire + eruption) * 1.15
            frame[:, :, 1] += (turbulent_fire + eruption) * 0.85
            frame[:, :, 2] += (turbulent_fire + eruption) * 0.20
            
            for c in range(3):
                frame[:, :, c] = np.where(alpha, np.clip(frame[:, :, c], 0, 255), 0)
            frames.append(frame.astype(np.uint8))
            
    elif mat_name == "cosmic_neutronium":
        colored_rgb = palette_cosmic_neutronium(gray)
        colored = np.zeros_like(base_arr)
        colored[:, :, :3] = colored_rgb
        colored[:, :, 3] = base_arr[:, :, 3]
        
        # Dense constellation star seeds
        valid_coords = np.argwhere((alpha) & (t_base > 0.35))
        np.random.seed(999)
        star_pts = [valid_coords[i % len(valid_coords)] for i in [3, 14, 25, 41, 58, 72, 85]] if len(valid_coords) > 90 else []
        star_phases = [0.0, 0.15, 0.32, 0.48, 0.65, 0.80, 0.92]
        star_colors = [
            (255, 120, 180), # Magenta pink
            (120, 220, 255), # Cyan star
            (255, 230, 140), # Gold star
            (180, 140, 255), # Violet star
            (140, 255, 200), # Emerald star
            (255, 255, 255), # Diamond white
            (255, 160, 120)  # Coral orange
        ]
        
        for f in range(n_frames):
            frame = colored.copy()
            t = f / n_frames
            
            # Subtle gravitational microlensing shimmer
            lensing = np.sin(2 * np.pi * (t * 1.5 + dist / 5.0)) * 12.0
            frame[:, :, 0] += lensing * 0.6
            frame[:, :, 1] += lensing * 0.8
            frame[:, :, 2] += lensing * 1.2
            
            for (sy, sx), sp, scol in zip(star_pts, star_phases, star_colors):
                glint = max(0.0, np.cos(((t - sp) % 1.0) * 2 * np.pi)) ** 8
                if glint > 0.05:
                    for dy, dx, weight in [(0, 0, 1.0), (0, 1, 0.4), (0, -1, 0.4), (1, 0, 0.4), (-1, 0, 0.4)]:
                        ny, nx = sy + dy, sx + dx
                        if 0 <= ny < h and 0 <= nx < w and alpha[ny, nx]:
                            v = glint * weight
                            frame[ny, nx, 0] += v * scol[0]
                            frame[ny, nx, 1] += v * scol[1]
                            frame[ny, nx, 2] += v * scol[2]
                            
            for c in range(3):
                frame[:, :, c] = np.where(alpha, np.clip(frame[:, :, c], 0, 255), 0)
            frames.append(frame.astype(np.uint8))
            
    return frames

def save_sample_gif(mat_name, item_name="ingot"):
    im_path = WD_ITEMS / f"{item_name}.png"
    im = Image.open(im_path)
    frames = generate_animation_frames(im, mat_name)
    
    pil_frames = []
    scale = 6
    w = 16
    for f in frames:
        img = Image.fromarray(f, mode="RGBA")
        bg = Image.new("RGBA", (w, w), (14, 18, 28, 255))
        bg.paste(img, (0, 0), img)
        scaled = bg.resize((w * scale, w * scale), Image.Resampling.NEAREST)
        pil_frames.append(scaled)
        
    out_path = OUT_DIR / f"{mat_name}_{item_name}.gif"
    pil_frames[0].save(out_path, format="GIF", save_all=True, append_images=pil_frames[1:], duration=66, loop=0)
    print(f"Saved: {out_path}")

materials = [
    "echoite", "universium", "ichorium",
    "tengam_purified", "tengam_attuned",
    "fallking", "odyssey",
    "draconium", "awakened_draconium", "cosmic_neutronium"
]

for m in materials:
    save_sample_gif(m, "ingot")
print("Done generating all sample GIFs!")
