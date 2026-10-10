import json
import base64
import numpy as np
from PIL import Image
from pathlib import Path

WD_ITEMS = Path("/home/raishxn/Downloads/Modernity-GTNH-2026-09-07/assets/gregtech/textures/items/materialicons/CUSTOM/WhiteDwarfMatter")
WD_BLOCKS = Path("/home/raishxn/Downloads/Modernity-GTNH-2026-09-07/assets/gregtech/textures/blocks/materialicons/CUSTOM/WhiteDwarfMatter")

OUT_DIR = Path("/tmp/echoite_candidates")
OUT_DIR.mkdir(parents=True, exist_ok=True)

def palette_echoite(gray_val):
    t = gray_val / 255.0
    r = np.zeros_like(t)
    g = np.zeros_like(t)
    b = np.zeros_like(t)
    
    # Sombra: Sculk abissal escuro (#0a2723 a #13463b)
    mask1 = t < 0.4
    s1 = np.clip(t / 0.4, 0, 1)
    r[mask1] = 9 + s1[mask1] * (22 - 9)
    g[mask1] = 34 + s1[mask1] * (72 - 34)
    b[mask1] = 30 + s1[mask1] * (65 - 30)
    
    # Meio-tom: Teal assinatura do GTNA #26734d
    mask2 = (t >= 0.4) & (t < 0.75)
    s2 = np.clip((t - 0.4) / 0.35, 0, 1)
    r[mask2] = 22 + s2[mask2] * (38 - 22)
    g[mask2] = 72 + s2[mask2] * (145 - 72)
    b[mask2] = 65 + s2[mask2] * (115 - 65)
    
    # Realce: Sculk ciano fluorescente (#00ffd5)
    mask3 = t >= 0.75
    s3 = np.clip((t - 0.75) / 0.25, 0, 1)
    r[mask3] = 38 + s3[mask3] * (110 - 38)
    g[mask3] = 145 + s3[mask3] * (235 - 145)
    b[mask3] = 115 + s3[mask3] * (210 - 115)
    
    return np.dstack([r, g, b])


