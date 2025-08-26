#!/usr/bin/env python3
"""
Minimal test server to diagnose issues
"""
print("Testing basic imports...")

try:
    print("1. Testing FastAPI import...")
    from fastapi import FastAPI
    print("   ✓ FastAPI imported successfully")
except Exception as e:
    print(f"   ✗ FastAPI import failed: {e}")

try:
    print("2. Testing uvicorn import...")
    import uvicorn
    print("   ✓ uvicorn imported successfully")
except Exception as e:
    print(f"   ✗ uvicorn import failed: {e}")

print("\n3. Creating minimal FastAPI app...")
try:
    app = FastAPI()
    
    @app.get("/")
    def read_root():
        return {"message": "Test server is running"}
    
    print("   ✓ Minimal app created")
    
    print("\n4. Starting server on http://localhost:8000")
    print("   Press Ctrl+C to stop")
    
    # Try to run with uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
    
except Exception as e:
    print(f"   ✗ Server failed to start: {e}")
    import traceback
    traceback.print_exc()