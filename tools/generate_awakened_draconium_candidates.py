import os
import math
import numpy as np
from PIL import Image
from pathlib import Path

OUT_DIR = Path("/tmp/awakened_draconium_candidates")
OUT_DIR.mkdir(parents=True, exist_ok=True)

BASE_MODERNITY = Path("/home/raishxn/Downloads/Modernity-GTNH-2026-09-07/assets/gregtech/textures/items/materialicons/CUSTOM/awakeneddraconium")
BLOCK_MODERNITY = Path("/home/raishxn/Downloads/Modernity-GTNH-2026-09-07/assets/gregtech/textures/blocks/materialicons/CUSTOM/awakeneddraconium/block1.png")

# Carrega formas básicas
def get_base_image(shape):
    if shape == "block":
        if BLOCK_MODERNITY.exists():
            return Image.open(BLOCK_MODERNITY).convert("RGBA")
        return Image.new("RGBA", (16, 16), (200, 200, 200, 255))
    
    file_name = f"{shape}.png"
    p = BASE_MODERNITY / file_name
    if p.exists():
        return Image.open(p).convert("RGBA")
    
    # Fallback para shape comum se gearGt
    if shape == "gear":
        p = BASE_MODERNITY / "gearGt.png"
        if p.exists():
            return Image.open(p).convert("RGBA")
            
    return Image.new("RGBA", (16, 16), (200, 200, 200, 255))

# Opção 1: Draconic Core Fusion (Fusão Solar & Arcos Coronais)
def render_option_1(base_arr, n_frames=30):
    h, w = base_arr.shape[:2]
    gray = base_arr[:, :, 0]
    alpha = base_arr[:, :, 3] > 0
    t_base = gray / 255.0
    y_coords, x_coords = np.ogrid[:h, :w]
    
    if np.sum(alpha) > 0:
        cy = np.sum(np.where(alpha, y_coords, 0)) / np.sum(alpha)
        cx = np.sum(np.where(alpha, x_coords, 0)) / np.sum(alpha)
    else:
        cy, cx = h / 2.0, w / 2.0
        
    dist = np.sqrt((x_coords - cx)**2 + (y_coords - cy)**2)
    max_d = max(1.0, np.max(dist[alpha])) if np.sum(alpha) > 0 else 8.0
    norm_dist = dist / max_d

    frames = []
    for f in range(n_frames):
        t = f / n_frames
        
        # Base de metal dracônico bronze/âmbar incandescente
        # Sombra: #380c02, Médio: #942b04, Realce: #d95304
        r = 56.0 + t_base * 170.0
        g = 12.0 + (t_base ** 1.4) * 85.0
        b = 2.0 + (t_base ** 2.2) * 20.0
        
        # 1. Pulso do núcleo térmico central (aquecimento rápido, relaxamento gradual)
        pulse = (np.sin(2 * np.pi * t) * 0.5 + 0.5) ** 1.8
        core_heat = np.exp(-norm_dist * 2.8) * (0.65 + 0.45 * pulse) * (t_base > 0.25)
        
        # 2. Arcos coronais giratórios (loops magnéticos de plasma)
        angle = np.arctan2(y_coords - cy, x_coords - cx)
        coronal_wave1 = np.sin(angle * 2.0 - 2 * np.pi * t * 1.5 + norm_dist * 4.0)
        coronal_loop1 = np.exp(-((coronal_wave1 - 0.7) / 0.35) ** 2) * (norm_dist > 0.2) * (norm_dist < 0.85)
        
        coronal_wave2 = np.cos(angle * 3.0 + 2 * np.pi * t * 2.0 - norm_dist * 3.0)
        coronal_loop2 = np.exp(-((coronal_wave2 - 0.6) / 0.4) ** 2) * (norm_dist > 0.3) * (norm_dist < 0.9)
        
        loops = (coronal_loop1 * 0.6 + coronal_loop2 * 0.4) * (0.5 + 0.5 * t_base)
        
        # 3. Flare estelar transitório (labareda súbita a cada ciclo)
        flare_t = (t * 2.0) % 1.0
        flare_int = (np.sin(np.pi * flare_t) ** 12) * np.exp(-norm_dist * 1.5) * 1.2
        
        # Combinação de iluminação de plasma
        total_plasma = core_heat * 1.3 + loops * 0.85 + flare_int * 0.95
        
        # Adiciona brilho de plasma solar
        r += total_plasma * 180.0
        g += total_plasma * 140.0
        b += total_plasma * 65.0
        
        # Núcleo branco-dourado superaquecido
        white_core = np.clip(total_plasma - 0.9, 0, 1.5) * 120.0
        r += white_core * 0.9
        g += white_core * 0.95
        b += white_core * 0.85
        
        frame = np.zeros((h, w, 4), dtype=np.uint8)
        frame[:, :, 0] = np.clip(np.where(alpha, r, 0), 0, 255)
        frame[:, :, 1] = np.clip(np.where(alpha, g, 0), 0, 255)
        frame[:, :, 2] = np.clip(np.where(alpha, b, 0), 0, 255)
        frame[:, :, 3] = base_arr[:, :, 3]
        frames.append(Image.fromarray(frame))
        
    return frames

