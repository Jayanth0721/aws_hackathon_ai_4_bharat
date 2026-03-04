# Media & Document Processing Guide

## Overview

The Ashoka platform now supports comprehensive media and document analysis:

- 🎵 **Audio Analysis** - Transcribe audio files using Whisper
- 🎥 **Video Analysis** - Extract audio and transcribe using Whisper
- 📄 **PDF Analysis** - Extract text from PDF documents
- 📝 **DOCX Analysis** - Extract text from Word documents
- 📃 **TXT/MD Analysis** - Direct text file reading

All extracted text is then analyzed using your existing Gemini AI for:
- Sentiment analysis
- Keyword extraction
- Topic identification
- Quality scoring
- Risk assessment

## Installation

### Quick Install (All Dependencies)

**Windows:**
```bash
install_media_dependencies.bat
```

**Linux/Mac:**
```bash
bash install_media_dependencies.sh
```

### Manual Install

```bash
# Audio/Video processing
pip install openai-whisper moviepy

# Document processing
pip install pdfplumber python-docx Pillow
```

## Testing

Run the test script to verify all processors are available:

```bash
python test_media_processing.py
```

## How It Works

### Audio Files (MP3, WAV, M4A, OGG)

1. Upload audio file
2. Whisper transcribes to text (locally, no API calls)
3. Text is sent to Gemini for analysis
4. Results displayed in dashboard

**Processing time:** ~30 seconds for 1-minute audio (first time downloads model)

### Video Files (MP4, MOV, AVI, WEBM)

1. Upload video file
2. Audio is extracted from video
3. Whisper transcribes audio to text
4. Text is sent to Gemini for analysis
5. Results displayed in dashboard

**Processing time:** ~1-2 minutes for 1-minute video

### PDF Documents

1. Upload PDF file
2. pdfplumber extracts text from all pages
3. Text is sent to Gemini for analysis
4. Results displayed in dashboard

**Processing time:** ~5-10 seconds for 10-page PDF

### DOCX Documents

1. Upload DOCX file
2. python-docx extracts text and tables
3. Text is sent to Gemini for analysis
4. Results displayed in dashboard

**Processing time:** ~2-5 seconds

## Supported File Types

| Type | Extensions | Processor | Status |
|------|-----------|-----------|--------|
| Audio | .mp3, .wav, .m4a, .ogg | Whisper (local) | ✅ Ready |
| Video | .mp4, .mov, .avi, .webm | Whisper (local) | ✅ Ready |
| PDF | .pdf | pdfplumber | ✅ Ready |
| Word | .docx | python-docx | ✅ Ready |
| Text | .txt, .md | Direct read | ✅ Ready |
| Image | .jpg, .png, .gif | OCR (future) | 🔄 Coming Soon |

## Technical Details

### Whisper Model

- **Model:** base (fastest, good accuracy)
- **Size:** ~140MB (downloads on first use)
- **Languages:** 99+ languages auto-detected
- **Runs:** Locally (no API calls, fully free)

**Upgrade to better accuracy:**
```python
# In src/services/media_processor.py, change:
self.model = whisper.load_model("base")  # Current
# To:
self.model = whisper.load_model("small")  # Better accuracy, slower
# Or:
self.model = whisper.load_model("medium")  # Best accuracy, slowest
```

### Fallback Behavior

If processors are not installed, the system falls back to mock data so the dashboard still works. This allows:
- Demo without installing heavy dependencies
- Gradual feature adoption
- Testing without full setup

## Performance Tips

### For Faster Processing

1. **Use base Whisper model** (default) - fastest
2. **Process shorter clips** - split long videos
3. **Use GPU** - Whisper supports CUDA for 10x speedup

### For Better Accuracy

1. **Upgrade Whisper model** to small or medium
2. **Use high-quality audio** - clear speech, low noise
3. **Single speaker** - works best with one person talking

## Troubleshooting

### Whisper Installation Issues

**Error:** "No module named 'whisper'"
```bash
pip install openai-whisper
```

**Error:** "ffmpeg not found"
```bash
# Windows (using chocolatey):
choco install ffmpeg

# Linux:
sudo apt install ffmpeg

# Mac:
brew install ffmpeg
```

### MoviePy Issues

**Error:** "MoviePy requires ffmpeg"
- Install ffmpeg (see above)

### PDF Processing Issues

**Error:** "No text extracted from PDF"
- PDF might be image-based (scanned document)
- Solution: Use OCR (future feature)

### Memory Issues

**Error:** "Out of memory"
- Process smaller files
- Use base Whisper model
- Close other applications

## Integration with Dashboard

The file upload in the dashboard automatically:
1. Detects file type
2. Routes to appropriate processor
3. Extracts text/transcript
4. Sends to Gemini for analysis
5. Displays results

No code changes needed - just upload and analyze!

## Cost Analysis

| Feature | Cost | Notes |
|---------|------|-------|
| Whisper (Audio/Video) | **FREE** | Runs locally |
| pdfplumber (PDF) | **FREE** | Open source |
| python-docx (DOCX) | **FREE** | Open source |
| Gemini Analysis | **FREE** | Using your existing API key |

**Total cost:** $0 (except Gemini API usage for analysis)

## Future Enhancements

- 🔄 Image OCR using Tesseract
- 🔄 Batch processing multiple files
- 🔄 Progress indicators for long files
- 🔄 Speaker diarization (who said what)
- 🔄 Timestamp extraction
- 🔄 Multi-language subtitle generation

## Questions?

Check the main README.md or SETUP.md for general platform setup.

For media processing specific issues, check the logs in the dashboard or run:
```bash
python test_media_processing.py
```
