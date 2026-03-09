import bpy
import math
from mathutils import Euler

INPUT_FILE = '/home/ubuntu_16gb/raj_work_space/PERSONAL/newPort/Portfolio-Website/public/models/raj.glb'
OUTPUT_FILE = '/home/ubuntu_16gb/raj_work_space/PERSONAL/newPort/Portfolio-Website/public/models/raj-sitting.glb'

print('=' * 60)
print('FIXING SITTING POSE - APPLYING AS REST POSE')
print('=' * 60)

# Clear scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Clear all actions
for action in bpy.data.actions:
    bpy.data.actions.remove(action)

# Import model
print('\n[1/6] Importing model...')
bpy.ops.import_scene.gltf(filepath=INPUT_FILE)

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

# Select only armature
bpy.ops.object.select_all(action='DESELECT')
armature.select_set(True)
bpy.context.view_layer.objects.active = armature

# Clear all existing animations first
if armature.animation_data:
    armature.animation_data.action = None

# Sitting pose - more aggressive rotations
SITTING_POSE = {
    # Hips - lower and rotate for sitting
    'Hips': (0, 0, 0),
    
    # Spine - lean forward slightly
    'Spine': (15, 0, 0),
    'Spine1': (10, 0, 0),
    'Spine2': (5, 0, 0),
    
    # Neck and Head - looking at screen
    'Neck': (-10, 0, 0),
    'Head': (-15, 0, 0),
    
    # Left leg - bent 90 degrees for sitting
    'LeftUpLeg': (-90, 10, 10),
    'LeftLeg': (85, 0, 0),
    'LeftFoot': (15, 0, 5),
    'LeftToeBase': (0, 0, 0),
    
    # Right leg - bent 90 degrees for sitting
    'RightUpLeg': (-90, -10, -10),
    'RightLeg': (85, 0, 0),
    'RightFoot': (15, 0, -5),
    'RightToeBase': (0, 0, 0),
    
    # Left arm - typing position (lowered, bent at elbow)
    'LeftShoulder': (0, 0, 10),
    'LeftArm': (45, 0, 40),  # Arm down and forward
    'LeftForeArm': (0, 50, 0),  # Elbow bent
    'LeftHand': (0, 0, 10),
    
    # Right arm - typing position
    'RightShoulder': (0, 0, -10),
    'RightArm': (45, 0, -40),
    'RightForeArm': (0, -50, 0),
    'RightHand': (0, 0, -10),
}

# Go to pose mode and apply sitting pose
print('\n[2/6] Applying sitting pose to bones...')
bpy.ops.object.mode_set(mode='POSE')

for bone_name, rotation in SITTING_POSE.items():
    if bone_name in armature.pose.bones:
        bone = armature.pose.bones[bone_name]
        bone.rotation_mode = 'XYZ'
        bone.rotation_euler = Euler((
            math.radians(rotation[0]),
            math.radians(rotation[1]),
            math.radians(rotation[2])
        ), 'XYZ')
        print(f'  ✓ {bone_name}: {rotation}')
    else:
        print(f'  ✗ {bone_name} not found')

# Update the scene
bpy.context.view_layer.update()

# IMPORTANT: Apply pose as rest pose
print('\n[3/6] Applying pose as REST POSE...')
bpy.ops.pose.armature_apply(selected=False)
print('  ✓ Pose applied as rest pose')

# Back to object mode
bpy.ops.object.mode_set(mode='OBJECT')

# Now create animations based on this new rest pose
print('\n[4/6] Creating animations...')

# Ensure animation data exists
if not armature.animation_data:
    armature.animation_data_create()

bpy.ops.object.mode_set(mode='POSE')

# Create introAnimation (static pose)
intro_action = bpy.data.actions.new(name='introAnimation')
armature.animation_data.action = intro_action

bpy.context.scene.frame_set(1)
for bone in armature.pose.bones:
    bone.keyframe_insert(data_path='rotation_euler', frame=1)
    bone.keyframe_insert(data_path='location', frame=1)

bpy.context.scene.frame_set(60)
for bone in armature.pose.bones:
    bone.keyframe_insert(data_path='rotation_euler', frame=60)
    bone.keyframe_insert(data_path='location', frame=60)

print('  ✓ introAnimation')

# Create Blink animation
blink_action = bpy.data.actions.new(name='Blink')
armature.animation_data.action = blink_action