def animate_echoite_candidate(base_im, option=1, n_frames=30):
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
    theta = np.arctan2(y_coords - cy, x_coords - cx)
    
    colored_rgb = palette_echoite(gray)
    colored = np.zeros_like(base_arr)
    colored[:, :, :3] = colored_rgb
    colored[:, :, 3] = base_arr[:, :, 3]
    
    frames = []
    
    if option == 1:
        # OPÇÃO 1: Sculk Tendrils & Bioluminescência Abissal
        # Raízes vivas que respiram organicamente e se propagam
        for f in range(n_frames):
            frame = colored.copy()
            t = f / n_frames
            
            # Tendrils orgânicos com deformação senoidal
            flow1 = np.sin(x_coords * 0.85 + np.cos(y_coords * 0.95 + t * 2 * np.pi) * 2.2)
            flow2 = np.cos(y_coords * 0.75 - np.sin(x_coords * 1.1 - t * 2 * np.pi) * 2.0)
            tendril_mesh = np.maximum(0, (flow1 * flow2 + 0.3) / 1.3) ** 2
            
            # Respiração bioluminescente suave dos nódulos
            nodule_pulse = np.sin(2 * np.pi * (t + (x_coords * 0.5 - y_coords * 0.4) / 5.0)) * 0.5 + 0.5
            bio_glow = tendril_mesh * (0.35 + 0.65 * nodule_pulse) * (0.3 + 0.7 * t_base) * 75.0
            
            # Cintilação nas pontas dos esporos sculk
            spores = np.sin(2 * np.pi * (t * 2.0 + x_coords * 1.3 + y_coords * 1.7)) ** 10 * 45.0 * (t_base > 0.45)
            
            frame[:, :, 0] += (bio_glow + spores) * 0.15
            frame[:, :, 1] += (bio_glow + spores) * 1.05
            frame[:, :, 2] += (bio_glow + spores) * 0.85
            
            for c in range(3):
                frame[:, :, c] = np.where(alpha, np.clip(frame[:, :, c], 0, 255), 0)
            frames.append(frame.astype(np.uint8))
            
    elif option == 2:
        # OPÇÃO 2: Sonic Boom Resonance & Frequência Acústica
        # Ondas concêntricas de choque acústico de alta velocidade com picos de interferência
        for f in range(n_frames):
            frame = colored.copy()
            t = f / n_frames
            
            # Ondas de choque em expansão ultra-rápida (2 ciclos por loop)
            wave1 = np.sin(2 * np.pi * (dist / 3.2 - t * 2.0))
            wave2 = np.sin(2 * np.pi * (dist / 2.0 - t * 3.0))
            acoustic_interf = ((wave1 * 0.65 + wave2 * 0.35) + 0.2) ** 2
            acoustic_wave = np.clip(acoustic_interf, 0, 1.2) * (t_base > 0.3) * 68.0
            
            # Explosão sônica periódica com pico estéreo
            boom = (np.sin(2 * np.pi * t) ** 14) * np.exp(-dist / 4.5) * 105.0
            
            # Faíscas de alta frequência do estalo acústico
            spark = (np.sin(2 * np.pi * (t * 4.0 + (x_coords + y_coords) * 0.8)) ** 12) * 55.0 * (t_base > 0.5)
            
            total_sonic = acoustic_wave + boom + spark
            frame[:, :, 0] += total_sonic * 0.25
            frame[:, :, 1] += total_sonic * 1.15
            frame[:, :, 2] += total_sonic * 1.10
            
            for c in range(3):
                frame[:, :, c] = np.where(alpha, np.clip(frame[:, :, c], 0, 255), 0)
            frames.append(frame.astype(np.uint8))
            
    elif option == 3:
        # OPÇÃO 3: Soul Ether Vortex (Vórtice Espiral de Almas)
        # Espiral rotativa de almas capturadas fluindo em direção ao núcleo do peito do Warden
        for f in range(n_frames):
            frame = colored.copy()
            t = f / n_frames
            
            # Espiral rotacional logarítmica
            spiral_angle = (theta + dist * 0.85 - t * 2 * np.pi) % (2 * np.pi)
            arms = (np.cos(spiral_angle * 2.0) * 0.5 + 0.5) ** 3
            vortex_glow = arms * np.clip(1.2 - dist / 8.5, 0.2, 1.2) * (0.35 + 0.65 * t_base) * 78.0
            
            # Pulso central do núcleo de almas (ribcage soul core)
            core_pulse = np.exp(-dist / 3.2) * (np.sin(2 * np.pi * t * 2.0) * 0.5 + 0.5) * 80.0
            
            # Almas espectrais viajando na órbita
            soul_orbit = np.sin(spiral_angle * 3.0 + t * 4 * np.pi) ** 8 * 50.0 * (dist > 2.0)
            
            total_vortex = vortex_glow + core_pulse + soul_orbit
            frame[:, :, 0] += total_vortex * 0.10
            frame[:, :, 1] += total_vortex * 0.95
            frame[:, :, 2] += total_vortex * 1.25  # Mais puxado pro azul/cyan espectral de alma
            
            for c in range(3):
                frame[:, :, c] = np.where(alpha, np.clip(frame[:, :, c], 0, 255), 0)
            frames.append(frame.astype(np.uint8))
            
    return frames


def save_candidate_gif(shape_type="ingot", option=1):
    if shape_type in ["block", "frame_gt"]:
        src_path = WD_BLOCKS / ("block1.png" if shape_type == "block" else "frameGt.png")
    else:
        src_map = {"ingot": "ingot.png", "plate": "plate.png", "gear": "gearGt.png"}
        src_path = WD_ITEMS / src_map[shape_type]
        
    im = Image.open(src_path)
    frames = animate_echoite_candidate(im, option=option)
    
    pil_frames = []
    scale = 6
    w = 16
    for f in frames:
        img = Image.fromarray(f, mode="RGBA")
        bg = Image.new("RGBA", (w, w), (11, 20, 24, 255))
        bg.paste(img, (0, 0), img)
        scaled = bg.resize((w * scale, w * scale), Image.Resampling.NEAREST)
        pil_frames.append(scaled)
        
    out_path = OUT_DIR / f"echoite_opt{option}_{shape_type}.gif"
    pil_frames[0].save(out_path, format="GIF", save_all=True, append_images=pil_frames[1:], duration=66, loop=0)
    print(f"Generated: {out_path.name}")

for opt in [1, 2, 3]:
    for shape in ["ingot", "plate", "gear", "block"]:
        save_candidate_gif(shape, opt)

print("Echoite candidate generation complete!")
