# Installing FFmpeg on Windows for Whisper Audio/Video Processing

## Problem

You're seeing this error:
```
[WinError 2] The system cannot find the file specified
Whisper processing failed
```

This happens because **Whisper requires FFmpeg** to process audio/video files, but FFmpeg is not installed or not in your system PATH.

## Solution: Install FFmpeg

### Option 1: Using winget (Recommended - Built into Windows 10/11)

**winget** is Microsoft's official package manager, pre-installed on Windows 10 (version 1809+) and Windows 11.

1. **Open PowerShell or Command Prompt** (no admin needed)

2. **Install FFmpeg**:
   ```bash
   winget install --id=Gyan.FFmpeg -e
   ```

3. **Verify installation**:
   ```bash
   ffmpeg -version
   ```

4. **Restart your terminal** and run the dashboard again

---

### Option 2: Using Chocolatey (Alternative)

**First, install Chocolatey:**

1. **Open PowerShell as Administrator**
2. **Run this command**:
   ```powershell
   Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
   ```

**Then install FFmpeg:**

3. **Install FFmpeg**:
   ```powershell
   choco install ffmpeg
   ```

4. **Verify installation**:
   ```powershell
   ffmpeg -version
   ```

5. **Restart your terminal** and run the dashboard again

---

### Option 3: Manual Installation

1. **Download FFmpeg**:
   - Go to: https://www.gyan.dev/ffmpeg/builds/
   - Download: `ffmpeg-release-essentials.zip`

2. **Extract the ZIP file**:
   - Extract to: `C:\ffmpeg`
   - You should have: `C:\ffmpeg\bin\ffmpeg.exe`

3. **Add to System PATH**:
   - Press `Win + X` → Select "System"
   - Click "Advanced system settings"
   - Click "Environment Variables"
   - Under "System variables", find "Path" and click "Edit"
   - Click "New" and add: `C:\ffmpeg\bin`
   - Click "OK" on all windows

4. **Verify installation**:
   - Open a NEW terminal (important!)
   - Run:
   ```bash
   ffmpeg -version
   ```

5. **Restart your terminal** and run the dashboard again

---

## After Installation

Once FFmpeg is installed:

1. **Close all terminals**
2. **Open a new terminal**
3. **Run the dashboard**:
   ```bash
   python run_dashboard.py
   ```

4. **Upload an audio/video file** - it should now work!

---

## Verification

To verify FFmpeg is working:

```bash
# Check FFmpeg version
ffmpeg -version

# Check if it's in PATH (Windows)
where ffmpeg
```

You should see output showing the FFmpeg version and location.

---

## What FFmpeg Does

FFmpeg is a free, open-source multimedia framework that:
- Converts audio/video formats
- Extracts audio from video files
- Processes audio streams
- Handles various codecs (MP3, WAV, MP4, etc.)

**Whisper uses FFmpeg to:**
- Load audio files in various formats
- Convert audio to the format Whisper expects
- Extract audio from video files (with MoviePy)

---

## Troubleshooting

### "ffmpeg is not recognized"
- Make sure you added FFmpeg to PATH correctly
- Restart your terminal after adding to PATH
- Try opening a NEW terminal window

### "Permission denied"
- Run PowerShell as Administrator when installing with Chocolatey
- winget doesn't require admin for most installations

### Still not working?
- Uninstall and reinstall FFmpeg
- Make sure the PATH points to the `bin` folder (e.g., `C:\ffmpeg\bin`)
- Restart your computer

---

## Alternative: Use Pre-converted Audio

If you can't install FFmpeg, you can:
1. Convert audio/video to WAV format using an online converter
2. Upload the WAV file instead
3. Whisper can process WAV files without FFmpeg

But this is not recommended - installing FFmpeg is much better!
