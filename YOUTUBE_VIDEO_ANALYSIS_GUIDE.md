# YouTube Video Analysis - User Guide

Complete guide to using the YouTube Video Analysis feature in Ashoka Platform.

## Table of Contents
1. [Overview](#overview)
2. [Getting Started](#getting-started)
3. [Analysis Modes](#analysis-modes)
4. [Supported URL Formats](#supported-url-formats)
5. [Step-by-Step Guide](#step-by-step-guide)
6. [Understanding Results](#understanding-results)
7. [Features](#features)
8. [Limitations](#limitations)
9. [Troubleshooting](#troubleshooting)
10. [Best Practices](#best-practices)

---

## Overview

The YouTube Video Analysis feature allows you to analyze YouTube videos directly from their URL without manual download. The system automatically:
- Extracts video metadata
- Downloads and transcribes audio (using Whisper AI)
- Analyzes content (using Gemini AI)
- Provides comprehensive insights

**Powered by:**
- **yt-dlp**: YouTube video/audio extraction
- **Whisper AI**: Audio transcription
- **Gemini AI**: Content analysis

---

## Getting Started

### Prerequisites

Before using YouTube analysis, ensure:
1. yt-dlp is installed (`pip install yt-dlp`)
2. FFmpeg is installed and in PATH
3. Whisper AI is installed (`pip install openai-whisper`)
4. Gemini API key is configured in `.env`

### Accessing the Feature

1. Log in to Ashoka Platform
2. Navigate to "Content Intelligence & Analysis"
3. Click the "YOUTUBE" tab
4. You'll see the YouTube analysis interface

---

## Analysis Modes

### Quick Summary (Fast - 2-5 seconds)

**What it does:**
- Retrieves video metadata only
- No download or transcription
- Instant results

**Includes:**
- Video title
- Channel name
- Duration
- View count
- Thumbnail image
- Video description

**Best for:**
- Quick video preview
- Checking video details
- Verifying correct video
- When you only need basic info

### Full Analysis (Comprehensive - 2-5 minutes)

**What it does:**
- Downloads audio from video
- Transcribes audio to text
- Analyzes content with AI
- Generates insights

**Includes:**
- All Quick Summary information
- Complete transcript
- AI-generated summary
- Sentiment analysis
- Keywords extraction
- Topics identification
- Key takeaways
- Word/character count

**Best for:**
- Understanding video content
- Content research
- Sentiment analysis
- Extracting key points
- Creating summaries

---

## Supported URL Formats

The system accepts various YouTube URL formats:

### Standard URLs
```
https://www.youtube.com/watch?v=dQw4w9WgXcQ
https://youtube.com/watch?v=dQw4w9WgXcQ
http://www.youtube.com/watch?v=dQw4w9WgXcQ
```

### Shortened URLs
```
https://youtu.be/dQw4w9WgXcQ
http://youtu.be/dQw4w9WgXcQ
```

### URLs with Parameters
```
https://www.youtube.com/watch?v=dQw4w9WgXcQ&feature=share
https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PLxxx
```

### URLs with Timestamps
```
https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=30s
https://youtu.be/dQw4w9WgXcQ?t=45
```

### YouTube Shorts
```
https://www.youtube.com/shorts/dQw4w9WgXcQ
```

### Mobile URLs
```
https://m.youtube.com/watch?v=dQw4w9WgXcQ
```

---

## Step-by-Step Guide

### Quick Summary Analysis

1. **Navigate to YouTube Tab**
   - Go to Content Intelligence & Analysis
   - Click "YOUTUBE" tab

2. **Enter YouTube URL**
   - Paste video URL in the input field
   - Example: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`

3. **Select Analysis Mode**
   - Choose "Quick Summary" (default)

4. **Click "Analyze Video"**
   - Wait 2-5 seconds for results

5. **View Results**
   - Video thumbnail appears
   - Metadata displayed below
   - Description available in expansion panel

### Full Analysis

1. **Navigate to YouTube Tab**
   - Go to Content Intelligence & Analysis
   - Click "YOUTUBE" tab

2. **Enter YouTube URL**
   - Paste video URL in the input field

3. **Select Analysis Mode**
   - Choose "Full Analysis"

4. **Click "Analyze Video"**
   - Progress indicator appears
   - Shows current stage (Downloading, Transcribing, Analyzing)
   - Wait 2-5 minutes depending on video length

5. **View Comprehensive Results**
   - Video information card
   - AI-generated summary
   - Sentiment analysis with confidence
   - Keywords (top 10)
   - Main topics
   - Key takeaways
   - Full transcript (expandable)

6. **Interact with Results**
   - Copy transcript to clipboard
   - Expand/collapse sections
   - Review detailed analysis

---

## Understanding Results

### Video Information

**Title**: Full video title as it appears on YouTube

**Channel**: Name of the YouTube channel/uploader

**Duration**: Video length in MM:SS format

**Views**: Total view count (formatted with commas)

**Language**: Detected language of the audio/transcript

**Thumbnail**: Video thumbnail image

### AI-Generated Summary

A concise 2-3 paragraph summary of the video content, highlighting:
- Main topic or theme
- Key points discussed
- Overall message or conclusion

### Sentiment Analysis

**Classification**: Positive, Neutral, or Negative

**Confidence**: Percentage indicating AI's confidence in the classification
- 90%+ = Very confident
- 70-90% = Confident
- <70% = Less confident

**Color Coding**:
- Green badge = Positive
- Gray badge = Neutral
- Red badge = Negative

### Keywords

Top 10 most relevant keywords extracted from the transcript:
- Displayed as orange badges
- Represents main concepts and terms
- Useful for quick topic identification

### Topics

Main topics or themes identified in the video:
- Listed with bullet points
- Organized by relevance
- Helps understand content structure

### Key Takeaways

3-5 most important points from the video:
- Numbered list
- Actionable insights
- Main lessons or conclusions

### Full Transcript

Complete text transcription of the video audio:
- Expandable section to save space
- Copy button for easy export
- Word and character count displayed
- Preserves original speech patterns

---

## Features

### Transcription Caching

**How it works:**
- Transcriptions are cached for 24 hours
- Analyzing the same video twice uses cached transcript
- Significantly faster second analysis (skips download/transcription)
- Cache automatically expires after 24 hours

**Benefits:**
- Faster repeat analysis
- Reduced processing time
- Lower resource usage
- Cost optimization

### Rate Limiting

**User Limits:**
- 10 analyses per hour per user
- Sliding window (resets gradually)
- Prevents abuse and ensures fair usage

**Admin Users:**
- Unlimited analyses
- No rate limiting
- For administrative purposes

**When limit exceeded:**
- Clear error message displayed
- Shows when you can analyze again
- Suggests waiting or contacting admin

### Query History

**Automatic Tracking:**
- All Full Analyses saved to history
- Quick Summaries not saved (metadata only)
- Accessible from dashboard

**History Includes:**
- Video URL and title
- Thumbnail
- Analysis timestamp
- Analysis mode
- Full results

**Benefits:**
- Review past analyses
- Track research progress
- Avoid duplicate work
- Reference previous insights

### Error Handling

**Clear Error Messages:**
- Specific error codes
- User-friendly descriptions
- Actionable guidance
- Stage information (where it failed)

**Error Types:**
- Invalid URL format
- Video unavailable
- Video too long
- Download failed
- Transcription failed
- Analysis failed
- Network errors
- Rate limit exceeded

### Progress Indicators

**Real-time Updates:**
- Loading spinner during processing
- Current stage display
- Estimated time remaining
- Cancel option (future feature)

**Stages:**
1. Validating URL
2. Fetching metadata
3. Downloading audio
4. Transcribing audio
5. Analyzing content
6. Storing results

---

## Limitations

### Video Duration

**Maximum**: 2 hours (7200 seconds)

**Reason**: 
- Processing time constraints
- Resource management
- Optimal user experience

**Workaround**: 
- Split long videos into segments
- Analyze key portions separately

### Video Availability

**Not Supported:**
- Private videos
- Deleted videos
- Region-restricted videos
- Age-restricted videos (some cases)
- Videos requiring login

**Error Message**: "Video unavailable. The video may be private, deleted, or restricted in your region."

### Rate Limiting

**Standard Users**: 10 analyses per hour

**Why**: 
- Fair resource allocation
- Prevent abuse
- Cost management
- Server load balancing

**Solution**: 
- Wait for rate limit to reset
- Contact admin for increased limits
- Use Quick Summary (doesn't count toward limit)

### URL Format

**Must be YouTube URLs only**

**Not Supported:**
- Vimeo, Dailymotion, etc.
- Direct video files
- Embedded players
- Playlist URLs (coming soon)

### Language Support

**Transcription**: 
- Whisper AI supports 90+ languages
- Automatic language detection
- Quality varies by language

**Analysis**: 
- Gemini AI works best with English
- Other languages supported but may vary in quality

---

## Troubleshooting

### "Invalid YouTube URL format"

**Cause**: URL doesn't match YouTube patterns

**Solutions:**
1. Check URL is from youtube.com or youtu.be
2. Ensure URL contains video ID
3. Remove extra characters or spaces
4. Try copying URL directly from browser
5. Use standard format: `https://www.youtube.com/watch?v=VIDEO_ID`

### "Video unavailable"

**Cause**: Video is private, deleted, or restricted

**Solutions:**
1. Verify video exists by opening in browser
2. Check if video is public
3. Try a different video
4. Check for region restrictions
5. Ensure video isn't age-restricted

### "Video duration exceeds the 2-hour limit"

**Cause**: Video is longer than 2 hours

**Solutions:**
1. Select a shorter video
2. Analyze specific segments separately
3. Use Quick Summary for basic info
4. Contact admin for special cases

### "Failed to extract audio from video"

**Cause**: Download or extraction error

**Solutions:**
1. Check internet connection
2. Verify FFmpeg is installed
3. Try again (temporary network issue)
4. Check if video has audio track
5. Try a different video

### "Transcription failed"

**Cause**: Whisper AI error or audio issue

**Solutions:**
1. Verify Whisper is installed
2. Check audio file was created
3. Ensure sufficient disk space
4. Try again (may be temporary)
5. Check console logs for details

### "Content analysis failed"

**Cause**: Gemini AI error or API issue

**Solutions:**
1. Verify Gemini API key is configured
2. Check API quota hasn't been exceeded
3. Verify internet connection
4. Try again later
5. Check console for specific error

### "Rate limit exceeded"

**Cause**: Exceeded 10 analyses per hour

**Solutions:**
1. Wait for rate limit window to reset
2. Use Quick Summary (doesn't count)
3. Contact admin for increased limits
4. Check when you can analyze again

### Processing Takes Too Long

**Normal Times:**
- Quick Summary: 2-5 seconds
- Full Analysis (5 min video): 2-3 minutes
- Full Analysis (30 min video): 5-10 minutes

**If Slower:**
1. Check internet speed
2. Verify system resources
3. Close other applications
4. Check if caching is working
5. Try shorter video first

---

## Best Practices

### Choosing Analysis Mode

**Use Quick Summary when:**
- You only need basic video info
- Checking if it's the right video
- Previewing before full analysis
- Saving time and resources
- Browsing multiple videos

**Use Full Analysis when:**
- You need detailed content insights
- Creating summaries or notes
- Researching specific topics
- Analyzing sentiment
- Extracting key points

### URL Management

**Best Practices:**
1. Copy URLs directly from browser
2. Use standard YouTube URLs when possible
3. Remove unnecessary parameters
4. Verify URL before analyzing
5. Keep URLs organized for reference

### Optimizing Performance

**Tips:**
1. Use cached results when available
2. Analyze shorter videos first
3. Use Quick Summary for previews
4. Close unnecessary browser tabs
5. Ensure stable internet connection

### Managing Rate Limits

**Strategies:**
1. Plan analyses in advance
2. Use Quick Summary liberally
3. Prioritize important videos
4. Spread analyses over time
5. Request admin access if needed

### Working with Results

**Recommendations:**
1. Copy transcripts for offline use
2. Save important analyses
3. Review key takeaways first
4. Use keywords for quick reference
5. Export results when needed

### Content Research

**Workflow:**
1. Use Quick Summary to preview videos
2. Select most relevant for Full Analysis
3. Review summaries and takeaways
4. Copy transcripts for detailed review
5. Organize findings by topic

---

## Advanced Tips

### Batch Analysis

**Current**: Analyze one video at a time

**Coming Soon**: Batch processing multiple videos

**Workaround**: 
- Queue videos in separate tabs
- Use Quick Summary for initial screening
- Full Analysis for selected videos

### Playlist Analysis

**Current**: Single video only

**Coming Soon**: Analyze entire playlists

**Workaround**:
- Analyze key videos individually
- Use Quick Summary for overview
- Full Analysis for important videos

### Export Options

**Current**: Copy transcript to clipboard

**Coming Soon**: 
- Export to PDF
- Export to DOCX
- Export to JSON
- Email results

**Workaround**:
- Copy and paste into document
- Screenshot results
- Save in browser

### Collaboration

**Current**: Individual analysis

**Coming Soon**: 
- Share analysis results
- Collaborative annotations
- Team workspaces

**Workaround**:
- Copy results to shared document
- Share video URL with team
- Discuss findings separately

---

## Support

### Getting Help

1. Check this guide first
2. Review SETUP.md for configuration
3. Check FEATURES.md for feature details
4. Review console logs for errors
5. Contact administrator

### Reporting Issues

When reporting problems, include:
- YouTube URL (if not sensitive)
- Error message received
- Analysis mode used
- Browser console logs
- Steps to reproduce

### Feature Requests

To request new features:
- Describe the use case
- Explain expected behavior
- Provide examples
- Suggest implementation

---

## Frequently Asked Questions

### Q: How long does Full Analysis take?

**A**: Typically 2-5 minutes for a 5-10 minute video. Longer videos take proportionally more time.

### Q: Can I analyze private videos?

**A**: No, only public YouTube videos are supported.

### Q: Does Quick Summary count toward rate limit?

**A**: No, only Full Analysis counts toward the 10/hour limit.

### Q: How accurate is the transcription?

**A**: Whisper AI is highly accurate (90%+) for clear audio in supported languages. Accuracy may vary with background noise or accents.

### Q: Can I analyze videos in other languages?

**A**: Yes, Whisper supports 90+ languages. Analysis quality is best for English but works for other languages.

### Q: How long are transcriptions cached?

**A**: 24 hours. After that, the video will be re-transcribed if analyzed again.

### Q: Can I download the transcript?

**A**: Currently, you can copy to clipboard. Export features coming soon.

### Q: What happens if analysis fails midway?

**A**: The system will show which stage failed and provide an error message. Temporary files are automatically cleaned up.

### Q: Can I cancel a running analysis?

**A**: Not currently. This feature is planned for future release.

### Q: Why is my video "too long"?

**A**: Videos over 2 hours are not supported due to processing constraints. This limit may be increased in future updates.

---

## Updates and Changelog

### Current Version: 1.0

**Features:**
- Quick Summary mode
- Full Analysis mode
- Transcription caching
- Rate limiting
- Query history
- Error handling
- Progress indicators

**Coming Soon:**
- Playlist analysis
- Subtitle integration
- Export options
- Batch processing
- Cancel operation
- Advanced filtering
- Collaborative features

---

## Conclusion

The YouTube Video Analysis feature provides powerful tools for understanding video content without manual transcription. By leveraging AI technologies (Whisper and Gemini), you can quickly extract insights, summaries, and key points from any public YouTube video.

For best results:
- Use Quick Summary for previews
- Use Full Analysis for detailed insights
- Leverage caching for repeat analyses
- Manage rate limits effectively
- Review all result sections

Happy analyzing!
