import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import { RoundedBoxGeometry } from "three/addons/geometries/RoundedBoxGeometry.js";

document.addEventListener("DOMContentLoaded", () => {
  const canvas = document.getElementById("interactive-cubes");
  const container = document.getElementById("canvas-container");

  // Set the initial size of the canvas to match the container
  canvas.width = container.clientWidth;
  canvas.height = container.clientHeight;

  let cubes = [];
  const cursor = new THREE.Vector3();
  const oPos = new THREE.Vector3();
  const vec = new THREE.Vector3();
  const dir = new THREE.Vector3();
  const gap = 0.3;
  let stride = window.innerWidth <= 768 ? 4 : 5;
  const displacement = window.innerWidth <= 768 ? 2 : 3.5;
  const intensity = 1;

  const scene = new THREE.Scene();
  scene.background = null;
  const sizes = {
    width: canvas.width,
    height: canvas.height,
  };
  const camera = new THREE.PerspectiveCamera(
    75,
    sizes.width / sizes.height,
    0.1,
    1000,
  );
  camera.position.set(8, 8, 8);
  scene.add(camera);

  const ambientLight = new THREE.AmbientLight(0xaaaaaa, 1.5);
  scene.add(ambientLight);

  const spotLight = new THREE.SpotLight(0xffffff, 1.5);
  spotLight.position.set(-15, 20, 15);
  spotLight.castShadow = true;
  spotLight.shadow.mapSize.width = 1024;
  spotLight.shadow.mapSize.height = 1024;
  scene.add(spotLight);

  const pointLight = new THREE.PointLight(0xff8888, 1, 50);
  pointLight.position.set(10, 5, -10);
  scene.add(pointLight);

  const directionalLight = new THREE.DirectionalLight(0x88ff88, 0.8);
  directionalLight.position.set(-5, 15, 10);
  scene.add(directionalLight);

  const renderer = new THREE.WebGLRenderer({ canvas, alpha: true });
  renderer.setSize(sizes.width, sizes.height);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.shadowMap.enabled = true;

  const createCubes = () => {
    cubes.forEach((cube) => scene.remove(cube));
    cubes = [];

    const geometry = new RoundedBoxGeometry(1, 1, 1, 2, 0.15);
    const material = new THREE.MeshLambertMaterial({ color: 0xffffff });
    const center = stride / 2;

    for (let x = 0; x < stride; x++) {
      for (let y = 0; y < stride; y++) {
        for (let z = 0; z < stride; z++) {
          const cube = new THREE.Mesh(geometry, material.clone());
          const position = new THREE.Vector3(
            x + x * gap - center,
            y + y * gap - center,
            z + z * gap - center,
          );
          cube.position.copy(position);
          cube.userData.originalPosition = position.clone();
          cube.userData.material = cube.material;
          cube.castShadow = true;
          cube.receiveShadow = true;
          scene.add(cube);
          cubes.push(cube);
        }
      }
    }
  };

  createCubes();

  const handleMouseMove = (event) => {
    const rect = canvas.getBoundingClientRect(); // Get the relative position of the canvas

    // Normalize the mouse coordinates within the canvas
    const mouse = new THREE.Vector2();
    mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1; // Normalized X position
    mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1; // Normalized Y position

    // Now update the cursor position
    cursor.set(mouse.x, mouse.y, 0.5).unproject(camera);

    // Compute direction to move the cubes
    dir.copy(cursor).sub(camera.position).normalize();
    cursor.add(dir.multiplyScalar(camera.position.length()));
  };
  window.addEventListener("mousemove", handleMouseMove);

  const handleResize = () => {
    sizes.width = container.clientWidth;
    sizes.height = container.clientHeight;
    camera.aspect = sizes.width / sizes.height;
    camera.updateProjectionMatrix();
    renderer.setSize(sizes.width, sizes.height);
    canvas.width = sizes.width;
    canvas.height = sizes.height;
  };

  window.addEventListener("resize", handleResize);

  const controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.enableZoom = false;

  const isMobile = window.innerWidth <= 768;
  if (isMobile) {
    controls.enableRotate = false;
    controls.enableZoom = false;
    controls.enablePan = false;

    renderer.domElement.style.touchAction = "auto";
  } else {
    controls.enableRotate = true;
    controls.enablePan = true;
  }

  function resizeCanvas() {
    renderer.setSize(container.clientWidth, container.clientHeight);
    camera.aspect = container.clientWidth / container.clientHeight;
    camera.updateProjectionMatrix();
  }

  window.addEventListener("resize", resizeCanvas);

  const animate = () => {
    requestAnimationFrame(animate);
    controls.update();

    cubes.forEach((cube) => {
      oPos.copy(cube.userData.originalPosition);
      dir.copy(oPos).sub(cursor).normalize();
      const dist = oPos.distanceTo(cursor);
      const distInv = displacement - dist;
      const col = Math.max(0.5, distInv) / 1.5;

      if (dist > displacement * 1.1) {
        cube.userData.material.color.setRGB(1, 1, 1);
      } else {
        cube.userData.material.color.setRGB(col / 2, col * 2, col * 4);
      }

      if (dist > displacement) {
        cube.position.lerp(oPos, 0.2);
      } else {
        vec.copy(oPos).add(dir.multiplyScalar(distInv * intensity));
        cube.position.lerp(vec, 0.2);
      }
    });

    renderer.render(scene, camera);
  };

  resizeCanvas();
  animate();
});
