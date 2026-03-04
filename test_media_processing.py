"""Test Media and Document Processing"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, 'src')

from src.services.media_processor import media_processor
from src.services.document_processor import document_processor

def test_processors():
    """Test if processors are available"""
    
    print("=" * 60)
    print("MEDIA & DOCUMENT PROCESSING TEST")
    print("=" * 60)
    print()
    
    # Test Whisper availability
    print("🎵 Audio/Video Processing (Whisper):")
    if media_processor.whisper_available:
        print("   ✅ Whisper is available and ready!")
        print("   📊 Model loaded: base")
    else:
        print("   ❌ Whisper not available")
        print("   💡 Install with: pip install openai-whisper")
        print("   💡 Or run: install_media_dependencies.bat (Windows)")
        print("   💡 Or run: bash install_media_dependencies.sh (Linux/Mac)")
    print()
    
    # Test PDF processing
    print("📄 PDF Processing (pdfplumber):")
    if document_processor.pdf_available:
        print("   ✅ pdfplumber is available and ready!")
    else:
        print("   ❌ pdfplumber not available")
        print("   💡 Install with: pip install pdfplumber")
    print()
    
    # Test DOCX processing
    print("📝 DOCX Processing (python-docx):")
    if document_processor.docx_available:
        print("   ✅ python-docx is available and ready!")
    else:
        print("   ❌ python-docx not available")
        print("   💡 Install with: pip install python-docx")
    print()
    
    # Summary
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    all_ready = (
        media_processor.whisper_available and
        document_processor.pdf_available and
        document_processor.docx_available
    )
    
    if all_ready:
        print("✅ All processors are ready!")
        print()
        print("You can now analyze:")
        print("  🎵 Audio files (MP3, WAV, M4A, OGG)")
        print("  🎥 Video files (MP4, MOV, AVI, WEBM)")
        print("  📄 PDF documents")
        print("  📝 DOCX documents")
        print("  📃 TXT/MD files")
    else:
        print("⚠️  Some processors are not available")
        print()
        print("To install all dependencies, run:")
        print("  Windows: install_media_dependencies.bat")
        print("  Linux/Mac: bash install_media_dependencies.sh")
        print()
        print("Or install individually:")
        if not media_processor.whisper_available:
            print("  pip install openai-whisper moviepy")
        if not document_processor.pdf_available:
            print("  pip install pdfplumber")
        if not document_processor.docx_available:
            print("  pip install python-docx")
    
    print()
    print("=" * 60)

if __name__ == "__main__":
    test_processors()
