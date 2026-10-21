#!/usr/bin/env python3
"""Graviton-Tier Procedural Mathematical Texture Generator for GTNA Endgame Items:
  1. Target Cartridge (Cartucho de Alvo - Lança Cinética Orbital)
  2. Contained Particles & Penning Traps (Anel Colisor de Antimatéria)
  3. Rift Probe (Sonda de Fenda - Portão de Fenda Dimensional)
  4. Depth Anchor (Âncora de Profundidade - Portão de Fenda Dimensional)
  5. Rift Singularity (Singularidade de Fenda - Portão de Fenda Dimensional)

Uses the exact same mathematical/physics shader engine as 'graviton_anomaly':
  - NumPy coordinate grid ray-marching & Signed Distance Fields (SDF)
  - Directional Phong lighting models with surface normals
  - Relativistic Doppler beaming & logarithmic spiral accretion disks
  - Spacetime gravitational ripples & Einstein lensing rings
  - Gyroscopic quantum probability wave rings & electric arc discharges
  - 16-frame buttery-smooth animated GIFs, 64x1024 vertical spritesheets, and .mcmeta files

Outputs to: tools/design/item_proposals/<category>/
"""

import math
import os
import numpy as np
from PIL import Image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROPOSALS_DIR = os.path.join(BASE_DIR, 'item_proposals')
NUM_FRAMES = 16

def save_transparent_gif(frames, out_path, duration=80):
    """Saves a list of RGBA PIL Images as a properly formatted transparent animated GIF."""
    p_frames = []
    for f in frames:
        alpha = f.split()[3]
        mask = Image.eval(alpha, lambda a: 255 if a < 16 else 0)
        rgb = f.convert('RGB')
        p_frame = rgb.convert('P', palette=Image.ADAPTIVE, colors=254)
        p_frame.paste(255, mask)
        p_frame.info['transparency'] = 255
        p_frames.append(p_frame)
        
    p_frames[0].save(
        out_path,
        save_all=True,
        append_images=p_frames[1:],
        duration=duration,
        loop=0,
        disposal=2,
        transparency=255
    )

def save_spritesheet_and_meta(frames, png_path, mcmeta_path, frametime=2):
    """Saves a vertical strip PNG (size x (size * num_frames)) and Minecraft .mcmeta."""
    size = frames[0].width
    strip = Image.new('RGBA', (size, size * len(frames)))
    for idx, f in enumerate(frames):
        strip.paste(f, (0, idx * size))
    strip.save(png_path)
    
    with open(mcmeta_path, 'w', encoding='utf-8') as mf:
        mf.write('{\n  "animation": {\n    "frametime": %d,\n    "interpolate": true\n  }\n}\n' % frametime)

