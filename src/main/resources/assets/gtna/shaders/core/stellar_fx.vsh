#version 150

// Stellar Containment Chamber effects (GTNA original). Object space is the mesh's own space: a unit sphere for the
// star and corona, a cone for the beams, a unit square for the disk.
in vec3 Position;
in vec2 UV0;

uniform mat4 ModelViewMat;
uniform mat4 ProjMat;

out vec3 objPos;
out vec3 viewNormal;
out vec2 uv;

void main() {
    objPos = Position;
    uv = UV0;
    viewNormal = normalize(mat3(ModelViewMat) * Position);
    gl_Position = ProjMat * ModelViewMat * vec4(Position, 1.0);
}
