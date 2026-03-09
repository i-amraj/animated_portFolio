import bpy

# Clear and import
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

bpy.ops.import_scene.gltf(filepath='/home/ubuntu_16gb/raj_work_space/PERSONAL/newPort/Portfolio-Website/public/models/raj.glb')

print('=' * 50)
print('MODEL ANALYSIS: raj.glb')
print('=' * 50)

# Find armature and list bones
for obj in bpy.context.scene.objects:
    if obj.type == 'ARMATURE':
        print(f'\nARMATURE: {obj.name}')
        print('BONES:')
        for bone in obj.data.bones:
            print(f'  - {bone.name}')

# List animations
print('\nANIMATIONS:')
if bpy.data.actions:
    for action in bpy.data.actions:
        print(f'  - {action.name}')
else:
    print('  (No animations found)')

print('=' * 50)
