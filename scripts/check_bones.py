import bpy
import math

# Load the final model and check bone rotations
MODEL_PATH = '/home/ubuntu_16gb/raj_work_space/PERSONAL/newPort/Portfolio-Website/public/models/raj-final.glb'

print('CHECKING FINAL MODEL BONE POSITIONS')
print('=' * 60)

# Clear
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Import
bpy.ops.import_scene.gltf(filepath=MODEL_PATH)

# Find armature
armature = None
for obj in bpy.context.scene.objects:
    if obj.type == 'ARMATURE':
        armature = obj
        break

print(f'Armature: {armature.name}\n')

# Check key bone positions
key_bones = ['Hips', 'Spine', 'Spine1', 'Head', 'LeftUpLeg', 'LeftLeg', 'RightUpLeg', 'RightLeg', 'LeftArm', 'LeftForeArm', 'RightArm', 'RightForeArm']

bpy.context.view_layer.objects.active = armature
bpy.ops.object.mode_set(mode='POSE')

print('BONE REST ROTATIONS (in degrees):')
print('-' * 60)

for bone_name in key_bones:
    if bone_name in armature.pose.bones:
        bone = armature.pose.bones[bone_name]
        
        # Get rest position from edit bones
        bpy.ops.object.mode_set(mode='EDIT')
        if bone_name in armature.data.edit_bones:
            edit_bone = armature.data.edit_bones[bone_name]
            head = edit_bone.head.copy()
            tail = edit_bone.tail.copy()
            
            # Calculate direction
            direction = tail - head
            
            print(f'{bone_name}:')
            print(f'  Head: ({head.x:.2f}, {head.y:.2f}, {head.z:.2f})')
            print(f'  Tail: ({tail.x:.2f}, {tail.y:.2f}, {tail.z:.2f})')
            print(f'  Direction: ({direction.x:.2f}, {direction.y:.2f}, {direction.z:.2f})')
        
        bpy.ops.object.mode_set(mode='POSE')

bpy.ops.object.mode_set(mode='OBJECT')

# Check if LeftUpLeg is pointing forward (sitting) or down (standing)
bpy.ops.object.mode_set(mode='EDIT')
left_up_leg = armature.data.edit_bones.get('LeftUpLeg')
if left_up_leg:
    direction = left_up_leg.tail - left_up_leg.head
    if abs(direction.y) > abs(direction.z):
        print('\n✅ LeftUpLeg is pointing FORWARD (SITTING POSE)')
    else:
        print('\n❌ LeftUpLeg is pointing DOWN (STANDING/T-POSE)')

bpy.ops.object.mode_set(mode='OBJECT')
print('\n' + '=' * 60)