head = armature.pose.bones.get('Head')
if head:
    head.rotation_mode = 'XYZ'
    bpy.context.scene.frame_set(1)
    head.keyframe_insert(data_path='rotation_euler', frame=1)
    
    bpy.context.scene.frame_set(8)
    orig_rot = list(head.rotation_euler)
    head.rotation_euler[0] += math.radians(3)
    head.keyframe_insert(data_path='rotation_euler', frame=8)
    
    bpy.context.scene.frame_set(16)
    head.rotation_euler = Euler(orig_rot, 'XYZ')
    head.keyframe_insert(data_path='rotation_euler', frame=16)

print('  ✓ Blink')

# Create browup animation
browup_action = bpy.data.actions.new(name='browup')
armature.animation_data.action = browup_action

if head:
    bpy.context.scene.frame_set(1)
    head.keyframe_insert(data_path='rotation_euler', frame=1)
    
    bpy.context.scene.frame_set(15)
    orig_rot = list(head.rotation_euler)
    head.rotation_euler[0] -= math.radians(5)
    head.keyframe_insert(data_path='rotation_euler', frame=15)
    
    bpy.context.scene.frame_set(30)
    head.rotation_euler = Euler(orig_rot, 'XYZ')
    head.keyframe_insert(data_path='rotation_euler', frame=30)

print('  ✓ browup')

# Create typing animation - animate fingers
typing_action = bpy.data.actions.new(name='typing')
armature.animation_data.action = typing_action

# Finger bones for typing
left_fingers = ['LeftHandIndex1', 'LeftHandIndex2', 'LeftHandMiddle1', 'LeftHandMiddle2', 
                'LeftHandRing1', 'LeftHandPinky1']
right_fingers = ['RightHandIndex1', 'RightHandIndex2', 'RightHandMiddle1', 'RightHandMiddle2',
                 'RightHandRing1', 'RightHandPinky1']

all_fingers = left_fingers + right_fingers

for i, finger_name in enumerate(all_fingers):
    finger = armature.pose.bones.get(finger_name)
    if finger:
        finger.rotation_mode = 'XYZ'
        offset = (i % 6) * 4  # Stagger timing
        
        # Rest position
        bpy.context.scene.frame_set(1 + offset)
        finger.keyframe_insert(data_path='rotation_euler', frame=1 + offset)
        
        # Press down
        bpy.context.scene.frame_set(8 + offset)
        orig = list(finger.rotation_euler)
        finger.rotation_euler[0] += math.radians(25)
        finger.keyframe_insert(data_path='rotation_euler', frame=8 + offset)
        
        # Back up
        bpy.context.scene.frame_set(16 + offset)
        finger.rotation_euler = Euler(orig, 'XYZ')
        finger.keyframe_insert(data_path='rotation_euler', frame=16 + offset)
        
        # Loop back
        bpy.context.scene.frame_set(48 + offset)
        finger.keyframe_insert(data_path='rotation_euler', frame=48 + offset)

print('  ✓ typing')

# Create key animations (key1-key6)
for key_num in range(1, 7):
    key_action = bpy.data.actions.new(name=f'key{key_num}')
    armature.animation_data.action = key_action
    
    # Pick a finger based on key number
    finger_idx = (key_num - 1) % len(all_fingers)
    finger_name = all_fingers[finger_idx]
    finger = armature.pose.bones.get(finger_name)
    
    if finger:
        finger.rotation_mode = 'XYZ'
        
        bpy.context.scene.frame_set(1)
        finger.keyframe_insert(data_path='rotation_euler', frame=1)
        
        bpy.context.scene.frame_set(5)
        orig = list(finger.rotation_euler)
        finger.rotation_euler[0] += math.radians(30)
        finger.keyframe_insert(data_path='rotation_euler', frame=5)
        
        bpy.context.scene.frame_set(10)
        finger.rotation_euler = Euler(orig, 'XYZ')
        finger.keyframe_insert(data_path='rotation_euler', frame=10)

print('  ✓ key1-key6')

bpy.ops.object.mode_set(mode='OBJECT')

# Export
print('\n[5/6] Exporting...')
bpy.ops.object.select_all(action='SELECT')

bpy.ops.export_scene.gltf(
    filepath=OUTPUT_FILE,
    export_format='GLB',
    export_animations=True,
    export_skins=True,
    export_morph=True,
    export_rest_position_armature=False,  # Use current pose, not rest
)

print('\n[6/6] Verifying...')
print(f'Output: {OUTPUT_FILE}')
print('\nAnimations exported:')
for action in bpy.data.actions:
    print(f'  - {action.name}')

print('\n' + '=' * 60)
print('✅ DONE!')
print('=' * 60)
