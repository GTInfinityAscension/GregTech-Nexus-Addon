#!/usr/bin/env python3
import os
import math
import numpy as np
from PIL import Image

OUT_DIR = "/tmp/gtna_items_preview"
os.makedirs(OUT_DIR, exist_ok=True)

NUM_FRAMES = 16

def save_transparent_gif(frames, out_path, duration=80):
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

# -------------------------------------------------------------------------
# GRAVITON ANOMALY (128x128) - Ultra Cinematic Relativistic Singularity
# -------------------------------------------------------------------------
def create_graviton_anomaly_128(num_frames=16):
    size = 128
    frames = []
    cx, cy = 63.5, 63.5
    
    y_coords, x_coords = np.mgrid[:size, :size].astype(np.float32)
    dx = x_coords - cx
    dy = y_coords - cy
    dist = np.sqrt(dx**2 + dy**2)
    angle = np.arctan2(dy, dx)
    
    r_singularity = 15.0 # Event horizon
    r_photon_in = 16.5
    r_photon_out = 26.0
    r_disk_max = 59.0
    
    for f in range(num_frames):
        phase = (f / num_frames) * 2 * math.pi
        arr = np.zeros((size, size, 4), dtype=np.float32)
        
        # 1. Spacetime Gravitational Wave Ripples (Background Distortions)
        wave = np.sin(dist / 6.5 - phase * 1.8)
        outer_m = (dist <= r_disk_max) & (dist > r_photon_in)
        rip_int = np.clip(wave * 0.5 + 0.5, 0, 1) * np.clip(1.0 - dist / r_disk_max, 0, 1) ** 1.8
        
        arr[outer_m, 0] = 60.0 * rip_int[outer_m]
        arr[outer_m, 1] = 18.0 * rip_int[outer_m]
        arr[outer_m, 2] = 120.0 * rip_int[outer_m]
        arr[outer_m, 3] = np.clip(rip_int[outer_m] * 200.0, 0, 255)
        
        # 2. Accretion Disk (3D Tilted Logarithmic Spiral with Relativistic Beaming)
        tilt_y = dy / 0.58
        tilted_r = np.sqrt(dx**2 + tilt_y**2)
        tilted_ang = np.arctan2(tilt_y, dx)
        
        # Multi-armed spiral with micro-turbulence
        sp_phase = phase
        arm1 = np.sin(2.0 * tilted_ang - 3.4 * np.log(np.maximum(tilted_r / 14.0, 0.1)) + sp_phase)
        arm2 = np.sin(2.0 * tilted_ang - 3.4 * np.log(np.maximum(tilted_r / 14.0, 0.1)) + sp_phase + math.pi)
        
        # Micro turbulence eddies
        eddy = 0.15 * np.sin(5.0 * tilted_ang + 2.0 * sp_phase) * np.cos(tilted_r / 4.0)
        spiral_density = np.maximum(arm1, arm2) + eddy
        
        disk_m = (tilted_r >= r_photon_in) & (tilted_r <= r_disk_max) & (dist <= r_disk_max)
        rad_falloff = np.clip(1.0 - (tilted_r - r_photon_in) / (r_disk_max - r_photon_in), 0, 1)
        disk_int = np.clip((spiral_density * 0.5 + 0.5) ** 1.3 * rad_falloff, 0, 1)
        
        # Relativistic Doppler Beaming
        # Left side moves toward observer (bright, blueshifted, x < 0)
        # Right side moves away (dimmer, redshifted, x > 0)
        doppler = 1.0 - 0.45 * (dx / r_disk_max)
        
        # Plasma color gradient:
        # Inner: Blinding white/cyan (#e0f7ff, #38bdf8)
        # Middle: Fiery gold/amber (#ffb703, #fb8500)
        # Outer: Cosmic violet/magenta (#c77dff, #7b2cbf)
        d_r = (255.0 * (rad_falloff**0.55) + 180.0 * (1.0 - rad_falloff)) * doppler
        d_g = (220.0 * (rad_falloff**1.1) + 40.0 * (1.0 - rad_falloff)) * doppler
        d_b = (140.0 * (rad_falloff**2.2) + 240.0 * (1.0 - rad_falloff)) * doppler
        
        apply_disk = disk_m & (disk_int > 0.05)
        arr[apply_disk, 0] = np.clip(arr[apply_disk, 0] + d_r[apply_disk] * disk_int[apply_disk], 0, 255)
        arr[apply_disk, 1] = np.clip(arr[apply_disk, 1] + d_g[apply_disk] * disk_int[apply_disk], 0, 255)
        arr[apply_disk, 2] = np.clip(arr[apply_disk, 2] + d_b[apply_disk] * disk_int[apply_disk], 0, 255)
        arr[apply_disk, 3] = np.clip(arr[apply_disk, 3] + disk_int[apply_disk] * 255.0, 0, 255)
        
        # 3. Photon Sphere & Einstein Lensing Ring
        photon_m = (dist >= r_photon_in - 1.5) & (dist <= r_photon_out)
        p_norm = 1.0 - np.abs(dist - (r_photon_in + r_photon_out) / 2.0) / ((r_photon_out - r_photon_in) / 2.0)
        p_int = np.clip(p_norm, 0, 1) ** 1.3
        
        pulse_p = 0.9 + 0.15 * math.sin(phase * 2.0)
        pr = 255.0 * pulse_p
        pg = np.clip(230.0 - 75.0 * (dx / r_photon_out), 120, 255) * pulse_p
        pb = np.clip(170.0 - 150.0 * (dx / r_photon_out), 35, 255) * pulse_p
        
        arr[photon_m, 0] = np.clip(arr[photon_m, 0] + pr * p_int[photon_m], 0, 255)
        arr[photon_m, 1] = np.clip(arr[photon_m, 1] + pg[photon_m] * p_int[photon_m], 0, 255)
        arr[photon_m, 2] = np.clip(arr[photon_m, 2] + pb[photon_m] * p_int[photon_m], 0, 255)
        arr[photon_m, 3] = np.clip(arr[photon_m, 3] + p_int[photon_m] * 255.0, 0, 255)
        
        # 4. Central Event Horizon (Absolute Singularity Void)
        eh_m = dist < r_singularity
        arr[eh_m, 0] = 2.0
        arr[eh_m, 1] = 1.0
        arr[eh_m, 2] = 4.0
        arr[eh_m, 3] = 255.0
        
        # Sharp gravitational shadow boundary
        eh_edge = (dist >= r_singularity - 2.5) & (dist < r_singularity)
        arr[eh_edge, 0] = 12.0
        arr[eh_edge, 1] = 6.0
        arr[eh_edge, 2] = 22.0
        
        # 5. Orbiting Graviton Quanta & Relativistic Energy Flares (8 particles)
        for i in range(8):
            sp_ang = phase * 1.5 + i * (math.pi / 4.0)
            sp_r = 30.0 + 8.0 * math.sin(phase * 1.2 + i * 1.5)
            sp_x = sp_r * math.cos(sp_ang)
            sp_y = sp_r * 0.58 * math.sin(sp_ang)
            sp_dist = np.sqrt((dx - sp_x)**2 + (dy - sp_y)**2)
            sp_m = (sp_dist < 2.5) & (dist <= r_disk_max)
            
            arr[sp_m, 0] = 255.0
            arr[sp_m, 1] = 245.0
            arr[sp_m, 2] = 190.0
            arr[sp_m, 3] = 255.0
            
        img_data = np.clip(arr, 0, 255).astype(np.uint8)
        frames.append(Image.fromarray(img_data, mode="RGBA"))
        
    return frames


