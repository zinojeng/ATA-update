#!/usr/bin/env python3
"""
Temporary server starter for Python 3.13 compatibility
"""
import subprocess
import sys
import os

# Ensure we're in the right directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Try to start the server using gunicorn as a fallback
try:
    # First, try with gunicorn (WSGI server)
    print("嘗試使用 gunicorn 啟動服務...")
    subprocess.run([
        sys.executable, "-m", "gunicorn",
        "main:app",
        "--bind", "127.0.0.1:8000",
        "--worker-class", "uvicorn.workers.UvicornWorker",
        "--reload"
    ])
except Exception as e:
    print(f"Gunicorn 啟動失敗: {e}")
    print("\n嘗試直接執行 main.py...")
    # Fallback to direct execution
    subprocess.run([sys.executable, "main.py"])