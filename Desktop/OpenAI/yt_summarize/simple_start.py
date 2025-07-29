#!/usr/bin/env python3
"""
Simple server starter that works around uvicorn issues
"""
import os
import sys

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import FastAPI app
from main import app

# Simple HTTP server using only standard library
if __name__ == "__main__":
    import subprocess
    
    print("啟動 FastAPI 服務...")
    print("服務網址: http://localhost:8000")
    print("按 Ctrl+C 停止服務")
    
    # Try different methods to start the server
    try:
        # Method 1: Try uvicorn directly
        import uvicorn
        uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
    except:
        try:
            # Method 2: Try using subprocess with explicit path
            subprocess.run([
                sys.executable, "-c",
                "from main import app; import uvicorn; uvicorn.run(app, host='127.0.0.1', port=8000)"
            ])
        except:
            # Method 3: Direct import and run
            print("使用備用啟動方式...")
            os.system(f"{sys.executable} main.py")