# -------------------------------------------------------------------------
# STABLE BOSON CONTAINMENT UNIT - REDESIGN CONCEPTS
# -------------------------------------------------------------------------

# CONCEPT 1: "Quantum Magnetic Chamber / Tokamak Cell" (Octagonal Industrial Core with Laser Tweezers & Higgs Orb)
def create_boson_redesign_tokamak(size=32, num_frames=16):
    frames = []
    scale = size / 32.0
    cx, cy = (size - 1) / 2.0, (size - 1) / 2.0
    
    y_coords, x_coords = np.mgrid[:size, :size].astype(np.float32)
    dx = x_coords - cx
    dy = y_coords - cy
    dist = np.sqrt(dx**2 + dy**2)
    angle = np.arctan2(dy, dx)
    
    r_outer = 14.5 * scale
    r_inner = 8.5 * scale
    
    for f in range(num_frames):
        phase = (f / num_frames) * 2 * math.pi
        arr = np.zeros((size, size, 4), dtype=np.float32)
        
        # Octagonal / Chamfered Heavy Neutronium Chassis
        # Distance metric for octagonal symmetry: max(|dx|, |dy|, (|dx|+|dy|)/1.3)
        oct_dist = np.maximum(np.maximum(np.abs(dx), np.abs(dy)), (np.abs(dx) + np.abs(dy)) / 1.35)
        
        chassis_m = (oct_dist <= r_outer) & (dist >= r_inner)
        
        # Directional light (-1, -1)
        dot_l = -( (dx / np.maximum(dist, 1e-4)) * 0.707 + (dy / np.maximum(dist, 1e-4)) * 0.707 )
        
        # High-tech gunmetal & dark cobalt-neutronium alloy
        arr[chassis_m, 0] = np.clip(50.0 + 30.0 * dot_l[chassis_m], 20, 140)
        arr[chassis_m, 1] = np.clip(60.0 + 35.0 * dot_l[chassis_m], 25, 160)
        arr[chassis_m, 2] = np.clip(80.0 + 45.0 * dot_l[chassis_m], 35, 200)
        arr[chassis_m, 3] = 255.0
        
        # Outer dark outline
        out_border = (oct_dist <= r_outer) & (oct_dist > r_outer - 1.0 * scale)
        arr[out_border, 0] = 18.0
        arr[out_border, 1] = 20.0
        arr[out_border, 2] = 28.0
        
        # Inner magnetic containment ring rim
        inner_rim = (dist >= r_inner) & (dist < r_inner + 1.2 * scale)
        arr[inner_rim, 0] = 180.0 # Bright polished chrome
        arr[inner_rim, 1] = 210.0
        arr[inner_rim, 2] = 240.0
        
        # 4 Superconducting Magnetic Solenoids (at 0, 90, 180, 270 deg)
        for ang in [0, math.pi/2, math.pi, 3*math.pi/2]:
            coil_x = cx + 11.5 * scale * math.cos(ang)
            coil_y = cy + 11.5 * scale * math.sin(ang)
            c_dist = np.sqrt((x_coords - coil_x)**2 + (y_coords - coil_y)**2)
            c_m = c_dist < 2.8 * scale
            # Gold superconducting coil
            arr[c_m, 0] = 245.0
            arr[c_m, 1] = 185.0
            arr[c_m, 2] = 45.0
            arr[c_m, 3] = 255.0
            
            # Coil center pin
            pin_m = c_dist < 1.1 * scale
            arr[pin_m, 0] = 255.0
            arr[pin_m, 1] = 240.0
            arr[pin_m, 2] = 150.0
            
        # 4 Quantum Emitter Needles pointing inward to the core
        for ang in [0, math.pi/2, math.pi, 3*math.pi/2]:
            nx_arr = cx + np.linspace(r_inner, r_inner - 2.8 * scale, 10) * math.cos(ang)
            ny_arr = cy + np.linspace(r_inner, r_inner - 2.8 * scale, 10) * math.sin(ang)
            for px, py in zip(nx_arr, ny_arr):
                ix, iy = int(round(px)), int(round(py))
                if 0 <= ix < size and 0 <= iy < size:
                    arr[iy, ix, 0] = 220.0
                    arr[iy, ix, 1] = 240.0
                    arr[iy, ix, 2] = 255.0
                    arr[iy, ix, 3] = 255.0
                    
        # Status LEDs on the 4 corners
        led_pulse = 0.7 + 0.3 * math.sin(phase)
        for ang in [math.pi/4, 3*math.pi/4, 5*math.pi/4, 7*math.pi/4]:
            lx = cx + 12.0 * scale * math.cos(ang)
            ly = cy + 12.0 * scale * math.sin(ang)
            l_dist = np.sqrt((x_coords - lx)**2 + (y_coords - ly)**2)
            l_m = l_dist < 1.3 * scale
            arr[l_m, 0] = 20.0 * led_pulse
            arr[l_m, 1] = 255.0 * led_pulse
            arr[l_m, 2] = 180.0 * led_pulse
            arr[l_m, 3] = 255.0
            
        # Vacuum Confinement Chamber (Inside r_inner)
        cham_m = dist < r_inner
        arr[cham_m, 0] = 10.0 # Deep cosmic space inside chamber
        arr[cham_m, 1] = 15.0
        arr[cham_m, 2] = 30.0
        arr[cham_m, 3] = 230.0
        
        # THE CAPTURED HIGGS / VECTOR BOSON (Pulsing Energy Orb & Quantum Lattice)
        b_pulse = 0.85 + 0.3 * math.sin(phase * 2.0)
        b_r = (3.6 + 0.8 * math.sin(phase)) * scale
        b_glow_r = 7.5 * scale
        
        b_int = np.clip(1.0 - (dist / b_r), 0, 1)
        g_int = np.clip(1.0 - (dist / b_glow_r), 0, 1) ** 1.5
        
        # Radiant Cyan/Teal to Ultraviolet Quantum Glow
        glow_r = 80.0 * g_int + 255.0 * (b_int ** 2.0)
        glow_g = 220.0 * g_int + 255.0 * (b_int ** 2.0)
        glow_b = 255.0 * g_int + 255.0 * b_int
        
        apply_g = cham_m & (g_int > 0.05)
        arr[apply_g, 0] = np.clip(arr[apply_g, 0] + glow_r[apply_g], 0, 255)
        arr[apply_g, 1] = np.clip(arr[apply_g, 1] + glow_g[apply_g], 0, 255)
        arr[apply_g, 2] = np.clip(arr[apply_g, 2] + glow_b[apply_g], 0, 255)
        arr[apply_g, 3] = 255.0
        
        # Pure white hot subatomic nucleus
        hot_c = cham_m & (dist < b_r * 0.45)
        arr[hot_c, 0] = 255.0
        arr[hot_c, 1] = 255.0
        arr[hot_c, 2] = 255.0
        arr[hot_c, 3] = 255.0
        
        # Rotating Quantum Probability Wave Rings (Interlocking Gyroscopic Orbits)
        # Ring 1
        a1 = phase
        rx1 = dx * math.cos(a1) - dy * math.sin(a1)
        ry1 = dx * math.sin(a1) + dy * math.cos(a1)
        r1_d = np.abs(np.sqrt((rx1 / 1.5)**2 + (ry1 / 0.6)**2) - 3.8 * scale)
        r1_m = cham_m & (r1_d < 0.8 * scale)
        
        # Ring 2
        a2 = -phase + math.pi/2
        rx2 = dx * math.cos(a2) - dy * math.sin(a2)
        ry2 = dx * math.sin(a2) + dy * math.cos(a2)
        r2_d = np.abs(np.sqrt((rx2 / 1.5)**2 + (ry2 / 0.6)**2) - 3.8 * scale)
        r2_m = cham_m & (r2_d < 0.8 * scale)
        
        for rm in [r1_m, r2_m]:
            arr[rm, 0] = np.clip(arr[rm, 0] + 50.0, 0, 255)
            arr[rm, 1] = np.clip(arr[rm, 1] + 240.0, 0, 255)
            arr[rm, 2] = np.clip(arr[rm, 2] + 255.0, 0, 255)
            arr[rm, 3] = 255.0
            
        # Micro electric arc discharges from the 4 emitters to the core
        if f % 3 in [0, 1]:
            emitter_ang = (f % 4) * (math.pi / 2.0)
            ex = cx + (r_inner - 2.8 * scale) * math.cos(emitter_ang)
            ey = cy + (r_inner - 2.8 * scale) * math.sin(emitter_ang)
            arc_pts = np.linspace(0, 1, 12)
            for t in arc_pts:
                w_offset = 0.8 * scale * math.sin(t * math.pi * 3 + phase * 4)
                px = (1 - t) * ex + t * cx + w_offset * (-math.sin(emitter_ang))
                py = (1 - t) * ey + t * cy + w_offset * (math.cos(emitter_ang))
                ix, iy = int(round(px)), int(round(py))
                if 0 <= ix < size and 0 <= iy < size and cham_m[iy, ix]:
                    arr[iy, ix, 0] = 200.0
                    arr[iy, ix, 1] = 250.0
                    arr[iy, ix, 2] = 255.0
                    arr[iy, ix, 3] = 255.0
                    
        img_data = np.clip(arr, 0, 255).astype(np.uint8)
        frames.append(Image.fromarray(img_data, mode="RGBA"))
        
    return frames

# CONCEPT 2: "Hyper-Cube Quantum Stasis Cell" (Precision Cassette / Stasis Cube with Tesseract Boson Lattice)
def create_boson_redesign_cube(size=32, num_frames=16):
    frames = []
    scale = size / 32.0
    cx, cy = (size - 1) / 2.0, (size - 1) / 2.0
    
    y_coords, x_coords = np.mgrid[:size, :size].astype(np.float32)
    dx = x_coords - cx
    dy = y_coords - cy
    dist = np.sqrt(dx**2 + dy**2)
    
    w_box = 13.5 * scale
    h_box = 13.5 * scale
    
    for f in range(num_frames):
        phase = (f / num_frames) * 2 * math.pi
        arr = np.zeros((size, size, 4), dtype=np.float32)
        
        # Heavy square cassette with chamfered cut corners
        box_mask = (np.abs(dx) <= w_box) & (np.abs(dy) <= h_box) & ((np.abs(dx) + np.abs(dy)) <= (w_box * 1.55))
        
        # Heavy chamfer shading
        dot_l = -( (dx / w_box) * 0.707 + (dy / h_box) * 0.707 )
        
        # Dark Neutronium-Carbon Armor Plate
        arr[box_mask, 0] = np.clip(45.0 + 35.0 * dot_l[box_mask], 20, 130)
        arr[box_mask, 1] = np.clip(52.0 + 40.0 * dot_l[box_mask], 24, 150)
        arr[box_mask, 2] = np.clip(68.0 + 50.0 * dot_l[box_mask], 32, 190)
        arr[box_mask, 3] = 255.0
        
        # Outer dark silhouette border
        # Inner chamber window
        w_inner = 8.5 * scale
        h_inner = 8.5 * scale
        inner_m = (np.abs(dx) < w_inner) & (np.abs(dy) < h_inner)
        
        # Beveled inner window frame
        frame_groove = (np.abs(dx) <= w_inner + 1.2 * scale) & (np.abs(dy) <= h_inner + 1.2 * scale) & ~inner_m
        arr[frame_groove, 0] = 160.0
        arr[frame_groove, 1] = 185.0
        arr[frame_groove, 2] = 220.0
        
        # 4 Corner Heat Sinks / Cryogenic Coolant Ports
        for sx in [-1, 1]:
            for sy in [-1, 1]:
                px = cx + sx * 10.5 * scale
                py = cy + sy * 10.5 * scale
                p_dist = np.sqrt((x_coords - px)**2 + (y_coords - py)**2)
                p_m = p_dist < 1.6 * scale
                arr[p_m, 0] = 30.0
                arr[p_m, 1] = 210.0 # Cyan cryo indicator
                arr[p_m, 2] = 255.0
                arr[p_m, 3] = 255.0
                
        # Status Data Bar on Top Edge
        top_bar = (np.abs(dx) <= 6.0 * scale) & (dy >= -12.5 * scale) & (dy <= -10.5 * scale)
        arr[top_bar, 0] = 255.0
        arr[top_bar, 1] = 180.0
        arr[top_bar, 2] = 40.0
        arr[top_bar, 3] = 255.0
        
        # Stasis Chamber Vacuum Glass
        arr[inner_m, 0] = 12.0
        arr[inner_m, 1] = 16.0
        arr[inner_m, 2] = 28.0
        arr[inner_m, 3] = 240.0
        
        # ROTATING TESSERACT / QUANTUM BOSON LATTICE
        # 4D Hypercube / Hexagonal Boson Matrix projected in 2D
        ang = phase
        rot_dx = dx * math.cos(ang) - dy * math.sin(ang)
        rot_dy = dx * math.sin(ang) + dy * math.cos(ang)
        
        # Glowing Boson Singularity Core
        pulse = 0.85 + 0.3 * math.sin(phase * 2)
        b_r = 3.5 * scale * pulse
        b_dist = np.sqrt(dx**2 + dy**2)
        b_int = np.clip(1.0 - b_dist / b_r, 0, 1) ** 1.8
        
        core_glow = inner_m & (b_dist < 7.5 * scale)
        glow_factor = np.clip(1.0 - b_dist / (7.5 * scale), 0, 1)
        
        arr[core_glow, 0] = np.clip(arr[core_glow, 0] + 120.0 * glow_factor[core_glow] + 255.0 * b_int[core_glow], 0, 255)
        arr[core_glow, 1] = np.clip(arr[core_glow, 1] + 240.0 * glow_factor[core_glow] + 255.0 * b_int[core_glow], 0, 255)
        arr[core_glow, 2] = np.clip(arr[core_glow, 2] + 255.0 * glow_factor[core_glow] + 255.0 * b_int[core_glow], 0, 255)
        
        # Super-intense white center
        white_c = inner_m & (b_dist < 1.8 * scale)
        arr[white_c, 0] = 255.0
        arr[white_c, 1] = 255.0
        arr[white_c, 2] = 255.0
        arr[white_c, 3] = 255.0
        
        # Rotating Lattice Struts (Geometric Crystal / Hexagonal Energy Cage)
        for i in range(6):
            arm_a = ang + i * (math.pi / 3.0)
            p_end_x = cx + 5.2 * scale * math.cos(arm_a)
            p_end_y = cy + 5.2 * scale * math.sin(arm_a)
            # Line from center to point
            t_pts = np.linspace(0, 1, 10)
            for t in t_pts:
                lx = (1 - t) * cx + t * p_end_x
                ly = (1 - t) * cy + t * p_end_y
                ix, iy = int(round(lx)), int(round(ly))
                if 0 <= ix < size and 0 <= iy < size and inner_m[iy, ix]:
                    arr[iy, ix, 0] = 200.0
                    arr[iy, ix, 1] = 255.0
                    arr[iy, ix, 2] = 255.0
                    arr[iy, ix, 3] = 255.0
                    
            # Vertex node spark
            vx, vy = int(round(p_end_x)), int(round(p_end_y))
            if 0 <= vx < size and 0 <= vy < size and inner_m[vy, vx]:
                arr[vy, vx, 0] = 255.0
                arr[vy, vx, 1] = 255.0
                arr[vy, vx, 2] = 255.0
                arr[vy, vx, 3] = 255.0
                
        img_data = np.clip(arr, 0, 255).astype(np.uint8)
        frames.append(Image.fromarray(img_data, mode="RGBA"))
        
    return frames

