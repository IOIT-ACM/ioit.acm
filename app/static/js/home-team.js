import * as THREE from "three";
import TWEEN from "three/addons/libs/tween.module.js";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import {
  CSS3DRenderer,
  CSS3DObject,
} from "three/addons/renderers/CSS3DRenderer.js";

const table = [
  {
    title: "Chair",
    image: "static/img/team/2024/chaitali.jpeg",
  },
  {
    title: "Administrator",
    image: "static/img/team/2024/sakshi-mane.jpeg",
  },
  {
    title: "Secretary",
    image: "static/img/team/2024/devang.jpeg",
  },
  {
    title: "Jt. Secretary",
    image: "static/img/team/2024/sarde.jpeg",
  },
  {
    title: "Executive Manager",
    image: "static/img/team/2024/sangole.jpeg",
  },
  {
    title: "Treasurer",
    image: "static/img/team/2024/vedant-vetkar.jpeg",
  },
  {
    title: "Event Management Head",
    image: "static/img/team/2024/vedant-rajput.jpeg",
  },
  {
    title: "Web Master",
    image: "static/img/team/2024/adimail.jpeg",
  },
  {
    title: "Web team Executive",
    image: "static/img/team/2024/web-swaroop.jpeg",
  },
  {
    title: "Technical Head",
    image: "static/img/team/2024/tech-pranita.jpeg",
  },
  {
    title: "Technical Member",
    image: "static/img/team/2024/tech-madhia.jpeg",
  },
  {
    title: "Management",
    image: "static/img/team/2024/mg-avdoot.jpeg",
  },
  {
    title: "Management",
    image: "static/img/team/2024/mg-gargi-patil.jpeg",
  },
  {
    title: "Documentation Member",
    image: "static/img/team/2024/doc-mansi.jpeg",
  },
  {
    title: "Documentation Member",
    image: "static/img/team/2024/doc-suha.jpeg",
  },
  {
    title: "award-2024",
    image: "static/img/gallery/award-2024/1.jpeg",
  },
  {
    title: "award-2024",
    image: "static/img/gallery/award-2024/2.jpeg",
  },
  {
    title: "award-2024",
    image: "static/img/gallery/award-2024/3.jpeg",
  },
  {
    title: "drive",
    image: "static/img/gallery/drive/1.jpeg",
  },
  {
    title: "drive",
    image: "static/img/gallery/drive/2.jpeg",
  },
  {
    title: "drive",
    image: "static/img/gallery/drive/3.jpeg",
  },
  {
    title: "esp",
    image: "static/img/gallery/esp/1.jpeg",
  },
  {
    title: "esp",
    image: "static/img/gallery/esp/2.jpeg",
  },
  {
    title: "esp",
    image: "static/img/gallery/esp/3.jpeg",
  },
  {
    title: "events",
    image: "static/img/gallery/events/1.jpeg",
  },
  {
    title: "events",
    image: "static/img/gallery/events/2.jpeg",
  },
  {
    title: "events",
    image: "static/img/gallery/events/3.jpeg",
  },
  {
    title: "tenet-2024",
    image: "static/img/gallery/tenet-2024/1.jpeg",
  },
  {
    title: "tenet-2024",
    image: "static/img/gallery/tenet-2024/2.jpeg",
  },
  {
    title: "tenet-2024",
    image: "static/img/gallery/tenet-2024/3.jpeg",
  },
];

let camera, scene, renderer;
let controls;
let currentTarget = "table";
let shuffleInterval;

const objects = [];
const targets = { table: [], sphere: [] };

init();
animate();

