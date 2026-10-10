import json
import base64
import numpy as np
from PIL import Image
from pathlib import Path

MOD_DIR = Path("/home/raishxn/Downloads/Modernity-GTNH-2026-09-07/assets/gregtech/textures")
OUT_DIR = Path("/tmp/universium_hybrid_candidates")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Templates:
# Ingot, Plate, Gear from Modernity Universium
# Block from BLOCK_UNIVERSIUM.png

def get_base_and_overlay(shape):
    if shape == "ingot":
        base = Image.open(MOD_DIR / "items/materialicons/CUSTOM/universium/ingot.png").convert("RGBA")
        ov = Image.open(MOD_DIR / "items/materialicons/CUSTOM/universium/ingot_OVERLAY.png").convert("RGBA")
    elif shape == "plate":
        base = Image.open(MOD_DIR / "items/materialicons/CUSTOM/universium/plate.png").convert("RGBA")
        ov = Image.open(MOD_DIR / "items/materialicons/CUSTOM/universium/plate_OVERLAY.png").convert("RGBA")
    elif shape == "gear":
        base = Image.open(MOD_DIR / "items/materialicons/CUSTOM/universium/gearGt.png").convert("RGBA")
        ov = Image.open(MOD_DIR / "items/materialicons/CUSTOM/universium/gearGt_OVERLAY.png").convert("RGBA")
    elif shape == "block":
        base = Image.open(MOD_DIR / "blocks/iconsets/BLOCK_UNIVERSIUM.png").convert("RGBA")
        # Block has no overlay, we generate a subtle bevel overlay from top/left borders
        arr = np.array(base)
        ov_arr = np.zeros_like(arr)
        # Bevel on border pixels
        h, w = arr.shape[:2]
        for y in range(h):
            for x in range(w):
                if (y == 0 or x == 0) and (y < h - 1 and x < w - 1):
                    ov_arr[y, x] = [255, 255, 255, 120]
        ov = Image.fromarray(ov_arr)
    return base, ov


