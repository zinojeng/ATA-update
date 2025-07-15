import { useState, useRef } from 'react'

export default function AdminPage() {
  const [uploadFiles, setUploadFiles] = useState([])
  const [isDragOver, setIsDragOver] = useState(false)
  const fileInputRef = useRef(null)

  const handleDragOver = (e) => {
    e.preventDefault()
    setIsDragOver(true)
  }

  const handleDragLeave = (e) => {
    e.preventDefault()
    setIsDragOver(false)
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setIsDragOver(false)
    
    const files = Array.from(e.dataTransfer.files)
    handleFiles(files)
  }

  const handleFileSelect = (e) => {
    if (e.target.files) {
      const files = Array.from(e.target.files)
      handleFiles(files)
    }
  }

  const handleFiles = (files) => {
    const newUploadFiles = files.map(file => ({
      id: Math.random().toString(36).substr(2, 9),
      name: file.name,
      size: file.size,
      type: file.type,
      status: 'pending',
      progress: 0
    }))

    setUploadFiles(prev => [...prev, ...newUploadFiles])

    // 模擬檔案處理流程
    newUploadFiles.forEach(uploadFile => {
      simulateFileProcessing(uploadFile.id)
    })
  }

  const simulateFileProcessing = async (fileId) => {
    // 模擬上傳進度
    setUploadFiles(prev => prev.map(file => 
      file.id === fileId ? { ...file, status: 'uploading' } : file
    ))

    for (let progress = 0; progress <= 100; progress += 10) {
      await new Promise(resolve => setTimeout(resolve, 200))
      setUploadFiles(prev => prev.map(file => 
        file.id === fileId ? { ...file, progress } : file
      ))
    }

    // 模擬轉錄處理
    setUploadFiles(prev => prev.map(file => 
      file.id === fileId ? { ...file, status: 'processing', progress: 0 } : file
    ))

    for (let progress = 0; progress <= 100; progress += 5) {
      await new Promise(resolve => setTimeout(resolve, 300))
      setUploadFiles(prev => prev.map(file => 
        file.id === fileId ? { ...file, progress } : file
      ))
    }

    // 完成處理
    setUploadFiles(prev => prev.map(file => 
      file.id === fileId ? { ...file, status: 'completed', progress: 100 } : file
    ))
  }

  const removeFile = (fileId) => {
    setUploadFiles(prev => prev.filter(file => file.id !== fileId))
  }

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  const getStatusText = (status) => {
    switch (status) {
      case 'pending': return '等待中'
      case 'uploading': return '上傳中'
      case 'processing': return '轉錄處理中'
      case 'completed': return '完成'
      case 'error': return '錯誤'
      default: return '未知'
    }
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'pending': return 'text-gray-600'
      case 'uploading': return 'text-blue-600'
      case 'processing': return 'text-yellow-600'
      case 'completed': return 'text-green-600'
      case 'error': return 'text-red-600'
      default: return 'text-gray-600'
    }
  }

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* 頁面標題 */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">管理後台</h1>
        <p className="text-gray-600">上傳演講錄音/錄影檔案，系統將自動進行轉錄與筆記整理</p>
      </div>

      {/* 上傳區域 */}
      <div className="mb-8">
        <div
          className={`border-2 border-dashed rounded-lg p-8 text-center hover:border-gray-400 transition-colors duration-200 cursor-pointer ${
            isDragOver ? 'border-blue-400 bg-blue-50' : 'border-gray-300'
          }`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current?.click()}
        >
          <input
            ref={fileInputRef}
            type="file"
            multiple
            accept="audio/*,video/*"
            onChange={handleFileSelect}
            className="hidden"
          />
          
          <div className="space-y-4">
            <div className="text-gray-400">
              <svg className="w-16 h-16 mx-auto" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM6.293 6.707a1 1 0 010-1.414l3-3a1 1 0 011.414 0l3 3a1 1 0 01-1.414 1.414L11 5.414V13a1 1 0 11-2 0V5.414L7.707 6.707a1 1 0 01-1.414 0z" clipRule="evenodd" />
              </svg>
            </div>
            
            <div className="text-center">
              <h3 className="text-lg font-medium text-gray-900 mb-2">
                拖放檔案到此處或點擊選擇
              </h3>
              <p className="text-gray-600">
                支援音檔格式：MP3, WAV, M4A<br />
                支援影片格式：MP4, MOV, AVI
              </p>
            </div>
            
            <div className="text-center">
              <button className="bg-gray-900 text-white px-6 py-2 rounded-lg hover:bg-gray-700 transition-colors">
                選擇檔案
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* 檔案處理狀態 */}
      {uploadFiles.length > 0 && (
        <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-lg font-semibold text-gray-900">檔案處理狀態</h2>
          </div>
          
          <div className="divide-y divide-gray-200">
            {uploadFiles.map(file => (
              <div key={file.id} className="px-6 py-4">
                <div className="flex items-center justify-between mb-2">
                  <div className="flex-1 min-w-0">
                    <h3 className="text-sm font-medium text-gray-900 truncate">
                      {file.name}
                    </h3>
                    <div className="flex items-center space-x-4 text-xs text-gray-500">
                      <span>{formatFileSize(file.size)}</span>
                      <span className={getStatusColor(file.status)}>
                        {getStatusText(file.status)}
                      </span>
                    </div>
                  </div>
                  
                  <button
                    onClick={() => removeFile(file.id)}
                    className="ml-4 text-gray-400 hover:text-gray-600"
                  >
                    <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
                    </svg>
                  </button>
                </div>
                
                {/* 進度條 */}
                {(file.status === 'uploading' || file.status === 'processing') && (
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                      style={{ width: `${file.progress}%` }}
                    ></div>
                  </div>
                )}
                
                {/* 完成狀態 */}
                {file.status === 'completed' && (
                  <div className="mt-2 flex items-center space-x-4">
                    <span className="text-sm text-green-600 flex items-center">
                      <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                      </svg>
                      處理完成
                    </span>
                    <span className="text-sm text-blue-600 hover:text-blue-800 cursor-pointer">
                      查看演講頁面
                    </span>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 使用說明 */}
      <div className="mt-8 bg-blue-50 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-blue-900 mb-4">使用說明</h3>
        <div className="space-y-2 text-sm text-blue-800">
          <p>• 支援的檔案格式：MP3, WAV, M4A（音檔）、MP4, MOV, AVI（影片）</p>
          <p>• 檔案大小限制：單檔最大 500MB</p>
          <p>• 處理時間：約為檔案時長的 1/4（例如：60分鐘演講約需 15分鐘處理）</p>
          <p>• 系統會自動進行語音轉錄、生成逐字稿、整理重點筆記</p>
          <p>• 處理完成後可在演講列表中查看結果</p>
        </div>
      </div>
    </div>
  )
}

