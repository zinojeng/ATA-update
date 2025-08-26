/** @type {import('next').NextConfig} */
const nextConfig = {
  // 禁用圖片最佳化
  images: {
    unoptimized: true
  },
  
  // 設定 trailing slash
  trailingSlash: true,
  
  // TypeScript 設定
  typescript: {
    // 在建置時忽略 TypeScript 錯誤（不建議在生產環境使用）
    ignoreBuildErrors: true,
  },
  
  // ESLint 設定
  eslint: {
    // 在建置時忽略 ESLint 錯誤（不建議在生產環境使用）
    ignoreDuringBuilds: true,
  },
}

module.exports = nextConfig

