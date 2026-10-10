import json
import base64
import numpy as np
from PIL import Image
from pathlib import Path

WD_ITEMS = Path("/home/raishxn/Downloads/Modernity-GTNH-2026-09-07/assets/gregtech/textures/items/materialicons/CUSTOM/WhiteDwarfMatter")
WD_BLOCKS = Path("/home/raishxn/Downloads/Modernity-GTNH-2026-09-07/assets/gregtech/textures/blocks/materialicons/CUSTOM/WhiteDwarfMatter")

OUT_DIR = Path("/tmp/universium_candidates")
OUT_DIR.mkdir(parents=True, exist_ok=True)

def palette_universium_base(gray_val):
    t = gray_val / 255.0
    r = np.zeros_like(t)
    g = np.zeros_like(t)
    b = np.zeros_like(t)
    
    # Sombra: Índigo cósmico abissal profundo (#130e2e)
    mask1 = t < 0.4
    s1 = np.clip(t / 0.4, 0, 1)
    r[mask1] = 20 + s1[mask1] * (58 - 20)
    g[mask1] = 12 + s1[mask1] * (38 - 12)
    b[mask1] = 48 + s1[mask1] * (108 - 48)
    
    # Meio-tom: Púrpura cósmica e magenta nebular (#8b3cb5)
    mask2 = (t >= 0.4) & (t < 0.75)
    s2 = np.clip((t - 0.4) / 0.35, 0, 1)
    r[mask2] = 58 + s2[mask2] * (142 - 58)
    g[mask2] = 38 + s2[mask2] * (78 - 38)
    b[mask2] = 108 + s2[mask2] * (195 - 108)
    
    # Realce: Radiação estelar ultra-violeta (#e8c4ff a #ffffff)
    mask3 = t >= 0.75
    s3 = np.clip((t - 0.75) / 0.25, 0, 1)
    r[mask3] = 142 + s3[mask3] * (245 - 142)
    g[mask3] = 78 + s3[mask3] * (210 - 78)
    b[mask3] = 195 + s3[mask3] * (255 - 195)
    
    return np.dstack([r, g, b])


