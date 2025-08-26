#!/usr/bin/env node

import fs from 'fs/promises'
import path from 'path'
import { createReadStream } from 'fs'
import OpenAI from 'openai'

// 初始化 OpenAI 客戶端
const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
  baseURL: process.env.OPENAI_API_BASE
})

interface TranscriptSegment {
  id: string
  startTime: number
  endTime: number
  text: string
}

interface ProcessedResult {
  title: string
  speaker: string
  date: string
  duration: string
  transcript: TranscriptSegment[]
  notes: string
  keywords: string[]
}

/**
 * 將檔案名稱轉換為 kebab-case slug
 */
function createSlug(filename: string): string {
  return filename
    .replace(/\.[^/.]+$/, '') // 移除副檔名
    .toLowerCase()
    .replace(/[^\w\s-]/g, '') // 移除特殊字符
    .replace(/\s+/g, '-') // 空格轉為連字符
    .replace(/-+/g, '-') // 多個連字符合併為一個
    .trim()
}

/**
 * 使用 Whisper API 進行語音轉錄
 */
async function transcribeAudio(audioPath: string): Promise<string> {
  console.log(`開始轉錄音檔: ${audioPath}`)
  
  try {
    const audioStream = createReadStream(audioPath)
    
    const transcription = await openai.audio.transcriptions.create({
      file: audioStream,
      model: 'whisper-1',
      language: 'zh',
      response_format: 'verbose_json',
      timestamp_granularities: ['segment']
    })
    
    console.log('轉錄完成')
    return transcription.text
  } catch (error) {
    console.error('轉錄失敗:', error)
    throw new Error(`轉錄失敗: ${error}`)
  }
}

/**
 * 將轉錄文本分段並添加時間戳
 */
function segmentTranscript(transcriptText: string): TranscriptSegment[] {
  // 簡單的分段邏輯：按句號、問號、驚嘆號分段
  const sentences = transcriptText
    .split(/[。！？]/)
    .filter(sentence => sentence.trim().length > 0)
    .map(sentence => sentence.trim() + '。')
  
  const segments: TranscriptSegment[] = []
  const avgSegmentDuration = 30 // 假設每段平均 30 秒
  
  sentences.forEach((sentence, index) => {
    const startTime = index * avgSegmentDuration
    const endTime = (index + 1) * avgSegmentDuration
    
    segments.push({
      id: `seg${index + 1}`,
      startTime,
      endTime,
      text: sentence
    })
  })
  
  return segments
}

/**
 * 使用 GPT-4 生成整理筆記和關鍵詞
 */
