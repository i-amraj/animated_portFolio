import bpy
import os

# File paths
ORIGINAL_CHAR = "/home/ubuntu_16gb/raj_work_space/PERSONAL/newPort/Portfolio-Website/public/models/original-character.glb"
USER_AVATAR = "/home/ubuntu_16gb/raj_work_space/PERSONAL/newPort/Portfolio-Website/raj_avatar/model (1).glb"
OUTPUT_FILE = "/home/ubuntu_16gb/raj_work_space/PERSONAL/newPort/Portfolio-Website/public/models/raj-final-character.glb"

print("=" * 60)
print("FACE SWAP SCRIPT")
print("=" * 60)

# Step 1: Clear scene
print("\n[1/7] Clearing scene...")
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Clear orphan data
for block in bpy.data.meshes:
    if block.users == 0:
        bpy.data.meshes.remove(block)
for block in bpy.data.armatures:
    if block.users == 0:
        bpy.data.armatures.remove(block)

# Step 2: Import original character
print("\n[2/7] Importing original character...")
bpy.ops.import_scene.gltf(filepath=ORIGINAL_CHAR)

# Get original character objects
original_armature = None
original_meshes = []

for obj in bpy.context.scene.objects:
    if obj.type == 'ARMATURE':
        original_armature = obj
        print(f"  Found armature: {obj.name}")
    elif obj.type == 'MESH':
        original_meshes.append(obj)
        print(f"  Found mesh: {obj.name}")

if not original_armature:
    print("ERROR: No armature found in original character!")
    exit(1)

print(f"\n  Original meshes: {[m.name for m in original_meshes]}")

# Store animation data
print("\n[3/7] Storing animation data...")
animations_count = 0
if original_armature.animation_data:
    if original_armature.animation_data.action:
        print(f"  Action: {original_armature.animation_data.action.name}")
        animations_count += 1

# List all actions in file
print("  All actions in file:")
for action in bpy.data.actions:
    print(f"    - {action.name}")
    animations_count += 1

print(f"  Total animations: {animations_count}")

# Step 4: Find head-related mesh in original
print("\n[4/7] Finding head mesh in original...")
head_mesh = None
body_mesh = None

for mesh in original_meshes:
    name_lower = mesh.name.lower()
    if 'head' in name_lower or 'face' in name_lower:
        head_mesh = mesh
        print(f"  Head mesh found: {mesh.name}")
    else:
        body_mesh = mesh

# If no specific head mesh, look at vertex groups
if not head_mesh and len(original_meshes) == 1:
    print("  Single mesh model - will try to identify head vertices by bone weights")
    body_mesh = original_meshes[0]

# Step 5: Import user avatar
print("\n[5/7] Importing user avatar...")

# Rename original objects to avoid conflicts
for obj in list(bpy.context.scene.objects):
    if obj.type == 'ARMATURE':
        obj.name = "Original_" + obj.name
    elif obj.type == 'MESH':
        obj.name = "Original_" + obj.name

bpy.ops.import_scene.gltf(filepath=USER_AVATAR)

# Find user avatar objects
user_armature = None
user_meshes = []

for obj in bpy.context.scene.objects:
    if not obj.name.startswith("Original_"):
        if obj.type == 'ARMATURE':
            user_armature = obj
            print(f"  User armature: {obj.name}")
        elif obj.type == 'MESH':
            user_meshes.append(obj)
            print(f"  User mesh: {obj.name}")

# Step 6: Swap head/face
print("\n[6/7] Performing face swap...")

# Find original armature again (name changed)
for obj in bpy.context.scene.objects:
    if obj.name.startswith("Original_") and obj.type == 'ARMATURE':
        original_armature = obj
        break

# Strategy: Delete user armature, parent user mesh to original armature
if user_armature:
    print(f"  Removing user armature: {user_armature.name}")
    bpy.data.objects.remove(user_armature, do_unlink=True)

# Find head bone in original armature
head_bone_name = None
for bone in original_armature.data.bones:
    bone_lower = bone.name.lower()
    if 'head' in bone_lower or 'spine006' in bone_lower:
        head_bone_name = bone.name
        print(f"  Head bone found: {bone.name}")
        break

# Delete original meshes (we'll use user's body)
print("  Removing original meshes...")
for mesh in list(bpy.context.scene.objects):
    if mesh.name.startswith("Original_") and mesh.type == 'MESH':
        print(f"    Removing: {mesh.name}")
        bpy.data.objects.remove(mesh, do_unlink=True)

# Parent user meshes to original armature
print("  Parenting user meshes to original armature...")
for mesh in user_meshes:
    # Select mesh and armature
    bpy.ops.object.select_all(action='DESELECT')
    mesh.select_set(True)
    original_armature.select_set(True)
    bpy.context.view_layer.objects.active = original_armature
    
    # Parent with automatic weights
    try:
        bpy.ops.object.parent_set(type='ARMATURE_AUTO')
        print(f"    Parented: {mesh.name}")
    except Exception as e:
        print(f"    Warning: Auto-weight failed for {mesh.name}, trying name...")
        try:
            bpy.ops.object.parent_set(type='ARMATURE_NAME')
            print(f"    Parented with name matching: {mesh.name}")
        except:
            # Manual parent
            mesh.parent = original_armature
            print(f"    Manually parented: {mesh.name}")

# Rename armature back
original_armature.name = original_armature.name.replace("Original_", "")

# Step 7: Export
print("\n[7/7] Exporting final character...")
bpy.ops.object.select_all(action='SELECT')

bpy.ops.export_scene.gltf(
    filepath=OUTPUT_FILE,
    export_format='GLB',
    export_animations=True,
    export_skins=True,
    export_morph=True,
    export_lights=False,
    export_cameras=False
)

print("\n" + "=" * 60)
print("✅ DONE!")
print(f"Output: {OUTPUT_FILE}")
print("=" * 60)
