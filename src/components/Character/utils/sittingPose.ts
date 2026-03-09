import * as THREE from "three";

/**
 * Apply sitting pose to a character with Mixamo skeleton
 * Using quaternions for proper bone rotation
 */
export function applySittingPose(character: THREE.Object3D): void {
  console.log("Applying sitting pose...");
  
  const bones: Record<string, THREE.Bone> = {};
  
  // Collect all bones
  character.traverse((object) => {
    if (object instanceof THREE.Bone) {
      bones[object.name] = object;
    }
  });
  
  console.log("Found bones:", Object.keys(bones).join(", "));
  
  // Helper function to rotate bone
  const rotateBone = (name: string, x: number, y: number, z: number) => {
    const bone = bones[name];
    if (bone) {
      const euler = new THREE.Euler(
        THREE.MathUtils.degToRad(x),
        THREE.MathUtils.degToRad(y),
        THREE.MathUtils.degToRad(z),
        'XYZ'
      );
      bone.quaternion.setFromEuler(euler);
      console.log(`  ✓ ${name}: [${x}, ${y}, ${z}]`);
    }
  };
  
  // Apply sitting pose - ADJUSTED VALUES
  // Spine - slight forward lean
  rotateBone('Spine', 12, 0, 0);
  rotateBone('Spine1', 8, 0, 0);
  rotateBone('Spine2', 5, 0, 0);
  
  // Head looking at screen
  rotateBone('Neck', -8, 0, 0);
  rotateBone('Head', -10, 0, 0);
  
  // Legs - sitting position
  rotateBone('LeftUpLeg', -95, 5, 5);
  rotateBone('LeftLeg', 95, 0, 0);
  rotateBone('LeftFoot', 10, 0, 0);
  
  rotateBone('RightUpLeg', -95, -5, -5);
  rotateBone('RightLeg', 95, 0, 0);
  rotateBone('RightFoot', 10, 0, 0);
  
  // Arms - typing position
  rotateBone('LeftShoulder', 5, 0, 5);
  rotateBone('LeftArm', 50, 5, 35);
  rotateBone('LeftForeArm', 0, 45, 0);
  rotateBone('LeftHand', -10, 0, 10);
  
  rotateBone('RightShoulder', 5, 0, -5);
  rotateBone('RightArm', 50, -5, -35);
  rotateBone('RightForeArm', 0, -45, 0);
  rotateBone('RightHand', -10, 0, -10);
  
  // Position adjustment for sitting
  character.position.set(0, -0.5, 0);
  
  console.log("Sitting pose applied!");
}

/**
 * Animate typing motion on fingers
 */
export function createTypingAnimation(character: THREE.Object3D): () => void {
  const fingerBones: THREE.Bone[] = [];
  const fingerNames = [
    'LeftHandIndex1', 'LeftHandMiddle1', 'LeftHandRing1', 'LeftHandPinky1',
    'RightHandIndex1', 'RightHandMiddle1', 'RightHandRing1', 'RightHandPinky1'
  ];
  
  character.traverse((object) => {
    if (object instanceof THREE.Bone && fingerNames.includes(object.name)) {
      fingerBones.push(object);
    }
  });
  
  let time = 0;
  
  return function updateTyping() {
    time += 0.05;
    
    fingerBones.forEach((finger, index) => {
      // Stagger the animation for each finger
      const offset = index * 0.5;
      const flex = Math.sin(time * 3 + offset) * 0.3;
      finger.rotation.x = flex;
    });
  };
}