async function generateNotes(transcriptText: string, filename: string): Promise<{ notes: string; keywords: string[] }> {
  console.log('開始生成整理筆記...')
  
  const prompt = `
請根據以下醫療演講的逐字稿，生成詳細的整理筆記和關鍵詞：

演講檔案名稱：${filename}
逐字稿內容：
${transcriptText}

請按照以下格式輸出：

## 整理筆記

### 主要重點
（列出演講的主要重點，使用 Markdown 格式）

### 詳細內容
（詳細整理演講內容，包含重要概念、診斷方法、治療原則等）

### 臨床應用
（如有提及臨床案例或應用，請詳細說明）

### 重要提醒
（列出講者強調的重要注意事項）

## 關鍵詞
（請提供 5-8 個最相關的關鍵詞，用逗號分隔）

請確保筆記內容專業、準確，適合醫事人員學習參考。
`

  try {
    const completion = await openai.chat.completions.create({
      model: 'gpt-4o',
      messages: [
        {
          role: 'system',
          content: '你是一位專業的醫療教育專家，擅長整理醫療演講內容並生成學習筆記。'
        },
        {
          role: 'user',
          content: prompt
        }
      ],
      temperature: 0.3,
      max_tokens: 4000
    })

    const response = completion.choices[0]?.message?.content || ''
    
    // 解析回應，分離筆記和關鍵詞
    const keywordsMatch = response.match(/## 關鍵詞\s*\n(.+?)(?:\n|$)/s)
    const keywords = keywordsMatch 
      ? keywordsMatch[1].split(',').map(k => k.trim()).filter(k => k.length > 0)
      : []
    
    // 移除關鍵詞部分，保留筆記內容
    const notes = response.replace(/## 關鍵詞\s*\n.+$/s, '').trim()
    
    console.log('筆記生成完成')
    return { notes, keywords }
  } catch (error) {
    console.error('筆記生成失敗:', error)
    throw new Error(`筆記生成失敗: ${error}`)
  }
}

/**
 * 提取音檔/影片的基本資訊
 */
async function extractMediaInfo(filePath: string): Promise<{ duration: string; title: string }> {
  // 這裡應該使用 ffprobe 或類似工具來提取媒體資訊
  // 為了簡化，這裡返回模擬資料
  const filename = path.basename(filePath)
  
  return {
    duration: '45:30', // 實際應該從媒體檔案中提取
    title: filename.replace(/\.[^/.]+$/, '').replace(/[-_]/g, ' ')
  }
}

/**
 * 主要處理函數
 */
async function processLecture(audioPath: string): Promise<void> {
  try {
    console.log(`開始處理演講檔案: ${audioPath}`)
    
    // 檢查檔案是否存在
    try {
      await fs.access(audioPath)
    } catch {
      throw new Error(`檔案不存在: ${audioPath}`)
    }
    
    const filename = path.basename(audioPath)
    const slug = createSlug(filename)
    
    // 提取媒體資訊
    const mediaInfo = await extractMediaInfo(audioPath)
    
    // 進行語音轉錄
    const transcriptText = await transcribeAudio(audioPath)
    
    // 分段處理逐字稿
    const transcript = segmentTranscript(transcriptText)
    
    // 生成整理筆記和關鍵詞
    const { notes, keywords } = await generateNotes(transcriptText, filename)
    
    // 組合結果
    const result: ProcessedResult = {
      title: mediaInfo.title,
      speaker: '待補充', // 可以從檔案名稱或內容中推斷
      date: new Date().toISOString().split('T')[0],
      duration: mediaInfo.duration,
      transcript,
      notes,
      keywords
    }
    
    // 儲存結果到檔案
    const outputPath = path.join(process.cwd(), 'public', 'notes', `${slug}.json`)
    await fs.mkdir(path.dirname(outputPath), { recursive: true })
    await fs.writeFile(outputPath, JSON.stringify(result, null, 2), 'utf-8')
    
    // 同時儲存 Markdown 格式的筆記
    const markdownPath = path.join(process.cwd(), 'public', 'notes', `${slug}.md`)
    const markdownContent = `# ${result.title}

**講者：** ${result.speaker}  
**日期：** ${result.date}  
**時長：** ${result.duration}  
**關鍵詞：** ${result.keywords.join(', ')}

---

${result.notes}

---

## 逐字稿

${result.transcript.map(seg => 
  `### ${Math.floor(seg.startTime / 60)}:${(seg.startTime % 60).toString().padStart(2, '0')} - ${Math.floor(seg.endTime / 60)}:${(seg.endTime % 60).toString().padStart(2, '0')}

${seg.text}
`).join('\n')}
`
    
    await fs.writeFile(markdownPath, markdownContent, 'utf-8')
    
    console.log(`處理完成！`)
    console.log(`JSON 檔案：${outputPath}`)
    console.log(`Markdown 檔案：${markdownPath}`)
    console.log(`演講頁面 URL：/lecture/${slug}`)
    
  } catch (error) {
    console.error('處理失敗:', error)
    process.exit(1)
  }
}

/**
 * 批次處理多個檔案
 */
async function batchProcess(inputDir: string): Promise<void> {
  try {
    const files = await fs.readdir(inputDir)
    const audioFiles = files.filter(file => 
      /\.(mp3|wav|m4a|mp4|mov|avi)$/i.test(file)
    )
    
    if (audioFiles.length === 0) {
      console.log('在指定目錄中找不到音檔或影片檔案')
      return
    }
    
    console.log(`找到 ${audioFiles.length} 個檔案，開始批次處理...`)
    
    for (const file of audioFiles) {
      const filePath = path.join(inputDir, file)
      await processLecture(filePath)
      console.log('---')
    }
    
    console.log('批次處理完成！')
  } catch (error) {
    console.error('批次處理失敗:', error)
    process.exit(1)
  }
}

// 命令列介面
async function main() {
  const args = process.argv.slice(2)
  
  if (args.length === 0) {
    console.log(`
使用方法：
  node transcribe_and_note.ts <音檔路徑>          # 處理單一檔案
  node transcribe_and_note.ts --batch <目錄路徑>  # 批次處理目錄中的所有檔案

範例：
  node transcribe_and_note.ts ./audio/lecture1.mp3
  node transcribe_and_note.ts --batch ./audio/

支援格式：MP3, WAV, M4A, MP4, MOV, AVI
`)
    process.exit(1)
  }
  
  if (args[0] === '--batch') {
    if (args.length < 2) {
      console.error('請指定要批次處理的目錄路徑')
      process.exit(1)
    }
    await batchProcess(args[1])
  } else {
    await processLecture(args[0])
  }
}

// 檢查環境變數
if (!process.env.OPENAI_API_KEY) {
  console.error('錯誤：請設定 OPENAI_API_KEY 環境變數')
  process.exit(1)
}

// 執行主程式
if (import.meta.url === `file://${process.argv[1]}`) {
  main().catch(console.error)
}

export { processLecture, batchProcess }