# ===========================================================================
# 1. TARGET CARTRIDGE (64x64, 16 frames)
# ===========================================================================
def create_target_cartridge_shader(size=64, num_frames=16, body_color=(0, 240, 255)):
    """Avionics Tactical Module:
    - Machined Duranium/Naquadah chassis with Phong directional lighting
    - Recessed circular optical targeting screen with coordinate crosshairs
    - Rotating radar scanline beam & pulsing laser reticle
    - Gold PCB interface edge connector pins
    - Animated telemetry LED sequence."""
    frames = []
    cx, cy = (size - 1) / 2.0, (size - 1) / 2.0
    y_coords, x_coords = np.mgrid[:size, :size].astype(np.float32)
    dx = x_coords - cx
    dy = y_coords - cy
    
    for f in range(num_frames):
        phase = (f / num_frames) * 2 * math.pi
        arr = np.zeros((size, size, 4), dtype=np.float32)
        
        # --- A. Outer Chassis (Chamfered Tech Rectangle) ---
        # Bounds: x in [-20, 20], y in [-23, 21]
        x_min, x_max = -20.0, 20.0
        y_min, y_max = -23.0, 21.0
        
        # Distance to box edges
        in_x = (dx >= x_min) & (dx <= x_max)
        in_y = (dy >= y_min) & (dy <= y_max)
        
        # Upper chamfer cuts: cut if (dx + dy) or (-dx + dy) exceed limit at top
        chamfer = 6.0
        c1 = (dx - x_min) + (dy - y_min) >= chamfer # Top-left
        c2 = (x_max - dx) + (dy - y_min) >= chamfer # Top-right
        
        chassis_m = in_x & in_y & c1 & c2
        
        # Directional Lighting (-1, -1) from top-left
        # Calculate surface normal based on edge proximity
        d_left = np.maximum(0.0, dx - x_min)
        d_right = np.maximum(0.0, x_max - dx)
        d_top = np.maximum(0.0, dy - y_min)
        d_bot = np.maximum(0.0, y_max - dy)
        
        nx = np.where(d_left < 3.0, -1.0, np.where(d_right < 3.0, 1.0, 0.0))
        ny = np.where(d_top < 3.0, -1.0, np.where(d_bot < 3.0, 1.0, 0.0))
        dot_l = -(nx * 0.707 + ny * 0.707)
        
        # Machined Cobalt-Duranium Alloy palette
        # Highlight: #7b8fa8, Base: #2d2640, Shadow: #140e22
        ch_r = np.clip(45.0 + 35.0 * dot_l, 18, 160)
        ch_g = np.clip(38.0 + 30.0 * dot_l, 14, 150)
        ch_b = np.clip(62.0 + 45.0 * dot_l, 25, 195)
        
        arr[chassis_m, 0] = ch_r[chassis_m]
        arr[chassis_m, 1] = ch_g[chassis_m]
        arr[chassis_m, 2] = ch_b[chassis_m]
        arr[chassis_m, 3] = 255.0
        
        # Outer dark silhouette border
        edge_dist = np.minimum(np.minimum(d_left, d_right), np.minimum(d_top, d_bot))
        out_border = chassis_m & (edge_dist < 1.0)
        arr[out_border, 0] = 16.0
        arr[out_border, 1] = 10.0
        arr[out_border, 2] = 24.0
        
        # --- B. Gold PCB Interface Connector Pins (Bottom: y in [21, 26]) ---
        for pin_x in range(-16, 17, 5):
            pin_m = (dx >= pin_x) & (dx <= pin_x + 2.5) & (dy >= 21.0) & (dy <= 26.5)
            arr[pin_m, 0] = 255.0 # Radiant gold
            arr[pin_m, 1] = 215.0
            arr[pin_m, 2] = 75.0
            arr[pin_m, 3] = 255.0
            
            # Shiny pin highlight
            arr[pin_m & (dx <= pin_x + 0.8), 0] = 255.0
            arr[pin_m & (dx <= pin_x + 0.8), 1] = 245.0
            arr[pin_m & (dx <= pin_x + 0.8), 2] = 180.0
            
        # --- C. Recessed Circular Targeting Lens / Screen ---
        sc_cy = -2.5
        s_dist = np.sqrt(dx**2 + (dy - sc_cy)**2)
        s_r = 13.5
        
        screen_m = s_dist <= s_r
        # Dark cosmic viewport glass
        arr[screen_m, 0] = 12.0
        arr[screen_m, 1] = 8.0
        arr[screen_m, 2] = 22.0
        arr[screen_m, 3] = 255.0
        
        # Screen Bezel Ring (Machined naquadah gold & chrome)
        bezel_m = (s_dist >= s_r - 1.5) & (s_dist <= s_r)
        arr[bezel_m, 0] = 210.0
        arr[bezel_m, 1] = 170.0
        arr[bezel_m, 2] = 50.0
        arr[bezel_m, 3] = 255.0
        
        # --- D. Rotating Holographic Targeting Reticle ---
        s_ang = np.arctan2(dy - sc_cy, dx)
        
        # Outer reticle ring (r = 10.0) with 8 vernier ticks
        r1_m = screen_m & (np.abs(s_dist - 10.0) < 0.65)
        # Inner reticle ring (r = 5.5)
        r2_m = screen_m & (np.abs(s_dist - 5.5) < 0.65)
        
        reticle_m = r1_m | r2_m
        arr[reticle_m, 0] = body_color[0] * 0.8
        arr[reticle_m, 1] = body_color[1] * 0.8
        arr[reticle_m, 2] = body_color[2] * 0.8
        
        # Rotating Radar Sweep Beam (2x speed)
        radar_ang = phase * 2.0
        ang_diff = (s_ang - radar_ang) % (2 * math.pi)
        sweep_m = screen_m & (s_dist < 10.0) & (ang_diff < math.pi * 0.65)
        sweep_int = np.clip(1.0 - ang_diff / (math.pi * 0.65), 0, 1) ** 2.0
        
        arr[sweep_m, 0] = np.clip(arr[sweep_m, 0] + body_color[0] * sweep_int[sweep_m] * 0.75, 0, 255)
        arr[sweep_m, 1] = np.clip(arr[sweep_m, 1] + body_color[1] * sweep_int[sweep_m] * 0.75, 0, 255)
        arr[sweep_m, 2] = np.clip(arr[sweep_m, 2] + body_color[2] * sweep_int[sweep_m] * 0.75, 0, 255)
        
        # Pulsing Cardinal Crosshair Lines
        cross_pulse = 0.8 + 0.3 * math.sin(phase * 3.0)
        c_line_x = screen_m & (np.abs(dy - sc_cy) < 0.65) & (s_dist < 11.5) & (s_dist > 1.5)
        c_line_y = screen_m & (np.abs(dx) < 0.65) & (s_dist < 11.5) & (s_dist > 1.5)
        cross_m = c_line_x | c_line_y
        arr[cross_m, 0] = np.clip(body_color[0] * cross_pulse, 0, 255)
        arr[cross_m, 1] = np.clip(body_color[1] * cross_pulse, 0, 255)
        arr[cross_m, 2] = np.clip(body_color[2] * cross_pulse, 0, 255)
        
        # White-Hot Central Lock Core
        lock_m = s_dist < 1.4
        arr[lock_m, 0] = 255.0
        arr[lock_m, 1] = 255.0
        arr[lock_m, 2] = 255.0
        
        # Specular Curved Glass Glare across screen (Diagonal curved glare streak)
        glare_line = screen_m & (np.abs(dx + (dy - sc_cy) + 4.0) < 1.0) & (dy - sc_cy < 4.0)
        arr[glare_line, 0] = np.clip(arr[glare_line, 0] + 120.0, 0, 255)
        arr[glare_line, 1] = np.clip(arr[glare_line, 1] + 150.0, 0, 255)
        arr[glare_line, 2] = np.clip(arr[glare_line, 2] + 200.0, 0, 255)
        
        # --- E. Lateral Telemetry LED Cluster ---
        # 3 LEDs on right flank: x in [15, 17], y = -14, -6, 2
        led_y_positions = [-14.0, -6.0, 2.0]
        led_colors = [
            (80.0, 255.0, 140.0), # Green (Sync OK)
            (0.0, 240.0, 255.0),  # Cyan (Data Bus)
            (255.0, 215.0, 80.0)  # Amber (Tracking)
        ]
        for l_idx, ly in enumerate(led_y_positions):
            l_dist = np.sqrt((dx - 16.0)**2 + (dy - ly)**2)
            l_pulse = 0.75 + 0.35 * math.sin(phase * 2.0 + l_idx * 1.5)
            l_m = l_dist < 1.5
            arr[l_m, 0] = np.clip(led_colors[l_idx][0] * l_pulse, 0, 255)
            arr[l_m, 1] = np.clip(led_colors[l_idx][1] * l_pulse, 0, 255)
            arr[l_m, 2] = np.clip(led_colors[l_idx][2] * l_pulse, 0, 255)
            arr[l_m, 3] = 255.0
            
        img_data = np.clip(arr, 0, 255).astype(np.uint8)
        frames.append(Image.fromarray(img_data, mode="RGBA"))
        
    return frames

