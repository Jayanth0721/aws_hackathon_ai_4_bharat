# Features Documentation - Ashoka Platform

Comprehensive guide to all features in the Ashoka GenAI Governance Platform.

## Recent UI/UX Improvements (March 2026)

### Dashboard Enhancements

**Command Center:**
- Session timer moved to header (top-right) with clock icon for better visibility
- Date-time display with calendar icon (07-Mar-2026 10:05 PM IST)
- Role badge display (USER/CREATOR/ADMIN)
- Purple "Workspace for {username}" text for personalization

**Help Section:**
- Renamed from "Help & Support" to "Help"
- Quick Help panels (Getting Started, Common Issues, Feature Access) now full-width
- Contact Support cards in horizontal layout

**Content Intelligence:**
- Analysis headers changed to black for better visibility
- Clear button now clears both input AND analysis results
- Improved user feedback

**Monitoring & Alerts:**
- Monitoring section hidden for User role (Creator/Admin only)
- Manual refresh buttons removed (auto-refresh only)
- System Health moved from Overview to Alerts panel
- Minimum 1 warning displayed for better visibility

**Overview Panel:**
- System Health section removed (now in Alerts)
- Enhanced platform details with Core Services and How It Works
- Cleaner focus on content metrics

**Authentication:**
- OTP input speed reduced by 0.5 seconds for smoother experience

