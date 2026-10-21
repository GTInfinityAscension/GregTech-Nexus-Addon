#!/usr/bin/env python3
"""
Audio Generator for GregTech Nexus Addon (GTNA) Original Multiblocks.
Synthesizes high-fidelity, procedurally generated sound effects for the 4 exclusive multiblocks:
  1. Antimatter Collider Ring (UIV)
  2. Stellar Containment Chamber (MAX)
  3. Dimensional Rift Gate (UIV)
  4. Kinetic Orbital Lance (UEV)

Outputs high quality Vorbis Mono .ogg (for in-game 3D positional audio)
and uncompressed .wav (for direct evaluation/listening).
"""

import os
import wave
import subprocess
import numpy as np

SAMPLE_RATE = 44100
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "evaluation")

# ---------------------------------------------------------------------------
# DSP Utility Functions
# ---------------------------------------------------------------------------

def time_vector(duration_sec, sr=SAMPLE_RATE):
    num_samples = int(duration_sec * sr)
    return np.linspace(0, duration_sec, num_samples, endpoint=False), num_samples

def freq_filter(signal, sr=SAMPLE_RATE, low_cutoff=None, high_cutoff=None, rolloff=18):
    """Zero-phase smooth frequency filter using FFT."""
    n = len(signal)
    freqs = np.fft.rfftfreq(n, d=1.0 / sr)
    spectrum = np.fft.rfft(signal)
    h = np.ones_like(freqs, dtype=np.float64)
    if low_cutoff is not None and low_cutoff > 0:
        h *= 1.0 / np.sqrt(1.0 + (low_cutoff / np.maximum(freqs, 1e-6)) ** (rolloff / 3.0))
    if high_cutoff is not None and high_cutoff < sr / 2:
        h *= 1.0 / np.sqrt(1.0 + (freqs / high_cutoff) ** (rolloff / 3.0))
    return np.fft.irfft(spectrum * h, n=n)

def resonant_bandpass(signal, center_freq, q=6.0, sr=SAMPLE_RATE):
    """Resonant 2nd-order band-pass filter."""
    n = len(signal)
    freqs = np.fft.rfftfreq(n, d=1.0 / sr)
    spectrum = np.fft.rfft(signal)
    ratio = np.maximum(freqs, 1e-3) / center_freq
    h = 1.0 / np.sqrt(1.0 + (q ** 2) * ((ratio - 1.0 / ratio) ** 2))
    return np.fft.irfft(spectrum * h, n=n)

def saturate(signal, drive=1.5):
    """Soft analog-style saturation (tanh)."""
    if drive <= 0:
        return signal
    return np.tanh(signal * drive) / np.tanh(drive)

def reverb_delays(signal, decay_sec=2.5, sr=SAMPLE_RATE):
    """Multi-tap diffusion reverb for large open spaces/shockwaves."""
    out = np.copy(signal)
    delays = [0.031, 0.043, 0.059, 0.083, 0.117, 0.163, 0.229, 0.317, 0.439, 0.607, 0.839, 1.157]
    for d in delays:
        delay_samples = int(d * sr)
        gain = np.exp(-d * 3.5 / decay_sec) * 0.28
        if delay_samples < len(signal):
            out[delay_samples:] += signal[:-delay_samples] * gain
    return out

def seamless_loop(signal, target_duration, crossfade_duration=1.0, sr=SAMPLE_RATE):
    """Creates a mathematically seamless loop by equal-power crossfading tail into head."""
    target_samples = int(target_duration * sr)
    cf_samples = int(crossfade_duration * sr)
    total_needed = target_samples + cf_samples
    
    if len(signal) < total_needed:
        # Tile if slightly short
        reps = int(np.ceil(total_needed / len(signal)))
        signal = np.tile(signal, reps)
        
    sig = signal[:total_needed].copy()
    head = sig[:target_samples].copy()
    tail = sig[target_samples:total_needed].copy()
    
    # Equal-power cosine curve
    t = np.linspace(0, 1, cf_samples)
    fade_in = np.sin(0.5 * np.pi * t)
    fade_out = np.cos(0.5 * np.pi * t)
    
    head[:cf_samples] = head[:cf_samples] * fade_in + tail * fade_out
    return head

