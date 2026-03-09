import bpy
import math
import os

MODEL_PATH = '/home/ubuntu_16gb/raj_work_space/PERSONAL/newPort/Portfolio-Website/public/models/raj.glb'
OUTPUT_IMAGE = '/home/ubuntu_16gb/raj_work_space/PERSONAL/newPort/Portfolio-Website/public/pose_test.png'

print('=' * 60)
print('TESTING SITTING POSE IN BLENDER')
print('=' * 60)

# Clear scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Import model
print('\n[1/4] Importing model...')
bpy.ops.import_scene.gltf(filepath=MODEL_PATH)

# Find armature
armature = None
for obj in bpy.context.scene.objects:
    if obj.type == 'ARMATURE':
        armature = obj
        break

if not armature:
    print('ERROR: No armature found!')
    exit(1)

print(f'Found armature: {armature.name}')

# Select armature
bpy.ops.object.select_all(action='DESELECT')
armature.select_set(True)
bpy.context.view_layer.objects.active = armature

# Apply sitting pose
print('\n[2/4] Applying sitting pose...')
bpy.ops.object.mode_set(mode='POSE')

# Sitting pose values (same as sittingPose.ts)
SITTING_POSE = {
    'Spine': (15, 0, 0),
    'Spine1': (10, 0, 0),
    'Spine2': (5, 0, 0),
    'Neck': (-10, 0, 0),
    'Head': (-15, 0, 0),
    'LeftUpLeg': (-100, 8, 8),
    'LeftLeg': (100, 0, 0),
    'LeftFoot': (15, 0, 5),
    'RightUpLeg': (-100, -8, -8),
    'RightLeg': (100, 0, 0),
    'RightFoot': (15, 0, -5),
    'LeftShoulder': (0, 0, 8),
    'LeftArm': (55, 0, 40),
    'LeftForeArm': (0, 55, 0),
    'LeftHand': (0, -10, 15),
    'RightShoulder': (0, 0, -8),
    'RightArm': (55, 0, -40),
    'RightForeArm': (0, -55, 0),
    'RightHand': (0, 10, -15),
}

for bone_name, rotation in SITTING_POSE.items():
    if bone_name in armature.pose.bones:
        bone = armature.pose.bones[bone_name]
        bone.rotation_mode = 'XYZ'
        bone.rotation_euler = (
            math.radians(rotation[0]),
            math.radians(rotation[1]),
            math.radians(rotation[2])
        )
        print(f'  ✓ {bone_name}')
    else:
        print(f'  ✗ {bone_name} not found')

bpy.ops.object.mode_set(mode='OBJECT')

# Setup camera
print('\n[3/4] Setting up camera and render...')
cam_data = bpy.data.cameras.new('Camera')
cam = bpy.data.objects.new('Camera', cam_data)
bpy.context.scene.collection.objects.link(cam)
bpy.context.scene.camera = cam

# Position camera to see the character from front
cam.location = (0, -3, 1.2)
cam.rotation_euler = (math.radians(80), 0, 0)

# Add light
light_data = bpy.data.lights.new('Light', type='SUN')
light = bpy.data.objects.new('Light', light_data)
bpy.context.scene.collection.objects.link(light)
light.location = (2, -2, 3)

# Render settings
bpy.context.scene.render.engine = 'BLENDER_EEVEE'
bpy.context.scene.render.resolution_x = 800
bpy.context.scene.render.resolution_y = 1000
bpy.context.scene.render.filepath = OUTPUT_IMAGE
bpy.context.scene.render.image_settings.file_format = 'PNG'

# World background
world = bpy.data.worlds.new('World')
bpy.context.scene.world = world
world.use_nodes = True
world.node_tree.nodes['Background'].inputs[0].default_value = (0.1, 0.1, 0.15, 1)

# Render
print('\n[4/4] Rendering...')
bpy.ops.render.render(write_still=True)

print(f'\n✅ Render saved to: {OUTPUT_IMAGE}')
print('=' * 60)
