import { useState, useEffect, useRef } from 'react'
import { useParams } from 'react-router-dom'

export default function LecturePage() {
  const { slug } = useParams()
  
  const [lectureData, setLectureData] = useState(null)
  const [activeTab, setActiveTab] = useState('transcript')
  const [currentTime, setCurrentTime] = useState(0)
  const [isPlaying, setIsPlaying] = useState(false)
  const [highlightedSegment, setHighlightedSegment] = useState(null)
  
  const videoRef = useRef(null)
  const audioRef = useRef(null)

  useEffect(() => {
    // 模擬載入演講資料
    const mockData = {
      title: '心臟病學基礎概念與臨床應用',
      speaker: '王醫師',
      date: '2024-01-15',
      duration: '45:30',
      videoUrl: '/videos/cardiology-basics-2024.mp4',
      audioUrl: '/audio/cardiology-basics-2024.mp3',
      transcript: [
        {
          id: 'seg1',
          startTime: 0,
          endTime: 30,
          text: '大家好，今天我們要討論心臟病學的基礎概念。心臟是人體最重要的器官之一，負責將血液輸送到全身各個部位。'
        },
        {
          id: 'seg2',
          startTime: 30,
          endTime: 60,
          text: '在臨床診斷中，我們需要了解各種心臟疾病的症狀和診斷方法。常見的心臟疾病包括冠心病、心律不整、心臟衰竭等。'
        },
        {
          id: 'seg3',
          startTime: 60,
          endTime: 90,
          text: '心電圖是診斷心臟疾病最基本也是最重要的工具之一。透過心電圖，我們可以觀察心臟的電氣活動，判斷是否有異常。'
        }
      ],
      notes: `# 心臟病學基礎概念與臨床應用

## 主要重點

### 1. 心臟解剖學基礎
- 心臟四個腔室：左心房、右心房、左心室、右心室
- 心臟瓣膜：二尖瓣、三尖瓣、主動脈瓣、肺動脈瓣
- 冠狀動脈系統

### 2. 常見心臟疾病
- **冠心病**：冠狀動脈狹窄或阻塞
- **心律不整**：心跳節律異常
- **心臟衰竭**：心臟泵血功能下降

### 3. 診斷工具
- 心電圖 (ECG)
- 心臟超音波
- 心導管檢查
- 運動心電圖

### 4. 治療原則
- 藥物治療
- 介入性治療
- 外科手術
- 生活方式調整

## 臨床案例分析

### 案例一：急性心肌梗塞
患者主訴胸痛，心電圖顯示 ST 段上升，診斷為急性心肌梗塞，立即進行緊急心導管治療。

### 案例二：心房顫動
患者心跳不規則，心電圖確診心房顫動，給予抗凝血劑治療預防中風。`,
      slides: [
        {
          id: 'slide1',
          timestamp: 0,
          imageUrl: '/slides/cardiology-slide-1.jpg',
          title: '心臟病學概論'
        },
        {
          id: 'slide2',
          timestamp: 30,
          imageUrl: '/slides/cardiology-slide-2.jpg',
          title: '心臟解剖結構'
        },
        {
          id: 'slide3',
          timestamp: 60,
          imageUrl: '/slides/cardiology-slide-3.jpg',
          title: '診斷工具介紹'
        }
      ]
    }
    setLectureData(mockData)
  }, [slug])

  const seekToTime = (time) => {
    const media = videoRef.current || audioRef.current
    if (media) {
      media.currentTime = time
    }
  }

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60)
    const secs = Math.floor(seconds % 60)
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }

  if (!lectureData) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-3/4 mb-4"></div>
          <div className="h-4 bg-gray-200 rounded w-1/2 mb-8"></div>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div className="aspect-video bg-gray-200 rounded-lg"></div>
            <div className="space-y-4">
              <div className="h-10 bg-gray-200 rounded"></div>
              <div className="h-64 bg-gray-200 rounded"></div>
            </div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* 演講標題資訊 */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">{lectureData.title}</h1>
        <div className="flex items-center space-x-4 text-gray-600">
          <span>講者：{lectureData.speaker}</span>
          <span>日期：{new Date(lectureData.date).toLocaleDateString('zh-TW')}</span>
          <span>時長：{lectureData.duration}</span>
        </div>
      </div>

      {/* 主要內容區域 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* 左側：影片/音檔播放器 */}
        <div className="space-y-4">
          <div className="aspect-video bg-black rounded-lg overflow-hidden">
            <div className="w-full h-full flex items-center justify-center bg-gray-900">
              <div className="text-center text-white">
                <div className="mb-4">
                  <svg className="w-16 h-16 mx-auto" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M9.383 3.076A1 1 0 0110 4v12a1 1 0 01-1.617.793l-4.146-3.317a1 1 0 00-.632-.226H2a1 1 0 01-1-1V7.5a1 1 0 011-1h1.605a1 1 0 00.632-.226l4.146-3.317a1 1 0 011.617.793zM14.657 5.757a1 1 0 011.414 0A9.972 9.972 0 0119 10a9.972 9.972 0 01-2.929 7.071 1 1 0 11-1.414-1.414A7.971 7.971 0 0017 10c0-2.21-.894-4.208-2.343-5.657a1 1 0 010-1.414zm-2.829 2.829a1 1 0 011.414 0A5.983 5.983 0 0115 10a5.983 5.983 0 01-1.758 4.243 1 1 0 11-1.415-1.415A3.987 3.987 0 0013 10a3.987 3.987 0 00-1.172-2.828 1 1 0 010-1.415z" clipRule="evenodd" />
                  </svg>
                </div>
                <p className="text-gray-300">演講媒體播放器</p>
                <p className="text-sm text-gray-400 mt-2">（演示版本 - 實際部署時會載入真實媒體檔案）</p>
              </div>
            </div>
          </div>
          
          {/* 播放進度資訊 */}
          <div className="text-sm text-gray-600 text-center">
            當前時間：{formatTime(currentTime)} / {lectureData.duration}
          </div>
        </div>

        {/* 右側：切換式內容 */}
        <div className="space-y-4">
          {/* Tab 切換按鈕 */}
          <div className="flex space-x-2">
            <button
              onClick={() => setActiveTab('transcript')}
              className={`px-4 py-2 text-sm font-medium rounded-lg transition-colors duration-200 ${
                activeTab === 'transcript' 
                  ? 'bg-gray-900 text-white' 
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
              }`}
            >
              逐字稿
            </button>
            <button
              onClick={() => setActiveTab('notes')}
              className={`px-4 py-2 text-sm font-medium rounded-lg transition-colors duration-200 ${
                activeTab === 'notes' 
                  ? 'bg-gray-900 text-white' 
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
              }`}
            >
              整理筆記
            </button>
            <button
              onClick={() => setActiveTab('slides')}
              className={`px-4 py-2 text-sm font-medium rounded-lg transition-colors duration-200 ${
                activeTab === 'slides' 
                  ? 'bg-gray-900 text-white' 
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
              }`}
            >
              投影片
            </button>
          </div>

          {/* Tab 內容 */}
          <div className="bg-white rounded-lg border border-gray-200 p-6 h-96 overflow-y-auto">
            {activeTab === 'transcript' && (
              <div className="space-y-3">
                <h3 className="text-lg font-semibold mb-4">演講逐字稿</h3>
                {lectureData.transcript.map(segment => (
                  <div
                    key={segment.id}
                    className="p-3 rounded-md transition-colors duration-200 cursor-pointer hover:bg-gray-50"
                    onClick={() => seekToTime(segment.startTime)}
                  >
                    <div className="text-xs text-gray-500 mb-1">
                      {formatTime(segment.startTime)} - {formatTime(segment.endTime)}
                    </div>
                    <div className="text-sm">{segment.text}</div>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'notes' && (
              <div className="prose prose-sm max-w-none">
                <div 
                  dangerouslySetInnerHTML={{ 
                    __html: lectureData.notes
                      .replace(/\n/g, '<br>')
                      .replace(/### /g, '<h3>')
                      .replace(/## /g, '<h2>')
                      .replace(/# /g, '<h1>')
                      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                  }} 
                />
              </div>
            )}

            {activeTab === 'slides' && (
              <div className="space-y-4">
                <h3 className="text-lg font-semibold mb-4">投影片截圖</h3>
                {lectureData.slides.map(slide => (
                  <div
                    key={slide.id}
                    className="border border-gray-200 rounded-lg p-4 cursor-pointer hover:bg-gray-50"
                    onClick={() => seekToTime(slide.timestamp)}
                  >
                    <div className="flex items-center space-x-4">
                      <div className="w-24 h-16 bg-gray-200 rounded flex-shrink-0 flex items-center justify-center">
                        <svg className="w-8 h-8 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M4 3a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zm12 12H4l4-8 3 6 2-4 3 6z" clipRule="evenodd" />
                        </svg>
                      </div>
                      <div className="flex-1">
                        <div className="text-sm font-medium">{slide.title || `投影片 ${slide.id}`}</div>
                        <div className="text-xs text-gray-500">時間：{formatTime(slide.timestamp)}</div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

