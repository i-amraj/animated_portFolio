import bpy
import json

# Load original character and extract its pose
ORIGINAL = '/home/ubuntu_16gb/raj_work_space/PERSONAL/newPort/Portfolio-Website/public/models/original-character.glb'

print('=' * 60)
print('EXTRACTING POSE FROM ORIGINAL CHARACTER')
print('=' * 60)

# Clear
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Import original
bpy.ops.import_scene.gltf(filepath=ORIGINAL)

# Find armature
armature = None
for obj in bpy.context.scene.objects:
    if obj.type == 'ARMATURE':
        armature = obj
        break

if not armature:
    print('ERROR: No armature!')
    exit(1)

print(f'\nArmature: {armature.name}')
print(f'\nBONES AND THEIR REST POSE:')
print('-' * 60)

# Get bone data
bpy.context.view_layer.objects.active = armature
bpy.ops.object.mode_set(mode='EDIT')

bone_data = {}
for bone in armature.data.edit_bones:
    head = bone.head.copy()
    tail = bone.tail.copy()
    roll = bone.roll
    
    parent_name = bone.parent.name if bone.parent else None
    
    bone_data[bone.name] = {
        'head': [head.x, head.y, head.z],
        'tail': [tail.x, tail.y, tail.z],
        'roll': roll,
        'parent': parent_name
    }
    print(f'{bone.name}:')
    print(f'  head: {head.x:.4f}, {head.y:.4f}, {head.z:.4f}')
    print(f'  tail: {tail.x:.4f}, {tail.y:.4f}, {tail.z:.4f}')

bpy.ops.object.mode_set(mode='OBJECT')

# Save to JSON
output_path = '/home/ubuntu_16gb/raj_work_space/PERSONAL/newPort/Portfolio-Website/scripts/original_pose.json'
with open(output_path, 'w') as f:
    json.dump(bone_data, f, indent=2)

print(f'\n\nSaved to: {output_path}')

# Also get animations
print('\n\nANIMATIONS:')
for action in bpy.data.actions:
    print(f'  - {action.name}')
