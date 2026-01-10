import forms from "@tailwindcss/forms";
import type { Config } from "tailwindcss";

export default {
  content: ["./src/**/*.{html,js,svelte,ts}"],

  theme: {
    extend: {
      colors: {
        lilac: "#8a61e7", // primary
        skyblue: "#80b3e3", // accent 1
        orange: "#fa9565", // accent 2
        mint: "#b8f2e6", // support 1
        pink: "#ffcad4", // support 2
        yellow: "#fff4b8", // highlight
        dark: "#4c3c84", // dark contrast
      },
      boxShadow: {
        pastel: "0 4px 12px rgba(0, 0, 0, 0.15)",
      },
    },
  },

  plugins: [forms],
} satisfies Config;

/* TODO: custom styles for
 - section
 - button
 - input
 - header
 */
