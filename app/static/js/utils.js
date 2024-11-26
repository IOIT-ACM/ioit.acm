function toggleNav() {
  const nav = document.getElementById("mobile-nav");
  nav.classList.toggle("hidden");
}

document.addEventListener("DOMContentLoaded", function () {
  fetch("/fetch-events")
    .then((response) => response.json())
    .then((data) => {
      // Populate Upcoming Events
      const upcomingSection = document.getElementById(
        "upcoming-events-section",
      );
      const upcomingEvents = document.getElementById("upcoming-events");
      if (data.upcoming.trim()) {
        upcomingSection.classList.remove("hidden");
        upcomingEvents.innerHTML = data.upcoming;
      }

      // Populate Past Events
      const pastSection = document.getElementById("past-events-section");
      const pastEvents = document.getElementById("past-events");
      if (data.past.trim()) {
        pastSection.classList.remove("hidden");
        pastEvents.innerHTML = data.past;
      }
    })
    .catch((error) => {
      console.error("Error fetching events:", error);
    });
});