# ===========================================================================
# 2. CONTAINED PARTICLES (64x64, 16 frames)
# ===========================================================================
def create_contained_particle_shader(size=64, num_frames=16, p_core_col=(0, 240, 255), p_glow_col=(180, 50, 255), is_dewar=False):
    """Cryogenic Penning Trap Capsule:
    - Superconducting magnetic endcaps (top/bottom) with copper/gold windings
    - Central hyperbolic quadrupole electrostatic ring electrode (saddle potential well)
    - Ultra-clear cylindrical quartz vacuum chamber with 3D cylindrical glass reflections
    - Central quantum particle with relativistic probability wave rings, pulsing nucleus, and electric arc discharges."""
    frames = []
    cx, cy = (size - 1) / 2.0, (size - 1) / 2.0
    y_coords, x_coords = np.mgrid[:size, :size].astype(np.float32)
    dx = x_coords - cx
    dy = y_coords - cy
    dist = np.sqrt(dx**2 + dy**2)
    
    # Chamber dimensions
    cyl_w = 14.5
    cyl_h = 22.0
    
    for f in range(num_frames):
        phase = (f / num_frames) * 2 * math.pi
        arr = np.zeros((size, size, 4), dtype=np.float32)
        
        # --- A. Transparent Vacuum Quartz Tube ---
        tube_m = (np.abs(dx) <= cyl_w) & (np.abs(dy) <= cyl_h)
        # Deep cosmic vacuum background inside tube
        arr[tube_m, 0] = 8.0
        arr[tube_m, 1] = 6.0
        arr[tube_m, 2] = 18.0
        arr[tube_m, 3] = 210.0
        
        # Glass Wall Edges (Outer boundaries)
        glass_edge_l = tube_m & (np.abs(dx + cyl_w) < 1.0)
        glass_edge_r = tube_m & (np.abs(dx - cyl_w) < 1.0)
        arr[glass_edge_l | glass_edge_r, 0] = 60.0
        arr[glass_edge_l | glass_edge_r, 1] = 80.0
        arr[glass_edge_l | glass_edge_r, 2] = 120.0
        arr[glass_edge_l | glass_edge_r, 3] = 255.0
        
        # --- B. Superconducting Endcap Pole Pieces (Top & Bottom) ---
        # Top Endcap: dy <= -17.0
        # Bottom Endcap: dy >= 17.0
        top_cap_m = (np.abs(dx) <= cyl_w + 2.5) & (dy <= -17.0) & (dy >= -cyl_h - 4.0)
        bot_cap_m = (np.abs(dx) <= cyl_w + 2.5) & (dy >= 17.0) & (dy <= cyl_h + 4.0)
        caps_m = top_cap_m | bot_cap_m
        
        # Directional Lighting for Endcaps
        d_nx = dx / (cyl_w + 2.5)
        d_ny = np.where(top_cap_m, -1.0, 1.0)
        dot_c = -(d_nx * 0.707 + d_ny * 0.707)
        
        arr[caps_m, 0] = np.clip(50.0 + 35.0 * dot_c[caps_m], 20, 160)
        arr[caps_m, 1] = np.clip(45.0 + 30.0 * dot_c[caps_m], 18, 150)
        arr[caps_m, 2] = np.clip(70.0 + 45.0 * dot_c[caps_m], 30, 200)
        arr[caps_m, 3] = 255.0
        
        # Copper Solenoid Coil Windings
        coils_top = (np.abs(dx) <= cyl_w + 1.5) & (dy >= -cyl_h - 2.0) & (dy <= -cyl_h + 1.0)
        coils_bot = (np.abs(dx) <= cyl_w + 1.5) & (dy >= cyl_h - 1.0) & (dy <= cyl_h + 2.0)
        arr[coils_top | coils_bot, 0] = 240.0 # Copper-gold
        arr[coils_top | coils_bot, 1] = 160.0
        arr[coils_top | coils_bot, 2] = 40.0
        
        # Hyperbolic Pole Tips Projecting Inward (Electrostatic Potential Peaks)
        tip_top = (dy >= -17.0) & (dy <= -11.0) & (np.abs(dx) <= (17.0 + dy) * 0.7)
        tip_bot = (dy <= 17.0) & (dy >= 11.0) & (np.abs(dx) <= (17.0 - dy) * 0.7)
        tips_m = tip_top | tip_bot
        arr[tips_m, 0] = 210.0 # Polished chrome electrode tips
        arr[tips_m, 1] = 230.0
        arr[tips_m, 2] = 255.0
        arr[tips_m, 3] = 255.0
        
        # Contact Terminal Prongs at Bottom
        for pr_x in [-9.0, 0.0, 9.0]:
            prong = (np.abs(dx - pr_x) <= 1.2) & (dy >= cyl_h + 4.0) & (dy <= cyl_h + 7.5)
            arr[prong, 0] = 255.0
            arr[prong, 1] = 215.0
            arr[prong, 2] = 80.0
            arr[prong, 3] = 255.0
            
        # --- C. Central Hyperbolic Quadrupole Ring Electrode ---
        # Torus lobes at left and right of central chamber (y in [-5, 5])
        left_lobe = ((dx + cyl_w + 0.5)**2 + (dy / 1.3)**2) <= 18.0
        right_lobe = ((dx - cyl_w - 0.5)**2 + (dy / 1.3)**2) <= 18.0
        lobes_m = left_lobe | right_lobe
        arr[lobes_m, 0] = 245.0 # Radiant gold-naquadah alloy
        arr[lobes_m, 1] = 185.0
        arr[lobes_m, 2] = 50.0
        arr[lobes_m, 3] = 255.0
        
        # --- D. Trapped Quantum Particle Core (Center: dx=0, dy=0) ---
        core_r = 4.2 + 0.8 * math.sin(phase * 2.0)
        glow_r = 13.0
        
        c_falloff = np.clip(1.0 - (dist / core_r), 0, 1)
        g_falloff = np.clip(1.0 - (dist / glow_r), 0, 1) ** 1.6
        
        # Dual-Color Radiant Plasma Emission (Base + Secondary Glow)
        glow_r_val = p_glow_col[0] * g_falloff + p_core_col[0] * (c_falloff ** 2.0)
        glow_g_val = p_glow_col[1] * g_falloff + p_core_col[1] * (c_falloff ** 2.0)
        glow_b_val = p_glow_col[2] * g_falloff + p_core_col[2] * c_falloff
        
        apply_glow = tube_m & (g_falloff > 0.04)
        arr[apply_glow, 0] = np.clip(arr[apply_glow, 0] + glow_r_val[apply_glow], 0, 255)
        arr[apply_glow, 1] = np.clip(arr[apply_glow, 1] + glow_g_val[apply_glow], 0, 255)
        arr[apply_glow, 2] = np.clip(arr[apply_glow, 2] + glow_b_val[apply_glow], 0, 255)
        arr[apply_glow, 3] = 255.0
        
        # White-Hot Subatomic Singularity
        hot_m = tube_m & (dist < core_r * 0.42)
        arr[hot_m, 0] = 255.0
        arr[hot_m, 1] = 255.0
        arr[hot_m, 2] = 255.0
        
        # --- E. Rotating Gyroscopic Quantum Wave Rings ---
        # Ring 1
        rx1 = dx * math.cos(phase) - dy * math.sin(phase)
        ry1 = dx * math.sin(phase) + dy * math.cos(phase)
        r1_d = np.abs(np.sqrt((rx1 / 1.6)**2 + (ry1 / 0.65)**2) - 5.5)
        r1_m = tube_m & (r1_d < 0.85)
        
        # Ring 2 (Counter-rotating)
        rx2 = dx * math.cos(-phase + math.pi/2) - dy * math.sin(-phase + math.pi/2)
        ry2 = dx * math.sin(-phase + math.pi/2) + dy * math.cos(-phase + math.pi/2)
        r2_d = np.abs(np.sqrt((rx2 / 1.6)**2 + (ry2 / 0.65)**2) - 5.5)
        r2_m = tube_m & (r2_d < 0.85)
        
        for rm in [r1_m, r2_m]:
            arr[rm, 0] = np.clip(arr[rm, 0] + 60.0, 0, 255)
            arr[rm, 1] = np.clip(arr[rm, 1] + p_core_col[1] * 0.8, 0, 255)
            arr[rm, 2] = np.clip(arr[rm, 2] + 255.0, 0, 255)
            
        # --- F. Specular Cylindrical Glass Reflections ---
        # Sharp highlight stripe on left
        glare_l = tube_m & (np.abs(dx + cyl_w - 3.5) < 0.75) & (np.abs(dy) < cyl_h - 2.0)
        arr[glare_l, 0] = np.clip(arr[glare_l, 0] + 160.0, 0, 255)
        arr[glare_l, 1] = np.clip(arr[glare_l, 1] + 200.0, 0, 255)
        arr[glare_l, 2] = np.clip(arr[glare_l, 2] + 255.0, 0, 255)
        
        # Soft glare stripe on right
        glare_r = tube_m & (np.abs(dx - cyl_w + 4.5) < 0.6) & (np.abs(dy) < cyl_h - 2.0)
        arr[glare_r, 0] = np.clip(arr[glare_r, 0] + 80.0, 0, 255)
        arr[glare_r, 1] = np.clip(arr[glare_r, 1] + 120.0, 0, 255)
        arr[glare_r, 2] = np.clip(arr[glare_r, 2] + 180.0, 0, 255)
        
        # Micro electric arc discharges from electrode to particle
        if f % 3 in [0, 1]:
            arc_phase = (f % 4) * (math.pi / 2.0)
            ex = 12.0 * math.cos(arc_phase)
            ey = 12.0 * math.sin(arc_phase)
            for t in np.linspace(0, 1, 14):
                w_wobble = 1.0 * math.sin(t * math.pi * 3 + phase * 4)
                px = (1 - t) * ex + w_wobble * (-math.sin(arc_phase))
                py = (1 - t) * ey + w_wobble * math.cos(arc_phase)
                ix, iy = int(round(cx + px)), int(round(cy + py))
                if 0 <= ix < size and 0 <= iy < size and tube_m[iy, ix]:
                    arr[iy, ix, 0] = 220.0
                    arr[iy, ix, 1] = 245.0
                    arr[iy, ix, 2] = 255.0
                    arr[iy, ix, 3] = 255.0
                    
        # If Dewar Cell: add heavy reinforced cryogenic exo-ribs
        if is_dewar:
            for rib_y in [-12.0, 12.0]:
                rib_m = (np.abs(dx) <= cyl_w + 3.0) & (np.abs(dy - rib_y) <= 1.5)
                arr[rib_m, 0] = 0.0
                arr[rib_m, 1] = 240.0
                arr[rib_m, 2] = 255.0
                arr[rib_m, 3] = 255.0
                
        img_data = np.clip(arr, 0, 255).astype(np.uint8)
        frames.append(Image.fromarray(img_data, mode="RGBA"))
        
    return frames