def generate_hybrid_frames(shape, option=1, n_frames=30):
    base_im, ov_im = get_base_and_overlay(shape)
    base_arr = np.array(base_im, dtype=np.float32)
    ov_arr = np.array(ov_im, dtype=np.float32)
    
    h, w = base_arr.shape[:2]
    alpha = base_arr[:, :, 3] > 0
    ov_mask = ov_arr[:, :, 3] > 50
    
    # Centers
    y_coords, x_coords = np.ogrid[:h, :w]
    cy = np.sum(np.where(alpha, y_coords, 0)) / max(1, np.sum(alpha))
    cx = np.sum(np.where(alpha, x_coords, 0)) / max(1, np.sum(alpha))
    dist = np.sqrt((x_coords - cx)**2 + (y_coords - cy)**2)
    theta = np.arctan2(y_coords - cy, x_coords - cx)
    
    # Base cosmic palette from user GTNH screenshot:
    # Deep midnight navy: [23, 35, 67] -> darker core [14, 20, 42], mid navy [25, 38, 75], outer [34, 50, 95]
    # Star colors:
    # Cyan: [80, 220, 210]
    # Teal/blue: [90, 160, 240]
    # Lavender: [180, 160, 255]
    # White: [255, 255, 255]
    
    # Fixed star seeds within shape
    np.random.seed(42 + option * 77)
    valid_coords = np.argwhere(alpha & ~ov_mask)
    n_stars = min(len(valid_coords), 35 if shape != "block" else 55)
    star_idx = np.random.choice(len(valid_coords), n_stars, replace=False)
    
    stars = []
    for idx in star_idx:
        sy, sx = valid_coords[idx]
        s_dist = np.sqrt((sx - cx)**2 + (sy - cy)**2)
        s_theta = np.arctan2(sy - cy, sx - cx)
        s_phase = np.random.uniform(0, 1)
        # Star color category
        cat = np.random.choice(["cyan", "lavender", "blue", "white"], p=[0.35, 0.25, 0.25, 0.15])
        if cat == "cyan":
            color = np.array([85.0, 215.0, 205.0])
        elif cat == "lavender":
            color = np.array([175.0, 150.0, 245.0])
        elif cat == "blue":
            color = np.array([100.0, 170.0, 250.0])
        else:
            color = np.array([255.0, 255.0, 255.0])
        stars.append({
            "pos": (sy, sx),
            "dist": s_dist,
            "theta": s_theta,
            "phase": s_phase,
            "color": color,
            "is_cross": (np.random.rand() < 0.2)
        })

    frames = []
    for f in range(n_frames):
        t = f / n_frames
        
        # 1. Base Navy Space Background
        frame = np.zeros((h, w, 4), dtype=np.float32)
        
        # Radial & spiral gradient
        # Option 1: Galactic Starfield Spiral (suave rotação galáctica de 2 braços)
        # Option 2: Avaritia Cosmic Nebula & Starburst (nebulosa mais brilhante com starbursts em cruz)
        # Option 3: Relativistic Cosmic Core & Keplerian Drift (rotação diferencial rápida no centro)
        
        if option == 1:
            spiral = np.sin(2.0 * theta - dist * 0.45 - t * 2 * np.pi)
            navy_r = 18.0 + (spiral * 0.5 + 0.5) * 14.0
            navy_g = 28.0 + (spiral * 0.5 + 0.5) * 20.0
            navy_b = 58.0 + (spiral * 0.5 + 0.5) * 35.0
            
        elif option == 2:
            spiral1 = np.sin(2.0 * theta - dist * 0.5 - t * 2 * np.pi)
            spiral2 = np.cos(3.0 * theta + dist * 0.3 + t * 2 * np.pi)
            nebula = np.clip(spiral1 * 0.6 + spiral2 * 0.4, -1, 1)
            navy_r = 16.0 + (nebula * 0.5 + 0.5) * 22.0
            navy_g = 24.0 + (nebula * 0.5 + 0.5) * 32.0
            navy_b = 52.0 + (nebula * 0.5 + 0.5) * 55.0
            
        else: # option == 3
            # Keplerian differential rotation
            omega = 1.0 / (dist * 0.3 + 1.0)
            diff_theta = theta - omega * t * 2 * np.pi * 1.5
            core_spiral = np.sin(2.0 * diff_theta - dist * 0.4)
            navy_r = 15.0 + (core_spiral * 0.5 + 0.5) * 18.0 + np.exp(-dist * 0.4) * 20.0
            navy_g = 22.0 + (core_spiral * 0.5 + 0.5) * 28.0 + np.exp(-dist * 0.4) * 30.0
            navy_b = 48.0 + (core_spiral * 0.5 + 0.5) * 45.0 + np.exp(-dist * 0.4) * 60.0

        frame[:, :, 0] = np.where(alpha, navy_r, 0)
        frame[:, :, 1] = np.where(alpha, navy_g, 0)
        frame[:, :, 2] = np.where(alpha, navy_b, 0)
        frame[:, :, 3] = np.where(alpha, 255, 0)

        # 2. Render Rotating / Twinkling Stars
        for star in stars:
            s_dist = star["dist"]
            s_theta = star["theta"]
            s_phase = star["phase"]
            color = star["color"]
            
            if option == 1:
                # Star orbits around center along spiral
                current_theta = s_theta + t * 2 * np.pi * 0.6
                cur_x = int(round(cx + np.cos(current_theta) * s_dist))
                cur_y = int(round(cy + np.sin(current_theta) * s_dist))
                twinkle = 0.55 + 0.45 * np.cos((t - s_phase) * 2 * np.pi * 2)
            elif option == 2:
                # Star fixed in galactic grid but bursts with cosmic flares
                cur_y, cur_x = star["pos"]
                # Flare when spiral wave passes
                sp_wave = np.sin(2.0 * s_theta - s_dist * 0.5 - t * 2 * np.pi)
                twinkle = np.clip(0.3 + 0.7 * (sp_wave * 0.5 + 0.5) ** 3 * (np.cos((t - s_phase) * 2 * np.pi * 3) * 0.5 + 0.5), 0.2, 1.2)
            else: # option == 3
                # Differential Keplerian orbit
                omega = 1.0 / (s_dist * 0.35 + 1.0)
                current_theta = s_theta + omega * t * 2 * np.pi * 1.2
                cur_x = int(round(cx + np.cos(current_theta) * s_dist))
                cur_y = int(round(cy + np.sin(current_theta) * s_dist))
                twinkle = 0.6 + 0.4 * np.cos((t - s_phase) * 2 * np.pi * 3)

            if 0 <= cur_y < h and 0 <= cur_x < w and alpha[cur_y, cur_x] and not ov_mask[cur_y, cur_x]:
                star_rgb = color * twinkle
                frame[cur_y, cur_x, :3] = np.clip(frame[cur_y, cur_x, :3] + star_rgb, 0, 255)
                
                # Cross flare (3x3) for brighter stars
                if star["is_cross"] and twinkle > 0.7:
                    flare_val = star_rgb * 0.35
                    for dy, dx in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        ny, nx = cur_y + dy, cur_x + dx
                        if 0 <= ny < h and 0 <= nx < w and alpha[ny, nx] and not ov_mask[ny, nx]:
                            frame[ny, nx, :3] = np.clip(frame[ny, nx, :3] + flare_val, 0, 255)

        # 3. Superimpose the GTNH White Ridge Overlay
        # pure white #ffffff highlight from GTNH screenshot with metallic sheen
        for y in range(h):
            for x in range(w):
                if ov_mask[y, x]:
                    # Sheen running along the ridge
                    ridge_pos = (x + y) * 0.3
                    if option == 1:
                        glint = 0.85 + 0.15 * np.cos(ridge_pos - t * 2 * np.pi * 2)
                        frame[y, x, 0] = min(255.0, 255.0 * glint)
                        frame[y, x, 1] = min(255.0, 255.0 * glint)
                        frame[y, x, 2] = 255.0
                    elif option == 2:
                        glint = 0.80 + 0.20 * np.cos(ridge_pos - t * 2 * np.pi * 3)
                        # Slight celestial cyan tint on ridge pulse
                        frame[y, x, 0] = min(255.0, 220.0 + 35.0 * glint)
                        frame[y, x, 1] = min(255.0, 240.0 + 15.0 * glint)
                        frame[y, x, 2] = 255.0
                    else:
                        glint = 0.90 + 0.10 * np.cos(ridge_pos * 2.0 - t * 2 * np.pi * 4)
                        frame[y, x, 0] = 255.0
                        frame[y, x, 1] = 255.0
                        frame[y, x, 2] = 255.0

        frames.append(Image.fromarray(np.clip(frame, 0, 255).astype(np.uint8)))

    # Save animated GIF
    gif_path = OUT_DIR / f"universium_hybrid_opt{option}_{shape}.gif"
    frames[0].save(
        gif_path,
        save_all=True,
        append_images=frames[1:],
        duration=70,  # ~14 fps (smooth)
        loop=0,
        disposal=2
    )
    print(f"Generated {gif_path.name}")

if __name__ == "__main__":
    for opt in [1, 2, 3]:
        for sh in ["ingot", "plate", "gear", "block"]:
            generate_hybrid_frames(sh, option=opt)