# Opção 2: Chaos Dragon Sparking Arcs (Descargas Elétricas e Runas)
def render_option_2(base_arr, n_frames=30):
    h, w = base_arr.shape[:2]
    gray = base_arr[:, :, 0]
    alpha = base_arr[:, :, 3] > 0
    t_base = gray / 255.0
    y_coords, x_coords = np.ogrid[:h, :w]
    
    # Detecção de arestas/chanfros
    gy, gx = np.gradient(gray)
    edge_mag = np.sqrt(gx**2 + gy**2)
    norm_edge = edge_mag / max(1.0, np.max(edge_mag))
    
    frames = []
    # Pontos de âncora para raios estocásticos determinísticos
    np.random.seed(42)
    
    for f in range(n_frames):
        t = f / n_frames
        
        # Base: obsidiana dracônica metálica escura com veios rubi
        r = 38.0 + t_base * 135.0
        g = 6.0 + (t_base ** 1.6) * 45.0
        b = 2.0 + (t_base ** 2.0) * 15.0
        
        # 1. Runas nas arestas e facetas chanfradas
        rune_flow = np.sin(2 * np.pi * (t * 1.5 + (x_coords * 0.4 - y_coords * 0.3))) * 0.5 + 0.5
        runes = (norm_edge ** 1.2) * (0.35 + 0.65 * rune_flow) * (t_base > 0.3)
        
        # 2. Descargas de plasma relampejante entre vértices
        # Fases de relâmpago: rápidos bursts de arco elétrico
        burst1 = (np.sin(2 * np.pi * (t * 3.0)) ** 16)
        burst2 = (np.sin(2 * np.pi * (t * 3.0 + 0.33)) ** 16)
        burst3 = (np.sin(2 * np.pi * (t * 3.0 + 0.66)) ** 16)
        
        # Caminhos dos 3 relâmpagos
        line1 = np.abs((x_coords * 0.8 + y_coords * 0.6) - (6.0 + np.sin(f * 0.8) * 3.0))
        arc1 = np.exp(-(line1 / 0.7)**2) * burst1
        
        line2 = np.abs((x_coords * 0.7 - y_coords * 0.7) - (-1.0 + np.cos(f * 0.9) * 2.5))
        arc2 = np.exp(-(line2 / 0.65)**2) * burst2
        
        line3 = np.abs((y_coords - 7.5) + np.sin(x_coords * 0.8 + f * 0.5) * 1.5)
        arc3 = np.exp(-(line3 / 0.6)**2) * burst3
        
        total_arcs = (arc1 + arc2 + arc3) * (t_base > 0.25)
        
        # 3. Faíscas pontuais nos cantos
        sparks = (np.sin(2 * np.pi * (t * 6.0 + x_coords * 1.2 + y_coords * 1.5)) ** 24) * 0.9 * (t_base > 0.6)
        
        # Aplicação de cores
        # Runas: laranja-fogo intenso (#ff4800)
        r += runes * 165.0
        g += runes * 55.0
        b += runes * 5.0
        
        # Arcos e faíscas: plasma dourado-elétrico com transição para branco
        r += (total_arcs + sparks) * 220.0
        g += (total_arcs + sparks) * 195.0
        b += (total_arcs + sparks) * 110.0
        
        frame = np.zeros((h, w, 4), dtype=np.uint8)
        frame[:, :, 0] = np.clip(np.where(alpha, r, 0), 0, 255)
        frame[:, :, 1] = np.clip(np.where(alpha, g, 0), 0, 255)
        frame[:, :, 2] = np.clip(np.where(alpha, b, 0), 0, 255)
        frame[:, :, 3] = base_arr[:, :, 3]
        frames.append(Image.fromarray(frame))
        
    return frames

