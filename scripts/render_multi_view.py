import bpy
import math

MODEL_PATH = '/home/ubuntu_16gb/raj_work_space/PERSONAL/newPort/Portfolio-Website/public/models/raj.glb'
OUTPUT_DIR = '/home/ubuntu_16gb/raj_work_space/PERSONAL/newPort/Portfolio-Website/public/'

print('=' * 60)
print('RENDERING MULTIPLE VIEWS')
print('=' * 60)

# Clear scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Import model
print('\n[1/5] Importing model...')
bpy.ops.import_scene.gltf(filepath=MODEL_PATH)

# Find armature
armature = None
for obj in bpy.context.scene.objects:
    if obj.type == 'ARMATURE':
        armature = obj
        break

print(f'Found armature: {armature.name}')

# Select armature
bpy.ops.object.select_all(action='DESELECT')
armature.select_set(True)
bpy.context.view_layer.objects.active = armature

# Apply sitting pose with adjusted values
print('\n[2/5] Applying sitting pose...')
bpy.ops.object.mode_set(mode='POSE')

# Better sitting pose values - adjusted for Mixamo bone orientations
SITTING_POSE = {
    # Spine - slight forward lean
    'Spine': (12, 0, 0),
    'Spine1': (8, 0, 0),
    'Spine2': (5, 0, 0),
    
    # Head
    'Neck': (-8, 0, 0),
    'Head': (-10, 0, 0),
    
    # Left leg - sitting
    # LeftUpLeg X rotation bends the thigh forward
    # Mixamo bones: positive X = forward rotation
    'LeftUpLeg': (-95, 5, 5),
    'LeftLeg': (95, 0, 0),  # Bend knee
    'LeftFoot': (10, 0, 0),
    
    # Right leg
    'RightUpLeg': (-95, -5, -5),
    'RightLeg': (95, 0, 0),
    'RightFoot': (10, 0, 0),
    
    # Left arm - lowered and bent for typing
    'LeftShoulder': (5, 0, 5),
    'LeftArm': (50, 5, 35),     # Arm down
    'LeftForeArm': (0, 45, 0),  # Elbow bent
    'LeftHand': (-10, 0, 10),
    
    # Right arm - mirrored
    'RightShoulder': (5, 0, -5),
    'RightArm': (50, -5, -35),
    'RightForeArm': (0, -45, 0),
    'RightHand': (-10, 0, -10),
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
        print(f'  ✓ {bone_name}: {rotation}')

bpy.ops.object.mode_set(mode='OBJECT')

# Setup world
print('\n[3/5] Setting up scene...')
world = bpy.data.worlds.new('World')
bpy.context.scene.world = world
world.use_nodes = True
world.node_tree.nodes['Background'].inputs[0].default_value = (0.15, 0.15, 0.2, 1)

# Add light
light_data = bpy.data.lights.new('Sun', type='SUN')
light_data.energy = 2
light = bpy.data.objects.new('Sun', light_data)
bpy.context.scene.collection.objects.link(light)
light.rotation_euler = (math.radians(45), math.radians(30), 0)

# Add fill light
fill_data = bpy.data.lights.new('Fill', type='AREA')
fill_data.energy = 100
fill = bpy.data.objects.new('Fill', fill_data)
bpy.context.scene.collection.objects.link(fill)
fill.location = (-2, -2, 1.5)
fill.rotation_euler = (math.radians(60), 0, math.radians(-45))

# Setup camera
cam_data = bpy.data.cameras.new('Camera')
cam = bpy.data.objects.new('Camera', cam_data)
bpy.context.scene.collection.objects.link(cam)
bpy.context.scene.camera = cam

# Render settings
bpy.context.scene.render.engine = 'BLENDER_EEVEE'
bpy.context.scene.render.resolution_x = 600
bpy.context.scene.render.resolution_y = 800
bpy.context.scene.render.image_settings.file_format = 'PNG'

# Render multiple views
print('\n[4/5] Rendering views...')

views = [
    ('front', (0, -3.5, 1), (80, 0, 0)),
    ('side', (-3.5, 0, 1), (80, 0, -90)),
    ('quarter', (-2.5, -2.5, 1.2), (75, 0, -45)),
]

for view_name, cam_loc, cam_rot in views:
    cam.location = cam_loc
    cam.rotation_euler = (math.radians(cam_rot[0]), math.radians(cam_rot[1]), math.radians(cam_rot[2]))
    
    output_path = f'{OUTPUT_DIR}pose_{view_name}.png'
    bpy.context.scene.render.filepath = output_path
    bpy.ops.render.render(write_still=True)
    print(f'  ✓ {view_name}: {output_path}')

print('\n[5/5] Done!')
print('=' * 60)
print('View renders at:')
print(f'  http://localhost:5175/pose_front.png')
print(f'  http://localhost:5175/pose_side.png')
print(f'  http://localhost:5175/pose_quarter.png')
print('=' * 60)
