// Video optimization
document.addEventListener("DOMContentLoaded", () => {
  const lazyVideos = document.querySelectorAll(".lazy-video");
  if (lazyVideos.length > 0) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const video = entry.target;
          if (video.getAttribute("data-src")) {
            video.src = video.getAttribute("data-src");
            video.load();
            observer.unobserve(video);
          }
        }
      });
    });
    lazyVideos.forEach((video) => observer.observe(video));
  }
});

document.addEventListener("DOMContentLoaded", () => {
  const groups = document.querySelectorAll(".video-hover-group");
  if (groups.length > 0) {
    const isMobile = /Mobi|Android/i.test(navigator.userAgent);

    groups.forEach((group) => {
      const video = group.querySelector("video");

      if (video) {
        group.addEventListener("mouseenter", () => {
          if (!isMobile) {
            video.play();
            video.muted = true; // Mute on hover
          }
        });

        group.addEventListener("mouseleave", () => {
          if (!isMobile) {
            video.pause();
            video.muted = true; // Keep muted when mouse leaves
          }
        });

        group.addEventListener("click", () => {
          video.play();
          video.muted = isMobile || !video.muted; // Unmute only if not on mobile
        });
      }
    });
  }
});

// MUN video
const videoContainer = document.getElementById("videoContainer");
const eventVideo = document.getElementById("eventVideo");
const eventImage = document.getElementById("eventImage");
const overlayText = document.getElementById("overlayText");

if (videoContainer && eventVideo && eventImage && overlayText) {
  videoContainer.addEventListener("click", function () {
    eventImage.style.display = "none";
    overlayText.style.display = "none";
    eventVideo.play();
    eventVideo.style.opacity = 1;
    eventVideo.controls = true;
  });
}
