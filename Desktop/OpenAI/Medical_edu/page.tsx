'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'

interface Lecture {
  slug: string
  title: string
  speaker: string
  date: string
  keywords: string[]
  duration?: string
  thumbnail?: string
}

export default function HomePage() {
  const [lectures, setLectures] = useState<Lecture[]>([])
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedKeyword, setSelectedKeyword] = useState('')

  useEffect(() => {
    // 模擬資料，實際應從 API 或檔案系統載入
    const mockLectures: Lecture[] = [
      {
        slug: 'cardiology-basics-2024',
        title: '心臟病學基礎概念與臨床應用',
        speaker: '王醫師',
        date: '2024-01-15',
        keywords: ['心臟病學', '臨床診斷', '基礎醫學'],
        duration: '45:30'
      },
      {
        slug: 'emergency-medicine-protocols',
        title: '急診醫學處置流程與案例分析',
        speaker: '李醫師',
        date: '2024-01-20',
        keywords: ['急診醫學', '處置流程', '案例分析'],
        duration: '52:15'
      },
      {
        slug: 'surgical-techniques-advanced',
        title: '進階外科手術技巧與併發症處理',
        speaker: '張醫師',
        date: '2024-01-25',
        keywords: ['外科手術', '技巧', '併發症'],
        duration: '38:45'
      }
    ]
    setLectures(mockLectures)
  }, [])

  const filteredLectures = lectures.filter(lecture => {
    const matchesSearch = lecture.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         lecture.speaker.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesKeyword = !selectedKeyword || lecture.keywords.includes(selectedKeyword)
    return matchesSearch && matchesKeyword
  })

  const allKeywords = Array.from(new Set(lectures.flatMap(lecture => lecture.keywords)))

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* 頁面標題 */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">醫療教育演講</h1>
        <p className="text-gray-600">探索最新的醫療知識與臨床經驗分享</p>
      </div>

      {/* 搜尋與篩選 */}
      <div className="mb-8 space-y-4">
        <div className="flex flex-col sm:flex-row gap-4">
          <div className="flex-1">
            <input
              type="text"
              placeholder="搜尋演講標題或講者..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-gray-500 focus:border-transparent"
            />
          </div>
          <div className="sm:w-48">
            <select
              value={selectedKeyword}
              onChange={(e) => setSelectedKeyword(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-gray-500 focus:border-transparent"
            >
              <option value="">所有分類</option>
              {allKeywords.map(keyword => (
                <option key={keyword} value={keyword}>{keyword}</option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* 演講卡片網格 */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredLectures.map(lecture => (
          <Link key={lecture.slug} href={`/lecture/${lecture.slug}`}>
            <div className="lecture-card">
              {/* 縮圖區域 */}
              <div className="aspect-video bg-gray-200 rounded-md mb-4 flex items-center justify-center">
                {lecture.thumbnail ? (
                  <img 
                    src={lecture.thumbnail} 
                    alt={lecture.title}
                    className="w-full h-full object-cover rounded-md"
                  />
                ) : (
                  <div className="text-gray-400">
                    <svg className="w-12 h-12" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M4 3a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zm3 2h6v4H7V5zm8 8v2h1v-2h-1zm-2-2H7v4h6v-4z" clipRule="evenodd" />
                    </svg>
                  </div>
                )}
              </div>

              {/* 演講資訊 */}
              <div className="space-y-3">
                <h3 className="text-lg font-semibold text-gray-900 line-clamp-2">
                  {lecture.title}
                </h3>
                
                <div className="flex items-center justify-between text-sm text-gray-600">
                  <span>{lecture.speaker}</span>
                  {lecture.duration && (
                    <span className="bg-gray-100 px-2 py-1 rounded">
                      {lecture.duration}
                    </span>
                  )}
                </div>
                
                <div className="text-sm text-gray-500">
                  {new Date(lecture.date).toLocaleDateString('zh-TW')}
                </div>
                
                {/* 關鍵詞標籤 */}
                <div className="flex flex-wrap gap-2">
                  {lecture.keywords.slice(0, 3).map(keyword => (
                    <span 
                      key={keyword}
                      className="inline-block bg-gray-100 text-gray-700 text-xs px-2 py-1 rounded-full"
                    >
                      {keyword}
                    </span>
                  ))}
                  {lecture.keywords.length > 3 && (
                    <span className="text-xs text-gray-500">
                      +{lecture.keywords.length - 3} 更多
                    </span>
                  )}
                </div>
              </div>
            </div>
          </Link>
        ))}
      </div>

      {/* 無結果提示 */}
      {filteredLectures.length === 0 && (
        <div className="text-center py-12">
          <div className="text-gray-400 mb-4">
            <svg className="w-16 h-16 mx-auto" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clipRule="evenodd" />
            </svg>
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">找不到相關演講</h3>
          <p className="text-gray-600">請嘗試調整搜尋條件或瀏覽所有演講</p>
        </div>
      )}
    </div>
  )
}

