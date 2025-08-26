import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: '醫療教育平台',
  description: '專為醫事人員設計的極簡視覺化教育平台',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="zh-TW">
      <body className={inter.className}>
        <nav className="border-b bg-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between h-16">
              <div className="flex items-center">
                <a href="/" className="text-xl font-semibold text-gray-900">
                  醫療教育平台
                </a>
              </div>
              <div className="flex items-center space-x-4">
                <a 
                  href="/" 
                  className="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium"
                >
                  演講列表
                </a>
                <a 
                  href="/admin" 
                  className="bg-gray-900 text-white px-3 py-2 rounded-md text-sm font-medium hover:bg-gray-700"
                >
                  管理後台
                </a>
              </div>
            </div>
          </div>
        </nav>
        <main className="min-h-screen bg-gray-50">
          {children}
        </main>
      </body>
    </html>
  )
}

