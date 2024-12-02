import * as THREE from "https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.module.js";

const canvas = document.getElementById("page-surface");
const container = canvas.parentElement;
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(
  40,
  container.clientWidth / container.clientHeight,
  0.7,
  1000,
);

const renderer = new THREE.WebGLRenderer({ canvas, alpha: true });
renderer.setSize(container.clientWidth, container.clientHeight);
renderer.setPixelRatio(window.devicePixelRatio);

scene.background = null;

const width = 4;
const height = 5;
const depth = 0.3;

const textureLoader = new THREE.TextureLoader();
const coverTexture = textureLoader.load("static/img/assets/acm-award-23.jpeg");

const coverMaterial = new THREE.MeshBasicMaterial({ map: coverTexture });
const sideMaterial = new THREE.MeshBasicMaterial({ color: 0x8b4513 });

const materials = [
  sideMaterial,
  sideMaterial,
  sideMaterial,
  sideMaterial,
  coverMaterial,
  coverMaterial,
];

const bookGeometry = new THREE.BoxGeometry(width, height, depth);
const book = new THREE.Mesh(bookGeometry, materials);
scene.add(book);

camera.position.z = 10;

let isDragging = false;
let previousMousePosition = { x: 0, y: 0 };
let dragRotation = { x: 0, y: 0 };

let continuousRotationSpeed = { x: 0.01, y: 0.01 };

// Mouse Event Listeners
canvas.addEventListener("mousedown", (event) => {
  isDragging = true;
  previousMousePosition.x = event.clientX;
  previousMousePosition.y = event.clientY;
});

canvas.addEventListener("mousemove", (event) => {
  if (isDragging) {
    const deltaMove = {
      x: event.clientX - previousMousePosition.x,
      y: event.clientY - previousMousePosition.y,
    };

    dragRotation.y += deltaMove.x * 0.01;
    dragRotation.x += deltaMove.y * 0.01;

    previousMousePosition.x = event.clientX;
    previousMousePosition.y = event.clientY;
  }
});

canvas.addEventListener("mouseup", () => {
  isDragging = false;
});

canvas.addEventListener("mouseleave", () => {
  isDragging = false;
});

canvas.addEventListener("touchstart", (event) => {
  isDragging = true;
  const touch = event.touches[0];
  previousMousePosition.x = touch.clientX;
  previousMousePosition.y = touch.clientY;
});

canvas.addEventListener("touchmove", (event) => {
  if (isDragging) {
    const touch = event.touches[0];
    const deltaMove = {
      x: touch.clientX - previousMousePosition.x,
      y: touch.clientY - previousMousePosition.y,
    };

    // Determine if movement is more vertical (Y-axis) or horizontal (X-axis)
    const absDeltaX = Math.abs(deltaMove.x);
    const absDeltaY = Math.abs(deltaMove.y);

    if (absDeltaX > absDeltaY) {
      // Horizontal movement: rotate the object
      event.preventDefault(); // Prevent scrolling only for horizontal movement
      dragRotation.y += deltaMove.x * 0.01;
      dragRotation.x += deltaMove.y * 0.01;
    }

    // Update previous position
    previousMousePosition.x = touch.clientX;
    previousMousePosition.y = touch.clientY;
  }
});

canvas.addEventListener("touchend", () => {
  isDragging = false;
});

function resizeCanvas() {
  // Adjust canvas size based on container dimensions
  renderer.setSize(container.clientWidth, container.clientHeight);
  camera.aspect = container.clientWidth / container.clientHeight;
  camera.updateProjectionMatrix();
}

window.addEventListener("resize", resizeCanvas);

function animate() {
  requestAnimationFrame(animate);

  book.rotation.y += continuousRotationSpeed.y;

  if (isDragging) {
    book.rotation.y += dragRotation.y;
    dragRotation.y = 0;
  }

  renderer.render(scene, camera);
}

resizeCanvas(); // Ensure initial fit
animate();
