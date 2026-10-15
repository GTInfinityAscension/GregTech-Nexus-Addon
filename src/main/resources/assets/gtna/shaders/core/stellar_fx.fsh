#version 150

// Modes: 0 neutron star surface, 1 corona, 2 pulsar beam, 3 accretion disk, 4 black hole, 5 rift horizon.
uniform float Time;
uniform float Mode;
uniform vec4 Tint;

in vec3 objPos;
in vec3 viewNormal;
in vec2 uv;

out vec4 fragColor;

float hash(vec3 p) {
    return fract(sin(dot(p, vec3(12.9, 78.2, 37.7))) * 43758.5);
}

float noise(vec3 p) {
    vec3 i = floor(p), f = fract(p);
    f = f * f * (3.0 - 2.0 * f);
    return mix(mix(mix(hash(i), hash(i + vec3(1, 0, 0)), f.x), mix(hash(i + vec3(0, 1, 0)), hash(i + vec3(1, 1, 0)), f.x), f.y),
               mix(mix(hash(i + vec3(0, 0, 1)), hash(i + vec3(1, 0, 1)), f.x), mix(hash(i + vec3(0, 1, 1)), hash(i + vec3(1, 1, 1)), f.x), f.y), f.z);
}

void main() {
    int mode = int(Mode + 0.5);
    float facing = abs(normalize(viewNormal).z);
    if (mode == 0) {
        vec3 p = objPos * 4.5;
        float s = noise(p * 0.9 + vec3(Time * 0.8)) * 0.6 + noise(p * 2.3 - vec3(Time * 1.3)) * 0.4;
        float limb = pow(facing, 0.35);
        vec3 col = mix(Tint.rgb, vec3(1.0), s) * (0.6 + 0.6 * limb);
        float spot = smoothstep(0.82, 0.98, abs(normalize(objPos).y));
        col += vec3(0.6, 0.8, 1.0) * spot * 2.0;
        fragColor = vec4(min(col, vec3(1.0)), 1.0);
    } else if (mode == 1) {
        float i = pow(1.0 - facing, 2.2);
        fragColor = vec4(Tint.rgb * 0.82 * i * (1.1 + 0.15 * sin(Time * 7.0)), i * Tint.a);
    } else if (mode == 2) {
        float a = (1.0 - uv.y) * (0.55 + 0.45 * sin(uv.y * 40.0 - Time * 20.0));
        fragColor = vec4(vec3(0.7, 0.85, 1.0) * a, a * 0.8 * Tint.a);
    } else if (mode == 3) {
        vec2 c = uv - 0.5;
        float r = length(c) * 2.0;
        if (r < 0.33 || r > 1.0) discard;
        float ang = atan(c.y, c.x);
        float s = 0.5 + 0.5 * sin(ang * 6.0 + 8.0 / r - Time * 3.0);
        float i = smoothstep(1.0, 0.6, r) * smoothstep(0.33, 0.45, r) * (0.4 + 0.6 * s);
        fragColor = vec4(mix(vec3(1.0, 0.45, 0.1), vec3(1.0, 0.85, 0.5), 1.0 - r) * i, i * Tint.a);
    } else if (mode == 5) {
        // Rift event horizon (the 3D preview's swirl), tinted with the biome colour.
        vec2 c = uv - 0.5;
        float r = length(c) * 2.0;
        if (r > 1.0) discard;
        float ang = atan(c.y, c.x) + Time * 0.6 + 3.0 / (r + 0.25);
        // Sample the noise on a circle so the angle wraps without a seam.
        vec2 dir = vec2(cos(ang), sin(ang));
        float s = noise(vec3(dir * 1.0, r * 6.0 - Time * 1.4)) * noise(vec3(dir * 2.3, r * 13.0 + Time + 3.7));
        vec3 col = mix(Tint.rgb * 0.35 + vec3(0.12, 0.02, 0.3), Tint.rgb * 0.6 + vec3(0.3, 0.5, 0.6), s);
        col += vec3(1.0) * pow(1.0 - r, 6.0) * 1.5;
        fragColor = vec4(col, (0.55 + 0.45 * s) * smoothstep(1.0, 0.85, r) * Tint.a);
    } else {
        // Event horizon with a thin photon ring at the silhouette.
        float ring = smoothstep(0.25, 0.0, facing) * 0.9;
        fragColor = vec4(vec3(1.0, 0.8, 0.55) * ring, 1.0);
    }
}