def normalize_and_export(filename_base, samples, sr=SAMPLE_RATE, target_peak_db=-1.0):
    """Normalizes audio and writes both .wav and Vorbis .ogg."""
    peak = np.max(np.abs(samples))
    if peak > 1e-6:
        target_amp = 10.0 ** (target_peak_db / 20.0)
        norm_samples = samples * (target_amp / peak)
    else:
        norm_samples = samples

    wav_path = os.path.join(OUT_DIR, f"{filename_base}.wav")
    ogg_path = os.path.join(OUT_DIR, f"{filename_base}.ogg")

    pcm_data = (np.clip(norm_samples, -1.0, 1.0) * 32767.0).astype(np.int16)
    with wave.open(wav_path, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(pcm_data.tobytes())

    # Encode to high quality mono Vorbis Ogg
    cmd = [
        "ffmpeg", "-y", "-i", wav_path,
        "-c:a", "libvorbis", "-q:a", "6",
        "-ac", "1",
        ogg_path
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"  [OK] Generated: {filename_base}.ogg ({len(samples)/sr:.2f}s)")

# ---------------------------------------------------------------------------
# 1. ANEL COLISOR DE ANTIMATÉRIA (Antimatter Collider Ring)
# ---------------------------------------------------------------------------

def synth_collider_loop():
    """
    Superconducting magnetic accelerator ring.
    Deep 48Hz cryogenic hum, 16Hz packet circulation pulse, 720Hz RF cavity drone,
    and fluid helium pressure hiss.
    """
    duration = 8.0
    cf = 1.2
    t, n = time_vector(duration + cf)
    
    # 1. Superconducting coils sub-bass hum (48 Hz + harmonics)
    hum = (0.50 * np.sin(2 * np.pi * 48.0 * t) +
           0.30 * np.sin(2 * np.pi * 96.0 * t + 0.5) +
           0.15 * np.sin(2 * np.pi * 144.0 * t + 1.2) +
           0.08 * np.sin(2 * np.pi * 240.0 * t + 2.0))
    hum = saturate(hum, 1.4)
    
    # 2. Relativistic bunch circulation (15.9 Hz modulation - rev frequency scaled)
    bunch_mod = 0.5 + 0.5 * np.sin(2 * np.pi * 15.915 * t) ** 2
    bunch_carrier = np.sin(2 * np.pi * 192.0 * t + 0.8 * np.sin(2 * np.pi * 48.0 * t))
    circulation = bunch_carrier * (0.25 * bunch_mod + 0.1)
    
    # 3. Superconducting RF cavities (high-tech precision whine)
    rf_tone = (0.07 * np.sin(2 * np.pi * 720.0 * t) +
               0.04 * np.sin(2 * np.pi * 1440.0 * t + 0.3) +
               0.02 * np.sin(2 * np.pi * 2160.0 * t + 0.7))
    # Subtle detune vibrato
    rf_tone *= (1.0 + 0.15 * np.sin(2 * np.pi * 0.4 * t))
    
    # 4. Liquid helium cryo coolant flow (low-pass shaped noise)
    noise = np.random.normal(0, 1, n)
    cryo = freq_filter(noise, low_cutoff=80, high_cutoff=400, rolloff=18) * 0.22
    cryo *= (1.0 + 0.2 * np.sin(2 * np.pi * 0.25 * t))
    
    raw = hum * 0.55 + circulation * 0.30 + rf_tone * 0.20 + cryo * 0.25
    raw = saturate(raw, 1.2)
    return seamless_loop(raw, duration, cf)

def synth_collider_quench():
    """
    Emergency magnet quench / beam dump SFX:
    Arc discharge, rapid pitch descent of magnetic field, and loud cryo vent burst.
    """
    duration = 3.2
    t, n = time_vector(duration)
    
    # Pitch descent: 850 Hz -> 40 Hz
    freq_sweep = 40.0 + 810.0 * np.exp(-t / 0.35)
    phase = 2 * np.pi * np.cumsum(freq_sweep) / SAMPLE_RATE
    mag_collapse = np.sin(phase) * np.exp(-t / 0.8)
    mag_collapse = saturate(mag_collapse, 2.5)
    
    # Arc snap at start
    noise = np.random.normal(0, 1, n)
    arc_snap = freq_filter(noise, low_cutoff=500, high_cutoff=6000) * np.exp(-t / 0.04) * 1.5
    
    # Cryo release hiss (starts at 0.15s, builds and decays over 2.5s)
    vent_env = np.maximum(0, t - 0.12) * np.exp(-np.maximum(0, t - 0.12) / 0.9)
    vent_env = vent_env / (np.max(vent_env) + 1e-6)
    vent_hiss = freq_filter(noise, low_cutoff=300, high_cutoff=2800) * vent_env * 0.7
    
    # Deep sub-bass dump thump
    sub_thump = np.sin(2 * np.pi * 42.0 * t) * np.exp(-t / 0.5) * 0.8
    
    out = arc_snap * 0.7 + mag_collapse * 0.6 + sub_thump * 0.7 + vent_hiss * 0.65
    return saturate(out, 1.3)

# ---------------------------------------------------------------------------
# 2. CÂMARA DE CONTENÇÃO ESTELAR (Stellar Containment Chamber)
# ---------------------------------------------------------------------------

def synth_stellar_pulsar_loop():
    """
    Neutron Star / Millisecond Pulsar mode:
    Deep gravitational core drone, 6 Hz rhythmic lighthouse beam sweeps,
    plasma accretion hiss and high-energy containment field.
    """
    duration = 8.0
    cf = 1.2
    t, n = time_vector(duration + cf)
    
    # 1. Gravitational core (34 Hz fundamental + rich low harmonics)
    core = (0.55 * np.sin(2 * np.pi * 34.0 * t) +
            0.35 * np.sin(2 * np.pi * 68.0 * t + 0.4) +
            0.20 * np.sin(2 * np.pi * 102.0 * t + 0.8))
    core = saturate(core, 1.6)
    
    # 2. Pulsar beam sweep (6.25 Hz pulse train: energetic cosmic swooshes)
    pulse_freq = 6.25
    sweep_phase = (t * pulse_freq) % 1.0
    # Asymmetric pulse shape resembling a focused beam sweeping past
    sweep_env = np.exp(-((sweep_phase - 0.5) ** 2) / 0.015)
    noise = np.random.normal(0, 1, n)
    sweep_sound = freq_filter(noise, low_cutoff=400, high_cutoff=2400) * sweep_env * 0.45
    
    # 3. Accretion disk plasma fizz (granular infalling matter)
    plasma_noise = freq_filter(noise, low_cutoff=1200, high_cutoff=5500) * 0.14
    plasma_noise *= (1.0 + 0.3 * np.sin(2 * np.pi * 1.5 * t))
    
    # 4. Containment bands hum (120 Hz resonant naquadah flux)
    bands = (0.20 * np.sin(2 * np.pi * 120.0 * t) +
             0.10 * np.sin(2 * np.pi * 240.0 * t + 0.5))
    
    raw = core * 0.55 + sweep_sound * 0.35 + plasma_noise * 0.20 + bands * 0.25
    raw = saturate(raw, 1.25)
    return seamless_loop(raw, duration, cf)

def synth_stellar_black_hole_loop():
    """
    Kerr Black Hole mode:
    Deep ominous event horizon drone, Penrose ergosphere vortex,
    dissonant spatial tension and subtle photon ring shimmer.
    """
    duration = 10.0
    cf = 1.5
    t, n = time_vector(duration + cf)
    
    # 1. Ultra-deep event horizon drone (24 Hz fundamental with micro-drift)
    sub = np.sin(2 * np.pi * 24.0 * t + 0.2 * np.sin(2 * np.pi * 0.08 * t)) * 0.65
    sub += np.sin(2 * np.pi * 48.0 * t + 0.5) * 0.35
    sub = saturate(sub, 1.8)
    
    # 2. Cosmic tritone (50 Hz and 70.7 Hz) - deep dissonance of distorted spacetime
    dissonance = (0.22 * np.sin(2 * np.pi * 50.0 * t) +
                  0.18 * np.sin(2 * np.pi * 70.71 * t + 1.1))
    
    # 3. Ergosphere vortex wind (bandpass swept noise)
    noise = np.random.normal(0, 1, n)
    vortex_center = 180.0 + 70.0 * np.sin(2 * np.pi * 0.12 * t)
    vortex = resonant_bandpass(noise, 200.0, q=3.0) * 0.35
    vortex *= (1.0 + 0.35 * np.cos(2 * np.pi * 0.12 * t))
    
    # 4. High-frequency photon ring shimmer (2400 Hz soft halo)
    photon_ring = (np.sin(2 * np.pi * 2400.0 * t) * 0.02 +
                   np.sin(2 * np.pi * 3600.0 * t) * 0.015)
    photon_ring *= (0.6 + 0.4 * np.sin(2 * np.pi * 0.3 * t))
    
    raw = sub * 0.60 + dissonance * 0.30 + vortex * 0.35 + photon_ring * 0.15
    raw = saturate(raw, 1.2)
    return seamless_loop(raw, duration, cf)

def synth_stellar_quake():
    """
    Starquake / crust rupture SFX:
    Sudden colossal rupture transient, vibrating neutronium hull, long deep decay.
    """
    duration = 3.8
    t, n = time_vector(duration)
    
    # Sudden heavy rupture crack
    noise = np.random.normal(0, 1, n)
    crack = freq_filter(noise, low_cutoff=250, high_cutoff=4500) * np.exp(-t / 0.035) * 1.8
    
    # Sub-bass seismic shock (32 Hz decaying over 3 seconds)
    seismic = np.sin(2 * np.pi * 32.0 * t) * np.exp(-t / 1.4) * 1.2
    seismic = saturate(seismic, 2.0)
    
    # Ringing metallic/gravitational mode (110 Hz + 225 Hz)
    ring = (np.sin(2 * np.pi * 110.0 * t) * 0.6 +
            np.sin(2 * np.pi * 225.0 * t) * 0.3) * np.exp(-t / 0.9)
    
    # Deep rolling thunder reverberation
    tail = freq_filter(noise, low_cutoff=40, high_cutoff=180) * np.exp(-t / 2.0) * 0.7
    tail = reverb_delays(tail, decay_sec=2.8)
    
    out = crack * 0.7 + seismic * 0.8 + ring * 0.45 + tail * 0.5
    return saturate(out, 1.3)

# ---------------------------------------------------------------------------
# 3. PORTÃO DE FENDA DIMENSIONAL (Dimensional Rift Gate)
# ---------------------------------------------------------------------------

def synth_rift_loop():
    """
    Dimensional Rift Gate open loop:
    Harmonic chords (110 Hz, 146.7 Hz, 165 Hz), ethereal planar wind,
    and delicate spacetime micro-fissure static.
    """
    duration = 8.0
    cf = 1.2
    t, n = time_vector(duration + cf)
    
    # 1. Harmonic alignment chord: 110 Hz (A2), 146.67 Hz (D3 - 4:3), 165 Hz (E3 - 3:2), 220 Hz (A3 - 2:1)
    # Slow chorus modulation creates the illusion of interdimensional alignment
    detune1 = 0.4 * np.sin(2 * np.pi * 0.15 * t)
    detune2 = 0.3 * np.cos(2 * np.pi * 0.22 * t)
    chord = (0.35 * np.sin(2 * np.pi * (110.0 + detune1) * t) +
             0.25 * np.sin(2 * np.pi * 146.67 * t + 0.3) +
             0.28 * np.sin(2 * np.pi * (165.0 + detune2) * t + 0.7) +
             0.18 * np.sin(2 * np.pi * 220.0 * t + 1.2))
    chord = saturate(chord, 1.3)
    
    # 2. Planar wind (flowing atmosphere across the horizon)
    noise = np.random.normal(0, 1, n)
    wind_low = resonant_bandpass(noise, 240.0, q=3.5) * 0.30
    wind_high = resonant_bandpass(noise, 620.0, q=4.0) * 0.20
    wind = (wind_low * (0.7 + 0.3 * np.sin(2 * np.pi * 0.2 * t)) +
            wind_high * (0.7 + 0.3 * np.cos(2 * np.pi * 0.2 * t)))
    
    # 3. Spacetime fissure static (delicate crystal-like micro bursts)
    fissures = freq_filter(noise, low_cutoff=3800, high_cutoff=8500) * 0.08
    fissures *= (np.sin(2 * np.pi * 3.7 * t) ** 4 + 0.3)
    
    raw = chord * 0.50 + wind * 0.45 + fissures * 0.25
    raw = saturate(raw, 1.2)
    return seamless_loop(raw, duration, cf)

def synth_rift_open():
    """
    Rift activation SFX:
    Rising harmonic resonance sweep followed by spatial rupture and deep portal whoosh.
    """
    duration = 3.5
    t, n = time_vector(duration)
    
    # Harmonic frequency sweep: 90 Hz -> 550 Hz over 1.4s
    sweep_t = np.clip(t / 1.4, 0.0, 1.0)
    sweep_f = 90.0 + 460.0 * (sweep_t ** 2)
    phase = 2 * np.pi * np.cumsum(sweep_f) / SAMPLE_RATE
    rise = np.sin(phase) * (1.0 - np.exp(-t / 0.3)) * np.exp(-np.maximum(0, t - 1.2) / 0.8)
    rise = saturate(rise, 2.0)
    
    # Rupture whoosh at 1.3s
    noise = np.random.normal(0, 1, n)
    whoosh_t = np.maximum(0, t - 1.2)
    whoosh_env = whoosh_t * np.exp(-whoosh_t / 0.6)
    whoosh_env /= (np.max(whoosh_env) + 1e-6)
    whoosh = resonant_bandpass(noise, 180.0, q=2.5) * whoosh_env * 0.8
    
    # Deep spatial expansion thud
    thud_t = np.maximum(0, t - 1.3)
    thud = np.sin(2 * np.pi * 45.0 * thud_t) * np.exp(-thud_t / 0.7) * 0.7
    
    out = rise * 0.6 + whoosh * 0.7 + thud * 0.6
    return saturate(out, 1.3)

# ---------------------------------------------------------------------------
# 4. LANÇA CINÉTICA ORBITAL (Kinetic Orbital Lance)
# ---------------------------------------------------------------------------

def synth_lance_fire():
    """
    Colossal orbital kinetic bombardment railgun blast:
      1. Hyper-fast supersonic rail arc crack (0 to 0.05s)
      2. Massive low-end kinetic explosion (0.04 to 0.8s)
      3. Long decaying atmospheric thunder & shockwave echo (0.3 to 4.5s)
    """
    duration = 4.5
    t, n = time_vector(duration)
    noise = np.random.normal(0, 1, n)
    
    # Phase 1: Supersonic rail arc snap (extreme transient attack)
    arc_snap = freq_filter(noise, low_cutoff=800, high_cutoff=9000) * np.exp(-t / 0.018) * 2.5
    # High-voltage laser/rail chirp
    chirp_f = 2400.0 * np.exp(-t / 0.03) + 80.0
    chirp_phase = 2 * np.pi * np.cumsum(chirp_f) / SAMPLE_RATE
    chirp = np.sin(chirp_phase) * np.exp(-t / 0.04) * 1.5
    
    # Phase 2: Detonation bass body (heavy cubic saturated 42Hz diving to 22Hz)
    dive_f = 22.0 + 26.0 * np.exp(-t / 0.25)
    dive_phase = 2 * np.pi * np.cumsum(dive_f) / SAMPLE_RATE
    bass_punch = np.sin(dive_phase) * np.exp(-t / 0.65) * 2.0
    bass_punch = saturate(bass_punch, 2.5)
    
    # Phase 3: Atmospheric horizon thunder (multi-tap reverberation)
    rumble_core = freq_filter(noise, low_cutoff=35, high_cutoff=160, rolloff=24) * np.exp(-t / 1.8) * 1.6
    rumble_echo = reverb_delays(rumble_core, decay_sec=3.2)
    
    # Mid-range explosive air displacement
    air_body = resonant_bandpass(noise, 320.0, q=2.0) * np.exp(-t / 0.45) * 0.9
    
    out = arc_snap * 0.8 + chirp * 0.5 + bass_punch * 0.95 + air_body * 0.6 + rumble_echo * 0.85
    return saturate(out, 1.4)

def synth_lance_charge_loop():
    """
    Capacitor bank charging loop:
    60 Hz heavy industrial grid drone, 960 Hz inductor whine,
    and cryogenic rail cooling turbines.
    """
    duration = 6.0
    cf = 1.0
    t, n = time_vector(duration + cf)
    
    # 1. 60 Hz high-power capacitor hum + 120 Hz + 180 Hz harmonics
    hum = (0.50 * np.sin(2 * np.pi * 60.0 * t) +
           0.35 * np.sin(2 * np.pi * 120.0 * t + 0.4) +
           0.20 * np.sin(2 * np.pi * 180.0 * t + 0.9) +
           0.10 * np.sin(2 * np.pi * 360.0 * t + 1.5))
    hum = saturate(hum, 1.4)
    # 1.0 Hz pulsating charge rhythm
    hum *= (0.85 + 0.15 * np.sin(2 * np.pi * 1.0 * t))
    
    # 2. High-voltage inductor whine (960 Hz with subtle vibrato)
    whine = (0.08 * np.sin(2 * np.pi * 960.0 * t) +
             0.04 * np.sin(2 * np.pi * 1920.0 * t + 0.3))
    whine *= (1.0 + 0.2 * np.sin(2 * np.pi * 2.0 * t))
    
    # 3. Cooling turbines / liquid nitrogen circulation
    noise = np.random.normal(0, 1, n)
    cooling = freq_filter(noise, low_cutoff=180, high_cutoff=650) * 0.22
    
    raw = hum * 0.60 + whine * 0.25 + cooling * 0.30
    raw = saturate(raw, 1.2)
    return seamless_loop(raw, duration, cf)

# ---------------------------------------------------------------------------
# Main Execution
# ---------------------------------------------------------------------------

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    print("=" * 60)
    print("GTNA Originals Audio Generator")
    print(f"Target directory: {OUT_DIR}")
    print("=" * 60)

    # 1. Collider
    print("\n[1/4] Anel Colisor de Antimatéria (Antimatter Collider Ring)...")
    normalize_and_export("collider_loop", synth_collider_loop())
    normalize_and_export("collider_quench", synth_collider_quench())

    # 2. Stellar Chamber
    print("\n[2/4] Câmara de Contenção Estelar (Stellar Containment Chamber)...")
    normalize_and_export("stellar_pulsar_loop", synth_stellar_pulsar_loop())
    normalize_and_export("stellar_black_hole_loop", synth_stellar_black_hole_loop())
    normalize_and_export("stellar_quake", synth_stellar_quake())

    # 3. Rift Gate
    print("\n[3/4] Portão de Fenda Dimensional (Dimensional Rift Gate)...")
    normalize_and_export("rift_loop", synth_rift_loop())
    normalize_and_export("rift_open", synth_rift_open())

    # 4. Kinetic Lance
    print("\n[4/4] Lança Cinética Orbital (Kinetic Orbital Lance)...")
    normalize_and_export("lance_fire", synth_lance_fire())
    normalize_and_export("lance_charge_loop", synth_lance_charge_loop())

    print("\n" + "=" * 60)
    print("All audio files generated successfully in evaluation folder!")
    print("=" * 60)

if __name__ == "__main__":
    main()
