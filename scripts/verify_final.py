import bpy
import math

MODEL_PATH = '/home/ubuntu_16gb/raj_work_space/PERSONAL/newPort/Portfolio-Website/public/models/raj-final.glb'
OUTPUT_PATH = '/home/ubuntu_16gb/raj_work_space/PERSONAL/newPort/Portfolio-Website/public/final_check.png'

print('RENDERING FINAL MODEL CHECK')

# Clear
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Import
bpy.ops.import_scene.gltf(filepath=MODEL_PATH)

print('Model imported!')

# Check bones
armature = None
for obj in bpy.context.scene.objects:
    if obj.type == 'ARMATURE':
        armature = obj
        break

print(f'Armature: {armature.name}')

# List animations
print('\nAnimations found:')
for action in bpy.data.actions:
    print(f'  - {action.name}')

# Setup render
world = bpy.data.worlds.new('World')
bpy.context.scene.world = world
world.use_nodes = True
world.node_tree.nodes['Background'].inputs[0].default_value = (0.12, 0.12, 0.18, 1)

# Lights
sun_data = bpy.data.lights.new('Sun', type='SUN')
sun_data.energy = 2
sun = bpy.data.objects.new('Sun', sun_data)
bpy.context.scene.collection.objects.link(sun)
sun.rotation_euler = (math.radians(50), math.radians(20), 0)

# Camera - front 3/4 view
cam_data = bpy.data.cameras.new('Camera')
cam = bpy.data.objects.new('Camera', cam_data)
bpy.context.scene.collection.objects.link(cam)
bpy.context.scene.camera = cam

cam.location = (-2, -3, 1.3)
cam.rotation_euler = (math.radians(75), 0, math.radians(-30))

# Render
bpy.context.scene.render.engine = 'BLENDER_EEVEE'
bpy.context.scene.render.resolution_x = 800
bpy.context.scene.render.resolution_y = 1000
bpy.context.scene.render.filepath = OUTPUT_PATH
bpy.ops.render.render(write_still=True)

print(f'\nSaved to: {OUTPUT_PATH}')
print('View at: http://localhost:5175/final_check.png')
