import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#17211F",
        surface: "#F8FAF9",
        line: "#D7E1DE",
        teal: "#115E59",
        coral: "#C8543D",
        gold: "#B4842D"
      }
    }
  },
  plugins: []
};

export default config;