# ===========================================================================
# 3. RIFT PROBE (64x64, 16 frames)
# ===========================================================================
def create_rift_probe_shader(size=64, num_frames=16):
    """Deep-Space Dimensional Reconnaissance Probe:
    - Diagonal supersonic needle fuselage with Machined Duranium specular highlights
    - Pulsing tachyon emitter tip with expanding spacetime phase shockwaves
    - 3D rotating gyroscopic gimbal rings (nested celestial astrolabe)
    - Glowing tachyon/chronon core
    - Suborbital ion thruster plume with plasma turbulence."""
    frames = []
    cx, cy = (size - 1) / 2.0, (size - 1) / 2.0
    y_coords, x_coords = np.mgrid[:size, :size].astype(np.float32)
    dx = x_coords - cx
    dy = y_coords - cy
    
    # Rotate coordinates 45 degrees so probe lies along horizontal axis:
    # u is along probe axis (forward = +u), v is transverse
    inv_sqrt2 = 1.0 / math.sqrt(2.0)
    u_coords = (dx - dy) * inv_sqrt2
    v_coords = (dx + dy) * inv_sqrt2
    
    for f in range(num_frames):
        phase = (f / num_frames) * 2 * math.pi
        arr = np.zeros((size, size, 4), dtype=np.float32)
        
        # --- A. Spacetime Tachyon Shockwaves (Expanding Ripples from Tip) ---
        tip_u = 24.0
        dist_tip = np.sqrt((u_coords - tip_u)**2 + v_coords**2)
        wave_tip = np.sin(dist_tip / 2.8 - phase * 2.0)
        rip_m = (dist_tip >= 2.0) & (dist_tip <= 18.0) & (u_coords > 10.0)
        rip_int = np.clip(wave_tip * 0.5 + 0.5, 0, 1) * np.clip(1.0 - dist_tip / 18.0, 0, 1) ** 1.5
        
        arr[rip_m, 0] = np.clip(arr[rip_m, 0] + 0.0 * rip_int[rip_m], 0, 255)
        arr[rip_m, 1] = np.clip(arr[rip_m, 1] + 220.0 * rip_int[rip_m], 0, 255)
        arr[rip_m, 2] = np.clip(arr[rip_m, 2] + 255.0 * rip_int[rip_m], 0, 255)
        arr[rip_m, 3] = np.clip(arr[rip_m, 3] + rip_int[rip_m] * 180.0, 0, 255)
        
        # --- B. Sleek Supersonic Needle Fuselage ---
        # Nose at u = 24.0, Tail at u = -22.0
        fuse_len = 46.0
        in_u = (u_coords >= -22.0) & (u_coords <= 24.0)
        
        # Fuselage profile width along u
        u_norm = np.clip((u_coords + 22.0) / fuse_len, 0, 1)
        # Tapered needle profile
        w_nose = 4.5 * np.maximum(0.0, 1.0 - (u_coords - 8.0) / 16.0)**0.8
        w_tail = 5.2 * np.maximum(0.0, 1.0 - (-12.0 - u_coords) / 10.0)**0.5
        half_w = np.where(u_coords > 8.0, w_nose, np.where(u_coords < -12.0, w_tail, 5.2))
        
        fuse_m = in_u & (np.abs(v_coords) <= half_w)
        
        # Directional Lighting for 3D Cylindrical Fuselage
        v_norm = v_coords / np.maximum(half_w, 1e-4)
        dot_f = -v_norm # Highlights upper flank, shadows lower flank
        
        arr[fuse_m, 0] = np.clip(45.0 + 35.0 * dot_f[fuse_m], 18, 160)
        arr[fuse_m, 1] = np.clip(40.0 + 30.0 * dot_f[fuse_m], 16, 150)
        arr[fuse_m, 2] = np.clip(65.0 + 45.0 * dot_f[fuse_m], 25, 200)
        arr[fuse_m, 3] = 255.0
        
        # Specular Highlight Spine along center of fuselage
        spine_m = fuse_m & (np.abs(v_coords + 0.8) < 0.75)
        arr[spine_m, 0] = np.clip(arr[spine_m, 0] + 120.0, 0, 255)
        arr[spine_m, 1] = np.clip(arr[spine_m, 1] + 150.0, 0, 255)
        arr[spine_m, 2] = np.clip(arr[spine_m, 2] + 210.0, 0, 255)
        
        # --- C. Tachyon Needle Emitter Tip (u in [20, 27]) ---
        tip_m = (u_coords >= 20.0) & (u_coords <= 27.0) & (np.abs(v_coords) <= (27.0 - u_coords) * 0.4)
        arr[tip_m, 0] = 0.0 # Cyan/white tachyon spark
        arr[tip_m, 1] = 240.0
        arr[tip_m, 2] = 255.0
        arr[tip_m, 3] = 255.0
        
        # Blinding Tip Spark
        spark_m = np.sqrt((u_coords - 26.5)**2 + v_coords**2) < 1.8
        arr[spark_m, 0] = 255.0
        arr[spark_m, 1] = 255.0
        arr[spark_m, 2] = 255.0
        arr[spark_m, 3] = 255.0
        
        # --- D. Rotating 3D Gyroscopic Gimbal Rings (Astrolabe around u = 0) ---
        # Outer Gold Ring: radius 12.0, tilted by phase
        cos_p = math.cos(phase)
        sin_p = math.sin(phase)
        
        # Elliptical ring projection around u=0
        ring1_d = np.abs(np.sqrt((u_coords / np.maximum(np.abs(cos_p), 0.15))**2 + v_coords**2) - 12.0)
        ring1_m = (ring1_d < 1.1) & (~fuse_m | (u_coords * cos_p > 0)) # in front of fuselage
        
        arr[ring1_m, 0] = 255.0 # Godforge gold
        arr[ring1_m, 1] = 215.0
        arr[ring1_m, 2] = 75.0
        arr[ring1_m, 3] = 255.0
        
        # Inner Cyan Phase Ring (Orthogonal rotation)
        cos_p2 = math.cos(-phase + math.pi/2)
        ring2_d = np.abs(np.sqrt((u_coords / np.maximum(np.abs(cos_p2), 0.15))**2 + v_coords**2) - 8.5)
        ring2_m = (ring2_d < 0.9) & (~fuse_m | (u_coords * cos_p2 > 0))
        arr[ring2_m, 0] = 0.0 # Cyan phase ring
        arr[ring2_m, 1] = 230.0
        arr[ring2_m, 2] = 255.0
        arr[ring2_m, 3] = 255.0
        
        # --- E. Chronon Reactor Core Window (Center: u = 0, v = 0) ---
        core_dist = np.sqrt(u_coords**2 + v_coords**2)
        core_m = core_dist < 4.2
        arr[core_m, 0] = 180.0 # Pulsing ultraviolet core
        arr[core_m, 1] = 50.0
        arr[core_m, 2] = 255.0
        arr[core_m, 3] = 255.0
        
        # Core Center
        core_hot = core_dist < 1.8
        arr[core_hot, 0] = 255.0
        arr[core_hot, 1] = 255.0
        arr[core_hot, 2] = 255.0
        
        # --- F. Suborbital Ion Thruster Plume (Rear: u < -22) ---
        plume_len = 12.0
        in_plume = (u_coords <= -22.0) & (u_coords >= -22.0 - plume_len)
        plume_w = 4.0 * (1.0 - (-22.0 - u_coords) / plume_len)
        
        wobble = 0.8 * np.sin(u_coords * 1.5 + phase * 4.0)
        plume_m = in_plume & (np.abs(v_coords - wobble) <= plume_w)
        p_falloff = np.clip(1.0 - (-22.0 - u_coords) / plume_len, 0, 1)
        
        arr[plume_m, 0] = np.clip(arr[plume_m, 0] + 0.0, 0, 255)
        arr[plume_m, 1] = np.clip(arr[plume_m, 1] + 230.0 * p_falloff[plume_m], 0, 255)
        arr[plume_m, 2] = np.clip(arr[plume_m, 2] + 255.0 * p_falloff[plume_m], 0, 255)
        arr[plume_m, 3] = np.clip(arr[plume_m, 3] + p_falloff[plume_m] * 240.0, 0, 255)
        
        img_data = np.clip(arr, 0, 255).astype(np.uint8)
        frames.append(Image.fromarray(img_data, mode="RGBA"))
        
    return frames

