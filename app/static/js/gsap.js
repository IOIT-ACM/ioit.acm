function applyTextReveal(element) {
  gsap.from(element, {
    y: 200, // Start from below
    opacity: 0, // Start with 0 opacity
    ease: "power4.out", // Smooth easing effect
    skewY: 15, // Apply a slight skew for effect
    delay: 0, // Delay the start for a smoother effect
    duration: 1, // Duration of the animation
    stagger: {
      amount: 0.3, // Delay between each element in the group
      start: "top", // Stagger from the top element first
    },
  });
}

const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        applyTextReveal(entry.target);
        observer.unobserve(entry.target);
      }
    });
  },
  {
    threshold: 0.07,
  },
);

document.querySelectorAll(".gsap-reveal").forEach((el) => {
  observer.observe(el);
});
