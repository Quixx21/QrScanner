import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  eslint: {
    ignoreDuringBuilds: true,
  },
  async rewrites() {
    return [
      {
        source: "/decode",
        destination: "http://qrscanner-backend:8000/decode"
      },
      {
        source: "/health",
        destination: "http://qrscanner-backend:8000/health",
      },
    ];
  },
};

export default nextConfig;
