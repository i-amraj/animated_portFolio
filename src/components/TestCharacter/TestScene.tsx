import { useEffect, useRef } from "react";
import * as THREE from "three";
import { GLTFLoader, DRACOLoader, OrbitControls } from "three-stdlib";
import { applySittingPose } from "./poseUtils";

const TestScene = () => {
  const canvasRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!canvasRef.current) return;

    // Setup
    const container = canvasRef.current;
    const width = container.clientWidth;
    const height = container.clientHeight;

    // Scene
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x1a1a2e);

    // Camera - moved further back to see full character
    const camera = new THREE.PerspectiveCamera(50, width / height, 0.1, 1000);
    camera.position.set(0, 1.2, 4);

    // Renderer
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    container.appendChild(renderer.domElement);

    // Orbit Controls - allows rotating/zooming with mouse
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.target.set(0, 0.8, 0); // Look at chest level
    controls.update();

    // Lights
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.7);
    scene.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xffffff, 1.2);
    directionalLight.position.set(5, 5, 5);
    scene.add(directionalLight);

    const backLight = new THREE.DirectionalLight(0xffffff, 0.5);
    backLight.position.set(-5, 3, -5);
    scene.add(backLight);

    const pointLight = new THREE.PointLight(0xc2a4ff, 1, 100);
    pointLight.position.set(0, 2, 2);
    scene.add(pointLight);

    // Grid Helper for reference
    const gridHelper = new THREE.GridHelper(4, 10, 0x444444, 0x222222);
    scene.add(gridHelper);

    // Load Model
    const loader = new GLTFLoader();
    const dracoLoader = new DRACOLoader();
    dracoLoader.setDecoderPath("/draco/");
    loader.setDRACOLoader(dracoLoader);

    let mixer: THREE.AnimationMixer | null = null;
    let headBone: THREE.Bone | null = null;

    loader.load(
      "/models/new-character.glb",
      (gltf) => {
        const model = gltf.scene;
        
        // Get model bounds BEFORE pose
        const box = new THREE.Box3().setFromObject(model);
        const size = box.getSize(new THREE.Vector3());
        const center = box.getCenter(new THREE.Vector3());
        
        console.log("Model size:", size);
        console.log("Model center:", center);
        
        // Scale to fit nicely (target height ~1.8 units)
        const targetHeight = 1.8;
        const currentHeight = size.y;
        const scale = targetHeight / currentHeight;
        model.scale.setScalar(scale);
        
        // Position model at ground level, centered
        model.position.set(0, 0, 0);
        model.position.x = -center.x * scale;
        model.position.z = -center.z * scale;
        // Put feet on ground (assuming model origin is at feet)
        model.position.y = -box.min.y * scale;
        
        scene.add(model);
        
        // Apply sitting pose AFTER adding to scene
        headBone = applySittingPose(model);
        
        // Setup animation mixer
        mixer = new THREE.AnimationMixer(model);
        
        // Play any existing animations
        if (gltf.animations.length > 0) {
          console.log("Animations found:", gltf.animations.map(a => a.name));
          gltf.animations.forEach(clip => {
            const action = mixer!.clipAction(clip);
            action.play();
          });
        } else {
          console.log("No animations in model");
        }
        
        console.log("✅ Model loaded successfully!");
        console.log("Scale applied:", scale);
        dracoLoader.dispose();
      },
      (progress) => {
        const percent = progress.total > 0 ? (progress.loaded / progress.total * 100).toFixed(0) : 'unknown';
        console.log(`Loading: ${percent}%`);
      },
      (error) => {
        console.error("Error loading model:", error);
      }
    );

    // Mouse tracking
    let mouse = { x: 0, y: 0 };
    const onMouseMove = (e: MouseEvent) => {
      mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
      mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;
    };
    window.addEventListener("mousemove", onMouseMove);

    // Animation loop
    const clock = new THREE.Clock();
    const animate = () => {
      requestAnimationFrame(animate);
      
      const delta = clock.getDelta();
      
      // Update controls
      controls.update();
      
      // Update animations
      if (mixer) mixer.update(delta);
      
      // Head follows mouse (only when not using orbit controls)
      if (headBone && !controls.enabled) {
        const maxRotY = Math.PI / 5;
        const maxRotX = Math.PI / 8;
        headBone.rotation.y = THREE.MathUtils.lerp(headBone.rotation.y, mouse.x * maxRotY, 0.1);
        headBone.rotation.x = THREE.MathUtils.lerp(headBone.rotation.x, -mouse.y * maxRotX, 0.1);
      }
      
      renderer.render(scene, camera);
    };
    animate();

    // Resize handler
    const onResize = () => {
      const w = container.clientWidth;
      const h = container.clientHeight;
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      renderer.setSize(w, h);
    };
    window.addEventListener("resize", onResize);

    // Cleanup
    return () => {
      window.removeEventListener("mousemove", onMouseMove);
      window.removeEventListener("resize", onResize);
      controls.dispose();
      renderer.dispose();
      container.removeChild(renderer.domElement);
    };
  }, []);

  return (
    <div style={{ width: "100vw", height: "100vh", background: "#1a1a2e" }}>
      <div 
        ref={canvasRef} 
        style={{ width: "100%", height: "100%" }}
      />
      <div style={{
        position: "absolute",
        top: 20,
        left: 20,
        color: "white",
        fontFamily: "monospace",
        background: "rgba(0,0,0,0.7)",
        padding: "15px",
        borderRadius: "8px",
        fontSize: "14px"
      }}>
        <h3 style={{ margin: "0 0 10px 0" }}>🧪 Test Character</h3>
        <p style={{ margin: "5px 0" }}>🖱️ Left click + drag: Rotate view</p>
        <p style={{ margin: "5px 0" }}>🔍 Scroll: Zoom in/out</p>
        <p style={{ margin: "5px 0" }}>📋 Check console (F12) for bones</p>
      </div>
    </div>
  );
};

export default TestScene;
