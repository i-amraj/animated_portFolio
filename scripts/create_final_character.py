import bpy
import math

MODEL_PATH = '/home/ubuntu_16gb/raj_work_space/PERSONAL/newPort/Portfolio-Website/public/models/raj.glb'
OUTPUT_PATH = '/home/ubuntu_16gb/raj_work_space/PERSONAL/newPort/Portfolio-Website/public/models/raj-final.glb'

print('=' * 60)
print('CREATING FINAL CHARACTER WITH BAKED SITTING POSE')
print('=' * 60)

# Clear scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Clear all existing actions
for action in bpy.data.actions:
    bpy.data.actions.remove(action)

# Import model
print('\n[1/4] Importing model...')
bpy.ops.import_scene.gltf(filepath=MODEL_PATH)

# Find armature and meshes
armature = None
meshes = []
for obj in bpy.context.scene.objects:
    if obj.type == 'ARMATURE':
        armature = obj
    elif obj.type == 'MESH':
        meshes.append(obj)

print(f'Found armature: {armature.name}')
print(f'Found {len(meshes)} meshes')

# Select armature
bpy.ops.object.select_all(action='DESELECT')
armature.select_set(True)
bpy.context.view_layer.objects.active = armature

# Clear animation data
if armature.animation_data:
    armature.animation_data.action = None

# Apply sitting pose
print('\n[2/4] Applying sitting pose...')
bpy.ops.object.mode_set(mode='POSE')

# Tested and verified sitting pose values
SITTING_POSE = {
    'Spine': (12, 0, 0),
    'Spine1': (8, 0, 0),
    'Spine2': (5, 0, 0),
    'Neck': (-8, 0, 0),
    'Head': (-10, 0, 0),
    'LeftUpLeg': (-95, 5, 5),
    'LeftLeg': (95, 0, 0),
    'LeftFoot': (10, 0, 0),
    'RightUpLeg': (-95, -5, -5),
    'RightLeg': (95, 0, 0),
    'RightFoot': (10, 0, 0),
    'LeftShoulder': (5, 0, 5),
    'LeftArm': (50, 5, 35),
    'LeftForeArm': (0, 45, 0),
    'LeftHand': (-10, 0, 10),
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
        print(f'  ✓ {bone_name}')

# Apply pose as rest pose
print('\n[3/4] Baking pose as rest pose...')
bpy.ops.pose.armature_apply(selected=False)

bpy.ops.object.mode_set(mode='OBJECT')

# Create basic animations
print('\n[3b/4] Creating animations...')
armature.animation_data_create()
bpy.ops.object.mode_set(mode='POSE')

# introAnimation - static sitting pose
intro_action = bpy.data.actions.new(name='introAnimation')
armature.animation_data.action = intro_action

for bone in armature.pose.bones:
    bone.keyframe_insert(data_path='rotation_euler', frame=1)
    bone.keyframe_insert(data_path='rotation_euler', frame=60)

print('  ✓ introAnimation')

# Blink animation
blink_action = bpy.data.actions.new(name='Blink')
armature.animation_data.action = blink_action

head = armature.pose.bones.get('Head')
if head:
    head.rotation_mode = 'XYZ'
    head.keyframe_insert(data_path='rotation_euler', frame=1)
    orig = list(head.rotation_euler)
    head.rotation_euler[0] += math.radians(2)
    head.keyframe_insert(data_path='rotation_euler', frame=8)
    head.rotation_euler = tuple(orig)
    head.keyframe_insert(data_path='rotation_euler', frame=16)

print('  ✓ Blink')

# browup animation
browup_action = bpy.data.actions.new(name='browup')
armature.animation_data.action = browup_action

if head:
    head.keyframe_insert(data_path='rotation_euler', frame=1)
    orig = list(head.rotation_euler)
    head.rotation_euler[0] -= math.radians(3)
    head.keyframe_insert(data_path='rotation_euler', frame=15)
    head.rotation_euler = tuple(orig)
    head.keyframe_insert(data_path='rotation_euler', frame=30)

print('  ✓ browup')

# typing animation - finger movements
typing_action = bpy.data.actions.new(name='typing')
armature.animation_data.action = typing_action

finger_bones = ['LeftHandIndex1', 'LeftHandMiddle1', 'RightHandIndex1', 'RightHandMiddle1']
for i, fname in enumerate(finger_bones):
    finger = armature.pose.bones.get(fname)
    if finger:
        finger.rotation_mode = 'XYZ'
        offset = i * 5
        
        finger.keyframe_insert(data_path='rotation_euler', frame=1 + offset)
        orig = list(finger.rotation_euler)
        finger.rotation_euler[0] += math.radians(20)
        finger.keyframe_insert(data_path='rotation_euler', frame=8 + offset)
        finger.rotation_euler = tuple(orig)
        finger.keyframe_insert(data_path='rotation_euler', frame=16 + offset)

print('  ✓ typing')

# key1-6 animations
for key_num in range(1, 7):
    key_action = bpy.data.actions.new(name=f'key{key_num}')
    armature.animation_data.action = key_action
    
    finger = armature.pose.bones.get(finger_bones[key_num % len(finger_bones)])
    if finger:
        finger.rotation_mode = 'XYZ'
        finger.keyframe_insert(data_path='rotation_euler', frame=1)
        orig = list(finger.rotation_euler)
        finger.rotation_euler[0] += math.radians(25)
        finger.keyframe_insert(data_path='rotation_euler', frame=5)
        finger.rotation_euler = tuple(orig)
        finger.keyframe_insert(data_path='rotation_euler', frame=10)

print('  ✓ key1-key6')

bpy.ops.object.mode_set(mode='OBJECT')

# Export
print('\n[4/4] Exporting...')
bpy.ops.object.select_all(action='SELECT')

bpy.ops.export_scene.gltf(
    filepath=OUTPUT_PATH,
    export_format='GLB',
    export_animations=True,
    export_skins=True,
)

print(f'\n✅ DONE! Saved to: {OUTPUT_PATH}')
print('=' * 60)
