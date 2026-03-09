import bpy
import math

INPUT_FILE = '/home/ubuntu_16gb/raj_work_space/PERSONAL/newPort/Portfolio-Website/public/models/raj.glb'
OUTPUT_FILE = '/home/ubuntu_16gb/raj_work_space/PERSONAL/newPort/Portfolio-Website/public/models/raj-sitting.glb'

print('=' * 60)
print('CREATING SITTING CHARACTER WITH ANIMATIONS')
print('=' * 60)

# Clear scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Import model
print('\n[1/5] Importing model...')
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

# Set armature as active
bpy.context.view_layer.objects.active = armature

# Sitting pose bone rotations (in degrees, will convert to radians)
SITTING_POSE = {
    # Spine - slight forward lean
    'Spine': (10, 0, 0),
    'Spine1': (5, 0, 0),
    'Spine2': (5, 0, 0),
    
    # Head - looking at screen
    'Neck': (-5, 0, 0),
    'Head': (-10, 0, 0),
    
    # Left leg - sitting
    'LeftUpLeg': (-90, 5, 5),
    'LeftLeg': (90, 0, 0),
    'LeftFoot': (10, 0, 0),
    
    # Right leg - sitting
    'RightUpLeg': (-90, -5, -5),
    'RightLeg': (90, 0, 0),
    'RightFoot': (10, 0, 0),
    
    # Left arm - typing position
    'LeftShoulder': (0, 0, 5),
    'LeftArm': (50, 0, 25),
    'LeftForeArm': (-30, 20, 0),
    'LeftHand': (-15, 0, 0),
    
    # Right arm - typing position
    'RightShoulder': (0, 0, -5),
    'RightArm': (50, 0, -25),
    'RightForeArm': (-30, -20, 0),
    'RightHand': (-15, 0, 0),
}

# Apply sitting pose
print('\n[2/5] Applying sitting pose...')
bpy.ops.object.mode_set(mode='POSE')

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
    else:
        print(f'  ✗ {bone_name} not found')

# Create introAnimation (current pose as keyframe)
print('\n[3/5] Creating introAnimation...')

# Create new action for intro
intro_action = bpy.data.actions.new(name='introAnimation')
armature.animation_data_create()

# Store current action
original_action = armature.animation_data.action

# Set intro action
armature.animation_data.action = intro_action

# Insert keyframes for all bones at frame 1 (static pose)
bpy.context.scene.frame_set(1)
for bone in armature.pose.bones:
    bone.keyframe_insert(data_path='rotation_euler', frame=1)
    bone.keyframe_insert(data_path='location', frame=1)

# Also at frame 60 (same pose - static)
bpy.context.scene.frame_set(60)
for bone in armature.pose.bones:
    bone.keyframe_insert(data_path='rotation_euler', frame=60)
    bone.keyframe_insert(data_path='location', frame=60)

print('  ✓ introAnimation created (60 frames)')

# Create Blink animation
print('\n[4/5] Creating Blink animation...')

blink_action = bpy.data.actions.new(name='Blink')
armature.animation_data.action = blink_action

# Simple blink - just head bone slight movement (placeholder)
# Real blink would need shape keys which we don't have
head_bone = armature.pose.bones.get('Head')
if head_bone:
    head_bone.rotation_mode = 'XYZ'
    
    # Frame 1 - normal
    bpy.context.scene.frame_set(1)
    head_bone.rotation_euler = (math.radians(-10), 0, 0)
    head_bone.keyframe_insert(data_path='rotation_euler', frame=1)
    
    # Frame 10 - slight nod (blink gesture)
    bpy.context.scene.frame_set(10)
    head_bone.rotation_euler = (math.radians(-12), 0, 0)
    head_bone.keyframe_insert(data_path='rotation_euler', frame=10)
    
    # Frame 20 - back to normal
    bpy.context.scene.frame_set(20)
    head_bone.rotation_euler = (math.radians(-10), 0, 0)
    head_bone.keyframe_insert(data_path='rotation_euler', frame=20)
    
    print('  ✓ Blink animation created')

# Create typing animation (body movement while typing)
print('\n[4b/5] Creating typing animation...')

typing_action = bpy.data.actions.new(name='typing')
armature.animation_data.action = typing_action

# Animate fingers slightly for typing feel
fingers = ['LeftHandIndex1', 'LeftHandMiddle1', 'RightHandIndex1', 'RightHandMiddle1']

for i, finger_name in enumerate(fingers):
    finger = armature.pose.bones.get(finger_name)
    if finger:
        finger.rotation_mode = 'XYZ'
        
        # Offset timing for each finger
        offset = i * 5
        
        # Up position
        bpy.context.scene.frame_set(1 + offset)
        finger.rotation_euler = (0, 0, 0)
        finger.keyframe_insert(data_path='rotation_euler', frame=1 + offset)
        
        # Down position (pressing key)
        bpy.context.scene.frame_set(10 + offset)
        finger.rotation_euler = (math.radians(30), 0, 0)
        finger.keyframe_insert(data_path='rotation_euler', frame=10 + offset)
        
        # Back up
        bpy.context.scene.frame_set(20 + offset)
        finger.rotation_euler = (0, 0, 0)
        finger.keyframe_insert(data_path='rotation_euler', frame=20 + offset)

print('  ✓ typing animation created')

# Create browup animation
print('\n[4c/5] Creating browup animation...')

browup_action = bpy.data.actions.new(name='browup')
armature.animation_data.action = browup_action

# Use head bone for eyebrow raise effect
if head_bone:
    # Frame 1 - normal
    bpy.context.scene.frame_set(1)
    head_bone.rotation_euler = (math.radians(-10), 0, 0)
    head_bone.keyframe_insert(data_path='rotation_euler', frame=1)
    
    # Frame 15 - raised (slight head tilt back)
    bpy.context.scene.frame_set(15)
    head_bone.rotation_euler = (math.radians(-5), 0, 0)
    head_bone.keyframe_insert(data_path='rotation_euler', frame=15)
    
    # Frame 30 - back to normal
    bpy.context.scene.frame_set(30)
    head_bone.rotation_euler = (math.radians(-10), 0, 0)
    head_bone.keyframe_insert(data_path='rotation_euler', frame=30)
    
    print('  ✓ browup animation created')

# Reset to frame 1
bpy.context.scene.frame_set(1)
bpy.ops.object.mode_set(mode='OBJECT')

# Export
print('\n[5/5] Exporting model...')
bpy.ops.object.select_all(action='SELECT')

bpy.ops.export_scene.gltf(
    filepath=OUTPUT_FILE,
    export_format='GLB',
    export_animations=True,
    export_skins=True,
    export_morph=True,
)

print('\n' + '=' * 60)
print('✅ DONE!')
print(f'Output: {OUTPUT_FILE}')
print('=' * 60)

# List all animations in final file
print('\nAnimations in exported file:')
for action in bpy.data.actions:
    print(f'  - {action.name}')
