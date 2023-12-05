#version 330 core

in vec2 frag_texcoord;
in vec3 frag_normal;

out vec4 frag_color;

void main()
{
    // Simple fragment shader, adjust as needed
    vec3 light_direction = normalize(vec3(1.0, 1.0, 1.0));
    float intensity = max(dot(frag_normal, light_direction), 0.0);

    vec3 base_color = vec3(0.7, 0.7, 0.7);
    vec3 final_color = base_color * intensity;

    frag_color = vec4(final_color, 1.0);
}
