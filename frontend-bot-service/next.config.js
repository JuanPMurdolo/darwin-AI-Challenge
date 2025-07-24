/** @type {import('next').NextConfig} */
const nextConfig = {
  // Enable standalone output for Docker
  output: "standalone",

  // Environment variables
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000",
    NEXT_PUBLIC_APP_URL: process.env.NEXT_PUBLIC_APP_URL || "http://localhost:3000",
  },

  // API rewrites for development
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: `${process.env.NEXT_PUBLIC_API_URL || "http://bot-service:8000"}/:path*`,
      },
    ]
  },

  // Image optimization
  images: {
    domains: ["localhost", "bot-service"],
    unoptimized: true, // For Docker deployment
  },

  // Disable telemetry
  telemetry: false,

  // Experimental features for better Docker support
  experimental: {
    outputFileTracingRoot: undefined,
  },

  // ESLint configuration
  eslint: {
    ignoreDuringBuilds: true,
  },

  // TypeScript configuration
  typescript: {
    ignoreBuildErrors: true,
  },
}

module.exports = nextConfig