def animate_universium_candidate(base_im, option=1, n_frames=30):
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
    
    colored_rgb = palette_universium_base(gray)
    colored = np.zeros_like(base_arr)
    colored[:, :, :3] = colored_rgb
    colored[:, :, 3] = base_arr[:, :, 3]
    
    frames = []
    
    if option == 1:
        # OPÇÃO 1: Cosmic Event Horizon (Lente Gravitacional Relativística & Anel de Einstein)
        for f in range(n_frames):
            frame = colored.copy()
            t = f / n_frames
            phi = t * 2 * np.pi
            
            # Anel de Einstein pulsante em r ~ 4.2
            r_einstein = 4.2 + 0.6 * np.sin(phi * 2.0)
            einstein_ring = np.exp(-((dist - r_einstein) / 0.8)**2) * 95.0
            
            # Doppler beaming relativístico (rotação rápida do disco de acreção)
            # Lado se aproximando (theta ~ 0 a pi) tem blueshift e maior intensidade
            beaming = (np.cos(theta - phi) * 0.4 + 0.6)
            accretion_glow = einstein_ring * beaming * (0.35 + 0.65 * t_base)
            
            # Radiação Hawking nos limites do horizonte (dist < 2.0)
            hawking = np.exp(-dist / 1.8) * (np.sin(phi * 3.0) ** 2) * 55.0
            
            # Jatos relativísticos bipolares (ao longo do eixo vertical y)
            jet_axis = np.exp(-((x_coords - cx) / 0.9)**2) * (np.abs(y_coords - cy) > 2.5)
            jet_pulse = np.sin(phi * 2.0 - np.abs(y_coords - cy) * 0.8)
            jet_glow = jet_axis * np.maximum(0, jet_pulse) * 65.0
            
            # Cores: Anel com blueshift azul-ciano/violeta elétrico
            frame[:, :, 0] += accretion_glow * 0.65 + hawking * 0.9 + jet_glow * 0.4
            frame[:, :, 1] += accretion_glow * 0.45 + hawking * 0.3 + jet_glow * 0.8
            frame[:, :, 2] += accretion_glow * 1.35 + hawking * 1.2 + jet_glow * 1.4
            
            for c in range(3):
                frame[:, :, c] = np.where(alpha, np.clip(frame[:, :, c], 0, 255), 0)
            frames.append(frame.astype(np.uint8))
            
    elif option == 2:
        # OPÇÃO 2: Polychromatic Prismatic Shifting (Dispersão Prismática & Cáusticas de Cristal Cósmico)
        for f in range(n_frames):
            frame = colored.copy()
            t = f / n_frames
            
            # Facetas prismáticas poligonais baseadas em grades triangulares
            facet1 = np.sin((x_coords * 0.8 + y_coords * 0.46) + t * 2 * np.pi)
            facet2 = np.sin((x_coords * 0.8 - y_coords * 0.46) - t * 2 * np.pi)
            facet3 = np.cos(y_coords * 0.92 + t * 4 * np.pi)
            
            # Aberração cromática: dispersão espectral separada para R, G, B
            caustic_r = (np.maximum(0, facet1) ** 3) * 85.0
            caustic_g = (np.maximum(0, facet2) ** 3) * 75.0
            caustic_b = (np.maximum(0, facet3) ** 3) * 110.0
            
            # Cintilação nas arestas de corte cristalino
            edge_glint = (np.abs(facet1 * facet2 * facet3) < 0.05) * 50.0 * (t_base > 0.4)
            
            # Refração interna brilhante
            frame[:, :, 0] += (caustic_r + edge_glint) * (0.3 + 0.7 * t_base)
            frame[:, :, 1] += (caustic_g + edge_glint) * (0.3 + 0.7 * t_base)
            frame[:, :, 2] += (caustic_b + edge_glint) * (0.3 + 0.7 * t_base)
            
            for c in range(3):
                frame[:, :, c] = np.where(alpha, np.clip(frame[:, :, c], 0, 255), 0)
            frames.append(frame.astype(np.uint8))
            
    elif option == 3:
        # OPÇÃO 3: Galactic Spiral Arm Collision (Fusão de Galáxias & Berçários Starburst)
        for f in range(n_frames):
            frame = colored.copy()
            t = f / n_frames
            
            # Curva de rotação galáctica diferencial (centro mais rápido, borda mais lenta)
            omega = 3.5 / (dist + 2.0)
            spiral_angle = (theta - omega * t * 2 * np.pi) % np.pi
            
            # Dois braços espirais logarítmicos
            arm_shape = np.sin(2.0 * spiral_angle - np.log(dist + 1.0) * 2.2)
            arm_glow = (np.maximum(0, arm_shape) ** 3) * 80.0 * (0.4 + 0.6 * t_base)
            
            # Berçários estelares (starburst knots) pontuais ao longo dos braços
            knots = np.sin(spiral_angle * 4.0 + dist * 1.5 - t * 6 * np.pi) ** 14 * 95.0 * (dist > 1.5)
            
            # Núcleo galáctico denso pulsante
            core = np.exp(-dist / 2.5) * (np.sin(2 * np.pi * t * 2.0) * 0.4 + 0.6) * 70.0
            
            total_galactic = arm_glow + knots + core
            frame[:, :, 0] += total_galactic * 0.85
            frame[:, :, 1] += total_galactic * 0.55
            frame[:, :, 2] += total_galactic * 1.30
            
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
    frames = animate_universium_candidate(im, option=option)
    
    pil_frames = []
    scale = 6
    w = 16
    for f in frames:
        img = Image.fromarray(f, mode="RGBA")
        bg = Image.new("RGBA", (w, w), (14, 12, 28, 255))
        bg.paste(img, (0, 0), img)
        scaled = bg.resize((w * scale, w * scale), Image.Resampling.NEAREST)
        pil_frames.append(scaled)
        
    out_path = OUT_DIR / f"universium_opt{option}_{shape_type}.gif"
    pil_frames[0].save(out_path, format="GIF", save_all=True, append_images=pil_frames[1:], duration=66, loop=0)
    print(f"Generated: {out_path.name}")

for opt in [1, 2, 3]:
    for shape in ["ingot", "plate", "gear", "block"]:
        save_candidate_gif(shape, opt)

print("Universium candidate generation complete!")
