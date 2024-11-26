/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html", // Matches all HTML files in the templates folder
    "./app/**/*.html", // Add this if your templates are nested
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
