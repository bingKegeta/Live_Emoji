import bpy
import pygame
from pygame.locals import *
from PIL import Image

blender_model_path = "RIGRESET.blend"

# Use bpy.ops.wm.open_mainfile to open the Blender file
bpy.ops.wm.open_mainfile(filepath=blender_model_path)

# Access the scene
scene = bpy.context.scene

# Access the collection and objects
face = bpy.data.collections.get("Male Head")
rig = face.objects.get('metarig')
obj = face.objects.get('Current.001')

if face:
    # Create a new camera object
    camera_data = bpy.data.cameras.new("Camera")
    camera = bpy.data.objects.new("Camera", camera_data)
    scene.collection.objects.link(camera)

    # Set the camera as the active camera
    scene.camera = camera

    # Set up render settings
    scene.render.image_settings.file_format = 'PNG'
    scene.render.filepath = "rendered_image.png"

    # Render the scene using the OpenGL renderer
    bpy.ops.render.render(write_still=True, use_viewport=True)

    # Load the rendered image directly using PIL
    img = Image.open(scene.render.filepath)
    img = img.transpose(Image.FLIP_TOP_BOTTOM)

    # Initialize Pygame
    pygame.init()
    display = pygame.display.set_mode((img.width, img.height))
    pygame.display.set_caption("Rendered Image")

    # Convert the image to Pygame format
    pygame_img = pygame.image.fromstring(img.tobytes(), img.size, img.mode)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Display the image
        display.blit(pygame_img, (0, 0))
        pygame.display.flip()
else:
    print("Object 'Male Head' not found in scene.")
