#version 330 core

layout(location = 0) in vec3 in_position;
layout(location = 1) in vec2 in_texcoord;
layout(location = 2) in vec3 in_normal;

uniform mat4 model;  // Model matrix from the application
uniform mat4 view;   // View matrix from the application
uniform mat4 projection;  // Projection matrix from the application
uniform vec3 bone_positions[NumBones];  // Array of bone positions from the application

out vec2 frag_texcoord;
out vec3 frag_normal;

void main()
{
    // Compute bone transformations based on bone_positions
    mat4 bone_transform = mat4(1.0);
    for (int i = 0; i < NumBones; ++i)
    {
        bone_transform += translate(mat4(1.0), bone_positions[i]) * scale(mat4(1.0), vec3(1.0));  // Adjust as needed
    }

    // Apply transformations
    mat4 model_view_projection = projection * view * model * bone_transform;
    gl_Position = model_view_projection * vec4(in_position, 1.0);

    frag_texcoord = in_texcoord;
    frag_normal = mat3(transpose(inverse(model))) * in_normal;  // Transform normals
}