# ===========================================================================
# 4. DEPTH ANCHOR (64x64, 16 frames)
# ===========================================================================
def create_depth_anchor_shader(size=64, num_frames=16):
    """Gravimetric Mooring Apparatus:
    - Heavy forged Duranium-Naquadah shank with directional metallic lighting
    - Spacetime gravitational distortion waves radiating outward along the mooring shank
    - Quantum flukes with phase-shifting tachyon energy cutting edges
    - Micro-singularity zero-point spatial lock core at the crown with event horizon and lensing."""
    frames = []
    cx, cy = (size - 1) / 2.0, (size - 1) / 2.0
    y_coords, x_coords = np.mgrid[:size, :size].astype(np.float32)
    dx = x_coords - cx
    dy = y_coords - cy
    
    crown_y = 15.0
    for f in range(num_frames):
        phase = (f / num_frames) * 2 * math.pi
        arr = np.zeros((size, size, 4), dtype=np.float32)
        
        # --- A. Spacetime Gravitational Distortion Waves (Radiating from Crown) ---
        dist_crown = np.sqrt(dx**2 + (dy - crown_y)**2)
        wave_g = np.sin(dist_crown / 3.4 - phase * 1.8)
        rip_m = (dist_crown >= 6.0) & (dist_crown <= 26.0)
        rip_int = np.clip(wave_g * 0.5 + 0.5, 0, 1) * np.clip(1.0 - dist_crown / 26.0, 0, 1) ** 1.6
        
        # Deep cosmic void violet and cyan ripples (same as graviton_anomaly!)
        arr[rip_m, 0] = 60.0 * rip_int[rip_m]
        arr[rip_m, 1] = 20.0 * rip_int[rip_m]
        arr[rip_m, 2] = 125.0 * rip_int[rip_m]
        arr[rip_m, 3] = np.clip(rip_int[rip_m] * 210.0, 0, 255)
        
        # --- B. Top Hoist Ring & Stock ---
        # Top ring at dy in [-25, -15]
        ring_cy = -20.0
        r_dist = np.sqrt(dx**2 + (dy - ring_cy)**2)
        ring_m = (r_dist >= 3.0) & (r_dist <= 7.0)
        
        arr[ring_m, 0] = 245.0 # Godforge gold
        arr[ring_m, 1] = 205.0
        arr[ring_m, 2] = 65.0
        arr[ring_m, 3] = 255.0
        
        # Stock (Horizontal crossbeam at dy = -14)
        stock_m = (np.abs(dy + 14.0) <= 2.2) & (np.abs(dx) <= 18.0)
        # Terminal stock endcaps
        end_left = np.sqrt((dx + 18.0)**2 + (dy + 14.0)**2) <= 3.2
        end_right = np.sqrt((dx - 18.0)**2 + (dy + 14.0)**2) <= 3.2
        all_stock = stock_m | end_left | end_right
        
        arr[all_stock, 0] = 50.0
        arr[all_stock, 1] = 40.0
        arr[all_stock, 2] = 68.0
        arr[all_stock, 3] = 255.0
        arr[end_left | end_right, 0] = 255.0 # Gold stock ends
        arr[end_left | end_right, 1] = 215.0
        arr[end_left | end_right, 2] = 75.0
        
        # --- C. Heavy Central Shank (dy in [-14, 15]) ---
        shank_w = 4.2
        shank_m = (np.abs(dx) <= shank_w) & (dy >= -14.0) & (dy <= 15.0)
        
        # Specular directional lighting for shank (Left highlight, right shadow)
        dot_s = -dx / shank_w
        arr[shank_m, 0] = np.clip(45.0 + 35.0 * dot_s[shank_m], 18, 160)
        arr[shank_m, 1] = np.clip(40.0 + 30.0 * dot_s[shank_m], 16, 150)
        arr[shank_m, 2] = np.clip(65.0 + 45.0 * dot_s[shank_m], 25, 200)
        arr[shank_m, 3] = 255.0
        
        # Center gold groove in shank
        groove_m = shank_m & (np.abs(dx) < 1.2)
        arr[groove_m, 0] = 255.0
        arr[groove_m, 1] = 215.0
        arr[groove_m, 2] = 75.0
        
        # --- D. Quantum Anchor Flukes (Curved Arms Sweeping Outward) ---
        # Parabolic arm curve: y_arm = crown_y - a * dx^2
        # Sweeping from (0, crown_y) out to (±22, -2)
        for side in [-1.0, 1.0]:
            # Parametric arm evaluation
            t_vals = np.linspace(0.0, 1.0, 60)
            arm_x = side * (t_vals * 22.0)
            arm_y = crown_y - (t_vals**1.5) * 18.0
            
            for ax, ay in zip(arm_x, arm_y):
                arm_dist = np.sqrt((dx - ax)**2 + (dy - ay)**2)
                arm_pixel = arm_dist < 3.2
                arr[arm_pixel, 0] = 48.0
                arr[arm_pixel, 1] = 42.0
                arr[arm_pixel, 2] = 70.0
                arr[arm_pixel, 3] = 255.0
                
            # Phase-shifting tachyon fluke blades at the tips
            tip_x = side * 22.0
            tip_y = -3.0
            blade_m = (np.abs(dx - tip_x) <= 3.8) & (dy >= tip_y - 6.0) & (dy <= tip_y + 4.0)
            blade_m = blade_m & (dy <= tip_y + 4.0 - np.abs(dx - tip_x) * 1.5)
            arr[blade_m, 0] = 0.0 # Cyan/white tachyon blade
            arr[blade_m, 1] = 240.0
            arr[blade_m, 2] = 255.0
            arr[blade_m, 3] = 255.0
            
            # Energy flow pulse along fluke arms
            for t_idx, (ax, ay) in enumerate(zip(arm_x, arm_y)):
                flow_pulse = math.sin(t_idx * 0.35 - phase * 3.0)
                if flow_pulse > 0.4:
                    e_dist = np.sqrt((dx - ax)**2 + (dy - ay)**2)
                    e_pix = e_dist < 1.4
                    arr[e_pix, 0] = 0.0
                    arr[e_pix, 1] = 240.0
                    arr[e_pix, 2] = 255.0
                    
        # --- E. Micro-Singularity Spatial Lock Core (at Crown: dx=0, dy=15) ---
        r_sing = 3.2
        r_lens = 6.2
        
        # Einstein Lensing Ring
        lens_m = (dist_crown >= r_sing) & (dist_crown <= r_lens)
        lens_int = np.clip(1.0 - np.abs(dist_crown - (r_sing + r_lens) / 2.0) / ((r_lens - r_sing) / 2.0), 0, 1) ** 1.4
        pulse_lens = 0.85 + 0.25 * math.sin(phase * 2.0)
        
        arr[lens_m, 0] = np.clip(arr[lens_m, 0] + 255.0 * lens_int[lens_m] * pulse_lens, 0, 255)
        arr[lens_m, 1] = np.clip(arr[lens_m, 1] + 215.0 * lens_int[lens_m] * pulse_lens, 0, 255)
        arr[lens_m, 2] = np.clip(arr[lens_m, 2] + 75.0 * lens_int[lens_m] * pulse_lens, 0, 255)
        arr[lens_m, 3] = 255.0
        
        # Event Horizon (Zero-Point Void Singularity)
        eh_m = dist_crown < r_sing
        arr[eh_m, 0] = 3.0
        arr[eh_m, 1] = 1.0
        arr[eh_m, 2] = 6.0
        arr[eh_m, 3] = 255.0
        
        img_data = np.clip(arr, 0, 255).astype(np.uint8)
        frames.append(Image.fromarray(img_data, mode="RGBA"))
        
    return frames

