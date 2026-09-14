/** @type {import('tailwindcss').Config} */
// Palette dérivée du logo Pilotech : bleu marine (texte), chevron bleu (froid) → orange (chaud).
const v = (name) => `rgb(var(--${name}) / <alpha-value>)`; // couleur pilotée par une variable CSS (mode clair / sombre)

module.exports = {
  darkMode: "class",
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
        ink: v("c-ink"),        // titres, texte fort
        body: v("c-body"),      // texte courant
        muted: v("c-muted"),    // texte secondaire
        paper: v("c-paper"),    // fond des pages et des cartes
        deep: v("c-deep"),      // footer, préchargeur, vidéos : toujours sombre
        tile: "#F2F5F9",        // fond des visuels produits : toujours clair (photos sur fond blanc)
        mist: v("c-mist"),      // sections alternées
        line: v("c-line"),      // filets
        brand: { DEFAULT: v("c-brand"), dark: v("c-brand-dark"), light: v("c-brand-light") },
        cool: { DEFAULT: "#0487F1", light: v("c-cool-light") },  // froid / rafraîchissement
        warm: { DEFAULT: "#E2622B", light: v("c-warm-light") },  // chaud / chauffage
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
