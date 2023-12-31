/** @type {import('next').NextConfig} */
const nextConfig = {
    reactStrictMode: false,
    swcMinify: true,
    // except for webpack, other parts are left as generated
    webpack: (config) => {
      config.watchOptions = {
        poll: 1000,
        aggregateTimeout: 300
      }
      config.experiments = {
        ...config.experiments,
        topLevelAwait: true,
      }
      return config
    }
  }
  
  module.exports = nextConfig