#version 150

// Full-screen pass in normalised device coordinates.
in vec3 Position;
in vec2 UV0;

out vec2 uv;

void main() {
    uv = UV0;
    gl_Position = vec4(Position.xy, 0.0, 1.0);
}
