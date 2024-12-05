import * as THREE from "three";
import TWEEN from "three/addons/libs/tween.module.js";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import {
  CSS3DRenderer,
  CSS3DObject,
} from "three/addons/renderers/CSS3DRenderer.js";

const table = [
  {
    name: "Chaitali Khachane",
    title: "Chair",
    image: "static/img/team/2024/chaitali.jpeg",
    linktree: "",
    github: "",
    linkedin: "https://www.linkedin.com/in/chaitali-khachane-322685236/",
    instagram: "",
    domain: "core",
  },
  {
    name: "Atharva Nawale",
    title: "Vice Chair",
    image: "static/img/team/2024/navle.jpeg",
    linktree: "",
    github: "",
    linkedin: "https://www.linkedin.com/in/atharva-nawale/",
    instagram: "",
    domain: "core",
  },
  {
    name: "Sakshi Mane",
    title: "Administrator",
    image: "static/img/team/2024/sakshi-mane.jpeg",
    linktree: "",
    github: "https://github.com/thesakshimane",
    linkedin: "https://www.linkedin.com/in/sakshi-mane-9b88aa289/",
    instagram: "https://www.instagram.com/the_sakshimane",
    domain: "core",
  },
  {
    name: "Devang Gandhi",
    title: "Secretary",
    image: "static/img/team/2024/devang.jpeg",
    linktree: "",
    github: "",
    linkedin: "https://www.linkedin.com/in/devang-gandhi-917304213/",
    instagram: "",
    domain: "core",
  },
  {
    name: "Aditya Sarade",
    title: "Jt. Secretary",
    image: "static/img/team/2024/sarde.jpeg",
    linktree: "",
    github: "https://github.com/adityasarade",
    linkedin: "https://www.linkedin.com/in/adityasarade",
    instagram: "https://www.instagram.com/aditya__14",
    domain: "core",
  },
  {
    name: "Aayush Sangole",
    title: "Executive Manager",
    image: "static/img/team/2024/sangole.jpeg",
    linktree: "",
    github: "",
    linkedin: "http://linkedin.com/in/ayush-sangole-336804220",
    instagram: "",
    domain: "core",
  },
  {
    name: "Pranav Vetkar",
    title: "Treasurer",
    image: "static/img/team/2024/vedant-vetkar.jpeg",
    linktree: "",
    github: "",
    linkedin: "https://www.linkedin.com/in/pranav-vetkar-4b773a254/",
    instagram: "",
    domain: "core",
  },
  {
    name: "Vedant Rajput",
    title: "Event Management Head",
    image: "static/img/team/2024/vedant-rajput.jpeg",
    linktree: "",
    github: "",
    linkedin: "https://www.linkedin.com/in/vedant-rajput-vr3012/",
    instagram: "",
    domain: "events",
  },
  {
    name: "Aditya Godse",
    title: "Web Master",
    image: "static/img/team/2024/adimail.jpeg",
    linktree: "",
    github: "https://github.com/adimail",
    linkedin: "",
    instagram: "",
    domain: "web",
  },
  {
    name: "Swaroop Patil",
    title: "Web team Executive",
    image: "static/img/team/2024/web-swaroop.jpeg",
    linktree: "https://linktr.ee/swarooppatilx",
    github: "https://github.com/swarooppatilx",
    linkedin: "https://www.linkedin.com/in/swarooppatilx",
    instagram: "https://www.instagram.com/swarooppatilx",
    domain: "web",
  },
  {
    name: "Ayush Musale",
    title: "Web Team Member",
    image: "static/img/team/2024/web-ayush.jpeg",
    linktree: "",
    github: "",
    linkedin: "https://www.linkedin.com/in/aayush-musale-517a7326a/",
    instagram: "",
    domain: "web",
  },
  {
    name: "Pranita Bobade",
    title: "Technical Head",
    image: "static/img/team/2024/tech-pranita.jpeg",
    linktree: "https://linktr.ee/pranita2405",
    github: "https://github.com/pranitab07",
    linkedin: "https://www.linkedin.com/in/pranita-bobade-21b02625b/",
    instagram: "https://www.instagram.com/pranita24_b",
    domain: "tech",
  },
  {
    name: "Atharva",
    title: "Technical Member",
    image: "static/img/team/2024/tech-atharva.jpeg",
    linktree: "https://linktr.ee/atharv_s16",
    github: "https://github.com/Atharvs16",
    linkedin: "https://www.linkedin.com/in/atharv-s16",
    instagram: "https://www.instagram.com/atharv_s16",
    domain: "tech",
  },
  {
    name: "Madhia",
    title: "Technical Member",
    image: "static/img/team/2024/tech-madhia.jpeg",
    linktree: "",
    github: "",
    linkedin: "",
    instagram: "",
    domain: "tech",
  },
  {
    name: "Anish",
    title: "Technical Member",
    image: "static/img/team/2024/tech-anish.jpeg",
    linktree: "",
    github: "",
    linkedin: "",
    instagram: "",
    domain: "tech",
  },
  {
    name: "Nayesha Nayak",
    title: "SIG Head",
    image: "static/img/team/2024/nayesha.jpeg",
    linktree: "",
    github: "",
    linkedin: "",
    instagram: "",
    domain: "special interest group",
  },
  {
    name: "Avdoot Chavan",
    title: "Management",
    image: "static/img/team/2024/mg-avdoot.jpeg",
    linktree: "",
    github: "",
    linkedin: "",
    instagram: "",
    domain: "management",
  },
  {
    name: "Gargi Patil",
    title: "Management",
    image: "static/img/team/2024/mg-gargi-patil.jpeg",
    linktree: "",
    github: "",
    linkedin: "",
    instagram: "",
    domain: "management",
  },
  {
    name: "Sanjana Media",
    title: "Media Executive",
    image: "static/img/team/2024/media-sanjana.jpeg",
    linktree: "",
    github: "",
    linkedin: "",
    instagram: "",
    domain: "media",
  },
  {
    name: "Mansi",
    title: "Documentation Member",
    image: "static/img/team/2024/doc-mansi.jpeg",
    linktree: "https://linktr.ee/manasichoudhari_23",
    github: "https://www.instagram.com/manasichoudhari_23/",
    linkedin: "www.linkedin.com/in/manasi-choudhari-887b1428a",
    instagram: "https://www.instagram.com/manasichoudhari_23/",
    domain: "documentation",
  },
  {
    name: "Devika",
    title: "Documentation Member",
    image: "static/img/team/2024/doc-devika.jpeg",
    linktree: "",
    github: "",
    linkedin: "",
    instagram: "",
    domain: "documentation",
  },
  {
    name: "Riddhi",
    title: "Documentation Member",
    image: "static/img/team/2024/doc-riddhi.jpeg",
    linktree: "",
    github: "",
    linkedin: "",
    instagram: "",
    domain: "documentation",
  },
  {
    name: "Shriya",
    title: "Documentation Member",
    image: "static/img/team/2024/doc-shriya.jpeg",
    linktree: "",
    github: "",
    linkedin: "",
    instagram: "",
    domain: "documentation",
  },
  {
    name: "Suha",
    title: "Documentation Member",
    image: "static/img/team/2024/doc-suha.jpeg",
    linktree: "https://linktr.ee/suha.k",
    github: "",
    linkedin: "https://www.linkedin.com/in/suha-karjatkar-886666233",
    instagram: "https://www.instagram.com/suhakarjatkar",
    domain: "documentation",
  },
  {
    name: "Vibhavari",
    title: "Documentation Member",
    image: "static/img/team/2024/doc-vibhavari.jpeg",
    linktree: "",
    github: "",
    linkedin: "",
    instagram: "",
    domain: "documentation",
  },
  {
    name: "Vivan",
    title: "Documentation Member",
    image: "static/img/team/2024/doc-vivan.jpeg",
    linktree: "",
    github: "",
    linkedin: "",
    instagram: "",
    domain: "documentation",
  },
  {
    name: "Nilay",
    title: "Documentation Member",
    image: "static/img/team/2024/doc-nilay.jpeg",
    linktree: "",
    github: "",
    linkedin: "",
    instagram: "",
    domain: "documentation",
  },
  {
    name: "Sejal",
    title: "Media Executive",
    image: "static/img/team/2024/media-sejal.jpeg",
    linktree: "",
    github: "",
    linkedin: "",
    instagram: "",
    domain: "media",
  },
  {
    name: "Supesh",
    title: "Media Executive",
    image: "static/img/team/2024/media-supesh.jpeg",
    linktree: "",
    github: "",
    linkedin: "",
    instagram: "",
    domain: "media",
  },
];

let camera, scene, renderer;
let controls;
let currentTarget = "table";

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
