#version 150

// GTNA item effects: procedural star field (Mode 0), flowing light (Mode 1) and crackling noise (Mode 2),
// drawn only where the mask texture is lit.

#moj_import <fog.glsl>

uniform sampler2D Sampler0;

uniform vec4 ColorModulator;
uniform float FogStart;
uniform float FogEnd;
uniform vec4 FogColor;

uniform float EffectTime;
uniform vec2 ViewAngle;
uniform float Density;
uniform float Opacity;
uniform int Mode;
uniform int AlphaMask;
uniform vec4 ColorA;
uniform vec4 ColorB;

in float vertexDistance;
in vec2 texCoord0;
in vec3 viewPos;

out vec4 fragColor;

float hash(vec2 p) {
    p = fract(p * vec2(233.34, 851.73));
    p += dot(p, p + 23.45);
    return fract(p.x * p.y);
}

float noise(vec2 p) {
    vec2 i = floor(p);
    vec2 f = fract(p);
    vec2 u = f * f * (3.0 - 2.0 * f);
    return mix(mix(hash(i), hash(i + vec2(1.0, 0.0)), u.x),
               mix(hash(i + vec2(0.0, 1.0)), hash(i + vec2(1.0, 1.0)), u.x), u.y);
}

float fbm(vec2 p) {
    float value = 0.0;
    float amplitude = 0.5;
    for (int i = 0; i < 5; i++) {
        value += amplitude * noise(p);
        p = p * 2.07 + vec2(11.3, 5.9);
        amplitude *= 0.5;
    }
    return value;
}

// Three parallax layers of twinkling points, one candidate star per grid cell.
float stars(vec2 p, float t, float threshold) {
    float total = 0.0;
    for (int layer = 0; layer < 3; layer++) {
        float depth = 1.0 + float(layer) * 0.8;
        vec2 q = p * depth + vec2(float(layer) * 17.3, t * 0.04 * (float(layer) + 1.0));
        vec2 cell = floor(q);
        float h = hash(cell);
        if (h < threshold) continue;
        vec2 center = vec2(hash(cell + 3.7), hash(cell + 9.1)) * 0.6 + 0.2;
        float d = length(fract(q) - center);
        float twinkle = 0.55 + 0.45 * sin(t * (1.3 + h * 3.0) + h * 61.0);
        float core = smoothstep(0.12 / depth, 0.0, d);
        float glow = smoothstep(0.35 / depth, 0.0, d) * 0.25;
        total += (core + glow) * twinkle / sqrt(depth);
    }
    return total;
}

void main() {
    vec4 m = texture(Sampler0, texCoord0);
    float mask = AlphaMask == 1 ? m.a : m.r * m.a;
    if (mask < 0.004) discard;

    vec2 p = viewPos.xy * Density + ViewAngle * 3.0;
    float t = EffectTime;
    vec3 col;
    float alpha;

    if (Mode == 0) {
        float cloud = fbm(p * 0.3 + vec2(t * 0.015, -t * 0.01));
        col = mix(ColorA.rgb, ColorB.rgb, smoothstep(0.35, 0.85, cloud));
        col += vec3(0.85, 0.92, 1.0) * stars(p, t, 0.78);
        alpha = 1.0;
    } else if (Mode == 1) {
        float flow = fbm(p * 0.45 + vec2(t * 0.06, -t * 0.035));
        float band = 0.5 + 0.5 * sin(flow * 9.0 + t * 0.7);
        col = mix(ColorA.rgb, ColorB.rgb, band);
        col = mix(col, vec3(1.0), pow(flow, 3.0) * 0.7);
        col += stars(p * 0.7, t * 1.5, 0.86) * 0.8;
        alpha = 0.85;
    } else {
        float step = floor(t * 10.0) / 10.0;
        float field = fbm(p * 0.6 + vec2(step * 0.8, step * 0.35));
        float ridge = pow(1.0 - abs(2.0 * fbm(p * 1.3 - vec2(t * 0.25, step)) - 1.0), 10.0);
        float flicker = 0.7 + 0.3 * hash(vec2(step, 4.2));
        col = mix(ColorA.rgb, ColorB.rgb, field) * flicker + ColorB.rgb * ridge * 1.6;
        alpha = 0.9;
    }

    vec4 color = vec4(clamp(col, 0.0, 1.0), alpha * mask * Opacity) * ColorModulator;
    fragColor = linear_fog(color, vertexDistance, FogStart, FogEnd, FogColor);
}
