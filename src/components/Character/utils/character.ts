import * as THREE from "three";
import { DRACOLoader, GLTF, GLTFLoader } from "three-stdlib";
import { setCharTimeline, setAllTimeline } from "../../utils/GsapScroll";

// Character Y position adjustment (negative = down, positive = up)
const CHARACTER_Y_OFFSET = -2.5;  // Adjust this value to move character up/down

// Sitting pose from pose tester
const SITTING_POSE: Record<string, [number, number, number]> = {
  'LeftUpLeg': [3, 19, -159],
  'LeftLeg': [-62, 28, 0],
  'LeftFoot': [44, -21, 0],
  'RightUpLeg': [9, 0, -173],
  'RightLeg': [-67, 12, 0],
  'RightFoot': [70, 10, 2],
  'LeftArm': [48, 175, -3],
  'LeftForeArm': [-33, -175, 75],
  'LeftHand': [62, 90, -17],
  'RightArm': [40, 74, -24],
  'RightForeArm': [96, -85, -10],
  'RightHand': [3, 0, 1],
  'Hips': [-75, 0, 0],
  'Spine': [83, 0, 0],
  'Spine1': [-8, 0, 0],
  'Spine2': [-9, 0, 0],
  'Neck': [28, 0, 0],
  'Head': [-13, 0, 0],
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
            
            // Apply sitting pose
            applySittingPose(character);
            
            // Move only the Armature (avatar), not desk/chair
            const armature = character.getObjectByName("Armature");
            if (armature) {
              armature.position.y += CHARACTER_Y_OFFSET;
              console.log("Moved only Armature by", CHARACTER_Y_OFFSET);
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
