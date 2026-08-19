/** @type {import('next').NextConfig} */
const nextConfig = {
  output: "standalone",
  env: {
    // On Vercel (production) always target the real backend. This ignores any
    // stale NEXT_PUBLIC_API_URL env var still pointing at an old Render URL.
    // Locally, honor the env var (or default to the dev backend on localhost).
    NEXT_PUBLIC_API_URL: process.env.VERCEL
      ? "https://formulab-backend.onrender.com/api/v1"
      : process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1",
  },
};

module.exports = nextConfig;
