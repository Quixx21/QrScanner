import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      keyframes: {
        floating: {
          "0%, 100%": { transform: "translate(0, 0) scale(1)" },
          "50%": { transform: "translate(20%, -10%) scale(1.1)" },
        },
      },
      animation: {
        floating: "floating 12s ease-in-out infinite",
      },
    },
  },
  plugins: [],
};
export default config;
