#version 150

#moj_import <fog.glsl>

in vec3 Position;
in vec4 Color;
in vec2 UV0;
in ivec2 UV2;
in vec3 Normal;

uniform mat4 ModelViewMat;
uniform mat4 ProjMat;
uniform int FogShape;

out float vertexDistance;
out vec2 texCoord0;
out vec3 viewPos;

void main() {
    vec4 view = ModelViewMat * vec4(Position, 1.0);
    gl_Position = ProjMat * view;
    viewPos = view.xyz;
    vertexDistance = fog_distance(ModelViewMat, Position, FogShape);
    texCoord0 = UV0;
}
