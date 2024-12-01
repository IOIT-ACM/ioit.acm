//
//
//Video optimization
//
//

document.addEventListener("DOMContentLoaded", () => {
  const lazyVideos = document.querySelectorAll(".lazy-video");

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        const video = entry.target;
        video.src = video.getAttribute("data-src");
        video.load();
        observer.unobserve(video);
      }
    });
  });

  lazyVideos.forEach((video) => observer.observe(video));
});

document.addEventListener("DOMContentLoaded", () => {
  const groups = document.querySelectorAll(".video-hover-group");

  groups.forEach((group) => {
    const video = group.querySelector("video");

    const isMobile = /Mobi|Android/i.test(navigator.userAgent);

    group.addEventListener("mouseenter", () => {
      if (video && !isMobile) {
        video.play();
        video.muted = true; // Mute on hover
      }
    });

    group.addEventListener("mouseleave", () => {
      if (video && !isMobile) {
        video.pause();
        video.muted = true; // Keep muted when mouse leaves
      }
    });

    group.addEventListener("click", () => {
      if (video) {
        video.play();
        video.muted = isMobile ? true : false; // Unmute only if not on mobile
      }
    });
  });
});

//
//
// MUN video
//
document
  .getElementById("videoContainer")
  .addEventListener("click", function () {
    const video = document.getElementById("eventVideo");
    const image = document.getElementById("eventImage");
    const overlay = document.getElementById("overlayText");

    image.style.display = "none";
    overlay.style.display = "none";

    video.play();
    video.style.opacity = 1;
    video.controls = true;
  }); //
