import * as THREE from "three";

// Bone name variants (different models use different naming conventions)
const BONE_NAMES = {
  head: ['Head', 'head', 'spine006', 'spine.006', 'Neck', 'mixamorigHead'],
  spine: ['Spine', 'spine', 'Spine1', 'mixamorigSpine'],
  spine1: ['Spine1', 'spine.001', 'Chest', 'mixamorigSpine1'],
  spine2: ['Spine2', 'spine.002', 'UpperChest', 'mixamorigSpine2'],
  hips: ['Hips', 'hips', 'pelvis', 'mixamorigHips'],
  
  // Left Leg
  leftUpLeg: ['LeftUpLeg', 'thigh.L', 'ThighL', 'mixamorigLeftUpLeg', 'upperleg_l', 'Thigh_L'],
  leftLeg: ['LeftLeg', 'shin.L', 'ShinL', 'mixamorigLeftLeg', 'lowerleg_l', 'Shin_L'],
  leftFoot: ['LeftFoot', 'foot.L', 'FootL', 'mixamorigLeftFoot'],
  
  // Right Leg
  rightUpLeg: ['RightUpLeg', 'thigh.R', 'ThighR', 'mixamorigRightUpLeg', 'upperleg_r', 'Thigh_R'],
  rightLeg: ['RightLeg', 'shin.R', 'ShinR', 'mixamorigRightLeg', 'lowerleg_r', 'Shin_R'],
  rightFoot: ['RightFoot', 'foot.R', 'FootR', 'mixamorigRightFoot'],
  
  // Left Arm
  leftShoulder: ['LeftShoulder', 'shoulder.L', 'mixamorigLeftShoulder'],
  leftArm: ['LeftArm', 'upper_arm.L', 'mixamorigLeftArm', 'upperarm_l', 'Arm_L'],
  leftForeArm: ['LeftForeArm', 'forearm.L', 'mixamorigLeftForeArm', 'lowerarm_l', 'ForeArm_L'],
  leftHand: ['LeftHand', 'hand.L', 'mixamorigLeftHand'],
  
  // Right Arm
  rightShoulder: ['RightShoulder', 'shoulder.R', 'mixamorigRightShoulder'],
  rightArm: ['RightArm', 'upper_arm.R', 'mixamorigRightArm', 'upperarm_r', 'Arm_R'],
  rightForeArm: ['RightForeArm', 'forearm.R', 'mixamorigRightForeArm', 'lowerarm_r', 'ForeArm_R'],
  rightHand: ['RightHand', 'hand.R', 'mixamorigRightHand'],
};

// Sitting pose rotations (in radians)
// Adjust these values based on your model's bone orientations
const SITTING_POSE: Record<string, { x: number; y: number; z: number }> = {
  // Spine - slight forward lean
  spine: { x: 0.1, y: 0, z: 0 },
  spine1: { x: 0.05, y: 0, z: 0 },
  
  // Left leg - bent at hip and knee for sitting
  leftUpLeg: { x: -1.57, y: 0.15, z: 0.1 },   // -90 degrees at hip
  leftLeg: { x: 1.57, y: 0, z: 0 },            // 90 degrees at knee
  leftFoot: { x: 0.2, y: 0, z: 0 },
  
  // Right leg
  rightUpLeg: { x: -1.57, y: -0.15, z: -0.1 }, // -90 degrees at hip
  rightLeg: { x: 1.57, y: 0, z: 0 },            // 90 degrees at knee
  rightFoot: { x: 0.2, y: 0, z: 0 },
  
  // Left arm - typing position
  leftShoulder: { x: 0, y: 0, z: 0.1 },
  leftArm: { x: 0.6, y: 0, z: 0.3 },
  leftForeArm: { x: -0.4, y: 0.3, z: 0 },
  leftHand: { x: -0.2, y: 0, z: 0 },
  
  // Right arm - typing position
  rightShoulder: { x: 0, y: 0, z: -0.1 },
  rightArm: { x: 0.6, y: 0, z: -0.3 },
  rightForeArm: { x: -0.4, y: -0.3, z: 0 },
  rightHand: { x: -0.2, y: 0, z: 0 },
};

// Find bone by checking multiple possible names
function findBone(bones: THREE.Bone[], key: keyof typeof BONE_NAMES): THREE.Bone | null {
  const possibleNames = BONE_NAMES[key];
  for (const name of possibleNames) {
    const bone = bones.find(b => 
      b.name === name || 
      b.name.toLowerCase() === name.toLowerCase() ||
      b.name.toLowerCase().includes(name.toLowerCase())
    );
    if (bone) return bone;
  }
  return null;
}

// Get all bones from the model
function getAllBones(object: THREE.Object3D): THREE.Bone[] {
  const bones: THREE.Bone[] = [];
  object.traverse((child) => {
    if ((child as THREE.Bone).isBone) {
      bones.push(child as THREE.Bone);
    }
  });
  return bones;
}

// Apply sitting pose to the character
export function applySittingPose(model: THREE.Object3D): THREE.Bone | null {
  const bones = getAllBones(model);
  const foundBones = new Map<string, THREE.Bone>();

  // Log all bones for debugging
  console.log("\n========================================");
  console.log("         MODEL BONES LIST              ");
  console.log("========================================");
  bones.forEach(b => console.log(`  📦 ${b.name}`));
  console.log("========================================\n");

  // Find all relevant bones
  console.log("🔍 Searching for bones...\n");
  for (const key of Object.keys(BONE_NAMES) as (keyof typeof BONE_NAMES)[]) {
    const bone = findBone(bones, key);
    if (bone) {
      foundBones.set(key, bone);
      console.log(`  ✅ Found ${key}: ${bone.name}`);
    } else {
      console.log(`  ❌ Missing: ${key}`);
    }
  }

  // Apply sitting pose
  console.log("\n🪑 Applying Sitting Pose...\n");
  let appliedCount = 0;
  for (const [key, rotation] of Object.entries(SITTING_POSE)) {
    const bone = foundBones.get(key);
    if (bone) {
      // Apply new rotation
      bone.rotation.set(rotation.x, rotation.y, rotation.z);
      
      console.log(`  🦴 ${bone.name}: (${rotation.x.toFixed(2)}, ${rotation.y.toFixed(2)}, ${rotation.z.toFixed(2)})`);
      appliedCount++;
    }
  }
  console.log(`\n  Applied pose to ${appliedCount} bones\n`);

  // Get head bone for mouse tracking
  const headBone = foundBones.get('head');
  
  console.log("========================================");
  console.log(`🎯 Head bone: ${headBone?.name || 'NOT FOUND - Mouse follow disabled'}`);
  console.log("========================================\n");
  
  return headBone || null;
}

export default { applySittingPose };