# ===========================================================================
# 5. RIFT SINGULARITY (64x64, 16 frames)
# ===========================================================================
def create_rift_singularity_shader(size=64, num_frames=16):
    """Graviton-Anomaly Peer / Showstopper:
    - 3D Tilted logarithmic spiral accretion disk with micro-turbulence
    - Relativistic Doppler beaming (approaching side blueshifted & ultra-bright, receding side redshifted)
    - Einstein lensing ring & pulsating photon sphere
    - Pure void pitch-black event horizon with sharp gravitational shadow
    - Spacetime gravitational wave ripples
    - Dimensional rift lightning fissures cracking open the event horizon into hyper-space
    - Precessing relativistic tachyon quanta."""
    frames = []
    cx, cy = (size - 1) / 2.0, (size - 1) / 2.0
    y_coords, x_coords = np.mgrid[:size, :size].astype(np.float32)
    dx = x_coords - cx
    dy = y_coords - cy
    dist = np.sqrt(dx**2 + dy**2)
    angle = np.arctan2(dy, dx)
    
    r_singularity = 7.0
    r_photon_in = 7.5
    r_photon_out = 12.5
    r_disk_max = 28.5
    
    for f in range(num_frames):
        phase = (f / num_frames) * 2 * math.pi
        arr = np.zeros((size, size, 4), dtype=np.float32)
        
        # --- A. Space-Time Warping Waves (Gravitational Ripples) ---
        ripple = np.sin(dist / 3.2 - phase * 1.8)
        outer_m = (dist <= r_disk_max) & (dist > r_photon_in)
        rip_int = np.clip(ripple * 0.5 + 0.5, 0, 1) * np.clip(1.0 - dist / r_disk_max, 0, 1) ** 1.8
        
        # Deep cosmic void violet & radiant cyan ripples
        arr[outer_m, 0] = 58.0 * rip_int[outer_m]
        arr[outer_m, 1] = 18.0 * rip_int[outer_m]
        arr[outer_m, 2] = 115.0 * rip_int[outer_m]
        arr[outer_m, 3] = np.clip(rip_int[outer_m] * 215.0, 0, 255)
        
        # --- B. Swirling Relativistic Accretion Disk (Tilted 3D Perspective) ---
        tilt_y = dy / 0.58
        tilted_r = np.sqrt(dx**2 + tilt_y**2)
        tilted_ang = np.arctan2(tilt_y, dx)
        
        # Multi-armed Logarithmic Spiral with Micro-Turbulence
        sp_phase = phase
        arm1 = np.sin(2.0 * tilted_ang - 3.4 * np.log(np.maximum(tilted_r / 7.0, 0.1)) + sp_phase)
        arm2 = np.sin(2.0 * tilted_ang - 3.4 * np.log(np.maximum(tilted_r / 7.0, 0.1)) + sp_phase + math.pi)
        
        eddy = 0.15 * np.sin(5.0 * tilted_ang + 2.0 * sp_phase) * np.cos(tilted_r / 2.5)
        spiral_density = np.maximum(arm1, arm2) + eddy
        
        disk_m = (tilted_r >= r_photon_in) & (tilted_r <= r_disk_max) & (dist <= r_disk_max)
        rad_falloff = np.clip(1.0 - (tilted_r - r_photon_in) / (r_disk_max - r_photon_in), 0, 1)
        disk_int = np.clip((spiral_density * 0.5 + 0.5) ** 1.25 * rad_falloff, 0, 1)
        
        # Relativistic Doppler Beaming
        # Left side (dx < 0) moves toward observer: ultra-bright, blueshifted
        # Right side (dx > 0) moves away: dimmer, redshifted
        doppler_boost = 1.0 - 0.45 * (dx / r_disk_max)
        
        # Plasma Temperature Gradient:
        # Inner: Blinding white/cyan (#e0f7ff, #38bdf8) & electric gold
        # Outer: Cosmic violet/magenta (#c77dff, #7b2cbf) & void purple
        disk_r = (255.0 * (rad_falloff**0.6) + 160.0 * (1.0 - rad_falloff)) * doppler_boost
        disk_g = (220.0 * (rad_falloff**1.1) + 40.0 * (1.0 - rad_falloff)) * doppler_boost
        disk_b = (140.0 * (rad_falloff**2.2) + 240.0 * (1.0 - rad_falloff)) * doppler_boost
        
        apply_disk = disk_m & (disk_int > 0.06)
        arr[apply_disk, 0] = np.clip(arr[apply_disk, 0] + disk_r[apply_disk] * disk_int[apply_disk], 0, 255)
        arr[apply_disk, 1] = np.clip(arr[apply_disk, 1] + disk_g[apply_disk] * disk_int[apply_disk], 0, 255)
        arr[apply_disk, 2] = np.clip(arr[apply_disk, 2] + disk_b[apply_disk] * disk_int[apply_disk], 0, 255)
        arr[apply_disk, 3] = np.clip(arr[apply_disk, 3] + disk_int[apply_disk] * 255.0, 0, 255)
        
        # --- C. Photon Sphere & Einstein Lensing Ring ---
        photon_m = (dist >= r_photon_in - 1.0) & (dist <= r_photon_out)
        p_norm = 1.0 - np.abs(dist - (r_photon_in + r_photon_out) / 2.0) / ((r_photon_out - r_photon_in) / 2.0)
        p_int = np.clip(p_norm, 0, 1) ** 1.35
        
        pulse_p = 0.88 + 0.18 * math.sin(phase * 2.0)
        pr = 255.0 * pulse_p
        pg = np.clip(230.0 - 75.0 * (dx / r_photon_out), 110, 255) * pulse_p
        pb = np.clip(170.0 - 150.0 * (dx / r_photon_out), 35, 255) * pulse_p
        
        arr[photon_m, 0] = np.clip(arr[photon_m, 0] + pr * p_int[photon_m], 0, 255)
        arr[photon_m, 1] = np.clip(arr[photon_m, 1] + pg[photon_m] * p_int[photon_m], 0, 255)
        arr[photon_m, 2] = np.clip(arr[photon_m, 2] + pb[photon_m] * p_int[photon_m], 0, 255)
        arr[photon_m, 3] = np.clip(arr[photon_m, 3] + p_int[photon_m] * 255.0, 0, 255)
        
        # --- D. Dimensional Rift Lightning Cracks (Fissures across Spacetime) ---
        for crack_idx in range(4):
            crack_ang = crack_idx * (math.pi / 2.0) + math.pi / 4.0 + 0.2 * math.sin(phase + crack_idx)
            c_cos = math.cos(crack_ang)
            c_sin = math.sin(crack_ang)
            for t_step in np.linspace(r_singularity, r_disk_max * 0.85, 22):
                jag = 1.2 * math.sin(t_step * 1.8 + phase * 3.0 + crack_idx * 2.0)
                px = t_step * c_cos + jag * (-c_sin)
                py = t_step * c_sin + jag * c_cos
                ix, iy = int(round(cx + px)), int(round(cy + py))
                if 0 <= ix < size and 0 <= iy < size:
                    arr[iy, ix, 0] = 0.0 # Blinding electric cyan
                    arr[iy, ix, 1] = 240.0
                    arr[iy, ix, 2] = 255.0
                    arr[iy, ix, 3] = 255.0
                    
        # --- E. Event Horizon (Absolute Singularity Void) ---
        eh_m = dist < r_singularity
        arr[eh_m, 0] = 2.0 # Absolute blackness
        arr[eh_m, 1] = 1.0
        arr[eh_m, 2] = 4.0
        arr[eh_m, 3] = 255.0
        
        # Sharp gravitational shadow boundary
        eh_edge = (dist >= r_singularity - 1.2) & (dist < r_singularity)
        arr[eh_edge, 0] = 14.0
        arr[eh_edge, 1] = 6.0
        arr[eh_edge, 2] = 24.0
        
        # --- F. Orbiting Tachyon Quanta & Relativistic Energy Flares ---
        for i in range(6):
            sp_ang = phase * 1.5 + i * (math.pi / 3.0)
            sp_r = 15.0 + 4.0 * math.sin(phase * 1.2 + i * 1.5)
            sp_x = sp_r * math.cos(sp_ang)
            sp_y = sp_r * 0.58 * math.sin(sp_ang)
            sp_dist = np.sqrt((dx - sp_x)**2 + (dy - sp_y)**2)
            sp_m = (sp_dist < 1.4) & (dist <= r_disk_max)
            
            arr[sp_m, 0] = 255.0
            arr[sp_m, 1] = 255.0
            arr[sp_m, 2] = 255.0
            arr[sp_m, 3] = 255.0
            
        img_data = np.clip(arr, 0, 255).astype(np.uint8)
        frames.append(Image.fromarray(img_data, mode="RGBA"))
        
    return frames