function init() {
  camera = new THREE.PerspectiveCamera(
    40,
    window.innerWidth / window.innerHeight,
    1,
    10000,
  );
  camera.position.z = 3000;

  scene = new THREE.Scene();

  // table

  for (let i = 0; i < table.length; i += 1) {
    const element = document.createElement("div");
    element.className = "member";
    element.style.backgroundImage = `url(${table[i].image})`;
    element.style.backgroundSize = "cover";
    element.style.backgroundPosition = "center";
    element.style.borderRadius = "10px";
    element.style.overflow = "hidden";
    element.style.position = "relative";
    element.style.width = "200px";
    element.style.height = "300px";
    element.style.boxShadow = "0 4px 8px rgba(0, 0, 0, 0.2)";

    const labelContainer = document.createElement("div");
    labelContainer.className = "label-container";
    labelContainer.style.position = "absolute";
    labelContainer.style.bottom = "0";
    labelContainer.style.left = "0";
    labelContainer.style.width = "100%";
    labelContainer.style.background = "rgba(0, 0, 0, 0.6)";
    labelContainer.style.color = "#fff";
    labelContainer.style.padding = "10px 0";
    labelContainer.style.textAlign = "center";

    const title = document.createElement("div");
    title.className = "title";
    title.textContent = table[i].title;
    title.style.fontSize = "12px";
    title.style.opacity = "0.8";
    labelContainer.appendChild(title);

    element.appendChild(labelContainer);

    const objectCSS = new CSS3DObject(element);
    objectCSS.position.x = Math.random() * 4000 - 2000;
    objectCSS.position.y = Math.random() * 4000 - 2000;
    objectCSS.position.z = Math.random() * 4000 - 2000;
    scene.add(objectCSS);

    objects.push(objectCSS);

    const object = new THREE.Object3D();
    object.position.x = Math.random() * 2000 - 1000;
    object.position.y = Math.random() * 2000 - 1000;
    object.position.z = Math.random() * 2000 - 1000;
    targets.table.push(object);
  }

  // sphere

  const vector = new THREE.Vector3();

  for (let i = 0, l = objects.length; i < l; i++) {
    const phi = Math.acos(-1 + (2 * i) / l);
    const theta = Math.sqrt(l * Math.PI) * phi;

    const object = new THREE.Object3D();

    object.position.setFromSphericalCoords(800, phi, theta);

    vector.copy(object.position).multiplyScalar(2);

    object.lookAt(vector);

    targets.sphere.push(object);
  }

  //

  renderer = new CSS3DRenderer();
  renderer.setSize(window.innerWidth, window.innerHeight);
  document.getElementById("container").appendChild(renderer.domElement);

  // Initialize OrbitControls
  controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.dampingFactor = 0.25;
  controls.screenSpacePanning = true;
  controls.maxPolarAngle = Math.PI / 2;
  controls.enableZoom = false; // Disable zoom by default

  // Event listeners to enable zoom when Ctrl key is pressed
  window.addEventListener("keydown", (event) => {
    if (event.key === "Control") {
      controls.enableZoom = true;
    }
  });

  window.addEventListener("keyup", (event) => {
    if (event.key === "Control") {
      controls.enableZoom = false;
    }
  });

  // For touch devices, use a flag to simulate the Ctrl key behavior
  let isCtrlPressed = false;

  window.addEventListener("keydown", (event) => {
    if (event.key === "Control") {
      isCtrlPressed = true;
    }
  });

  window.addEventListener("keyup", (event) => {
    if (event.key === "Control") {
      isCtrlPressed = false;
    }
  });

  // Override the OrbitControls `onMouseWheel` and `onTouchMove` handlers
  const originalMouseWheelHandler = controls.mouseButtons.WHEEL;
  const originalTouchMoveHandler = controls.touches.ONE;

  controls.addEventListener("start", () => {
    if (!isCtrlPressed) {
      controls.mouseButtons.WHEEL = null;
      controls.touches.ONE = null;
    } else {
      controls.mouseButtons.WHEEL = originalMouseWheelHandler;
      controls.touches.ONE = originalTouchMoveHandler;
    }
  });
  controls.addEventListener("change", render);

  const buttonTable = document.getElementById("table");
  buttonTable.addEventListener("click", function () {
    currentTarget = "table";
    transform(targets.table, 2000);
  });

  const buttonSphere = document.getElementById("sphere");
  buttonSphere.addEventListener("click", function () {
    currentTarget = "sphere";
    transform(targets.sphere, 2000);
  });

  transform(targets.table, 2000);

  window.addEventListener("resize", onWindowResize);
}

function transform(targets, duration) {
  TWEEN.removeAll();

  shuffleArray(targets);

  for (let i = 0; i < objects.length; i++) {
    const object = objects[i];
    const target = targets[i];

    new TWEEN.Tween(object.position)
      .to(
        {
          x: target.position.x,
          y: target.position.y,
          z: target.position.z,
        },
        Math.random() * duration + duration,
      )
      .easing(TWEEN.Easing.Exponential.InOut)
      .start();

    new TWEEN.Tween(object.rotation)
      .to(
        {
          x: target.rotation.x,
          y: target.rotation.y,
          z: target.rotation.z,
        },
        Math.random() * duration + duration,
      )
      .easing(TWEEN.Easing.Exponential.InOut)
      .start();
  }

  new TWEEN.Tween(this)
    .to({}, duration * 2)
    .onUpdate(render)
    .start();
}

function onWindowResize() {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();

  renderer.setSize(window.innerWidth, window.innerHeight);

  render();
}

function animate() {
  requestAnimationFrame(animate);
  TWEEN.update();
  controls.update();
}

function render() {
  renderer.render(scene, camera);
}

function shuffleArray(array) {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
}

function startShuffling() {
  shuffleInterval = setInterval(() => {
    if (currentTarget === "sphere") {
      shuffleArray(targets.sphere);
      transform(targets.sphere, 2000);
    } else {
      shuffleArray(targets.table);
      transform(targets.table, 2000);
    }
  }, 7000);
}

startShuffling();
