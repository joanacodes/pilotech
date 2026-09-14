/** @type {import('tailwindcss').Config} */
// Palette dérivée du logo Pilotech : bleu marine (texte), chevron bleu (froid) → orange (chaud).
module.exports = {
  content: [
    "./_layouts/**/*.html",
    "./_includes/**/*.html",
    "./_products/**/*.md",
    "./*.{html,md}",
    "./climatisation/**/*.html",
    "./ventilation/**/*.html",
    "./services/**/*.html",
    "./blog/**/*.html",
    "./assets/js/**/*.js",
  ],
  // Classes ajoutées dynamiquement par assets/js/site.js
  safelist: ["is-open", "is-visible", "is-active", "is-current", "hidden", "overflow-hidden"],
  theme: {
    container: { center: true, padding: { DEFAULT: "1.25rem", lg: "2rem" } },
    extend: {
      colors: {
        ink: "#14213D",      // titres, texte fort
        body: "#3D4A5F",     // texte courant
        muted: "#6B7889",    // texte secondaire
        brand: { DEFAULT: "#294D7C", dark: "#1E3A5F", light: "#E8EFF7" }, // marine du logo
        cool: { DEFAULT: "#0487F1", light: "#E3F1FE" },  // froid / rafraîchissement
        warm: { DEFAULT: "#E2622B", light: "#FCEDE4" },  // chaud / chauffage
        mist: "#F2F5F9",     // fond des sections alternées
        line: "#D9E0EA",     // filets
      },
      fontFamily: {
        sans: ['"IBM Plex Sans"', "system-ui", "sans-serif"],
        display: ['"IBM Plex Sans Condensed"', '"IBM Plex Sans"', "system-ui", "sans-serif"],
      },
      fontSize: {
        "display-xl": ["clamp(2.6rem, 5.5vw, 4.6rem)", { lineHeight: "1", letterSpacing: "-0.01em" }],
        "display-lg": ["clamp(2.1rem, 3.8vw, 3.2rem)", { lineHeight: "1.05", letterSpacing: "-0.01em" }],
        "display-md": ["clamp(1.6rem, 2.4vw, 2.1rem)", { lineHeight: "1.1" }],
      },
      fontWeight: { 500: "500", 600: "600", 700: "700" },
      maxWidth: { prose: "68ch", site: "76rem" },
      borderRadius: { DEFAULT: "4px", md: "6px", lg: "8px" },
    },
  },
  plugins: [],
};
