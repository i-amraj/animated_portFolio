// GLB Validation Script
// Validates the raj-final.glb file structure

const fs = require('fs');
const path = require('path');

const GLB_PATH = path.join(__dirname, '../public/models/raj-final.glb');

console.log('=' .repeat(60));
console.log('GLB FILE VALIDATION');
console.log('=' .repeat(60));

// Read GLB file
const buffer = fs.readFileSync(GLB_PATH);
console.log(`\nFile size: ${(buffer.length / 1024 / 1024).toFixed(2)} MB`);

// GLB Header validation
const magic = buffer.toString('ascii', 0, 4);
const version = buffer.readUInt32LE(4);
const length = buffer.readUInt32LE(8);

console.log(`\nGLB Header:`);
console.log(`  Magic: ${magic} (should be "glTF")`);
console.log(`  Version: ${version} (should be 2)`);
console.log(`  Length: ${length} bytes`);

if (magic !== 'glTF') {
  console.log('\n❌ ERROR: Invalid GLB magic number!');
  process.exit(1);
}

if (version !== 2) {
  console.log('\n❌ ERROR: Not glTF 2.0 format!');
  process.exit(1);
}

console.log('\n✅ Valid GLB header');

// Parse JSON chunk
const chunk0Length = buffer.readUInt32LE(12);
const chunk0Type = buffer.readUInt32LE(16);
const jsonData = buffer.toString('utf8', 20, 20 + chunk0Length);

let gltf;
try {
  gltf = JSON.parse(jsonData);
  console.log('\n✅ JSON chunk parsed successfully');
} catch (e) {
  console.log('\n❌ ERROR: Failed to parse JSON chunk!');
  process.exit(1);
}

// Check structure
console.log('\nGLTF Structure:');
console.log(`  Scenes: ${gltf.scenes?.length || 0}`);
console.log(`  Nodes: ${gltf.nodes?.length || 0}`);
console.log(`  Meshes: ${gltf.meshes?.length || 0}`);
console.log(`  Materials: ${gltf.materials?.length || 0}`);
console.log(`  Textures: ${gltf.textures?.length || 0}`);
console.log(`  Skins: ${gltf.skins?.length || 0}`);
console.log(`  Animations: ${gltf.animations?.length || 0}`);

// Check animations
console.log('\nAnimations:');
if (gltf.animations && gltf.animations.length > 0) {
  gltf.animations.forEach((anim, i) => {
    console.log(`  ${i + 1}. ${anim.name || 'unnamed'} (${anim.channels?.length || 0} channels)`);
  });
  
  // Check required animations
  const required = ['introAnimation', 'typing', 'Blink', 'browup'];
  const found = gltf.animations.map(a => a.name);
  
  console.log('\nRequired animations check:');
  required.forEach(name => {
    if (found.includes(name)) {
      console.log(`  ✅ ${name}`);
    } else {
      console.log(`  ❌ ${name} MISSING`);
    }
  });
} else {
  console.log('  ❌ No animations found!');
}

// Check skins (for skeletal animation)
console.log('\nSkeleton:');
if (gltf.skins && gltf.skins.length > 0) {
  const skin = gltf.skins[0];
  const jointCount = skin.joints?.length || 0;
  console.log(`  ✅ Skin found with ${jointCount} joints`);
  
  // List some bone names
  if (skin.joints && gltf.nodes) {
    const keyBones = ['Hips', 'LeftUpLeg', 'LeftLeg', 'RightUpLeg', 'RightLeg', 'LeftArm', 'RightArm', 'Head'];
    const boneNames = skin.joints.map(idx => gltf.nodes[idx]?.name).filter(Boolean);
    
    console.log('\n  Key bones check:');
    keyBones.forEach(name => {
      if (boneNames.includes(name)) {
        console.log(`    ✅ ${name}`);
      } else {
        console.log(`    ❌ ${name} not found`);
      }
    });
  }
} else {
  console.log('  ❌ No skins found!');
}

console.log('\n' + '=' .repeat(60));
console.log('✅ VALIDATION COMPLETE');
console.log('=' .repeat(60));