# ===========================================================================
# GENERATION ORCHESTRATOR
# ===========================================================================
def main():
    print(">>> Iniciando GERAÇÃO MATEMÁTICA GRAVITON-TIER (Shaders NumPy Relativísticos)...")
    
    # 1. Target Cartridge
    print("  [1/5] Gerando 'target_cartridge' (16 frames 64x64 animados)...")
    tc_dir = os.path.join(PROPOSALS_DIR, 'target_cartridge')
    tc_frames = create_target_cartridge_shader(64, NUM_FRAMES, body_color=(0, 240, 255))
    save_transparent_gif(tc_frames, os.path.join(tc_dir, 'target_cartridge_64.gif'), duration=80)
    save_spritesheet_and_meta(tc_frames,
                              os.path.join(tc_dir, '64x64', 'target_cartridge_64.png'),
                              os.path.join(tc_dir, '64x64', 'target_cartridge_64.png.mcmeta'))
    print("      -> Salvo: target_cartridge_64.gif e target_cartridge_64.png (strip 64x1024)")
    
    # 2. Contained Particles (Antiproton, Higgs, W-Boson, X-Nexus, Dewar)
    print("  [2/5] Gerando 'contained_particles' (16 frames 64x64 animados)...")
    cp_dir = os.path.join(PROPOSALS_DIR, 'contained_particles')
    # Antiproton
    p_anti_frames = create_contained_particle_shader(64, NUM_FRAMES, (0, 240, 255), (180, 50, 255))
    save_transparent_gif(p_anti_frames, os.path.join(cp_dir, 'contained_antiproton_64.gif'), duration=80)
    save_spritesheet_and_meta(p_anti_frames,
                              os.path.join(cp_dir, '64x64', 'contained_antiproton_64.png'),
                              os.path.join(cp_dir, '64x64', 'contained_antiproton_64.png.mcmeta'))
                              
    # Higgs Boson
    p_higgs_frames = create_contained_particle_shader(64, NUM_FRAMES, (255, 230, 70), (255, 140, 20))
    save_transparent_gif(p_higgs_frames, os.path.join(cp_dir, 'contained_higgs_64.gif'), duration=80)
    save_spritesheet_and_meta(p_higgs_frames,
                              os.path.join(cp_dir, '64x64', 'contained_higgs_64.png'),
                              os.path.join(cp_dir, '64x64', 'contained_higgs_64.png.mcmeta'))
                              
    # X-Nexus
    p_nexus_frames = create_contained_particle_shader(64, NUM_FRAMES, (180, 40, 255), (80, 10, 180))
    save_transparent_gif(p_nexus_frames, os.path.join(cp_dir, 'contained_x_nexus_64.gif'), duration=80)
    save_spritesheet_and_meta(p_nexus_frames,
                              os.path.join(cp_dir, '64x64', 'contained_x_nexus_64.png'),
                              os.path.join(cp_dir, '64x64', 'contained_x_nexus_64.png.mcmeta'))
                              
    # Antiproton Dewar Cell
    dewar_frames = create_contained_particle_shader(64, NUM_FRAMES, (0, 240, 255), (180, 50, 255), is_dewar=True)
    save_transparent_gif(dewar_frames, os.path.join(cp_dir, 'antiproton_cell_64.gif'), duration=80)
    save_spritesheet_and_meta(dewar_frames,
                              os.path.join(cp_dir, '64x64', 'antiproton_cell_64.png'),
                              os.path.join(cp_dir, '64x64', 'antiproton_cell_64.png.mcmeta'))
    print("      -> Salvos: contained_antiproton, contained_higgs, contained_x_nexus, antiproton_cell (GIFs & strips)")

    # 3. Rift Probe
    print("  [3/5] Gerando 'rift_probe' (16 frames 64x64 animados)...")
    rp_dir = os.path.join(PROPOSALS_DIR, 'rift_probe')
    rp_frames = create_rift_probe_shader(64, NUM_FRAMES)
    save_transparent_gif(rp_frames, os.path.join(rp_dir, 'rift_probe_64.gif'), duration=80)
    save_spritesheet_and_meta(rp_frames,
                              os.path.join(rp_dir, '64x64', 'rift_probe_64.png'),
                              os.path.join(rp_dir, '64x64', 'rift_probe_64.png.mcmeta'))
    print("      -> Salvo: rift_probe_64.gif e rift_probe_64.png (strip 64x1024)")

    # 4. Depth Anchor
    print("  [4/5] Gerando 'depth_anchor' (16 frames 64x64 animados)...")
    da_dir = os.path.join(PROPOSALS_DIR, 'depth_anchor')
    da_frames = create_depth_anchor_shader(64, NUM_FRAMES)
    save_transparent_gif(da_frames, os.path.join(da_dir, 'depth_anchor_64.gif'), duration=80)
    save_spritesheet_and_meta(da_frames,
                              os.path.join(da_dir, '64x64', 'depth_anchor_64.png'),
                              os.path.join(da_dir, '64x64', 'depth_anchor_64.png.mcmeta'))
    print("      -> Salvo: depth_anchor_64.gif e depth_anchor_64.png (strip 64x1024)")

    # 5. Rift Singularity
    print("  [5/5] Gerando 'rift_singularity' (16 frames 64x64 animados - RIVAL DO GRAVITON ANOMALY)...")
    rs_dir = os.path.join(PROPOSALS_DIR, 'rift_singularity')
    rs_frames = create_rift_singularity_shader(64, NUM_FRAMES)
    save_transparent_gif(rs_frames, os.path.join(rs_dir, 'rift_singularity_64.gif'), duration=80)
    save_spritesheet_and_meta(rs_frames,
                              os.path.join(rs_dir, '64x64', 'rift_singularity_64.png'),
                              os.path.join(rs_dir, '64x64', 'rift_singularity_64.png.mcmeta'))
    print("      -> Salvo: rift_singularity_64.gif e rift_singularity_64.png (strip 64x1024)")
    
    print(">>> [SUCESSO COMPLETO] Todos os 5 itens foram gerados no padrão exato do Graviton Anomaly!")

if __name__ == '__main__':
    main()