if __name__ == "__main__":
    # 1. Graviton Anomaly 128x
    print("Generating Graviton Anomaly (128x)...")
    grav_128 = create_graviton_anomaly_128(NUM_FRAMES)
    save_transparent_gif(grav_128, f"{OUT_DIR}/graviton_anomaly_128.gif", duration=80)
    strip_128 = Image.new("RGBA", (128, 128 * NUM_FRAMES))
    for i, f in enumerate(grav_128):
        strip_128.paste(f, (0, i * 128))
    strip_128.save(f"{OUT_DIR}/graviton_anomaly_128_strip.png")
    print(f"Generated graviton_anomaly_128: {strip_128.size}")
    
    # 2. Stable Boson Redesign Concept 1 (Tokamak Cell) - 32x, 64x, 128x
    print("Generating Boson Redesign 1 (Tokamak Cell)...")
    tokamak_32 = create_boson_redesign_tokamak(32, NUM_FRAMES)
    tokamak_64 = create_boson_redesign_tokamak(64, NUM_FRAMES)
    tokamak_128 = create_boson_redesign_tokamak(128, NUM_FRAMES)
    
    save_transparent_gif(tokamak_32, f"{OUT_DIR}/boson_tokamak_32.gif")
    save_transparent_gif(tokamak_64, f"{OUT_DIR}/boson_tokamak_64.gif")
    save_transparent_gif(tokamak_128, f"{OUT_DIR}/boson_tokamak_128.gif")
    
    t_strip_32 = Image.new("RGBA", (32, 32 * NUM_FRAMES))
    for i, f in enumerate(tokamak_32): t_strip_32.paste(f, (0, i * 32))
    t_strip_32.save(f"{OUT_DIR}/boson_tokamak_32_strip.png")
    
    t_strip_64 = Image.new("RGBA", (64, 64 * NUM_FRAMES))
    for i, f in enumerate(tokamak_64): t_strip_64.paste(f, (0, i * 64))
    t_strip_64.save(f"{OUT_DIR}/boson_tokamak_64_strip.png")
    
    t_strip_128 = Image.new("RGBA", (128, 128 * NUM_FRAMES))
    for i, f in enumerate(tokamak_128): t_strip_128.paste(f, (0, i * 128))
    t_strip_128.save(f"{OUT_DIR}/boson_tokamak_128_strip.png")
    
    # 3. Stable Boson Redesign Concept 2 (Stasis Cube) - 32x, 64x, 128x
    print("Generating Boson Redesign 2 (Stasis Cube)...")
    cube_32 = create_boson_redesign_cube(32, NUM_FRAMES)
    cube_64 = create_boson_redesign_cube(64, NUM_FRAMES)
    cube_128 = create_boson_redesign_cube(128, NUM_FRAMES)
    
    save_transparent_gif(cube_32, f"{OUT_DIR}/boson_cube_32.gif")
    save_transparent_gif(cube_64, f"{OUT_DIR}/boson_cube_64.gif")
    save_transparent_gif(cube_128, f"{OUT_DIR}/boson_cube_128.gif")
    
    c_strip_32 = Image.new("RGBA", (32, 32 * NUM_FRAMES))
    for i, f in enumerate(cube_32): c_strip_32.paste(f, (0, i * 32))
    c_strip_32.save(f"{OUT_DIR}/boson_cube_32_strip.png")
    
    c_strip_64 = Image.new("RGBA", (64, 64 * NUM_FRAMES))
    for i, f in enumerate(cube_64): c_strip_64.paste(f, (0, i * 64))
    c_strip_64.save(f"{OUT_DIR}/boson_cube_64_strip.png")
    
    c_strip_128 = Image.new("RGBA", (128, 128 * NUM_FRAMES))
    for i, f in enumerate(cube_128): c_strip_128.paste(f, (0, i * 128))
    c_strip_128.save(f"{OUT_DIR}/boson_cube_128_strip.png")
    
    print("All redesigns and 128x generated successfully!")
