#!/bin/bash

# YouTube Summarizer - Python 3.11 Startup Script
# Uses Python 3.11 for better compatibility

echo "========================================"
echo "YouTube 影片摘要產生器 - 啟動腳本"
echo "使用 Python 3.11 以確保相容性"
echo "========================================"
echo ""

# Use Python 3.11
PYTHON_CMD=python3.11

# Check if Python 3.11 is installed
if ! command -v $PYTHON_CMD &> /dev/null; then
    echo "❌ 錯誤：未找到 Python 3.11"
    echo "請安裝 Python 3.11"
    exit 1
fi

# Display Python version
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1)
echo "✅ 使用 Python: $PYTHON_VERSION"
echo ""

# Check if virtual environment exists (for Python 3.11)
if [ ! -d "venv_py311" ]; then
    echo "🔧 建立 Python 3.11 虛擬環境..."
    $PYTHON_CMD -m venv venv_py311
    echo "✅ 虛擬環境建立完成"
    echo ""
fi

# Activate virtual environment
echo "🔄 啟動虛擬環境..."
source venv_py311/bin/activate

# Install/Update dependencies
echo "📦 安裝相依套件..."
echo ""

pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "✅ 相依套件準備完成"
echo ""

# Create necessary directories
echo "📁 確保必要的目錄存在..."
mkdir -p audio transcripts summaries metadata cookies
echo "✅ 目錄準備完成"
echo ""

# Start the application
echo "🚀 啟動 YouTube 摘要服務..."
echo "========================================"
echo ""
echo "服務即將在以下網址啟動："
echo "👉 http://localhost:8000"
echo ""
echo "請在瀏覽器中開啟上述網址使用服務"
echo ""
echo "按 Ctrl+C 可以停止服務"
echo ""
echo "========================================"
echo ""

# Run with Python 3.11
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload