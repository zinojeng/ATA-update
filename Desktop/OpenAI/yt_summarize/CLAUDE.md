# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application (development mode with auto-reload)
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload

# Or use the convenience script that auto-updates critical dependencies
./run.sh
```

### Testing
```bash
# Test DOCX conversion functionality
python test_improved_converter.py

# Test API endpoints
python test_api.py

# Test parsing functionality
python test_parsing.py

# Test basic converter
python test_converter.py
```

### Building and Deployment
```bash
# Build Docker image
docker build -t yt-summarizer .

# Run with Docker
docker run -p 8000:8000 --env-file .env yt-summarizer
```

## Architecture

This is a FastAPI-based web application that processes YouTube videos through a multi-stage pipeline:

1. **Video Download** (`yt_summarizer.py`): Uses yt-dlp to download YouTube videos and extract audio
2. **Transcription**: Leverages OpenAI Whisper API to convert audio to text with automatic chunking for large files
3. **Summarization**: Dual-model approach using Google Gemini (primary) and OpenAI GPT (fallback) to generate structured summaries
4. **Export**: Converts summaries to multiple formats (DOCX, Markdown, TXT) with proper formatting preservation

### Key Components

- **`main.py`**: FastAPI application entry point with web UI and API endpoints
- **`yt_summarizer.py`**: Core video processing logic and orchestration
- **`task_manager.py`**: Manages concurrent tasks with persistence to `tasks.json`
- **`improved_md_to_docx.py`**: Advanced Markdown to Word conversion maintaining formatting
- **`config.py`**: Centralized configuration management for API keys and paths
- **`error_handler.py`**: Retry logic and error handling for API calls
- **`batch_processor.py`**: Handles multiple video processing concurrently

### API Integration

The application uses two AI services:
- **OpenAI**: Required for Whisper transcription, optional for summarization
- **Google Gemini**: Primary summarization model with better Chinese language support

API keys can be provided via:
1. Web interface (takes precedence)
2. Environment variables in `.env` file
3. Direct environment variables

### Task Flow

1. User submits YouTube URL via web interface
2. Task created and tracked in `task_manager.py`
3. Video downloaded to `audio/` directory
4. Audio transcribed and saved to `transcripts/`
5. Summary generated and saved to `summaries/`
6. Results displayed with download options
7. Temporary files cleaned up (configurable)

### Error Handling

- Automatic retry with exponential backoff for API failures
- Fallback from Gemini to OpenAI if primary model fails
- Comprehensive error messages displayed to users
- Task persistence allows recovery from crashes