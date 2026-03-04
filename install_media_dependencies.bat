@echo off
echo ========================================
echo Installing Media Processing Dependencies
echo ========================================
echo.

echo Installing Whisper for audio/video transcription...
pip install openai-whisper

echo.
echo Installing MoviePy for video processing...
pip install moviepy

echo.
echo Installing pdfplumber for PDF processing...
pip install pdfplumber

echo.
echo Installing Pillow for image processing...
pip install Pillow

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo You can now process:
echo - Audio files (MP3, WAV, M4A, OGG)
echo - Video files (MP4, MOV, AVI, WEBM)
echo - PDF documents
echo - DOCX documents
echo.
echo Note: First-time Whisper usage will download the model (~140MB for base model)
echo.
pause
