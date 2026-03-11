import * as THREE from "three";
import { DRACOLoader, GLTF, GLTFLoader } from "three-stdlib";
import { setCharTimeline, setAllTimeline } from "../../utils/GsapScroll";

// Character position offset
const CHARACTER_Y_OFFSET = -0.7;

// Character scale (H=height, W=width)
const CHARACTER_SCALE = { x: 1.20, y: 1.30, z: 1.20 };

// Sitting pose
const SITTING_POSE: Record<string, [number, number, number]> = {
  'LeftUpLeg': [-86, 0, -180],
  'LeftLeg': [-98, 0, 0],
  'LeftFoot': [75, 2, 0],
  'RightUpLeg': [-92, 0, 180],
  'RightLeg': [-96, 11, -1],
  'RightFoot': [66, -2, 2],
  'LeftShoulder': [78, -3, -105],
  'LeftArm': [38, 41, 39],
  'LeftForeArm': [15, 4, 42],
  'LeftHand': [-13, 19, 12],
  'RightShoulder': [47, 11, 103],
  'RightArm': [60, 17, 15],
  'RightForeArm': [-80, -59, -119],
  'RightHand': [-12, -31, -7],
  'Hips': [8, 0, 0],
  'Spine': [-2, 0, 0],
  'Spine1': [-9, 0, 0],
  'Spine2': [-9, 0, 0],
  'Neck': [38, -2, 0],
  'Head': [-4, 0, 0],
};

function applySittingPose(character: THREE.Object3D) {
  character.traverse((obj) => {
    if ((obj as THREE.Bone).isBone) {
      const bone = obj as THREE.Bone;
      const rotation = SITTING_POSE[bone.name];
      if (rotation) {
        bone.rotation.set(
          THREE.MathUtils.degToRad(rotation[0]),
          THREE.MathUtils.degToRad(rotation[1]),
          THREE.MathUtils.degToRad(rotation[2])
        );
        console.log(`Applied ${bone.name}: ${rotation}`);
      }
    }
  });
  console.log("Sitting pose applied!");
}

const setCharacter = (
  renderer: THREE.WebGLRenderer,
  scene: THREE.Scene,
  camera: THREE.PerspectiveCamera
) => {
  const loader = new GLTFLoader();
  const dracoLoader = new DRACOLoader();
  dracoLoader.setDecoderPath("/draco/");
  loader.setDRACOLoader(dracoLoader);

  const loadCharacter = () => {
    return new Promise<GLTF | null>(async (resolve, reject) => {
      try {
        let character: THREE.Object3D;
        loader.load(
          "/models/raj.glb",  // Original model - pose applied at runtime
          async (gltf) => {
            character = gltf.scene;

            // Hide monitor, frame, screenlight immediately before any render
            // Use direct children loop since getObjectByName might miss dot-named objects
            character.children.forEach((child: any) => {
              if (["Plane.004", "Cube.002", "screenlight"].includes(child.name)) {
                child.visible = false;
                console.log("Hidden:", child.name);
              }
            });

            // Apply sitting pose
            applySittingPose(character);

            // Move only the Armature (avatar), not desk/chair
            const armature = character.getObjectByName("Armature");
            if (armature) {
              // Store original scale and multiply by our scale factor
              const originalScale = {
                x: armature.scale.x,
                y: armature.scale.y,
                z: armature.scale.z
              };
              console.log("Original armature scale:", originalScale);

              // SET position directly (same as pose-tester)
              armature.position.y = CHARACTER_Y_OFFSET;

              // Apply scale as multiplier of original
              armature.scale.set(
                originalScale.x * CHARACTER_SCALE.x,
                originalScale.y * CHARACTER_SCALE.y,
                originalScale.z * CHARACTER_SCALE.z
              );
              console.log("Moved to y:", CHARACTER_Y_OFFSET, "Scaled to:", armature.scale);
            }

            await renderer.compileAsync(character, camera, scene);
            character.traverse((child: any) => {
              if (child.isMesh) {
                const mesh = child as THREE.Mesh;
                child.castShadow = true;
                child.receiveShadow = true;
                mesh.frustumCulled = true;
              }
            });
            resolve(gltf);
            setCharTimeline(character, camera);
            setAllTimeline();

            // Try to set foot positions if they exist
            const footR = character.getObjectByName("footR");
            const footL = character.getObjectByName("footL");
            if (footR) footR.position.y = 3.36;
            if (footL) footL.position.y = 3.36;

            dracoLoader.dispose();
          },
          undefined,
          (error) => {
            console.error("Error loading GLTF model:", error);
            reject(error);
          }
        );
      } catch (err) {
        reject(err);
        console.error(err);
      }
    });
  };

  return { loadCharacter };
};

export default setCharacter;
