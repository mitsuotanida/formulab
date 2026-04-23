import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: "class",
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        background: "#0A0A0F",
        surface: "#13131A",
        "surface-2": "#1C1C28",
        border: "#2A2A3D",
        primary: "#6366F1",
        "primary-light": "#818CF8",
        accent: "#10B981",
        "accent-warn": "#F59E0B",
        destructive: "#EF4444",
        muted: "#6B7280",
        foreground: "#F9FAFB",
        "foreground-muted": "#9CA3AF",
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
        mono: ["JetBrains Mono", "monospace"],
      },
      boxShadow: {
        "neon-primary": "0 0 20px rgba(99, 102, 241, 0.4)",
        "neon-accent": "0 0 20px rgba(16, 185, 129, 0.4)",
      },
      animation: {
        "fade-in": "fadeIn 0.3s ease-in-out",
        "slide-up": "slideUp 0.4s ease-out",
        "pulse-slow": "pulse 3s ease-in-out infinite",
      },
      keyframes: {
        fadeIn: { "0%": { opacity: "0" }, "100%": { opacity: "1" } },
        slideUp: { "0%": { transform: "translateY(20px)", opacity: "0" }, "100%": { transform: "translateY(0)", opacity: "1" } },
      },
    },
  },
  plugins: [],
};

export default config;