## Table of Contents
1. [Content Intelligence & Analysis](#content-intelligence--analysis)
2. [AI Content Generator](#ai-content-generator)
3. [Multi-Platform Content Transformer](#multi-platform-content-transformer)
4. [Real-Time Monitoring](#real-time-monitoring)
5. [Alerts & Notifications](#alerts--notifications)
6. [Security Dashboard](#security-dashboard)
7. [User Profile & Settings](#user-profile--settings)

---

## Content Intelligence & Analysis

### Text Analysis (Working)

Analyze text content using Google Gemini AI.

**How to use:**
1. Navigate to "Content Intelligence & Analysis"
2. Select "TEXT" tab
3. Paste or type your content
4. Click "Analyze Text"

**Analysis includes:**
- **Summary**: AI-generated summary of content
- **Sentiment**: Positive/Neutral/Negative with confidence score
- **Keywords**: Key terms extracted from content
- **Topics**: Main topics identified
- **Takeaways**: Key points and insights
- **Quality Score**: Overall content quality (0-100%)
- **Word/Character Count**: Content statistics

**Results are stored** in database and appear in "Analysis & Generator History" table.

### File Upload Support

Upload files for future analysis (currently showing preview with remove option).

**Supported file types:**

#### Audio Files
- Formats: MP3, WAV, M4A, OGG
- Shows: 🎵 filename with red X remove button

#### Image Files
- Formats: JPG, PNG, GIF, WEBP
- Shows: 📷 filename with red X remove button

#### Video Files
- Formats: MP4, MOV, AVI, WEBM
- Shows: 🎥 filename with red X remove button

#### Document Files
- Formats: PDF, DOCX, TXT, MD
- Shows: 📄 filename with red X remove button

**How to remove uploaded files:**
- Click the red "X" button next to filename
- File preview will be cleared
- You can upload another file

### Analysis History

View all previously analyzed content.

**Features:**
- Table showing all analyzed content
- Preview button (👁️) to view full analysis
- Reload button (📁) to load content back into analyzer
- Sorted by most recent first

---

## AI Content Generator

Generate AI-powered content using Google Gemini.

### Content Restrictions

**Admin-controlled restrictions** may block content generation if your prompt contains restricted keywords or phrases. If blocked:
- You'll see a detailed violation message
- Lists which restrictions were violated
- Modify your prompt to remove restricted terms

See [Security Dashboard - AI Content Generation Restrictions](#ai-content-generation-restrictions-admin-only) for details.

### Text/Notes Generation (Working)

**How to use:**
1. Navigate to "AI Content Generator" section
2. Select "Text/Notes" option
3. Enter your prompt (e.g., "Write a professional email about project updates")
4. Click "Generate Content"

**Features:**
- AI-generated professional content
- Copy to clipboard button
- "Analyze This Content" button (sends to analyzer)
- "Use in Transformer" button (loads into transformer)
- **Restriction checking**: Prompts are checked against admin-defined restrictions

**If content is blocked:**
- ⛔ Red warning card appears
- Shows which keywords violated restrictions
- Explains why each restriction exists
- Prompts you to modify your request

### Image Generation (Coming Soon)

Select "Image" option to see coming soon message.

### Video Generation (Coming Soon)

Select "Video" option to see coming soon message.

---

## Multi-Platform Content Transformer

Transform content for different social media platforms.

**How to use:**
1. Navigate to "Multi-Platform Content Transformer"
2. Enter your original content
3. Select target platforms (multiple selection allowed):
   - Twitter
   - LinkedIn
   - Instagram
   - Facebook
   - Blog
4. Choose tone:
   - Professional
   - Casual
   - Formal
   - Friendly
5. Toggle "Include Hashtags" if desired
6. Click "Transform Content"

**Results:**
- Platform-specific transformed content
- Character count for each platform
- Copy button for each transformation
- All transformations stored in history

### Transform History

View and reload past transformations.

**Features:**
- Table showing last 20 transformations
- Preview button (👁️) to view all platform versions
- Reload button (📁) to load back into transformer
- Shows: original content, platforms, tone, hashtag setting

---

## Real-Time Monitoring

Track system performance and operations.

**Access:** Creator and Admin roles only (hidden for User role)

**Metrics displayed:**
- **Total Operations**: Count of all operations
- **Success Rate**: Percentage of successful operations
- **Avg Latency**: Average response time
- **Active Alerts**: Current alert count

**Operation types tracked:**
- Content analysis
- Content transformation
- Risk assessment
- Quality checks

**Refresh:**
- Auto-refreshes every 30 seconds
- Manual refresh button removed for cleaner UI

**Role-Based Visibility:**
- ✅ Visible for Creator role
- ✅ Visible for Admin role
- ❌ Hidden for User role

---

## Alerts & Notifications

Real-time alerts from Content Intelligence analysis and Multi-Platform Content Transformer operations.

### UI Improvements

**Recent Changes:**
- Manual refresh button removed (auto-refresh only)
- System Health section moved from Overview to Alerts panel
- Minimum 1 warning always displayed for better visibility
- Cleaner, more focused interface

### System Health

**Now located in Alerts panel** (moved from Overview):
- **AI Model Performance**: 95% operational
- **Content Processing Rate**: Real-time metrics
- **Storage Utilization**: Current usage levels
- **Status Badges**: API, Database, AI health indicators

### Data Sources

Alerts are generated from:
- **Content Intelligence History**: Analysis results, sentiment detection, quality scores
- **Transform History**: Platform transformations, tone conversions
- **Risk Assessments**: Policy violations, toxicity detection, backlash risks

### Alert Types

#### Critical Alerts (Red)
- High-risk content detected
- Content should be blocked
- Security violations
- High toxicity scores

#### Warning Alerts (Orange)
- Low quality content (< 60%)
- Negative sentiment detected (> 70% confidence)
- High policy/backlash risk
- Review recommended

#### Success Alerts (Green)
- High quality content (≥ 85%)
- Successful transformations
- Positive outcomes
- Content analyzed successfully

#### Info Alerts (Blue)
- General information
- System notifications
- Content processed

### Alert Statistics

Dashboard shows:
- **Critical**: Requires immediate action
- **Warnings**: Review recommended (minimum 1 displayed)
- **Success**: Operations completed
- **Total Alerts**: Last 24 hours

### Alert Filtering

Filter alerts by type:
- **All**: Show all alerts
- **Critical**: Only critical alerts
- **Warning**: Only warnings
- **Info**: Only informational alerts
- **Success**: Only success notifications

### Time Display

Alerts show relative time:
- "Just now" (< 1 minute)
- "X minutes ago"
- "X hours ago"
- "X days ago"

### Auto-Refresh

- Alerts auto-refresh every 10 minutes
- Manual refresh button removed for cleaner UI
- Shows last 20 most recent alerts

---

## Security Dashboard

**Access:** Admin users only (role: admin)

### Login Activity Monitoring

Track all login attempts:
- Username
- IP Address
- Location
- Device Information
- Status (Success/Failed)
- Timestamp
- Session ID

**Features:**
- Real-time updates
- Success/failure indicators
- Geographic tracking
- Device fingerprinting
- 7-day login activity chart

### Security Events

Monitor security-related events:
- Login events
- Password verification
- Session creation/extension
- Settings updates
- New device detection

**Event details:**
- Event type
- Description
- Timestamp
- Associated user
- Metadata

### Security Metrics

Dashboard displays:
- **Active Sessions**: Current user sessions
- **Failed Login Attempts**: Last 24 hours
- **Security Score**: Overall security health (0-100%)
- **Last Password Change**: Days since last change

### AI Content Generation Restrictions (Admin Only)

**NEW FEATURE**: Control what content can be generated by AI.

**Purpose:**
- Block AI content generation for specific keywords/phrases
- Prevent generation of inappropriate, illegal, or policy-violating content
- Admin-controlled content governance

**How to use:**
1. Navigate to Security tab (admin only)
2. Scroll to "AI Content Generation Restrictions" section (red card)
3. Enter restriction keyword/phrase (e.g., "violence", "hate speech")
   - You can enter multiple keywords separated by commas: "violence, hate speech, illegal"
   - Each keyword will be checked separately
4. Optionally add description explaining why it's restricted
5. Click "Add Restriction"

**Features:**
- **Add Restrictions**: Define keywords/phrases to block
- **Multiple Keywords**: Separate keywords with commas (e.g., "bjp, congress, politics")
- **Active/Inactive Toggle**: Enable/disable restrictions without deleting
- **Delete Restrictions**: Remove restrictions permanently
- **Description Field**: Document why each restriction exists
- **Real-time Enforcement**: Blocks content generation immediately
- **Case-Insensitive**: Matches keywords regardless of case

**When user tries to generate restricted content:**
- ⛔ Generation is blocked
- Detailed violation message shown
- Lists all violated restrictions
- Suggests removing restricted terms

**Restriction Management:**
- View all active restrictions
- See who added each restriction and when
- Toggle restrictions on/off
- Delete restrictions
- Restrictions are case-insensitive

**Example restrictions:**
- "violence" - Prevents violent content
- "hate speech" - Blocks discriminatory content
- "illegal activities" - Prevents illegal content generation
- "explicit content" - Blocks adult content
- "bjp, congress, politics" - Blocks political party content (multiple keywords in one restriction)
- "competitor1, competitor2" - Prevents competitor mentions

### Access Control

Security tab visibility:
- ✅ Visible for admin role
- ❌ Hidden for user role
- ❌ Hidden for creator role

---

## User Profile & Settings

### Profile Information

View your account details:
- Username
- Email (format: username@ashoka.ai)
- Role (User, Creator, or Admin)
- Account creation date

**Access:** Click profile icon in top-right corner

### Settings

Configure your preferences:

#### Language
- English (default)
- Spanish
- French
- German

#### Notifications
- Enable/disable notifications
- Email alerts toggle

#### Auto-save
- Enable/disable auto-save

#### Session Timeout
- 15 minutes
- 30 minutes (default)
- 60 minutes
- 120 minutes

### Theme Toggle

Switch between:
- Light mode (default)
- Dark mode

### Logout

Securely end your session:
- Click logout button
- Session is invalidated
- Redirected to login page

---

## Role-Based Features

### User Role (Default)
- Content analysis
- Content generation
- Content transformation
- View monitoring
- View alerts
- ❌ No security dashboard access

### Creator Role
- All User role features
- Enhanced content creation tools
- ❌ No security dashboard access

### Admin Role
- All User role features
- All Creator role features
- ✅ Security dashboard access
- User management capabilities
- System configuration

---

## Keyboard Shortcuts

- `Ctrl + /`: Focus search
- `Esc`: Close dialogs
- `Enter`: Submit forms

---

## Tips & Best Practices

### Content Analysis
- Longer content provides better analysis
- Use clear, well-structured text
- Check quality score for improvement areas

### Content Transformation
- Be specific with tone selection
- Review character counts for platform limits
- Use hashtags strategically

### Security
- Change default passwords
- Monitor login activity regularly
- Review security events

### Performance
- Clear old data periodically
- Monitor system metrics
- Report unusual patterns

---

## Coming Soon Features

These features will be available in future updates:

1. **Audio Analysis**: Transcription and content analysis
2. **Image Analysis**: OCR and visual content analysis
3. **Video Analysis**: Transcription and video content analysis
4. **Document Analysis**: PDF and document parsing
5. **Image Generation**: AI-powered image creation
6. **Video Generation**: AI-powered video creation
7. **Advanced Analytics**: Detailed reporting and insights
8. **API Access**: Programmatic access to features
9. **Batch Processing**: Process multiple files at once
10. **Export Options**: Export data in various formats

---

## Support & Feedback

For questions or issues:
1. Check SETUP.md for configuration help
2. Review this documentation
3. Check console logs for errors
4. Verify API key configuration
