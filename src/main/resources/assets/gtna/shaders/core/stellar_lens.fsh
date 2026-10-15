#version 150

// Gravitational lens around the star (fictional strength). The star's own disc is left alone; around it the background
// is pulled towards the centre (deflection ~ Rs^2 / r, never reaching into the disc), and a faint blue ring sits at
// 1.25 Rs, like the 3D preview.
uniform sampler2D Scene;
uniform sampler2D SceneDepth;
uniform float FrontDepth;
uniform vec2 Center;
uniform float Radius;
uniform float StarRadius;
uniform float Strength;
uniform float Aspect;

in vec2 uv;

out vec4 fragColor;

void main() {
    vec2 d = uv - Center;
    d.x *= Aspect;
    float r = length(d);
    vec2 st = uv;
    float ring = 0.0;
    float edge = StarRadius * 1.08;
    if (Strength > 0.0 && r > edge) {
        float b = Strength * Radius * Radius / r * smoothstep(edge, edge * 1.6, r);
        b = min(b, (r - edge) * 0.5);
        vec2 off = normalize(d) * b;
        off.x /= Aspect;
        st = uv - off;
        ring = Strength * exp(-pow((r - Radius * 1.25) / (Radius * 0.12), 2.0)) * 0.35;
    }
    // Only what lies behind the corona bends: a pixel covered by something nearer (the hull, a wall) is left alone,
    // and nearer things are never pulled into the lens.
    if (texture(SceneDepth, uv).r < FrontDepth) {
        st = uv;
        ring = 0.0;
    } else if (texture(SceneDepth, clamp(st, 0.0, 1.0)).r < FrontDepth) {
        st = uv;
    }
    vec4 col = texture(Scene, clamp(st, 0.0, 1.0));
    fragColor = vec4(col.rgb + vec3(0.55, 0.75, 1.0) * ring, 1.0);
}
