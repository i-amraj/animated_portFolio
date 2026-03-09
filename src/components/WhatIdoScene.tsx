import { useEffect, useRef } from "react";
import * as THREE from "three";
import { GLTFLoader, DRACOLoader } from "three-stdlib";
import "./styles/WhatIdoScene.css";

const WhatIdoScene = () => {
    const mountRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (!mountRef.current) return;
        const container = mountRef.current;
        const W = container.clientWidth;
        const H = container.clientHeight;

        // ── Renderer ────────────────────────────────────────────
        const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
        renderer.setSize(W, H);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        renderer.toneMapping = THREE.ACESFilmicToneMapping;
        renderer.toneMappingExposure = 1.2;
        renderer.shadowMap.enabled = true;
        renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        container.appendChild(renderer.domElement);

        // ── Scene ────────────────────────────────────────────────
        const scene = new THREE.Scene();

        // ── Camera ───────────────────────────────────────────────
        const camera = new THREE.PerspectiveCamera(42, W / H, 0.1, 100);
        camera.position.set(-0.3, 1.95, 4.2);
        camera.lookAt(0, 1.1, 0);

        // ── Lighting ─────────────────────────────────────────────
        const ambient = new THREE.AmbientLight(0xffffff, 0.5);
        scene.add(ambient);

        // Rim light (purple, from back-right) — matches website theme
        const rimLight = new THREE.DirectionalLight(0x9b7fff, 3.5);
        rimLight.position.set(2, 3, -3);
        scene.add(rimLight);

        // Key light (soft white, from front-left)
        const keyLight = new THREE.DirectionalLight(0xdde8ff, 2.5);
        keyLight.position.set(-2, 4, 3);
        keyLight.castShadow = true;
        scene.add(keyLight);

        // Monitor screen glow (cyan-blue from front)
        const screenGlow = new THREE.PointLight(0x7eb8ff, 6, 4);
        screenGlow.position.set(0, 1.7, 1.0);
        scene.add(screenGlow);

        // Flicker screen glow
        let glowIntensity = 6;
        const flickerGlow = () => {
            glowIntensity = 5.5 + Math.random() * 2;
            screenGlow.intensity = glowIntensity;
            setTimeout(flickerGlow, 80 + Math.random() * 300);
        };
        flickerGlow();

        // ── Materials ─────────────────────────────────────────────
        const woodMat = new THREE.MeshStandardMaterial({ color: 0x2c1a0e, roughness: 0.8, metalness: 0.05 });
        const metalMat = new THREE.MeshStandardMaterial({ color: 0x888888, roughness: 0.3, metalness: 0.8 });
        const screenMat = new THREE.MeshStandardMaterial({
            color: 0x1a1a2e, emissive: 0x7eb8ff, emissiveIntensity: 0.5, roughness: 0.2, metalness: 0.5
        });
        const whiteMat = new THREE.MeshStandardMaterial({ color: 0xf0f0f0, roughness: 0.6 });
        const darkMat = new THREE.MeshStandardMaterial({ color: 0x222222, roughness: 0.5, metalness: 0.3 });
        const chairWhite = new THREE.MeshStandardMaterial({ color: 0xd0cfe8, roughness: 0.7 });

        function box(w: number, h: number, d: number, mat: THREE.Material, x = 0, y = 0, z = 0) {
            const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), mat);
            m.position.set(x, y, z);
            m.castShadow = true; m.receiveShadow = true;
            scene.add(m); return m;
        }
        function cyl(rt: number, rb: number, h: number, mat: THREE.Material, x = 0, y = 0, z = 0) {
            const m = new THREE.Mesh(new THREE.CylinderGeometry(rt, rb, h, 16), mat);
            m.position.set(x, y, z);
            m.castShadow = true;
            scene.add(m); return m;
        }

        // ── DESK ─────────────────────────────────────────────────
        // Desktop surface
        box(2.0, 0.05, 0.85, woodMat, 0, 1.0, -0.1);
        // Desk legs
        box(0.06, 1.0, 0.06, metalMat, -0.92, 0.5, -0.45);
        box(0.06, 1.0, 0.06, metalMat, 0.92, 0.5, -0.45);
        box(0.06, 1.0, 0.06, metalMat, -0.92, 0.5, 0.3);
        box(0.06, 1.0, 0.06, metalMat, 0.92, 0.5, 0.3);
        // Desk cross bar
        box(1.88, 0.04, 0.04, metalMat, 0, 0.08, -0.4);

        // ── MONITOR ──────────────────────────────────────────────
        // Monitor stand base
        box(0.25, 0.02, 0.2, darkMat, 0, 1.05, -0.45);
        // Monitor stand neck
        box(0.04, 0.35, 0.04, darkMat, 0, 1.22, -0.45);
        // Monitor back frame
        box(0.82, 0.52, 0.04, darkMat, 0, 1.6, -0.56);
        // Monitor screen
        box(0.76, 0.46, 0.01, screenMat, 0, 1.6, -0.53);
        // Monitor bezel (thin black border)
        box(0.79, 0.49, 0.025, new THREE.MeshStandardMaterial({ color: 0x111111, roughness: 0.5 }), 0, 1.6, -0.545);

        // ── KEYBOARD ─────────────────────────────────────────────
        box(0.55, 0.02, 0.2, darkMat, 0.1, 1.04, 0.1);
        // keyboard detail rows
        for (let r = 0; r < 4; r++) {
            for (let c = 0; c < 12; c++) {
                box(0.038, 0.012, 0.035,
                    new THREE.MeshStandardMaterial({ color: 0x333333, roughness: 0.6 }),
                    -0.22 + c * 0.044, 1.056, 0.01 + r * 0.042);
            }
        }

        // ── MUG / CUP ────────────────────────────────────────────
        cyl(0.045, 0.04, 0.1, new THREE.MeshStandardMaterial({ color: 0xc03030, roughness: 0.7 }), 0.75, 1.1, 0.05);

        // ── CHAIR ────────────────────────────────────────────────
        const seatY = 0.48;
        // Seat
        box(0.55, 0.05, 0.48, chairWhite, 0, seatY, 0.38);
        // Backrest
        box(0.55, 0.46, 0.04, chairWhite, 0, seatY + 0.28, 0.14);
        // Chair legs
        const legMat = new THREE.MeshStandardMaterial({ color: 0x888888, roughness: 0.3, metalness: 0.7 });
        box(0.03, seatY, 0.03, legMat, -0.25, seatY / 2, 0.6);
        box(0.03, seatY, 0.03, legMat, 0.25, seatY / 2, 0.6);
        box(0.03, seatY, 0.03, legMat, -0.25, seatY / 2, 0.16);
        box(0.03, seatY, 0.03, legMat, 0.25, seatY / 2, 0.16);
        // Armrests
        box(0.03, 0.03, 0.38, chairWhite, -0.3, seatY + 0.1, 0.38);
        box(0.03, 0.03, 0.38, chairWhite, 0.3, seatY + 0.1, 0.38);

        // ── FLOOR (subtle) ───────────────────────────────────────
        const floorMat = new THREE.MeshStandardMaterial({ color: 0x0d0d1a, roughness: 1.0 });
        const floor = new THREE.Mesh(new THREE.PlaneGeometry(6, 6), floorMat);
        floor.rotation.x = -Math.PI / 2;
        floor.receiveShadow = true;
        scene.add(floor);

        // ── Load Character GLB ───────────────────────────────────
        const loader = new GLTFLoader();
        const draco = new DRACOLoader();
        draco.setDecoderPath("/draco/");
        loader.setDRACOLoader(draco);

        let mixer: THREE.AnimationMixer | null = null;
        const clock = new THREE.Clock();

        loader.load(
            "/models/raj-sitting.glb",
            (gltf) => {
                const char = gltf.scene;
                // Character is exported with armature at y=0.45, no extra offset needed
                char.position.set(0, 0, 0);
                char.rotation.y = Math.PI * 0.05; // slight angle
                char.traverse((child: any) => {
                    if (child.isMesh) {
                        child.castShadow = true;
                        child.receiveShadow = true;
                    }
                });
                scene.add(char);

                if (gltf.animations.length > 0) {
                    mixer = new THREE.AnimationMixer(char);
                    const action = mixer.clipAction(gltf.animations[0]);
                    action.play();
                }
                draco.dispose();
            },
            undefined,
            (err) => console.error("Character load error:", err)
        );

        // ── Animate ───────────────────────────────────────────────
        let animId: number;
        const animate = () => {
            animId = requestAnimationFrame(animate);
            const delta = clock.getDelta();
            if (mixer) mixer.update(delta);
            // Subtle screen glow pulse on monitor material
            (screenMat as any).emissiveIntensity = 0.45 + Math.sin(Date.now() * 0.002) * 0.08;
            renderer.render(scene, camera);
        };
        animate();

        // ── Resize ────────────────────────────────────────────────
        const onResize = () => {
            const W2 = container.clientWidth;
            const H2 = container.clientHeight;
            camera.aspect = W2 / H2;
            camera.updateProjectionMatrix();
            renderer.setSize(W2, H2);
        };
        window.addEventListener("resize", onResize);

        return () => {
            cancelAnimationFrame(animId);
            window.removeEventListener("resize", onResize);
            if (container.contains(renderer.domElement)) {
                container.removeChild(renderer.domElement);
            }
            renderer.dispose();
            scene.clear();
        };
    }, []);

    return <div ref={mountRef} className="whatido-scene" />;
};

export default WhatIdoScene;