# Opção 3: Awakened Dragon Scales (Escamas Vivas & Células Convectivas)
def render_option_3(base_arr, n_frames=30):
    h, w = base_arr.shape[:2]
    gray = base_arr[:, :, 0]
    alpha = base_arr[:, :, 3] > 0
    t_base = gray / 255.0
    y_coords, x_coords = np.ogrid[:h, :w]
    
    # Centros de convecção celular (padrão Voronoi estático com translação dinâmica)
    centers = [
        (4.0, 4.0), (12.0, 3.5), (7.5, 8.0), (3.0, 12.5), (12.5, 12.0), (8.0, 14.5)
    ]
    
    frames = []
    for f in range(n_frames):
        t = f / n_frames
        
        # Base: escamas com tom rico de âmbar rubi e bronze escuro
        r = 45.0 + t_base * 155.0
        g = 10.0 + (t_base ** 1.5) * 60.0
        b = 3.0 + (t_base ** 2.5) * 12.0
        
        # 1. Células convectivas solares (Bénard cells)
        dists = []
        for i, (cx, cy) in enumerate(centers):
            # Pequeno movimento orbital orgânico
            dcx = cx + np.sin(2 * np.pi * (t + i / 6.0)) * 0.8
            dcy = cy + np.cos(2 * np.pi * (t + i / 6.0)) * 0.8
            d = np.sqrt((x_coords - dcx)**2 + (y_coords - dcy)**2)
            dists.append(d)
            
        dists_sorted = np.sort(np.array(dists), axis=0)
        d1 = dists_sorted[0]
        d2 = dists_sorted[1]
        
        # Borda entre células (fissuras de magma em convecção)
        fissure = np.exp(-((d2 - d1) / 0.8)**2) * (0.6 + 0.4 * np.sin(2 * np.pi * (t * 2.0 + d1 * 0.5)))
        
        # Centro das células: magma ascendente superaquecido
        cell_core = np.exp(-d1 / 1.8) * (0.5 + 0.5 * np.cos(2 * np.pi * (t * 1.5 + d1 * 0.8)))
        
        # 2. Varredura especular nas escamas (sweep de luz a 45 graus)
        diag = (x_coords + y_coords) * 0.707
        sweep_pos = (t * 22.0) % 22.0
        specular_sweep = np.exp(-((diag - sweep_pos) / 1.6)**2) * 0.85 * (t_base > 0.4)
        
        # Aplicação de cores
        # Fissuras de magma: laranja vivo incandescente (#ff5500)
        r += fissure * 150.0
        g += fissure * 65.0
        b += fissure * 5.0
        
        # Centros celulares: amarelo-dourado solar (#ffaa00)
        r += cell_core * 175.0
        g += cell_core * 125.0
        b += cell_core * 20.0
        
        # Especular sweep: reflexo de ouro solar puro (#fff0aa)
        r += specular_sweep * 160.0
        g += specular_sweep * 145.0
        b += specular_sweep * 85.0
        
        frame = np.zeros((h, w, 4), dtype=np.uint8)
        frame[:, :, 0] = np.clip(np.where(alpha, r, 0), 0, 255)
        frame[:, :, 1] = np.clip(np.where(alpha, g, 0), 0, 255)
        frame[:, :, 2] = np.clip(np.where(alpha, b, 0), 0, 255)
        frame[:, :, 3] = base_arr[:, :, 3]
        frames.append(Image.fromarray(frame))
        
    return frames

def save_gif(frames, out_path):
    frames[0].save(
        out_path,
        save_all=True,
        append_images=frames[1:],
        duration=50,
        loop=0,
        disposal=2
    )

def main():
    shapes = ["ingot", "plate", "gear", "block"]
    options = [
        (1, "core_fusion", render_option_1),
        (2, "sparking_arcs", render_option_2),
        (3, "dragon_scales", render_option_3),
    ]
    
    for opt_idx, opt_name, renderer in options:
        print(f"Gerando Opção {opt_idx}: {opt_name}...")
        for shape in shapes:
            base_im = get_base_image(shape)
            base_arr = np.array(base_im, dtype=np.float32)
            frames = renderer(base_arr, n_frames=30)
            
            out_file = OUT_DIR / f"awakened_draconium_opt{opt_idx}_{shape}.gif"
            save_gif(frames, out_file)
            print(f"  ✓ {out_file.name}")
            
    print("Todas as opções para Awakened Draconium foram geradas com sucesso!")

if __name__ == "__main__":
    main()
