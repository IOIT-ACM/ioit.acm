/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html", // Matches all HTML files in the templates folder
    "./app/**/*.html", // Add this if your templates are nested
  ],
  theme: {
    extend: {
      animation: {
        "grow-shrink": "growShrink 3s ease-in-out infinite",
      },
      keyframes: {
        growShrink: {
          "0%, 100%": { transform: "scale(1)" },
          "50%": { transform: "scale(1.1)" },
        },
      },
      colors: {
        "brand-card-dark": "#030F1C",
        "brand-gray": "#A1AAB2",
        "brand-button": "#252A31",
        "brand-sea": "#4DA2FF",
        "brand-ocean": "#011829",
        "brand-aqua": "#C0E6FF",
      },
    },
  },
  plugins: [],
};
